from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field

import numpy as np
import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String

from acare_bringup.paths import SYSTEM_YAML
from acare_bringup.qos_profiles import TOPIC_VOICE_PIPELINE, TOPIC_TTS, TOPIC_STATE, TOPIC_SENSOR
from acare_msgs.msg import AuthRequest, AuthResult, Intent, RobotState, StateTransition, Transcript, ValidatedIntent
from acare_msgs.srv import EnrolStaff

from .face_detect import PassiveFaceDetector
from .storage import UserStore
from .verify_face import FaceVerifier
from .verify_voice import VoiceVerifier


@dataclass
class PendingLogin:
    user_id: str
    name: str
    role: str
    face_confidence: float
    created_at: float


@dataclass
class PendingIntent:
    tool: str
    action: str
    confidence: float


@dataclass
class PendingEnrollment:
    name: str
    role: str
    created_at: float
    deadline_at: float
    face_embeddings: list[np.ndarray] = field(default_factory=list)
    voice_embeddings: list[np.ndarray] = field(default_factory=list)
    last_face_capture_at: float = 0.0
    last_voice_capture_at: float = 0.0
    cancelled: bool = False
    failure_reason: str = ""


class AuthNode(Node):
    LOGIN_PROMPT_COOLDOWN_S = 5.0
    ENROL_TIMEOUT_S = 25.0
    ENROL_FACE_SAMPLE_PERIOD_S = 0.15
    ENROL_VOICE_SAMPLE_PERIOD_S = 0.60
    ENROL_START_AUDIO_GUARD_S = 2.0
    ENROL_MIN_AUDIO_SAMPLES = 12_000
    ALLOWED_ROLES = {"surgeon", "nurse", "admin"}

    def __init__(self):
        super().__init__("auth_node")
        self._io_group = ReentrantCallbackGroup()
        self.validated_pub = self.create_publisher(ValidatedIntent, "/validated_intent", TOPIC_VOICE_PIPELINE)
        self.auth_pub = self.create_publisher(AuthResult, "/auth_result", TOPIC_VOICE_PIPELINE)
        self.tts_pub = self.create_publisher(String, "/tts_request", TOPIC_TTS)
        self.transition_pub = self.create_publisher(StateTransition, "/state_transition", TOPIC_STATE)
        self.create_subscription(Intent, "/intent_result", self._on_intent, TOPIC_VOICE_PIPELINE, callback_group=self._io_group)
        self.create_subscription(AuthRequest, "/auth_request", self._on_auth_request, TOPIC_VOICE_PIPELINE, callback_group=self._io_group)
        self.create_subscription(Transcript, "/raw_transcript", self._on_transcript, TOPIC_VOICE_PIPELINE, callback_group=self._io_group)
        self.create_subscription(RobotState, "/robot_state", self._on_robot_state, TOPIC_STATE, callback_group=self._io_group)
        self.create_subscription(
            Image,
            "/ascamera_hp60c/camera_publisher/rgb0/image",
            self._on_rgb,
            TOPIC_SENSOR,
            callback_group=self._io_group,
        )
        # Gazebo bridge publishes RGB as /camera/rgb — accept both so the same
        # auth_node code works on real hardware (HP60C) and in simulation.
        self.create_subscription(
            Image,
            "/camera/rgb",
            self._on_rgb,
            TOPIC_SENSOR,
            callback_group=self._io_group,
        )
        self.create_service(EnrolStaff, "/enrol_staff", self._on_enrol, callback_group=self._io_group)

        self.store = UserStore()
        self.face_detector = PassiveFaceDetector()
        self.face_verifier = FaceVerifier()
        self.voice_verifier = VoiceVerifier()

        system_cfg = self._load_system_config()
        auth_cfg = system_cfg.get("auth", {}) if isinstance(system_cfg, dict) else {}
        self._robot_state = "LOGGED_OUT"
        self._demo_mode = bool(system_cfg.get("demo_mode", False)) if isinstance(system_cfg, dict) else False
        self._enrol_voice_samples = max(1, int(auth_cfg.get("enrol_voice_samples", 3)))
        self._enrol_face_frames = max(1, int(auth_cfg.get("enrol_face_frames", 10)))
        self._pending_login: PendingLogin | None = None
        self._pending_intent: PendingIntent | None = None
        self._pending_enrolment: PendingEnrollment | None = None
        self._active_user_id = ""
        self._active_user_name = ""
        self._active_user_role = ""
        self._latest_rgb = None
        self._last_face_similarity = 0.0
        self._last_face_seen_at = 0.0
        self._voice_drift_failures = 0
        self._awaiting_reconfirm = False
        self._last_prompted_user_id = ""
        self._last_login_prompt_at = 0.0
        self._last_voice_check_ok = True
        self._last_voice_check_confidence = 0.0
        self._last_voice_check_at = 0.0
        self._enrol_condition = threading.Condition()

        if hasattr(self.voice_verifier, "THRESHOLD"):
            self.voice_verifier.THRESHOLD = float(auth_cfg.get("voice_similarity_threshold", self.voice_verifier.THRESHOLD))
        if hasattr(self.face_verifier, "THRESHOLD"):
            self.face_verifier.THRESHOLD = float(auth_cfg.get("face_similarity_threshold", self.face_verifier.THRESHOLD))

        self.create_timer(0.5, self._passive_face_scan)
        self.create_timer(0.5, self._handover_face_check)
        self.create_timer(10.0, self._session_timeout_check)
        self._last_activity_at = time.monotonic()
        self._session_timeout_s = 300.0
        self.get_logger().info(
            f"Auth node ready demo_mode={self._demo_mode} "
            f"face_backend={self.face_verifier.available} voice_backend={self.voice_verifier.available}"
        )
        if not self._demo_mode and not self.face_detector.available:
            self.get_logger().error("Passive face detector unavailable. Install MediaPipe for always-on login scan.")
        if not self._demo_mode and not self.face_verifier.available:
            self.get_logger().error("Face verification backend unavailable. Install insightface and camera dependencies.")
        if not self._demo_mode and not self.voice_verifier.available:
            self.get_logger().error("Voice verification backend unavailable. Install SpeechBrain and torch runtime dependencies.")

    def _load_system_config(self) -> dict:
        try:
            import yaml

            with open(SYSTEM_YAML, "r", encoding="utf-8") as handle:
                return yaml.safe_load(handle) or {}
        except Exception:
            return {}

    def _publish_tts(self, text: str):
        self.tts_pub.publish(String(data=text))

    def _maybe_prompt(self, text: str, cooldown_s: float = LOGIN_PROMPT_COOLDOWN_S):
        now = time.monotonic()
        if (now - self._last_login_prompt_at) < cooldown_s:
            return
        self._last_login_prompt_at = now
        self._publish_tts(text)

    def _transition_state(self, target: str, reason: str):
        msg = StateTransition()
        msg.target_state = target
        msg.reason = reason
        self.transition_pub.publish(msg)

    def _publish_auth(self, success: bool, user_id: str, name: str, role: str, face_verified: bool, face_conf: float, voice_conf: float):
        msg = AuthResult()
        msg.user_id = user_id
        msg.name = name
        msg.role = role
        msg.success = success
        msg.face_verified = face_verified
        msg.face_confidence = float(face_conf)
        msg.voice_confidence = float(voice_conf)
        self.auth_pub.publish(msg)

    def _publish_validated_intent(self, pending: PendingIntent):
        msg = ValidatedIntent()
        msg.tool = pending.tool
        msg.action = pending.action
        msg.user_id = self._active_user_id
        msg.name = self._active_user_name
        msg.authenticated = True
        self.validated_pub.publish(msg)

    def _activate_session(self, user_id: str, name: str, role: str):
        self._active_user_id = user_id
        self._active_user_name = name
        self._active_user_role = role
        self._voice_drift_failures = 0
        self._awaiting_reconfirm = False
        self._last_prompted_user_id = ""
        self._last_voice_check_ok = True
        self._last_voice_check_confidence = 0.0
        self._last_voice_check_at = 0.0

    def _logout(self, publish_transition: bool = True):
        self._active_user_id = ""
        self._active_user_name = ""
        self._active_user_role = ""
        self._pending_login = None
        self._pending_intent = None
        self._voice_drift_failures = 0
        self._awaiting_reconfirm = False
        self._last_voice_check_ok = True
        self._last_voice_check_confidence = 0.0
        self._last_voice_check_at = 0.0
        if publish_transition:
            self._transition_state("LOGGED_OUT", "auth_logout")

    def _normalise_embedding_mean(self, embeddings: list[np.ndarray]) -> np.ndarray | None:
        if not embeddings:
            return None
        stacked = np.vstack([np.asarray(emb, dtype=np.float32) for emb in embeddings])
        mean = stacked.mean(axis=0).astype(np.float32)
        norm = float(np.linalg.norm(mean))
        if not np.isfinite(norm) or norm < 1e-6:
            return None
        return mean / norm

    def _find_best_face_match(self):
        users = self.store.all_active()
        if not users:
            return None, 0.0

        if self._demo_mode or not self.face_verifier.available or self._latest_rgb is None:
            best = users[-1]
            return best, 0.99

        import cv2
        bgr_frame = cv2.cvtColor(self._latest_rgb, cv2.COLOR_RGB2BGR)

        best_user = None
        best_sim = 0.0
        for user in users:
            if user.face_emb is None:
                continue
            matched, sim = self.face_verifier.verify(bgr_frame, user.face_emb)
            if sim > best_sim:
                best_sim = sim
                best_user = user
            if matched:
                break
        return best_user, best_sim

    def _passive_face_scan(self):
        if self._robot_state != "LOGGED_OUT" or self._pending_login is not None or self._pending_enrolment is not None:
            return
        if self._active_user_id:
            return

        # Demo mode: don't require a camera frame. If at least one user is
        # enrolled, auto-prompt them. If none are enrolled, auto-create a
        # default demo user so the pipeline can be exercised end-to-end.
        if self._demo_mode:
            users = self.store.all_active()
            if not users:
                try:
                    self.store.enrol(
                        name="Demo User",
                        role="surgeon",
                        voice_emb=None,
                        face_emb=None,
                    )
                    users = self.store.all_active()
                except Exception as exc:
                    self.get_logger().warn(f"Demo auto-enrol failed: {exc}")
                    return
            if not users:
                return
            user = users[-1]
            self._pending_login = PendingLogin(
                user_id=user.user_id,
                name=user.name,
                role=user.role,
                face_confidence=0.99,
                created_at=time.monotonic(),
            )
            self._last_prompted_user_id = user.user_id
            self._maybe_prompt(f"Welcome {user.name}. Say confirm to log in.")
            return

        if self._latest_rgb is None:
            return

        face_present = self.face_detector.face_present(self._latest_rgb) if self.face_detector.available else True
        if not face_present and not self._demo_mode:
            return

        user, sim = self._find_best_face_match()
        if user is None:
            return
        self._pending_login = PendingLogin(
            user_id=user.user_id,
            name=user.name,
            role=user.role,
            face_confidence=sim,
            created_at=time.monotonic(),
        )
        self._last_prompted_user_id = user.user_id
        self._maybe_prompt(f"Welcome {user.name}. Say confirm to log in.")

    def _handover_face_check(self):
        if self._robot_state != "HANDOVER" or not self._active_user_id:
            return
        user = self.store.get(self._active_user_id)
        if user is None:
            return

        if self._demo_mode or not self.face_verifier.available or self._latest_rgb is None or user.face_emb is None:
            self._last_face_similarity = 0.99
            self._publish_auth(True, user.user_id, user.name, user.role, True, 0.99, 0.99)
            return

        import cv2
        bgr_frame = cv2.cvtColor(self._latest_rgb, cv2.COLOR_RGB2BGR)
        matched, sim = self.face_verifier.verify(bgr_frame, user.face_emb)
        self._last_face_similarity = sim
        self._publish_auth(matched, user.user_id, user.name, user.role, matched, sim, 0.99)

    def _runtime_voice_check(self):
        if not self._active_user_id:
            return
        if self._last_voice_check_ok:
            self._voice_drift_failures = 0
            return
        self._voice_drift_failures += 1
        if self._voice_drift_failures >= 3 and not self._awaiting_reconfirm:
            self._awaiting_reconfirm = True
            self._publish_tts("Having trouble recognising your voice. Please re-confirm identity.")

    def _session_timeout_check(self):
        if not self._active_user_id:
            return
        if self._robot_state in {"ESTOP", "HOLDING", "HANDOVER"}:
            self._last_activity_at = time.monotonic()
            return
        elapsed = time.monotonic() - self._last_activity_at
        if elapsed > self._session_timeout_s:
            self.get_logger().info(
                f"Session timeout after {elapsed:.0f}s of inactivity for {self._active_user_name}"
            )
            self._publish_tts("Session timed out due to inactivity. Please log in again.")
            self._logout()

    def _transcript_to_audio_tensor(self, msg: Transcript):
        if msg.pcm16 is None or int(msg.sample_rate_hz) != 16000:
            return None
        try:
            import torch
            arr = np.asarray(msg.pcm16, dtype=np.int16)
            if arr.size == 0:
                return None
            audio_np = arr.astype(np.float32) / 32767.0
            if not np.isfinite(audio_np).all():
                return None
            return torch.from_numpy(audio_np)
        except Exception:
            return None

    def _sample_enrolment_voice(self, msg: Transcript, text: str):
        pending = self._pending_enrolment
        if pending is None or not self.voice_verifier.available or not msg.is_final or not text:
            return
        now = time.monotonic()
        with self._enrol_condition:
            pending = self._pending_enrolment
            if pending is None or pending.cancelled or pending.failure_reason:
                return
            if len(pending.voice_embeddings) >= self._enrol_voice_samples:
                return
            if (now - pending.last_voice_capture_at) < self.ENROL_VOICE_SAMPLE_PERIOD_S:
                return
            pending.last_voice_capture_at = now

        audio_tensor = self._transcript_to_audio_tensor(msg)
        if audio_tensor is None or int(audio_tensor.numel()) < self.ENROL_MIN_AUDIO_SAMPLES:
            return
        voice_emb = self.voice_verifier.embed(audio_tensor)
        if voice_emb is None:
            return

        with self._enrol_condition:
            pending = self._pending_enrolment
            if pending is None or pending.cancelled or pending.failure_reason:
                return
            if len(pending.voice_embeddings) >= self._enrol_voice_samples:
                return
            pending.voice_embeddings.append(np.asarray(voice_emb, dtype=np.float32))
            self._enrol_condition.notify_all()

    def _bootstrap_voice_embedding(self, user_id: str, msg: Transcript) -> bool:
        user = self.store.get(user_id)
        if user is None or not self.voice_verifier.available:
            return False
        audio_tensor = self._transcript_to_audio_tensor(msg)
        if audio_tensor is None:
            return False
        voice_emb = self.voice_verifier.embed(audio_tensor)
        if voice_emb is None:
            return False
        self.store.update_voice_embedding(user.user_id, voice_emb)
        return True

    def _verify_runtime_voice(self, msg: Transcript):
        self._last_voice_check_ok = True
        self._last_voice_check_confidence = 0.0
        self._last_voice_check_at = time.monotonic()
        if not self._active_user_id or not self.voice_verifier.available:
            return
        user = self.store.get(self._active_user_id)
        if user is None or user.voice_emb is None:
            return
        audio_tensor = self._transcript_to_audio_tensor(msg)
        if audio_tensor is None:
            return
        ok, sim = self.voice_verifier.verify(audio_tensor, user.voice_emb)
        self._last_voice_check_ok = ok
        self._last_voice_check_confidence = sim

    def _resolve_pending_intent(self):
        if self._pending_intent is None or not self._active_user_id:
            return
        pending = self._pending_intent
        self._pending_intent = None
        self._publish_validated_intent(pending)

    def _on_rgb(self, msg: Image):
        try:
            arr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)
            self._latest_rgb = arr.copy()
            self._last_face_seen_at = time.monotonic()
        except Exception:
            self._latest_rgb = None
            return

        if not self.face_verifier.available:
            return

        import cv2
        bgr_frame = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

        now = time.monotonic()
        with self._enrol_condition:
            pending = self._pending_enrolment
            if pending is None or pending.cancelled or pending.failure_reason:
                return
            if len(pending.face_embeddings) >= self._enrol_face_frames:
                return
            if (now - pending.last_face_capture_at) < self.ENROL_FACE_SAMPLE_PERIOD_S:
                return
            pending.last_face_capture_at = now

        face_emb = self.face_verifier.embed(bgr_frame)
        if face_emb is None:
            return

        with self._enrol_condition:
            pending = self._pending_enrolment
            if pending is None or pending.cancelled or pending.failure_reason:
                return
            if len(pending.face_embeddings) >= self._enrol_face_frames:
                return
            pending.face_embeddings.append(np.asarray(face_emb, dtype=np.float32))
            self._enrol_condition.notify_all()

    def _on_robot_state(self, msg: RobotState):
        self._robot_state = msg.state
        if msg.state == "LOGGED_OUT":
            self._logout(publish_transition=False)
        if msg.active_user_id and msg.active_user_id != self._active_user_id:
            user = self.store.get(msg.active_user_id)
            if user:
                self._activate_session(user.user_id, user.name, user.role)

    def _on_enrol(self, request: EnrolStaff.Request, response: EnrolStaff.Response):
        name = (request.name or "").strip()
        role = (request.role or "").strip().lower()
        if not name:
            response.success = False
            response.staff_id = ""
            response.message = "Name is required."
            return response
        if role not in self.ALLOWED_ROLES:
            response.success = False
            response.staff_id = ""
            response.message = f"Role must be one of: {', '.join(sorted(self.ALLOWED_ROLES))}."
            return response
        if self._robot_state not in {"LOGGED_OUT", "STANDBY"}:
            response.success = False
            response.staff_id = ""
            response.message = f"Cannot enrol while robot state is {self._robot_state}."
            return response
        if not self._demo_mode and not self.face_verifier.available:
            response.success = False
            response.staff_id = ""
            response.message = "Face verification backend unavailable. Install insightface before enrolment."
            return response
        if not self._demo_mode and not self.voice_verifier.available:
            response.success = False
            response.staff_id = ""
            response.message = "Voice verification backend unavailable. Install SpeechBrain before enrolment."
            return response
        face_target = self._enrol_face_frames if self.face_verifier.available else 0
        voice_target = self._enrol_voice_samples if self.voice_verifier.available else 0

        pending = PendingEnrollment(
            name=name,
            role=role,
            created_at=time.monotonic(),
            deadline_at=time.monotonic() + self.ENROL_TIMEOUT_S,
            last_voice_capture_at=time.monotonic() + self.ENROL_START_AUDIO_GUARD_S,
        )
        with self._enrol_condition:
            if self._pending_enrolment is not None:
                response.success = False
                response.staff_id = ""
                response.message = "Another enrolment is already in progress."
                return response
            self._pending_enrolment = pending

        if face_target and voice_target:
            prompt = f"Starting enrolment for {name}. Please face the camera and say {voice_target} short phrases clearly."
        elif face_target:
            prompt = f"Starting enrolment for {name}. Please face the camera for biometric capture."
        elif voice_target:
            prompt = f"Starting enrolment for {name}. Please say {voice_target} short phrases clearly."
        else:
            prompt = f"Starting enrolment for {name} in demo mode."
        self._publish_tts(prompt)
        self.get_logger().info(
            f"Enrolment started for {name} role={role} "
            f"voice_target={voice_target} face_target={face_target}"
        )

        def _background_enrol():
            try:
                while True:
                    with self._enrol_condition:
                        current = self._pending_enrolment
                        if current is None:
                            break
                        if current.cancelled:
                            return
                        if current.failure_reason:
                            return
                        face_done = len(current.face_embeddings) >= face_target
                        voice_done = len(current.voice_embeddings) >= voice_target
                        if face_done and voice_done:
                            break
                        remaining = current.deadline_at - time.monotonic()
                        if remaining <= 0.0:
                            break
                        self._enrol_condition.wait(timeout=min(0.5, remaining))

                with self._enrol_condition:
                    current = self._pending_enrolment
                    self._pending_enrolment = None

                face_count = len(pending.face_embeddings)
                voice_count = len(pending.voice_embeddings)
                if face_count < face_target or voice_count < voice_target:
                    msg = "Enrolment timed out before capturing required biometrics. Please try again."
                    self.get_logger().warn(msg)
                    self._publish_tts(msg)
                    return

                face_emb = self._normalise_embedding_mean(pending.face_embeddings) if face_target else None
                voice_emb = self._normalise_embedding_mean(pending.voice_embeddings) if voice_target else None
                if (face_target and face_emb is None) or (voice_target and voice_emb is None):
                    msg = "Failed to process enrolment biometrics. Please try again."
                    self.get_logger().warn(msg)
                    self._publish_tts(msg)
                    return

                record = self.store.enrol(name, role, voice_emb=voice_emb, face_emb=face_emb)
                self.get_logger().info(f"Enrolment completed for {record.user_id} in background.")
            finally:
                with self._enrol_condition:
                    if self._pending_enrolment is pending:
                        self._pending_enrolment = None

        threading.Thread(target=_background_enrol, daemon=True).start()
        
        response.success = True
        response.staff_id = ""
        response.message = f"Enrolment started for {name}. Please follow voice prompts."
        return response

    def _on_intent(self, msg: Intent):
        if self._robot_state == "ESTOP":
            self.get_logger().warn("Ignoring intent because robot is in ESTOP.")
            return
        if self._pending_enrolment is not None:
            self.get_logger().warn("Ignoring intent while enrolment is in progress.")
            return
        action = (msg.action or "").lower()
        if action == "logout":
            if self._robot_state in {"HOLDING", "HANDOVER"}:
                self._publish_tts("Cannot log out while holding a tool.")
                return
            self._logout()
            return
        if action != "fetch":
            return

        self._pending_intent = PendingIntent(tool=msg.tool, action=msg.action, confidence=msg.confidence)
        if self._active_user_id:
            recent_voice_window_s = 5.0
            if (
                self.voice_verifier.available
                and (time.monotonic() - self._last_voice_check_at) <= recent_voice_window_s
                and not self._last_voice_check_ok
            ):
                self._runtime_voice_check()
                self._publish_tts(f"Command not processed. Only {self._active_user_name} can issue commands.")
                return
            self._runtime_voice_check()
            self._resolve_pending_intent()
        elif self._pending_login is None:
            self._maybe_prompt("Authentication required. Please face the camera and say confirm.")

    def _on_auth_request(self, msg: AuthRequest):
        if msg.request_type == "validate_intent" and msg.tool and self._pending_intent is None:
            self._pending_intent = PendingIntent(tool=msg.tool, action="fetch", confidence=msg.confidence)

    def _on_transcript(self, msg: Transcript):
        if self._robot_state == "ESTOP":
            return
        self._last_activity_at = time.monotonic()
        text = (msg.text or "").strip().lower()
        if self._pending_enrolment is not None:
            if text in {"cancel", "abort", "stop enrolment", "stop enrollment"}:
                with self._enrol_condition:
                    if self._pending_enrolment is not None:
                        self._pending_enrolment.cancelled = True
                        self._pending_enrolment.failure_reason = "Enrolment cancelled by operator voice command."
                        self._enrol_condition.notify_all()
                return
            self._sample_enrolment_voice(msg, text)
        if not text:
            return

        if self._active_user_id:
            self._verify_runtime_voice(msg)

        if text in {"logout", "log out"}:
            self._logout()
            return

        if text in {"confirm", "yes", "go ahead", "login", "log in"} and self._pending_login is not None:
            pending = self._pending_login
            user = self.store.get(pending.user_id)
            voice_conf = 0.99 if self._demo_mode else 0.0
            if user is not None and self.voice_verifier.available:
                audio_tensor = self._transcript_to_audio_tensor(msg)
                if user.voice_emb is not None and audio_tensor is not None:
                    ok, voice_conf = self.voice_verifier.verify(audio_tensor, user.voice_emb)
                    if not ok:
                        self._pending_login = pending
                        self._publish_tts("Identity not recognised. Please contact admin.")
                        return
                elif user.voice_emb is not None and audio_tensor is None and not self._demo_mode:
                    self._pending_login = pending
                    self._maybe_prompt("Please say confirm again.", cooldown_s=1.0)
                    return
                elif audio_tensor is not None:
                    self._pending_login = pending
                    self._publish_tts(
                        "Voice template not enrolled. Please contact admin to complete voice enrolment."
                    )
                    return
            self._pending_login = None
            self._activate_session(pending.user_id, pending.name, pending.role)
            self._publish_auth(
                True,
                pending.user_id,
                pending.name,
                pending.role,
                True,
                pending.face_confidence,
                voice_conf if self.voice_verifier.available else 0.99,
            )
            self._transition_state("STANDBY", f"login_{pending.user_id}")
            self._publish_tts(f"Logged in as {pending.name}. How can I assist?")
            self._resolve_pending_intent()
            return

        if self._awaiting_reconfirm and text in {"confirm", "yes"} and self._active_user_id:
            if not self._last_voice_check_ok:
                self._publish_tts("Voice verification failed. Please try again.")
                return
            self._awaiting_reconfirm = False
            self._voice_drift_failures = 0
            self._publish_tts("Identity reconfirmed.")
            self._resolve_pending_intent()
            return

        if self._robot_state == "HANDOVER" and self._active_user_id:
            if text in {"lower", "higher"}:
                user = self.store.get(self._active_user_id)
                if user:
                    delta = -0.05 if text == "lower" else 0.05
                    self.store.update_handover_offset(user.user_id, user.handover_z_offset + delta)


def main(args=None):
    rclpy.init(args=args)
    node = AuthNode()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

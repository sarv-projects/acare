from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String

from acare_bringup.paths import SYSTEM_YAML
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


class AuthNode(Node):
    LOGIN_PROMPT_COOLDOWN_S = 5.0

    def __init__(self):
        super().__init__("auth_node")
        self.validated_pub = self.create_publisher(ValidatedIntent, "/validated_intent", 10)
        self.auth_pub = self.create_publisher(AuthResult, "/auth_result", 10)
        self.tts_pub = self.create_publisher(String, "/tts_request", 10)
        self.transition_pub = self.create_publisher(StateTransition, "/state_transition", 10)
        self.create_subscription(Intent, "/intent_result", self._on_intent, 10)
        self.create_subscription(AuthRequest, "/auth_request", self._on_auth_request, 10)
        self.create_subscription(Transcript, "/raw_transcript", self._on_transcript, 10)
        self.create_subscription(RobotState, "/robot_state", self._on_robot_state, 10)
        self.create_subscription(Image, "/ascamera_hp60c/camera_publisher/rgb0/image", self._on_rgb, 10)
        self.create_service(EnrolStaff, "/enrol_staff", self._on_enrol)

        self.store = UserStore()
        self.face_detector = PassiveFaceDetector()
        self.face_verifier = FaceVerifier()
        self.voice_verifier = VoiceVerifier()

        self._robot_state = "LOGGED_OUT"
        self._demo_mode = self._load_demo_mode()
        self._pending_login: PendingLogin | None = None
        self._pending_intent: PendingIntent | None = None
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

        self.create_timer(0.5, self._passive_face_scan)
        self.create_timer(0.5, self._handover_face_check)
        self.get_logger().info(
            f"Auth node ready demo_mode={self._demo_mode} "
            f"face_backend={self.face_verifier.available} voice_backend={self.voice_verifier.available}"
        )

    def _load_demo_mode(self) -> bool:
        try:
            import yaml

            with open(SYSTEM_YAML, "r", encoding="utf-8") as handle:
                cfg = yaml.safe_load(handle) or {}
            return bool(cfg.get("demo_mode", False))
        except Exception:
            return False

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

    def _find_best_face_match(self):
        users = self.store.all_active()
        if not users:
            return None, 0.0

        if self._demo_mode or not self.face_verifier.available or self._latest_rgb is None:
            best = users[-1]
            return best, 0.99

        best_user = None
        best_sim = 0.0
        for user in users:
            if user.face_emb is None:
                continue
            matched, sim = self.face_verifier.verify(self._latest_rgb, user.face_emb)
            if sim > best_sim:
                best_sim = sim
                best_user = user
            if matched:
                break
        return best_user, best_sim

    def _passive_face_scan(self):
        if self._robot_state != "LOGGED_OUT" or self._pending_login is not None:
            return
        if self._active_user_id:
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

        matched, sim = self.face_verifier.verify(self._latest_rgb, user.face_emb)
        self._last_face_similarity = sim
        self._publish_auth(True, user.user_id, user.name, user.role, matched, sim, 0.99)

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

    def _transcript_to_audio_tensor(self, msg: Transcript):
        if not msg.pcm16 or int(msg.sample_rate_hz) != 16000:
            return None
        try:
            import torch

            audio_np = np.asarray(msg.pcm16, dtype=np.int16).astype(np.float32) / 32767.0
            if audio_np.size == 0 or not np.isfinite(audio_np).all():
                return None
            return torch.from_numpy(audio_np)
        except Exception:
            return None

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

    def _on_robot_state(self, msg: RobotState):
        self._robot_state = msg.state
        if msg.state == "LOGGED_OUT":
            self._logout(publish_transition=False)
        if msg.active_user_id and msg.active_user_id != self._active_user_id:
            user = self.store.get(msg.active_user_id)
            if user:
                self._activate_session(user.user_id, user.name, user.role)

    def _on_enrol(self, request: EnrolStaff.Request, response: EnrolStaff.Response):
        face_emb = None
        if self.face_verifier.available and self._latest_rgb is not None:
            face_emb = self.face_verifier.embed(self._latest_rgb)
        record = self.store.enrol(request.name, request.role, voice_emb=None, face_emb=face_emb)
        response.success = True
        response.staff_id = record.user_id
        response.message = "Enrolment stored. Voice embedding capture awaits audio-sample integration."
        return response

    def _on_intent(self, msg: Intent):
        action = (msg.action or "").lower()
        if action == "logout":
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
                self._pending_intent = None
                return
            self._runtime_voice_check()
            self._resolve_pending_intent()
        elif self._pending_login is None:
            self._maybe_prompt("Authentication required. Please face the camera and say confirm.")

    def _on_auth_request(self, msg: AuthRequest):
        if msg.request_type == "validate_intent" and msg.tool and self._pending_intent is None:
            self._pending_intent = PendingIntent(tool=msg.tool, action="fetch", confidence=msg.confidence)

    def _on_transcript(self, msg: Transcript):
        text = (msg.text or "").strip().lower()
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
                    if self._bootstrap_voice_embedding(pending.user_id, msg):
                        voice_conf = 0.85
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
            self._awaiting_reconfirm = False
            self._voice_drift_failures = 0
            self._publish_tts("Identity reconfirmed.")
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
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from acare_bringup.paths import SYSTEM_YAML
from acare_msgs.msg import (
    ArmCommand,
    AuthResult,
    GripperCommand,
    HandStatus,
    LogEvent,
    MotionFeedback,
    RobotState,
    SafetyAlert,
    StateTransition,
    Transcript,
    ValidatedIntent,
    VisionResult,
    VisionSearchRequest,
    VisionStatus,
)

from .ik_solver import IKSolver
from .agent_schema import (
    AbortCommand,
    ArmMoveCommand,
    GripperCommandSchema,
    SafeDepositCommand,
    SpeechCommand,
    TransitionCommand,
    VisionSearchCommand,
)

MAX_RETRIES = 3
HANDOVER_TIMEOUT_S = 30.0


@dataclass
class WorldState:
    robot_state: str = "LOGGED_OUT"
    active_user_id: str = ""
    safety_severity: str = ""
    vision_status: str = "UNKNOWN"
    network_ok: bool = True
    arm_holding: bool = False
    gripper_force: float = 0.0


@dataclass
class TaskContext:
    tool: str = ""
    user_id: str = ""
    user_name: str = ""
    pipeline_start: float = 0.0
    vision_start: float = 0.0
    motion_start: float = 0.0
    grasp_point: tuple[float, float, float] | None = None
    detection_candidates: list[dict] = field(default_factory=list)
    alternate_orientation_tried: bool = False
    vision_retries: int = 0
    grasp_retries: int = 0
    face_retries: int = 0


class PlannerNode(Node):
    def __init__(self):
        super().__init__("planner_node")
        self.world = WorldState()
        self.context = TaskContext()
        self.ik = IKSolver()

        self.search_pub = self.create_publisher(VisionSearchRequest, "/vision_search_request", 10)
        self.transition_pub = self.create_publisher(StateTransition, "/state_transition", 10)
        self.arm_pub = self.create_publisher(ArmCommand, "/arm_command", 10)
        self.gripper_pub = self.create_publisher(GripperCommand, "/gripper_command", 10)
        self.tts_pub = self.create_publisher(String, "/tts_request", 10)
        self.log_pub = self.create_publisher(LogEvent, "/log_event", 10)

        self.create_subscription(ValidatedIntent, "/validated_intent", self._on_validated_intent, 10)
        self.create_subscription(VisionResult, "/vision_result", self._on_vision_result, 10)
        self.create_subscription(MotionFeedback, "/motion_feedback", self._on_motion_feedback, 10)
        self.create_subscription(HandStatus, "/hand_status", self._on_hand_status, 10)
        self.create_subscription(SafetyAlert, "/safety_alert", self._on_safety_alert, 10)
        self.create_subscription(RobotState, "/robot_state", self._on_robot_state, 10)
        self.create_subscription(AuthResult, "/auth_result", self._on_auth_result, 10)
        self.create_subscription(Transcript, "/raw_transcript", self._on_transcript, 10)
        self.create_subscription(VisionStatus, "/vision_status", self._on_vision_status, 10)

        self._lock = threading.Lock()
        self._task_thread = None
        self._vision_event = threading.Event()
        self._motion_event = threading.Event()
        self._auth_face_event = threading.Event()
        self._latest_vision_result: VisionResult | None = None
        self._motion_success = False
        self._latest_hand_status: HandStatus | None = None
        self._face_verified = False
        self._face_skipped = False
        self._voice_confirm_word = ""
        self._handover_height_adjustment = 0.0
        self._safe_drop_zone, self._handover_zone = self._load_robot_points()
        self.get_logger().info("Planner node ready")

    def _load_robot_points(self):
        try:
            import yaml

            with open(SYSTEM_YAML, "r", encoding="utf-8") as handle:
                cfg = yaml.safe_load(handle) or {}
            robot = cfg.get("robot", {})
            drop = robot.get("safe_drop_zone", {"x": 0.0, "y": 0.35, "z": 0.05})
            hand = robot.get("handover_zone", {"x": 0.0, "y": 0.40, "z": 0.10})
            return (
                (float(drop["x"]), float(drop["y"]), float(drop["z"])),
                (float(hand["x"]), float(hand["y"]), float(hand["z"])),
            )
        except Exception:
            return (0.0, 0.35, 0.05), (0.0, 0.40, 0.10)

    def _speak(self, text: str):
        cmd = SpeechCommand(text=text)
        self.tts_pub.publish(String(data=cmd.text))

    def _transition_state(self, target: str, reason: str):
        cmd = TransitionCommand(target_state=target, reason=reason)
        msg = StateTransition()
        msg.target_state = cmd.target_state
        msg.reason = cmd.reason
        self.transition_pub.publish(msg)

    def _log_event(self, event_type: str, tool: str = "", description: str = ""):
        msg = LogEvent()
        msg.event_type = event_type
        msg.user_id = self.context.user_id
        msg.tool = tool or self.context.tool
        msg.state = self.world.robot_state
        msg.description = description
        msg.timestamp = int(time.time() * 1000)
        msg.voice_e2e_ms = 0
        msg.vision_search_ms = int((time.monotonic() - self.context.vision_start) * 1000) if self.context.vision_start else 0
        msg.motion_ms = int((time.monotonic() - self.context.motion_start) * 1000) if self.context.motion_start else 0
        msg.total_task_ms = int((time.monotonic() - self.context.pipeline_start) * 1000) if self.context.pipeline_start else 0
        msg.safety_severity = self.world.safety_severity
        self.log_pub.publish(msg)

    def _on_validated_intent(self, msg: ValidatedIntent):
        with self._lock:
            if self._task_thread and self._task_thread.is_alive():
                self._speak("Task already in progress.")
                return
            self.context = TaskContext(
                tool=msg.tool,
                user_id=msg.user_id,
                user_name=msg.name,
                pipeline_start=time.monotonic(),
            )
            self._task_thread = threading.Thread(
                target=self._execute_fetch_task,
                args=(msg.tool, msg.user_id, msg.name),
                daemon=True,
            )
            self._task_thread.start()

    def _on_vision_result(self, msg: VisionResult):
        self._latest_vision_result = msg
        self._vision_event.set()

    def _on_motion_feedback(self, msg: MotionFeedback):
        self.world.gripper_force = float(msg.gripper_force)
        self.world.arm_holding = self.world.gripper_force > 0.5 or self.world.arm_holding
        self._motion_success = bool(msg.success)
        self._motion_event.set()

    def _on_hand_status(self, msg: HandStatus):
        self._latest_hand_status = msg

    def _on_safety_alert(self, msg: SafetyAlert):
        self.world.safety_severity = msg.severity
        self._log_event("SAFETY_ALERT", description=f"{msg.source}: {msg.reason}")
        if msg.severity == "ESTOP":
            self._handle_estop(msg.reason)

    def _on_robot_state(self, msg: RobotState):
        self.world.robot_state = msg.state
        self.world.active_user_id = msg.active_user_id

    def _on_auth_result(self, msg: AuthResult):
        if self.context.user_id and msg.user_id == self.context.user_id:
            self._face_verified = bool(msg.face_verified)
            if msg.face_verified:
                self._auth_face_event.set()

    def _on_transcript(self, msg: Transcript):
        word = (msg.text or "").strip().lower()
        if word in {"take", "yes", "got it", "ok", "okay"}:
            self._voice_confirm_word = word
        elif word == "lower":
            self._handover_height_adjustment -= 0.05
        elif word == "higher":
            self._handover_height_adjustment += 0.05

    def _on_vision_status(self, msg: VisionStatus):
        self.world.vision_status = msg.status

    def _check_world_state(self) -> bool:
        if self.world.safety_severity == "ESTOP":
            self._speak("Emergency stop active.")
            return False
        if self.world.vision_status in {"LOADING", "ERROR"}:
            self._speak("System initialising. Please wait.")
            timeout = time.monotonic() + 30.0
            while time.monotonic() < timeout and self.world.vision_status == "LOADING":
                time.sleep(0.1)
            if self.world.vision_status != "READY":
                return False
        if not self.world.network_ok:
            self._speak("Voice service unavailable.")
            return False
        return True

    def _execute_fetch_task(self, tool: str, user_id: str, user_name: str):
        try:
            if not self._check_world_state():
                self._abort_task("System not ready for task execution.")
                return

            self._transition_state("PROCESSING", f"processing_{tool}")
            self._send_gripper_open()
            if not self._phase_vision_search(tool, user_id):
                self._abort_task(f"Cannot locate {tool}. Can you confirm it is on the tray?")
                return

            self._transition_state("EXECUTING", f"executing_{tool}")
            if not self._phase_grasp(tool):
                self._abort_task(f"Unable to grasp {tool}. Please reposition it.")
                return

            if not self._phase_handover(tool, user_id, user_name):
                self._speak(f"No collection detected. Returning {tool} to tray.")
                self._safe_deposit(tool)
                return

            self._log_success()
            self._speak("Handover complete. Is there anything else?")
            self._transition_state("STANDBY", f"handover_complete_{tool}")
        finally:
            self.context = TaskContext()

    def _phase_vision_search(self, tool: str, user_id: str) -> bool:
        for attempt in range(1, MAX_RETRIES + 1):
            self.context.vision_retries = attempt
            self.context.vision_start = time.monotonic()
            if attempt == 1:
                self._speak(f"Searching for {tool}.")
            elif attempt == 2:
                self._speak(f"Still searching for {tool}. Please keep the tray clear.")
            else:
                self._speak(f"Last attempt to find {tool}.")

            if self._execute_vision_search(tool, reset_probability_map=(attempt == 3), priority_zones=[]):
                return True
        return False

    def _execute_vision_search(self, tool: str, reset_probability_map: bool, priority_zones: list[str]) -> bool:
        cmd = VisionSearchCommand(
            tool=tool,
            reset_probability_map=bool(reset_probability_map),
            priority_zones=list(priority_zones),
        )
        req = VisionSearchRequest()
        req.tool = cmd.tool
        req.reset_probability_map = cmd.reset_probability_map
        req.priority_zones = cmd.priority_zones
        self._vision_event.clear()
        self.search_pub.publish(req)
        if not self._vision_event.wait(timeout=30.0):
            return False
        result = self._latest_vision_result
        if result is None or not result.found or result.confidence < 0.7:
            return False
        self.context.grasp_point = (result.x, result.y, result.z)
        self.context.detection_candidates = []
        for candidate in result.candidates_json:
            try:
                self.context.detection_candidates.append(json.loads(candidate))
            except Exception:
                continue
        return True

    def _phase_grasp(self, tool: str) -> bool:
        for attempt in range(1, MAX_RETRIES + 1):
            self.context.grasp_retries = attempt
            force_target = min(10.0, 3.0 + max(0, attempt - 1))
            if self.context.grasp_point is None:
                return False
            pregrasp = (self.context.grasp_point[0], self.context.grasp_point[1], self.context.grasp_point[2] + 0.05)
            if not self._send_arm_move(pregrasp, velocity_scale=self._velocity_scale() * 0.8):
                continue
            if not self._send_arm_move(self.context.grasp_point, velocity_scale=self._velocity_scale() * 0.5):
                continue
            self._send_gripper_grasp(force_target)
            time.sleep(0.5)
            self.world.arm_holding = True
            if self.world.gripper_force >= 0.5 or attempt == 1:
                self._transition_state("HOLDING", f"holding_{tool}")
                return True
            if self.context.detection_candidates:
                next_candidate = self.context.detection_candidates.pop(0)
                self.context.grasp_point = (
                    float(next_candidate["x"]),
                    float(next_candidate["y"]),
                    float(next_candidate["z"]),
                )
        return False

    def _phase_handover(self, tool: str, user_id: str, user_name: str) -> bool:
        self._transition_state("HOLDING", f"move_to_handover_{tool}")
        handover_pose = (
            self._handover_zone[0],
            self._handover_zone[1],
            self._handover_zone[2] + self._handover_height_adjustment,
        )
        if not self._send_arm_move(handover_pose, velocity_scale=self._velocity_scale() * 0.6):
            return False

        self._transition_state("HANDOVER", f"handover_{tool}")
        self._speak(f"{tool} ready. Please face the camera.")
        self._auth_face_event.clear()
        self._voice_confirm_word = ""
        self._face_verified = False
        self._face_skipped = False
        handover_start = time.monotonic()

        current_pose = list(handover_pose)
        for attempt in range(1, 4):
            self.context.face_retries = attempt
            if self._wait_for_face_verify(user_id, timeout=8.0):
                break
            if attempt == 1:
                current_pose[2] += 0.05
                self._speak("Please face the camera.")
                self._send_arm_move(tuple(current_pose), velocity_scale=self._velocity_scale() * 0.3)
            elif attempt == 2:
                current_pose[2] = handover_pose[2] - 0.05
                self._speak("Adjusting position for face verification.")
                self._send_arm_move(tuple(current_pose), velocity_scale=self._velocity_scale() * 0.3)
            else:
                self._face_skipped = True
                self._speak("Face verification unavailable. Proceeding with voice and hand confirmation only.")

        if (time.monotonic() - handover_start) > HANDOVER_TIMEOUT_S:
            return False

        self._speak("Please place your open palm under the gripper.")
        if not self._wait_for_hand_detect(timeout=10.0):
            self._speak("Please open your palm.")
            if not self._wait_for_hand_detect(timeout=8.0):
                return False

        self._speak("Say take to receive.")
        if not self._wait_for_voice_confirm(user_id, timeout=5.0):
            self._speak("Say take to receive.")
            if not self._wait_for_voice_confirm(user_id, timeout=5.0):
                return False

        if not self._validate_release():
            self._speak("Handover verification failed. Returning tool to tray.")
            return False

        if self._face_skipped:
            self._log_event("FACE_VERIFY_SKIPPED", tool=tool, description="Face unavailable at handover")
        self._send_gripper_release()
        self.world.arm_holding = False
        return True

    def _validate_release(self) -> bool:
        hand_ok = self._latest_hand_status is not None and self._latest_hand_status.hand_detected and self._latest_hand_status.is_open and self._latest_hand_status.palm_up
        voice_ok = bool(self._voice_confirm_word)
        if not hand_ok or not voice_ok:
            return False
        if self._face_skipped:
            return True
        return self._face_verified

    def _wait_for_face_verify(self, user_id: str, timeout: float) -> bool:
        if self._face_skipped:
            return True
        return self._auth_face_event.wait(timeout=timeout)

    def _wait_for_hand_detect(self, timeout: float) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            hs = self._latest_hand_status
            if hs and hs.hand_detected and hs.is_open and hs.palm_up:
                return True
            time.sleep(0.1)
        return False

    def _wait_for_voice_confirm(self, user_id: str, timeout: float) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self._voice_confirm_word in {"take", "yes", "got it", "ok", "okay"}:
                return True
            time.sleep(0.05)
        return False

    def _send_arm_move(self, position: tuple[float, float, float], velocity_scale: float = 1.0, rotation_offset_deg: float = 0.0) -> bool:
        validated = ArmMoveCommand(
            x=float(position[0]),
            y=float(position[1]),
            z=float(position[2]),
            velocity_scale=float(max(0.1, velocity_scale)),
            rotation_offset_deg=float(rotation_offset_deg),
        )
        self.context.motion_start = time.monotonic()
        q = self.ik.solve_grasp((validated.x, validated.y, validated.z))
        cmd = ArmCommand()
        cmd.command = "MOVE"
        cmd.joint_angles = [float(v) for v in q]
        cmd.velocity_scale = validated.velocity_scale
        cmd.accel_limit = 0.3
        cmd.blocking = True
        self._motion_event.clear()
        self.arm_pub.publish(cmd)
        if not self._motion_event.wait(timeout=15.0):
            return False
        return self._motion_success

    def _send_gripper_open(self) -> bool:
        validated = GripperCommandSchema(command="RELEASE", force_target=0.0)
        cmd = GripperCommand()
        cmd.command = validated.command.value
        cmd.force_target = validated.force_target
        self.gripper_pub.publish(cmd)
        time.sleep(0.6)
        self.world.arm_holding = False
        return True

    def _send_gripper_grasp(self, force_target: float) -> bool:
        validated = GripperCommandSchema(command="GRASP", force_target=float(force_target))
        cmd = GripperCommand()
        cmd.command = validated.command.value
        cmd.force_target = validated.force_target
        self.gripper_pub.publish(cmd)
        return True

    def _send_gripper_release(self) -> bool:
        validated = GripperCommandSchema(command="RELEASE", force_target=0.0)
        cmd = GripperCommand()
        cmd.command = validated.command.value
        cmd.force_target = validated.force_target
        self.gripper_pub.publish(cmd)
        time.sleep(0.6)
        return True

    def _safe_deposit(self, tool: str = ""):
        validated = SafeDepositCommand(tool=tool)
        self._send_arm_move(self._safe_drop_zone, velocity_scale=0.3)
        self._send_gripper_release()
        self.world.arm_holding = False
        self._transition_state("STANDBY", f"safe_deposit_{validated.tool or self.context.tool}")
        self._log_event("SAFE_DEPOSIT", tool=validated.tool, description="Returned tool to tray")

    def _handle_estop(self, reason: str):
        if self.world.arm_holding:
            self._safe_deposit(self.context.tool)
        self._transition_state("ESTOP", f"estop_{reason}")

    def _abort_task(self, message: str):
        validated = AbortCommand(message=message)
        self._speak(validated.message)
        self._log_event("TASK_ABORTED", description=validated.message)
        self._transition_state("STANDBY", "task_aborted")

    def _log_success(self):
        self._log_event(
            "TASK_COMPLETE",
            description=(
                f"vision_retries={self.context.vision_retries} "
                f"grasp_retries={self.context.grasp_retries} "
                f"face_retries={self.context.face_retries}"
            ),
        )

    def _velocity_scale(self) -> float:
        if self.world.safety_severity == "CRITICAL":
            return 0.5
        if self.world.safety_severity == "WARNING":
            return 0.75
        return 1.0


def main(args=None):
    rclpy.init(args=args)
    node = PlannerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

from __future__ import annotations

import json
import math
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

from .ik_solver import IKSolver, cartesian_pose
from .agentic_planner import AgenticPlanner
from .handover_fsm import HandoverSubstate, HandoverSubstateMachine
from .agent_schema import (
    AbortCommand,
    ArmMoveCommand,
    GripperCommandSchema,
    SafeDepositCommand,
    SafeLimitSchema,
    SpeechCommand,
    TransitionCommand,
    VisionSearchCommand,
    validate_agentic_decision,
)
from acare_bringup.qos_profiles import (
    TOPIC_COMMAND, TOPIC_SENSOR, TOPIC_STATE, TOPIC_VISION,
    TOPIC_VOICE_PIPELINE, TOPIC_LOGGING, TOPIC_TTS,
)

MAX_RETRIES = 3
HANDOVER_TIMEOUT_S = 30.0
# Dynamic palm tracking: velocity during incremental approach (very slow, contact-safe)
PALM_APPROACH_VELOCITY = 0.3
# Minimum distance change (metres) before arm moves toward palm — prevents jitter
PALM_TRACKING_MIN_DELTA_M = 0.02


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
        self.agentic = AgenticPlanner(logger=self.get_logger())

        # Publishers — QoS per spec Section V
        self.search_pub     = self.create_publisher(VisionSearchRequest, "/vision_search_request", TOPIC_VISION)
        self.transition_pub = self.create_publisher(StateTransition,     "/state_transition",      TOPIC_STATE)
        self.arm_pub        = self.create_publisher(ArmCommand,          "/arm_command",           TOPIC_COMMAND)
        self.gripper_pub    = self.create_publisher(GripperCommand,      "/gripper_command",       TOPIC_COMMAND)
        self.tts_pub        = self.create_publisher(String,              "/tts_request",           TOPIC_TTS)
        self.log_pub        = self.create_publisher(LogEvent,            "/log_event",             TOPIC_LOGGING)
        # Handover substate is published as a structured String so log_node
        # and admin tools can reconstruct the multi-modal verification
        # timeline without parsing free-text logs.
        self.handover_substate_pub = self.create_publisher(String, "/handover_substate", TOPIC_STATE)
        self._handover_fsm = HandoverSubstateMachine(
            publish=lambda s: self.handover_substate_pub.publish(String(data=s)),
            logger=self.get_logger(),
        )

        # Subscribers — QoS per spec Section V
        self.create_subscription(ValidatedIntent, "/validated_intent", self._on_validated_intent, TOPIC_VOICE_PIPELINE)
        self.create_subscription(VisionResult,    "/vision_result",    self._on_vision_result,    TOPIC_VISION)
        self.create_subscription(MotionFeedback,  "/motion_feedback",  self._on_motion_feedback,  TOPIC_SENSOR)
        self.create_subscription(HandStatus,      "/hand_status",      self._on_hand_status,      TOPIC_VISION)
        self.create_subscription(SafetyAlert,     "/safety_alert",     self._on_safety_alert,     TOPIC_STATE)
        self.create_subscription(RobotState,      "/robot_state",      self._on_robot_state,      TOPIC_STATE)
        self.create_subscription(AuthResult,      "/auth_result",      self._on_auth_result,      TOPIC_VOICE_PIPELINE)
        self.create_subscription(Transcript,      "/raw_transcript",   self._on_transcript,       TOPIC_VOICE_PIPELINE)
        self.create_subscription(VisionStatus,    "/vision_status",    self._on_vision_status,    TOPIC_VISION)

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
        self._kiosk_rest_pose, self._kiosk_interaction_pose, self._kiosk_return_timeout_s = self._load_kiosk_poses()
        self.safe_limits = self._load_safe_limits()
        self._presentation_timer = None
        self._current_named_pose = ""
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

    def _load_kiosk_poses(self):
        try:
            import yaml

            with open(SYSTEM_YAML, "r", encoding="utf-8") as handle:
                cfg = yaml.safe_load(handle) or {}
            robot = cfg.get("robot", {})
            arm = cfg.get("arm", {})
            rest = [float(v) for v in arm.get("kiosk_rest_joint_angles", [0.0, 0.15, -0.35, 0.0, 0.10, 0.0])]
            interaction = [float(v) for v in arm.get("kiosk_interaction_joint_angles", [0.0, -0.10, -0.05, 0.0, -0.05, 0.0])]
            timeout_s = float(robot.get("kiosk_return_to_rest_seconds", 12.0))
            if len(rest) != 6 or len(interaction) != 6:
                raise ValueError("Kiosk poses must contain 6 joint angles each")
            return rest, interaction, max(3.0, timeout_s)
        except Exception:
            return [0.0, 0.15, -0.35, 0.0, 0.10, 0.0], [0.0, -0.10, -0.05, 0.0, -0.05, 0.0], 12.0

    def _load_safe_limits(self) -> SafeLimitSchema:
        try:
            import yaml
            from acare_bringup.paths import THRESHOLDS_YAML

            with open(THRESHOLDS_YAML, "r", encoding="utf-8") as handle:
                threshold_cfg = yaml.safe_load(handle) or {}
            with open(SYSTEM_YAML, "r", encoding="utf-8") as handle:
                system_cfg = yaml.safe_load(handle) or {}
            safety = threshold_cfg.get("safety", {})
            soft = system_cfg.get("arm", {}).get("control_soft_limits", {}) or {}
            velocity_hard = float(safety.get("velocity_limit_degs", 120.0))
            current_hard = float(safety.get("current_limit_A", 8.0))
            temperature_hard = float(safety.get("temperature_estop_C", 75.0))
            gripper_force_hard = float(safety.get("gripper_force_limit_N", 15.0))
            velocity_soft_ratio = float(soft.get("velocity_soft_ratio", 0.90))
            current_soft_margin = float(soft.get("current_soft_margin_a", 0.50))
            temperature_soft_margin = float(soft.get("temperature_soft_margin_c", 5.0))
            gripper_force_soft_ratio = float(soft.get("gripper_force_soft_ratio", 0.90))
            return SafeLimitSchema(
                velocity_hard_deg_s=velocity_hard,
                velocity_soft_deg_s=max(5.0, velocity_hard * velocity_soft_ratio),
                current_hard_a=current_hard,
                current_soft_a=max(0.1, current_hard - current_soft_margin),
                temperature_hard_c=temperature_hard,
                temperature_soft_c=max(5.0, temperature_hard - temperature_soft_margin),
                gripper_force_hard_n=gripper_force_hard,
                gripper_force_soft_n=max(0.5, gripper_force_hard * gripper_force_soft_ratio),
                max_command_velocity_scale=float(soft.get("max_command_velocity_scale", 0.85)),
                max_command_accel_limit=float(soft.get("max_command_accel_limit", 0.25)),
                kiosk_velocity_scale=float(soft.get("kiosk_velocity_scale", 0.22)),
                kiosk_accel_limit=float(soft.get("kiosk_accel_limit", 0.10)),
            )
        except Exception:
            return SafeLimitSchema(
                velocity_hard_deg_s=120.0,
                velocity_soft_deg_s=108.0,
                current_hard_a=8.0,
                current_soft_a=7.5,
                temperature_hard_c=75.0,
                temperature_soft_c=70.0,
                gripper_force_hard_n=15.0,
                gripper_force_soft_n=13.5,
                max_command_velocity_scale=0.85,
                max_command_accel_limit=0.25,
                kiosk_velocity_scale=0.22,
                kiosk_accel_limit=0.10,
            )

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

    def _cancel_presentation_timer(self):
        if self._presentation_timer:
            self._presentation_timer.cancel()
            self._presentation_timer = None

    def _schedule_return_to_rest(self):
        self._cancel_presentation_timer()
        self._presentation_timer = threading.Timer(self._kiosk_return_timeout_s, self._return_to_rest_if_logged_out)
        self._presentation_timer.daemon = True
        self._presentation_timer.start()

    def _return_to_rest_if_logged_out(self):
        with self._lock:
            if self.world.robot_state == "LOGGED_OUT":
                self._send_named_pose("rest")

    def _send_named_pose(self, pose_name: str) -> bool:
        if pose_name == self._current_named_pose:
            return True
        joint_angles = self._kiosk_rest_pose if pose_name == "rest" else self._kiosk_interaction_pose
        ok = self._send_joint_pose(
            joint_angles,
            velocity_scale=self.safe_limits.kiosk_velocity_scale,
            accel_limit=self.safe_limits.kiosk_accel_limit,
        )
        if ok:
            self._current_named_pose = pose_name
        return ok

    def _send_joint_pose(self, joint_angles: list[float], velocity_scale: float, accel_limit: float) -> bool:
        cmd = ArmCommand()
        cmd.command = "MOVE"
        cmd.mode = "JOINT"
        cmd.joint_angles = [float(v) for v in joint_angles]
        cmd.pose = []
        cmd.velocity_scale = min(float(velocity_scale), self.safe_limits.max_command_velocity_scale)
        cmd.accel_limit = min(float(accel_limit), self.safe_limits.max_command_accel_limit)
        cmd.blocking = True
        self._motion_event.clear()
        self.arm_pub.publish(cmd)
        if not self._motion_event.wait(timeout=15.0):
            return False
        return self._motion_success

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

    def _ensure_state(self, target: str, reason: str, allowed_from: set[str]) -> bool:
        """Drive the global FSM through any prerequisite states needed to reach ``target``.

        validated_intent typically arrives while the global FSM is still in
        STANDBY (the user's first command after login). PROCESSING is only
        legal from LISTENING, so the planner has to step through
        STANDBY -> LISTENING -> PROCESSING. This helper hides that pathing
        and waits for /robot_state confirmations between steps so we never
        publish a motion command while state_manager is still on a stale
        state.
        """
        path_to: dict[str, list[str]] = {
            "PROCESSING": ["LISTENING", "PROCESSING"],
            "EXECUTING":  ["EXECUTING"],
            "HOLDING":    ["HOLDING"],
            "HANDOVER":   ["HANDOVER"],
            "STANDBY":    ["STANDBY"],
            "ESTOP":      ["ESTOP"],
        }
        steps = path_to.get(target, [target])

        for idx, step in enumerate(steps):
            current = self.world.robot_state
            if current == step:
                continue
            if idx == 0 and current not in allowed_from and current != step:
                self.get_logger().warn(
                    f"_ensure_state: refusing transition from {current} to {target}"
                )
                return False
            self._transition_state(step, reason if step == target else f"{reason}_step")
            for _ in range(20):
                if self.world.robot_state == step:
                    break
                time.sleep(0.05)
            if self.world.robot_state != step:
                self.get_logger().warn(
                    f"_ensure_state: timeout waiting for {step} "
                    f"(still in {self.world.robot_state})"
                )
                return False
        return True

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
        if msg.state == "LOGGED_OUT":
            self._send_gripper_open()
            self._send_named_pose("rest")
            self._schedule_return_to_rest()
        else:
            self._cancel_presentation_timer()

    def _on_auth_result(self, msg: AuthResult):
        if self.context.user_id and msg.user_id == self.context.user_id:
            self._face_verified = bool(msg.face_verified)
            if msg.face_verified:
                self._auth_face_event.set()

    def _on_transcript(self, msg: Transcript):
        word = (msg.text or "").strip().lower()
        if word and self.world.robot_state == "LOGGED_OUT":
            self._send_named_pose("interaction")
            self._schedule_return_to_rest()
        if word in {"take", "yes", "got it", "ok", "okay"}:
            self._voice_confirm_word = word
        # H2: only honour height adjustments while we are actually in the
        # HANDOVER substate. Outside it, "lower"/"higher" might be the user
        # saying something completely unrelated and silently mutating the
        # offset would carry across sessions.
        elif word == "lower" and self.world.robot_state == "HANDOVER":
            self._handover_height_adjustment -= 0.05
        elif word == "higher" and self.world.robot_state == "HANDOVER":
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

            if not self._ensure_state(
                "PROCESSING",
                f"processing_{tool}",
                allowed_from={"STANDBY", "LISTENING", "PROCESSING"},
            ):
                self._abort_task("Cannot start task: robot is not in a ready state.")
                return
            self._send_gripper_open()
            if not self._phase_vision_search(tool, user_id):
                self._abort_task(f"Cannot locate {tool}. Can you confirm it is on the tray?")
                return

            if not self._ensure_state(
                "EXECUTING",
                f"executing_{tool}",
                allowed_from={"PROCESSING"},
            ):
                self._abort_task("Cannot proceed: state machine refused EXECUTING.")
                return
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
        """
        Agentic vision search with LLM-based strategy and recovery.
        Every agentic proposal is schema-validated before use.
        Invalid proposals → deterministic fallback activates.
        """
        from datetime import datetime
        current_hour = datetime.now().hour

        for attempt in range(1, MAX_RETRIES + 1):
            self.context.vision_retries = attempt
            self.context.vision_start = time.monotonic()

            if attempt == 1:
                raw_strategy = self.agentic.propose_search_strategy(
                    tool, user_id, current_hour, attempt
                )
                validated = validate_agentic_decision(raw_strategy)
                if validated:
                    self._speak(validated.tts_message)
                    reset_map = validated.params.reset_probability_map
                    priority_zones = validated.params.priority_zones
                else:
                    # Schema validation failed — use safe defaults
                    self.get_logger().warn("Agentic search strategy failed validation — using defaults")
                    self._speak(f"Searching for {tool}.")
                    reset_map = False
                    priority_zones = []
            else:
                raw_recovery = self.agentic.propose_vision_recovery(
                    tool, attempt, self.world.safety_severity, self.world.network_ok
                )
                validated = validate_agentic_decision(raw_recovery)
                if validated:
                    self._speak(validated.tts_message)
                    action = validated.action.value
                    reset_map = validated.params.reset_probability_map
                    priority_zones = validated.params.priority_zones
                else:
                    # Fallback: deterministic escalation
                    self.get_logger().warn(f"Agentic vision recovery attempt {attempt} failed validation")
                    if attempt == 2:
                        self._speak(f"Still searching for {tool}. Please keep the tray clear.")
                    else:
                        self._speak(f"Last attempt to find {tool}.")
                    action = "RETRY_UNIFORM_SEARCH"
                    reset_map = (attempt == MAX_RETRIES)
                    priority_zones = []

                # H3: respect an explicit abort proposal so we don't keep
                # searching forever after the LLM has already given up.
                if action == "ABORT_TOOL_NOT_FOUND":
                    self.get_logger().info(
                        f"Vision recovery requested ABORT_TOOL_NOT_FOUND on attempt {attempt}"
                    )
                    return False

                if validated and validated.action.value == "ASK_USER_CONFIRM_LOCATION":
                    time.sleep(5.0)

            if self._execute_vision_search(tool, reset_probability_map=reset_map, priority_zones=priority_zones):
                self.agentic.learn_from_success(
                    type('Ctx', (), {'tool_canonical': tool, 'zone_found': self._get_last_zone()})(),
                    user_id
                )
                return True

        return False

    def _get_last_zone(self) -> str:
        """Get zone from last vision result for learning."""
        if self._latest_vision_result and self._latest_vision_result.found:
            return self._latest_vision_result.zone
        return ""

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
        """
        Agentic grasp with schema-validated LLM recovery.
        Every agentic proposal is validated before execution.
        Invalid proposals → deterministic escalation (reposition → force increase).
        """
        base_force = 3.0

        for attempt in range(1, MAX_RETRIES + 1):
            self.context.grasp_retries = attempt

            if attempt == 1:
                force_target = base_force
                rotation_deg = 0.0
            else:
                raw_recovery = self.agentic.propose_grasp_recovery(
                    tool, attempt, self.world.gripper_force, self.world.safety_severity
                )
                validated = validate_agentic_decision(raw_recovery)
                if validated:
                    self._speak(validated.tts_message)
                    force_target = base_force + validated.params.force_delta_n
                    rotation_deg = validated.params.rotation_deg
                else:
                    # Deterministic fallback: escalate force by 1N per attempt
                    self.get_logger().warn(f"Agentic grasp recovery attempt {attempt} failed validation")
                    self._speak(f"Retrying grasp of {tool}.")
                    force_target = base_force + (attempt - 1)
                    rotation_deg = 15.0 * (attempt - 1)

                # Safety clamp — NEVER exceed soft limit regardless of what LLM says
                force_target = min(force_target, float(self.safe_limits.gripper_force_soft_n))

            if self.context.grasp_point is None:
                return False

            pregrasp = (
                self.context.grasp_point[0],
                self.context.grasp_point[1],
                self.context.grasp_point[2] + 0.05,
            )
            if not self._send_arm_move(pregrasp, velocity_scale=self._velocity_scale() * 0.8):
                continue
            if not self._send_arm_move(
                self.context.grasp_point,
                velocity_scale=self._velocity_scale() * 0.5,
                rotation_offset_deg=rotation_deg,
            ):
                continue
            self._send_gripper_grasp(force_target)
            time.sleep(0.5)
            self.world.arm_holding = True

            if self.world.gripper_force >= 0.5:
                self._transition_state("HOLDING", f"holding_{tool}")
                return True

            # Grasp failed — try next detection candidate if available
            if self.context.detection_candidates:
                next_candidate = self.context.detection_candidates.pop(0)
                self.context.grasp_point = (
                    float(next_candidate["x"]),
                    float(next_candidate["y"]),
                    float(next_candidate["z"]),
                )

        return False

    def _phase_handover(self, tool: str, user_id: str, user_name: str) -> bool:
        """
        Full handover with:
        - Agentic face recovery (Z-height search via gpt-oss-120b)
        - Dynamic palm tracking (incremental approach toward /hand_status x,y,z)
        - Voice confirmation
        - Safety-validated release gate

        Substate progression is published to /handover_substate via
        :class:`HandoverSubstateMachine` so log_node, admin tools, and
        replay harnesses can reconstruct the multi-modal verification
        timeline.
        """
        self._handover_fsm.reset()
        self._handover_fsm.to_approaching(reason=f"tool:{tool}")
        self._transition_state("HOLDING", f"move_to_handover_{tool}")

        # Reset per-handover height adjustment. The previous implementation
        # let it accumulate across sessions because it lived on the node
        # rather than the TaskContext.
        self._handover_height_adjustment = 0.0

        # Get handover pose with learned user Z-offset
        z_offset = self.agentic.get_handover_z_offset(user_id)
        handover_pose = (
            self._handover_zone[0],
            self._handover_zone[1],
            self._handover_zone[2] + z_offset + self._handover_height_adjustment,
        )
        if not self._send_arm_move(handover_pose, velocity_scale=self._velocity_scale() * 0.6):
            self._handover_fsm.to_aborted("approach_failed")
            return False

        self._transition_state("HANDOVER", f"handover_{tool}")
        self._handover_fsm.to_face_verify(reason=f"face_verify_{user_id}")
        self._speak(f"{tool} ready. Please face the camera.")
        self._auth_face_event.clear()
        self._voice_confirm_word = ""
        self._face_verified = False
        self._face_skipped = False
        handover_start = time.monotonic()

        # --- SUBSTATE 1: FACE_VERIFY (agentic Z-height recovery) ---
        current_z = handover_pose[2]
        for attempt in range(1, 4):
            self.context.face_retries = attempt
            if self._wait_for_face_verify(user_id, timeout=8.0):
                break

            # Agentic recovery: propose Z adjustment or voice+hand fallback
            raw_recovery = self.agentic.propose_handover_face_recovery(
                user_name, tool, attempt, current_z
            )
            validated = validate_agentic_decision(raw_recovery)
            if validated:
                self._speak(validated.tts_message)
                action = validated.action.value
                z_delta = validated.params.z_offset_m
            else:
                # Deterministic fallback
                self.get_logger().warn(f"Agentic handover face recovery attempt {attempt} failed validation")
                if attempt == 1:
                    action = "HANDOVER_Z_UP"
                    z_delta = 0.05
                    self._speak("Please look at the camera.")
                elif attempt == 2:
                    action = "HANDOVER_Z_DOWN"
                    z_delta = -0.05
                    self._speak("Please face the camera directly.")
                else:
                    action = "HANDOVER_VOICE_HAND_ONLY"
                    z_delta = 0.0
                    self._speak("Face verification unavailable. Proceeding with voice and hand confirmation only.")

            if action == "HANDOVER_VOICE_HAND_ONLY":
                self._face_skipped = True
                self._log_event("FACE_VERIFY_SKIPPED", tool=tool,
                                description="Face unavailable — proceeding on voice+hand")
                break
            elif action == "HANDOVER_Z_UP":
                current_z += abs(z_delta) if z_delta != 0.0 else 0.05
                self._send_arm_move(
                    (handover_pose[0], handover_pose[1], current_z),
                    velocity_scale=self._velocity_scale() * 0.3,
                )
            elif action == "HANDOVER_Z_DOWN":
                current_z -= abs(z_delta) if z_delta != 0.0 else 0.05
                self._send_arm_move(
                    (handover_pose[0], handover_pose[1], current_z),
                    velocity_scale=self._velocity_scale() * 0.3,
                )

        if (time.monotonic() - handover_start) > HANDOVER_TIMEOUT_S:
            self._handover_fsm.to_aborted("face_verify_timeout")
            return False

        # --- SUBSTATE 2: HAND_DETECT + DYNAMIC PALM TRACKING ---
        self._handover_fsm.to_hand_detect(reason="face_ok")
        self._speak("Please place your open palm under the gripper.")
        hand_ok = self._wait_for_hand_detect_with_tracking(
            current_arm_pos=(handover_pose[0], handover_pose[1], current_z),
            timeout=10.0,
        )
        if not hand_ok:
            self._speak("Please open your palm and hold it steady.")
            hand_ok = self._wait_for_hand_detect_with_tracking(
                current_arm_pos=(handover_pose[0], handover_pose[1], current_z),
                timeout=8.0,
            )
        if not hand_ok:
            self._handover_fsm.to_aborted("hand_detect_timeout")
            return False

        # --- SUBSTATE 3: VOICE_CONFIRM ---
        self._handover_fsm.to_voice_confirm(reason="hand_ok")
        self._speak("Say take to receive.")
        if not self._wait_for_voice_confirm(user_id, timeout=5.0):
            self._speak("Say take to receive.")
            if not self._wait_for_voice_confirm(user_id, timeout=5.0):
                self._handover_fsm.to_aborted("voice_confirm_timeout")
                return False

        # --- RELEASE GATE ---
        if not self._validate_release():
            self._speak("Handover verification failed. Returning tool to tray.")
            self._handover_fsm.to_aborted("release_validation_failed")
            return False

        self._handover_fsm.to_releasing(reason="all_checks_passed")

        if self._face_skipped:
            self._log_event("FACE_VERIFY_SKIPPED", tool=tool,
                            description=f"Handover to {user_id} without face verification")

        # Learn height preference for next session
        if self._handover_height_adjustment != 0.0:
            cmd = "higher" if self._handover_height_adjustment > 0 else "lower"
            self.agentic.learn_height_adjustment(user_id, cmd)

        self._send_gripper_release()
        self.world.arm_holding = False
        self._handover_fsm.to_complete(reason="gripper_released")
        return True

    def _wait_for_hand_detect_with_tracking(
        self,
        current_arm_pos: tuple[float, float, float],
        timeout: float,
    ) -> bool:
        """
        Spec Section VII: Dynamic palm tracking.
        Waits for hand detection AND incrementally approaches the palm center
        using real-time /hand_status (x,y,z). Each position update validated
        by workspace bounds. Velocity: PALM_APPROACH_VELOCITY (very slow).

        The arm makes small incremental moves toward the detected palm,
        updating its target as the hand position changes. This handles
        the case where the user's hand isn't perfectly aligned with the
        fixed handover zone.
        """
        deadline = time.monotonic() + timeout
        last_move_target = current_arm_pos
        last_move_time = 0.0

        while time.monotonic() < deadline:
            hs = self._latest_hand_status
            if hs is None:
                time.sleep(0.1)
                continue

            if hs.hand_detected and hs.is_open and hs.palm_up:
                # Hand is ready — check if we should approach closer
                palm_pos = (hs.x, hs.y, hs.z)

                # Only move if palm position is valid (non-zero) and within workspace
                if palm_pos[0] != 0.0 or palm_pos[1] != 0.0 or palm_pos[2] != 0.0:
                    # Check if palm moved enough to warrant a new arm move
                    delta = sum((a - b) ** 2 for a, b in zip(palm_pos, last_move_target)) ** 0.5
                    now = time.monotonic()

                    if delta > PALM_TRACKING_MIN_DELTA_M and (now - last_move_time) > 0.5:
                        # Validate target is within workspace
                        w = {'xmin': -0.4, 'xmax': 0.4, 'ymin': -0.3, 'ymax': 0.3, 'zmin': 0.0, 'zmax': 0.5}
                        x, y, z = palm_pos
                        if (w['xmin'] <= x <= w['xmax'] and
                            w['ymin'] <= y <= w['ymax'] and
                            w['zmin'] <= z <= w['zmax']):
                            # Move arm toward palm (non-blocking, slow)
                            self._send_arm_move(palm_pos, velocity_scale=PALM_APPROACH_VELOCITY)
                            last_move_target = palm_pos
                            last_move_time = now

                return True  # Hand detected, open, palm up — success

            # Hand detected but not ready (closed or not palm-up)
            if hs.hand_detected and not hs.is_open:
                pass  # Wait — user is positioning

            time.sleep(0.1)

        return False

    def _validate_release(self) -> bool:
        """
        Spec Section VII (SafetyKernel.validate_release):
        Hand detected AND voice confirmed are BOTH required.
        Face is ALWAYS advisory — if face_verified is False but hand+voice pass,
        proceed and log FACE_SKIPPED. Do NOT block on face failure alone.
        """
        hand_ok = (
            self._latest_hand_status is not None
            and self._latest_hand_status.hand_detected
            and self._latest_hand_status.is_open
            and self._latest_hand_status.palm_up
        )
        voice_ok = bool(self._voice_confirm_word)
        # Hard requirement: both hand and voice must pass
        if not hand_ok or not voice_ok:
            return False
        # Face is advisory — log skip but do not block
        if not self._face_verified and not self._face_skipped:
            self.get_logger().warn("validate_release: face not verified — proceeding on hand+voice (FACE_SKIPPED logged)")
            self._face_skipped = True   # ensure it gets logged
        return True

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
            velocity_scale=float(min(max(0.1, velocity_scale), self.safe_limits.max_command_velocity_scale)),
            rotation_offset_deg=float(rotation_offset_deg),
        )
        self._current_named_pose = ""
        self.context.motion_start = time.monotonic()

        # B1: try real IK. If we have no calibrated solver, publish in
        # CARTESIAN mode and let the embedded layer (Teensy firmware in
        # production, simulator in dev) handle the final motion. Never
        # fabricate joint angles equal to the cartesian XYZ — that bug
        # would have driven joint 1 to ``x`` radians, joint 2 to ``y``
        # radians and so on, with no kinematic relation to the target.
        rotation_rad = math.radians(validated.rotation_offset_deg)
        target_xyz = (validated.x, validated.y, validated.z)
        joint_angles = self.ik.solve_grasp(target_xyz)

        cmd = ArmCommand()
        cmd.command = "MOVE"
        cmd.velocity_scale = validated.velocity_scale
        cmd.accel_limit = self.safe_limits.max_command_accel_limit
        cmd.blocking = True

        if joint_angles is not None and len(joint_angles) == 6:
            cmd.mode = "JOINT"
            cmd.joint_angles = [float(v) for v in joint_angles]
            cmd.pose = cartesian_pose(target_xyz, (0.0, 0.0, rotation_rad))
        else:
            cmd.mode = "CARTESIAN"
            cmd.joint_angles = []
            cmd.pose = cartesian_pose(target_xyz, (0.0, 0.0, rotation_rad))
            if self.ik.has_solver is False and not getattr(self, "_ik_warning_logged", False):
                self.get_logger().warn(
                    f"IKSolver: {self.ik.status}; publishing cartesian-mode arm commands"
                )
                self._ik_warning_logged = True

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
        validated = GripperCommandSchema(
            command="GRASP",
            force_target=min(float(force_target), self.safe_limits.gripper_force_soft_n),
        )
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

    def destroy_node(self):
        self._cancel_presentation_timer()
        super().destroy_node()


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

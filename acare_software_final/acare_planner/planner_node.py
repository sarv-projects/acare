# acare_planner/planner_node.py
import queue
import threading
import time
import json
import yaml

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from acare_bringup.paths import SYSTEM_YAML
from acare_msgs.msg import (
    ArmCommand, GripperCommand, VisionSearchRequest, StateTransition, LogEvent,
    ValidatedIntent, VisionResult, MotionFeedback, HandStatus, SafetyAlert,
    RobotState, AuthResult, Transcript, VisionStatus, AuthRequest
)

from .agentic_planner import AgenticPlanner
from .tool_kernel import ToolKernel
from .state_snapshot import TaskSnapshot, WorldState as WorldSnapshot, TaskObjective, Budget, LastAction
from .voice_sync import VoiceSyncBridge
from .hw_translator import HWTranslator
from .task_memory import TaskMemory
from .ik_solver import IKSolver
from .safety_kernel import SafetyKernel, RetryCounters

from acare_bringup.qos_profiles import (
    TOPIC_COMMAND, TOPIC_SENSOR, TOPIC_STATE, TOPIC_VISION,
    TOPIC_VOICE_PIPELINE, TOPIC_LOGGING, TOPIC_TTS,
)

class WorldState:
    def __init__(self):
        self.robot_state = "LOGGED_OUT"
        self.active_user_id = ""
        self.safety_severity = "OK"
        self.vision_status = "UNKNOWN"
        self.network_ok = True
        self.arm_holding = False
        self.gripper_force = 0.0

class PlannerNode(Node):
    def __init__(self):
        super().__init__("planner_node")
        self.world = WorldState()
        self.agentic = AgenticPlanner(logger=self.get_logger())
        self.hw_translator = HWTranslator()
        self.task_memory = TaskMemory()
        self.voice_sync = VoiceSyncBridge()
        self.ik = IKSolver()
        
        # Publishers
        self.search_pub = self.create_publisher(VisionSearchRequest, "/vision_search_request", TOPIC_VISION)
        self.transition_pub = self.create_publisher(StateTransition, "/state_transition", TOPIC_STATE)
        self.arm_pub = self.create_publisher(ArmCommand, "/arm_command", TOPIC_COMMAND)
        self.gripper_pub = self.create_publisher(GripperCommand, "/gripper_command", TOPIC_COMMAND)
        self.tts_pub = self.create_publisher(String, "/tts_request", TOPIC_TTS)
        self.log_pub = self.create_publisher(LogEvent, "/log_event", TOPIC_LOGGING)
        self.vision_penalty_pub = self.create_publisher(String, "/vision_penalty", TOPIC_VISION)
        self.auth_req_pub = self.create_publisher(AuthRequest, "/auth_request", TOPIC_STATE)

        # Subscribers
        self.create_subscription(ValidatedIntent, "/validated_intent", self._on_validated_intent, TOPIC_VOICE_PIPELINE)
        self.create_subscription(VisionResult, "/vision_result", self._on_vision_result, TOPIC_VISION)
        self.create_subscription(MotionFeedback, "/motion_feedback", self._on_motion_feedback, TOPIC_SENSOR)
        self.create_subscription(HandStatus, "/hand_status", self._on_hand_status, TOPIC_VISION)
        self.create_subscription(SafetyAlert, "/safety_alert", self._on_safety_alert, TOPIC_STATE)
        self.create_subscription(RobotState, "/robot_state", self._on_robot_state, TOPIC_STATE)
        self.create_subscription(AuthResult, "/auth_result", self._on_auth_result, TOPIC_VOICE_PIPELINE)
        self.create_subscription(Transcript, "/raw_transcript", self._on_transcript, TOPIC_VOICE_PIPELINE)
        self.create_subscription(VisionStatus, "/vision_status", self._on_vision_status, TOPIC_VISION)

        self._lock = threading.Lock()
        self._task_thread = None
        self._vision_event = threading.Event()
        self._motion_queue = queue.Queue(maxsize=1)
        self._auth_event = threading.Event()
        self._estop_active = threading.Event()
        
        self._last_vision_result = None
        self._last_auth_success = False
        self._hand_detected = False
        self._last_approach_rotation = 0.0

        # Load configs
        self._workspace = self._load_workspace()
        self.face_verify_z, self.presentation_z = self._load_z_heights()

        self.safety_kernel = SafetyKernel(self._workspace)
        self.retry_counters = RetryCounters()
        
        self.context = type('TaskContext', (), {'tool': '', 'user_id': '', 'grasp_point': None})()
        self.get_logger().info("Planner node ready")

    def _load_workspace(self):
        try:
            with open(SYSTEM_YAML, "r", encoding="utf-8") as handle:
                cfg = yaml.safe_load(handle) or {}
            ws = cfg.get("robot", {}).get("workspace", {})
            if ws:
                return {k: float(ws.get(k, 0.0)) for k in ['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax']}
        except:
            pass
        return {'xmin': -0.6, 'xmax': 0.6, 'ymin': -0.6, 'ymax': 0.6, 'zmin': 0.0, 'zmax': 0.75}

    def _load_z_heights(self):
        try:
            with open(SYSTEM_YAML, "r", encoding="utf-8") as handle:
                cfg = yaml.safe_load(handle) or {}
            robot = cfg.get("robot", {})
            return float(robot.get("face_verify_z", 0.85)), float(robot.get("presentation_z", 0.45))
        except:
            return 0.85, 0.45

    def _on_validated_intent(self, msg: ValidatedIntent):
        with self._lock:
            if self._task_thread and self._task_thread.is_alive():
                self._speak("Task already in progress.")
                return
            # TODO(Architectural Upgrade): Using a python threading.Thread for the agentic loop is ad-hoc 
            # and lacks native ROS preemption. Best robotics practices dictate migrating this to a ROS2 Action Server.
            self._task_thread = threading.Thread(
                target=self._run_agentic_task,
                args=(msg.tool, msg.user_id, msg.name),
                daemon=True,
            )
            self._task_thread.start()

    def _run_agentic_task(self, tool: str, user_id: str, user_name: str):
        self._estop_active.clear()

        if self.world.safety_severity == "ESTOP":
            self._speak("Emergency stop active. Cannot start task.")
            return

        with self._lock:
            self._last_vision_result = None
            self._hand_detected = False

        self.retry_counters.reset()
        self.safety_kernel.reset_failures()

        self.context.tool = tool
        self.context.user_id = user_id
        self.context.grasp_point = None

        prior = self.task_memory.get_user_prior(user_id)
        
        snapshot = TaskSnapshot(
            objective=TaskObjective(tool=tool, user=user_name, task_phase="SEARCHING"),
            world=WorldSnapshot(
                arm_at="REST",
                gripper="OPEN",
                safety=self.world.safety_severity,
                holding_tool=self.world.arm_holding,
                vision_ready=(self.world.vision_status == "READY")
            ),
            last_action=LastAction(tool_call="", result="", reason=""),
            action_history=[],
            budget=Budget(calls_used=0, calls_remaining=20),
            tried_and_failed=[],
            zones_searched=[],
            user_prior=prior,
            available_tools=["vision_scan", "arm_move", "arm_approach", "gripper_close", "gripper_open", "detect_face", "detect_hand", "speak", "ask_user", "complete_task", "abort_task"]
        )

        tk = ToolKernel(self, snapshot, self.hw_translator)
        self.transition_pub.publish(StateTransition(target_state="EXECUTING"))
        self.agentic.run_task(self, tk, snapshot)
        
        if self._estop_active.is_set():
            self.transition_pub.publish(StateTransition(target_state="STANDBY"))
        else:
            if snapshot.last_action.tool_call and snapshot.last_action.tool_call.startswith("complete_task"):
                self.task_memory.save_outcome(user_id, tool, self._last_vision_result.zone if self._last_vision_result else None, True)
            self.transition_pub.publish(StateTransition(target_state="STANDBY"))
            
        self.context.tool = ""
        self.context.user_id = ""

    def _on_transcript(self, msg: Transcript):
        self.voice_sync.on_transcript(msg.text or "")
        
    def _on_vision_result(self, msg: VisionResult):
        with self._lock:
            self._last_vision_result = msg
        self._vision_event.set()

    def _on_motion_feedback(self, msg: MotionFeedback):
        self.world.gripper_force = float(msg.gripper_force)
        try:
            self._motion_queue.put_nowait(bool(msg.success))
        except queue.Full:
            pass

    def _on_hand_status(self, msg: HandStatus):
        with self._lock:
            self._hand_detected = bool(msg.hand_detected and msg.is_open and msg.hand_approaching)

    def _on_safety_alert(self, msg: SafetyAlert):
        self.world.safety_severity = msg.severity
        if msg.severity == "ESTOP":
            self._estop_active.set()
            self._vision_event.set()
            self._auth_event.set()
            try:
                self._motion_queue.put_nowait(False)
            except queue.Full:
                pass
            
            if self.world.arm_holding:
                # During an ESTOP, the hardware controller freezes the arm instantly. 
                # Sending a RELEASE command here will be rejected by the embedded_interface_node.
                # We MUST retain self.world.arm_holding = True so the system remembers it holds a sharp tool.
                pass

    def _on_robot_state(self, msg: RobotState):
        self.world.robot_state = msg.state
        self.world.active_user_id = msg.active_user_id

    def _on_auth_result(self, msg: AuthResult):
        self._last_auth_success = bool(msg.face_verified)
        self._auth_event.set()

    def _on_vision_status(self, msg: VisionStatus):
        self.world.vision_status = msg.status

    def _speak(self, text: str):
        self.tts_pub.publish(String(data=text))
        
    def _send_vision_search_request(self, tool: str, zone: str = 'ALL'):
        priority_zones = [zone] if zone and zone not in ('ALL', 'AUTO') else []
        if zone == 'AUTO':
            priority_zones = ['AUTO']
        req = VisionSearchRequest(tool=tool, reset_probability_map=False, priority_zones=priority_zones)
        self.search_pub.publish(req)
        
    def _send_arm_move(self, x: float, y: float, z: float) -> bool:
        ik_result = self.ik.solve_with_status((x, y, z))
        if not ik_result.reachable:
            return False
            
        cmd = ArmCommand(
            command="MOVE",
            joint_angles=[float(v) for v in ik_result.joint_angles],
            velocity_scale=0.5,
            accel_limit=0.25,
            blocking=True
        )
        self.arm_pub.publish(cmd)
        return True

    def _send_gripper_command(self, cmd_type: str, force: float = 0.0):
        cmd = GripperCommand(command=cmd_type, force_target=force)
        self.gripper_pub.publish(cmd)
        
    def _request_auth_face(self):
        req = AuthRequest(modality="face", timeout_s=10.0)
        self.auth_req_pub.publish(req)
        
    def _publish_vision_penalty(self):
        self.vision_penalty_pub.publish(String(data=self.context.tool))

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

from __future__ import annotations

import threading
import time

import rclpy
from rclpy.node import Node

from acare_bringup.paths import SYSTEM_YAML
from acare_msgs.msg import ArmCommand, EmergencySignal, GripperCommand, MotionFeedback
from acare_msgs.msg import RobotState


class EmbeddedInterfaceNode(Node):
    def __init__(self):
        super().__init__("embedded_interface_node")
        self.feedback_pub = self.create_publisher(MotionFeedback, "/motion_feedback", 10)
        self.create_subscription(ArmCommand, "/arm_command", self._on_arm_command, 10)
        self.create_subscription(GripperCommand, "/gripper_command", self._on_gripper_command, 10)
        self.create_subscription(EmergencySignal, "/emergency_stop", self._on_estop, 10)
        self.create_subscription(RobotState, "/robot_state", self._on_robot_state, 10)
        self._lock = threading.Lock()
        self._estop = False
        self._robot_state = "LOGGED_OUT"
        self._kiosk_rest_pose, self._kiosk_interaction_pose, self._kiosk_velocity_scale, self._kiosk_accel_limit = self._load_kiosk_policy()
        self.get_logger().info("Embedded interface node ready in controller-agnostic mode")

    def _load_kiosk_policy(self):
        try:
            import yaml

            with open(SYSTEM_YAML, "r", encoding="utf-8") as handle:
                cfg = yaml.safe_load(handle) or {}
            arm = cfg.get("arm", {}) or {}
            soft = arm.get("control_soft_limits", {}) or {}
            rest = [float(v) for v in arm.get("kiosk_rest_joint_angles", [0.0, 0.15, -0.35, 0.0, 0.10, 0.0])]
            interaction = [float(v) for v in arm.get("kiosk_interaction_joint_angles", [0.0, -0.10, -0.05, 0.0, -0.05, 0.0])]
            kiosk_velocity = float(soft.get("kiosk_velocity_scale", 0.22))
            kiosk_accel = float(soft.get("kiosk_accel_limit", 0.10))
            if len(rest) != 6 or len(interaction) != 6:
                raise ValueError("Kiosk poses must contain 6 joints")
            return rest, interaction, kiosk_velocity, kiosk_accel
        except Exception:
            return [0.0, 0.15, -0.35, 0.0, 0.10, 0.0], [0.0, -0.10, -0.05, 0.0, -0.05, 0.0], 0.22, 0.10

    def _on_robot_state(self, msg: RobotState):
        self._robot_state = msg.state

    def _joint_pose_matches(self, actual: list[float], expected: list[float], tol: float = 0.03) -> bool:
        if len(actual) != len(expected):
            return False
        return all(abs(float(a) - float(b)) <= tol for a, b in zip(actual, expected))

    def _is_allowed_logged_out_arm_command(self, msg: ArmCommand) -> bool:
        if msg.command != "MOVE":
            return False
        if not self._joint_pose_matches(msg.joint_angles, self._kiosk_rest_pose) and not self._joint_pose_matches(msg.joint_angles, self._kiosk_interaction_pose):
            return False
        if float(msg.velocity_scale) > self._kiosk_velocity_scale + 1e-6:
            return False
        if float(msg.accel_limit) > self._kiosk_accel_limit + 1e-6:
            return False
        return True

    def _publish_feedback(self, success: bool, phase: str, error: str = "", gripper_force: float = 0.0):
        msg = MotionFeedback()
        msg.success = success
        msg.phase = phase
        msg.error = error
        msg.joint_positions = []
        msg.joint_velocities = []
        msg.joint_currents = []
        msg.temperatures = []
        msg.gripper_force = gripper_force
        msg.imu_roll = 0.0
        msg.imu_pitch = 0.0
        msg.imu_yaw = 0.0
        self.feedback_pub.publish(msg)

    def _simulate_motion(self, phase: str, duration_s: float = 0.5, gripper_force: float = 0.0):
        time.sleep(duration_s)
        with self._lock:
            if self._estop:
                self._publish_feedback(False, phase, "estop_active")
                return
        self._publish_feedback(True, phase, gripper_force=gripper_force)

    def _on_arm_command(self, msg: ArmCommand):
        if self._robot_state == "LOGGED_OUT" and not self._is_allowed_logged_out_arm_command(msg):
            self.get_logger().warn("Rejected non-kiosk arm command while LOGGED_OUT")
            self._publish_feedback(False, f"arm_{msg.command.lower()}", "logged_out_pose_guard")
            return
        threading.Thread(
            target=self._simulate_motion,
            args=(f"arm_{msg.command.lower()}", 0.7 if msg.blocking else 0.1),
            daemon=True,
        ).start()

    def _on_gripper_command(self, msg: GripperCommand):
        if self._robot_state == "LOGGED_OUT" and msg.command in {"GRASP", "CLOSE"}:
            self.get_logger().warn("Rejected grasp command while LOGGED_OUT")
            self._publish_feedback(False, f"gripper_{msg.command.lower()}", "logged_out_gripper_guard")
            return
        force = msg.force_target if msg.command in {"GRASP", "CLOSE"} else 0.0
        threading.Thread(
            target=self._simulate_motion,
            args=(f"gripper_{msg.command.lower()}", 0.2),
            kwargs={"gripper_force": force},
            daemon=True,
        ).start()

    def _on_estop(self, _msg: EmergencySignal):
        with self._lock:
            self._estop = True
        self._publish_feedback(False, "estop", "Emergency stop active")


def main(args=None):
    rclpy.init(args=args)
    node = EmbeddedInterfaceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

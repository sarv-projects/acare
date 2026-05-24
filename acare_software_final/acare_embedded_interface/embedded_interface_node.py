from __future__ import annotations

import threading
import time

import rclpy
from rclpy.node import Node

from acare_msgs.msg import ArmCommand, EmergencySignal, GripperCommand, MotionFeedback


class EmbeddedInterfaceNode(Node):
    def __init__(self):
        super().__init__("embedded_interface_node")
        self.feedback_pub = self.create_publisher(MotionFeedback, "/motion_feedback", 10)
        self.create_subscription(ArmCommand, "/arm_command", self._on_arm_command, 10)
        self.create_subscription(GripperCommand, "/gripper_command", self._on_gripper_command, 10)
        self.create_subscription(EmergencySignal, "/emergency_stop", self._on_estop, 10)
        self._lock = threading.Lock()
        self._estop = False
        self.get_logger().info("Embedded interface node ready in controller-agnostic mode")

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
        threading.Thread(
            target=self._simulate_motion,
            args=(f"arm_{msg.command.lower()}", 0.7 if msg.blocking else 0.1),
            daemon=True,
        ).start()

    def _on_gripper_command(self, msg: GripperCommand):
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

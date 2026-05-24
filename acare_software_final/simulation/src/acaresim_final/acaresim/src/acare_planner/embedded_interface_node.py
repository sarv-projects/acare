import threading
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from acare_msgs.msg import ArmCommand, GripperCommand, MotionFeedback
from std_srvs.srv import Trigger

ARM_JOINTS = [
    "base", "shoulder", "elbow",
    "wrist_1", "wrist_2", "wrist_3"
]
GRIPPER_JOINT = ["gripper_slider_right"]

class EmbeddedInterfaceNode(Node):
    def __init__(self):
        super().__init__('embedded_interface')
        self._arm_sub = self.create_subscription(ArmCommand, '/arm_command', self._on_arm_cmd, 10)
        self._gripper_sub = self.create_subscription(GripperCommand, '/gripper_command', self._on_gripper_cmd, 10)
        self._feedback_pub = self.create_publisher(MotionFeedback, '/motion_feedback', 10)

        self._arm_client = ActionClient(self, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory')
        self._gripper_client = ActionClient(self, FollowJointTrajectory, '/gripper_controller/follow_joint_trajectory')

        if not self._arm_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().warn("Arm controller not available — running in SIM mode")
        if not self._gripper_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().warn("Gripper controller not available")

    def _publish_feedback(self, success: bool, phase: str, error: str = ""):
        fb = MotionFeedback()
        fb.success = success
        fb.phase = phase
        fb.error = error
        self._feedback_pub.publish(fb)

    def _on_arm_cmd(self, msg):
        target_positions = list(msg.joint_angles)
        if len(target_positions) != len(ARM_JOINTS):
            self.get_logger().warn(f"Expected {len(ARM_JOINTS)} joints, got {len(target_positions)}")
            self._publish_feedback(False, "invalid_joint_count", f"Expected {len(ARM_JOINTS)}")
            return

        if not self._arm_client.server_is_ready():
            self.get_logger().info(f"[SIM] Arm would move to: {[f'{j:.3f}' for j in target_positions]}")
            time.sleep(1.0)
            self._publish_feedback(True, "sim_move_complete")
            return

        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = ARM_JOINTS
        point = JointTrajectoryPoint()
        point.positions = target_positions
        point.time_from_start = Duration(sec=3)
        goal_msg.trajectory.points = [point]

        send_goal_future = self._arm_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self._arm_goal_cb)

    def _arm_goal_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self._publish_feedback(False, "goal_rejected")
            return
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(lambda f: self._publish_feedback(
            f.result().result.error_code == 0, "arm_execution_complete"))

    def _on_gripper_cmd(self, msg):
        close_cmd = msg.command in ("GRASP", "CLOSE")
        position = 0.0 if close_cmd else -0.04

        if not self._gripper_client.server_is_ready():
            self.get_logger().info(f"[SIM] Gripper: {'CLOSE' if close_cmd else 'OPEN'}")
            time.sleep(0.3)
            return

        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = GRIPPER_JOINT
        point = JointTrajectoryPoint()
        point.positions = [position]
        point.time_from_start = Duration(sec=1)
        goal_msg.trajectory.points = [point]
        self._gripper_client.send_goal_async(goal_msg)


def main():
    rclpy.init()
    node = EmbeddedInterfaceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

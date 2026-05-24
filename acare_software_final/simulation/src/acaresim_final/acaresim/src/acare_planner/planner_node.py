import rclpy
from rclpy.node import Node
from acare_msgs.msg import (
    ValidatedIntent, VisionSearchRequest, VisionResult,
    StateTransition, RobotState, ArmCommand, GripperCommand,
    MotionFeedback, HandStatus
)
import time

FETCH_POSES = {
    "scalpel":       [0.0, -0.8, 0.3, 0.0, 0.0, 0.0],
    "scissors":      [0.3, -0.6, 0.4, 0.0, 0.0, 0.0],
    "forceps":       [-0.3, -0.7, 0.3, 0.0, 0.0, 0.0],
    "bandage":       [0.5, -0.5, 0.2, 0.0, 0.0, 0.0],
    "gauze":         [-0.4, -0.6, 0.3, 0.0, 0.0, 0.0],
    "thermometer":   [0.2, -0.9, 0.5, 0.0, 0.0, 0.0],
    "oximeter":      [-0.2, -0.8, 0.4, 0.0, 0.0, 0.0],
    "plaster":       [0.4, -0.7, 0.2, 0.0, 0.0, 0.0],
}

HOME_POSE = [0.0, -1.57, 1.57, 0.0, 0.0, 0.0]

class PlannerNode(Node):
    def __init__(self):
        super().__init__('planner_node')
        self._intent_sub = self.create_subscription(ValidatedIntent, '/validated_intent', self._on_intent, 10)
        self._vision_sub = self.create_subscription(VisionResult, '/vision_result', self._on_vision, 10)
        self._state_sub = self.create_subscription(RobotState, '/robot_state', self._on_state, 10)
        self._hand_sub = self.create_subscription(HandStatus, '/hand_status', self._on_hand, 10)
        self._feedback_sub = self.create_subscription(MotionFeedback, '/motion_feedback', self._on_feedback, 10)

        self._search_pub = self.create_publisher(VisionSearchRequest, '/vision_search_request', 10)
        self._transition_pub = self.create_publisher(StateTransition, '/state_transition', 10)
        self._arm_pub = self.create_publisher(ArmCommand, '/arm_command', 10)
        self._gripper_pub = self.create_publisher(GripperCommand, '/gripper_command', 10)

        self.current_state = "LOGGED_OUT"
        self.pending_tool = None
        self._vision_enabled = False

    def _on_state(self, msg):
        self.current_state = msg.state

    def _on_hand(self, msg):
        self.get_logger().debug(f"Hand: detected={msg.hand_detected} pos=({msg.x:.2f},{msg.y:.2f},{msg.z:.2f})")

    def _on_feedback(self, msg):
        pass

    def _publish_transition(self, target: str, reason: str = ""):
        transition = StateTransition()
        transition.target_state = target
        transition.reason = reason
        self._transition_pub.publish(transition)

    def _on_intent(self, msg):
        tool = msg.tool.lower()
        self.get_logger().info(f"Intent received: fetch {tool}")
        self.pending_tool = tool

        self._publish_transition("LISTENING", f"voice_detected")
        self._publish_transition("PROCESSING", f"received_intent_{tool}")

        if self._vision_enabled:
            req = VisionSearchRequest()
            req.tool = tool
            self._search_pub.publish(req)
        else:
            self._exec_no_vision(tool)

    def _on_vision(self, msg):
        if not self.pending_tool:
            return
        tool = self.pending_tool
        if msg.found:
            self.get_logger().info(f"Found {msg.tool} at ({msg.x:.2f},{msg.y:.2f},{msg.z:.2f})")
            self._publish_transition("EXECUTING", f"found_{tool}")
            self._move_to_pose(msg.x, msg.y, msg.z)
        else:
            self.get_logger().warn(f"Tool {tool} not found by vision")
            self._publish_transition("STANDBY", f"vision_not_found_{tool}")

    def _exec_no_vision(self, tool):
        self._publish_transition("EXECUTING", f"no_vision_{tool}")

        if tool in FETCH_POSES:
            joints = FETCH_POSES[tool]
        else:
            joints = HOME_POSE
            self.get_logger().warn(f"No stored pose for {tool}, using home")

        cmd = ArmCommand()
        cmd.command = "MOVE"
        cmd.joint_angles = joints
        cmd.velocity_scale = 0.5
        cmd.accel_limit = 0.3
        cmd.blocking = True
        self._arm_pub.publish(cmd)
        self.get_logger().info(f"Published arm command for {tool}")

        time.sleep(0.5)
        gripper = GripperCommand()
        gripper.command = "GRASP"
        gripper.force_target = 5.0
        self._gripper_pub.publish(gripper)

        self._publish_transition("HOLDING", f"grasped_{tool}")

    def _move_to_pose(self, x, y, z):
        cmd = ArmCommand()
        cmd.command = "MOVE_TO_POSE"
        cmd.joint_angles = [x, y, z, 0.0, 0.0, 0.0]
        cmd.velocity_scale = 0.5
        cmd.accel_limit = 0.3
        cmd.blocking = True
        self._arm_pub.publish(cmd)
        self.get_logger().info(f"Moving to vision pose ({x:.2f},{y:.2f},{z:.2f})")

        time.sleep(0.5)
        gripper = GripperCommand()
        gripper.command = "GRASP"
        self._gripper_pub.publish(gripper)

        self._publish_transition("HOLDING", "vision_grasp_done")

    def set_vision_enabled(self, enabled: bool):
        self._vision_enabled = enabled


def main():
    rclpy.init()
    node = PlannerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

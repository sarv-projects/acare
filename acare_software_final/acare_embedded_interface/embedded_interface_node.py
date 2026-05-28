"""
ACARE embedded interface node — bridge between high-level planner commands
and either:
  1. Gazebo's ros2_control controllers (sim path), or
  2. Teensy 4.1 over UART/CAN (real-hardware path, future).

Spec Reference: Section XV (Embedded Interface — UART / CAN bridge).

Sim path (current):
  Subscribes to /arm_command and /gripper_command from the planner.
  Publishes a FollowJointTrajectory action goal to /arm_controller/follow_joint_trajectory
  (the controller spawned by gz_ros2_control inside Gazebo).
  Mirrors gripper commands onto /gripper_controller/follow_joint_trajectory.
  Publishes MotionFeedback on /motion_feedback after each command.

Real-hardware path (future): write to a serial bridge, parse CAN telemetry.
The code path is selected at runtime via system.yaml (interface.mode).
"""
from __future__ import annotations

import threading
import time
from typing import List

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from builtin_interfaces.msg import Duration
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from acare_bringup.paths import SYSTEM_YAML
from acare_msgs.msg import (
    ArmCommand,
    EmergencySignal,
    GripperCommand,
    MotionFeedback,
    RobotState,
)


# Spec joint order — must match URDF and ros2_controllers.yaml
ARM_JOINT_NAMES = ["base", "shoulder", "elbow", "wrist_1", "wrist_2", "wrist_3"]
GRIPPER_JOINT_NAMES = ["gripper_slider_right"]
ARM_ACTION_TOPIC = "/arm_controller/follow_joint_trajectory"
GRIPPER_ACTION_TOPIC = "/gripper_controller/follow_joint_trajectory"

# Default motion durations (seconds). Tuned for safety, not speed.
DEFAULT_ARM_DURATION = 2.5
DEFAULT_GRIPPER_DURATION = 0.7

# Gripper command → slider position (metres). Values from URDF limits.
GRIPPER_OPEN_POS = 0.0
GRIPPER_CLOSE_POS = 0.04


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

        (
            self._kiosk_rest_pose,
            self._kiosk_interaction_pose,
            self._kiosk_velocity_scale,
            self._kiosk_accel_limit,
        ) = self._load_kiosk_policy()

        # Action clients to Gazebo controllers. Note: these don't block the
        # init flow — they wait at first send_goal_async call.
        self._arm_client = ActionClient(self, FollowJointTrajectory, ARM_ACTION_TOPIC)
        self._gripper_client = ActionClient(self, FollowJointTrajectory, GRIPPER_ACTION_TOPIC)

        self.get_logger().info(
            f"Embedded interface ready arm={ARM_ACTION_TOPIC} gripper={GRIPPER_ACTION_TOPIC}"
        )

    # ------------------------------------------------------------------
    # Config
    # ------------------------------------------------------------------
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
        except Exception as exc:
            self.get_logger().warn(f"Falling back to default kiosk poses: {exc}")
            return (
                [0.0, 0.15, -0.35, 0.0, 0.10, 0.0],
                [0.0, -0.10, -0.05, 0.0, -0.05, 0.0],
                0.22,
                0.10,
            )

    def _on_robot_state(self, msg: RobotState):
        self._robot_state = msg.state

    # ------------------------------------------------------------------
    # Command guards
    # ------------------------------------------------------------------
    def _joint_pose_matches(self, actual: List[float], expected: List[float], tol: float = 0.03) -> bool:
        if len(actual) != len(expected):
            return False
        return all(abs(float(a) - float(b)) <= tol for a, b in zip(actual, expected))

    def _is_allowed_logged_out_arm_command(self, msg: ArmCommand) -> bool:
        if msg.command != "MOVE":
            return False
        if not self._joint_pose_matches(list(msg.joint_angles), self._kiosk_rest_pose) and not self._joint_pose_matches(list(msg.joint_angles), self._kiosk_interaction_pose):
            return False
        if float(msg.velocity_scale) > self._kiosk_velocity_scale + 1e-6:
            return False
        if float(msg.accel_limit) > self._kiosk_accel_limit + 1e-6:
            return False
        return True

    # ------------------------------------------------------------------
    # Feedback publishing
    # ------------------------------------------------------------------
    def _publish_feedback(self, success: bool, phase: str, error: str = "", gripper_force: float = 0.0):
        msg = MotionFeedback()
        msg.success = success
        msg.phase = phase
        msg.error = error
        msg.joint_positions = []
        msg.joint_velocities = []
        msg.joint_currents = []
        msg.temperatures = []
        msg.gripper_force = float(gripper_force)
        msg.imu_roll = 0.0
        msg.imu_pitch = 0.0
        msg.imu_yaw = 0.0
        self.feedback_pub.publish(msg)

    # ------------------------------------------------------------------
    # Trajectory builders
    # ------------------------------------------------------------------
    @staticmethod
    def _build_trajectory(
        joint_names: List[str],
        positions: List[float],
        duration_s: float,
    ) -> FollowJointTrajectory.Goal:
        traj = JointTrajectory()
        traj.joint_names = joint_names
        point = JointTrajectoryPoint()
        point.positions = [float(p) for p in positions]
        secs = int(duration_s)
        nsecs = int((duration_s - secs) * 1e9)
        point.time_from_start = Duration(sec=secs, nanosec=nsecs)
        traj.points = [point]
        goal = FollowJointTrajectory.Goal()
        goal.trajectory = traj
        return goal

    # ------------------------------------------------------------------
    # Async send helpers
    # ------------------------------------------------------------------
    def _send_goal_async(self, client: ActionClient, goal: FollowJointTrajectory.Goal, phase: str, gripper_force: float = 0.0):
        if self._estop:
            self._publish_feedback(False, phase, "estop_active")
            return
        if not client.wait_for_server(timeout_sec=2.0):
            self.get_logger().warn(f"{phase}: controller action server not available")
            self._publish_feedback(False, phase, "controller_unavailable")
            return

        future = client.send_goal_async(goal)

        def on_accepted(fut):
            handle = fut.result()
            if not handle.accepted:
                self._publish_feedback(False, phase, "goal_rejected")
                return
            result_future = handle.get_result_async()
            result_future.add_done_callback(lambda f: self._on_result(f, phase, gripper_force))

        future.add_done_callback(on_accepted)

    def _on_result(self, future, phase: str, gripper_force: float):
        try:
            result = future.result().result
            error_code = getattr(result, "error_code", 0)
        except Exception as exc:
            self._publish_feedback(False, phase, f"result_error:{exc}")
            return
        if error_code == 0:
            self._publish_feedback(True, phase, gripper_force=gripper_force)
        else:
            self._publish_feedback(False, phase, f"controller_error:{error_code}")

    # ------------------------------------------------------------------
    # Subscribers
    # ------------------------------------------------------------------
    def _on_arm_command(self, msg: ArmCommand):
        if self._robot_state == "LOGGED_OUT" and not self._is_allowed_logged_out_arm_command(msg):
            self.get_logger().warn("Rejected non-kiosk arm command while LOGGED_OUT")
            self._publish_feedback(False, f"arm_{msg.command.lower()}", "logged_out_pose_guard")
            return

        if msg.command not in {"MOVE", "MOVE_REL"}:
            self._publish_feedback(False, f"arm_{msg.command.lower()}", "unsupported_command")
            return

        positions = list(msg.joint_angles)
        if len(positions) != len(ARM_JOINT_NAMES):
            self._publish_feedback(False, f"arm_{msg.command.lower()}", f"expected_{len(ARM_JOINT_NAMES)}_joints")
            return

        # Velocity scale → trajectory duration. Faster scale → shorter duration.
        vel = max(0.05, min(1.0, float(msg.velocity_scale) or 0.5))
        duration = DEFAULT_ARM_DURATION / vel
        goal = self._build_trajectory(ARM_JOINT_NAMES, positions, duration)
        phase = f"arm_{msg.command.lower()}"
        self._send_goal_async(self._arm_client, goal, phase)

    def _on_gripper_command(self, msg: GripperCommand):
        if self._robot_state == "LOGGED_OUT" and msg.command in {"GRASP", "CLOSE"}:
            self.get_logger().warn("Rejected grasp command while LOGGED_OUT")
            self._publish_feedback(False, f"gripper_{msg.command.lower()}", "logged_out_gripper_guard")
            return

        cmd = msg.command.upper()
        if cmd in {"GRASP", "CLOSE"}:
            position = GRIPPER_CLOSE_POS
            force = float(msg.force_target)
        elif cmd in {"RELEASE", "OPEN"}:
            position = GRIPPER_OPEN_POS
            force = 0.0
        else:
            self._publish_feedback(False, f"gripper_{cmd.lower()}", "unsupported_command")
            return

        goal = self._build_trajectory(GRIPPER_JOINT_NAMES, [position], DEFAULT_GRIPPER_DURATION)
        phase = f"gripper_{cmd.lower()}"
        self._send_goal_async(self._gripper_client, goal, phase, gripper_force=force)

    def _on_estop(self, _msg: EmergencySignal):
        with self._lock:
            self._estop = True
        # Best-effort cancel of any in-flight goals (controllers will halt).
        try:
            self._arm_client.cancel_all_goals_async()
            self._gripper_client.cancel_all_goals_async()
        except Exception:
            pass
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

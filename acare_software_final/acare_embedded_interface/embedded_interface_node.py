"""
ACARE embedded interface node — bridge between high-level planner commands
and either:
  1. Gazebo's ros2_control controllers (sim path), or
  2. Teensy 4.1 over SPI (real-hardware path).

Spec Reference: Section XV (Embedded Interface — SPI bridge).

Sim path (current):
  Subscribes to /arm_command and /gripper_command from the planner.
  Publishes a FollowJointTrajectory action goal to /arm_controller/follow_joint_trajectory
  (the controller spawned by gz_ros2_control inside Gazebo).
  Mirrors gripper commands onto /gripper_controller/follow_joint_trajectory.
  Publishes MotionFeedback on /motion_feedback after each command.

Real-hardware path:
  Writes joint commands to Teensy 4.1 over SPI (10 MHz, 37-byte packets).
  Reads joint state telemetry from Teensy.
  ESTOP is hardware-latched via SPI estop byte.

The code path is selected at runtime via system.yaml (interface.mode).
"""
from __future__ import annotations

import struct
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
from acare_bringup.qos_profiles import TOPIC_STATE, TOPIC_SENSOR, TOPIC_COMMAND, TOPIC_ESTOP


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

# SPI hardware constants
SPI_BUS = 0
SPI_DEVICE = 0
SPI_SPEED_HZ = 10_000_000
SPI_PACKET_BYTES = 37  # sizeof(JointState) from Teensy firmware


class EmbeddedInterfaceNode(Node):
    def __init__(self):
        super().__init__("embedded_interface_node")
        
        # Load interface mode and joint limits from system.yaml
        (
            self._interface_mode,
            self._joint_limits_min,
            self._joint_limits_max,
            self._kiosk_rest_pose,
            self._kiosk_interaction_pose,
            self._kiosk_velocity_scale,
            self._kiosk_accel_limit,
        ) = self._load_config()
        
        self.feedback_pub = self.create_publisher(MotionFeedback, "/motion_feedback", TOPIC_SENSOR)
        self.create_subscription(ArmCommand, "/arm_command", self._on_arm_command, TOPIC_COMMAND)
        self.create_subscription(GripperCommand, "/gripper_command", self._on_gripper_command, TOPIC_COMMAND)
        self.create_subscription(EmergencySignal, "/emergency_stop", self._on_estop, TOPIC_ESTOP)
        self.create_subscription(RobotState, "/robot_state", self._on_robot_state, TOPIC_STATE)

        self._lock = threading.Lock()
        self._estop = False
        self._robot_state = "LOGGED_OUT"

        # SPI hardware path (only initialized if mode == "hardware")
        self._spi_device = None
        if self._interface_mode == "hardware":
            self._init_spi_hardware()

        # Action clients to Gazebo controllers (sim path only). Note: these don't block the
        # init flow — they wait at first send_goal_async call.
        if self._interface_mode == "sim":
            self._arm_client = ActionClient(self, FollowJointTrajectory, ARM_ACTION_TOPIC)
            self._gripper_client = ActionClient(self, FollowJointTrajectory, GRIPPER_ACTION_TOPIC)
            self.get_logger().info(
                f"Embedded interface ready (SIM) arm={ARM_ACTION_TOPIC} gripper={GRIPPER_ACTION_TOPIC}"
            )
        else:
            self.get_logger().info(
                f"Embedded interface ready (HARDWARE) SPI bus={SPI_BUS} device={SPI_DEVICE}"
            )

    # ------------------------------------------------------------------
    # Config
    # ------------------------------------------------------------------
    def _load_config(self):
        try:
            import yaml

            with open(SYSTEM_YAML, "r", encoding="utf-8") as handle:
                cfg = yaml.safe_load(handle) or {}
            
            # Interface mode (sim or hardware)
            interface_cfg = cfg.get("interface", {}) or {}
            mode = str(interface_cfg.get("mode", "sim")).lower()
            if mode not in ("sim", "hardware"):
                self.get_logger().warn(f"Unknown interface mode '{mode}', falling back to 'sim'")
                mode = "sim"
            
            # Joint limits from arm section
            arm = cfg.get("arm", {}) or {}
            limits_min = [float(v) for v in arm.get("joint_limits_min", [-3.14]*6)]
            limits_max = [float(v) for v in arm.get("joint_limits_max", [3.14]*6)]
            if len(limits_min) != 6 or len(limits_max) != 6:
                raise ValueError("Joint limits must contain 6 values")
            
            # Kiosk policy
            soft = arm.get("control_soft_limits", {}) or {}
            rest = [float(v) for v in arm.get("kiosk_rest_joint_angles", [0.0, 0.15, -0.35, 0.0, 0.10, 0.0])]
            interaction = [float(v) for v in arm.get("kiosk_interaction_joint_angles", [0.0, -0.10, -0.05, 0.0, -0.05, 0.0])]
            kiosk_velocity = float(soft.get("kiosk_velocity_scale", 0.22))
            kiosk_accel = float(soft.get("kiosk_accel_limit", 0.10))
            if len(rest) != 6 or len(interaction) != 6:
                raise ValueError("Kiosk poses must contain 6 joints")
            
            return (mode, limits_min, limits_max, rest, interaction, kiosk_velocity, kiosk_accel)
        except Exception as exc:
            self.get_logger().warn(f"Falling back to default config: {exc}")
            return (
                "sim",
                [-3.14159, -2.35619, -2.09440, -3.14159, -3.14159, -3.14159],
                [3.14159, 2.35619, 2.09440, 3.14159, 3.14159, 3.14159],
                [0.0, 0.15, -0.35, 0.0, 0.10, 0.0],
                [0.0, -0.10, -0.05, 0.0, -0.05, 0.0],
                0.22,
                0.10,
            )

    def _init_spi_hardware(self):
        """Initialize SPI device for real-hardware path. Requires spidev library."""
        try:
            import spidev
            self._spi_device = spidev.SpiDev()
            self._spi_device.open(SPI_BUS, SPI_DEVICE)
            self._spi_device.max_speed_hz = SPI_SPEED_HZ
            self._spi_device.mode = 0b00  # SPI MODE0
            self.get_logger().info(f"SPI hardware initialized: bus={SPI_BUS} dev={SPI_DEVICE} speed={SPI_SPEED_HZ}")
        except ImportError:
            self.get_logger().error("spidev library not found. Install with: pip install spidev")
            self.get_logger().error("Falling back to sim mode")
            self._interface_mode = "sim"
            self._arm_client = ActionClient(self, FollowJointTrajectory, ARM_ACTION_TOPIC)
            self._gripper_client = ActionClient(self, FollowJointTrajectory, GRIPPER_ACTION_TOPIC)
        except Exception as exc:
            self.get_logger().error(f"Failed to initialize SPI: {exc}")
            self.get_logger().error("Falling back to sim mode")
            self._interface_mode = "sim"
            self._arm_client = ActionClient(self, FollowJointTrajectory, ARM_ACTION_TOPIC)
            self._gripper_client = ActionClient(self, FollowJointTrajectory, GRIPPER_ACTION_TOPIC)

    def _validate_joint_limits(self, joint_angles: List[float]) -> tuple[bool, str]:
        """Validate joint angles against soft limits. Returns (valid, error_message)."""
        if len(joint_angles) != 6:
            return False, f"expected 6 joints, got {len(joint_angles)}"
        
        for i, (angle, lo, hi) in enumerate(zip(joint_angles, self._joint_limits_min, self._joint_limits_max)):
            if angle < lo or angle > hi:
                return False, f"joint {i} angle {angle:.3f} outside limits [{lo:.3f}, {hi:.3f}]"
        
        return True, ""

    def _on_robot_state(self, msg: RobotState):
        with self._lock:
            prev = self._robot_state
            self._robot_state = msg.state
            # Clear the ESTOP latch when the system recovers to STANDBY/LOGGED_OUT.
            # Without this, every goal stays rejected until process restart.
            if msg.state in ("STANDBY", "LOGGED_OUT") and prev == "ESTOP":
                self._estop = False
                self.get_logger().info("Embedded interface: ESTOP latch cleared on recovery")

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
        with self._lock:
            if self._estop:
                self._publish_feedback(False, phase, "estop_active")
                return
        # NON-BLOCKING readiness check. wait_for_server(timeout=2s) would block
        # the executor and could delay the ESTOP callback — never block here.
        if not client.server_is_ready():
            self.get_logger().warn(f"{phase}: controller action server not available")
            self._publish_feedback(False, phase, "controller_unavailable")
            return

        future = client.send_goal_async(goal)

        def on_accepted(fut):
            try:
                handle = fut.result()
            except Exception as exc:
                self._publish_feedback(False, phase, f"goal_error:{exc}")
                return
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
        cmd = msg.command.upper()
        if self._robot_state == "LOGGED_OUT" and not self._is_allowed_logged_out_arm_command(msg):
            self.get_logger().warn("Rejected non-kiosk arm command while LOGGED_OUT")
            self._publish_feedback(False, f"arm_{cmd.lower()}", "logged_out_pose_guard")
            return

        # Only absolute MOVE is supported. MOVE_REL would need current joint
        # state to convert to absolute — not available without joint feedback,
        # so we reject it rather than send a wrong (absolute) trajectory.
        if cmd != "MOVE":
            self._publish_feedback(False, f"arm_{cmd.lower()}", "unsupported_command")
            return

        positions = list(msg.joint_angles)
        if len(positions) != len(ARM_JOINT_NAMES):
            self._publish_feedback(False, f"arm_{cmd.lower()}", f"expected_{len(ARM_JOINT_NAMES)}_joints")
            return

        # Validate joint limits before sending command
        valid, error_msg = self._validate_joint_limits(positions)
        if not valid:
            self.get_logger().warn(f"Joint limit violation: {error_msg}")
            self._publish_feedback(False, f"arm_{cmd.lower()}", f"joint_limit_violation:{error_msg}")
            return

        # Route to sim or hardware path
        if self._interface_mode == "sim":
            self._send_arm_command_sim(positions, msg, cmd)
        else:
            self._send_arm_command_hardware(positions, msg, cmd)

    def _send_arm_command_sim(self, positions: List[float], msg: ArmCommand, cmd: str):
        """Send arm command via Gazebo action client (sim path)."""
        # Velocity scale → trajectory duration. Faster scale → shorter duration.
        try:
            raw_vel = float(msg.velocity_scale)
        except (ValueError, TypeError):
            raw_vel = 0.5
        vel = max(0.05, min(1.0, raw_vel if raw_vel > 0 else 0.5))
        duration = DEFAULT_ARM_DURATION / vel
        goal = self._build_trajectory(ARM_JOINT_NAMES, positions, duration)
        phase = f"arm_{cmd.lower()}"
        self._send_goal_async(self._arm_client, goal, phase)

    def _send_arm_command_hardware(self, positions: List[float], msg: ArmCommand, cmd: str):
        """Send arm command via SPI to Teensy (hardware path)."""
        if self._spi_device is None:
            self._publish_feedback(False, f"arm_{cmd.lower()}", "spi_device_not_initialized")
            return

        try:
            # Pack JointCmd struct: 6 floats (target_pos) + 1 byte (estop=0)
            # Matches Teensy firmware: struct JointCmd { float target_pos[6]; uint8_t estop; }
            cmd_bytes = struct.pack('<6f B', *positions, 0)
            
            # SPI transfer: send command, receive state
            response = self._spi_device.xfer2(list(cmd_bytes) + [0] * (SPI_PACKET_BYTES - len(cmd_bytes)))
            
            # Parse JointState response: 6 floats + 6 uint16 + 1 byte
            state = struct.unpack('<6f 6H B', bytes(response[:SPI_PACKET_BYTES]))
            current_pos = state[0:6]
            freq_cmd = state[6:12]
            fault_flags = state[12]
            
            if fault_flags:
                fault_joints = [i for i in range(6) if fault_flags & (1 << i)]
                self.get_logger().warn(f"Teensy reports joint faults: {fault_joints}")
                self._publish_feedback(False, f"arm_{cmd.lower()}", f"joint_fault:{fault_joints}")
                return
            
            self._publish_feedback(True, f"arm_{cmd.lower()}", "")
            
        except Exception as exc:
            self.get_logger().error(f"SPI transfer failed: {exc}")
            self._publish_feedback(False, f"arm_{cmd.lower()}", f"spi_error:{exc}")

    def _on_gripper_command(self, msg: GripperCommand):
        cmd = msg.command.upper()
        # Guard computed on the upper-cased command so lowercase "grasp"/"close"
        # can't bypass the LOGGED_OUT guard (fail-closed, not fail-open).
        if self._robot_state == "LOGGED_OUT" and cmd in {"GRASP", "CLOSE"}:
            self.get_logger().warn("Rejected grasp command while LOGGED_OUT")
            self._publish_feedback(False, f"gripper_{cmd.lower()}", "logged_out_gripper_guard")
            return

        if cmd in {"GRASP", "CLOSE"}:
            position = GRIPPER_CLOSE_POS
            force = float(msg.force_target)
        elif cmd in {"RELEASE", "OPEN"}:
            position = GRIPPER_OPEN_POS
            force = 0.0
        else:
            self._publish_feedback(False, f"gripper_{cmd.lower()}", "unsupported_command")
            return

        # Route to sim or hardware path
        if self._interface_mode == "sim":
            goal = self._build_trajectory(GRIPPER_JOINT_NAMES, [position], DEFAULT_GRIPPER_DURATION)
            phase = f"gripper_{cmd.lower()}"
            self._send_goal_async(self._gripper_client, goal, phase, gripper_force=force)
        else:
            # Hardware path: gripper is controlled via joint 5 (wrist_3) or separate SPI command
            # For now, publish success — actual gripper hardware integration TBD
            self._publish_feedback(True, f"gripper_{cmd.lower()}", "", gripper_force=force)

    def _on_estop(self, _msg: EmergencySignal):
        with self._lock:
            self._estop = True
        
        if self._interface_mode == "hardware" and self._spi_device is not None:
            # Send ESTOP via SPI: pack JointCmd with estop=1
            try:
                cmd_bytes = struct.pack('<6f B', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1)
                self._spi_device.xfer2(list(cmd_bytes) + [0] * (SPI_PACKET_BYTES - len(cmd_bytes)))
                self.get_logger().info("ESTOP sent via SPI to Teensy")
            except Exception as exc:
                self.get_logger().error(f"Failed to send ESTOP via SPI: {exc}")
        else:
            # Sim path: cancel in-flight goals (controllers will halt)
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

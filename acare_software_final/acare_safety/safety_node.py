# acare_safety/safety_node.py
# Spec Reference: Section XIII (Emergency Stop System — Trigger 2)
# Section XIV (LiDAR Safety System)
#
# Monitors two safety inputs:
#   1. LiDAR proximity — YDLIDAR T-mini Plus on /scan topic
#   2. MCU telemetry — joint currents, temperatures, gripper force on /motion_feedback
#
# Publishes SafetyAlert to /safety_alert with severity:
#   WARNING  — reduce velocity, continue task
#   CRITICAL — reduce velocity 50%, continue task
#   ESTOP    — immediate stop, safe deposit if holding
#
# Thresholds loaded from thresholds.yaml.
# All threshold values are non-negotiable per spec.
#
# LiDAR zones:
#   > 600mm  — safe, full velocity
#   400-600mm — caution, WARNING
#   < 400mm  — danger, ESTOP
#
# Known limitation: LiDAR at 80cm height detects torso only.
# A hand entering from below is not detected.

import yaml
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan
from acare_bringup.paths import THRESHOLDS_YAML

try:
    from acare_msgs.msg import SafetyAlert, MotionFeedback
    MSGS_OK = True
except ImportError:
    MSGS_OK = False

THRESHOLDS_PATH = THRESHOLDS_YAML

# Defaults — overridden by thresholds.yaml
DEFAULTS = {
    'current_limit_A':        8.0,
    'current_warning_A':      6.0,
    'temperature_estop_C':   75.0,
    'temperature_slow_C':    65.0,
    'temperature_warning_C': 55.0,
    'velocity_limit_degs':  120.0,
    'lidar_caution_mm':      600,
    'lidar_stop_mm':         400,
    'gripper_force_limit_N':  15.0,
    'gripper_force_warning_N':10.0,
}


class SafetyNode(Node):
    """
    Monitors LiDAR proximity and MCU telemetry.
    Publishes graded SafetyAlert messages to /safety_alert.

    Uses BEST_EFFORT QoS for sensor data (always use latest, drop stale).
    Uses RELIABLE QoS for safety alerts (must be delivered).
    """

    def __init__(self):
        super().__init__('safety_node')
        self.T = dict(DEFAULTS)
        self._load_thresholds()

        if not MSGS_OK:
            self.get_logger().error('acare_msgs not available — safety_node cannot run')
            return

        # RELIABLE QoS for alerts — must not be dropped
        self.alert_pub = self.create_publisher(SafetyAlert, '/safety_alert', 10)

        # BEST_EFFORT for sensor data — always use latest
        sensor_qos = QoSProfile(depth=10,
                                reliability=ReliabilityPolicy.BEST_EFFORT)

        self.create_subscription(LaserScan, '/scan',
                                 self._on_lidar, sensor_qos)
        self.create_subscription(MotionFeedback, '/motion_feedback',
                                 self._on_telemetry, sensor_qos)

        self.get_logger().info('Safety node ready')

    def _load_thresholds(self):
        if not THRESHOLDS_PATH.exists():
            return
        try:
            with open(THRESHOLDS_PATH) as f:
                cfg = yaml.safe_load(f)
            self.T.update(cfg.get('safety', {}))
        except Exception as e:
            self.get_logger().warn(f'Could not load thresholds.yaml: {e} — using defaults')

    def _publish_alert(self, severity: str, reason: str, source: str):
        msg = SafetyAlert()
        msg.severity = severity
        msg.reason   = reason
        msg.source   = source
        self.alert_pub.publish(msg)
        self.get_logger().warn(f'[{severity}] {source}: {reason}')

    def _on_lidar(self, msg: LaserScan):
        """
        Checks the front arc (middle third of scan) for proximity.
        LiDAR is base-mounted at ~80cm, scanning horizontal torso plane.
        Front arc = roughly ±60° from forward direction.
        """
        n = len(msg.ranges)
        if n == 0:
            return

        # Middle third of scan = front arc
        front = msg.ranges[n // 3: 2 * n // 3]
        valid = [r for r in front
                 if msg.range_min < r < msg.range_max and r > 0]
        if not valid:
            return

        min_dist_mm = min(valid) * 1000.0   # metres → mm

        if min_dist_mm < self.T['lidar_stop_mm']:
            self._publish_alert(
                'ESTOP',
                f'Person {min_dist_mm:.0f}mm from robot (limit: {self.T["lidar_stop_mm"]}mm)',
                'lidar')
        elif min_dist_mm < self.T['lidar_caution_mm']:
            self._publish_alert(
                'WARNING',
                f'Person {min_dist_mm:.0f}mm — reduced speed',
                'lidar')

    def _on_telemetry(self, msg: MotionFeedback):
        """
        Checks MCU telemetry at 50Hz for safety threshold violations.
        Checks: joint currents, joint temperatures, gripper force.
        """
        # Joint currents
        for i, curr in enumerate(msg.joint_currents):
            if curr > self.T['current_limit_A']:
                self._publish_alert(
                    'ESTOP',
                    f'Joint {i+1} overcurrent {curr:.1f}A (limit: {self.T["current_limit_A"]}A)',
                    'current')
            elif curr > self.T['current_warning_A']:
                self._publish_alert(
                    'WARNING',
                    f'Joint {i+1} current {curr:.1f}A',
                    'current')

        # Joint temperatures
        for i, temp in enumerate(msg.temperatures):
            if temp > self.T['temperature_estop_C']:
                self._publish_alert(
                    'ESTOP',
                    f'Joint {i+1} overtemp {temp:.1f}°C (limit: {self.T["temperature_estop_C"]}°C)',
                    'temp')
            elif temp > self.T['temperature_slow_C']:
                self._publish_alert(
                    'CRITICAL',
                    f'Joint {i+1} temp {temp:.1f}°C — thermal limit approaching',
                    'temp')
            elif temp > self.T['temperature_warning_C']:
                self._publish_alert(
                    'WARNING',
                    f'Joint {i+1} temp {temp:.1f}°C',
                    'temp')

        # Gripper force
        if msg.gripper_force > self.T['gripper_force_limit_N']:
            self._publish_alert(
                'ESTOP',
                f'Gripper force spike {msg.gripper_force:.1f}N (limit: {self.T["gripper_force_limit_N"]}N)',
                'gripper')
        elif msg.gripper_force > self.T['gripper_force_warning_N']:
            self._publish_alert(
                'WARNING',
                f'Gripper force {msg.gripper_force:.1f}N',
                'gripper')


def main(args=None):
    rclpy.init(args=args)
    node = SafetyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

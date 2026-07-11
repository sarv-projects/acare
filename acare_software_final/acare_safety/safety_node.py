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
# CAUTION: Software-only ESTOPs over a ROS2 network with Python GIL latency 
# are critically unviable for real-world surgical robots. A hardwired physical 
# ESTOP circuit MUST be implemented for ISO medical compliance.
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

import time
import threading
import yaml
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan
from acare_bringup.paths import THRESHOLDS_YAML
from acare_bringup.qos_profiles import TOPIC_SENSOR, TOPIC_STATE, TOPIC_COMMAND, TOPIC_ESTOP

try:
    from acare_msgs.msg import SafetyAlert, MotionFeedback, EmergencySignal
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

    Recovery: a periodic timer checks if all safety conditions have cleared
    and publishes an OK alert so downstream nodes know the danger has passed.
    """

    RECOVERY_CHECK_PERIOD_S = 2.0
    RECOVERY_QUIET_PERIOD_S = 5.0

    def __init__(self):
        super().__init__('safety_node')
        self.T = dict(DEFAULTS)
        self._load_thresholds()

        self._last_alert_times = {}
        self._alert_throttle_s = 1.0

        self._active_conditions: dict[str, float] = {}
        self._lock = threading.Lock()
        self._espress_latched = False

        if not MSGS_OK:
            self.get_logger().error('acare_msgs not available — safety_node cannot run')
            return

        self.alert_pub = self.create_publisher(SafetyAlert, '/safety_alert', TOPIC_STATE)

        # Dedicated /emergency_stop publisher (redundant ESTOP path)
        self._estop_pub = self.create_publisher(EmergencySignal, '/emergency_stop', TOPIC_ESTOP)

        # Subscriber mirror — listen for ESTOP signals from other nodes
        self.create_subscription(EmergencySignal, '/emergency_stop',
                                 self._on_emergency_stop, TOPIC_ESTOP)

        self.create_subscription(LaserScan, '/scan',
                                 self._on_lidar, TOPIC_SENSOR)
        self.create_subscription(MotionFeedback, '/motion_feedback',
                                 self._on_telemetry, TOPIC_SENSOR)

        self._recovery_timer = self.create_timer(self.RECOVERY_CHECK_PERIOD_S, self._check_recovery)

        # Periodic self-test — verify /emergency_stop has subscribers
        self._self_test_timer = self.create_timer(30.0, self._self_test)

        self.get_logger().info('Safety node ready')
        self.get_logger().info(
            'HARDWARE REQUIREMENT: Software-only ESTOP over ROS2 with Python GIL '
            'latency is NOT sufficient for ISO medical compliance. '
            'A hardwired physical ESTOP circuit MUST be implemented in the final system. '
            'See Spec Section XIII (Emergency Stop System — Trigger 2).'
        )

    def _load_thresholds(self):
        if not THRESHOLDS_PATH.exists():
            return
        try:
            with open(THRESHOLDS_PATH) as f:
                cfg = yaml.safe_load(f)
            loaded = cfg.get('safety', {})
            for key, expected_type in [('current_limit_A', (int, float)), ('current_warning_A', (int, float)),
                                        ('temperature_estop_C', (int, float)), ('temperature_slow_C', (int, float)),
                                        ('temperature_warning_C', (int, float)), ('lidar_caution_mm', (int, float)),
                                        ('lidar_stop_mm', (int, float)), ('gripper_force_limit_N', (int, float)),
                                        ('gripper_force_warning_N', (int, float))]:
                if key in loaded and not isinstance(loaded[key], expected_type):
                    self.get_logger().warn(f'thresholds.yaml: {key} has wrong type ({type(loaded[key]).__name__}), skipping')
                    del loaded[key]
            self.T.update(loaded)
        except Exception as e:
            self.get_logger().warn(f'Could not load thresholds.yaml: {e} — using defaults')

    def _publish_alert(self, severity: str, reason: str, source: str, condition_key: str = ''):
        if not condition_key:
            condition_key = (severity, source)

        if severity != 'ESTOP':
            now = time.monotonic()
            last = self._last_alert_times.get(condition_key, 0.0)
            if (now - last) < self._alert_throttle_s:
                return
            self._last_alert_times[condition_key] = now

        with self._lock:
            self._active_conditions[condition_key] = time.monotonic()

        msg = SafetyAlert()
        msg.severity = severity
        msg.reason   = reason
        msg.source   = source
        msg.stamp    = self.get_clock().now().to_msg()
        self.alert_pub.publish(msg)

        if severity == 'ESTOP':
            # CRITICAL logging with ISO-formatted timestamp
            ts = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            self.get_logger().critical(f'[{ts}] ESTOP from {source}: {reason}')

            # stdout/stderr alert for hardware watchdog detection
            print(f'[ESTOP][{ts}] source={source} reason={reason}', flush=True)

            # Set latched ESTOP state (persists across state transitions)
            self._espress_latched = True

            # Publish to redundant /emergency_stop path
            try:
                emsg = EmergencySignal()
                emsg.stamp = self.get_clock().now().to_msg()
                emsg.reason = reason
                emsg.source = source
                self._estop_pub.publish(emsg)
            except Exception:
                self.get_logger().error('Failed to publish /emergency_stop')
        else:
            self.get_logger().warn(f'[{severity}] {source}: {reason}')

    def _check_recovery(self):
        now = time.monotonic()
        with self._lock:
            expired = [k for k, t in self._active_conditions.items()
                       if (now - t) > self.RECOVERY_QUIET_PERIOD_S]
            for k in expired:
                del self._active_conditions[k]

            if expired and not self._active_conditions:
                msg = SafetyAlert()
                msg.severity = 'OK'
                msg.reason = 'All safety conditions cleared'
                msg.source = 'safety_node'
                self.alert_pub.publish(msg)
                self.get_logger().info('[OK] All safety conditions cleared')

    def _on_emergency_stop(self, msg: EmergencySignal):
        """React to ESTOP signals from other nodes via /emergency_stop (redundant path)."""
        ts = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        self.get_logger().critical(
            f'[{ts}] External ESTOP received from {msg.source}: {msg.reason}')
        self._espress_latched = True
        print(f'[ESTOP][{ts}] external source={msg.source} reason={msg.reason}', flush=True)

    def _self_test(self):
        """Periodic self-test: verify /emergency_stop topic has at least one subscriber."""
        try:
            subs = self.get_subscriptions_info_by_topic('/emergency_stop')
            count = len(subs)
            if count == 0:
                self.get_logger().warn(
                    'SELF-TEST: /emergency_stop has NO subscribers — '
                    'ESTOP signals will not be received by any node')
            else:
                self.get_logger().debug(
                    f'SELF-TEST PASS: /emergency_stop has {count} subscriber(s)')
        except Exception as e:
            self.get_logger().warn(
                f'SELF-TEST: could not check /emergency_stop subscribers: {e}')

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

        if min_dist_mm <= self.T['lidar_stop_mm']:
            self._publish_alert(
                'ESTOP',
                f'Person {min_dist_mm:.0f}mm from robot (limit: {self.T["lidar_stop_mm"]}mm)',
                'lidar')
        elif min_dist_mm <= self.T['lidar_caution_mm']:
            self._publish_alert(
                'WARNING',
                f'Person {min_dist_mm:.0f}mm — reduced speed',
                'lidar')

    def _on_telemetry(self, msg: MotionFeedback):
        """
        Checks MCU telemetry at 50Hz for safety threshold violations.
        Checks: joint currents, joint temperatures, gripper force.
        Each joint gets its own throttle key to avoid cross-joint suppression.
        """
        for i, curr in enumerate(msg.joint_currents):
            if curr > self.T['current_limit_A']:
                self._publish_alert(
                    'ESTOP',
                    f'Joint {i+1} overcurrent {curr:.1f}A (limit: {self.T["current_limit_A"]}A)',
                    'current',
                    condition_key=f'estop_current_j{i+1}')
            elif curr > self.T['current_warning_A']:
                self._publish_alert(
                    'WARNING',
                    f'Joint {i+1} current {curr:.1f}A',
                    'current',
                    condition_key=f'warning_current_j{i+1}')

        for i, temp in enumerate(msg.temperatures):
            if temp > self.T['temperature_estop_C']:
                self._publish_alert(
                    'ESTOP',
                    f'Joint {i+1} overtemp {temp:.1f}°C (limit: {self.T["temperature_estop_C"]}°C)',
                    'temp',
                    condition_key=f'estop_temp_j{i+1}')
            elif temp > self.T['temperature_slow_C']:
                self._publish_alert(
                    'CRITICAL',
                    f'Joint {i+1} temp {temp:.1f}°C — thermal limit approaching',
                    'temp',
                    condition_key=f'critical_temp_j{i+1}')
            elif temp > self.T['temperature_warning_C']:
                self._publish_alert(
                    'WARNING',
                    f'Joint {i+1} temp {temp:.1f}°C',
                    'temp',
                    condition_key=f'warning_temp_j{i+1}')

        if msg.gripper_force > self.T['gripper_force_limit_N']:
            self._publish_alert(
                'ESTOP',
                f'Gripper force spike {msg.gripper_force:.1f}N (limit: {self.T["gripper_force_limit_N"]}N)',
                'gripper',
                condition_key='estop_gripper')
        elif msg.gripper_force > self.T['gripper_force_warning_N']:
            self._publish_alert(
                'WARNING',
                f'Gripper force {msg.gripper_force:.1f}N',
                'gripper',
                condition_key='warning_gripper')


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

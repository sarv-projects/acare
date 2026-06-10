#!/usr/bin/env python3
# acare_bringup/supervisor_node.py
# Spec Reference: Section V (Node Crash Recovery)
#
# Proper ROS2 node — runs as part of the ROS2 stack.
# Monitors all ACARE nodes via ROS2 graph discovery and handles crashes.
#
# Auto-restart (non-critical nodes):
#   log_node, admin_node, dialogue_node, voice_node, auth_node
#   (uses subprocess ros2 run for restart)
#
# No auto-restart (critical nodes) — trigger ESTOP instead:
#   safety_node, embedded_interface_node, state_manager, planner_node, vision_node
#
# Detection method: rclpy graph API (get_node_names())
# Check interval: 5 seconds (timer-based)
# ESTOP trigger: publisher on /emergency_stop

import subprocess
import rclpy
from rclpy.node import Node as RclpyNode
from rclpy.qos import QoSProfile, ReliabilityPolicy
from acare_bringup.paths import LOG_DIR
from acare_bringup.qos_profiles import TOPIC_ESTOP

try:
    from acare_msgs.msg import EmergencySignal, LogEvent, StateTransition
    from std_msgs.msg import String
    MSGS_OK = True
except ImportError:
    MSGS_OK = False

# Nodes that can be auto-restarted without triggering ESTOP
AUTO_RESTART = {'log_node', 'admin_node', 'dialogue_node', 'voice_node', 'auth_node'}
# Critical nodes — if they crash, trigger ESTOP
CRITICAL = {'safety_node', 'embedded_interface_node', 'state_manager', 'planner_node', 'vision_node'}

# ROS2 fully-qualified node names as they appear in the ROS graph
NODE_ROS_NAMES = {
    'log_node':                '/log_node',
    'admin_node':              '/admin_node',
    'dialogue_node':           '/dialogue_node',
    'voice_node':              '/voice_node',
    'auth_node':               '/auth_node',
    'safety_node':             '/safety_node',
    'embedded_interface_node': '/embedded_interface_node',
    'state_manager':           '/state_manager',
    'planner_node':            '/planner_node',
    'vision_node':             '/vision_node',
}

# Commands to start each node (used for auto-restart)
NODE_CMDS = {
    'log_node':                ['ros2', 'run', 'acare_logging',           'log_node'],
    'admin_node':              ['ros2', 'run', 'acare_admin',             'admin_node'],
    'dialogue_node':           ['ros2', 'run', 'acare_dialogue',          'dialogue_node'],
    'voice_node':              ['ros2', 'run', 'acare_voice',             'voice_node'],
    'auth_node':               ['ros2', 'run', 'acare_auth',              'auth_node'],
    'safety_node':             ['ros2', 'run', 'acare_safety',            'safety_node'],
    'embedded_interface_node': ['ros2', 'run', 'acare_embedded_interface','interface_node'],
    'state_manager':           ['ros2', 'run', 'acare_planner',           'state_manager'],
    'planner_node':            ['ros2', 'run', 'acare_planner',           'planner_node'],
    'vision_node':             ['ros2', 'run', 'acare_vision',            'vision_node'],
}


class SupervisorNode(RclpyNode):
    """Monitors all ACARE nodes via ROS2 graph discovery and handles crashes."""

    def __init__(self):
        super().__init__('supervisor_node')

        if not MSGS_OK:
            self.get_logger().error(
                'acare_msgs not available — supervisor_node cannot publish '
                'EmergencySignal. ESTOP and power recovery functionality disabled.'
            )

        # ESTOP publisher (primary monitor function)
        self._estop_pub = None
        if MSGS_OK:
            self._estop_pub = self.create_publisher(
                EmergencySignal, '/emergency_stop', TOPIC_ESTOP
            )

        # Check power recovery condition on startup (Spec Section XVII)
        self._check_power_recovery()

        # Start 5-second monitoring timer (replaces while + sleep loop)
        self._timer = self.create_timer(5.0, self._check_nodes)

        self.get_logger().info('Supervisor node ready. Monitoring interval: 5s')

    # ------------------------------------------------------------------
    # Node discovery & health monitoring
    # ------------------------------------------------------------------

    def _check_nodes(self):
        """Periodic check: discover alive nodes via ROS2 graph and handle failures."""
        alive_nodes = self.get_node_names()
        for name, ros_name in NODE_ROS_NAMES.items():
            if ros_name not in alive_nodes:
                self.get_logger().warn(
                    '%s (%s) not found in ROS2 graph', name, ros_name
                )
                if name in AUTO_RESTART:
                    self._restart_node(name)
                elif name in CRITICAL:
                    self._trigger_estop(f'Critical node {name} crashed')

    def _restart_node(self, name: str):
        """Restart a non-critical node via subprocess."""
        cmd = NODE_CMDS.get(name)
        if not cmd:
            self.get_logger().error('Unknown node: %s', name)
            return
        try:
            self.get_logger().warn('Restarting %s...', name)
            subprocess.Popen(cmd)
            self.get_logger().info('%s restart initiated', name)
        except Exception as e:
            self.get_logger().error('Failed to restart %s: %s', name, e)

    def _trigger_estop(self, reason: str):
        """Publish EmergencySignal to /emergency_stop."""
        if not self._estop_pub:
            self.get_logger().error(
                'Cannot publish ESTOP — acare_msgs not available. Reason: %s',
                reason,
            )
            return
        msg = EmergencySignal()
        msg.stamp = self.get_clock().now().to_msg()
        msg.reason = reason
        msg.source = 'supervisor'
        self._estop_pub.publish(msg)
        self.get_logger().warn('ESTOP TRIGGERED: %s', reason)

    # ------------------------------------------------------------------
    # Power Recovery (Spec Section XVII)
    # ------------------------------------------------------------------

    def _check_power_recovery(self):
        """Check SQLite database for last known state before shutdown.

        If the last state was EXECUTING, HOLDING, or HANDOVER, the arm was
        mid-task during an unexpected shutdown. Publishes safe-state
        transition, TTS warning, and log event.
        """
        import sqlite3

        db_path = LOG_DIR / 'acare_logs.db'
        if not db_path.exists():
            self.get_logger().info('No log DB found — clean boot.')
            return

        try:
            conn = sqlite3.connect(str(db_path))
            row = conn.execute(
                'SELECT state FROM events ORDER BY timestamp DESC LIMIT 1'
            ).fetchone()
            conn.close()

            if row is None:
                return

            last_state = str(row[0]).upper()
            self.get_logger().info('Last known state from DB: %s', last_state)

            if last_state in {'EXECUTING', 'HOLDING', 'HANDOVER'}:
                self.get_logger().warn(
                    'POWER_RECOVERY: last state was mid-task. Publishing safe state.'
                )
                self._publish_recovery_signals()

        except Exception as e:
            self.get_logger().error('Power recovery check failed: %s', e)

    def _publish_recovery_signals(self):
        """Publish power recovery signals: safe state, TTS, and log event."""
        if not MSGS_OK:
            self.get_logger().error(
                'Cannot publish power recovery signals — acare_msgs not available. '
                'Falling back to subprocess ros2 topic pub.'
            )
            self._publish_recovery_signals_subprocess()
            return

        # Create transient publishers for recovery signals
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            depth=10,
        )
        best_effort_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            depth=10,
        )

        state_pub = self.create_publisher(
            StateTransition, '/state_transition', reliable_qos
        )
        tts_pub = self.create_publisher(
            String, '/tts_request', reliable_qos
        )
        log_pub = self.create_publisher(
            LogEvent, '/log_event', best_effort_qos
        )

        # Brief pause to allow subscriber discovery
        import time
        time.sleep(0.5)

        # 1. State transition to STANDBY
        state_msg = StateTransition()
        state_msg.target_state = 'STANDBY'
        state_msg.reason = 'power_recovery'
        state_pub.publish(state_msg)
        self.get_logger().info('Published /state_transition -> STANDBY (power_recovery)')

        # 2. TTS warning
        tts_msg = String()
        tts_msg.data = 'System recovered from unexpected shutdown. Please verify workspace.'
        tts_pub.publish(tts_msg)
        self.get_logger().info('Published /tts_request')

        # 3. Log event
        log_msg = LogEvent()
        log_msg.event_type = 'POWER_RECOVERY'
        log_msg.user_id = ''
        log_msg.tool = ''
        log_msg.state = 'STANDBY'
        log_msg.description = 'Recovered from unexpected shutdown'
        log_msg.timestamp = 0
        log_msg.voice_e2e_ms = 0
        log_msg.vision_search_ms = 0
        log_msg.motion_ms = 0
        log_msg.total_task_ms = 0
        log_msg.safety_severity = ''
        log_pub.publish(log_msg)
        self.get_logger().info('Published /log_event (POWER_RECOVERY)')

    def _publish_recovery_signals_subprocess(self):
        """Fallback: use subprocess ros2 topic pub for recovery signals."""
        def _pub(topic, msg_type, payload):
            try:
                subprocess.run(
                    ['ros2', 'topic', 'pub', '--once', topic, msg_type, payload],
                    timeout=5.0,
                )
            except Exception as e:
                self.get_logger().error('Failed to publish %s: %s', topic, e)

        _pub(
            '/state_transition', 'acare_msgs/msg/StateTransition',
            '{target_state: "STANDBY", reason: "power_recovery"}',
        )
        _pub(
            '/tts_request', 'std_msgs/msg/String',
            '{data: "System recovered from unexpected shutdown. Please verify workspace."}',
        )
        _pub(
            '/log_event', 'acare_msgs/msg/LogEvent',
            ('{event_type: "POWER_RECOVERY", user_id: "", tool: "", '
             'state: "STANDBY", description: "Recovered from unexpected shutdown", '
             'timestamp: 0, voice_e2e_ms: 0, vision_search_ms: 0, '
             'motion_ms: 0, total_task_ms: 0, safety_severity: ""}'),
        )


def main(args=None):
    rclpy.init(args=args)
    node = SupervisorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

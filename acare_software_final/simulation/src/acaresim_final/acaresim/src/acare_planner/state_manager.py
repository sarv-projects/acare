# acare_planner/state_manager.py
# Spec Reference: Section VI (Global Robot State Machine)
#
# Enforces the global robot state machine.
# All state transitions go through this node — no node changes state directly.
# Publishes /robot_state after every valid transition.
#
# Valid states: OFFLINE, LOGGED_OUT, STANDBY, LISTENING, PROCESSING,
#               EXECUTING, HOLDING, HANDOVER, ESTOP, ERROR
#
# Logout guard: logout rejected from EXECUTING, HOLDING, HANDOVER.
# ESTOP override: any ESTOP safety alert immediately transitions to ESTOP.
# Inactivity timeout: 5 minutes in STANDBY → auto-logout.

import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

try:
    from acare_msgs.msg import RobotState, StateTransition, SafetyAlert
    MSGS_OK = True
except ImportError:
    MSGS_OK = False

VALID_TRANSITIONS = {
    'OFFLINE':    {'LOGGED_OUT', 'ESTOP'},
    'LOGGED_OUT': {'STANDBY', 'ESTOP'},
    'STANDBY':    {'LISTENING', 'LOGGED_OUT', 'ESTOP'},
    'LISTENING':  {'PROCESSING', 'STANDBY', 'ESTOP'},
    'PROCESSING': {'EXECUTING', 'STANDBY', 'ESTOP'},
    'EXECUTING':  {'HOLDING', 'ESTOP'},
    'HOLDING':    {'HANDOVER', 'ESTOP'},
    'HANDOVER':   {'STANDBY', 'ESTOP'},
    'ESTOP':      {'STANDBY'},
    'ERROR':      {'OFFLINE'},
}

NO_LOGOUT_FROM = {'EXECUTING', 'HOLDING', 'HANDOVER'}
INACTIVITY_TIMEOUT_S = 300.0   # 5 minutes


class StateManager(Node):

    def __init__(self):
        super().__init__('state_manager')
        self.state = 'OFFLINE'
        self.active_user_id = ''
        self._lock = threading.Lock()
        self._inactivity_timer = None

        if MSGS_OK:
            self.state_pub = self.create_publisher(RobotState, '/robot_state', 10)
            self.create_subscription(StateTransition, '/state_transition',
                                     self._on_transition, 10)
            self.create_subscription(SafetyAlert, '/safety_alert',
                                     self._on_safety_alert, 10)
        else:
            self.get_logger().error('acare_msgs not available — state_manager cannot run')
            return

        # Boot into LOGGED_OUT
        self._transition('LOGGED_OUT')
        self.get_logger().info('State manager ready')

    def _on_transition(self, msg: 'StateTransition'):
        with self._lock:
            target = msg.target_state
            reason = msg.reason if hasattr(msg, 'reason') else ''

            # Logout guard
            if target == 'LOGGED_OUT' and self.state in NO_LOGOUT_FROM:
                self.get_logger().warn(
                    f'Logout rejected — cannot logout from {self.state}')
                return

            self._transition(target, reason)

    def _on_safety_alert(self, msg: 'SafetyAlert'):
        if msg.severity == 'ESTOP':
            with self._lock:
                self._transition('ESTOP', f'Safety: {msg.source} — {msg.reason}')

    def _transition(self, target: str, reason: str = ''):
        """
        Performs a state transition if valid.
        Publishes /robot_state after every successful transition.
        Resets inactivity timer when entering STANDBY.
        """
        allowed = VALID_TRANSITIONS.get(self.state, set())
        if target not in allowed and target != self.state:
            self.get_logger().error(
                f'Invalid transition {self.state} → {target} (reason: {reason})')
            return

        prev = self.state
        self.state = target

        msg = RobotState()
        msg.state = target
        msg.active_user_id = self.active_user_id
        self.state_pub.publish(msg)

        self.get_logger().info(f'State: {prev} → {target}' +
                               (f' [{reason}]' if reason else ''))

        # Manage inactivity timer
        self._reset_inactivity_timer()

    def _reset_inactivity_timer(self):
        if self._inactivity_timer:
            self._inactivity_timer.cancel()
            self._inactivity_timer = None

        if self.state == 'STANDBY':
            self._inactivity_timer = threading.Timer(
                INACTIVITY_TIMEOUT_S, self._auto_logout)
            self._inactivity_timer.daemon = True
            self._inactivity_timer.start()

    def _auto_logout(self):
        with self._lock:
            self.get_logger().info('Session timeout — auto-logout')
            self._transition('LOGGED_OUT', 'inactivity timeout')

    def destroy_node(self):
        if self._inactivity_timer:
            self._inactivity_timer.cancel()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = StateManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

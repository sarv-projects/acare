# acare_planner/state_manager.py
# Spec Reference: Section VI (Global Robot State Machine)
#
# Enforces the global robot state machine.
# All state transitions go through this node — no node changes state directly.
# Publishes /robot_state after every valid transition.
# Subscribes to /emergency_stop (EmergencySignal) for supervisor ESTOP routing.
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
from acare_bringup.qos_profiles import TOPIC_STATE, TOPIC_VOICE_PIPELINE, TOPIC_TTS, TOPIC_ESTOP

try:
    from acare_msgs.msg import RobotState, StateTransition, SafetyAlert, AuthResult, EmergencySignal
    MSGS_OK = True
except ImportError:
    MSGS_OK = False

VALID_TRANSITIONS = {
    'OFFLINE':    {'LOGGED_OUT'},
    'LOGGED_OUT': {'STANDBY'},
    # STANDBY can go to LISTENING (voice-driven flow: STANDBY→LISTENING→PROCESSING)
    # or directly to PROCESSING (planner-driven flow: task received while in STANDBY).
    # Both paths are valid — the planner skips LISTENING when it already has a
    # validated intent and goes straight to task execution.
    'STANDBY':    {'LISTENING', 'PROCESSING', 'LOGGED_OUT'},
    'LISTENING':  {'PROCESSING', 'STANDBY'},
    'PROCESSING': {'EXECUTING', 'STANDBY'},
    'EXECUTING':  {'HOLDING', 'ESTOP'},
    'HOLDING':    {'HANDOVER', 'ESTOP'},
    'HANDOVER':   {'STANDBY', 'ESTOP'},
    'ESTOP':      {'STANDBY'},
    'ERROR':      {'OFFLINE'},
}

NO_LOGOUT_FROM = {'EXECUTING', 'HOLDING', 'HANDOVER'}
INACTIVITY_TIMEOUT_S = 300.0    # 5 minutes — spec Section VII
HARD_TTL_DEFAULT_S   = 7200.0   # 2 hours  — spec Section VII (session_hard_ttl_seconds)


class StateManager(Node):

    def __init__(self):
        super().__init__('state_manager')
        self.state = 'OFFLINE'
        self.active_user_id = ''
        self._lock = threading.Lock()
        self._inactivity_timer = None
        self._hard_ttl_timer = None   # spec Section VII: 2-hour hard TTL
        self._hard_ttl_s = HARD_TTL_DEFAULT_S
        self._tts_pub = None   # set up after publishers ready

        if MSGS_OK:
            self.state_pub = self.create_publisher(RobotState, '/robot_state', TOPIC_STATE)
            self._tts_pub = self.create_publisher(__import__('std_msgs.msg', fromlist=['String']).String, '/tts_request', TOPIC_TTS)
            self.create_subscription(StateTransition, '/state_transition',
                                     self._on_transition, TOPIC_STATE)
            self.create_subscription(SafetyAlert, '/safety_alert',
                                     self._on_safety_alert, TOPIC_STATE)
            self.create_subscription(AuthResult, '/auth_result',
                                     self._on_auth_result, TOPIC_VOICE_PIPELINE)
            self.create_subscription(EmergencySignal, '/emergency_stop',
                                     self._on_emergency_stop, TOPIC_ESTOP)
        else:
            self.get_logger().error('acare_msgs not available — state_manager cannot run')
            return

        # Load hard TTL from system.yaml if available
        self._hard_ttl_s = self._load_hard_ttl()

        # Boot into LOGGED_OUT
        self._transition('LOGGED_OUT')
        self._publish_current_state()
        self.get_logger().info(
            f'State manager ready — inactivity={INACTIVITY_TIMEOUT_S}s '
            f'hard_ttl={self._hard_ttl_s}s'
        )

    def _load_hard_ttl(self) -> float:
        try:
            import yaml
            from acare_bringup.paths import SYSTEM_YAML
            with open(SYSTEM_YAML) as f:
                cfg = yaml.safe_load(f) or {}
            return float(cfg.get('voice', {}).get('session_hard_ttl_seconds', HARD_TTL_DEFAULT_S))
        except Exception:
            return HARD_TTL_DEFAULT_S

    def _say(self, text: str):
        if self._tts_pub:
            from std_msgs.msg import String
            self._tts_pub.publish(String(data=text))

    def _on_transition(self, msg: 'StateTransition'):
        target = msg.target_state
        reason = msg.reason if hasattr(msg, 'reason') else ''
        with self._lock:
            # Logout guard
            if target == 'LOGGED_OUT' and self.state in NO_LOGOUT_FROM:
                self.get_logger().warn(
                    f'Logout rejected — cannot logout from {self.state}')
                return

            self._transition(target, reason)
        self._publish_current_state()

    def _on_safety_alert(self, msg: 'SafetyAlert'):
        with self._lock:
            if msg.severity == 'ESTOP':
                self._transition('ESTOP', f'Safety: {msg.source} — {msg.reason}')
            elif msg.severity == 'OK' and self.state == 'ESTOP':
                self._transition('STANDBY', f'Safety cleared: {msg.source} — {msg.reason}')
        self._publish_current_state()

    def _on_emergency_stop(self, msg: 'EmergencySignal'):
        with self._lock:
            self._transition('ESTOP', f'Emergency: {msg.source} — {msg.reason}')
        self._publish_current_state()

    def _on_auth_result(self, msg: 'AuthResult'):
        with self._lock:
            if msg.success and msg.user_id:
                self.active_user_id = msg.user_id
                if self.state == 'LOGGED_OUT':
                    self._transition('STANDBY', f'auth:{msg.user_id}')
                    self._start_hard_ttl()   # spec Section VII: 2-hour hard TTL starts at login
        self._publish_current_state()

    def _publish_current_state(self):
        msg = RobotState()
        with self._lock:
            msg.state = self.state
            msg.active_user_id = self.active_user_id
        self.state_pub.publish(msg)

    def _transition(self, target: str, reason: str = ''):
        """
        Performs a state transition if valid.
        Caller is responsible for publishing via _publish_current_state()
        after releasing self._lock.
        Resets inactivity timer when entering STANDBY.
        """
        # ESTOP and ERROR are always reachable from ANY state — safety overrides
        # the transition table. This is non-negotiable per spec Section XIII.
        if target in ('ESTOP', 'ERROR'):
            pass
        else:
            allowed = VALID_TRANSITIONS.get(self.state, set())
            if target not in allowed and target != self.state:
                self.get_logger().error(
                    f'Invalid transition {self.state} → {target} (reason: {reason})')
                return

        prev = self.state
        self.state = target

        if target == 'LOGGED_OUT':
            self.active_user_id = ''
            self._cancel_hard_ttl()   # cancel hard TTL on any logout

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
                INACTIVITY_TIMEOUT_S, self._auto_logout_inactivity)
            self._inactivity_timer.daemon = True
            self._inactivity_timer.start()

    def _start_hard_ttl(self):
        """Spec Section VII: 2-hour hard TTL regardless of activity."""
        self._cancel_hard_ttl()
        self._hard_ttl_timer = threading.Timer(self._hard_ttl_s, self._auto_logout_hard_ttl)
        self._hard_ttl_timer.daemon = True
        self._hard_ttl_timer.start()

    def _cancel_hard_ttl(self):
        if self._hard_ttl_timer:
            self._hard_ttl_timer.cancel()
            self._hard_ttl_timer = None

    def _auto_logout_inactivity(self):
        with self._lock:
            name = self.active_user_id or 'user'
            self.get_logger().info('Session inactivity timeout — auto-logout')
            self._say(f'Session timeout. Logging out.')
            self._cancel_hard_ttl()
            self._transition('LOGGED_OUT', 'inactivity_timeout')
        self._publish_current_state()

    def _auto_logout_hard_ttl(self):
        with self._lock:
            self.get_logger().info('Session hard TTL expired — auto-logout')
            self._say('Session time limit reached. Logging out.')
            self._transition('LOGGED_OUT', 'hard_ttl_expired')
        self._publish_current_state()

    def destroy_node(self):
        if self._inactivity_timer:
            self._inactivity_timer.cancel()
        self._cancel_hard_ttl()
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

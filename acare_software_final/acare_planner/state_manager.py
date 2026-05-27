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
# ESTOP override: any ESTOP safety alert immediately transitions to ESTOP
#                 from ANY state (per spec design.md "Any → ESTOP").
# Inactivity timeout: 5 minutes in STANDBY → auto-logout.
#
# Persistence: every transition is written to a single-row SQLite table
# (~/.acare/state.db, override with $ACARE_STATE_DIR). On boot, recover_state()
# reads the last persisted state. If the last state was mid-task
# (EXECUTING, HOLDING, HANDOVER) the recovered state is collapsed to STANDBY
# for safety, and a /tts_request alert is emitted.

import os
import threading
import time
from pathlib import Path

import rclpy
import sqlite3
from rclpy.node import Node
from std_msgs.msg import String

from acare_bringup.qos_profiles import TOPIC_STATE, TOPIC_VOICE_PIPELINE, TOPIC_TTS
from acare_bringup.paths import STATE_DB

try:
    from acare_msgs.msg import RobotState, StateTransition, SafetyAlert, AuthResult
    MSGS_OK = True
except ImportError:
    MSGS_OK = False

ALL_STATES = {
    'OFFLINE', 'LOGGED_OUT', 'STANDBY', 'LISTENING', 'PROCESSING',
    'EXECUTING', 'HOLDING', 'HANDOVER', 'ESTOP', 'ERROR',
}

# Transitions allowed when nothing has gone wrong. ESTOP/ERROR edges
# are added below so the table can be amended in one place.
VALID_TRANSITIONS = {
    'OFFLINE':    {'LOGGED_OUT'},
    'LOGGED_OUT': {'STANDBY', 'OFFLINE'},
    'STANDBY':    {'LISTENING', 'LOGGED_OUT', 'STANDBY'},
    'LISTENING':  {'PROCESSING', 'STANDBY'},
    'PROCESSING': {'EXECUTING', 'STANDBY', 'LISTENING'},
    'EXECUTING':  {'HOLDING', 'STANDBY'},
    'HOLDING':    {'HANDOVER', 'STANDBY'},
    'HANDOVER':   {'STANDBY', 'HOLDING'},
    'ESTOP':      {'STANDBY', 'LOGGED_OUT', 'ERROR'},
    'ERROR':      {'OFFLINE', 'LOGGED_OUT'},
}

# Spec Section VI: ESTOP overrides everything. Any state may transition to ESTOP.
for _state in ALL_STATES:
    VALID_TRANSITIONS.setdefault(_state, set()).add('ESTOP')

# Any operational state may degrade to ERROR on a fault that is not safety-class.
for _state in ('STANDBY', 'LISTENING', 'PROCESSING', 'EXECUTING',
               'HOLDING', 'HANDOVER', 'ESTOP'):
    VALID_TRANSITIONS.setdefault(_state, set()).add('ERROR')

NO_LOGOUT_FROM = {'EXECUTING', 'HOLDING', 'HANDOVER'}
INACTIVITY_TIMEOUT_S = 300.0    # 5 minutes — spec Section VII
HARD_TTL_DEFAULT_S   = 7200.0   # 2 hours  — spec Section VII (session_hard_ttl_seconds)

# States that mean "the arm was actively manipulating something". After an
# unexpected reboot we never resume these — we collapse to STANDBY and warn.
UNSAFE_RECOVERY_STATES = {'EXECUTING', 'HOLDING', 'HANDOVER'}


def _state_db_path() -> Path:
    """Resolve the persistent state DB to a writable, user-owned location.

    Delegates to acare_bringup.paths.STATE_DB which honours $ACARE_DATA_DIR
    and falls back to ~/.acare. Never written inside the colcon install
    tree, which gets blown away by every `colcon build`.
    """
    STATE_DB.parent.mkdir(parents=True, exist_ok=True)
    return STATE_DB


class StateManager(Node):

    STATE_DB_SCHEMA = """
    CREATE TABLE IF NOT EXISTS state_snapshot (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        state TEXT NOT NULL,
        active_user_id TEXT NOT NULL DEFAULT '',
        reason TEXT NOT NULL DEFAULT '',
        updated_at INTEGER NOT NULL
    );
    """

    def __init__(self):
        super().__init__('state_manager')
        self.state = 'OFFLINE'
        self.active_user_id = ''
        self._lock = threading.Lock()
        self._inactivity_timer = None
        self._hard_ttl_timer = None
        self._hard_ttl_s = HARD_TTL_DEFAULT_S
        self._tts_pub = None

        # Persistence — SQLite single-row table for crash recovery.
        self._state_db_path = _state_db_path()
        self._state_conn = sqlite3.connect(str(self._state_db_path), check_same_thread=False)
        self._state_conn.execute(self.STATE_DB_SCHEMA)
        self._state_conn.commit()

        if MSGS_OK:
            self.state_pub = self.create_publisher(RobotState, '/robot_state', TOPIC_STATE)
            self._tts_pub = self.create_publisher(String, '/tts_request', TOPIC_TTS)
            self.create_subscription(StateTransition, '/state_transition',
                                     self._on_transition, TOPIC_STATE)
            self.create_subscription(SafetyAlert, '/safety_alert',
                                     self._on_safety_alert, TOPIC_STATE)
            self.create_subscription(AuthResult, '/auth_result',
                                     self._on_auth_result, TOPIC_VOICE_PIPELINE)
        else:
            self.get_logger().error('acare_msgs not available — state_manager cannot run')
            return

        self._hard_ttl_s = self._load_hard_ttl()

        # Try to recover from a previous run.
        recovered_state, recovered_user, recovered_reason = self._recover_state_locked()
        if recovered_state is None:
            # Clean boot — go to LOGGED_OUT.
            self._transition('LOGGED_OUT', 'cold_boot')
        else:
            # Preserve any active session id; the auth subsystem will revalidate.
            self.active_user_id = recovered_user or ''
            self.state = 'OFFLINE'  # ensure transition table accepts the recovered target
            VALID_TRANSITIONS.setdefault('OFFLINE', set()).add(recovered_state)
            self._transition(recovered_state, f'recovered:{recovered_reason}')
            if recovered_state == 'STANDBY' and recovered_reason.startswith('unsafe_state_collapse'):
                self._say(
                    'System recovered from an unexpected shutdown. '
                    'Please verify the workspace before continuing.'
                )

        self.get_logger().info(
            f'State manager ready — inactivity={INACTIVITY_TIMEOUT_S}s '
            f'hard_ttl={self._hard_ttl_s}s state_db={self._state_db_path}'
        )

    # -------------------------------------------------------------------- #
    # Persistence                                                          #
    # -------------------------------------------------------------------- #

    def persist_state(self, reason: str = '') -> None:
        """Write the current state to disk. Called after every transition.

        Failures are swallowed and logged — persistence MUST NOT block or
        crash the safety-critical state machine.
        """
        try:
            self._state_conn.execute(
                'INSERT INTO state_snapshot (id, state, active_user_id, reason, updated_at) '
                'VALUES (1, ?, ?, ?, ?) '
                'ON CONFLICT(id) DO UPDATE SET '
                '  state=excluded.state, '
                '  active_user_id=excluded.active_user_id, '
                '  reason=excluded.reason, '
                '  updated_at=excluded.updated_at',
                (self.state, self.active_user_id, reason or '', int(time.time())),
            )
            self._state_conn.commit()
        except Exception as exc:  # pragma: no cover - defensive
            self.get_logger().warn(f'persist_state failed: {exc}')

    def _recover_state_locked(self):
        """Read the last persisted state. Returns (state, user_id, reason) or (None, ...).

        If the persisted state was mid-task we collapse to STANDBY and tag the
        reason so the operator gets a TTS warning.
        """
        try:
            row = self._state_conn.execute(
                'SELECT state, active_user_id, reason, updated_at FROM state_snapshot WHERE id = 1'
            ).fetchone()
        except Exception as exc:
            self.get_logger().warn(f'recover_state read failed: {exc}')
            return None, None, ''

        if row is None:
            return None, None, ''

        state, user_id, reason, _updated = row
        state = (state or '').upper()
        if state not in ALL_STATES:
            return None, None, ''
        if state in UNSAFE_RECOVERY_STATES:
            self.get_logger().warn(
                f'Recovering from unsafe state {state} → collapsing to STANDBY'
            )
            return 'STANDBY', user_id, f'unsafe_state_collapse_from_{state}'
        if state == 'OFFLINE':
            return None, None, ''
        return state, user_id, reason or 'recover'

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
            self._tts_pub.publish(String(data=text))

    # -------------------------------------------------------------------- #
    # ROS callbacks                                                        #
    # -------------------------------------------------------------------- #

    def _on_transition(self, msg: 'StateTransition'):
        with self._lock:
            target = msg.target_state
            reason = msg.reason if hasattr(msg, 'reason') else ''

            if target == 'LOGGED_OUT' and self.state in NO_LOGOUT_FROM:
                self.get_logger().warn(
                    f'Logout rejected — cannot logout from {self.state}')
                return

            self._transition(target, reason)

    def _on_safety_alert(self, msg: 'SafetyAlert'):
        severity = (msg.severity or '').upper()
        if severity == 'ESTOP':
            with self._lock:
                self._transition('ESTOP', f'safety:{msg.source}:{msg.reason}')
        elif severity == 'CLEAR' and self.state == 'ESTOP':
            # Voice/admin requested ESTOP clear. Drop back to STANDBY if a user
            # was active, otherwise to LOGGED_OUT.
            with self._lock:
                target = 'STANDBY' if self.active_user_id else 'LOGGED_OUT'
                self._transition(target, f'estop_cleared:{msg.source}:{msg.reason}')

    def _on_auth_result(self, msg: 'AuthResult'):
        with self._lock:
            if msg.success and msg.user_id:
                self.active_user_id = msg.user_id
                if self.state == 'LOGGED_OUT':
                    self._transition('STANDBY', f'auth:{msg.user_id}')
                    self._start_hard_ttl()
                else:
                    self._publish_current_state()

    # -------------------------------------------------------------------- #
    # Core transition                                                      #
    # -------------------------------------------------------------------- #

    def _publish_current_state(self):
        msg = RobotState()
        msg.state = self.state
        msg.active_user_id = self.active_user_id
        self.state_pub.publish(msg)

    def _transition(self, target: str, reason: str = ''):
        """
        Performs a state transition if valid.
        Publishes /robot_state, persists the snapshot, then resets timers.
        Self-transitions (e.g. STANDBY→STANDBY) are accepted as a re-publish.
        """
        if target not in ALL_STATES:
            self.get_logger().error(f'Unknown target state {target!r}')
            return

        allowed = VALID_TRANSITIONS.get(self.state, set())
        if target not in allowed and target != self.state:
            self.get_logger().error(
                f'Invalid transition {self.state} → {target} (reason: {reason})')
            return

        prev = self.state
        self.state = target

        if target == 'LOGGED_OUT':
            self.active_user_id = ''
            self._cancel_hard_ttl()

        self._publish_current_state()
        self.persist_state(reason)

        self.get_logger().info(f'State: {prev} → {target}' +
                               (f' [{reason}]' if reason else ''))

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
            self.get_logger().info('Session inactivity timeout — auto-logout')
            self._say('Session timeout. Logging out.')
            self._cancel_hard_ttl()
            self._transition('LOGGED_OUT', 'inactivity_timeout')

    def _auto_logout_hard_ttl(self):
        with self._lock:
            self.get_logger().info('Session hard TTL expired — auto-logout')
            self._say('Session time limit reached. Logging out.')
            self._transition('LOGGED_OUT', 'hard_ttl_expired')

    def destroy_node(self):
        if self._inactivity_timer:
            self._inactivity_timer.cancel()
        self._cancel_hard_ttl()
        try:
            self._state_conn.close()
        except Exception:
            pass
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

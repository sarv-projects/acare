from enum import Enum, auto
from typing import Optional, Callable, Dict, List
from dataclasses import dataclass
import threading
import time


class SystemState(Enum):
    IDLE        = "IDLE"
    LISTENING   = "LISTENING"
    PROCESSING  = "PROCESSING"
    RESPONDING  = "RESPONDING"
    CLARIFYING  = "CLARIFYING"
    CONFIRMED   = "CONFIRMED"
    ASSISTING   = "ASSISTING"
    ESTOP       = "ESTOP"
    ERROR       = "ERROR"


# Mapping from ROS2 robot states to voice FSM states
ROS2_TO_VOICE_STATE = {
    'OFFLINE':     SystemState.ERROR,
    'LOGGED_OUT':  SystemState.IDLE,
    'STANDBY':     SystemState.IDLE,
    'LISTENING':   SystemState.LISTENING,
    'PROCESSING':  SystemState.PROCESSING,
    'EXECUTING':   SystemState.ASSISTING,
    'HOLDING':     SystemState.ASSISTING,
    'HANDOVER':    SystemState.ASSISTING,
    'ESTOP':       SystemState.ESTOP,
    'ERROR':       SystemState.ERROR,
}

# Voice states that should trigger ROS2 state transitions
VOICE_TO_ROS2_TRANSITION = {
    SystemState.ESTOP: 'ESTOP',
    SystemState.ERROR: 'ERROR',
}


@dataclass
class StateContext:
    pending_intent: Optional[Dict] = None
    last_tool_requested: Optional[str] = None
    session_user_id: Optional[str] = None
    session_name: Optional[str] = None
    last_transcript: str = ""
    clarification_attempts: int = 0
    max_clarification_attempts: int = 2


class StateManager:

    VALID_TRANSITIONS = {
        SystemState.IDLE:       [SystemState.LISTENING],
        SystemState.LISTENING:  [SystemState.PROCESSING, SystemState.ASSISTING,
                                SystemState.ESTOP, SystemState.ERROR],
        SystemState.PROCESSING: [SystemState.RESPONDING, SystemState.CLARIFYING,
                                SystemState.ASSISTING, SystemState.CONFIRMED,
                                SystemState.LISTENING, SystemState.ESTOP, SystemState.ERROR],
        SystemState.RESPONDING: [SystemState.LISTENING, SystemState.PROCESSING,
                                SystemState.ESTOP, SystemState.ERROR],
        SystemState.CLARIFYING: [SystemState.CONFIRMED, SystemState.PROCESSING,
                                SystemState.LISTENING, SystemState.ESTOP, SystemState.ERROR],
        SystemState.CONFIRMED:  [SystemState.LISTENING, SystemState.PROCESSING,
                                SystemState.ESTOP, SystemState.ERROR],
        SystemState.ASSISTING:  [SystemState.LISTENING, SystemState.PROCESSING,
                                SystemState.ESTOP, SystemState.ERROR],
        SystemState.ESTOP:      [SystemState.LISTENING, SystemState.ERROR],
        SystemState.ERROR:      [SystemState.LISTENING, SystemState.IDLE],
    }

    def __init__(self):
        self._state = SystemState.IDLE
        self._lock = threading.RLock()
        self._context = StateContext()
        self._callbacks: Dict[SystemState, List[Callable]] = {s: [] for s in SystemState}
        self._transition_callbacks: List[Callable] = []
        self._state_entry_time = time.time()
        self._state_history: List[tuple] = []
        self._transition_publisher: Optional[Callable[[str, str], None]] = None

    @property
    def state(self) -> SystemState:
        with self._lock:
            return self._state

    @property
    def context(self) -> StateContext:
        with self._lock:
            return self._context

    def is_logged_in(self) -> bool:
        with self._lock:
            return self._context.session_user_id is not None

    def can_execute(self) -> bool:
        with self._lock:
            return (self._context.session_user_id is not None and
                    self._state != SystemState.ESTOP and
                    self._state not in (SystemState.IDLE, SystemState.ERROR))

    def transition(self, new_state: SystemState, reason: str = "") -> bool:
        with self._lock:
            old_state = self._state
            if new_state not in self.VALID_TRANSITIONS.get(old_state, []):
                # ESTOP and ERROR are always reachable from ANY state — safety overrides
                if new_state == SystemState.ESTOP:
                    print(f"[StateManager] ESTOP triggered: {old_state.value} -> {new_state.value} ({reason})")
                elif new_state == SystemState.ERROR:
                    print(f"[StateManager] ERROR triggered: {old_state.value} -> {new_state.value} ({reason})")
                else:
                    print(f"[StateManager] INVALID transition: {old_state.value} -> {new_state.value} ({reason})")
                    return False
            self._state = new_state
            self._state_entry_time = time.time()
            self._state_history.append((old_state, time.time(), reason))
            if len(self._state_history) > 50:
                self._state_history = self._state_history[-50:]
            print(f"[StateManager] {old_state.value} -> {new_state.value} ({reason})")
            for cb in self._callbacks.get(new_state, []):
                try:
                    cb(old_state, new_state, self._context)
                except Exception as e:
                    print(f"[StateManager] Callback error: {e}")
            for cb in self._transition_callbacks:
                try:
                    cb(old_state, new_state, self._context)
                except Exception as e:
                    print(f"[StateManager] Transition callback error: {e}")
            
            # Notify ROS2 FSM of critical state transitions
            if new_state in VOICE_TO_ROS2_TRANSITION:
                self._notify_ros2_transition(new_state, reason)
            
            return True

    def on_state(self, state: SystemState, callback: Callable):
        self._callbacks[state].append(callback)

    def on_transition(self, callback: Callable):
        self._transition_callbacks.append(callback)

    def time_in_state(self) -> float:
        with self._lock:
            return time.time() - self._state_entry_time

    def get_history(self) -> List[tuple]:
        with self._lock:
            return self._state_history.copy()

    def reset_context(self):
        with self._lock:
            self._context = StateContext()

    def set_session(self, user_id: str, name: str):
        with self._lock:
            self._context.session_user_id = user_id
            self._context.session_name = name

    def set_pending_intent(self, intent: Dict):
        with self._lock:
            self._context.pending_intent = intent
            self._context.clarification_attempts = 0

    def clear_pending_intent(self):
        with self._lock:
            self._context.pending_intent = None
            self._context.clarification_attempts = 0

    def increment_clarification(self) -> bool:
        with self._lock:
            self._context.clarification_attempts += 1
            return self._context.clarification_attempts >= self._context.max_clarification_attempts

    def sync_from_ros2_state(self, ros2_state: str):
        """
        Sync voice FSM from ROS2 /robot_state topic.
        Maps ROS2 robot states to voice FSM states.
        Called by voice node when receiving /robot_state updates.
        """
        voice_state = ROS2_TO_VOICE_STATE.get(ros2_state)
        if voice_state is None:
            print(f"[StateManager] Unknown ROS2 state: {ros2_state}")
            return
        
        # Only sync if it's a meaningful state change (not internal voice states)
        if voice_state in (SystemState.ESTOP, SystemState.ERROR, SystemState.IDLE):
            with self._lock:
                if self._state != voice_state:
                    print(f"[StateManager] ROS2 sync: {ros2_state} → {voice_state.value}")
                    self.transition(voice_state, f"ros2_sync:{ros2_state}")

    def set_transition_publisher(self, publisher_fn: Callable[[str, str], None]):
        """
        Set callback function to publish state transitions to /state_transition.
        Called when voice FSM enters critical states (ESTOP, ERROR).
        
        publisher_fn signature: fn(target_state: str, reason: str)
        """
        self._transition_publisher = publisher_fn

    def _notify_ros2_transition(self, voice_state: SystemState, reason: str):
        """
        Publish state transition to ROS2 FSM when voice FSM enters critical state.
        Called automatically by transition() for states in VOICE_TO_ROS2_TRANSITION.
        """
        ros2_target = VOICE_TO_ROS2_TRANSITION.get(voice_state)
        if ros2_target and self._transition_publisher is not None:
            try:
                self._transition_publisher(ros2_target, f"voice_fsm:{reason}")
                print(f"[StateManager] Published ROS2 transition: {ros2_target} (voice:{voice_state.value})")
            except Exception as e:
                print(f"[StateManager] Failed to publish ROS2 transition: {e}")


_state_manager_instance: Optional[StateManager] = None

def get_state_manager() -> StateManager:
    global _state_manager_instance
    if _state_manager_instance is None:
        _state_manager_instance = StateManager()
    return _state_manager_instance

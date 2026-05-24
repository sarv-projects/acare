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
                                SystemState.LISTENING, SystemState.ESTOP, SystemState.ERROR],
        SystemState.RESPONDING: [SystemState.LISTENING, SystemState.PROCESSING,
                                SystemState.ESTOP, SystemState.ERROR],
        SystemState.CLARIFYING: [SystemState.CONFIRMED, SystemState.LISTENING,
                                SystemState.ESTOP, SystemState.ERROR],
        SystemState.CONFIRMED:  [SystemState.LISTENING, SystemState.ESTOP, SystemState.ERROR],
        SystemState.ASSISTING:  [SystemState.LISTENING, SystemState.ESTOP, SystemState.ERROR],
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
                if new_state == SystemState.ESTOP:
                    pass
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


_state_manager_instance: Optional[StateManager] = None

def get_state_manager() -> StateManager:
    global _state_manager_instance
    if _state_manager_instance is None:
        _state_manager_instance = StateManager()
    return _state_manager_instance

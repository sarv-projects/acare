"""Formal AuthFlow state machine.

Spec ref: design.md §AuthFlowStateMachine, voice.md §IV (auth flow).
The auth_node logic was previously inlined as scattered booleans
(``self._pending_login``, ``self._awaiting_reconfirm``, etc.) so log_node
could not reconstruct the auth path and tests had to assert on private
attributes.

This FSM encapsulates the canonical sequence:

    DETECTION -> GREETING -> VERIFICATION -> SESSION_CREATED
                                       \\-> MANUAL_FALLBACK -> SESSION_CREATED
                                       \\-> FAILURE
                                       \\-> ENROLMENT (admin path)

Every transition is forwarded to a publish hook so the rest of the
graph and the audit log can see auth progress without inspecting
auth_node internals.
"""

from __future__ import annotations

import threading
from enum import Enum
from typing import Callable, Optional


class AuthFlowState(Enum):
    IDLE = "IDLE"
    DETECTION = "DETECTION"
    GREETING = "GREETING"
    VERIFICATION = "VERIFICATION"
    MANUAL_FALLBACK = "MANUAL_FALLBACK"
    ENROLMENT = "ENROLMENT"
    SESSION_CREATED = "SESSION_CREATED"
    FAILURE = "FAILURE"


_VALID = {
    AuthFlowState.IDLE:           {AuthFlowState.DETECTION, AuthFlowState.ENROLMENT},
    AuthFlowState.DETECTION:      {AuthFlowState.GREETING, AuthFlowState.IDLE,
                                   AuthFlowState.MANUAL_FALLBACK},
    AuthFlowState.GREETING:       {AuthFlowState.VERIFICATION, AuthFlowState.IDLE,
                                   AuthFlowState.MANUAL_FALLBACK},
    AuthFlowState.VERIFICATION:   {AuthFlowState.SESSION_CREATED,
                                   AuthFlowState.MANUAL_FALLBACK,
                                   AuthFlowState.FAILURE},
    AuthFlowState.MANUAL_FALLBACK:{AuthFlowState.SESSION_CREATED,
                                   AuthFlowState.FAILURE,
                                   AuthFlowState.IDLE},
    AuthFlowState.ENROLMENT:      {AuthFlowState.IDLE, AuthFlowState.FAILURE},
    AuthFlowState.SESSION_CREATED:{AuthFlowState.IDLE},
    AuthFlowState.FAILURE:        {AuthFlowState.IDLE, AuthFlowState.DETECTION},
}


class AuthFlowStateMachine:
    """Lightweight FSM with optional ROS publish hook."""

    def __init__(self, publish: Optional[Callable[[str], None]] = None,
                 logger=None):
        self._state = AuthFlowState.IDLE
        self._lock = threading.Lock()
        self._publish = publish
        self._logger = logger

    @property
    def state(self) -> AuthFlowState:
        with self._lock:
            return self._state

    def reset(self, reason: str = "logout"):
        self.transition(AuthFlowState.IDLE, reason)

    def transition(self, target: AuthFlowState, reason: str = "") -> bool:
        with self._lock:
            allowed = _VALID.get(self._state, set())
            if target not in allowed and target is not self._state:
                if self._logger:
                    self._logger.warn(
                        f"AuthFlow: rejected {self._state.value} -> "
                        f"{target.value} ({reason})"
                    )
                return False
            prev, self._state = self._state, target
        if self._logger:
            self._logger.info(
                f"AuthFlow: {prev.value} -> {target.value}"
                + (f" [{reason}]" if reason else "")
            )
        if self._publish is not None:
            try:
                self._publish(f"{prev.value}->{target.value}:{reason}")
            except Exception:
                if self._logger:
                    self._logger.warn("AuthFlow publish callback failed")
        return True

    # Convenience helpers used by auth_node.
    def to_detection(self, reason="face_present"):
        return self.transition(AuthFlowState.DETECTION, reason)

    def to_greeting(self, reason="welcome_prompt"):
        return self.transition(AuthFlowState.GREETING, reason)

    def to_verification(self, reason="confirm_command"):
        return self.transition(AuthFlowState.VERIFICATION, reason)

    def to_manual_fallback(self, reason: str):
        return self.transition(AuthFlowState.MANUAL_FALLBACK, reason)

    def to_enrolment(self, reason="admin_enrol"):
        return self.transition(AuthFlowState.ENROLMENT, reason)

    def to_session(self, reason: str):
        return self.transition(AuthFlowState.SESSION_CREATED, reason)

    def to_failure(self, reason: str):
        return self.transition(AuthFlowState.FAILURE, reason)

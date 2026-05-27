"""Formal substate machine for the HANDOVER phase.

Spec ref: design.md §HandoverSubstateMachine, voice.md §VII (multi-modal
verification). The global :class:`StateManager` only models the coarse
``HOLDING -> HANDOVER -> STANDBY`` arc. The fine-grained substates that
make handover safe (face verify, hand detect, voice confirm, release,
abort) used to live as inline comments in
``planner_node._phase_handover`` so log_node could not see them, the
admin CLI could not query them, and tests could not enforce them. This
module turns those comments into a real FSM and publishes every
transition to ``/handover_substate`` as a ``std_msgs/String`` of the form
``<from>-><to>:<reason>``.

Consumers (log_node, admin_cli, replay tools) can therefore reconstruct a
full handover timeline without parsing free-text logs.
"""

from __future__ import annotations

import threading
from enum import Enum
from typing import Callable, Optional


class HandoverSubstate(Enum):
    IDLE = "IDLE"
    APPROACHING = "APPROACHING"
    FACE_VERIFY = "FACE_VERIFY"
    HAND_DETECT = "HAND_DETECT"
    VOICE_CONFIRM = "VOICE_CONFIRM"
    RELEASING = "RELEASING"
    COMPLETE = "COMPLETE"
    ABORTED = "ABORTED"


# Edges allowed by the spec. ABORTED is reachable from any non-terminal
# substate; COMPLETE only from RELEASING.
_VALID = {
    HandoverSubstate.IDLE: {HandoverSubstate.APPROACHING},
    HandoverSubstate.APPROACHING: {HandoverSubstate.FACE_VERIFY, HandoverSubstate.ABORTED},
    HandoverSubstate.FACE_VERIFY: {HandoverSubstate.HAND_DETECT, HandoverSubstate.ABORTED},
    HandoverSubstate.HAND_DETECT: {HandoverSubstate.VOICE_CONFIRM, HandoverSubstate.ABORTED},
    HandoverSubstate.VOICE_CONFIRM: {HandoverSubstate.RELEASING, HandoverSubstate.ABORTED},
    HandoverSubstate.RELEASING: {HandoverSubstate.COMPLETE, HandoverSubstate.ABORTED},
    HandoverSubstate.COMPLETE: {HandoverSubstate.IDLE},
    HandoverSubstate.ABORTED: {HandoverSubstate.IDLE},
}


# Always allow ABORTED so safety has the last word.
for _state in list(_VALID.keys()):
    _VALID[_state].add(HandoverSubstate.ABORTED)


class HandoverSubstateMachine:
    """Plain-Python FSM with a publish hook.

    Pass a publish callback (e.g. ``lambda s: pub.publish(String(data=s))``)
    to forward every transition to ``/handover_substate``. The callback is
    optional so the class is trivially testable offline.
    """

    def __init__(self, publish: Optional[Callable[[str], None]] = None,
                 logger=None):
        self._state = HandoverSubstate.IDLE
        self._lock = threading.Lock()
        self._publish = publish
        self._logger = logger

    @property
    def state(self) -> HandoverSubstate:
        with self._lock:
            return self._state

    def reset(self):
        with self._lock:
            prev = self._state
            self._state = HandoverSubstate.IDLE
        self._emit(prev, HandoverSubstate.IDLE, "reset")

    def transition(self, target: HandoverSubstate, reason: str = "") -> bool:
        with self._lock:
            allowed = _VALID.get(self._state, set())
            if target not in allowed and target is not self._state:
                if self._logger:
                    self._logger.warn(
                        f"HandoverSubstateMachine: rejected "
                        f"{self._state.value} -> {target.value} ({reason})"
                    )
                return False
            prev = self._state
            self._state = target
        self._emit(prev, target, reason)
        return True

    # Convenience helpers — keep the call sites in planner_node.py readable.
    def to_approaching(self, reason="enter_handover_zone"):
        return self.transition(HandoverSubstate.APPROACHING, reason)

    def to_face_verify(self, reason="start_face_verify"):
        return self.transition(HandoverSubstate.FACE_VERIFY, reason)

    def to_hand_detect(self, reason="face_ok"):
        return self.transition(HandoverSubstate.HAND_DETECT, reason)

    def to_voice_confirm(self, reason="hand_ok"):
        return self.transition(HandoverSubstate.VOICE_CONFIRM, reason)

    def to_releasing(self, reason="voice_ok"):
        return self.transition(HandoverSubstate.RELEASING, reason)

    def to_complete(self, reason="release_ok"):
        return self.transition(HandoverSubstate.COMPLETE, reason)

    def to_aborted(self, reason: str):
        return self.transition(HandoverSubstate.ABORTED, reason)

    # ------------------------------------------------------------------ #

    def _emit(self, prev: HandoverSubstate, target: HandoverSubstate, reason: str):
        if self._logger:
            self._logger.info(
                f"HandoverSubstate: {prev.value} -> {target.value}"
                + (f" [{reason}]" if reason else "")
            )
        if self._publish is not None:
            try:
                self._publish(f"{prev.value}->{target.value}:{reason}")
            except Exception:
                if self._logger:
                    self._logger.warn("HandoverSubstate publish callback failed")

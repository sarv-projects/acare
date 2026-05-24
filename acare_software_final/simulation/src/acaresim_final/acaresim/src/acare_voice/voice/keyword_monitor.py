import threading
import time
import numpy as np
import sounddevice as sd

# These are the exact keywords from the spec
ESTOP_KEYWORDS = ["stop", "halt", "emergency", "abort", "ruko", "bas"]

SAMPLE_RATE = 16000
# Larger chunks here — we don't need 32ms precision, 
# we need fast keyword scanning
CHUNK_DURATION = 0.1   # 100ms chunks
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)  # 1600 samples

class KeywordMonitor:
    def __init__(self, on_estop):
        """
        on_estop is called immediately when keyword detected.
        Receives the keyword that triggered it as argument.
        """
        self.on_estop = on_estop
        self.is_running = False
        self._thread = None
        self.estop_active = False  # ADD THIS
        # We use a simple energy-based approach first —
        # check if audio is loud enough to be speech,
        # then check transcript from a local recogniser
        # For now we use a lightweight local approach: vosk or 
        # just match against Deepgram partials
        # We'll use Deepgram partial transcripts — 
        # they come fast enough for this purpose
        self._last_partial = ""
        self._collision_timer = None

    def check_partial(self, partial_text):
        """
        Called from ASR with every partial (non-final) transcript.
        Partials come much faster than finals — good for keyword detection.
        This is what gives us <200ms latency.
        """
        if self.estop_active or not partial_text:
            return
        
        try:
            text = partial_text.lower().strip()
            words = [w.strip(".,!?") for w in text.split()]
            for keyword in ESTOP_KEYWORDS:
                if keyword in words:
                    self._handle_keyword_detected(keyword, text)
                    return
        except (AttributeError, TypeError):
            # Handle invalid input gracefully
            return

    def _handle_keyword_detected(self, keyword, full_text):
        """
        Keyword found in partial transcript.
        Start 100ms collision window — check if more speech follows.
        """
        # Cancel any existing collision timer
        if self._collision_timer:
            self._collision_timer.cancel()
        
        # Start 100ms window
        # If this fires without being cancelled — genuine ESTOP
        self._collision_timer = threading.Timer(
            0.1,  # 100ms
            self._confirm_estop,
            args=[keyword, full_text]
        )
        self._collision_timer.start()

    def _confirm_estop(self, keyword, text):
        """
        Called after 100ms if no cancellation came.
        Means no more speech followed — genuine emergency.
        """
        self.estop_active = True
        print(f"ESTOP confirmed: keyword='{keyword}'")
        self.on_estop(keyword)
    
    def reset_estop(self):
        """
        Reset ESTOP flag after emergency is handled.
        Call this after the robot has been secured and user confirms clear.
        """
        self.estop_active = False
        print("ESTOP cleared. System ready.")

    def cancel_if_continuation(self, new_partial):
        """
        Called when new speech detected after keyword.
        Cancels the collision timer — it was a false trigger.
        Example: "stop, actually bring the scalpel"
        """
        if self._collision_timer and self._collision_timer.is_alive():
            # More speech came in — cancel ESTOP
            self._collision_timer.cancel()
            self._collision_timer = None
            print("ESTOP cancelled — continuation detected")
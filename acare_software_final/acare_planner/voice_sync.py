# acare_planner/voice_sync.py
import queue
import re
import threading

CONFIRM_WORDS = [
    "yes", "yeah", "yep", "yup", "sure", "thanks",
    "correct", "right", "affirmative", "confirm",
    "go ahead", "do it", "proceed", "absolutely",
    "got it",
]
CONFIRM_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in CONFIRM_WORDS) + r")\b",
    re.I,
)

OK_RE = re.compile(r"\b(ok|okay)\b(?!\s*\w)", re.I)


class VoiceSyncBridge:
    def __init__(self):
        self._queue = queue.Queue(maxsize=1)
        self._waiting = False
        self._expected_type = None
        self._lock = threading.Lock()

    def start_wait(self, expected_type: str):
        with self._lock:
            while not self._queue.empty():
                self._queue.get_nowait()
            self._waiting = True
            self._expected_type = expected_type

    def wait_for_response(self, timeout: float) -> str:
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return ""
        finally:
            with self._lock:
                self._waiting = False

    def on_transcript(self, text: str):
        with self._lock:
            if not self._waiting:
                return

            text_lower = text.lower().strip()
            if self._expected_type == 'CONFIRM':
                if CONFIRM_RE.search(text_lower) or OK_RE.search(text_lower):
                    try:
                        self._queue.put_nowait(text)
                    except queue.Full:
                        pass
            elif self._expected_type == 'LOCATION':
                if len(text_lower) > 2:
                    try:
                        self._queue.put_nowait(text)
                    except queue.Full:
                        pass
            elif self._expected_type == 'ANY':
                if len(text_lower) > 0:
                    try:
                        self._queue.put_nowait(text)
                    except queue.Full:
                        pass

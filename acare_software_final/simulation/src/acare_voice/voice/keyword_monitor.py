import threading
import time

ESTOP_KEYWORDS = ["stop", "halt", "emergency", "abort", "ruko", "bas"]

CONTINUATION_WORDS = [
    "moving", "that", "there", "here", "now", "please",
    "the", "it", "doing", "working", "processing"
]

RECOVERY_KEYWORDS = ["resume", "continue", "proceed", "clear", "reset", "go"]


class KeywordMonitor:

    def __init__(self, on_estop, on_resume=None):
        self.on_estop = on_estop
        self.on_resume = on_resume
        self.estop_active = False
        self._lock = threading.Lock()
        self._collision_timer = None
        self._last_keyword = None
        self._last_detection_time = 0.0
        self._cooldown_period = 2.0

    def check_partial(self, partial_text):
        if not partial_text:
            return

        with self._lock:
            if self.estop_active:
                if self.on_resume:
                    self._check_recovery(partial_text)
                return

            if time.time() - self._last_detection_time < self._cooldown_period:
                return

        try:
            text = partial_text.lower().strip()
            words = [w.strip(".,!?;:'\"") for w in text.split()]

            for keyword in ESTOP_KEYWORDS:
                if keyword in words:
                    idx = words.index(keyword)

                    if idx + 1 < len(words):
                        next_word = words[idx + 1]
                        if next_word in CONTINUATION_WORDS:
                            return

                    self._handle_keyword_detected(keyword, text)
                    return

        except (AttributeError, TypeError, ValueError):
            return

    def _check_recovery(self, text):
        text = text.lower().strip()
        words = [w.strip(".,!?;:'\"") for w in text.split()]

        for keyword in RECOVERY_KEYWORDS:
            if keyword in words:
                if len(words) <= 3:
                    print(f"[KeywordMonitor] Recovery keyword detected: '{keyword}'")
                    if self.on_resume:
                        self.on_resume(keyword)
                return

    def _handle_keyword_detected(self, keyword, full_text):
        with self._lock:
            if self._collision_timer and self._collision_timer.is_alive():
                self._collision_timer.cancel()

            self._last_keyword = keyword

            self._collision_timer = threading.Timer(
                0.2,
                self._confirm_estop,
                args=[keyword, full_text]
            )
            self._collision_timer.start()

    def _confirm_estop(self, keyword, text):
        with self._lock:
            if self.estop_active:
                return

            self.estop_active = True
            self._last_detection_time = time.time()
            self._collision_timer = None

        print(f"[KeywordMonitor] ESTOP confirmed: keyword='{keyword}'")
        try:
            self.on_estop(keyword)
        except Exception as e:
            print(f"[KeywordMonitor] ESTOP callback error: {e}")

    def reset_estop(self):
        with self._lock:
            self.estop_active = False
            if self._collision_timer and self._collision_timer.is_alive():
                self._collision_timer.cancel()
                self._collision_timer = None
        print("[KeywordMonitor] ESTOP cleared. System ready.")

    def cancel_if_continuation(self, new_text):
        with self._lock:
            if self._collision_timer and self._collision_timer.is_alive():
                text = new_text.lower().strip()
                words = [w.strip(".,!?;:'\"") for w in text.split()]

                if words and words[0] in CONTINUATION_WORDS:
                    self._collision_timer.cancel()
                    self._collision_timer = None
                    print(f"[KeywordMonitor] ESTOP cancelled \u2014 continuation: '{new_text}'")
                    return True

                if len(words) > 3:
                    self._collision_timer.cancel()
                    self._collision_timer = None
                    print(f"[KeywordMonitor] ESTOP cancelled \u2014 long continuation")
                    return True

        return False

    def force_estop(self, keyword="manual"):
        with self._lock:
            self.estop_active = True
            self._last_detection_time = time.time()
        print(f"[KeywordMonitor] Manual ESTOP triggered: '{keyword}'")
        try:
            self.on_estop(keyword)
        except Exception as e:
            print(f"[KeywordMonitor] Manual ESTOP callback error: {e}")

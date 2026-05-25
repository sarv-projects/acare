import re
from typing import Tuple


class SemanticTurnDetector:

    def __init__(self):
        self.INCOMPLETE_PATTERNS = [
            re.compile(r'\b(and|but|or|so|because|if|when|while|although)\s*$', re.I),
            re.compile(r'\b(need|want|get|bring|fetch|give|pass|hand)\s*$', re.I),
            re.compile(r'\b(the|a|an|this|that|these|those|my|your)\s*$', re.I),
            re.compile(r'\b(can|could|would|will|should|may|might)\s*$', re.I),
            re.compile(r'\b(um|uh|er|ehm)\s*$', re.I),
            re.compile(r'[,;:\-]\s*$'),
        ]

        self.COMPLETE_PATTERNS = [
            re.compile(r'[.!?]\s*$'),
            re.compile(r'\b(please|thanks|thank you|now|immediately|quickly)\s*$', re.I),
            re.compile(r'\b(yes|no|yeah|nope|correct|wrong|right|sure)\s*$', re.I),
            re.compile(r'\b(stop|halt|abort|emergency|cancel|resume|continue)\s*$', re.I),
        ]

        self.COMPLETE_COMMANDS = [
            re.compile(r'^(bring|fetch|get|give|pass|hand)\s+(me\s+)?(the\s+)?\w+', re.I),
            re.compile(r'^(need|want|require)\s+(the\s+)?\w+', re.I),
            re.compile(r'^\w+\s+(please|now|thanks|thank you)\s*$', re.I),
        ]

        self.FILLER_WORDS = ['um', 'uh', 'er', 'ehm', 'like', 'you know', 'sort of']
        self.MIN_COMMAND_WORDS = 2

    def predict(self, transcript: str, speech_duration: float = 0.0) -> Tuple[bool, float]:
        if not transcript or not transcript.strip():
            return (False, 0.0)

        text = transcript.strip()
        words = text.split()

        if len(words) < self.MIN_COMMAND_WORDS:
            if len(words) == 1 and words[0].lower() in [
                'stop', 'halt', 'abort', 'yes', 'no', 'cancel', 'resume', 'continue'
            ]:
                return (True, 0.95)
            return (False, 0.3)

        for pattern in self.COMPLETE_COMMANDS:
            if pattern.match(text):
                return (True, 0.9)

        for pattern in self.INCOMPLETE_PATTERNS:
            if pattern.search(text):
                return (False, 0.7)

        for pattern in self.COMPLETE_PATTERNS:
            if pattern.search(text):
                return (True, 0.8)

        filler_count = sum(1 for f in self.FILLER_WORDS if f in text.lower())
        if filler_count > 0:
            if filler_count / len(words) > 0.3:
                return (False, 0.6)

        if speech_duration > 3.0:
            return (True, 0.6)

        tools = ['cream', 'scissors', 'forceps',
                'thermometer', 'oximeter', 'plaster']
        has_tool = any(t in text.lower() for t in tools)
        has_action = any(a in text.lower() for a in ['bring', 'fetch', 'get', 'need', 'want'])
        if has_tool and has_action:
            return (True, 0.75)

        if len(words) < 4:
            return (False, 0.5)

        return (True, 0.5)

    def should_extend_silence_timeout(self, transcript: str,
                                     base_timeout: float,
                                     speech_duration: float) -> float:
        is_complete, confidence = self.predict(transcript, speech_duration)

        if not is_complete and confidence > 0.5:
            extension = min(1.0, confidence)
            return base_timeout + extension

        if is_complete and confidence > 0.7:
            reduction = min(0.3, confidence * 0.3)
            return max(0.3, base_timeout - reduction)

        return base_timeout


_detector_instance = None

def get_turn_detector() -> SemanticTurnDetector:
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = SemanticTurnDetector()
    return _detector_instance

import re
from typing import Optional, Dict, Tuple

from acare_bringup.constants import VALID_TOOLS, ESTOP_KEYWORDS, CONFIRM_WORDS, REJECT_WORDS

_TOOLS_PATTERN = "|".join(t.upper() for t in VALID_TOOLS)

FETCH_PATTERNS = [
    re.compile(rf"(?:bring|fetch|get|give|pass)\s+(?:me\s+)?(?:the\s+)?({_TOOLS_PATTERN})", re.I),
    re.compile(rf"(?:need|want|require)\s+(?:the\s+)?({_TOOLS_PATTERN})", re.I),
    re.compile(rf"(?:hand|pass)\s+(?:me\s+)?(?:the\s+)?({_TOOLS_PATTERN})", re.I),
]

CONFIRM_PATTERNS = [
    re.compile(r"\b(yes|yeah|yep|yup|correct|right|sure|absolutely|affirmative|confirm|go ahead|do it|proceed)\b", re.I),
    re.compile(r"\b(ok|okay)\b(?!\s*\w)", re.I),
    re.compile(r"\b(yes|yeah)\s+(please|go ahead|that's right|that is right)\b", re.I),
]

REJECT_PATTERNS = [
    re.compile(r"\b(no|nope|nah|negative|wrong|incorrect|not that|something else|cancel|never mind|nevermind|forget it)\b", re.I),
    re.compile(r"\b(no|nope)\s+(thank you|thanks|that's wrong|that is wrong)\b", re.I),
]

ESTOP_PATTERNS = [
    re.compile(r"\b(" + "|".join(ESTOP_KEYWORDS) + r")\b", re.I),
    re.compile(r"\b(stop|halt)\s+(everything|all|now|immediately|right now)\b", re.I),
]

RESUME_PATTERNS = [
    re.compile(r"\b(resume|continue|proceed|go|clear|all clear|safe|reset)\b", re.I),
    re.compile(r"\b(system|robot)\s+(resume|continue|reset)\b", re.I),
]

CANCEL_PATTERNS = [
    re.compile(r"\b(cancel|never mind|nevermind|forget it|ignore that|scratch that)\b", re.I),
]

MULTI_TOOL_INDICATORS = [
    re.compile(r"\b(and|plus|also|then|after that|next)\b", re.I),
]

FOLLOW_UP_PATTERNS = [
    re.compile(rf"^(and\s+(?:the\s+)?({_TOOLS_PATTERN}))$", re.I),
    re.compile(r"^(?:the\s+)?(other|that|same|next)\s+(one|tool|thing|item)$", re.I),
    re.compile(r"^(?:get|bring|fetch)\s+(?:that|it|the other one)$", re.I),
]


def parse_fast_intent(transcript: str, last_tool: Optional[str] = None) -> Optional[Dict]:
    if not transcript or not transcript.strip():
        return None

    text = transcript.strip().lower()

    for pattern in ESTOP_PATTERNS:
        if pattern.search(text):
            return {
                "tool": None,
                "action": "estop",
                "confidence": 0.99,
                "source": "fast",
                "type": "estop"
            }

    for pattern in RESUME_PATTERNS:
        if pattern.search(text):
            return {
                "tool": None,
                "action": "resume",
                "confidence": 0.95,
                "source": "fast",
                "type": "resume"
            }

    for pattern in CANCEL_PATTERNS:
        if pattern.search(text):
            return {
                "tool": None,
                "action": "cancel",
                "confidence": 0.95,
                "source": "fast",
                "type": "cancel"
            }

    for pattern in CONFIRM_PATTERNS:
        if pattern.search(text):
            return {
                "tool": None,
                "action": "confirm",
                "confidence": 0.95,
                "source": "fast",
                "type": "confirm"
            }

    for pattern in REJECT_PATTERNS:
        if pattern.search(text):
            return {
                "tool": None,
                "action": "reject",
                "confidence": 0.95,
                "source": "fast",
                "type": "reject"
            }

    for pattern in FOLLOW_UP_PATTERNS:
        match = pattern.search(text)
        if match:
            tool = match.group(1).lower() if match.lastindex and match.group(1) else last_tool
            if tool and tool in VALID_TOOLS:
                return {
                    "tool": tool,
                    "action": "fetch",
                    "confidence": 0.85,
                    "source": "fast",
                    "type": "follow_up"
                }

    multi_count = sum(1 for p in MULTI_TOOL_INDICATORS if p.search(text))
    tool_count = sum(1 for tool in VALID_TOOLS if re.search(rf"\b{tool}\b", text))

    if tool_count >= 2:
        return {
            "tool": None,
            "action": "fetch",
            "confidence": 0.7,
            "source": "fast",
            "type": "multi_tool",
            "detected_tools": [t for t in VALID_TOOLS if re.search(rf"\b{t}\b", text)]
        }

    for pattern in FETCH_PATTERNS:
        match = pattern.search(text)
        if match:
            tool = match.group(1).lower()
            if tool in VALID_TOOLS:
                return {
                    "tool": tool,
                    "action": "fetch",
                    "confidence": 0.92,
                    "source": "fast",
                    "type": "command"
                }

    for tool in VALID_TOOLS:
        if re.search(rf"\b{tool}\b", text):
            return {
                "tool": tool,
                "action": "fetch",
                "confidence": 0.65,
                "source": "fast",
                "type": "command"
            }

    return None


def is_simple_command(transcript: str) -> bool:
    text = transcript.strip().lower()
    if any(p.search(text) for p in ESTOP_PATTERNS):
        return True
    if any(p.search(text) for p in CONFIRM_PATTERNS + REJECT_PATTERNS):
        return True
    if any(p.search(text) for p in FETCH_PATTERNS):
        return True
    if any(re.search(rf"\b{t}\b", text) for t in VALID_TOOLS):
        return True
    return False

import re
from typing import Optional, Dict, Tuple

VALID_TOOLS = ["cream", "scissors", "forceps", "thermometer", "oximeter", "plaster"]

FETCH_PATTERNS = [
    re.compile(r"(?:bring|fetch|get|give|pass)\s+(?:me\s+)?(?:the\s+)?(CREAM|SCISSORS|FORCEPS|THERMOMETER|OXIMETER|PLASTER)", re.I),
    re.compile(r"(?:need|want|require)\s+(?:the\s+)?(CREAM|SCISSORS|FORCEPS|THERMOMETER|OXIMETER|PLASTER)", re.I),
    re.compile(r"(?:hand|pass)\s+(?:me\s+)?(?:the\s+)?(CREAM|SCISSORS|FORCEPS|THERMOMETER|OXIMETER|PLASTER)", re.I),
]

CONFIRM_PATTERNS = [
    re.compile(r"^(yes|yeah|yep|yup|correct|right|sure|absolutely|affirmative|confirm|go ahead|do it|proceed|ok|okay)$", re.I),
    re.compile(r"^(yes|yeah)\s+(please|go ahead|that's right|that is right)$", re.I),
]

REJECT_PATTERNS = [
    re.compile(r"^(no|nope|nah|negative|wrong|incorrect|not that|something else|cancel|never mind|nevermind|forget it)$", re.I),
    re.compile(r"^(no|nope)\s+(thank you|thanks|that's wrong|that is wrong)$", re.I),
]

ESTOP_PATTERNS = [
    re.compile(r"^(stop|halt|abort|emergency|freeze|hold|cease|kill)$", re.I),
    re.compile(r"^(stop|halt)\s+(everything|all|now|immediately|right now)$", re.I),
]

RESUME_PATTERNS = [
    re.compile(r"^(resume|continue|proceed|go|clear|all clear|safe|reset)$", re.I),
    re.compile(r"^(system|robot)\s+(resume|continue|reset)$", re.I),
]

CANCEL_PATTERNS = [
    re.compile(r"^(cancel|never mind|nevermind|forget it|ignore that|scratch that)$", re.I),
]

MULTI_TOOL_INDICATORS = [
    re.compile(r"\b(and|plus|also|then|after that|next)\b", re.I),
]

FOLLOW_UP_PATTERNS = [
    re.compile(r"^(and\s+(?:the\s+)?(CREAM|SCISSORS|FORCEPS|THERMOMETER|OXIMETER|PLASTER))$", re.I),
    re.compile(r"^(?:the\s+)?(other|that|same|next)\s+(one|tool|thing|item)$", re.I),
    re.compile(r"^(?:get|bring|fetch)\s+(?:that|it|the other one)$", re.I),
]


def parse_fast_intent(transcript: str, last_tool: Optional[str] = None) -> Optional[Dict]:
    if not transcript or not transcript.strip():
        return None

    text = transcript.strip().lower()

    for pattern in ESTOP_PATTERNS:
        if pattern.match(text):
            return {
                "tool": None,
                "action": "estop",
                "confidence": 0.99,
                "source": "fast",
                "type": "estop"
            }

    for pattern in RESUME_PATTERNS:
        if pattern.match(text):
            return {
                "tool": None,
                "action": "resume",
                "confidence": 0.95,
                "source": "fast",
                "type": "resume"
            }

    for pattern in CANCEL_PATTERNS:
        if pattern.match(text):
            return {
                "tool": None,
                "action": "cancel",
                "confidence": 0.95,
                "source": "fast",
                "type": "cancel"
            }

    for pattern in CONFIRM_PATTERNS:
        if pattern.match(text):
            return {
                "tool": None,
                "action": "confirm",
                "confidence": 0.95,
                "source": "fast",
                "type": "confirm"
            }

    for pattern in REJECT_PATTERNS:
        if pattern.match(text):
            return {
                "tool": None,
                "action": "reject",
                "confidence": 0.95,
                "source": "fast",
                "type": "reject"
            }

    for pattern in FOLLOW_UP_PATTERNS:
        match = pattern.match(text)
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
        match = pattern.match(text)
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
    if any(p.match(text) for p in ESTOP_PATTERNS):
        return True
    if any(p.match(text) for p in CONFIRM_PATTERNS + REJECT_PATTERNS):
        return True
    if any(p.match(text) for p in FETCH_PATTERNS):
        return True
    if any(re.search(rf"\b{t}\b", text) for t in VALID_TOOLS):
        return True
    return False

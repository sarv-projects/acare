import re
from typing import Tuple, List

VALID_TOOLS = [
    "scalpel", "scissors", "forceps", "bandage",
    "gauze", "thermometer", "oximeter", "plaster",
]

FILLER_WORDS = [
    r"\bum\b", r"\buh\b", r"\ber\b", r"\behm\b",
    r"\bplease\b", r"\bkindly\b", r"\bjust\b",
    r"\bquickly\b",
]

POLITE_MARKERS = [
    r"\bcan you\b", r"\bcould you\b", r"\bwould you\b",
    r"\bwill you\b", r"\bcan we\b", r"\bcould we\b",
]

SIMPLE_ALIASES = {
    "blade":          "scalpel",
    "surgical blade": "scalpel",
    "bandage cloth":  "bandage",
    "gauze pad":      "gauze",
    "gauze swab":     "gauze",
    "pulse ox":       "oximeter",
    "spo2":           "oximeter",
    "band aid":       "plaster",
    "bandaid":        "plaster",
    "adhesive strip": "plaster",
}


def normalise(transcript: str) -> Tuple[str, bool, List[str]]:
    if not transcript or not transcript.strip():
        return ("", False, [])

    text = transcript.strip()

    text = text.lower()

    for pattern in FILLER_WORDS:
        text = re.sub(pattern, "", text)

    for pattern in POLITE_MARKERS:
        text = re.sub(pattern, "", text)

    text = re.sub(r"\s+", " ", text).strip()

    text = re.sub(r"[^\w\s\-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    for alias, canonical in SIMPLE_ALIASES.items():
        text = re.sub(r"\b" + re.escape(alias) + r"\b", canonical, text)

    found_tools = []
    for tool in VALID_TOOLS:
        if re.search(r"\b" + re.escape(tool) + r"\b", text):
            found_tools.append(tool)

    # Multi-tool detection — only flag if tools are connected by conjunctions
    # or appear in parallel imperative structure.
    # "bring scissors — not the forceps, the scissors" → single tool (scissors)
    # "bring scissors and forceps" → multi-tool
    # "not the forceps" / "instead of the forceps" → negation, not a request
    multi_tool = False
    if len(found_tools) >= 2:
        multi_tool = _is_genuine_multi_tool(text, found_tools)

    return (text, multi_tool, found_tools)


def _is_genuine_multi_tool(text: str, found_tools: List[str]) -> bool:
    """
    Returns True only when the user is genuinely requesting multiple tools
    in a single utterance. Returns False for negation patterns like:
      "bring the scissors not the forceps"
      "the scissors instead of the forceps"
      "scissors — not forceps, scissors"

    Genuine multi-tool patterns require a conjunction or sequential marker
    connecting the tool names:
      "bring scissors and forceps"
      "I need the gauze plus the bandage"
      "scissors then forceps"
    """
    # Conjunctions / sequential markers that indicate genuine multi-tool request
    MULTI_CONJUNCTIONS = re.compile(
        r"\b(and|plus|also|then|after that|as well as|along with|both)\b", re.I
    )
    # Negation patterns that indicate the user is EXCLUDING a tool
    NEGATION_PATTERNS = re.compile(
        r"\b(not|dont|don't|no|instead of|rather than|without|except|but not)\b", re.I
    )

    # Check if a conjunction exists between any two tool positions
    tool_positions = []
    for tool in found_tools:
        match = re.search(r"\b" + re.escape(tool) + r"\b", text)
        if match:
            tool_positions.append((match.start(), match.end(), tool))

    tool_positions.sort(key=lambda x: x[0])

    if len(tool_positions) < 2:
        return False

    # Check text between each pair of consecutive tool mentions
    for i in range(len(tool_positions) - 1):
        between = text[tool_positions[i][1]:tool_positions[i + 1][0]]

        # If there's a negation word between tools, it's NOT multi-tool
        if NEGATION_PATTERNS.search(between):
            return False

        # If there's a conjunction between tools, it IS multi-tool
        if MULTI_CONJUNCTIONS.search(between):
            return True

    # No conjunction found between tools — check if negation appears before
    # any tool mention (e.g., "not the forceps, the scissors")
    for start, end, tool in tool_positions:
        # Look at the 20 chars before this tool mention for negation
        prefix_start = max(0, start - 20)
        prefix = text[prefix_start:start]
        if NEGATION_PATTERNS.search(prefix):
            return False

    # Two tools mentioned without conjunction or negation — ambiguous.
    # Default to NOT flagging as multi-tool. Let Groq intent parser handle it.
    # This avoids the false positive on "bring scissors — the scissors"
    return False


def get_multi_tool_prompt(tools: List[str]) -> str:
    if len(tools) == 2:
        return f"One at a time. Which first \u2014 {tools[0]} or {tools[1]}?"
    else:
        listed = ", ".join(tools[:-1]) + f" or {tools[-1]}"
        return f"One at a time. Which first \u2014 {listed}?"


if __name__ == "__main__":
    cases = [
        "Bring the SCALPEL please",
        "um, can you could you bring me the scissors",
        "um please bring me the bandage cloth",
        "scissors and scalpel please, could you",
        "fetch the blade quickly",
        "I need the pulse ox",
        "bring me the forceps and the gauze now",
        # Negation cases — should NOT flag as multi-tool
        "bring the scissors not the forceps",
        "the scissors instead of the forceps",
        "scissors not forceps the scissors",
        "I want the scalpel not the scissors",
        # Genuine multi-tool — should flag
        "bring scissors and forceps",
        "I need gauze plus bandage",
        "scissors then the scalpel",
        "",
        "   ",
    ]
    for t in cases:
        cleaned, multi, tools = normalise(t)
        print(f"IN:    {repr(t)}")
        print(f"OUT:   {repr(cleaned)}  | multi={multi} | tools={tools}")
        if multi:
            print(f"  -> TTS: {get_multi_tool_prompt(tools)}")
        print()

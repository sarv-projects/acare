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

    multi_tool = len(found_tools) >= 2

    return (text, multi_tool, found_tools)


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

"""
ACARE Text Normaliser
Spec Reference: Section IX, A11

Pipeline:
  1. Lowercase
  2. Strip filler words (um, uh, please, can you, could you, etc.)
  3. Strip punctuation
  4. Simple unambiguous alias expansion (see alias_expansion.py)
  5. Multi-tool detection  → flag MULTI_TOOL before Groq

This runs BEFORE alias_expansion.py and BEFORE Groq intent parsing.
Contextual aliases like "the sharp one" pass through intact — Groq resolves them.
"""

import re
from typing import Tuple, List, Optional

# ---------------------------------------------------------------------------
# Spec-defined valid tools (mirrored from intent_parser.py)
# ---------------------------------------------------------------------------
VALID_TOOLS = [
    "scalpel", "scissors", "forceps", "bandage",
    "gauze", "thermometer", "oximeter", "plaster",
]

# ---------------------------------------------------------------------------
# Filler words to strip — spoken language noise from operating theatre
# ---------------------------------------------------------------------------
FILLER_WORDS = [
    r"\bum\b", r"\buh\b", r"\ber\b", r"\behm\b",
    r"\bplease\b", r"\bcan you\b", r"\bcould you\b",
    r"\bwould you\b", r"\bwill you\b",
    r"\bjust\b", r"\bkindly\b", r"\bquickly\b",
    r"\blike\b",
]

# ---------------------------------------------------------------------------
# Simple unambiguous aliases that don't need LLM resolution
# Anything ambiguous ("the sharp one") passes through to Groq
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Main normalisation function
# ---------------------------------------------------------------------------

def normalise(transcript: str) -> Tuple[str, bool, List[str]]:
    """
    Full normalisation pipeline.

    Args:
        transcript: Raw STT output from Deepgram

    Returns:
        Tuple of:
          - cleaned_text   : Normalised text ready for Groq
          - multi_tool     : True if 2+ tool names detected (flag for clarification)
          - detected_tools : List of tool names found (populated when multi_tool=True)

    Example:
        >>> normalise("um can you please bring me the scalpel and scissors")
        ("bring me the scalpel and scissors", True, ["scalpel", "scissors"])

        >>> normalise("Bring the SCALPEL please")
        ("bring the scalpel", False, [])
    """
    if not transcript or not transcript.strip():
        return ("", False, [])

    text = transcript.strip()

    # Step 1: Lowercase
    text = text.lower()

    # Step 2: Strip filler words
    for pattern in FILLER_WORDS:
        text = re.sub(pattern, "", text)

    # Step 3: Strip leading/trailing/double whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Step 4: Strip punctuation (keep hyphens for compound words)
    text = re.sub(r"[^\w\s\-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Step 5: Simple unambiguous alias expansion
    for alias, canonical in SIMPLE_ALIASES.items():
        # Only replace if it's a whole-phrase match
        text = re.sub(r"\b" + re.escape(alias) + r"\b", canonical, text)

    # Step 6: Multi-tool detection
    found_tools = []
    for tool in VALID_TOOLS:
        if re.search(r"\b" + re.escape(tool) + r"\b", text):
            found_tools.append(tool)

    multi_tool = len(found_tools) >= 2

    return (text, multi_tool, found_tools)


def get_multi_tool_prompt(tools: List[str]) -> str:
    """
    Build clarification TTS prompt for multi-tool detection.
    Spec: "One at a time. Which first — {A} or {B}?"
    """
    if len(tools) == 2:
        return f"One at a time. Which first — {tools[0]} or {tools[1]}?"
    else:
        listed = ", ".join(tools[:-1]) + f" or {tools[-1]}"
        return f"One at a time. Which first — {listed}?"


# ---------------------------------------------------------------------------
# Quick smoke test
# ---------------------------------------------------------------------------
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

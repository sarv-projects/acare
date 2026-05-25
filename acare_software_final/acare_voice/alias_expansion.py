"""
ACARE Alias Expansion - Simple Alias to Canonical Tool Mapping

Maps user-spoken aliases to canonical tool names.
Example: "sharp one" → "scalpel", "long tool" → "forceps"

Spec Reference: XIII. INTENT RECOGNITION & LLM LAYER (Lines 1350, 1408-1439)
Context-aware alias resolution for surgical tools in operating room.
"""

from typing import Optional, Dict, List, Tuple
import re


# ============================================================================
# ALIAS MAPPING DICTIONARY
# ============================================================================

# Maps spoken aliases to canonical tool names
# Key: alias phrase (lowercase for case-insensitive matching)
# Value: canonical tool name (must be in VALID_TOOLS)
ALIAS_MAP = {
    # Cream aliases
    "cream": "cream",
    "lotion": "cream",
    "ointment": "cream",
    "topical": "cream",
    "the cream": "cream",
    "tube": "cream",

    # Scissors aliases
    "scissors": "scissors",
    "cuts": "scissors",
    "cutting tool": "scissors",
    "snips": "scissors",
    "medical scissors": "scissors",

    # Forceps aliases
    "forceps": "forceps",
    "forcep": "forceps",
    "long tool": "forceps",
    "grabber": "forceps",
    "grasper": "forceps",
    "surgical forceps": "forceps",
    "tweezers": "forceps",
    "clamps": "forceps",

    # Thermometer aliases
    "thermometer": "thermometer",
    "temp": "thermometer",
    "temperature": "thermometer",
    "temp probe": "thermometer",

    # Oximeter aliases
    "oximeter": "oximeter",
    "oxygen meter": "oximeter",
    "pulse ox": "oximeter",
    "oxymeter": "oximeter",
    "spo2": "oximeter",

    # Plaster aliases
    "plaster": "plaster",
    "cast": "plaster",
    "band aid": "plaster",
    "bandaid": "plaster",
    "adhesive strip": "plaster",
}

# List of valid canonical tool names (from intent_parser.py)
VALID_TOOLS = ["cream", "scissors", "forceps", "thermometer", "oximeter", "plaster"]

# Ambiguous aliases that could map to multiple tools
# These need user confirmation
AMBIGUOUS_ALIASES = {
    "cutting tool": ["scissors", "forceps"],
    "long tool": ["forceps"],
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def detect_aliases_in_transcript(transcript: str) -> List[Tuple[str, str]]:
    """
    Find all aliases mentioned in the transcript.
    
    Returns:
        List of (alias_phrase, canonical_tool) tuples found in transcript
        Example: [("sharp one", "scalpel"), ("cutting tool", "scissors")]
    
    NOTE: Returns first match for each alias phrase detected.
    Does NOT filter ambiguous aliases - caller must check.
    """
    found_aliases = []
    transcript_lower = transcript.lower()
    
    # Check each alias in the map
    for alias_phrase, canonical_tool in ALIAS_MAP.items():
        # Simple substring matching (case-insensitive)
        if alias_phrase in transcript_lower:
            found_aliases.append((alias_phrase, canonical_tool))
    
    return found_aliases


def is_ambiguous_alias(alias_phrase: str) -> bool:
    """
    Check if an alias phrase is ambiguous (maps to multiple tools).
    
    Args:
        alias_phrase: The alias string (lowercase)
    
    Returns:
        True if ambiguous, False otherwise
    
    Example:
        >>> is_ambiguous_alias("cutting tool")
        True  # Could be scalpel or scissors
        >>> is_ambiguous_alias("sharp one")
        False  # Always scalpel
    """
    return alias_phrase in AMBIGUOUS_ALIASES


def get_ambiguous_options(alias_phrase: str) -> List[str]:
    """
    Get the list of possible canonical tools for an ambiguous alias.
    
    Args:
        alias_phrase: The alias string (lowercase)
    
    Returns:
        List of possible canonical tools, empty if not ambiguous
    
    Example:
        >>> get_ambiguous_options("cutting tool")
        ["scalpel", "scissors"]
    """
    return AMBIGUOUS_ALIASES.get(alias_phrase, [])


def expand_aliases(transcript: str) -> Tuple[str, Optional[str], bool]:
    """
    Main function: Expand aliases in transcript to canonical tool names.
    
    Process:
    1. Detect all aliases in transcript
    2. If exactly 1 alias found:
       - If not ambiguous: return (modified_transcript, canonical_tool, False)
       - If ambiguous: return (transcript, None, True) - needs clarification
    3. If multiple aliases: return (transcript, None, True) - needs clarification
    4. If no aliases: return (transcript, None, False)
    
    Args:
        transcript: Raw user input (e.g., "bring me the sharp one")
    
    Returns:
        Tuple of:
        - modified_transcript: Input with alias replaced by canonical tool (or original)
        - canonical_tool: The expanded tool name, or None if unclear
        - needs_clarification: True if ambiguous and needs user confirmation
    
    Examples:
        >>> expand_aliases("bring me the sharp one")
        ("bring me the scalpel", "scalpel", False)
        
        >>> expand_aliases("bring me the cutting tool")
        ("bring me the cutting tool", None, True)  # Ambiguous
        
        >>> expand_aliases("bring me the scalpel")
        ("bring me the scalpel", None, False)  # No alias
    """
    found_aliases = detect_aliases_in_transcript(transcript)
    
    # No aliases detected
    if not found_aliases:
        return (transcript, None, False)
    
    # Multiple aliases detected → ambiguous
    if len(found_aliases) > 1:
        print(f"[ALIAS_EXPANSION] Multiple aliases detected: {found_aliases}")
        return (transcript, None, True)
    
    # Exactly one alias detected
    alias_phrase, canonical_tool = found_aliases[0]
    
    # Check if this single alias is ambiguous
    if is_ambiguous_alias(alias_phrase):
        print(f"[ALIAS_EXPANSION] Ambiguous alias detected: '{alias_phrase}' -> {get_ambiguous_options(alias_phrase)}")
        return (transcript, None, True)
    
    # Single, unambiguous alias → expand it
    print(f"[ALIAS_EXPANSION] Alias expanded: '{alias_phrase}' -> '{canonical_tool}'")
    modified_transcript = transcript.replace(alias_phrase, canonical_tool)
    return (modified_transcript, canonical_tool, False)


def validate_tool(tool_name: str) -> bool:
    """
    Check if a tool name is in the valid tools list.
    
    Args:
        tool_name: Tool name to validate
    
    Returns:
        True if tool is valid, False otherwise
    """
    return tool_name.lower() in VALID_TOOLS


# ============================================================================
# DEMO / TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ACARE Alias Expansion - Test Examples")
    print("=" * 70)
    
    test_cases = [
        "bring me the sharp one",                          # Clear alias
        "bring me the cutting tool",                       # Ambiguous
        "fetch the scalpel please",                        # No alias
        "I need the long tool",                            # Ambiguous
        "get me the blade",                                # Clear alias
        "can you bring me the grasper",                    # Clear alias
        "scissors and scalpel",                            # Multiple items
    ]
    
    for transcript in test_cases:
        modified, tool, needs_clarify = expand_aliases(transcript)
        print(f"\nInput:  '{transcript}'")
        print(f"Output: '{modified}'")
        print(f"Tool:   {tool}")
        print(f"Clarify Needed: {needs_clarify}")

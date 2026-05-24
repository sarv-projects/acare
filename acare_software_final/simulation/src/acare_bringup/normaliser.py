# acare_voice/normaliser.py
# Spec Reference: Section IX (Voice Command Pipeline — normaliser.py)
#
# Called after Deepgram STT, before Groq intent parsing.
# Cleans raw transcript text and detects multi-tool requests.
#
# Steps:
#   1. Lowercase
#   2. Strip punctuation (keep apostrophes)
#   3. Strip filler words (longest first to avoid partial matches)
#   4. Simple unambiguous alias expansion only
#      (contextual aliases like 'the sharp one' pass through to Groq)
#   5. Multi-tool detection — flag if 2+ tool names found
#
# Tool names match the trained model's canonical names:
#   cream, scissors, oximeter, plaster, forceps, thermometer
# (mapped from model classes: cream, medical scissors, oxymeter,
#  plaster, surgical forceps, thermometer)

import re

FILLER_WORDS = {
    'um', 'uh', 'er', 'ah', 'hmm', 'please', 'kindly',
    'can you', 'could you', 'would you',
    'can you please', 'could you please', 'would you please',
}

# Simple unambiguous aliases only — contextual ones go to Groq
SIMPLE_ALIASES = {
    'pulse ox':       'oximeter',
    'spo2':           'oximeter',
    'sp02':           'oximeter',
    'oxymeter':       'oximeter',
    'temp probe':     'thermometer',
    'temperature':    'thermometer',
    'band aid':       'plaster',
    'band-aid':       'plaster',
    'bandaid':        'plaster',
    'adhesive strip': 'plaster',
    'medical scissors': 'scissors',
    'surgical scissors': 'scissors',
    'surgical forceps': 'forceps',
    'tweezers':       'forceps',
    'clamps':         'forceps',
    'lotion':         'cream',
    'ointment':       'cream',
}

# Canonical tool names (matching model output via CANONICAL map in yolo_infer.py)
TOOL_NAMES = {
    'cream', 'scissors', 'oximeter', 'plaster', 'forceps', 'thermometer',
}


def normalise(raw: str) -> dict:
    """
    Cleans and normalises a raw STT transcript.

    Input:  raw string from Deepgram
    Output: dict with keys:
        'text'        — cleaned text string
        'multi_tool'  — True if 2+ tool names detected
        'tools_found' — list of tool names found (empty if < 2)

    Examples:
        'Um, can you bring the forceps please' → 'bring the forceps'
        'bring scissors and oximeter'          → multi_tool=True, tools=['scissors','oximeter']
        'bring the oxymeter'                   → 'bring the oximeter' (alias expanded)
    """
    text = raw.lower().strip()

    # Step 1: Strip punctuation, keep apostrophes and spaces
    text = re.sub(r"[^\w\s']", ' ', text)

    # Step 2: Strip filler words — longest first to avoid partial matches
    for filler in sorted(FILLER_WORDS, key=len, reverse=True):
        text = re.sub(r'\b' + re.escape(filler) + r'\b', ' ', text)
    text = ' '.join(text.split())   # collapse multiple spaces

    # Step 3: Simple alias expansion — longest aliases first
    for alias, canonical in sorted(SIMPLE_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(alias, canonical)

    # Step 4: Multi-tool detection
    found_tools = [t for t in TOOL_NAMES if re.search(r'\b' + re.escape(t) + r'\b', text)]
    multi_tool = len(found_tools) >= 2

    return {
        'text':        text,
        'multi_tool':  multi_tool,
        'tools_found': found_tools if multi_tool else [],
    }


def get_multi_tool_prompt(tools: list) -> str:
    """Returns the TTS prompt for a multi-tool request."""
    if len(tools) == 2:
        return f'One at a time. Which first — {tools[0]} or {tools[1]}?'
    return f'One at a time. Which tool do you need first?'


if __name__ == '__main__':
    # Quick smoke test
    tests = [
        ('Um, can you please bring the forceps', 'bring the forceps'),
        ('bring me the oxymeter', 'bring me the oximeter'),
        ('scissors and oximeter please', None),   # multi-tool
        ('bring the surgical forceps', 'bring the forceps'),
        ('I need the temp probe', 'i need the thermometer'),
    ]
    print('normaliser.py smoke test:')
    all_pass = True
    for raw, expected in tests:
        result = normalise(raw)
        if expected is None:
            ok = result['multi_tool']
        else:
            ok = result['text'] == expected
        status = 'PASS' if ok else 'FAIL'
        if not ok:
            all_pass = False
        print(f'  [{status}] "{raw}" → "{result["text"]}" multi={result["multi_tool"]}')
    print('All tests passed.' if all_pass else 'SOME TESTS FAILED.')

"""
acare_bringup/constants.py
Single source of truth for system-wide constants.

Every package imports tool names, ESTOP keywords, and recovery keywords
from here so that a single edit propagates everywhere.
"""

VALID_TOOLS = [
    "cream",
    "scissors",
    "forceps",
    "thermometer",
    "oximeter",
    "plaster",
]

ESTOP_KEYWORDS = [
    "stop", "halt", "emergency", "abort", "ruko", "bas",
    "freeze", "hold", "cease", "kill",
]

RECOVERY_KEYWORDS = [
    "resume", "continue", "proceed", "clear", "reset", "go",
]

CONFIRM_WORDS = [
    "yes", "yeah", "yep", "yup", "correct", "right",
    "sure", "affirmative", "confirm", "ok", "okay",
    "go ahead", "do it", "proceed", "absolutely",
]

REJECT_WORDS = [
    "no", "nope", "nah", "negative", "wrong", "incorrect",
    "not that", "something else", "cancel", "never mind",
    "nevermind", "forget it",
]

TTS_VOICE = "en-IN-NeerjaNeural"

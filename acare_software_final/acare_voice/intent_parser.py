from dotenv import load_dotenv
from groq import Groq
import json
import os
from .fast_intent import parse_fast_intent, is_simple_command
from acare_bringup.constants import VALID_TOOLS

load_dotenv()


def _get_client() -> Groq:
    """Lazy Groq client. Raises only when actually used, not at import time."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    return Groq(api_key=api_key)


SYSTEM_PROMPT = f"""You are only a voice command parser for a surgical robot called ACARE.
Your only job is to extract structured intent from voice commands spoken by surgeons.

Rules:
- Only respond with a JSON object, nothing else
- No markdown, no explanation, just raw JSON
- tool must be one of: {VALID_TOOLS}
- action is always "fetch" for bring/fetch/get commands
- confidence is your certainty from 0.0 to 1.0
- If command is unclear or tool not recognised, set confidence below 0.6
- If user says "yes", "yeah", "correct" \u2014 return: {{"action": "confirm", "confidence": 0.95}}
- If user says "no", "nope", "wrong" \u2014 return: {{"action": "reject", "confidence": 0.95}}
- If user says "cancel", "never mind" \u2014 return: {{"action": "cancel", "confidence": 0.95}}

Output format:
{{"tool": "tool_name", "action": "fetch", "confidence": 0.95}}"""


def parse_intent(transcript, last_tool=None):
    if is_simple_command(transcript):
        fast_result = parse_fast_intent(transcript, last_tool)
        if fast_result and fast_result.get("confidence", 0) >= 0.85:
            return fast_result

    try:
        response = _get_client().chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": transcript}
            ],
            temperature=0.0,
            max_tokens=100,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content.strip()
        try:
            intent = json.loads(raw)
        except json.JSONDecodeError:
            if raw.count('{') > 1:
                return {"multi_tool": True, "raw": raw}
            print(f"Groq returned invalid JSON: {raw}")
            return None

        if intent.get("tool") not in VALID_TOOLS and intent.get("action") not in ("confirm", "reject", "cancel"):
            print(f"Unknown tool returned: {intent.get('tool')}")
            return None

        if intent.get("action") not in ("fetch", "confirm", "reject", "cancel", "estop", "resume"):
            return None

        return intent

    except Exception as e:
        print(f"Groq API error: {e}")
        return None

from dotenv import load_dotenv
from groq import Groq
import json
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

VALID_TOOLS = ["scalpel", "scissors", "forceps", "bandage", "gauze", "thermometer", "oximeter", "plaster"]

SYSTEM_PROMPT = f"""You are only a voice command parser for a surgical robot called ACARE.
Your only job is to extract structured intent from voice commands spoken by surgeons.

Rules:
- Only respond with a JSON object, nothing else
- No markdown, no explanation, just raw JSON
- tool must be one of: {VALID_TOOLS}
- action is always "fetch" for bring/fetch/get commands
- confidence is your certainty from 0.0 to 1.0
- If command is unclear or tool not recognised (e.g., if asked "knife" for "scalpel"), don't grant it. Set confidence below 0.6

Output format:
{{"tool": "tool_name", "action": "fetch", "confidence": 0.95}}"""

def parse_intent(transcript):
    """
    Takes transcript string like "bring me the scalpel".
    Sends to Groq, gets back structured JSON.
    Returns dict with tool, action, confidence.
    Returns None if API fails or JSON is invalid.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": transcript}
            ],
            temperature=0.0,  # deterministic — same input always gives same output
            max_tokens=100,   # intent JSON is tiny
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content.strip()
        if raw.count('{')>1:
            return {
                "multi_tool":True,
                "raw":raw
            }
        intent = json.loads(raw)

        # Validate tool exists in our dataset
        if intent.get("tool") not in VALID_TOOLS:
            print(f"Unknown tool returned: {intent.get('tool')}")
            return None
        if intent.get("action") != "fetch":
            return None
        

        return intent

    except json.JSONDecodeError:
        print(f"Groq returned invalid JSON: {raw}")
        return None

    except Exception as e:
        print(f"Groq API error: {e}")
        return None
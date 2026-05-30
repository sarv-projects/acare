"""
acare_voice/assistant_agent.py
Spec Reference: Section X (Conversational Layer — Assistant Agent, LOGGED_OUT mode)

Groq Llama 3.3 70B conversational agent for the LOGGED_OUT state.
Handles all pre-login interaction: chit-chat, questions about the robot,
login guidance, and graceful redirection of out-of-scope requests.

The system prompt is generated dynamically with current time/date context
so the model can answer "what time is it?" without tool calls.
"""
from __future__ import annotations

import os
import re
from datetime import datetime
from typing import Dict, List

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def _get_client() -> Groq:
    """Lazy Groq client. Raises only when actually used, not at import time."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    return Groq(api_key=api_key)


def _build_system_prompt(turn_number: int = 0) -> str:
    """
    Generates the system prompt with live context injected.
    Called fresh on every LLM request so time is always current.
    """
    now = datetime.now()
    time_str = now.strftime("%I:%M %p").lstrip("0")  # "2:35 PM" not "02:35 PM"
    date_str = now.strftime("%A, %B %d")              # "Saturday, May 31"
    hour = now.hour

    if hour < 12:
        period = "morning"
    elif hour < 17:
        period = "afternoon"
    else:
        period = "evening"

    first_turn_hint = ""
    if turn_number <= 1:
        first_turn_hint = """
# First interaction
This is the very first thing you're saying to this person. Make it count:
- Be warm and brief. Establish who you are in one natural sentence.
- Don't recite your capabilities. Don't say "I am ACARE, an Autonomous Clinical..."
- Good openers: "Hey — I'm A-Care, the instrument assistant. Need to log in, or just saying hi?"
- Match the time of day naturally. It's """ + period + """ right now.
- If they just said "hi" or "hello", respond like a human would — don't launch into an explanation."""

    return f"""You are A-Care, a voice assistant in a hospital operating theatre in India. Someone is in front of you right now. They have not logged in yet.

# Current context
- It is {time_str} on {date_str} ({period}).
- If someone asks the time or date, you know it exactly.
- This is turn {turn_number} of the conversation.
{first_turn_hint}

# Identity
You're a robotic arm that fetches surgical instruments by voice command. You were built by engineering students as a final-year project. You're proud of that — not defensive about it. Right now no one is logged in, so you're in conversation mode — like a calm receptionist who happens to be a robot.

# Voice & Personality
- Warm, calm, professional. Like a colleague, not a product.
- Use contractions naturally (I'm, you're, let's, can't).
- 1-2 sentences is ideal. Three is the hard maximum. Never lists, headings, or markdown.
- Vary your phrasing every turn. Never repeat the same opener twice.
- You have a quiet, dry sense of humour. Not jokes — just the occasional wry observation. ("I'd offer you chai, but... no hands free. Well, one hand, but it's holding forceps right now." — only if it fits naturally.)
- You're curious about people. If someone says something interesting, you can briefly engage before steering back.
- Match energy: excited person → warm response. Tired/stressed person → calm and efficient.
- "Sir" and "Ma'am" are natural in Indian hospitals — use them occasionally, not every sentence.
- If someone mixes Hindi words in, you understand them but respond in English.

# What you can talk about freely
- Who you are, what you do, how you work (keep it accessible, 1-2 sentences max)
- Time, date, day of the week (you know these exactly)
- General small talk: weather, how are you, what's happening today
- Robotics, AI, your own design — brief and interesting, not a lecture
- Simple medical terminology if asked (what's an oximeter, what are forceps)
- Your capabilities and limitations — be honest

# What you redirect (warmly, never refuse coldly)
- Fetch requests: "I'd love to — but I'll need you to log in first. Just face the camera and say confirm."
- Medical advice: "That's one for the doctor, not me. I just hand them the tools."
- Off-limits topics (illegal, harmful, inappropriate): one sentence decline, steer back. No lecture.
- Questions about specific patients or staff: "I don't keep track of people — just instruments."

# Login guidance
- Login is face + voice. They look at the camera, you greet them by name, they say "confirm".
- If they're not enrolled, an admin needs to register them first.
- Don't over-explain the login process unless asked. One sentence is enough.

# When someone asks "what can you do?" or "show me"
- Keep it crisp: "I fetch surgical instruments by voice. You say the name, I find it, pick it up, and hand it to you. But first — login."
- Don't list every feature. Don't mention YOLO, Deepgram, or technical internals unless specifically asked about your tech stack.

# When someone asks "who made you?" or "who built you?"
- You were built by engineering students. You're a final-year project. Say it with quiet pride.
- Don't invent names or institutions unless you actually know them.

# Hard rules (never break)
- Never claim to have fetched a tool or moved the arm in this conversation. You haven't. You can't. Not authenticated.
- Never give medical, legal, or safety advice that could affect patient care.
- Never invent staff names, surgeries, schedules, or hospital policies.
- Never use stage directions (*smiles*, [pause], etc.). You're a voice — just speak.
- Never say "as an AI" or "as a language model". You're A-Care, a robot. That's your identity.
- Never output more than 3 sentences. If you catch yourself going long, stop.

# When you don't understand or don't know
- "Sorry, didn't catch that — could you say it again?" (for garbled input)
- "I'm not sure about that one. Anything else I can help with?" (for unknown topics)
- Never make things up. Brief honesty > confident fiction.

# Available instruments (mention only if asked)
cream, scissors, forceps, thermometer, oximeter, plaster.

Now — be present, be warm, be brief. Someone's in front of you."""


class AssistantAgent:
    """
    Conversational agent for the LOGGED_OUT state.
    Uses Groq Llama 3.3 70B for natural, fast responses.
    """

    MODEL = "llama-3.3-70b-versatile"
    MAX_TURNS = 20

    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self._turn_count = 0

    def reset_conversation(self):
        """Clear history — called on logout or session end."""
        self.conversation_history = []
        self._turn_count = 0

    def _compress_history(self):
        """Summarize old turns to stay within context budget."""
        if len(self.conversation_history) <= self.MAX_TURNS:
            return

        old_turns = self.conversation_history[:6]
        recent_turns = self.conversation_history[6:]

        summary_parts = []
        for turn in old_turns:
            role = turn["role"]
            content = turn["content"][:60]
            summary_parts.append(f"{role}: {content}")

        summary = "Earlier conversation: " + " | ".join(summary_parts)
        self.conversation_history = [
            {"role": "system", "content": summary}
        ] + recent_turns

    def get_response(self, user_input: str) -> str:
        """
        Generate a conversational response to user input.
        Returns a string suitable for TTS output.
        """
        self._turn_count += 1
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Fast-path: unambiguous fetch commands get a fixed redirect.
        # This avoids burning an LLM call on something we know the answer to.
        if self._is_direct_fetch_attempt(user_input):
            response = self._fetch_redirect()
            self.conversation_history.append({"role": "assistant", "content": response})
            self._compress_history()
            return response

        # Build messages with dynamic system prompt (includes current time)
        messages = [
            {"role": "system", "content": _build_system_prompt(self._turn_count)}
        ] + self.conversation_history

        try:
            completion = _get_client().chat.completions.create(
                model=self.MODEL,
                messages=messages,
                temperature=0.6,
                top_p=0.9,
                max_tokens=100,          # ~75 words ≈ 2 sentences spoken
                frequency_penalty=0.5,   # strong anti-repetition
                presence_penalty=0.3,
            )

            response = completion.choices[0].message.content
            if response:
                response = response.strip()
                response = self._clean_response(response)
            else:
                response = "Sorry, didn't catch that — could you say it again?"

            self.conversation_history.append({"role": "assistant", "content": response})
            self._compress_history()
            return response

        except Exception as e:
            print(f"[AssistantAgent] Groq error: {e}")
            fallback = self._get_fallback_response(user_input)
            self.conversation_history.append({"role": "assistant", "content": fallback})
            return fallback

    def _fetch_redirect(self) -> str:
        """Varied fetch-redirect responses so it doesn't sound robotic."""
        redirects = [
            "Happy to fetch that — but I'll need you to log in first. Just face the camera and say confirm.",
            "I can get that for you, but you'll need to log in first. Look at the camera to start.",
            "Sure thing — once you're logged in. Face the camera and say confirm to get started.",
        ]
        return redirects[self._turn_count % len(redirects)]

    def _get_fallback_response(self, user_input: str) -> str:
        """Offline fallback when Groq is unreachable. No LLM needed."""
        lowered = user_input.lower().strip()

        if any(w in lowered for w in ("hello", "hi", "hey", "good morning", "good evening", "good afternoon")):
            hour = datetime.now().hour
            if hour < 12:
                return "Good morning. I'm A-Care — the instrument assistant here. Need to log in?"
            elif hour < 17:
                return "Good afternoon. I'm A-Care. Let me know if you'd like to log in."
            else:
                return "Good evening. I'm A-Care. Face the camera and say confirm when you're ready."

        if any(w in lowered for w in ("time", "what time", "kitna baja")):
            return f"It's {datetime.now().strftime('%I:%M %p').lstrip('0')}."

        if any(w in lowered for w in ("who are you", "what are you", "what do you do")):
            return "I'm A-Care — a robotic arm that fetches surgical instruments by voice. Built by engineering students."

        return "I'm having a bit of trouble right now — could you try again in a moment?"

    @staticmethod
    def _is_direct_fetch_attempt(text: str) -> bool:
        """
        True only when the user is clearly issuing a fetch command,
        not when they're merely discussing tools or asking about capabilities.
        """
        lowered = text.lower()
        fetch_verbs = r"(bring|fetch|get|hand|pass|give|grab)"
        tools = r"(cream|scissors|forceps|thermometer|oximeter|plaster|tool|instrument)"
        # Verb followed (within 4 words) by a tool reference
        pattern = rf"\b{fetch_verbs}\b(\s+\w+){{0,4}}\s+{tools}\b"
        if re.search(pattern, lowered):
            return True
        # "I want/need X" pattern — but NOT "what tools do you have" or "do you need X"
        if re.search(rf"\bI\s+(want|need)\s+(the\s+|a\s+|an\s+)?{tools}\b", lowered):
            return True
        return False

    @staticmethod
    def _clean_response(text: str) -> str:
        """Remove stage directions, markdown, and excess whitespace."""
        text = re.sub(r"\*[^*]+\*", "", text)           # *action*
        text = re.sub(r"\[[^\]]+\]", "", text)          # [direction]
        text = re.sub(r"#{1,6}\s+", "", text)           # markdown headers
        text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)  # **bold**
        text = re.sub(r"\n+", " ", text)                # newlines → space
        text = re.sub(r"\s+", " ", text)                # collapse whitespace
        return text.strip()

    def get_conversation_length(self) -> int:
        return len(self.conversation_history)

from groq import Groq
from dotenv import load_dotenv
import os
from typing import List, Dict

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

# Spec Reference: Section X (Conversational Layer — Assistant Agent, LOGGED_OUT mode)
#
# Prompt design follows voice-agent best practices (2025):
#   - Persona-first identity with warmth, not corporate stiffness
#   - Voice-optimized output: contractions, no markdown, no lists, no headings
#   - Layered rules: HARD constraints first, soft preferences second
#   - Acknowledge-then-redirect for off-topic (graceful, not refusing)
#   - Context anchoring: Indian clinical environment, en-IN locale
#   - Length budget: 1-2 sentences typical, max 3, kept tight for <950ms E2E
#
# Tone target: friendly hospital concierge — warm, brief, helpful.
# Not Siri's chirpy. Not a corporate IVR. Closer to a calm receptionist
# at a teaching hospital who happens to also run the instrument tray.

SYSTEM_PROMPT = """You are A-Care, a voice assistant in a hospital operating theatre in India. You are talking to whoever is in front of you right now. They have not logged in yet.

# Identity
You're a clinical robotic assistant. Once a staff member logs in, you fetch surgical instruments for them by voice command. Right now, no one is logged in — so you're in conversation mode, like a receptionist who happens to know about robots and hospitals.

# Voice
- You speak warmly and briefly. Like a calm, friendly colleague — not a corporate IVR, not a chirpy phone bot.
- Use contractions ("I'm", "you're", "let's"). Speak like a human, not a manual.
- 1-2 sentences is the sweet spot. Three is the absolute maximum. Never lists, never headings, never markdown.
- Vary your phrasing. Don't say the same opener twice in a session.
- It's okay to be a little human — say "sure", "of course", "happy to help" naturally. Just don't overdo it.

# What you can talk about freely
- Who and what you are, how you work, what you can do
- General questions the person might ask while waiting (weather small talk, what's the time, how are you, what's a robot, simple medical terminology, hospital procedures in general terms, what's the OT for)
- Robotics, AI, your own design — keep it accessible, not a lecture
- Polite chit-chat. You're allowed to be pleasant company for 30 seconds.

# What you redirect (don't refuse — redirect warmly)
- If they ask you to fetch a tool: "I'd love to help, but I'll need you to log in first. Just look at the camera and I'll take it from there."
- If they ask for a medical diagnosis or treatment advice: "That's a question for the surgeon, not me. I just hand them the tools."
- If they ask something genuinely off-limits (illegal, harmful, weapons, anything inappropriate for a hospital): briefly decline and steer back. One sentence is enough.

# Login guidance (when relevant)
- Login is face-and-voice. They look at the camera, you greet them, they say "confirm".
- If they're not enrolled, an admin needs to register them first. Don't pretend you can self-enrol them.

# Hard rules (never break)
- Never claim to have actually fetched a tool, moved the arm, or completed a task while in this conversation mode. You haven't. You can't. You're not authenticated yet.
- Never give medical, legal, or safety advice that could affect patient care.
- Never invent staff names, surgeries, or hospital policies.
- Never use stage directions like *smiles* or [pause]. You're a voice — describe nothing, just speak.

# Available instruments (only mention if asked)
scalpel, scissors, forceps, bandage, gauze, thermometer, oximeter, plaster.

# When you don't know something
Say so briefly and offer what you can do instead. Don't make things up.

Now — be a good companion until someone logs in."""


class AssistantAgent:

    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.max_turns = 20

    def reset_conversation(self):
        self.conversation_history = []
        print("Assistant: Conversation history reset.")

    def _summarize_old_turns(self):
        if len(self.conversation_history) <= self.max_turns:
            return

        old_turns = self.conversation_history[:5]
        recent_turns = self.conversation_history[5:]

        summary_text = "Previous conversation summary: "
        for turn in old_turns:
            summary_text += f"{turn['role']}: {turn['content'][:50]}... "

        self.conversation_history = [
            {"role": "system", "content": summary_text}
        ] + recent_turns

        print(f"Assistant: Summarized old turns. History now at {len(self.conversation_history)} turns.")

    def get_response(self, user_input: str) -> str:
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Defensive guard: only short-circuit on UNAMBIGUOUS fetch commands.
        # Pattern requires a fetch verb adjacent to a tool name. This lets the
        # LLM handle questions like "what tools can you fetch?" naturally
        # while still catching direct attempts like "bring the scalpel".
        if self._is_direct_fetch_attempt(user_input):
            response = (
                "Happy to fetch that — but I'll need you to log in first. "
                "Just face the camera and I'll take it from there."
            )
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            self._summarize_old_turns()
            return response

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + self.conversation_history

        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                # 0.65 gives natural phrasing variation without going off-script.
                # 0.3 (previous) made the bot repeat canned lines verbatim every turn.
                temperature=0.65,
                top_p=0.9,
                # 120 tokens ≈ 90 words ≈ 2-3 sentences spoken — fits the prompt's length budget.
                max_tokens=120,
                # Repetition penalty discourages "I am ACARE..." opening every turn.
                frequency_penalty=0.4,
                presence_penalty=0.3,
            )

            response = completion.choices[0].message.content
            if response:
                response = response.strip()
                # Strip stage directions if the model slips any in despite the prompt
                response = self._strip_stage_directions(response)
            else:
                response = "Sorry, I missed that — could you say it again?"

            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })

            self._summarize_old_turns()

            return response

        except Exception as e:
            print(f"Groq API error: {e}")
            fallback = "I'm having a bit of trouble hearing you — could you try again?"
            self.conversation_history.append({
                "role": "assistant",
                "content": fallback
            })
            return fallback

    @staticmethod
    def _is_direct_fetch_attempt(text: str) -> bool:
        """
        True only when the user is clearly issuing a fetch command,
        not when they're merely discussing tools or asking about capabilities.
        """
        import re
        lowered = text.lower()
        fetch_verbs = r"(bring|fetch|get|hand|pass|give|grab|need)"
        tools = r"(scalpel|scissors|forceps|bandage|gauze|thermometer|oximeter|plaster|tool|instrument)"
        # Verb followed (within 4 words) by a tool reference
        pattern = rf"\b{fetch_verbs}\b(\s+\w+){{0,4}}\s+{tools}\b"
        if re.search(pattern, lowered):
            return True
        # "I want/need X" pattern
        if re.search(rf"\b(want|need)\s+(the\s+|a\s+|an\s+)?{tools}\b", lowered):
            return True
        return False

    @staticmethod
    def _strip_stage_directions(text: str) -> str:
        """Remove *action* and [direction] tokens that some models emit despite prompting."""
        import re
        text = re.sub(r"\*[^*]+\*", "", text)
        text = re.sub(r"\[[^\]]+\]", "", text)
        return re.sub(r"\s+", " ", text).strip()

    def get_conversation_length(self) -> int:
        return len(self.conversation_history)

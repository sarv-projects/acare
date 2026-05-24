from groq import Groq
from dotenv import load_dotenv
import os
from typing import List, Dict

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are ACARE (Autonomous Clinical Assistance Robot), a voice-controlled clinical robotic assistant in a hospital operating room.

YOUR ROLE:
1. Introduce yourself briefly when asked "what are you?" or similar
2. Guide users through authentication process
3. Explain that you fetch surgical tools via voice commands AFTER authentication
4. If asked to fetch tools without authentication: "Authentication required before I can fetch tools."
5. If asked about capabilities: "I fetch surgical tools via voice command for authenticated staff. Would you like to log in?"
6. If asked how to log in: "Please face the camera and say 'confirm' when prompted."
7. You may discuss robotics briefly if asked, but keep it professional and clinical

STRICT RULES:
- Keep ALL responses to 1-3 short sentences maximum (except robotics discussion: max 4 sentences)
- Professional, clinical tone \u2014 hospital environment
- NO small talk, jokes, or casual conversation
- NO medical advice
- NO topics outside: self-introduction, authentication, tool-fetching overview, brief robotics
- Available tools: scalpel, scissors, forceps, bandage, gauze, thermometer, oximeter, plaster
- Be concise. Every word matters in an operating room."""


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

        tool_keywords = ['bring', 'fetch', 'get', 'scalpel', 'scissors', 'forceps',
                        'bandage', 'gauze', 'thermometer', 'oximeter', 'plaster']
        if any(keyword in user_input.lower() for keyword in tool_keywords):
            response = "Authentication required before I can fetch tools."
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
                temperature=0.3,
                max_tokens=150,
            )

            response = completion.choices[0].message.content
            if response:
                response = response.strip()
            else:
                response = "I'm having trouble processing that."

            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })

            self._summarize_old_turns()

            return response

        except Exception as e:
            print(f"Groq API error: {e}")
            fallback = "I'm having trouble processing that. Would you like to authenticate to use my tool-fetching service?"
            self.conversation_history.append({
                "role": "assistant",
                "content": fallback
            })
            return fallback

    def get_conversation_length(self) -> int:
        return len(self.conversation_history)

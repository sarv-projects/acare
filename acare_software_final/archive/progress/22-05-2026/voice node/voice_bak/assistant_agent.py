"""
Assistant Agent - LOGGED_OUT State Conversational AI

Activates when state = LOGGED_OUT and voice input detected.
Bounded to two contexts only: ACARE self-introduction and guided auth flow.
Professional, clinical tone - 1-3 sentences maximum, no small talk.
"""

from groq import Groq
from dotenv import load_dotenv
import os
from typing import List, Dict

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

# System prompt - defines bounded behavior
SYSTEM_PROMPT = """You are ACARE (Autonomous Clinical Assistance Robot), a voice-controlled clinical robotic assistant.

Your role is ONLY to:
1. Introduce yourself when asked "what are you?" or similar.
2. Guide users through the authentication process
3. Explain that you fetch surgical tools via voice commands AFTER authentication
4.If asked to fetch tools without authentication, respond with "Authentication required before I can fetch tools."
5. If asked about your capabilities, respond with "I fetch surgical tools via voice command for authenticated staff. Would you like to log in?"
6. If asked how to log in, respond with "Please face the camera and say 'confirm' when prompted."
7.You can even talk about robotics if prompted, but keep it brief and professional.
STRICT RULES:
- Keep responses to 1-3 sentences maximum. Explain your capabilities more if asked. You can speak about robotics, but always limit to 1-3 sentences.
- Professional, clinical tone - this is a hospital environment
- NO small talk, jokes, or casual conversation
-If you talk about robotics,you can talk about 4-5 lines as needed.
- If asked to fetch tools: "Authentication required before I can fetch tools."
- If asked about your capabilities: "I fetch surgical tools via voice command for authenticated staff. Would you like to log in?"
- If asked how to log in: "Please face the camera and say 'confirm' when prompted."
- DO NOT provide medical advice
- DO NOT engage in topics outside: self-introduction, authentication, tool-fetching overview. You may explain about robotics if prompted only.

Available tools: scalpel, scissors, forceps, bandage, gauze, thermometer, oximeter, plaster.

Keep it brief, professional, and bounded."""


class AssistantAgent:
    """
    Groq-powered conversational agent for LOGGED_OUT state.
    Bounded to ACARE introduction and auth guidance only.
    """
    
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.max_turns = 20  # Spec: capped at 20 turns to prevent RAM exhaustion
        
    def reset_conversation(self):
        """Reset conversation history. Called on new session start."""
        self.conversation_history = []
        print("Assistant: Conversation history reset.")
    
    def _summarize_old_turns(self):
        """
        If history exceeds 20 turns, summarize older turns to save RAM.
        Keeps most recent 15 turns + summary of oldest 5.
        """
        if len(self.conversation_history) <= self.max_turns:
            return
        
        # Take oldest 5 turns to summarize
        old_turns = self.conversation_history[:5]
        recent_turns = self.conversation_history[5:]
        
        # Create summary
        summary_text = "Previous conversation summary: "
        for turn in old_turns:
            summary_text += f"{turn['role']}: {turn['content'][:50]}... "
        
        # Replace with summary + recent turns
        self.conversation_history = [
            {"role": "system", "content": summary_text}
        ] + recent_turns
        
        print(f"Assistant: Summarized old turns. History now at {len(self.conversation_history)} turns.")
    
    def get_response(self, user_input: str) -> str:
        """
        Get assistant response for user input.
        
        Args:
            user_input: User's spoken query
            
        Returns:
            Assistant's response (1-3 sentences, professional tone)
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Check for tool fetch requests - immediate bounded response
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
        
        # Prepare messages for Groq API
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + self.conversation_history
        
        try:
            # Call Groq API
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Updated to newest Groq model
                messages=messages,
                temperature=0.3,  # Spec: slightly creative but bounded
                max_tokens=150,   # Spec: force brevity
            )
            
            response = completion.choices[0].message.content
            if response:
                response = response.strip()
            else:
                response = "I'm having trouble processing that."
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Manage history size
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
        """Return current conversation history length."""
        return len(self.conversation_history)


# Example usage and testing
if __name__ == "__main__":
    agent = AssistantAgent()
    
    print("=== ACARE Assistant Agent Test ===")
    print("Type 'reset' to clear history, 'quit' to exit\n")
    
    # Test scenarios from spec
    test_queries = [
        "What are you?",
        "What can you do?",
        "Bring me a scalpel",
        "How do I log in?",
        "Tell me a joke",
    ]
    
    print("Running automated tests:\n")
    for query in test_queries:
        print(f"User: {query}")
        response = agent.get_response(query)
        print(f"ACARE: {response}")
        print(f"[History: {agent.get_conversation_length()} turns]\n")
    
    print("\n=== Interactive Mode ===")
    agent.reset_conversation()
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("ACARE: Goodbye.")
            break
        
        if user_input.lower() == 'reset':
            agent.reset_conversation()
            continue
        
        response = agent.get_response(user_input)
        print(f"ACARE: {response}")
        print(f"[History: {agent.get_conversation_length()} turns]")

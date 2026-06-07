# test_assistant.py
import sys
import os

# Add acare_voice dir to path to import AssistantAgent
sys.path.append(r"C:\Users\Sonali\Desktop\ACARE\acare_software_final")

# Reconfigure stdout to use UTF-8 to prevent Unicode encoding errors on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Read the .env file in acare_voice and set MISTRAL_API_KEY
env_path = r"C:\Users\Sonali\Desktop\ACARE\acare_software_final\acare_voice\.env"
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.startswith("MISTRAL_API_KEY="):
                os.environ["MISTRAL_API_KEY"] = line.split("=", 1)[1].strip()
                break

from acare_voice.assistant_agent import AssistantAgent

try:
    print("Initializing AssistantAgent...")
    agent = AssistantAgent()
    print("Testing chitchat...")
    response = agent.get_response("hello, what is your name?")
    print(f"User: hello, what is your name?")
    print(f"Agent: {response}")
    
    print("\nTesting time query...")
    response = agent.get_response("what time is it?")
    print(f"User: what time is it?")
    print(f"Agent: {response}")
    
    print("\nTesting fetch attempt redirect...")
    response = agent.get_response("fetch some scissors please")
    print(f"User: fetch some scissors please")
    print(f"Agent: {response}")
    
except Exception as e:
    print(f"Error testing AssistantAgent: {e}")

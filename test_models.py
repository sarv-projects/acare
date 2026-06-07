# test_models.py
import os
import sys

# Reconfigure stdout to use UTF-8 to prevent Unicode encoding errors on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


# Add acare_voice dir to path to import dotenv if needed
sys.path.append(r"C:\Users\Sonali\Desktop\ACARE\acare_software_final")

# Read the .env file in acare_voice
env_path = r"C:\Users\Sonali\Desktop\ACARE\acare_software_final\acare_voice\.env"
groq_key = None
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.startswith("GROQ_API_KEY="):
                groq_key = line.split("=", 1)[1].strip()
                break

if not groq_key:
    print("GROQ_API_KEY not found in .env")
    sys.exit(1)

os.environ["GROQ_API_KEY"] = groq_key
print("Loaded GROQ_API_KEY from .env")

# Try to list models via Groq API
try:
    from groq import Groq
    client = Groq(api_key=groq_key)
    print("Listing models from Groq:")
    models = client.models.list()
    for model in models.data:
        print(f"  - {model.id}")
except Exception as e:
    print(f"Error listing models: {e}")

# Now query openai/gpt-oss-120b with a complex, long-context prompt
try:
    print("\nSending complex, long-context request to openai/gpt-oss-120b...")
    
    # Let's generate a long context of a simulated surgical robot trajectory failure
    context = """
    Scenario Details:
    Surgical Assistance Robot (ACARE) is operating in a sterile cleanroom environment.
    Command: Fetch surgical forceps for J5 wrist yaw alignment.
    Robot State: EXECUTING
    Action: Move to tray position X=0.45, Y=0.00, Z=0.05.
    LiDAR telemetry: Detected obstacle at 450mm in front-arc (safety severity: WARNING, speed reduced to 75%).
    YOLOv11 Detection: Found forceps with 0.88 confidence. 
    Alternate candidates: none.
    
    Trajectory Phase: Pre-grasp approach to X=0.45, Y=0.00, Z=0.10.
    IK Solver Output: Reachable, Joint angles: [0.12, -0.45, 0.85, 0.0, 0.32, -0.15].
    Motion Feedback: Success.
    
    Grasp Descent Phase: Arm move to X=0.45, Y=0.00, Z=0.05.
    Motion Feedback: Success.
    Gripper Grasp Command: target force = 3.5N.
    Telemetry Feedback: actual gripper force = 0.12N (Expected >= 0.5N).
    Status: GRASP_FAILED.
    
    Problem Description:
    The target instrument has a highly polished metallic surface with round cylindrical handles.
    The parallel jaws of the gripper are slipping off the handles because the approach orientation (0 deg offset) 
    fails to align with the axis of the handle. Additionally, safety warning limits J3 current to 6.2A.
    
    Task for LLM:
    Based on the above context, determine:
    1. A detailed reasoning analysis of why the grasp failed.
    2. Suggest an alternate wrist roll/pitch angle (rotation_offset_deg) and grasp force delta.
    3. Output your proposal in the strict JSON schema matching the system FSM.
    """
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are the agentic decision layer of ACARE. Propose recovery actions."},
            {"role": "user", "content": context}
        ],
        temperature=0.1,
        max_tokens=512
    )
    print("\nResponse from openai/gpt-oss-120b:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error querying openai/gpt-oss-120b: {e}")

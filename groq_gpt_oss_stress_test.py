#!/usr/bin/env python3
"""
Groq GPT-OSS 120B Stress Test for ACARE Surgical Robot Planner
Tests rate limits and JSON output quality with realistic planner context.
"""
import os, sys, json, time
from pathlib import Path

# Load .env
ENV_PATH = Path(__file__).parent / "acare_software_final" / "acare_voice" / ".env"
if ENV_PATH.exists():
    for line in open(ENV_PATH):
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            os.environ[k] = v

KEY = os.environ.get("GROQ_API_KEY")
if not KEY:
    print("ERROR: No GROQ_API_KEY found in .env")
    sys.exit(1)

from openai import OpenAI
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=KEY, timeout=15.0)

# Realistic ACARE planner system prompt (from agentic_planner.py)
SYSTEM_PROMPT = """You are the ACARE surgical robot planner. You control a 6-DOF robotic arm in a sterile clinical environment.

Available tools:
- vision_scan(zone: str): Search for tools in Zone A/B/C using Bayesian NBV
- arm_move(target_xyz: list[float], wrist_rpy: list[float]): Move arm to 3D pose
- arm_approach(target_xyz: list[float], direction: str): Approach from TOP/LEFT/RIGHT
- gripper_close(force_level: str): Close gripper with SOFT/MEDIUM/FIRM force
- gripper_open(): Release tool
- detect_face(): Verify surgeon presence
- detect_hand(): Check for handover readiness
- speak(text: str): TTS announcement
- ask_user(prompt: str): Request surgeon input
- complete_task(): Mark tray assembly done
- abort_task(reason: str): Emergency abort

Recovery ladders (follow strictly):
- GRASP_FAIL/SLIP_DETECTED:
  Rung 1: gripper_close(FIRM)
  Rung 2: arm_approach(SIDE_LEFT) + retry
  Rung 3: vision_scan(new_zone) + retry
- UNREACHABLE:
  Rung 1: Try alternate approach direction
  Rung 2: Ask user for repositioning
- VISION_FAIL (3+ searches empty):
  Rung 1: Calibrate camera
  Rung 2: Ask user for tool location

Return JSON: {"tool": "tool_name", "params": {...}, "reason": "brief explanation"}
"""

# Realistic state snapshots (simulating a tray assembly sequence)
STATE_TEMPLATES = [
    # Initial search phase
    {"state": "SEARCHING", "task": "Assemble surgical tray with scalpel, forceps, scissors", "action_history": [], "tried_and_failed": [], "joint_angles": [0.0, -0.5, 1.2, 0.0, 0.3, 0.0], "gripper_state": "OPEN", "current_zone": "A"},
    
    # After first vision scan
    {"state": "SEARCHING", "task": "Assemble surgical tray with scalpel, forceps, scissors", "action_history": [{"tool": "vision_scan", "params": {"zone": "A"}, "result": "TOOL_NOT_FOUND"}], "tried_and_failed": ["vision_scan(A)"], "joint_angles": [0.1, -0.4, 1.1, 0.0, 0.4, 0.1], "gripper_state": "OPEN", "current_zone": "A"},
    
    # Moving to Zone B
    {"state": "SEARCHING", "task": "Assemble surgical tray with scalpel, forceps, scissors", "action_history": [{"tool": "vision_scan", "params": {"zone": "A"}, "result": "TOOL_NOT_FOUND"}, {"tool": "vision_scan", "params": {"zone": "B"}, "result": "TOOL_FOUND", "tool_class": "scalpel", "confidence": 0.87}], "tried_and_failed": ["vision_scan(A)"], "joint_angles": [-0.3, -0.6, 1.3, 0.0, 0.2, -0.1], "gripper_state": "OPEN", "current_zone": "B", "detected_tools": [{"class": "scalpel", "xyz": [0.45, 0.12, 0.08], "confidence": 0.87}]},
    
    # Approaching scalpel
    {"state": "APPROACHING", "task": "Assemble surgical tray with scalpel, forceps, scissors", "action_history": [{"tool": "vision_scan", "params": {"zone": "B"}, "result": "TOOL_FOUND", "tool_class": "scalpel"}, {"tool": "arm_approach", "params": {"target_xyz": [0.45, 0.12, 0.08], "direction": "TOP"}, "result": "APPROACH_COMPLETE"}], "tried_and_failed": ["vision_scan(A)"], "joint_angles": [-0.28, -0.55, 1.25, 0.0, 0.8, -0.1], "gripper_state": "OPEN", "current_zone": "B", "target_tool": "scalpel"},
    
    # First grasp attempt (slip detected)
    {"state": "GRASPING", "task": "Assemble surgical tray with scalpel, forceps, scissors", "action_history": [{"tool": "arm_approach", "params": {"target_xyz": [0.45, 0.12, 0.08], "direction": "TOP"}, "result": "APPROACH_COMPLETE"}, {"tool": "gripper_close", "params": {"force_level": "MEDIUM"}, "result": "SLIP_DETECTED"}], "tried_and_failed": ["vision_scan(A)", "gripper_close(MEDIUM)"], "joint_angles": [-0.28, -0.55, 1.25, 0.0, 0.9, -0.1], "gripper_state": "PARTIAL_CLOSE", "current_zone": "B", "target_tool": "scalpel"},
    
    # Recovery rung 1: FIRM grip
    {"state": "RECOVERING", "task": "Assemble surgical tray with scalpel, forceps, scissors", "action_history": [{"tool": "gripper_close", "params": {"force_level": "MEDIUM"}, "result": "SLIP_DETECTED"}, {"tool": "gripper_close", "params": {"force_level": "FIRM"}, "result": "GRASP_SUCCESS"}], "tried_and_failed": ["vision_scan(A)", "gripper_close(MEDIUM)"], "joint_angles": [-0.28, -0.55, 1.25, 0.0, 0.85, -0.1], "gripper_state": "CLOSED", "gripper_force": 2.3, "current_zone": "B", "held_tool": "scalpel"},
    
    # Lifting scalpel
    {"state": "HOLDING", "task": "Assemble surgical tray with scalpel, forceps, scissors", "action_history": [{"tool": "gripper_close", "params": {"force_level": "FIRM"}, "result": "GRASP_SUCCESS"}, {"tool": "arm_move", "params": {"target_xyz": [0.35, 0.0, 0.25], "wrist_rpy": [0.0, 0.0, 0.0]}, "result": "MOTION_COMPLETE"}], "tried_and_failed": ["vision_scan(A)", "gripper_close(MEDIUM)"], "joint_angles": [0.0, -0.3, 0.8, 0.0, 0.2, 0.0], "gripper_state": "CLOSED", "held_tool": "scalpel"},
    
    # Moving to tray placement zone
    {"state": "PLACING", "task": "Assemble surgical tray with scalpel, forceps, scissors", "action_history": [{"tool": "arm_move", "params": {"target_xyz": [0.35, 0.0, 0.25], "wrist_rpy": [0.0, 0.0, 0.0]}, "result": "MOTION_COMPLETE"}, {"tool": "arm_move", "params": {"target_xyz": [0.5, -0.2, 0.15], "wrist_rpy": [0.0, 0.0, 0.0]}, "result": "MOTION_COMPLETE"}], "tried_and_failed": ["vision_scan(A)", "gripper_close(MEDIUM)"], "joint_angles": [0.2, -0.4, 0.9, 0.0, 0.3, 0.0], "gripper_state": "CLOSED", "held_tool": "scalpel"},
    
    # Releasing scalpel
    {"state": "PLACING", "task": "Assemble surgical tray with scalpel, forceps, scissors", "action_history": [{"tool": "arm_move", "params": {"target_xyz": [0.5, -0.2, 0.15], "wrist_rpy": [0.0, 0.0, 0.0]}, "result": "MOTION_COMPLETE"}, {"tool": "gripper_open", "params": {}, "result": "RELEASE_SUCCESS"}], "tried_and_failed": ["vision_scan(A)", "gripper_close(MEDIUM)"], "joint_angles": [0.2, -0.4, 0.9, 0.0, 0.3, 0.0], "gripper_state": "OPEN", "tray_contents": ["scalpel"]},
    
    # Searching for forceps
    {"state": "SEARCHING", "task": "Assemble surgical tray with scalpel, forceps, scissors", "action_history": [{"tool": "gripper_open", "params": {}, "result": "RELEASE_SUCCESS"}, {"tool": "vision_scan", "params": {"zone": "B"}, "result": "TOOL_NOT_FOUND"}], "tried_and_failed": ["vision_scan(A)", "gripper_close(MEDIUM)", "vision_scan(B)_forceps"], "joint_angles": [-0.3, -0.6, 1.3, 0.0, 0.2, -0.1], "gripper_state": "OPEN", "current_zone": "B", "tray_contents": ["scalpel"]},
]

results = []
TOTAL_CALLS = 35

print(f"Starting Groq GPT-OSS 120B stress test ({TOTAL_CALLS} calls)...")
print("=" * 70)

for i in range(TOTAL_CALLS):
    # Rotate through state templates for realistic progression
    state = STATE_TEMPLATES[i % len(STATE_TEMPLATES)]
    state_msg = json.dumps(state, indent=2)
    
    print(f"[{i+1}/{TOTAL_CALLS}] Calling GPT-OSS 120B...", flush=True)
    start = time.time()
    
    try:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Current state:\n{state_msg}\n\nDecide the next action. Return JSON."}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=256
        )
        elapsed = time.time() - start
        content = resp.choices[0].message.content
        
        # Try to parse JSON
        try:
            data = json.loads(content)
            tool = data.get('tool', 'N/A')
            reason = data.get('reason', '')[:50]
            print(f"  ✓ {elapsed:.2f}s - {tool}: {reason}", flush=True)
            results.append({
                "call": i+1, 
                "status": "OK", 
                "time": elapsed, 
                "tool": tool,
                "reason": reason,
                "json_valid": True
            })
        except json.JSONDecodeError as e:
            print(f"  ✗ {elapsed:.2f}s - JSON PARSE ERROR: {str(e)[:60]}", flush=True)
            print(f"    Content preview: {content[:100]}...", flush=True)
            results.append({
                "call": i+1, 
                "status": "JSON_ERROR", 
                "time": elapsed, 
                "error": str(e)[:100],
                "json_valid": False
            })
            
    except Exception as e:
        elapsed = time.time() - start
        err = str(e)
        if "429" in err or "rate" in err.lower():
            print(f"  ✗ {elapsed:.2f}s - RATE LIMIT: {err[:80]}", flush=True)
            results.append({"call": i+1, "status": "RATE_LIMIT", "time": elapsed, "error": err[:150]})
        else:
            print(f"  ✗ {elapsed:.2f}s - ERROR: {err[:80]}", flush=True)
            results.append({"call": i+1, "status": "ERROR", "time": elapsed, "error": err[:150]})
    
    # Small delay to avoid overwhelming the API
    time.sleep(0.5)

print("\n" + "=" * 70)
print("STRESS TEST RESULTS - Groq GPT-OSS 120B")
print("=" * 70)

ok = sum(1 for r in results if r['status'] == 'OK')
json_err = sum(1 for r in results if r['status'] == 'JSON_ERROR')
rl = sum(1 for r in results if r['status'] == 'RATE_LIMIT')
other = sum(1 for r in results if r['status'] == 'ERROR')

print(f"Total calls:        {TOTAL_CALLS}")
print(f"Successful (OK):    {ok} ({100*ok/TOTAL_CALLS:.1f}%)")
print(f"JSON parse errors:  {json_err} ({100*json_err/TOTAL_CALLS:.1f}%)")
print(f"Rate limits (429):  {rl} ({100*rl/TOTAL_CALLS:.1f}%)")
print(f"Other errors:       {other} ({100*other/TOTAL_CALLS:.1f}%)")

if ok > 0:
    avg_time = sum(r['time'] for r in results if r['status'] == 'OK') / ok
    print(f"\nAverage latency (OK calls): {avg_time:.2f}s")

if rl > 0:
    first_rl = next(r for r in results if r['status'] == 'RATE_LIMIT')
    print(f"\n⚠ RATE LIMIT HIT at call #{first_rl['call']}")
    print(f"  Error: {first_rl['error']}")

# Compare with Nemotron-49B results
print("\n" + "=" * 70)
print("COMPARISON: GPT-OSS 120B vs Nemotron-49B")
print("=" * 70)
print(f"{'Metric':<25} {'GPT-OSS 120B':<15} {'Nemotron-49B':<15}")
print("-" * 70)
print(f"{'JSON Success Rate':<25} {100*ok/TOTAL_CALLS:.1f}%{'':<10} {100*2/10:.1f}%")
print(f"{'Rate Limits':<25} {rl}{'':<13} 0")
print(f"{'Avg Latency':<25} {avg_time:.2f}s{'':<11} 3.64s")

print("\n" + "=" * 70)

# Save results
with open("/mnt/c/users/sonali/desktop/acare/groq_gpt_oss_results.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"Results saved to groq_gpt_oss_results.json")

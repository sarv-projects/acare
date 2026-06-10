#!/usr/bin/env python3
"""
NVIDIA NIM Rate Limit Test for ACARE Agentic Planner
Tests actual API behavior with 35 sequential calls using realistic planner context
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

# Load .env from acare_voice directory
ENV_PATH = Path(__file__).parent / "acare_software_final" / "acare_voice" / ".env"
if ENV_PATH.exists():
    with open(ENV_PATH) as f:
        for line in f:
            if line.strip() and not line.startswith('#') and '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
    print(f"✓ Loaded .env from {ENV_PATH}")
else:
    print(f"✗ .env not found at {ENV_PATH}")
    sys.exit(1)

# Verify API key
NVIDIA_KEY = os.environ.get("NVIDIA_API_KEY")
if not NVIDIA_KEY:
    print("✗ NVIDIA_API_KEY not found in environment")
    sys.exit(1)
print(f"✓ NVIDIA API key loaded: {NVIDIA_KEY[:20]}...{NVIDIA_KEY[-10:]}")

# Initialize OpenAI client
try:
    from openai import OpenAI
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_KEY,
        timeout=10.0
    )
    print("✓ OpenAI client initialized")
except ImportError:
    print("✗ openai package not installed. Install with: pip install openai")
    sys.exit(1)
except Exception as e:
    print(f"✗ Client init failed: {e}")
    sys.exit(1)

# Exact system prompt from agentic_planner.py
PLANNER_SYSTEM_PROMPT = """You are the task executor for ACARE, a surgical instrument fetch robot.
You receive a state snapshot and return exactly ONE tool call as JSON.
HARD RULES:
* Return ONLY a JSON object. No markdown. No explanation outside JSON.
* Call exactly one tool per turn. Never plan ahead.
* Never repeat an action that appears in tried_and_failed.
* Never fabricate tools or parameters not in available_tools.
* If budget.calls_remaining <= 2 and task is not near completion, call abort_task.
* Speech must be brief (<20 words), clinical, professional. No medical advice.
* NEVER move the arm to a position not listed in available arm positions.
* Follow the recovery ladders EXACTLY. Do not improvise or skip rungs.
TASK SEQUENCE:
1. vision_scan -> find the tool
2. arm_move(PREGRASP) -> above tool
3. arm_move(GRASP_POINT) -> descend to tool
4. gripper_close(NORMAL) -> grasp
5. arm_move(FACE_HEIGHT) -> face user
6. detect_face -> verify identity
7. arm_move(PRESENTATION) -> present tool
8. speak -> instruct user
9. detect_hand -> user reaches
10. ask_user(expect=CONFIRM) -> voice confirm
11. gripper_open -> release
12. complete_task
RECOVERY LADDERS — follow in strict order, never skip rungs:
VISION FAILURE (vision_scan returns NOT_FOUND):
  Rung 1: If user_prior.preferred_zone exists and not yet tried -> vision_scan({'zone': preferred_zone})
  Rung 2: vision_scan({'zone': 'AUTO'}) — queries Bayesian probability map
  Rung 3: If AUTO fails -> ask_user("I cannot find the [tool]. Is it on the tray?")
  Rung 4: If user responds with location -> vision_scan({'zone': that_zone})
  Rung 5: If user says no or timeout -> abort_task("Unable to locate [tool]")
GRASP FAILURE (gripper_close returns SLIP_DETECTED):
  Rung 1: gripper_close(FIRM) — same position, more force
  Rung 2: arm_approach(SIDE_LEFT) then arm_move(PREGRASP) then arm_move(GRASP_POINT) then gripper_close(FIRM) — different angle
  Rung 3: If detection_candidates exist in snapshot -> arm_move to next candidate, repeat grasp
  Rung 4: abort_task("Unable to grasp [tool]")
ARM UNREACHABLE (arm_move returns UNREACHABLE):
  Rung 1: arm_approach(SIDE_LEFT) then retry arm_move
  Rung 2: arm_approach(SIDE_RIGHT) then retry arm_move
  Rung 3: If detection_candidates exist -> arm_move to next candidate
  Rung 4: abort_task("[tool] is out of reach")
FACE DETECTION FAILURE (detect_face returns NO_FACE or WRONG_FACE):
  Rung 1: speak("Please look at the camera") then detect_face
  Rung 2: speak("Please face the camera directly") then detect_face
  Rung 3: Skip face. Proceed to arm_move(PRESENTATION). Face is advisory.
HAND DETECTION FAILURE (detect_hand returns NO_HAND):
  Rung 1: speak("Please reach for the tool") then detect_hand
  Rung 2: speak("Hold your hand near the gripper") then detect_hand
  Rung 3: abort_task("Handover failed - no hand detected")
VOICE CONFIRM FAILURE (ask_user returns TIMEOUT):
  Rung 1: speak("Say take to receive") then ask_user(expect=CONFIRM)
  Rung 2: abort_task("No voice confirmation received")
ESTOP (any tool returns ESTOP):
  -> abort_task("ESTOP") immediately. No recovery. No retry.
RESPONSE FORMAT:
{
  "thought": "brief reason, max 1 sentence",
  "tool": "tool_name",
  "params": {"param1": "value1"},
  "speak": "optional tts message or null"
}
EXAMPLES:
State: task_phase=SEARCHING, zones_searched=[], user_prior.preferred_zone=C
Response: {"thought":"User prefers zone C, start there","tool":"vision_scan","params":{"zone":"C"},"speak":null}
State: task_phase=SEARCHING, last_action=vision_scan(A) NOT_FOUND, zones_searched=[A,B]
Response: {"thought":"A and B failed, try C","tool":"vision_scan","params":{"zone":"C"},"speak":null}
State: task_phase=GRASPING, last_action=gripper_close(NORMAL) SLIP_DETECTED
Response: {"thought":"Normal grip slipped, increase firmness","tool":"gripper_close","params":{"firmness":"FIRM"},"speak":"Adjusting grip. One moment."}
State: task_phase=HANDOVER, last_action=detect_face() NO_FACE, action_history has 2 face failures
Response: {"thought":"Face failed twice, skip and proceed to present","tool":"arm_move","params":{"position":"PRESENTATION"},"speak":"Proceeding with voice and hand verification."}
"""

def generate_realistic_snapshot(call_num: int) -> Dict:
    """Generate increasingly complex state snapshots simulating a real task"""
    
    # Base snapshot structure matching state_snapshot.py
    base = {
        "objective": {
            "tool": "scalpel",
            "user": "Dr. Smith",
            "task_phase": "SEARCHING"
        },
        "world": {
            "arm_at": "REST",
            "gripper": "OPEN",
            "safety": "OK",
            "holding_tool": False,
            "vision_ready": True
        },
        "last_action": {
            "tool_call": "",
            "result": "",
            "reason": ""
        },
        "action_history": [],
        "budget": {
            "calls_used": call_num,
            "calls_remaining": max(0, 20 - call_num)
        },
        "tried_and_failed": [],
        "zones_searched": [],
        "user_prior": {
            "preferred_zone": "C",
            "handover_z_offset": "MEDIUM"
        },
        "available_tools": [
            "vision_scan", "arm_move", "arm_approach", "gripper_close", 
            "gripper_open", "detect_face", "detect_hand", "speak", 
            "ask_user", "complete_task", "abort_task"
        ]
    }
    
    # Simulate progression through task phases with realistic failures and retries
    if call_num == 0:
        # Initial state - start searching
        base["last_action"]["tool_call"] = ""
        base["last_action"]["result"] = "INIT"
        
    elif call_num == 1:
        # First vision scan in preferred zone
        base["last_action"]["tool_call"] = "vision_scan({'zone': 'C'})"
        base["last_action"]["result"] = "NOT_FOUND"
        base["last_action"]["reason"] = "No scalpel detected in zone C after 3 frames"
        base["zones_searched"] = ["C"]
        base["tried_and_failed"] = ["vision_scan({'zone': 'C'})"]
        base["action_history"] = [
            {"call": "vision_scan({'zone': 'C'})", "result": "NOT_FOUND", "n": 1}
        ]
        
    elif call_num == 2:
        # Try AUTO zone (Bayesian)
        base["last_action"]["tool_call"] = "vision_scan({'zone': 'AUTO'})"
        base["last_action"]["result"] = "NOT_FOUND"
        base["last_action"]["reason"] = "Bayesian map suggests zone A, no detection"
        base["zones_searched"] = ["C", "A"]
        base["tried_and_failed"] = [
            "vision_scan({'zone': 'C'})",
            "vision_scan({'zone': 'AUTO'})"
        ]
        base["action_history"] = [
            {"call": "vision_scan({'zone': 'C'})", "result": "NOT_FOUND", "n": 1},
            {"call": "vision_scan({'zone': 'AUTO'})", "result": "NOT_FOUND", "n": 1}
        ]
        
    elif call_num == 3:
        # Ask user for help
        base["last_action"]["tool_call"] = 'ask_user({"question": "I cannot find the scalpel. Is it on the tray?", "expect": "LOCATION"})'
        base["last_action"]["result"] = "SUCCESS"
        base["last_action"]["reason"] = "User responded: 'Check zone B'"
        base["zones_searched"] = ["C", "A"]
        base["tried_and_failed"] = [
            "vision_scan({'zone': 'C'})",
            "vision_scan({'zone': 'AUTO'})",
            'ask_user({"question": "...", "expect": "LOCATION"})'
        ]
        base["action_history"] = [
            {"call": "vision_scan({'zone': 'C'})", "result": "NOT_FOUND", "n": 1},
            {"call": "vision_scan({'zone': 'AUTO'})", "result": "NOT_FOUND", "n": 1},
            {"call": "ask_user(...)", "result": "SUCCESS", "n": 1}
        ]
        
    elif call_num == 4:
        # Vision scan in user-suggested zone - SUCCESS
        base["objective"]["task_phase"] = "SEARCHING"
        base["last_action"]["tool_call"] = "vision_scan({'zone': 'B'})"
        base["last_action"]["result"] = "SUCCESS"
        base["last_action"]["reason"] = "Scalpel detected at (x=0.45, y=-0.12, z=0.08) with conf=0.92"
        base["zones_searched"] = ["C", "A", "B"]
        base["world"]["vision_ready"] = True
        base["tried_and_failed"] = [
            "vision_scan({'zone': 'C'})",
            "vision_scan({'zone': 'AUTO'})"
        ]
        base["action_history"] = [
            {"call": "vision_scan({'zone': 'AUTO'})", "result": "NOT_FOUND", "n": 1},
            {"call": "ask_user(...)", "result": "SUCCESS", "n": 1},
            {"call": "vision_scan({'zone': 'B'})", "result": "SUCCESS", "n": 1}
        ]
        
    elif call_num == 5:
        # Move to pregrasp
        base["objective"]["task_phase"] = "GRASPING"
        base["last_action"]["tool_call"] = "arm_move({'position': 'PREGRASP'})"
        base["last_action"]["result"] = "SUCCESS"
        base["last_action"]["reason"] = "Arm at pregrasp pose above detected tool"
        base["world"]["arm_at"] = "PREGRASP"
        base["action_history"] = [
            {"call": "ask_user(...)", "result": "SUCCESS", "n": 1},
            {"call": "vision_scan({'zone': 'B'})", "result": "SUCCESS", "n": 1},
            {"call": "arm_move({'position': 'PREGRASP'})", "result": "SUCCESS", "n": 1}
        ]
        
    elif call_num == 6:
        # Move to grasp point
        base["objective"]["task_phase"] = "GRASPING"
        base["last_action"]["tool_call"] = "arm_move({'position': 'GRASP_POINT'})"
        base["last_action"]["result"] = "SUCCESS"
        base["last_action"]["reason"] = "Arm descended to grasp pose"
        base["world"]["arm_at"] = "GRASP_POINT"
        base["action_history"] = [
            {"call": "vision_scan({'zone': 'B'})", "result": "SUCCESS", "n": 1},
            {"call": "arm_move({'position': 'PREGRASP'})", "result": "SUCCESS", "n": 1},
            {"call": "arm_move({'position': 'GRASP_POINT'})", "result": "SUCCESS", "n": 1}
        ]
        
    elif call_num == 7:
        # First grasp attempt - SLIP
        base["objective"]["task_phase"] = "GRASPING"
        base["last_action"]["tool_call"] = "gripper_close({'firmness': 'NORMAL'})"
        base["last_action"]["result"] = "SLIP_DETECTED"
        base["last_action"]["reason"] = "Gripper force insufficient, tool slipped"
        base["world"]["gripper"] = "CLOSED"
        base["tried_and_failed"] = [
            "vision_scan({'zone': 'C'})",
            "vision_scan({'zone': 'AUTO'})",
            "gripper_close({'firmness': 'NORMAL'})"
        ]
        base["action_history"] = [
            {"call": "arm_move({'position': 'PREGRASP'})", "result": "SUCCESS", "n": 1},
            {"call": "arm_move({'position': 'GRASP_POINT'})", "result": "SUCCESS", "n": 1},
            {"call": "gripper_close({'firmness': 'NORMAL'})", "result": "SLIP_DETECTED", "n": 1}
        ]
        
    elif call_num == 8:
        # Retry with FIRM grip - SUCCESS
        base["objective"]["task_phase"] = "GRASPING"
        base["last_action"]["tool_call"] = "gripper_close({'firmness': 'FIRM'})"
        base["last_action"]["result"] = "SUCCESS"
        base["last_action"]["reason"] = "Tool grasped successfully with increased force"
        base["world"]["gripper"] = "CLOSED"
        base["world"]["holding_tool"] = True
        base["tried_and_failed"] = [
            "vision_scan({'zone': 'C'})",
            "vision_scan({'zone': 'AUTO'})",
            "gripper_close({'firmness': 'NORMAL'})"
        ]
        base["action_history"] = [
            {"call": "arm_move({'position': 'GRASP_POINT'})", "result": "SUCCESS", "n": 1},
            {"call": "gripper_close({'firmness': 'NORMAL'})", "result": "SLIP_DETECTED", "n": 1},
            {"call": "gripper_close({'firmness': 'FIRM'})", "result": "SUCCESS", "n": 1}
        ]
        
    elif call_num == 9:
        # Move to face height
        base["objective"]["task_phase"] = "HANDOVER"
        base["last_action"]["tool_call"] = "arm_move({'position': 'FACE_HEIGHT'})"
        base["last_action"]["result"] = "SUCCESS"
        base["last_action"]["reason"] = "Arm raised to face detection height"
        base["world"]["arm_at"] = "FACE_HEIGHT"
        base["action_history"] = [
            {"call": "gripper_close({'firmness': 'NORMAL'})", "result": "SLIP_DETECTED", "n": 1},
            {"call": "gripper_close({'firmness': 'FIRM'})", "result": "SUCCESS", "n": 1},
            {"call": "arm_move({'position': 'FACE_HEIGHT'})", "result": "SUCCESS", "n": 1}
        ]
        
    elif call_num == 10:
        # First face detection - NO_FACE
        base["objective"]["task_phase"] = "HANDOVER"
        base["last_action"]["tool_call"] = "detect_face({})"
        base["last_action"]["result"] = "NO_FACE"
        base["last_action"]["reason"] = "No face detected in camera frame"
        base["tried_and_failed"] = [
            "vision_scan({'zone': 'C'})",
            "vision_scan({'zone': 'AUTO'})",
            "gripper_close({'firmness': 'NORMAL'})",
            "detect_face({})"
        ]
        base["action_history"] = [
            {"call": "gripper_close({'firmness': 'FIRM'})", "result": "SUCCESS", "n": 1},
            {"call": "arm_move({'position': 'FACE_HEIGHT'})", "result": "SUCCESS", "n": 1},
            {"call": "detect_face({})", "result": "NO_FACE", "n": 1}
        ]
        
    elif call_num == 11:
        # Speak to user
        base["objective"]["task_phase"] = "HANDOVER"
        base["last_action"]["tool_call"] = "speak({'text': 'Please look at the camera'})"
        base["last_action"]["result"] = "SUCCESS"
        base["last_action"]["reason"] = "TTS playback completed"
        base["action_history"] = [
            {"call": "arm_move({'position': 'FACE_HEIGHT'})", "result": "SUCCESS", "n": 1},
            {"call": "detect_face({})", "result": "NO_FACE", "n": 1},
            {"call": "speak({'text': 'Please look at the camera'})", "result": "SUCCESS", "n": 1}
        ]
        
    elif call_num == 12:
        # Second face detection - SUCCESS
        base["objective"]["task_phase"] = "HANDOVER"
        base["last_action"]["tool_call"] = "detect_face({})"
        base["last_action"]["result"] = "SUCCESS"
        base["last_action"]["reason"] = "Face verified: Dr. Smith (confidence=0.89)"
        base["tried_and_failed"] = [
            "vision_scan({'zone': 'C'})",
            "vision_scan({'zone': 'AUTO'})",
            "gripper_close({'firmness': 'NORMAL'})"
        ]
        base["action_history"] = [
            {"call": "detect_face({})", "result": "NO_FACE", "n": 1},
            {"call": "speak({'text': 'Please look at the camera'})", "result": "SUCCESS", "n": 1},
            {"call": "detect_face({})", "result": "SUCCESS", "n": 1}
        ]
        
    elif call_num >= 13 and call_num < 35:
        # Continue with remaining steps (presentation, hand detection, voice confirm, etc.)
        # Simulate various failures and recoveries to stress-test the API
        phase_step = (call_num - 13) % 5
        
        if phase_step == 0:
            base["objective"]["task_phase"] = "HANDOVER"
            base["last_action"]["tool_call"] = "arm_move({'position': 'PRESENTATION'})"
            base["last_action"]["result"] = "SUCCESS"
            base["world"]["arm_at"] = "PRESENTATION"
        elif phase_step == 1:
            base["last_action"]["tool_call"] = "detect_hand({})"
            base["last_action"]["result"] = "NO_HAND"
            base["last_action"]["reason"] = "No hand detected near gripper"
            base["tried_and_failed"].append("detect_hand({})")
        elif phase_step == 2:
            base["last_action"]["tool_call"] = "speak({'text': 'Please reach for the tool'})"
            base["last_action"]["result"] = "SUCCESS"
        elif phase_step == 3:
            base["last_action"]["tool_call"] = "detect_hand({})"
            base["last_action"]["result"] = "SUCCESS"
            base["last_action"]["reason"] = "Hand detected approaching"
        else:
            base["last_action"]["tool_call"] = "ask_user({'question': 'Take it', 'expect': 'CONFIRM'})"
            base["last_action"]["result"] = "SUCCESS" if call_num % 3 != 0 else "TIMEOUT"
            base["last_action"]["reason"] = "User confirmed" if call_num % 3 != 0 else "No response within 10s"
            
        # Keep action history bounded (like real planner does)
        if len(base["action_history"]) > 3:
            base["action_history"] = base["action_history"][-3:]
    
    else:
        # Final calls - complete or abort
        base["objective"]["task_phase"] = "HANDOVER"
        base["last_action"]["tool_call"] = "gripper_open({})"
        base["last_action"]["result"] = "SUCCESS"
        base["world"]["gripper"] = "OPEN"
        base["world"]["holding_tool"] = False
    
    # Convert to JSON message format expected by planner
    return {
        "role": "user",
        "content": f"Current State Snapshot:\n```json\n{json.dumps(base, indent=2)}\n```\nAnalyze the state and propose the next tool call."
    }


def test_nvidia_nim_rate_limits():
    """Execute 35 sequential API calls and track rate limit behavior"""
    
    print("\n" + "="*80)
    print("NVIDIA NIM Rate Limit Test - ACARE Agentic Planner")
    print("="*80)
    print(f"Target: 35 sequential calls with realistic planner context")
    print(f"Model: nvidia/llama-3.3-nemotron-super-49b-v1")
    print(f"Expected free-tier limit: ~100 requests/hour")
    print("="*80 + "\n")
    
    results = []
    rate_limit_hits = 0
    total_time = 0
    
    for i in range(35):
        print(f"\n[Call {i+1}/35] ", end="", flush=True)
        
        # Generate realistic state snapshot
        snapshot_msg = generate_realistic_snapshot(i)
        messages = [
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            snapshot_msg
        ]
        
        # Make API call
        start_time = time.time()
        try:
            response = client.chat.completions.create(
                model="nvidia/llama-3.3-nemotron-super-49b-v1",
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=256
            )
            elapsed = time.time() - start_time
            total_time += elapsed
            
            # Parse response
            content = response.choices[0].message.content
            decision = json.loads(content)
            
            # Log success
            print(f"✓ {elapsed:.2f}s | Tool: {decision.get('tool', 'N/A'):<20} | Thought: {decision.get('thought', '')[:40]}...")
            
            results.append({
                "call_num": i + 1,
                "status": "SUCCESS",
                "elapsed": elapsed,
                "tool": decision.get("tool"),
                "thought": decision.get("thought"),
                "error": None
            })
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = str(e)
            
            # Check if it's a rate limit error
            if "429" in error_msg or "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
                rate_limit_hits += 1
                print(f"✗ {elapsed:.2f}s | RATE LIMIT HIT: {error_msg[:80]}...")
                results.append({
                    "call_num": i + 1,
                    "status": "RATE_LIMIT",
                    "elapsed": elapsed,
                    "tool": None,
                    "thought": None,
                    "error": error_msg
                })
            else:
                print(f"✗ {elapsed:.2f}s | ERROR: {error_msg[:80]}...")
                results.append({
                    "call_num": i + 1,
                    "status": "ERROR",
                    "elapsed": elapsed,
                    "tool": None,
                    "thought": None,
                    "error": error_msg
                })
        
        # Small delay between calls (not too fast to avoid instant rate limiting)
        if i < 34:
            time.sleep(0.5)
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    error_count = sum(1 for r in results if r["status"] == "ERROR")
    
    print(f"Total calls:           35")
    print(f"Successful:            {success_count}")
    print(f"Rate limit hits:       {rate_limit_hits}")
    print(f"Other errors:          {error_count}")
    print(f"Total time:            {total_time:.2f}s")
    print(f"Average latency:       {total_time/max(success_count, 1):.2f}s per call")
    print()
    
    if rate_limit_hits > 0:
        print(f"⚠ RATE LIMIT CONFIRMED: Hit {rate_limit_hits} times during test")
        print(f"  First hit at call #{next(r['call_num'] for r in results if r['status'] == 'RATE_LIMIT')}")
        print(f"  This confirms the free-tier limit is being enforced")
    else:
        print(f"✓ NO RATE LIMITS HIT: All 35 calls succeeded")
        print(f"  The API accepted all requests within the test window")
    
    print()
    
    # Show tool distribution
    tool_counts = {}
    for r in results:
        if r["tool"]:
            tool_counts[r["tool"]] = tool_counts.get(r["tool"], 0) + 1
    
    if tool_counts:
        print("Tool call distribution:")
        for tool, count in sorted(tool_counts.items(), key=lambda x: -x[1]):
            print(f"  {tool:<25} {count} calls")
    
    print("="*80)
    
    return results


if __name__ == "__main__":
    try:
        results = test_nvidia_nim_rate_limits()
        
        # Save detailed results to JSON
        results_file = Path(__file__).parent / "nim_rate_limit_results.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Detailed results saved to: {results_file}")
        
    except KeyboardInterrupt:
        print("\n\n✗ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

#!/usr/bin/env python3
"""
DeepSeek vs Nemotron-49B Benchmark for ACARE Agentic Planner
Tests: deepseek-v3.1-terminus, deepseek-v4-flash, nemotron-super-49b-v1
Uses actual ACARE planner prompts and validates JSON tool-call output.
"""

import os
import sys
import time
import json
import requests
from pathlib import Path

# --- Configuration ---
TEST_CALLS_PER_MODEL = 5
REQUEST_TIMEOUT = 15.0  # seconds
INTER_CALL_DELAY = 1.0  # seconds between calls

# ACARE Planner System Prompt (from agentic_planner.py)
SYSTEM_PROMPT = """You are the agentic planner for ACARE, an autonomous clinical assistance robot.
You must respond with a JSON object containing exactly:
- "tool": the tool name to execute
- "params": dictionary of parameters for the tool
- "reason": brief explanation of why this tool is chosen

Available tools:
- vision_scan(zone: str) - Search for tools in a zone (A, B, C)
- arm_move(x: float, y: float, z: float) - Move arm to position in meters
- arm_approach(x: float, y: float, z: float, direction: str) - Approach from direction (ABOVE, SIDE_LEFT, SIDE_RIGHT)
- gripper_close(force: str) - Close gripper (NORMAL, FIRM, GENTLE)
- gripper_open() - Open gripper
- detect_face() - Verify surgeon face for handover
- detect_hand() - Detect open palm for handover
- speak(message: str) - Speak to surgeon
- ask_user(question: str) - Ask surgeon a question
- complete_task() - Mark task complete
- abort_task(reason: str) - Abort with reason

Current state: Robot at REST position, gripper OPEN, holding: NONE, safety: OK
Objective: Fetch medical scissors for Dr. Smith"""

# Test prompts simulating different planner states
TEST_PROMPTS = [
    "I need to find the scissors. What should I do first?",
    "I scanned zone A but didn't find scissors. What's the next step?",
    "Found scissors at position (0.45, 0.0, 0.05). How should I grasp it?",
    "Gripper closed successfully with NORMAL force. What now?",
    "Tool is held securely. How do I present it to the surgeon for handover?"
]


def load_nvidia_key():
    """Load NVIDIA API key from .env file or environment"""
    env_paths = [
        Path("acare_software_final/acare_voice/.env"),
        Path("acare_voice/.env"),
        Path("../acare_voice/.env"),
        Path("/mnt/c/users/sonali/desktop/acare/acare_software_final/acare_voice/.env"),
        Path(".env"),
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("NVIDIA_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        print(f"✓ Loaded API key from {env_path}")
                        print(f"  Key prefix: {key[:15]}...")
                        return key
    
    # Try environment variable
    key = os.environ.get("NVIDIA_API_KEY")
    if key:
        print("✓ Loaded API key from environment variable")
        return key
    
    print("✗ NVIDIA_API_KEY not found in .env or environment")
    return None


def call_nvidia_model(model_id: str, messages: list, api_key: str):
    """Call NVIDIA NIM API with given model"""
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_id,
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": 256,
        "stream": False
    }
    
    # Add thinking=False for DeepSeek models (hybrid inference)
    if "deepseek" in model_id.lower():
        payload["extra_body"] = {
            "chat_template_kwargs": {
                "thinking": False
            }
        }
    
    start = time.time()
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)
        latency = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            
            # Try to parse as JSON
            try:
                # Clean up potential markdown code blocks
                cleaned = content.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()
                
                parsed = json.loads(cleaned)
                return {
                    "status": "ok",
                    "latency": latency,
                    "content": content[:200],
                    "parsed": parsed,
                    "tool": parsed.get("tool", "N/A"),
                    "tokens_in": usage.get("prompt_tokens", 0),
                    "tokens_out": usage.get("completion_tokens", 0)
                }
            except json.JSONDecodeError as e:
                return {
                    "status": "json_error",
                    "latency": latency,
                    "content": content[:200],
                    "parse_error": str(e),
                    "tokens_in": usage.get("prompt_tokens", 0),
                    "tokens_out": usage.get("completion_tokens", 0)
                }
        elif response.status_code == 429:
            return {
                "status": "rate_limited",
                "latency": latency,
                "error": f"HTTP 429: {response.text[:150]}"
            }
        else:
            return {
                "status": "error",
                "latency": latency,
                "error": f"HTTP {response.status_code}: {response.text[:150]}"
            }
    except requests.exceptions.Timeout:
        return {
            "status": "timeout",
            "latency": time.time() - start,
            "error": f"Timeout after {REQUEST_TIMEOUT}s"
        }
    except Exception as e:
        return {
            "status": "exception",
            "latency": time.time() - start,
            "error": str(e)
        }


def test_model(model_id: str, api_key: str, num_calls: int = TEST_CALLS_PER_MODEL):
    """Test a model with ACARE-style prompts"""
    print(f"\n{'='*70}")
    print(f"Testing: {model_id}")
    print(f"{'='*70}")
    
    results = []
    for i, prompt in enumerate(TEST_PROMPTS[:num_calls]):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        print(f"\nCall {i+1}/{num_calls}: {prompt[:60]}...")
        result = call_nvidia_model(model_id, messages, api_key)
        results.append(result)
        
        if result["status"] == "ok":
            print(f"  ✓ {result['latency']:.3f}s | {result['tokens_in']}+{result['tokens_out']} tokens")
            print(f"    Tool: {result['tool']}")
            if result.get('parsed', {}).get('reason'):
                print(f"    Reason: {result['parsed']['reason'][:80]}")
        elif result["status"] == "json_error":
            print(f"  ⚠ JSON parse failed | {result['latency']:.3f}s")
            print(f"    Error: {result.get('parse_error', 'Unknown')[:80]}")
            print(f"    Content: {result['content'][:100]}...")
        elif result["status"] == "rate_limited":
            print(f"  ✗ RATE LIMITED | {result['latency']:.3f}s")
            print(f"    {result.get('error', '')[:100]}")
        else:
            print(f"  ✗ {result['status']} | {result['latency']:.3f}s")
            print(f"    Error: {result.get('error', 'Unknown')[:100]}")
        
        time.sleep(INTER_CALL_DELAY)
    
    # Summary
    ok_count = sum(1 for r in results if r["status"] == "ok")
    rate_limited = sum(1 for r in results if r["status"] == "rate_limited")
    latencies = [r["latency"] for r in results if r["status"] in ["ok", "json_error"]]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    
    print(f"\n{model_id} Summary:")
    print(f"  Success: {ok_count}/{num_calls} ({ok_count/num_calls:.0%})")
    print(f"  Rate Limited: {rate_limited}/{num_calls}")
    print(f"  Avg latency: {avg_latency:.3f}s")
    
    return {
        "model": model_id,
        "results": results,
        "success_rate": ok_count / num_calls,
        "rate_limited": rate_limited,
        "avg_latency": avg_latency
    }


def main():
    print("="*70)
    print("DeepSeek vs Nemotron-49B Benchmark for ACARE")
    print("="*70)
    
    api_key = load_nvidia_key()
    if not api_key:
        print("\n" + "="*70)
        print("ERROR: NVIDIA_API_KEY not found")
        print("="*70)
        print("\nPlease set NVIDIA_API_KEY in one of these locations:")
        print("  1. acare_voice/.env")
        print("  2. .env in current directory")
        print("  3. NVIDIA_API_KEY environment variable")
        print("\nExample .env line:")
        print('  NVIDIA_API_KEY="nvapi-xxxxxxxxxxxxx"')
        return 1
    
    # Models to test (in order of recommendation)
    models = [
        "deepseek-ai/deepseek-v3.1-terminus",      # Recommended primary
        "deepseek-ai/deepseek-v4-flash",           # Alternative (may have tool bugs)
        "nvidia/llama-3.3-nemotron-super-49b-v1",  # Current baseline
    ]
    
    all_results = []
    for model in models:
        result = test_model(model, api_key, num_calls=TEST_CALLS_PER_MODEL)
        all_results.append(result)
        time.sleep(3)  # Pause between models
    
    # Final comparison
    print("\n" + "="*70)
    print("FINAL COMPARISON")
    print("="*70)
    print(f"{'Model':<45} {'Success':<10} {'Rate Ltd':<10} {'Avg Latency':<15}")
    print("-"*70)
    for r in all_results:
        print(f"{r['model']:<45} {r['success_rate']:.0%}     {r['rate_limited']}       {r['avg_latency']:.3f}s")
    
    # Recommendation
    print("\n" + "="*70)
    print("RECOMMENDATION")
    print("="*70)
    
    best_model = max(all_results, key=lambda x: (x['success_rate'], -x['rate_limited']))
    print(f"Best performing model: {best_model['model']}")
    print(f"  Success rate: {best_model['success_rate']:.0%}")
    print(f"  Rate limited: {best_model['rate_limited']} times")
    print(f"  Avg latency: {best_model['avg_latency']:.3f}s")
    
    # Save results
    output_file = Path(__file__).parent / "deepseek_benchmark_results.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n✓ Results saved to {output_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

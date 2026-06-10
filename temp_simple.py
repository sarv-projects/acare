#!/usr/bin/env python3
"""Simple NVIDIA NIM rate limit test - 10 calls only"""
import os, sys, json, time
from pathlib import Path

# Load .env
ENV_PATH = Path(__file__).parent / "acare_software_final" / "acare_voice" / ".env"
if ENV_PATH.exists():
    for line in open(ENV_PATH):
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            os.environ[k] = v

KEY = os.environ.get("NVIDIA_API_KEY")
if not KEY:
    print("No key"); sys.exit(1)

from openai import OpenAI
client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=KEY, timeout=10.0)

SYSTEM = "You are a surgical robot planner. Return JSON with tool and params."
results = []

for i in range(10):
    print(f"[{i+1}/10] Calling API...", flush=True)
    start = time.time()
    try:
        resp = client.chat.completions.create(
            model="nvidia/llama-3.3-nemotron-super-49b-v1",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"State: searching for scalpel, call #{i+1}. Return JSON."}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=128
        )
        elapsed = time.time() - start
        data = json.loads(resp.choices[0].message.content)
        print(f"  ✓ {elapsed:.2f}s - {data.get('tool', 'N/A')}", flush=True)
        results.append({"call": i+1, "status": "OK", "time": elapsed, "tool": data.get('tool')})
    except Exception as e:
        elapsed = time.time() - start
        err = str(e)
        if "429" in err or "rate" in err.lower():
            print(f"  ✗ {elapsed:.2f}s - RATE LIMIT: {err[:60]}", flush=True)
            results.append({"call": i+1, "status": "RATE_LIMIT", "time": elapsed, "error": err[:100]})
        else:
            print(f"  ✗ {elapsed:.2f}s - ERROR: {err[:60]}", flush=True)
            results.append({"call": i+1, "status": "ERROR", "time": elapsed, "error": err[:100]})
    time.sleep(1)

print("\n" + "="*60)
ok = sum(1 for r in results if r['status'] == 'OK')
rl = sum(1 for r in results if r['status'] == 'RATE_LIMIT')
print(f"Results: {ok} OK, {rl} rate limits, {10-ok-rl} errors")
if rl > 0:
    print(f"⚠ RATE LIMIT CONFIRMED at call #{next(r['call'] for r in results if r['status']=='RATE_LIMIT')}")
else:
    print("✓ No rate limits hit")
print("="*60)

with open("/mnt/c/users/sonali/desktop/acare/nim_test_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("Results saved to nim_test_results.json")

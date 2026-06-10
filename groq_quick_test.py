#!/usr/bin/env python3
"""Quick Groq GPT-OSS 120B test - 10 calls"""
import os, sys, json, time
from pathlib import Path

ENV_PATH = Path(__file__).parent / "acare_software_final" / "acare_voice" / ".env"
if ENV_PATH.exists():
    for line in open(ENV_PATH):
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            os.environ[k] = v

KEY = os.environ.get("GROQ_API_KEY")
if not KEY:
    print("No GROQ_API_KEY"); sys.exit(1)

from openai import OpenAI
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=KEY, timeout=15.0)

SYSTEM = "You are a surgical robot planner. Return JSON: {\"tool\": \"name\", \"params\": {...}, \"reason\": \"brief\"}"
STATE = {"state": "SEARCHING", "task": "Find scalpel", "action_history": [], "zone": "A"}

results = []
for i in range(10):
    print(f"[{i+1}/10] Calling...", flush=True)
    start = time.time()
    try:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"State: {json.dumps(STATE)}. Decide next action."}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=128
        )
        elapsed = time.time() - start
        content = resp.choices[0].message.content
        try:
            data = json.loads(content)
            print(f"  ✓ {elapsed:.2f}s - {data.get('tool', 'N/A')}", flush=True)
            results.append({"call": i+1, "status": "OK", "time": elapsed, "tool": data.get('tool')})
        except:
            print(f"  ✗ {elapsed:.2f}s - JSON ERROR", flush=True)
            results.append({"call": i+1, "status": "JSON_ERROR", "time": elapsed})
    except Exception as e:
        elapsed = time.time() - start
        err = str(e)
        if "429" in err or "rate" in err.lower():
            print(f"  ✗ {elapsed:.2f}s - RATE LIMIT", flush=True)
            results.append({"call": i+1, "status": "RATE_LIMIT", "time": elapsed, "error": err[:100]})
        else:
            print(f"  ✗ {elapsed:.2f}s - ERROR: {err[:60]}", flush=True)
            results.append({"call": i+1, "status": "ERROR", "time": elapsed, "error": err[:100]})
    time.sleep(0.5)

print("\n" + "="*60)
ok = sum(1 for r in results if r['status'] == 'OK')
rl = sum(1 for r in results if r['status'] == 'RATE_LIMIT')
print(f"Results: {ok}/10 OK, {rl} rate limits")
if ok > 0:
    avg = sum(r['time'] for r in results if r['status'] == 'OK') / ok
    print(f"Avg latency: {avg:.2f}s")
print("="*60)

with open("/mnt/c/users/sonali/desktop/acare/groq_test_results.json", "w") as f:
    json.dump(results, f, indent=2)

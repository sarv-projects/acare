# ACARE Agentic Layer — How It Works

## Overview
The agentic layer is the robot's decision-making brain. It takes a voice command like "fetch scissors" and breaks it down into executable steps, handling failures, safety checks, and recovery automatically.

## Core Loop (agentic_planner.py)

```
User says "fetch scissors"
         │
         ▼
┌─────────────────────────────────────────┐
│  1. LLM Decision (NIM → Groq → Fixed)  │
│     "What should I do next?"            │
│     Returns: vision_scan(zone='AUTO')   │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  2. ToolKernel executes the decision    │
│     - Safety check (L0-L6 gates)        │
│     - Runs the actual tool call         │
│     - Returns result + status           │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  3. Result fed back into LLM            │
│     "Found scissors at (0.45, 0, 0.05)" │
│     LLM decides next step               │
└──────────────────┬──────────────────────┘
                   │
                   ▼
           ┌───────┴───────┐
           │   Done?       │
           │   No → loop   │
           │   Yes → stop  │
           └───────────────┘
```

This runs in a `while True` loop with:
- **Timeout:** adaptive budget (min 180s, calculated per phase)
- **Circuit breaker:** 3 consecutive API failures → skip LLM for 60s
- **Recovery ladder:** NIM → Groq → Deterministic → Abort

---

## Triple Fallback Chain

```
NIM Nemotron-49B (Nvidia, 0.5s latency)
    ↓ failure
Groq Llama 3.3-70B (cloud, 1s latency)
    ↓ failure
Deterministic (code-based, 2ms - always works)
    ↓ failure  
Abort task gracefully
```

**Why 3 tiers:** The robot must never hang waiting for an API. If Nvidia is down, try Groq. If Groq is down, use hardcoded logic. If even that fails, stop safely and ask for help.

---

## State Machine (10 states)

```
OFFLINE → LOGGED_OUT → STANDBY → LISTENING → PROCESSING → 
EXECUTING → HOLDING → HANDOVER → STANDBY (loop)
                            
Any state → ESTOP → STANDBY or OFFLINE
Any state → ERROR → OFFLINE
```

**Key transitions:**
- Listening → Processing: VAD detects speech
- Processing → Executing: Validated intent received
- Executing → Holding: Task completed, arm at presentation
- Holding → Handover: Hand detected reaching for tool
- Handover → Standby: Tool taken, return to rest

---

## Agentic Task Execution Phases

### Phase 1: SEARCH
```
LLM: "vision_scan(zone='A')" 
  → Camera looks at Zone A
  → YOLO checks if tool is there
  → Returns (found=True, xyz=0.45,0,0.05)
LLM: "vision_scan(zone='B')" 
  → If not found in A, try B
  → Bayesian map tracks which zones found tools before
```

### Phase 2: GRASPING
```
LLM: "arm_move(position='PREGRASP')"
  → IK solver computes 6 joint angles
  → Safety checks joint limits
  → Sends to embedded interface
LLM: "arm_move(position='GRASP_POINT')"
  → Moves to exact tool position
LLM: "gripper_close(force=NORMAL)"
  → Closes gripper with 1.0N force
  → Checks force feedback for slip detection
```

### Phase 3: HANDOVER
```
LLM: "arm_move(position='PRESENTATION')"
  → Arm moves to handover position
LLM: "hand_detect()"
  → MediaPipe detects hand in frame
  → Checks hand is in valid zone (x:0.1-0.65, y:<0.4, z>0)
LLM: "gripper_open()"
  → Releases tool into surgeon's hand
```

---

## Safety Gates (L0-L6) — Checked Before EVERY Tool Call

```
L0: ESTOP check           — Is emergency stop active?
L1: Tool Gate             — Is this tool valid?
L2: Workspace bounds      — Is target within reachable area?
L3: Joint limits          — Are all joint angles feasible?
L4: Consecutive failures  — Have we failed 3+ times?
L5: LLM budget            — Have we made 20+ LLM calls?
L6: Gripper force anomaly — Is force > 50N?
```

**All 7 must pass GREEN** before any tool executes. If red, the action is rejected with a specific error.

---

## Circuit Breaker (added June 14)

```
API calls succeed → normal operation
3 consecutive failures → circuit OPENS
  → All LLM calls skipped for 60s
  → Falls directly to deterministic logic
60s passes → circuit CLOSES
  → LLM calls attempted again
Any success → reset counter
```

Prevents hammering dead APIs. The robot degrades gracefully instead of hanging.

---

## Adaptive Deadline (added June 14)

Instead of a fixed 120s timeout:
- **SEARCH phase:** (remaining zones × 60s) + (4 arm moves × 30s) + 30s buffer
- **GRASP phase:** 3 arm moves × 30s + 30s buffer  
- **HANDOVER phase:** 1 arm move × 30s + 30s buffer
- **Minimum:** 180s regardless
- **Configurable:** via `planner.task_timeout_s` in system.yaml

---

## Sequence Counter for Motion Safety (added June 14)

```
Before each arm_move:
  self._motion_seq += 1
  
When feedback arrives:
  stamp with current seq number
  if seq != expected: discard (stale result)
  
If ESTOP unblock sent:
  retry until queue accepts
  never silently drop
```

Prevents a known race: previous motion's feedback arriving after new motion starts → false success/failure.

---

## Complete Data Flow

```
Mic → VAD → Deepgram ASR → "fetch scissors"
  → Groq Intent Parser → {tool: scissors, confidence: 0.94}
    → Auth validates → ValidatedIntent
      → Planner.AgenticPlanner.run_task(intent)
        → [LOOP START]
          → LLM decides: vision_scan(zone='A')
            → Safety kernel L0-L6 check
              → ToolKernel.vision_scan()
                → YOLO inference
                  → Result: found at (0.45, 0, 0.05)
                    → LLM decides: arm_move(GRASP_POINT)
                      → IK solver → 6 joint angles
                        → ToolKernel.arm_move()
                          → embedded_interface
                            → SPI → Teensy → motors
        → [LOOP END when HANDOVER complete]
```


The agentic layer was the most bug-dense part of the codebase — 14 race conditions were fixed in the planner, tool kernel, and safety kernel alone. Every fix was about making the robot safe even when APIs fail, threads race, or sensors return garbage.

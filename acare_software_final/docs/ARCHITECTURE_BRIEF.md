# ACARE — Software Architecture Brief

## System Overview
ACARE is a voice-controlled surgical assistant robot. 11 ROS2 packages, ~18,000 lines of Python. The entire software stack is complete and demo-ready.

---

## Agentic & AI Layer (the brain)

### 1. Voice Pipeline — Speech → Intent
```
Mic → Silero VAD (speech detection) → Deepgram Nova-2 (ASR) → 
Normaliser + Alias Expansion → Groq 8B (intent parsing) → 
Fast Intent (regex fallback, <200ms) → Validated Intent
```
- **VAD:** 32ms chunks, 16kHz, detects speech within 200ms
- **ASR:** Deepgram streaming, Nova-2 model, 340ms typical latency
- **Intent parser:** Groq Llama 3.3-8B, returns JSON `{tool, action, confidence}`
- **Fast intent:** Regex bypass for unambiguous commands (no LLM call needed)
- **Alias expansion:** 30+ medical aliases → canonical tool names (e.g. "tube" → "cream")
- **Mic fix:** PCM2902 USB mic at 44100Hz → software resampled to 16kHz

### 2. Agentic Planner — Task Execution
```
Validated Intent → NIM Nemotron-49B (primary) → Groq 70B (fallback) → 
Deterministic (last resort) → ToolKernel execution → IK → Arm command
```
- **Triple LLM fallback:** NIM (Nvidia, 0.5s) → Groq (Cloud, 1s) → Deterministic (always works)
- **Circuit breaker:** After 3 consecutive API failures, skip LLM for 60s
- **Adaptive deadline:** Dynamic task timeout (min 180s), calculated per phase
- **Phases:** SEARCH → GRASPING → HANDOVER → DONE, with agentic recovery at each step
- **Safety kernel (L0-L6):** Every tool call checked against ESTOP, workspace bounds, joint limits, failure counters, LLM budget, gripper force

### 3. Dialogue Manager — Conversation
- **Multi-turn context:** Tracks last intent, pending clarifications, tool history
- **Clarification:** Low confidence (<0.6) → re-prompt; medium (<0.8) → confirm
- **Multi-tool:** "scissors and forceps" → asks "which first?"
- **Assistant agent:** Groq 70B for pre-login conversation (chit-chat, guidance, redirect)

### 4. Authentication — Biometric Gate
- **Passive face scan:** MediaPipe, 0.5s timer, auto-detects approaching person
- **Face verification:** InsightFace buffalo_sc, 512-D embedding, cosine >0.78
- **Voice verification:** ECAPA-TDNN ONNX, 192-D embedding, cosine >0.85
- **Voice drift:** 3 consecutive failed checks → force re-authentication

---

## Perception Layer (vision)

### 5. Vision Pipeline
```
Camera → YOLO26 ONNX (NMS-free, 6 classes) → 
NBV search (Bayesian probability map) → 3D localization → Robot frame transform
```
- **YOLO26:** 320×320 input (config says 640), 6 classes (cream, scissors, forceps, thermometer, oximeter, plaster), ~850ms on Pi 5 CPU
- **Low-light enhancement:** CLAHE + Gamma correction + HSV profiling. Fallback when V_mean < 75 (threshold: max(0.50, conf-0.12))
- **Motion blur rejection:** Laplacian variance < 100 → skip frame
- **NBV:** Next-Best-View search across 3 zones (A/B/C). Bayesian probability map: 3 zones × 8 tools = 24 entries, clamped [0.05, 0.90]
- **Coordinates:** FK-based compute_T_for_viewpoint → pixel_to_robot → arm frame

### 6. Hand Tracking (MediaPipe)
- **Handover phase:** Detects and tracks surgeon's hand for tool delivery
- **Bounds check:** 0.10 < x < 0.65, |y| < 0.40, z > 0.0
- Mutual exclusion with YOLO to save CPU on Pi 5

---

## Infrastructure Layer

### 7. ROS2 Nodes (11 packages)
| Node | Function |
|------|----------|
| `safety_node` | LiDAR zones (400mm/600mm), current (8A), temp (75°C) |
| `state_manager` | 10-state FSM from OFFLINE to HANDOVER |
| `auth_node` | Face + voice biometric gate |
| `voice_node` | VAD→ASR→intent→TTS orchestration |
| `dialogue_node` | ROS2 wrapper for dialogue |
| `planner_node` | Task orchestration with agentic recovery |
| `vision_node` | YOLO + NBV + hand tracking |
| `embedded_interface` | SPI bridge to Teensy firmware |
| `supervisor_node` | Crash recovery, 5s polling, healthcheck service |
| `log_node` | SQLite audit trail, 200MB auto-rotate |
| `admin_node` | CLI enrolment, calibration |

### 8. Safety Architecture
- **L0-L6 gates:** Every tool execution checked against 6 safety layers
- **Dual ESTOP path:** Both `/safety_alert` and `/emergency_stop` topics
- **Hardware latch:** Teensy SPI watchdog at 200ms timeout
- **ESTOP->state machine:** Supervisor ESTOP now routes through state_manager (fixed June 14)

### 9. Concurrency Model
- **MultiThreadedExecutor** (4 threads) for planner, vision, auth
- **MutuallyExclusiveCallbackGroup** for subscriptions (prevents races)
- **ReentrantCallbackGroup** for timer (allows blocking on Event.wait)
- **Sequence counter** on arm commands to reject stale motion feedback
- **11 race conditions fixed** in June 14-15 audit (intent overwrite, queue drain, pending_login, etc.)

---

## Key Stats
- **Lines of code:** ~15,000 Python + 764 C++ firmware
- **Bugs found/fixed:** 119 found, 108 fixed (11 hardware/firmware remaining)
- **Files modified:** 22 across recent fix passes
- **API dependencies:** Deepgram (STT), Groq (intent + dialogue), Nvidia NIM (planning)
- **Demo readiness:** Software complete. Hardware needs SPI wiring + Teensy flash + 24V power.

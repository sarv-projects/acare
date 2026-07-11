# ACARE — Complete Project Documentation

**Autonomous Clinical Assistance Robot with Multimodal Biometric Authentication and Dynamic Human Handover**

**Version:** 1.0 | **Status:** Final

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Hardware Specifications](#3-hardware-specifications)
4. [Embedded Firmware (Teensy 4.1)](#4-embedded-firmware-teensy-41)
5. [Software Package Reference](#5-software-package-reference)
6. [ROS2 Communication Architecture](#6-ros2-communication-architecture)
7. [State Machine & Planner Architecture](#7-state-machine--planner-architecture)
8. [Vision Pipeline](#8-vision-pipeline)
9. [Voice Pipeline](#9-voice-pipeline)
10. [Authentication & Biometrics](#10-authentication--biometrics)
11. [Safety Architecture](#11-safety-architecture)
12. [Configuration Reference](#12-configuration-reference)
13. [SPI Communication Protocol](#13-spi-communication-protocol)
14. [Performance Specifications](#14-performance-specifications)
15. [Calibration & Deployment](#15-calibration--deployment)
16. [Pending Work & Future Scope](#16-pending-work--future-scope)

---

## 1. Project Overview

### 1.1 Institutional Details

| Field | Details |
|---|---|
| Institution | Ramaiah Institute of Technology, Bengaluru |
| Department | Electronics and Communication Engineering |
| Guide | Dr. Lakshmi Shrinivasan, Associate Professor |
| Team | Sathvik Rao, Sarvesh Bhattacharyya, Shreevanth M, Shreyas S |
| Funding | ₹40,000 — Institutional Grant |
| License | Apache License 2.0 |

### 1.2 Problem Statement

ACARE addresses the following challenges in Indian clinical environments:

- Staff fatigue from repetitive tool retrieval during 10-12 hour surgical shifts
- Hygiene risks from manual handling of sterile instruments
- Procedure delays caused by instrument unavailability or incorrect delivery
- Absence of affordable autonomous assistance solutions in Indian healthcare settings

### 1.3 Solution Overview

ACARE is a stationary 6-DOF semi-autonomous robotic arm designed for clinical environments. It performs voice-commanded, biometrically authenticated, autonomous pick-and-place operations with human oversight. The system integrates:

- **Voice-driven control** — natural language command parsing via LLMs
- **Dual biometric authentication** — face + voice verification for every session
- **Autonomous vision search** — Bayesian Next-Best-View with YOLO object detection
- **Dynamic handover** — 3-gate protocol (face + palm + voice confirmation)
- **Layered safety architecture** — independent software and firmware ESTOP paths

### 1.4 Scope

- Stationary pick-and-place operation only (no navigation)
- Contactless operation — entirely voice commanded
- Dual biometric authentication — voice and face combined for every session
- Single active user session at any time
- Single tool per command (multi-tool requests trigger clarification)
- Next-Best-View intelligent search (not continuous scanning)
- Direct handover — tool delivered from gripper into staff's hand

### 1.5 Key Differentiators

| Feature | ACARE | Prior Art |
|---|---|---|
| Multimodal biometric auth (voice + face) | Required for every command | Rare or absent |
| Voice-driven retrieval with structured intent parsing | Groq/NIM LLM extraction | GUI or manual control |
| Agentic LLM task planner with triple fallback | NIM → Groq → deterministic | Hardcoded state machines |
| Bayesian probabilistic vision search | Persistent probability map, NBV | Exhaustive scanning |
| Dynamic handover with palm tracking | 3-gate protocol | Fixed handover positions |
| Dual-layer ESTOP (software + firmware) | Independent paths | Single-layer safety |
| Analytical IK solver | Deterministic, 0.0000m round-trip | Numerical/optimisation-based |
| Wrist-mounted RGBD camera with dynamic FK | Per-pose camera transform | Fixed table-mounted cameras |
| Sub-200ms ESTOP keyword detection | Dedicated thread, 100ms debounce | Integrated into main loop |

---

## 2. System Architecture

ACARE employs a two-layer hierarchical architecture:

```
┌─────────────────────────────────────────────────────────────┐
│              SOFTWARE LAYER (Raspberry Pi 5)                  │
│  ROS2 Jazzy + Python 3.12 — All AI, planning, orchestration   │
│                                                                │
│  Voice Pipeline  →  Dialogue  →  Auth  →  Planner  →  Vision  │
│       │               │           │         │          │       │
│       └─────── Safety ─────── Logging ──── Admin ──────┘       │
│                                                                │
│  embedded_interface_node.py — ONLY point of contact            │
└──────────────────────────┬─────────────────────────────────────┘
                           │ SPI 10 MHz / Gazebo
┌──────────────────────────▼─────────────────────────────────────┐
│              EMBEDDED LAYER (Teensy 4.1 Cortex-M7)              │
│  200 Hz PID control, safety ISRs, SPI slave, watchdog           │
└─────────────────────────────────────────────────────────────────┘
```

### 2.1 Technology Stack

| Component | Technology |
|---|---|
| High-Level Compute | Raspberry Pi 5 (8GB), Ubuntu 24.04 LTS |
| Real-Time Compute | Teensy 4.1 (Cortex-M7, 600 MHz) |
| Robotics Framework | ROS2 Jazzy Jalisco |
| Computer Vision | YOLO26 ONNX, OpenCV, MediaPipe |
| Facial Recognition | InsightFace buffalo_sc |
| Speaker Verification | SpeechBrain ECAPA-TDNN ONNX |
| Task Planning | NVIDIA NIM Nemotron-49B / Groq Llama 70B |
| Speech-to-Text | Deepgram Nova-2 (streaming) |
| Text-to-Speech | Edge TTS / Kokoro ONNX / pyttsx3 |
| Voice Activity Detection | Silero VAD |
| Communication Bus | SPI 10 MHz (Pi ↔ Teensy), Modbus ASCII (Teensy ↔ RMCS-3002) |

### 2.2 External Dependencies

| Service | Purpose | Fallback |
|---|---|---|
| Deepgram Nova-2 | Streaming speech-to-text | None (pipeline dead without it) |
| Groq API | Intent parsing + fallback planner | Deterministic hardcoded logic |
| NVIDIA NIM | Agentic planner (primary) | Groq 70B → deterministic |
| Microsoft Edge TTS | Speech synthesis | Kokoro ONNX → pyttsx3 |

---

## 3. Hardware Specifications

### 3.1 Component Inventory

| Component | Specification |
|---|---|
| **Arm** | 6-DOF serial manipulator (PETG + Aluminium) |
| **Links** | 352 mm (base) + 400 mm (upper arm) + 400 mm (forearm) + 236 mm (wrist+TCP) |
| **Motors** | BLDC with RMCS-3002 drivers (6× dedicated UARTs) |
| **Encoders** | AS5600 magnetic (12-bit, I2C via TCA9548A mux) |
| **Vision Camera** | YDLIDAR HP60C RGBD (640×480, 12.4 Hz, wrist-mounted) |
| **Safety LiDAR** | YDLIDAR T-mini Plus 2D (proximity zones) |
| **Audio** | USB sound card + active speaker + microphone |
| **Gripper** | Parallel-jaw with rubber pads, linear-actuator driven, FSR force sensing |
| **Power** | 24V motor rail (dedicated), 5V logic rail, hardware ESTOP cutoff |
| **Communication** | SPI bus (10 MHz, 64-byte frames, full-duplex) |

### 3.2 Joint Configuration

| Joint | Name | Range (deg) | Range (rad) | Gearbox |
|---|---|---|---|---|
| J1 | Base | ±180 | ±3.14 | — |
| J2 | Shoulder | ±135 | ±2.36 | 22:1 |
| J3 | Elbow | ±120 | ±2.09 | 15:1 |
| J4 | Wrist Roll | ±180 | ±3.14 | TBD |
| J5 | Wrist Pitch | ±180 | ±3.14 | TBD |
| J6 | Wrist Yaw | ±180 | ±3.14 | TBD |

### 3.3 Sensor Inventory

- **RGBD Camera**: YDLIDAR HP60C (640×480 RGB @ 12.4 Hz, 640×480 depth @ 12.4 Hz)
- **Proximity LiDAR**: YDLIDAR T-mini Plus (torso-level 2D scan, 50 Hz)
- **Joint Encoders**: AS5600 magnetic encoders (×6, I2C via TCA9548A)
- **Current Sensing**: Shunt resistors on motor driver boards
- **Thermal Sensors**: Thermistors in joint motor housings
- **Force Sensor**: Analog FSR at gripper fingertips
- **IMU**: Onboard accelerometer/gyroscope for base orientation
- **Audio**: Cardioid mic (USB sound card) + active speaker

---

## 4. Embedded Firmware (Teensy 4.1)

### 4.1 Firmware File Reference

| File | Location | Description |
|---|---|---|
| `main_teensy_firmware.ino` | `embedded/firmware/` | Primary firmware — SPI slave, 200 Hz PID, 6× UART for RMCS-3002 |
| `rmcs3002_modbus_3motor.ino` | `embedded/firmware/` | 3-motor Modbus ASCII open-loop controller (reference) |
| `rmcs3002_pwm_test.ino` | `embedded/firmware/` | Legacy RMCS-3002 PWM open-loop test |
| `phase1_pi5_spi_master.py` | `embedded/firmware/` | Early SPI master test script (Pi 5 side) |
| `phase1_teensy_spi_slave.ino` | `embedded/firmware/` | Early SPI slave test (Teensy side) |

### 4.2 Control Loop Architecture

| Loop | Frequency | Purpose |
|---|---|---|
| PID Position/Velocity Control | 200 Hz | Joint servo control for all 6 DOF |
| Sensor Polling | 100 Hz | AS5600 encoders, current shunts, thermistors |
| Telemetry Publishing | 50 Hz | Joint state streaming to Pi via SPI |
| Watchdog Heartbeat | 5 Hz | SPI keepalive; triggers ESTOP after 500 ms silence |

### 4.3 Embedded FSM States

| State | Description |
|---|---|
| IDLE | Powered, holding position |
| POSITION_CONTROL | Executing joint trajectory commands |
| GRIPPER_CONTROL | Gripper in force-control mode |
| ESTOP | PWM disabled, brakes engaged |
| FAULT | Hardware threshold exceeded (latched) |
| CALIBRATION | Homing routine in progress |

### 4.4 Hardware Fault Protections

| Condition | Threshold | Action | Fault Code |
|---|---|---|---|
| Joint overcurrent | > 8 A for > 100 ms | PWM cutoff | 1 |
| Joint overtemperature | > 75 °C | ESTOP shutdown | 2 |
| Encoder soft limit breach | Mechanical limit | Motion halt | 3 |
| Joint velocity exceedance | > 120 °/s | Motion halt | 4 |
| Gripper force exceedance | > 15 N | Gripper release | 5 |
| SPI watchdog timeout | > 500 ms | ESTOP | 6 |

### 4.5 Encoder Interface

- AS5600 I2C at 400 kHz via TCA9548A multiplexer
- Angle: `raw_count / 4096 × 2π` radians
- Exponential moving average filter: `filtered = 0.7 × raw + 0.3 × prev`
- Zero offsets stored in EEPROM during homing

---

## 5. Software Package Reference

### 5.1 Package Inventory

| Package | Type | Purpose | Files |
|---|---|---|---|
| `acare_msgs` | CMake | 18 message + 1 service definitions | 22 |
| `acare_bringup` | Python | Config, launch, paths, QoS, supervisor | 13 |
| `acare_voice` | Python | Voice pipeline (VAD → ASR → intent → TTS) | 30 |
| `acare_dialogue` | Python | ROS2 dialogue node, transcript processing | 6 |
| `acare_auth` | Python | Face + voice biometric authentication | 10 |
| `acare_planner` | Python | FSM, agentic planner, IK solver, safety kernel | 17 |
| `acare_vision` | Python | YOLO, NBV search, 3D localisation, hand tracking | 13 |
| `acare_safety` | Python | LiDAR proximity + MCU telemetry monitoring | 6 |
| `acare_logging` | Python | SQLite audit trail with auto-rotation | 6 |
| `acare_embedded_interface` | Python | Gazebo/SPI hardware bridge | 6 |
| `acare_admin` | Python | Staff management, calibration, CLI | 7 |

### 5.2 acare_msgs — Message & Service Definitions

**Type:** CMake package
**Messages (18):**

| Message | Fields | Purpose |
|---|---|---|
| `ArmCommand.msg` | command, joint_angles[6], velocity_scale, accel_limit, blocking | Joint-level arm motion command |
| `AuthRequest.msg` | request_type, modality, timeout_s, tool, confidence | Auth request from dialogue to auth node |
| `AuthResult.msg` | user_id, name, role, success, face_verified, face_confidence, voice_confidence | Auth result broadcast |
| `EmergencySignal.msg` | reason, source | ESTOP signal — highest priority |
| `GripperCommand.msg` | command (GRASP/RELEASE), force_target | Gripper command |
| `HandStatus.msg` | hand_detected, is_open, palm_up, hand_approaching, x, y, z, confidence | Hand detection for handover |
| `Intent.msg` | tool, action, destination, confidence | Parsed intent from dialogue |
| `LogEvent.msg` | event_type, user_id, tool, state, description, timestamp, latency fields | Audit log entry |
| `MotionFeedback.msg` | success, phase, error, joint_positions[], joint_velocities[], joint_currents[], temperatures[], gripper_force, imu | Motion feedback from embedded |
| `ProbabilityUpdate.msg` | zone, tool, new_probability | Bayesian map update |
| `RobotState.msg` | state, active_user_id | FSM state broadcast |
| `SafetyAlert.msg` | severity (WARNING/CRITICAL/ESTOP), reason, source | Safety alert |
| `StateTransition.msg` | target_state, reason | State transition request |
| `Transcript.msg` | text, is_final, pcm16, sample_rate_hz | ASR transcript with audio |
| `ValidatedIntent.msg` | tool, action, user_id, name, authenticated | Auth-verified intent |
| `VisionResult.msg` | found, tool, x, y, z, confidence, zone, candidates_json[] | Detection + 3D localisation |
| `VisionSearchRequest.msg` | tool, reset_probability_map, priority_zones[] | Vision search command |
| `VisionStatus.msg` | status (LOADING/READY/ERROR/SEARCHING) | Vision pipeline state |

**Services (1):**
| Service | Request | Response |
|---|---|---|
| `EnrolStaff.srv` | name, role | success, staff_id, message |

### 5.3 acare_bringup — Shared Infrastructure

**`paths.py`** — Centralised path constants: `REPO_ROOT`, `CONFIG_DIR`, `SYSTEM_YAML`, `THRESHOLDS_YAML`, `PROBABILITY_MAP_YAML`, `USERS_DB`, `MODEL_DIR`

**`qos_profiles.py`** — Per-topic QoS profiles:
- `TOPIC_SENSOR` — BEST_EFFORT depth=1 (motion feedback, LiDAR)
- `TOPIC_COMMAND` — RELIABLE depth=10 (arm/gripper/emergency commands)
- `TOPIC_STATE` — RELIABLE + TRANSIENT_LOCAL depth=1 (robot state, safety alerts)
- `TOPIC_LOGGING` — BEST_EFFORT depth=10 (log events)
- `TOPIC_VISION` — RELIABLE depth=10 (vision results, requests)
- `TOPIC_VOICE_PIPELINE` — RELIABLE depth=10 (transcripts, intents, auth)
- `TOPIC_TTS` — RELIABLE depth=10 (TTS requests)
- `TOPIC_ESTOP` — RELIABLE depth=10 (emergency stop signals)

**`supervisor_node.py`** — ROS2 node for crash recovery:
- Monitors all 11 nodes every 5s via ROS2 graph API
- Auto-restarts: log_node, admin_node, dialogue_node, voice_node, auth_node
- Critical nodes (no restart — triggers ESTOP): safety_node, embedded_interface_node, state_manager, planner_node, vision_node
- Power recovery: reads last state from SQLite on boot; performs safe deposit if last state was EXECUTING/HOLDING/HANDOVER

**`constants.py`** — Shared constants: ESTOP keywords, recovery keywords, confirm/reject words, voice names

**`launch/acare.launch.py`** — Staggered launch for all 11 ROS2 nodes:
1. log_node (0s)
2. safety_node (1s)
3. voice_node (2s)
4. dialogue_node (4s)
5. state_manager (5s)
6. auth_node (6s)
7. planner_node (8s)
8. embedded_interface_node (9s)
9. vision_node (10s)
10. admin_node (12s)
11. supervisor_node (13s)

**Config files:**
- `config/system.yaml` — Main system configuration (147 lines)
- `config/thresholds.yaml` — Safety thresholds (18 lines)
- `config/probability_map.yaml` — Bayesian priors for 6 tools × 3 zones (30 lines)

### 5.4 acare_voice — Voice Pipeline

**Type:** Python package | **Files:** 30

| File | Key Classes/Functions | Lines | Purpose |
|---|---|---|---|
| `voice_node.py` | `VoiceNode` | 471 | Standalone orchestrator: state machine, pipeline coordination |
| `voice_ros_node.py` | `VoiceNodeROS` | 225 | ROS2 bridge — subscribes ROS topics, drives standalone pipeline |
| `vad.py` | `VADListener` | 189 | Silero VAD, 32ms chunks, 0.5s min speech, 0.8s silence flush |
| `asr.py` | `ASRClient` | 272 | Deepgram Nova-2 streaming WebSocket with reconnect logic |
| `keyword_monitor.py` | `KeywordMonitor` | 135 | Dedicated ESTOP thread, 100ms debounce, continuation-word cancellation |
| `tts.py` | `speak()`, `speak_urgent()` | 119 | Dual TTS: edge-tts normal, pyttsx3 urgent |
| `tts_queue.py` | `TTSQueue` | 309 | Priority queue with barge-in, echo avoidance, 3-tier fallback |
| `intent_parser.py` | `parse_intent()` | 75 | Groq Llama 3.1 8B intent extraction → structured JSON |
| `fast_intent.py` | `parse_fast_intent()` | 168 | Regex-based intent for ESTOP/confirm/cancel/commands (bypasses LLM) |
| `normaliser.py` | `normalise()` | 161 | Text cleaning, filler removal, multi-tool detection |
| `alias_expansion.py` | `expand_aliases()` | 243 | Alias → canonical tool mapping with word-boundary regex |
| `assistant_agent.py` | `AssistantAgent` | 284 | Groq 70B conversational agent for LOGGED_OUT assistant mode |
| `dialogue_manager.py` | `DialogueManager` | 171 | Multi-turn state, confirmation handling, follow-up resolution |
| `earcons.py` | `play_*()` | 90 | Audio cues: listen_start, turn_ready, confirm, barge-in, ESTOP |
| `state_manager.py` | `StateManager` | 223 | Standalone voice FSM (standalone mode, not ROS2) |
| `conversation_eval.py` | — | 269 | Conversation quality evaluation utility |
| `main.py` | `main()` | 31 | Standalone entry point (non-ROS2 laptop testing) |

**Voice Pipeline Flow:**
1. VAD (Silero, 16 kHz, 32ms chunks) detects speech onset
2. ASR streams audio to Deepgram Nova-2 (endpointing=300ms, utterance_end_ms=1000)
3. Normaliser cleans transcript (lowercase, filler removal, punctuation)
4. Alias expansion maps user aliases to canonical tools ("blade" → "scalpel")
5. Fast intent regex checks for ESTOP/resume/confirm/reject first (no LLM)
6. Intent parser (Groq 8B, JSON mode) extracts structured intent
7. Dialogue manager handles multi-turn: confirmation, follow-up, pronoun resolution
8. TTS queue speaks response with 3-tier fallback

**ESTOP Keyword Detection:**
- 6 keywords: `stop`, `halt`, `emergency`, `abort`, `ruko`, `bas`
- 100ms collision window debounce
- Continuation-word safety ("stop moving" ≠ ESTOP)
- Backstop detection on final transcripts (short utterances ≤ 2 words)
- Dedicated thread, < 200ms end-to-end latency

**TTS Fallback Chain:**
1. Edge TTS (`en-IN-NeerjaNeural`) — cloud, high quality
2. Kokoro ONNX INT8 — offline fallback
3. pyttsx3 — emergency fallback, always available

### 5.5 acare_dialogue — ROS2 Dialogue Node

**Type:** Python package | **Files:** 6

**`dialogue_node.py`** (223 lines):
- Subscribes: `/raw_transcript` (Transcript), `/robot_state` (RobotState), `/validated_intent` (ValidatedIntent), `/vision_result` (VisionResult)
- Publishes: `/intent_result` (Intent), `/tts_request` (String)
- Pronoun resolution — resolves "it", "that", "the same one" from context
- Session memory — tools_fetched list, conversation_history (last 20 turns)
- Clarification loop — ambiguous requests trigger user prompts
- Assistant mode — delegates to AssistantAgent when LOGGED_OUT
- Confidence gating — intents with confidence < 0.8 enter clarification loop

### 5.6 acare_auth — Biometric Authentication

**Type:** Python package | **Files:** 10

| File | Classes | Lines | Purpose |
|---|---|---|---|
| `auth_node.py` | `AuthNode`, `PendingLogin`, `PendingEnrollment` | 770 | Master auth orchestrator: login flow, voice drift, enrolment loop |
| `face_detect.py` | `PassiveFaceDetector` | 27 | MediaPipe face detection (passive scan, 0.5s timer) |
| `verify_face.py` | `FaceVerifier` | 41 | InsightFace buffalo_sc, 512-D embedding, cosine similarity ≥ 0.78 |
| `verify_voice.py` | `VoiceVerifier` | 176 | ECAPA-TDNN ONNX, 192-D embedding, cosine similarity ≥ 0.85 |
| `storage.py` | `UserStore`, `UserRecord` | 153 | SQLite database, face/voice embeddings as NPY blobs |
| `export_ecapa_onnx.py` | — | 75 | One-time ECAPA-TDNN → ONNX export script |

**Authentication Flow:**
1. **Passive face scan** (0.5s timer): MediaPipe detects face → matches enrolled users via InsightFace
2. **Login prompt**: "Welcome [name]. Say confirm to log in."
3. **Voice verification**: "confirm" utterance → ECAPA-TDNN compares embedding against stored profile
4. **Session activation**: Publishes AuthResult, transitions STANDBY, starts 2-hour hard TTL
5. **Runtime voice drift**: Every transcript verified against stored embedding; 3 consecutive failures → reconfirmation prompt
6. **Handover face check**: During HANDOVER, face similarity checked every 0.7s (advisory gate)

**Enrolment Flow (via `/enrol_staff` service):**
- Captures 10 face frames + 3 voice samples
- Normalises embeddings via mean + L2 normalisation
- Stores in SQLite with NPY serialisation
- Roles: surgeron, nurse, admin

**UserStore Schema:**
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    voice_emb BLOB, face_emb BLOB,
    registered_at INTEGER NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    handover_z_offset REAL NOT NULL DEFAULT 0.0
);
```

### 5.7 acare_planner — Task Planner & State Machine

**Type:** Python package | **Files:** 17

| File | Classes | Lines | Purpose |
|---|---|---|---|
| `planner_node.py` | `PlannerNode`, `WorldState` | 389 | Master task orchestrator: timer-based polling, multi-threaded executor |
| `agentic_planner.py` | `AgenticPlanner` | 376 | LLM agentic loop with NIM/Groq/deterministic fallback |
| `state_manager.py` | `StateManager` | 235 | 10-state global FSM with all valid transitions |
| `ik_solver.py` | `IKSolver`, `IKResult` | 348 | Analytical 6-DOF IK (geometric 2-link + spherical wrist) |
| `tool_kernel.py` | `ToolKernel` | 307 | 6-layer tool execution safety gate |
| `safety_kernel.py` | `SafetyKernel`, `RetryCounters` | 117 | Deterministic 6-layer safety validation |
| `tool_registry.py` | Constants | 131 | Canonical tool ↔ YOLO class mapping (6 tools) |
| `state_snapshot.py` | `TaskSnapshot`, `WorldState`, `TaskObjective`, `Budget`, `LastAction` | 69 | Bounded LLM context snapshot (~1500 tokens) |
| `task_memory.py` | `TaskMemory` | 70 | SQLite task outcomes + user priors |
| `hw_translator.py` | `HWTranslator` | 75 | Maps command to hardware parameters |
| `voice_sync.py` | `VoiceSyncBridge` | 66 | Voice confirmation bridge for ask_user tool |
| `agent_schema.py` | `ToolCallSchema`, `validate_agentic_decision()` | 23 | Pydantic LLM output validation |

**10-State FSM:**
```
OFFLINE → LOGGED_OUT → STANDBY → LISTENING → PROCESSING → EXECUTING → HOLDING → HANDOVER → STANDBY
```

| State | Description | Allowed Transitions |
|---|---|---|
| OFFLINE | System off / booting | LOGGED_OUT |
| LOGGED_OUT | No active user session | STANDBY |
| STANDBY | User authenticated, idle | LISTENING, PROCESSING, LOGGED_OUT |
| LISTENING | Voice pipeline active | PROCESSING, STANDBY |
| PROCESSING | Task execution | EXECUTING, STANDBY |
| EXECUTING | Arm moving to grasp | HOLDING, ESTOP |
| HOLDING | Tool grasped, moving | HANDOVER, ESTOP |
| HANDOVER | Handover protocol | STANDBY, ESTOP |
| ESTOP | Emergency stop (any state) | STANDBY |
| ERROR | Irrecoverable fault | OFFLINE |

**Key properties:**
- ESTOP reachable from ANY state (safety override)
- Logout guard: rejected from EXECUTING, HOLDING, HANDOVER
- Inactivity timeout: 5 minutes in STANDBY → auto-logout
- Hard TTL: 2 hours from login

**Agentic Planner Details:**
- Primary: NVIDIA NIM `llama-3.3-nemotron-super-49b-v1`
- Fallback: Groq `llama-3.3-70b-versatile`
- Deterministic: Hardcoded logic (zero LLM dependency)
- 11 tools: vision_scan, arm_move, arm_approach, gripper_close, gripper_open, detect_face, detect_hand, speak, ask_user, complete_task, abort_task
- Bounded context: action history capped at 3 entries, failed actions compressed
- Circuit breaker: 3+ consecutive API failures → skip LLM for 60s
- Degradation logging: publishes LLM_FALLBACK or LLM_CIRCUIT_OPEN LogEvents

**Safety Kernel (6-Layer Gate):**
| Layer | Check | Action |
|---|---|---|
| L1 | ESTOP active | Reject all non-abort actions |
| L2 | Workspace bounds | Reject outside x/y ±0.60m, z 0.0-0.75m |
| L3 | Joint limits / IK reachability | Reject unreachable targets |
| L4 | Consecutive failures | Abort after 3 failures |
| L5 | LLM call budget | Abort when 20 calls exhausted |
| L6 | Gripper force anomaly | Reject GRASP if force > 50N |

**Analytical IK Solver:**
- Geometry: base 0.352m, upper_arm 0.400m, forearm 0.400m, wrist+tool 0.236m
- J1: base rotation via atan2(y, x)
- J2/J3: planar 2-link IK via law of cosines (elbow-up configuration)
- J4/J5/J6: wrist orientation for top-down grasp
- Joint limit clamping with reachable flag — never raises
- FK self-test: verified to 0.0000m round-trip error

**Tool Registry (6 canonical tools):**
| Canonical | YOLO Class | Example Aliases |
|---|---|---|
| cream | cream | lotion, ointment, topical |
| scissors | medical scissors | cutting tool, snips |
| forceps | surgical forceps | tweezers, clamps, graspers |
| thermometer | thermometer | temp probe |
| oximeter | oxymeter | pulse ox, spo2 |
| plaster | plaster | bandaid, adhesive strip |

### 5.8 acare_vision — Perception Pipeline

**Type:** Python package | **Files:** 13

| File | Classes | Lines | Purpose |
|---|---|---|---|
| `vision_node.py` | `VisionNode` | 622 | Orchestrator: mode switching (IDLE/SEARCH/HANDOVER), camera health monitor |
| `yolo_infer.py` | `YOLO26ONNX` | 433 | YOLO26 NMS-free ONNX inference with low-light enhancement |
| `nbv_search.py` | `NBVSearch` | 589 | Bayesian NBV search, 3 zones, wrist micro-offsets, temporal consistency |
| `localiser.py` | `Localiser` | 272 | Pinhole back-projection, wrist-mounted camera FK |
| `hand_tracker.py` | `HandTracker` | 216 | MediaPipe Hands for handover (palm detection, 3D position) |
| `fake_detector.py` | `FakeDetector` | 138 | Dual-signal fake rejection (Laplacian + depth variance) |
| `hp60c_camera_node.py` | `HP60CCameraNode` | 154 | Camera frame cache from ascamera topics |
| `camera_probe.py` | — | 80 | Camera diagnostics and parameter probing |

**VisionNode Modes:**
- IDLE — no active task
- SEARCH — NBV search running, YOLO active, HandTracker stopped
- HANDOVER — HandTracker active, YOLO not called
- YOLO and MediaPipe Hands NEVER run simultaneously

**YOLO Inference (acare_v26.onnx):**
- Input: 320×320 RGB, output: [1, 300, 6] NMS-free format
- 6 classes: cream, medical scissors, oxymeter, plaster, surgical forceps, thermometer
- ONNX Runtime with CPUExecutionProvider, 4 intra-op threads
- Scene-adaptive: HSV V-channel analysis, gamma correction (1.55/1.85), CLAHE, unsharp mask
- Confidence thresholds: normal=0.70, low-light=0.56
- Multi-frame IoU deduplication (threshold 0.5)
- Blur rejection: Laplacian variance < 100 → skip frame

**NBV Search:**
- 3 zones (A=left, B=centre, C=right) defined by calibrated viewpoints
- Wrist micro-offsets: ±0.035 rad J5, ±0.025 rad J6 for 3-frame capture
- Per-viewpoint dynamic camera transform via `compute_T_for_viewpoint()`
- Bayesian map update: found → ×1.5, not found → ×0.7, passive seen → ×1.3
- Normalise → clamp [0.05, 0.90]
- Temporal consistency: object within 50px in previous viewpoint → promoted at 0.65 confidence

**3D Localisation:**
- Pinhole camera: X = (u - cx) × Z / fx, Y = (v - cy) × Z / fy
- HP60C intrinsics: fx=572.04, fy=571.49, cx=329.27, cy=242.09 (auto-updated from /camera_info)
- Median-of-window fallback (40×40) for sparse depth pixels
- Wrist-mounted camera transform: `T_robot_camera = T_robot_flange(FK) × T_flange_camera`
- `T_flange_camera`: fixed 4×4 offset (default 40mm forward, 20mm below flange)

**Hand Tracking:**
- MediaPipe Hands: max 1 hand, detection confidence ≥ 0.70, tracking confidence ≥ 0.60
- Open palm: 3+ fingers extended (tip y < PIP y)
- Palm centre: average of WRIST + 4 MCP landmarks
- Wrist-mounted camera support via `set_viewpoint_joints()` + `T_override`

### 5.9 acare_safety — Safety Monitoring

**Type:** Python package | **Files:** 6

**`safety_node.py`** (320 lines):
- **LiDAR proximity** (YDLIDAR T-mini Plus, `/scan`):
  - Front arc = middle third of scan (±60° from forward)
  - > 600mm: SAFE | 400-600mm: WARNING | < 400mm: ESTOP
- **MCU telemetry** (`/motion_feedback`):
  - 6 joint currents: ESTOP > 8.0A, WARNING > 6.0A
  - 6 joint temperatures: ESTOP > 75°C, CRITICAL > 65°C, WARNING > 55°C
  - Gripper force: ESTOP > 15N, WARNING > 10N
- Alert throttling: WARNING/CRITICAL at 1/sec per (severity, source) pair
- ESTOP is NEVER throttled — every ESTOP published immediately
- Redundant ESTOP via `/emergency_stop` publisher
- Recovery check: 2s periodic timer, clears after 5s of no active conditions
- Self-test: 30s timer verifies `/emergency_stop` has subscribers

### 5.10 acare_logging — Audit Trail

**Type:** Python package | **Files:** 6

**`log_node.py`** (171 lines):
- Subscribes `/log_event` (BEST_EFFORT QoS)
- SQLite database at `logs/acare_logs.db`
- Batched writes: 10-event batch, 5s periodic flush
- Thread-safe: SQLite lock serialises access
- Auto-rotation at 200 MB: oldest 20% archived to gzipped CSV
- Schema: event_id, timestamp, staff_id, event_type, tool, state, description, safety_severity, latency fields

### 5.11 acare_embedded_interface — Hardware Bridge

**Type:** Python package | **Files:** 6

**`embedded_interface_node.py`** (511 lines):
- ONLY point of contact between ROS2 software and hardware
- Subscribes: `/arm_command`, `/gripper_command`, `/emergency_stop`, `/robot_state`
- Publishes: `/motion_feedback` after every command

**Simulation path (active):**
- Action clients to Gazebo controllers: `/arm_controller/follow_joint_trajectory`, `/gripper_controller/follow_joint_trajectory`
- Async goal sending (non-blocking — critical for ESTOP responsiveness)
- Joint trajectory goals with velocity-scaled duration (default 2.5s arm, 0.7s gripper)

**Guards:**
- LOGGED_OUT arm guard: only kiosk poses at reduced velocity/accel
- LOGGED_OUT gripper guard: GRASP/CLOSE rejected
- ESTOP hard latch: all goals rejected while active; cleared via `/clear_estop` service
- MOVE_REL rejection: only absolute MOVE supported
- Joint limit validation before sending commands

**Hardware path (SPI):**
- Mode selected via `system.yaml interface.mode: "hardware"`
- Pi 5 as SPI Master via `/dev/spidev0.0`
- Teensy 4.1 as SPI Slave, DMA double-buffered
- Attention line (ATTN) for sub-millisecond hardware fault signalling

### 5.12 acare_admin — Administration CLI

**Type:** Python package | **Files:** 7

**`admin_cli.py`** (323 lines):

| Command | Description |
|---|---|
| `enrol --name --role` | Triggers biometric enrolment via ROS2 service |
| `revoke --id` | Marks staff member inactive |
| `list-staff` | Lists all enrolled staff |
| `set-api-key --service --key` | Stores encrypted API key |
| `set-threshold --sensor --value` | Updates safety thresholds |
| `show-logs --last` | Recent log events from SQLite |
| `export-logs` | All log events to CSV |
| `status` | ROS2 node list + Pi health |
| `calibrate` | 7-step calibration procedure |
| `demo-mode --enable/--disable` | Toggle demo mode |

**`admin_node.py`** (24 lines) — Minimal ROS2 node with 30s heartbeat timer

### 5.13 Supporting Files

**`sim_files/`** — Gazebo simulation launch helpers (12 files):
- `acare_sim.launch.py` — Full simulation launch
- `gz_bridge.yaml` — Gazebo-ROS bridge topic config
- `gz_ros2_control.xacro` — Gazebo ros2_control plugin
- `launch_full_sim.sh`, `setup_full_sim.sh` — Sim setup and launch scripts
- `test_detect.py`, `test_localise.py`, `test_vr_module.py` — Standalone test scripts
- `check_depth.py`, `update_intrinsics.py` — Camera utilities

**`scripts/`** — Build, deployment, and validation helpers (11 files):
- `build_workspace.sh` — Colcon build
- `launch_validate.sh` — Post-launch validation
- `validate_ros_graph.py` — ROS graph topology verification
- `preflight_ros_env.py` — Environment pre-check
- `acare_gazebo_demo.sh` — Gazebo demo script
- `acare_mock_demo.sh` — MoveIt2 mock demo script
- `demo_dashboard.py` — FastAPI dashboard (852 lines)
- `setup_pi_kiosk.sh` — Pi kiosk mode setup
- `install_ros2.sh`, `setup_sudo.sh` — Pi setup scripts

**`camera_configs/`** — HP60C encrypted configuration files

**`models/`** — Trained ML models:
- `acare_v26.onnx` (9.4 MB) — YOLO26 NMS-free, 6 surgical tool classes
- `acare_v11.onnx` (77 MB) — Legacy YOLO11 (stale)
- `model.pt` (39 MB) — PyTorch training checkpoint

---

## 6. ROS2 Communication Architecture

### 6.1 Topic Map

| Topic | Type | Publisher(s) | Subscriber(s) | QoS |
|---|---|---|---|---|
| `/robot_state` | RobotState | StateManager | All nodes | TRANSIENT_LOCAL |
| `/state_transition` | StateTransition | AuthNode, PlannerNode | StateManager | RELIABLE |
| `/safety_alert` | SafetyAlert | SafetyNode, VoiceNode | StateManager, PlannerNode | RELIABLE |
| `/emergency_stop` | EmergencySignal | VoiceNode, SafetyNode | EmbeddedInterface, StateManager | RELIABLE |
| `/raw_transcript` | Transcript | VoiceNodeROS | DialogueNode, AuthNode | RELIABLE |
| `/intent_result` | Intent | DialogueNode | AuthNode | RELIABLE |
| `/validated_intent` | ValidatedIntent | AuthNode | PlannerNode, DialogueNode | RELIABLE |
| `/auth_result` | AuthResult | AuthNode | StateManager, PlannerNode | RELIABLE |
| `/auth_request` | AuthRequest | PlannerNode, DialogueNode | AuthNode | RELIABLE |
| `/tts_request` | String | StateManager, PlannerNode, AuthNode | VoiceNodeROS | RELIABLE |
| `/vision_search_request` | VisionSearchRequest | PlannerNode | VisionNode | RELIABLE |
| `/vision_result` | VisionResult | VisionNode | PlannerNode, DialogueNode | RELIABLE |
| `/vision_status` | VisionStatus | VisionNode | PlannerNode | RELIABLE |
| `/vision_penalty` | String | PlannerNode | VisionNode (NBV) | RELIABLE |
| `/hand_status` | HandStatus | VisionNode | PlannerNode | RELIABLE |
| `/arm_command` | ArmCommand | PlannerNode, VisionNode | EmbeddedInterface | RELIABLE |
| `/gripper_command` | GripperCommand | PlannerNode | EmbeddedInterface | RELIABLE |
| `/motion_feedback` | MotionFeedback | EmbeddedInterface | PlannerNode, SafetyNode, VisionNode | BEST_EFFORT |
| `/log_event` | LogEvent | PlannerNode, VisionNode, SafetyNode | LogNode | BEST_EFFORT |
| `/scan` | LaserScan | YDLIDAR driver | SafetyNode | BEST_EFFORT |

### 6.2 Camera Topics (from ascamera node)

| Topic | Type | Rate |
|---|---|---|
| `/ascamera_hp60c/camera_publisher/rgb0/image` | Image (BGR8) | 12.4 Hz |
| `/ascamera_hp60c/camera_publisher/depth0/image_raw` | Image (16UC1) | 12.4 Hz |
| `/ascamera_hp60c/camera_publisher/rgb0/camera_info` | CameraInfo | — |
| `/ascamera_hp60c/camera_publisher/depth0/camera_info` | CameraInfo | — |
| `/ascamera_hp60c/camera_publisher/depth0/points` | PointCloud2 | — |

### 6.3 Services

| Service | Caller | Server |
|---|---|---|
| `/enrol_staff` | AdminCLI | AuthNode |
| `/clear_estop` | AdminCLI | EmbeddedInterface |

---

## 7. State Machine & Planner Architecture

### 7.1 10-State FSM — Complete Transition Table

```
                  ┌─────────┐
                  │ OFFLINE │
                  └────┬────┘
                       │
                  ┌────▼─────┐
          ┌──────►│LOGGED_OUT│◄──────────┐
          │       └────┬─────┘           │
          │            │                 │
          │       ┌────▼───┐             │
          │       │ STANDBY ├───┐         │
          │       └───┬─┬───┘   │         │
          │           │ │       │         │
          │     ┌─────┘ └──────┐ │         │
          │     ▼              ▼  │         │
          │ ┌─────────┐  ┌──────────┐ │         │
          │ │LISTENING│  │PROCESSING│ │         │
          │ └────┬────┘  └────┬─────┘ │         │
          │      │            │       │         │
          │      └──────┬─────┘       │         │
          │             ▼             │         │
          │        ┌──────────┐       │         │
          │        │EXECUTING │──┐    │         │
          │        └────┬─────┘  │    │         │
          │             │        │    │         │
          │        ┌────▼──┐     │    │         │
          │        │HOLDING├─────┤    │         │
          │        └────┬──┘     │    │         │
          │             │        │    │         │
          │        ┌────▼───┐    │    │         │
          │        │HANDOVER├────┤    │         │
          │        └────┬───┘    │    │         │
          │             │        │    │         │
          └─────────────┼────────┘    │         │
                        │             │         │
        ┌───────────────────┴───────────┐ │         │
        ▼                                ▼ │         │
   ┌─────────┐                     ┌───▼────┐ │         │
   │ ESTOP   │◄── from ANY state ─┤  ERROR  │ │         │
   └────┬────┘                     └────┬───┘ │         │
        │                               │      │
        └──────────────┬────────────────┘      │
                       │                       │
                       ▼                       │
                  ┌─────────┐                  │
                  │ STANDBY │◄──────────────────┘
                  └─────────┘
```

### 7.2 Task Execution Flow

1. **Validated Intent** arrives → PlannerNode creates TaskSnapshot with LLM context
2. **Agentic Planner loop**: LLM proposes one tool call per turn
3. **Tool Kernel** validates: schema → dedup → 6-layer safety gate → ESTOP check
4. **Vision search**: arm moves to NBV viewpoints, YOLO detects, localiser computes 3D
5. **Grasp**: IK solver computes joint angles → arm moves to pregrasp → descend → grip
6. **Handover**: face (advisory) → palm detection → voice confirmation → release
7. **Memory update**: task outcome saved to SQLite, Bayesian map updated

### 7.3 Recovery Ladders

**Vision failure:**
1. Try `preferred_zone` from user priors
2. Query Bayesian probability map (AUTO)
3. Ask user for location
4. Abort if still not found

**Grasp failure:**
1. Increase grip force (FIRM)
2. Change approach angle (SIDE_LEFT/SIDE_RIGHT)
3. Try next detection candidate
4. Abort

**Handover failure:**
1. Face retry with voice prompt
2. Hand detection retry with voice prompt
3. Voice confirmation retry
4. Abort

---

## 8. Vision Pipeline

### 8.1 Detection Pipeline

```
Camera → scene profile (HSV analysis)
       → low-light? → gamma correction (1.55/1.85) + CLAHE + unsharp mask
       → YOLO26 ONNX inference (320×320 input, NMS-free output)
       → confidence threshold (0.70 normal / 0.56 low-light)
       → temporal consistency check (50px proximity promotion at 0.65)
       → fake detection (Laplacian < 120 + depth variance < 0.002 m²)
       → 3D localisation (pinhole + dynamic wrist-camera transform)
       → workspace boundary check
       → publish VisionResult
```

### 8.2 Bayesian NBV Search

- 3 zones (A, B, C) with calibrated viewpoints
- Sorted by P(tool | zone) from probability map
- 3 frame captures per viewpoint with wrist micro-offsets
- Bayesian update: found ×1.5, not found ×0.7, passive seen ×1.3
- Probability clamped to [0.05, 0.90] after each update
- Vision penalty: successful grasp failures decay zone probability by ×0.3

### 8.3 3D Localisation

For a detection at pixel (u, v) with depth Z mm:

```
X = (u - cx) × Z / fx
Y = (v - cy) × Z / fy
Z = depth_mm / 1000.0

P_robot = T_robot_camera × [X, Y, Z, 1]^T
```

Where `T_robot_camera` is computed dynamically per arm pose via FK for wrist-mounted cameras.

---

## 9. Voice Pipeline

### 9.1 Processing Flow

```
Mic → Silero VAD (32ms chunks)
    → Deepgram Nova-2 (streaming, endpointing=300ms)
    → Transcript
    → Normaliser (lowercase, filler removal, punctuation)
    → Alias Expansion (word-boundary regex)
    → Fast Intent (ESTOP/confirm/cancel regex — no LLM)
    → Intent Parser (Groq 8B, JSON mode)
    → Dialogue Manager (multi-turn, confirmation)
    → TTS Queue (3-tier fallback)
```

### 9.2 State Machine

Voice pipeline has its own FSM (standalone mode):
`IDLE → LISTENING → PROCESSING → RESPONDING → CLARIFYING → CONFIRMED → ASSISTING → ESTOP → ERROR`

### 9.3 ESTOP Detection

- Dedicated thread, never blocked by other processing
- 100ms collision window (debounce)
- 6 keywords: stop, halt, emergency, abort, ruko, bas
- Continuation-word cancellation: "stop moving" ≠ ESTOP
- Final-transcript backstop: short utterances (≤ 2 words) re-checked
- < 200ms end-to-end from utterance to `/emergency_stop` publish

---

## 10. Authentication & Biometrics

### 10.1 Two-Layer Identity Model

**Layer 1 — Initial Login:**
1. Passive face scan (MediaPipe, 0.5s timer) detects face
2. Matches against enrolled profiles via InsightFace buffalo_sc (cosine ≥ 0.78)
3. Prompts identified user: "Welcome [name]. Say confirm to log in."
4. Voice verification: ECAPA-TDNN checks "confirm" utterance (cosine ≥ 0.85)

**Layer 2 — Active Session Consistency:**
1. Every subsequent command sampled for speaker verification
2. Voice embedding compared against logged-in user (not all profiles)
3. 3 consecutive failures → reconfirmation prompt
4. Pending intent retained during reconfirmation

### 10.2 Demo Mode

When `demo_mode: true`:
- Biometric auth bypassed (auto-enrols "Demo User")
- Returns 0.99 confidence for all verification calls
- No camera or microphone needed for end-to-end testing

---

## 11. Safety Architecture

### 11.1 Dual-Layer Safety

**Software layer (Pi 5):**
- SafetyNode monitors LiDAR + MCU telemetry
- Publishes graded SafetyAlert: WARNING → CRITICAL → ESTOP
- ESTOP never throttled; others 1/sec
- Self-test every 30s verifies `/emergency_stop` subscribers

**Firmware layer (Teensy 4.1):**
- ISRs cut motor power directly on overcurrent/overtemp
- 200ms SPI watchdog — no valid packet → immediate PWM disable
- Hardware ESTOP button — direct 24V cutoff

### 11.2 ESTOP Triggers

| Trigger | Latency | Source |
|---|---|---|
| Voice keyword | < 200ms | Dedicated thread, 100ms debounce |
| LiDAR proximity (< 400mm) | < 100ms | SafetyNode |
| Overcurrent (> 8A) | Immediate | Teensy ISR |
| Overtemperature (> 75°C) | Immediate | Teensy ISR |
| SPI watchdog timeout (> 200ms) | 200ms | Teensy firmware |
| Physical ESTOP button | Immediate | Hardware 24V cutoff |

### 11.3 Handover Safety (3-Gate Protocol)

1. **Face detection** — Advisory only (never aborts alone)
2. **Palm detection** — Required (MediaPipe Hands, X-axis depth approach)
3. **Voice confirmation** — Required ("Say 'take' to receive")

All gates must pass before gripper release. Timeout: 30s → safe deposit to tray.

---

## 12. Configuration Reference

### 12.1 system.yaml (147 lines)

**`robot.workspace`** — Reachable envelope: x/y ±0.60m, z 0.0-0.75m
**`robot.safe_drop_zone`** — (0.0, 0.35, 0.05) [placeholder]
**`robot.handover_zone`** — (0.0, 0.40, 0.10) [placeholder]
**`arm.link_lengths`** — base 0.352m, upper_arm 0.400m, forearm 0.400m, wrist 0.236m
**`arm.joint_limits_min/max`** — All 6 joints in radians
**`arm.kiosk_rest_joint_angles`** — [0.0, 0.15, -0.35, 0.0, 0.10, 0.0]
**`arm.kiosk_interaction_joint_angles`** — [0.0, -0.10, -0.05, 0.0, -0.05, 0.0]
**`arm.control_soft_limits`** — kiosk_velocity_scale=0.22, kiosk_accel_limit=0.10
**`camera`** — Intrinsics, T_flange_camera, T_robot_camera
**`vision.model_path`** — `models/acare_v26.onnx`
**`vision.confidence_threshold`** — 0.70 (normal), 0.56 (low-light)
**`voice.estop_keywords`** — [stop, halt, emergency, abort, ruko, bas]
**`voice.edge_tts_voice`** — `en-IN-NeerjaNeural`
**`auth.voice_similarity_threshold`** — 0.85
**`auth.face_similarity_threshold`** — 0.78
**`planner.tool_budget_per_task`** — 20
**`planner.llm_timeout_s`** — 4.0
**`demo_mode`** — true (bypasses biometric auth for testing)

### 12.2 thresholds.yaml (18 lines)

| Parameter | Warning | ESTOP |
|---|---|---|
| current_limit_A | 6.0 A | 8.0 A |
| temperature_C | 55°C / 65°C slow | 75°C |
| lidar_mm | 600 mm | 400 mm |
| gripper_force_limit_N | 10.0 N | 15.0 N |
| velocity_limit_deg_s | 80 °/s | 120 °/s |

### 12.3 probability_map.yaml (30 lines)

- 3 zones (zone_A, zone_B, zone_C)
- 6 tool classes per zone
- Values sum to 1.0 per zone
- Clamped to [0.05, 0.90] after Bayesian updates

### 12.4 Environment Variables (.env)

| Variable | Required | Purpose |
|---|---|---|
| `DEEPGRAM_API_KEY` | Yes | Deepgram Nova-2 STT |
| `GROQ_API_KEY` | Yes | Groq LLM (intent + fallback) |
| `NVIDIA_API_KEY` | No | NVIDIA NIM (primary planner) |

---

## 13. SPI Communication Protocol

### 13.1 Physical Layer

| Signal | Pi 5 GPIO | Teensy 4.1 Pin |
|---|---|---|
| MOSI | Pin 19 (GPIO 10) | Pin 11 |
| MISO | Pin 21 (GPIO 9) | Pin 12 |
| SCLK | Pin 23 (GPIO 11) | Pin 13 |
| CS | Pin 24 (GPIO 8) | Pin 10 |
| ATTN | Pin 22 (GPIO 25) | Pin 9 |

- **Clock:** 10 MHz, Mode 0 (CPOL=0, CPHA=0)
- **Frame size:** 64 bytes fixed, full-duplex
- **Error control:** CRC32 in last 4 bytes
- **Watchdog:** 200ms timeout → Teensy disables PWM

### 13.2 Command Frame (Pi → Teensy) — 64 Bytes

| Offset | Size | Field |
|---|---|---|
| 0-1 | 2B | Header (0xAA 0x55) |
| 2 | 1B | Sequence ID |
| 3 | 1B | Command type (0x01 MOVE, 0x02 GRASP, 0x03 RELEASE, 0x04 ESTOP, 0x05 HEARTBEAT) |
| 4-27 | 24B | 6× float32 joint targets (radians) |
| 28-31 | 4B | float32 velocity scale (0.0-1.0) |
| 32-35 | 4B | float32 acceleration limit |
| 36-39 | 4B | float32 gripper force target (N) |
| 40 | 1B | System state enum |
| 41-59 | 19B | Reserved |
| 60-63 | 4B | CRC32 |

### 13.3 Telemetry Frame (Teensy → Pi) — 64 Bytes

| Offset | Size | Field |
|---|---|---|
| 0-1 | 2B | Header (0xAA 0x55) |
| 2 | 1B | Echo sequence ID |
| 3 | 1B | Teensy state (IDLE/POSITION_CONTROL/GRIPPER_CONTROL/ESTOP/FAULT) |
| 4 | 1B | Fault code |
| 5-28 | 24B | 6× float32 actual joint positions |
| 29-52 | 24B | 6× float32 actual joint velocities |
| 53-56 | 4B | float32 gripper force (N) |
| 57-62 | 6B | IMU pitch/roll/yaw (3× int16) |
| 63 | 1B | Reserved |

---

## 14. Performance Specifications

### 14.1 System Latency KPIs

| Metric | Target | Method |
|---|---|---|
| ESTOP latency | < 200 ms | Voice keyword to motor PWM disable |
| STT endpointing | 300 ms | Deepgram silence threshold |
| Face verification | < 500 ms | InsightFace embedding comparison |
| Voice verification | < 600 ms | ECAPA-TDNN ONNX inference |
| YOLO inference | < 850 ms | Single frame, Pi 5 CPU |
| IK resolution | 0.0000 m | Analytical FK/IK round-trip |
| Task completion | < 120 s | Total from intent to handover |

### 14.2 Biometric Thresholds

| Parameter | Value | Location |
|---|---|---|
| Voice similarity (cosine) | ≥ 0.85 | system.yaml auth.voice_similarity_threshold |
| Face similarity (cosine) | ≥ 0.78 | system.yaml auth.face_similarity_threshold |
| Voice enrolment samples | 3 | system.yaml auth.enrol_voice_samples |
| Face enrolment frames | 10 | system.yaml auth.enrol_face_frames |

### 14.3 Vision Thresholds

| Parameter | Normal Light | Low Light |
|---|---|---|
| YOLO confidence | ≥ 0.70 | ≥ 0.56 |
| Scene brightness cutoff (V-mean) | — | < 80 |
| Temporal consistency radius | 50 px | 50 px |
| Temporal promotion confidence | 0.65 | 0.65 |

### 14.4 Safety Limits

| Parameter | Warning | ESTOP |
|---|---|---|
| Joint current | > 6.0 A | > 8.0 A |
| Joint temperature | > 55°C / > 65°C slow | > 75°C |
| Joint velocity | > 80 °/s | > 120 °/s |
| LiDAR proximity (base) | 400-600 mm | < 400 mm |
| Gripper force | > 10 N | > 15 N |

---

## 15. Calibration & Deployment

### 15.1 Physical Calibration Steps

1. **Joint homing** — Move each joint to limit switch, zero encoder
2. **Camera intrinsics** — NOT required (HP60C auto-publishes from driver)
3. **Workspace confirmation** — Verify system.yaml coordinates
4. **Safe drop zone** — Manually position arm, record joint angles
5. **NBV viewpoints** — Move arm to each tray zone, record 6 joint angles
6. **Fake detection calibration** — 20 real + 20 fake samples, compute thresholds
7. **LiDAR baseline** — Clear workspace, record reference scan

### 15.2 Deployment Checklist

- [ ] Create `.env` with Deepgram, Groq API keys
- [ ] Build workspace: `colcon build && source install/setup.bash`
- [ ] Verify all 11 nodes: `ros2 node list`
- [ ] Check camera streams: `ros2 topic echo /ascamera_hp60c/.../rgb0/image`
- [ ] Test voice standalone: `python3 -m acare_voice.main`
- [ ] Verify ESTOP: publish `/emergency_stop` manually
- [ ] Run IK self-test: `python3 -m acare_planner.ik_solver`

### 15.3 Tray Placement

- Instrument tray must sit **0.40-0.55 m from the arm base**
- Closer than 0.40m → elbow past -120° limit
- Max reach: 0.80m; practical top-down grasp: 0.40-0.55m

---

## 16. Pending Work & Future Scope

### Physical Calibration (Requires Arm Assembly)

| # | Item | Effort |
|---|---|---|
| C1 | Measure T_flange_camera (flange-to-lens offset) | 10 min |
| C2 | Calibrate DH parameters for all 6 joints | 2-3 hrs |
| C3 | Calibrate NBV viewpoints for tray zones | 30 min |

### Hardware Bring-Up

| # | Item | Effort |
|---|---|---|
| H1 | SPI wiring + Teensy firmware flash | 30 min |
| H2 | Motor PID tuning (P/I/D per joint) | 1-2 days |
| H3 | AS5600 encoder offset calibration | 1 hr |
| H4 | ESTOP hardware test and documentation | 1 hr |

### Software Enhancements

| # | Item | Effort |
|---|---|---|
| S1 | Dynamic FK extrinsics into NBV search | 30 min |
| S2 | Voice-driven staff registration | Medium |
| S3 | Offline STT fallback (Vosk/whisper.cpp) | Medium |
| S4 | ActionServer migration (replace polling) | Large |

---

## Revision History

| Date | Changes |
|---|---|
| 2026-06-09 | Initial complete documentation (22 bugs fixed) |
| 2026-06-11 | +10 additional bug fixes, 32 total fixed |
| 2026-06-12 | Full code audit, 4 more fixes, Pi deployment |
| 2026-06-13 | 15 additional fixes across all packages |
| 2026-07-11 | Final cleanup: repo structure reorganised, stale files removed, documentation consolidated for academic submission |

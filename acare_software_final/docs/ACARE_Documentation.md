# ACARE — Complete Project Documentation

**Autonomous Clinical Assistance Robot with Multimodal Biometric Authentication and Dynamic Human Handover**

---

## 0. PROJECT OVERVIEW & DOMAIN MAP

| Field | Details |
|---|---|
| Institution | Ramaiah Institute of Technology, Bengaluru |
| Department | Electronics and Communication Engineering |
| Guide | Dr. Lakshmi Shrinivasan, Associate Professor |
| Team | Sathvik Rao · Sarvesh Bhattacharyya · Shreevanth M · Shreyas S |
| Funding | ₹40,000 — Institutional Grant |
| Status | Active Development — June 2026 |

### Domain Map
| Domain | Scope |
|---|---|
| SOFTWARE | AI pipelines, ROS2 nodes, orchestration, admin CLI |
| HARDWARE | Mechanical, electrical, power, physical components |
| EMBEDDED / FIRMWARE | Teensy 4.1 motor control, sensor ISR loops, PID |
| INTEGRATION BOUNDARY | Protocol contracts between software and embedded |

### Objective
ACARE is a stationary 6-DOF semi-autonomous robotic arm designed for clinical environments — specifically plastic surgery departments — where surgical tools must be fetched and delivered to authorised staff repeatedly across long procedure shifts. The robot replaces the manual, hygiene-risk-bearing task of instrument handling by providing a voice-commanded, biometrically authenticated, autonomous pick-and-place system with human oversight.

### Core Problems Solved
- Staff fatigue from repetitive tool retrieval during 10–12-hour surgical shifts
- Hygiene risks from manual handling of sterile instruments
- Procedure delays caused by instrument unavailability or incorrect delivery
- Absence of affordable autonomous assistance solutions in Indian healthcare settings

### Scope — Finalised
- Stationary pick-and-place operation only — navigation removed from scope
- Contactless operation — entirely voice commanded, no physical input required
- Dual biometric authentication — voice and face combined for every session
- Single active user session at any time — one command per turn
- Single tool per command — multi-tool requests handled via clarification dialogue
- Next-Best-View intelligent search — not continuous scanning
- Direct handover — tool delivered from gripper directly into authenticated staff's hand

### System Architecture Summary
ACARE is a two-layer hierarchical robotic system. The high-level intelligence layer runs on a Raspberry Pi 5 using ROS2. The real-time motor control layer runs on a Teensy 4.1 (Cortex-M7).
These two layers communicate via SPI bus. All AI and software pipelines are isolated from hardware control.

- SOFTWARE — Raspberry Pi 5 + ROS2 + Python AI Nodes
- EMBEDDED / FIRMWARE — Teensy 4.1 / Cortex-M7 + ESP32 + PID + Safety ISR
- HARDWARE — 6-DOF Arm + Sensors + Power System

### Key Differentiation vs Prior Art
Unlike MOXI, TIAGo, TUG, or LIO, ACARE integrates multimodal biometric authentication (voice + face), voice-driven instrument retrieval with structured intent parsing, adaptive probabilistic vision search, and dynamic human-robot handover with real-time palm tracking — all within a layered safety architecture that separates high-level intelligence from deterministic motor control.

---

## 0.1 Deep System Architecture Map

```mermaid
graph TD
    %% ==========================================
    %% EXTERNAL CLOUD SERVICES
    %% ==========================================
    subgraph Cloud["External Cloud Services (Required)"]
        Deepgram["Deepgram Nova-2 (Streaming STT)"]
        Groq["Groq API (Llama Intent / Fallback LLM)"]
        NIM["NVIDIA NIM Nemotron-49B (Agentic Planner)"]
        EdgeTTS["Microsoft Edge TTS (Response Gen)"]
    end

    %% ==========================================
    %% HARDWARE, ENVIRONMENT & PHYSICAL LAYER
    %% ==========================================
    subgraph Physical["Hardware & Physical Environment"]
        User["Surgical Staff"]
        Mic["Microphone (USB Sound Card)"]
        Speaker["Active Speaker"]
        Camera["YDLIDAR HP60C RGBD Camera"]
        LiDAR["YDLIDAR T-mini Plus 2D LiDAR"]
        Arm["6-DOF Serial Manipulator (PETG + Aluminum)"]
        Motors["BLDC Motors + RMCS-3002l Drivers"]
        Encoders["AS5600 Magnetic Encoders (I2C)"]
        Sensors["Current Shunts, Thermistors, Gripper FSR"]
        ESTOP_Btn["Physical Hard-Cut ESTOP Button"]
        Workspace["Surgical Tray & Safe Drop Zone"]
    end

    %% ==========================================
    %% EMBEDDED FIRMWARE LAYER (TEENSY 4.1)
    %% ==========================================
    subgraph Firmware["Embedded Firmware (Teensy 4.1)"]
        SPI_Slave["SPI0 DMA Slave (10 MHz)"]
        MotorControl["200 Hz PID Motor Control Loop"]
        SensorPoll["100 Hz Sensor Polling Loop"]
        SafetyISR["Hardware Fault Protections (Soft/Hard Cut)"]
        Watchdog["5 Hz Keepalive Watchdog"]
        
        SPI_Slave <--> MotorControl
        SPI_Slave <--> SensorPoll
        SensorPoll --> Encoders
        SensorPoll --> Sensors
        MotorControl --> Motors
        ESTOP_Btn -.->|Direct 24V PWM Cutoff| Motors
        SafetyISR --> MotorControl
        Watchdog --> MotorControl
    end

    %% ==========================================
    %% ROS2 SOFTWARE LAYER (RASPBERRY PI 5)
    %% ==========================================
    subgraph Software["ROS2 Software Layer (Raspberry Pi 5)"]
        
        subgraph Bringup["acare_bringup & Admin"]
            Supervisor["supervisor_node.py (ROS2 Node — Graph API Monitor)"]
            AdminCLI["acare_admin (CLI, Calibration, Config Updates)"]
        end

        subgraph Voice["acare_voice"]
            VoiceNode["Voice Orchestrator"]
            VAD["Silero VAD (32ms Chunks)"]
            Keyword["ESTOP Keyword Thread (<200ms)"]
            TTS_Stack["TTS Manager (Edge-TTS / Kokoro ONNX / pyttsx3)"]
        end

        subgraph Dialogue["acare_dialogue"]
            DialogueNode["Dialogue & Context Normaliser"]
            IntentRegex["fast_intent (Regex Bypass)"]
        end

        subgraph Auth["acare_auth"]
            AuthNode["Auth Gate & Enrolment Loop"]
            FaceDetect["MediaPipe Face (Passive Scan)"]
            FaceVerify["InsightFace buffalo_sc (Cosine >0.78)"]
            VoiceVerify["SpeechBrain ECAPA-TDNN ONNX (>0.85)"]
            SQLiteUser["users.db (Biometric Storage)"]
        end

        subgraph Planner["acare_planner"]
            StateManager["StateManager (10-State Global FSM)"]
            PlannerNode["PlannerNode (Master Orchestrator)"]
            Agentic["AgenticPlanner (LLM Adapter)"]
            SafetyKernel["Deterministic Safety Kernel (6-Layer Guard)"]
            IK["IKSolver (Analytical 6-DOF)"]
            Handover["3-Gate Handover Protocol"]
            TaskMem["Task Memory & Bayesian Priors"]
        end

        subgraph Vision["acare_vision"]
            VisionNode["Vision Orchestrator"]
            YOLO["YOLO26ONNX (NMS-Free INT8 CPU)"]
            Localiser["Depth -> 3D Back-Projector"]
            NBV["Bayesian NBV Search Engine"]
            FakeDetect["Fake Detector (Laplacian Texture & Depth Var)"]
            HandTrack["MediaPipe Hands (X-Axis Depth Approach)"]
        end

        subgraph Safety["acare_safety"]
            SafetyNode["Safety Monitor (LiDAR Zones & Telemetry)"]
        end

        subgraph Logging["acare_logging"]
            LogNode["Audit Trail Logger (SQLite, 200MB Auto-Rotate)"]
        end

        subgraph EmbeddedInterface["acare_embedded_interface"]
            InterfaceNode["SPI / UART Hardware Bridge"]
        end
    end

    %% ==========================================
    %% DATA FLOWS & COMMUNICATION (TOPOLOGY)
    %% ==========================================

    %% Physical to Voice
    User -->|Voice Commands| Mic
    Mic --> VoiceNode
    VoiceNode --> VAD
    VAD -->|Stream| Deepgram
    VoiceNode --> Keyword
    Deepgram -->|/raw_transcript| DialogueNode
    Keyword -->|/emergency_stop| StateManager

    %% Dialogue to Intent
    DialogueNode --> IntentRegex
    DialogueNode -->|LLM Intent Parsing| Groq
    DialogueNode -->|/intent_result| AuthNode

    %% Auth & Biometrics
    Camera --> FaceDetect
    FaceDetect --> FaceVerify
    Deepgram --> VoiceVerify
    FaceVerify <--> SQLiteUser
    VoiceVerify <--> SQLiteUser
    AuthNode -->|/validated_intent| PlannerNode
    AuthNode -->|/state_transition| StateManager

    %% Planning & Agentic Reasoning
    PlannerNode <--> Agentic
    Agentic <--> NIM
    Agentic <--> TaskMem
    Agentic -->|Propose Search Strategy (AUTO)| NBV
    
    %% Vision Pipeline
    PlannerNode -->|/vision_search_request| VisionNode
    Camera --> VisionNode
    VisionNode --> YOLO
    VisionNode --> Localiser
    VisionNode --> NBV
    VisionNode --> FakeDetect
    VisionNode -->|/vision_result| PlannerNode
    
    %% Safety Kernel & Motion
    PlannerNode --> SafetyKernel
    SafetyKernel --> IK
    IK -->|/arm_command & /gripper_command| InterfaceNode
    InterfaceNode <-->|SPI 10MHz DMA Frame| SPI_Slave
    InterfaceNode -->|/motion_feedback| SafetyNode
    InterfaceNode -->|/motion_feedback| PlannerNode

    %% Handover Protocol (Sub-Flow)
    PlannerNode --> Handover
    Handover -->|Trigger Hand Search| HandTrack
    HandTrack --> Camera

    %% Safety & Telemetry
    LiDAR --> SafetyNode
    SafetyNode -->|/safety_alert| StateManager
    SafetyNode -->|/safety_alert| PlannerNode
    Keyword -->|ESTOP Hard-Cut /safe_deposit| PlannerNode

    %% Feedback & Audio Out
    PlannerNode -->|/tts_request| VoiceNode
    AuthNode -->|/tts_request| VoiceNode
    SafetyNode -->|Urgent TTS /tts_request| VoiceNode
    VoiceNode --> TTS_Stack
    TTS_Stack -->|Cloud TTS| EdgeTTS
    TTS_Stack --> Speaker

    %% System Auditing
    PlannerNode -->|/log_event| LogNode
    VisionNode -->|/log_event| LogNode
    AuthNode -->|/log_event| LogNode

    %% Workspace Physical Action
    Motors --> Arm
    Arm --> Workspace
    Workspace --> Camera
```

---


## QUICK COMMANDS (copy-paste ready)

### SSH into Pi
```bash
ssh acare@10.178.112.174
# password: acare1234
# home WiFi (Airtel_Sarsou): ssh acare@192.168.1.2
```

### Find Pi IP if it changed
```powershell
arp -a
# then try: ssh -o ConnectTimeout=3 acare@192.168.1.X "hostname"
```

### Sync code from laptop to Pi (run from Windows PowerShell)
```powershell
$PI = "acare@192.168.1.2"
$SRC = "C:\Users\Sonali\Desktop\ACARE\acare_software_final"
foreach ($pkg in @("acare_bringup","acare_msgs","acare_planner","acare_safety","acare_logging","acare_vision","acare_voice","acare_auth","acare_dialogue","acare_embedded_interface","acare_admin")) {
    scp -r "$SRC\$pkg" "${PI}:~/acare_ws/src/"
}
scp "$SRC\models\acare_v26.onnx" "${PI}:~/acare_ws/src/models/"
```

### Rebuild on Pi (run after syncing code)
```bash
cd ~/acare_ws && colcon build && source install/setup.bash
```

### Start camera on Pi
```bash
cd ~/acare_ws && ros2 launch ascamera hp60c.launch.py
```

### Run full ROS2 system on Pi
```bash
cd ~/acare_ws && source install/setup.bash && ros2 launch acare_bringup acare.launch.py
```

### Run voice pipeline standalone on laptop (no Pi needed)
```powershell
cd C:\Users\Sonali\Desktop\ACARE\acare_software_final\acare_voice
& "C:\Users\Sonali\Desktop\ACARE\.venv\Scripts\python.exe" -u main.py
```

### Run Gazebo simulation (on WSL)
```bash
~/acare_sim_ws/launch_full_sim.sh
```

### Check Pi health
```bash
vcgencmd measure_temp && df -h / && free -h
```

### Shut down Pi (always do this before unplugging)
```bash
sudo shutdown now
```

### Add new WiFi to Pi (safe — does NOT disconnect)
```bash
# This Pi uses systemd-networkd + netplan (NOT NetworkManager).
# nmcli is NOT available. Add via netplan connection add:
# WARNING: editing /etc/netplan/*.yaml over SSH can corrupt config if SSH drops.
# Only add when stable and connected — use nmcli IF NetworkManager is installed.
# Check with: systemctl status NetworkManager
```

### Test YOLO detection on Pi (camera must be running)
```bash
source /opt/ros/jazzy/setup.bash && source ~/acare_ws/install/setup.bash
python3 ~/test_detect.py
```

### Test 3D localisation on Pi (camera must be running)
```bash
source /opt/ros/jazzy/setup.bash && source ~/acare_ws/install/setup.bash
python3 ~/test_localise.py
```

### Check ROS2 topics are live
```bash
source /opt/ros/jazzy/setup.bash && source ~/acare_ws/install/setup.bash
ros2 topic list
ros2 topic echo /robot_state --once
```

### IK solver self-test (on laptop or Pi)
```bash
python3 -m acare_planner.ik_solver
```

---



A full line-by-line review found and fixed the following defects:

### Safety-critical (BLOCKER)
- **ESTOP was silently dropped from most states.** `state_manager._transition()` rejected ESTOP unless it was in the current state's allowed-transitions list — so an ESTOP alert in STANDBY/LISTENING/PROCESSING was ignored. Fixed: ESTOP and ERROR now bypass the transition table and are reachable from ANY state.
- **Voice "stop" did not trigger ESTOP.** Keyword detection only ran on Deepgram partials; with `endpointing=15000` (15s) partials were rare. Fixed: added a final-transcript ESTOP backstop in `voice_node._on_transcript` + reduced endpointing to 300ms.
- **Embedded interface blocked the executor.** `wait_for_server(timeout=2s)` in a callback could delay the ESTOP callback. Fixed: non-blocking `server_is_ready()`.

### High
- **Voice latency:** Deepgram `endpointing` was 15000ms (15s) → every command took 15s to finalize. Fixed to 300ms + `utterance_end_ms=1000`.
- **Gripper guard fail-open:** lowercase "grasp"/"close" bypassed the LOGGED_OUT guard. Fixed: guard computed on upper-cased command.
- **ESTOP latch never reset** in embedded interface — every goal rejected until restart. Fixed: cleared on recovery to STANDBY/LOGGED_OUT.
- **Log events silently dropped:** log_node subscribed RELIABLE but planner published BEST_EFFORT (QoS mismatch). Fixed: subscribe with TOPIC_LOGGING.
- **Log rotation could crash/fill disk** (IN-clause variable limit). Fixed: delete by timestamp cutoff.
- **Hand tracking fed BGR to MediaPipe** (needs RGB) → degraded handover detection. Fixed: BGR→RGB conversion.

### Medium
- **State machine invalid transition** PROCESSING→ASSISTING. Fixed: added valid edges.
- **fast_intent used `.match()`** (start-anchored) → "I would like scissors" missed. Fixed: `.search()`.
- **alias_expansion substring match** → "youtube"→cream, "attempt"→thermometer. Fixed: word-boundary matching + removed dangerous short aliases.
- **Planner workspace hardcoded** (±0.4) contradicting system.yaml (±0.6). Fixed: load from config.
- **ESTOP didn't interrupt a running task thread.** Fixed: `_estop_active` event checked between phases + blocks new moves.
- **Per-task state leaked** (height adjustment, voice confirm word). Fixed: reset at task start.
- **NBV crash on padded None frames.** Fixed: pick first non-None reference frame.
- **agent_schema workspace bound** ±1.0 too loose. Fixed: ±0.85 (matches 0.8m reach); IK is the real gate.
- **log_node SQLite thread-safety** + no periodic flush + TEXT timestamp ordering. Fixed: lock + 5s flush timer + INTEGER timestamps.

### Low
- safety_node alert spam at 50Hz. Fixed: 1s throttle for WARNING/CRITICAL (ESTOP never throttled).
- localiser div-by-zero guard on bad intrinsics. Fixed.
- localiser single-pixel depth read missed sparse depth. Fixed: median-of-window fallback.

All fixes verified by parse + logic tests. IK FK/IK round-trip still 0.0000m. ESTOP reachable from all 10 states (verified).

### Recent Agentic Planner & Safety Sweep Fixes
- **Agentic Planner State Sync**: Added missing `StateTransition` publishers inside the agentic loop. Handled ESTOP cleanly by breaking loop to STANDBY without unhandled exceptions. Saved memory outcomes.
- **Dialogue/Auth Race Condition**: Removed redundant `validate_intent` publishes from dialogue; `auth_node.py` now exclusively intercepts `/intent_result`.
- **Dialogue Confidence Gate**: Fast intents with confidence < 0.8 now transition to an internal clarification loop instead of executing blindly.
- **Dialogue Memory Leak**: Clears temporary tracking state on `LOGGED_OUT`, `ESTOP`, or `HANDOVER`.
- **Voice Drift Handling**: `auth_node.py` now retains `_pending_intent` during voice re-confirmation instead of dropping it entirely.
- **Safety**: `voice_ros_node.py` and `auth_node.py` explicitly ignore all incoming intents and transcript processing when the robot is in `ESTOP`.
- **Vision Crash/Logic**: `fake_detector.py` guarded against OpenCV crashes from degenerate bounding boxes; `hand_tracker.py` uses X-axis for forward depth approach.
- **Admin CLI Resiliency**: Safely handles empty `system.yaml` or `thresholds.yaml` files.
- **Schema Cleanup**: Removed 9 unused Pydantic models from `agent_schema.py` to prevent validation clashes.

---

## 1. Pi Credentials & Known Hosts

### Credentials

| Field | Value |
|---|---|
| Username | `acare` |
| Password | `acare1234` |
| Hostname | `acare` |
| WiFi | `Airtel_Sarsou`, `motorola edge 70 fusion` (Hotspot, password: `12344321`) |

### Current IPs

| Network | IP |
|---|---|
| Airtel_Sarsou | `192.168.1.2` |
| sarv_wifi (mobile hotspot) | `10.178.112.174` (latest) |
| motorola edge 70 fusion (hotspot) | TBD |

### Known Hosts

| Date | IP | Network | Notes |
|---|---|---|---|
| 2026-06-10 | TBD | motorola edge 70 fusion (hotspot) | Added network from Shreyas Ec |
| 2026-06-02 | `10.178.112.174` | sarv_wifi (mobile hotspot) | Confirmed working after power cycle |
| 2026-05-29 | `10.12.133.174` | sarv_wifi (mobile hotspot) | Previous session |
| 2026-05-29 | `192.168.1.2` | Airtel_Sarsou | After reflash, DHCP assigned new IP |
| (old) | `192.168.1.72` | Airtel_Sarsou | Original IP before reflash — no longer valid |
| (old) | `192.168.1.73` | Airtel_Sarsou | Alternate old IP — no longer valid |

### Saved WiFi Networks (in netplan — systemd-networkd)

- `Airtel_Sarsou`
- `sarv_wifi`
- `motorola edge 70 fusion`

**Note:** This Pi uses `systemd-networkd` + netplan (NOT NetworkManager). The `nmcli` command only works if NetworkManager is installed. WiFi networks are stored in `/etc/netplan/50-cloud-init.yaml`.

---

## 2. Software Architecture — Package Map

| Package | Type | Purpose |
|---|---|---|
| `acare_msgs/` | CMake | ROS2 message/service definitions (18 `.msg` + 1 `.srv`). Defines the typed contract between all nodes. |
|| `acare_bringup/` | Python | Shared infrastructure: `paths.py` (all file paths), `qos_profiles.py` (per-topic QoS), `config/` (system.yaml, thresholds.yaml, probability_map.yaml), `launch/`, `supervisor_node.py` (ROS2 node — graph API monitoring & power recovery). |
| `acare_voice/` | Python | Voice pipeline: VAD (Silero) → ASR (Deepgram Nova-2 streaming) → normaliser → alias expansion → intent parser (Groq 8B) → fast_intent (regex) → assistant agent (Groq 70B for LOGGED_OUT conversation) → TTS (edge-tts normal, pyttsx3 urgent) → keyword monitor (ESTOP). Also: `voice_ros_node.py` (ROS2 wrapper), `voice_node.py` (standalone orchestrator), `dialogue_manager.py`, `semantic_turn_detector.py`, `tts_queue.py`, `tts_cache.py`, `earcons.py`. |
| `acare_dialogue/` | Python | ROS2 dialogue node: subscribes to `/raw_transcript`, runs intent parsing + assistant agent, publishes `/intent_result`. Handles pronoun resolution, multi-tool detection, session memory. |
| `acare_auth/` | Python | Biometric authentication: passive face scan (MediaPipe), face verification (InsightFace buffalo_sc), voice verification (ECAPA-TDNN via ONNX), user storage (SQLite), enrolment service. Publishes `/validated_intent` after auth gate passes. |
| `acare_planner/` | Python | Task planner: `state_manager.py` (10-state FSM), `planner_node.py` (full task orchestration), `agentic_planner.py` (NIM Nemotron-49B primary + Groq 70B fallback for reasoning), `agent_schema.py` (Pydantic validation), `handover.py` (3-gate protocol), `ik_solver.py`, `tool_registry.py`. |
| `acare_safety/` | Python | Safety monitoring: LiDAR proximity zones (600mm caution, 400mm ESTOP), MCU telemetry (current, temperature, gripper force), publishes graded `SafetyAlert`. |
| `acare_vision/` | Python | Perception: `vision_node.py` (orchestrator), `yolo_infer.py` (YOLO26 NMS-free ONNX), `nbv_search.py` (Bayesian probability map + next-best-view), `localiser.py` (depth→3D), `hand_tracker.py` (MediaPipe Hands for handover), `fake_detector.py`, `hp60c_camera_node.py`. |
| `acare_logging/` | Python | Audit trail: SQLite database, batched writes, auto-rotation at 200 MB. |
| `acare_embedded_interface/` | Python | Bridge between planner commands (`/arm_command`, `/gripper_command`) and hardware. In simulation: FollowJointTrajectory action client to Gazebo controllers. On real hardware: SPI to Teensy 4.1. |
| `acare_admin/` | Python | Staff management CLI: enrol users, manage API keys, run calibration. |
| `models/` | Data | YOLO26 ONNX (`acare_v26.onnx`, 9.8 MB), legacy YOLO11 (`acare_v11.onnx`), training checkpoint (`model.pt`). |
| `simulation/` | Mixed | Gazebo simulation files (WSL Ubuntu 24.04). Not used on Pi. |
| `archive/` | — | Old prototypes and backups. Not deployed. |
| `scripts/` | Shell/Python | Build helpers (`build_workspace.sh`, `launch_validate.sh`), ROS graph validation (`validate_ros_graph.py`, `preflight_ros_env.py`). |
| `camera_configs/` | Data | HP60C encrypted config JSON files. |

---

## 3. File-by-File Breakdown

### acare_msgs/

| File | Description |
|---|---|
| `msg/ArmCommand.msg` | Joint-level arm motion command |
| `msg/AuthRequest.msg` | Authentication request payload |
| `msg/AuthResult.msg` | Authentication result (pass/fail + user ID) |
| `msg/EmergencySignal.msg` | Emergency stop signal |
| `msg/GripperCommand.msg` | Gripper open/close/force command |
| `msg/HandStatus.msg` | Hand detection status for handover |
| `msg/Intent.msg` | Parsed intent (action + tool + confidence) |
| `msg/LogEvent.msg` | Structured audit log entry |
| `msg/MotionFeedback.msg` | Arm/gripper motion feedback from embedded |
| `msg/ProbabilityUpdate.msg` | Bayesian probability map update |
| `msg/RobotState.msg` | Current FSM state broadcast |
| `msg/SafetyAlert.msg` | Graded safety alert (WARNING/ESTOP) |
| `msg/StateTransition.msg` | Requested state transition |
| `msg/Transcript.msg` | Raw speech transcript from ASR |
| `msg/ValidatedIntent.msg` | Auth-verified intent ready for planner |
| `msg/VisionResult.msg` | Object detection + 3D localisation result |
| `msg/VisionSearchRequest.msg` | Request to search for a specific tool |
| `msg/VisionStatus.msg` | Vision pipeline status (searching/found/failed) |
| `srv/EnrolStaff.srv` | Service to enrol a new staff member |

### acare_bringup/

| File | Description |
|---|---|
| `paths.py` | Centralised path constants for all packages |
| `qos_profiles.py` | Per-topic QoS profiles (RELIABLE, BEST_EFFORT, TRANSIENT_LOCAL) |
| `supervisor.py` | Power recovery supervisor (restarts nodes after brown-out) |
| `__init__.py` | Package init |
| `config/system.yaml` | Global system configuration (includes `demo_mode`, `camera.control_overrides`) |
| `config/thresholds.yaml` | Safety and detection thresholds |
| `config/probability_map.yaml` | Bayesian prior for tool locations |
| `launch/acare.launch.py` | Full system launch file |

### acare_voice/

| File | Description |
|---|---|
| `main.py` | Entry point — instantiates VoiceNode and runs standalone loop |
| `voice_node.py` | Master controller: audio state machine, pipeline orchestration |
| `voice_ros_node.py` | ROS2 wrapper — bridges standalone voice pipeline to ROS2 topics (ignores transcripts during ESTOP) |
| `asr.py` | Deepgram Nova-2 streaming WebSocket client |
| `vad.py` | Silero VAD — 32 ms chunks, speech/silence detection |
| `tts.py` | Dual TTS: edge-tts (normal) + pyttsx3 (urgent/fallback) |
| `tts_queue.py` | Priority queue for TTS utterances |
| `tts_cache.py` | Disk cache for pre-generated TTS audio |
| `intent_parser.py` | Groq LLM intent extraction → structured JSON |
| `fast_intent.py` | Regex-based fast intent for common commands (no LLM call) |
| `normaliser.py` | Text cleaning: lowercase, filler strip, punctuation removal |
| `alias_expansion.py` | Alias → canonical tool mapping (e.g. "blade" → "scalpel") |
| `keyword_monitor.py` | Always-on ESTOP keyword thread, 100 ms collision window |
| `assistant_agent.py` | Groq conversational agent for LOGGED_OUT state |
| `dialogue_manager.py` | Multi-turn dialogue state tracking |
| `semantic_turn_detector.py` | Detects turn boundaries using semantic cues |
| `earcons.py` | Non-speech audio cues (beeps, chimes) |
| `state_manager.py` | Local state machine for standalone voice mode |
| `conversation_eval.py` | Conversation quality evaluation utility |
| `README.md` | Package documentation |

### acare_dialogue/

| File | Description |
|---|---|
| `dialogue_node.py` | ROS2 node: subscribes `/raw_transcript`, publishes `/intent_result` (with <0.8 confidence gating) |
| `__init__.py` | Package init |

### acare_auth/

| File | Description |
|---|---|
| `auth_node.py` | ROS2 auth node: orchestrates face + voice verification (ignores in ESTOP, retains intent on drift) |
| `face_detect.py` | MediaPipe face detection (passive scan) |
| `verify_face.py` | InsightFace buffalo_sc face embedding comparison |
| `verify_voice.py` | ECAPA-TDNN ONNX voice embedding comparison |
| `storage.py` | SQLite user database (embeddings, metadata) |
| `export_ecapa_onnx.py` | One-time script to export ECAPA-TDNN to ONNX |
| `__init__.py` | Package init |

### acare_planner/

| File | Description |
|---|---|
| `hw_translator.py` | Maps unified command actions to distinct joint/gripper payloads |
| `state_snapshot.py` | Bounded data context snapshot provided to the LLM agent |
| `task_memory.py` | Short-term memory storing previous tool calls, outcomes, and reasoning |
| `tool_kernel.py` | 6-layer safe tool execution validation boundary. Wires `SafetyKernel` as L0 gate — runs 6-layer validation (ESTOP, workspace bounds, joint limits, consecutive failures, LLM call budget, gripper force anomaly) via `self.node.safety_kernel.evaluate()` before every tool execution. |
| `voice_sync.py` | Synchronises TTS speech output with planner actions |
| `state_manager.py` | 10-state FSM with all valid transitions |
| `planner_node.py` | ROS2 node: full task orchestration from intent to completion |
| `agentic_planner.py` | Primary task orchestration driver: evaluates tools and drives task sequence |
| `agent_schema.py` | Strict 20-line Pydantic model (`ToolCallSchema`) validating LLM output |
| `ik_solver.py` | Analytical 6-DOF inverse kinematics (geometric 2-link + spherical wrist). Loads link lengths + joint limits from system.yaml. FK/IK verified to 0.0000m. |
| `tool_registry.py` | Canonical tool list with physical properties |
| `__init__.py` | Package init |

### acare_safety/

| File | Description |
|---|---|
| `safety_node.py` | ROS2 node: LiDAR zones + MCU telemetry → graded SafetyAlert |
| `__init__.py` | Package init |

### acare_vision/

| File | Description |
|---|---|
| `vision_node.py` | ROS2 orchestrator: coordinates detection, localisation, search |
| `yolo_infer.py` | YOLO26 NMS-free ONNX inference |
| `nbv_search.py` | Bayesian probability map + next-best-view planner |
| `localiser.py` | Depth-to-3D projection with wrist-mounted camera FK: pinhole back-projection + per-pose `T_override` via `compute_T_for_viewpoint()` |
| `hand_tracker.py` | MediaPipe Hands for palm detection during handover (X-axis depth approach + wrist-camera `T_override` transform) |
| `fake_detector.py` | Synthetic detector for testing without camera (with bounding box crash guards) |
| `hp60c_camera_node.py` | HP60C camera driver node (RGB + Depth) |
| `camera_probe.py` | Camera connectivity diagnostic tool |
| `__init__.py` | Package init |

### acare_logging/

| File | Description |
|---|---|
| `log_node.py` | ROS2 node: subscribes `/log_event`, batched SQLite writes, 200 MB rotation |
| `__init__.py` | Package init |

### acare_embedded_interface/

| File | Description |
|---|---|
| `embedded_interface_node.py` | ROS2 node: translates arm/gripper commands to hardware (Gazebo or Teensy) |
| `__init__.py` | Package init |

### acare_admin/

| File | Description |
|---|---|
| `admin_cli.py` | CLI tool with safe YAML parsing for staff enrolment, key management, calibration |
| `admin_node.py` | ROS2 service node for admin operations |
| `__init__.py` | Package init |

### scripts/

| File | Description |
|---|---|
| `build_workspace.sh` | Colcon build helper with symlink-install |
| `launch_validate.sh` | Post-launch validation (checks all nodes alive) |
| `validate_ros_graph.py` | Validates ROS2 topic graph matches expected topology |
| `preflight_ros_env.py` | Pre-flight environment check (ROS2 sourced, deps available) |

---

## 4. ROS2 Topic Map

| Topic | Message Type | Publisher(s) | Subscriber(s) | QoS |
|---|---|---|---|---|
| `/robot_state` | `RobotState` | StateManager | All nodes | TRANSIENT_LOCAL |
| `/state_transition` | `StateTransition` | AuthNode, PlannerNode | StateManager | RELIABLE |
| `/safety_alert` | `SafetyAlert` | SafetyNode, VoiceNode | StateManager, PlannerNode | RELIABLE + TRANSIENT_LOCAL |
| `/emergency_stop` | `EmergencySignal` | VoiceNode, SupervisorNode | EmbeddedInterface, StateManager | RELIABLE |
| `/raw_transcript` | `Transcript` | VoiceNodeROS | DialogueNode, AuthNode | RELIABLE |
| `/intent_result` | `Intent` | DialogueNode | AuthNode | RELIABLE |
| `/auth_request` | `AuthRequest` | DialogueNode | AuthNode | RELIABLE |
| `/validated_intent` | `ValidatedIntent` | AuthNode | DialogueNode, PlannerNode | RELIABLE |
| `/auth_result` | `AuthResult` | AuthNode | StateManager, PlannerNode | RELIABLE |
| `/tts_request` | `String` | StateManager, PlannerNode, AuthNode, DialogueNode | VoiceNodeROS | RELIABLE |
| `/vision_search_request` | `VisionSearchRequest` | PlannerNode | VisionNode | RELIABLE |
| `/vision_result` | `VisionResult` | VisionNode | PlannerNode, DialogueNode | RELIABLE |
| `/vision_status` | `VisionStatus` | VisionNode | PlannerNode | RELIABLE |
| `/hand_status` | `HandStatus` | VisionNode | PlannerNode | RELIABLE |
| `/arm_command` | `ArmCommand` | PlannerNode | EmbeddedInterface | RELIABLE |
| `/gripper_command` | `GripperCommand` | PlannerNode | EmbeddedInterface | RELIABLE |
| `/motion_feedback` | `MotionFeedback` | EmbeddedInterface | PlannerNode, SafetyNode, VisionNode | BEST_EFFORT |
| `/log_event` | `LogEvent` | PlannerNode, VisionNode, SupervisorNode | LogNode | BEST_EFFORT |
| `/scan` | `LaserScan` | LiDAR driver | SafetyNode | BEST_EFFORT |

### Camera Topics

| Topic | Type | Source |
|---|---|---|
| `/ascamera_hp60c/camera_publisher/rgb0/image` | `Image` (BGR8) | HP60C driver |
| `/ascamera_hp60c/camera_publisher/depth0/image_raw` | `Image` (16UC1) | HP60C driver |
| `/ascamera_hp60c/camera_publisher/rgb0/camera_info` | `CameraInfo` | HP60C driver |
| `/ascamera_hp60c/camera_publisher/depth0/camera_info` | `CameraInfo` | HP60C driver |
| `/ascamera_hp60c/camera_publisher/depth0/points` | `PointCloud2` | HP60C driver |

---

## 5. Data Flow — End-to-End Pipeline

**Scenario:** Surgeon says "fetch scissors" → tool delivered to hand.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  1. Mic → VAD (Silero) → Deepgram Nova-2 streaming → raw transcript    │
│  2. Transcript → DialogueNode → normalise → alias expand → intent parse│
│  3. Intent → AuthNode → voice verify → /validated_intent               │
│  4. ValidatedIntent → PlannerNode → state transition to PROCESSING     │
│  5. PlannerNode triggers AgenticPlanner (NIM Nemotron-49B)             │
│  6. AgenticPlanner decides strategy → VisionNode searches for tool     │
│  7. VisionNode → YOLO detect → localise 3D → /vision_result            │
│  8. AgenticPlanner evaluates VisionResult, decides IK target           │
│  9. PlannerNode runs IK solver → /arm_command → EmbeddedInterface      │
│ 10. AgenticPlanner sequences grasp → /gripper_command → grasp          │
│ 11. PlannerNode → state HOLDING → HANDOVER                             │
│ 12. HandoverProtocol: face advisory + palm detection + voice confirm   │
│ 13. Gripper release → state STANDBY                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step-by-step detail:

1. **Mic → VAD → ASR:** Silero VAD detects speech onset. Audio streams to Deepgram Nova-2 via WebSocket. Final transcript emitted on `/raw_transcript`.
2. **Transcript → Intent:** DialogueNode normalises text, expands aliases, then calls Groq 8B for structured intent extraction. Fast intents (ESTOP/confirm) bypass the LLM.
3. **Intent → Auth gate:** AuthNode verifies the speaker (face+voice). On pass, publishes `/validated_intent`.
4. **Agentic Orchestration:** PlannerNode receives the validated intent and hands over control to the `AgenticPlanner` (NIM Nemotron-49B).
5. **Vision search:** The LLM proposes a search strategy (zones, probability map). VisionNode runs YOLO26 inference and 3D localisation. Result published on `/vision_result`.
6. **Agentic Evaluation:** The `AgenticPlanner` receives the vision result, evaluates safety margins, and outputs a strict JSON tool command (e.g. `move_arm`).
7. **Motion planning:** PlannerNode receives the LLM's target, runs the deterministic IK solver to validate reachability, and publishes `ArmCommand`.
8. **Grasp & Handover:** The LLM commands the grasp, checks feedback, and transitions the system to HANDOVER. Handover completes via 3 gates: face (advisory), palm (required), voice (required).

---

## 6. Where Embedded/Hardware Fits

```
┌──────────────────────────────────────────────────────────────────┐
│                    SOFTWARE (Raspberry Pi 5)                       │
│  All ROS2 nodes, AI inference, voice, vision, planning            │
│                                                                    │
│  embedded_interface_node.py  ←── ONLY point of contact            │
└──────────────────┬───────────────────────────────────────────────┘
                   │  SPI (10 MHz SPI0 Bus) + GPIO Interrupt Pin
┌──────────────────▼───────────────────────────────────────────────┐
│                   EMBEDDED (Teensy 4.1)                            │
│  PID motor control, safety ISRs, SPI Slave SPI0, watchdog         │
└──────────────────────────────────────────────────────────────────┘
```

### Boundary rules:

- **Software (Pi 5):** All ROS2 nodes, AI inference (YOLO, LLMs, ECAPA-TDNN), voice pipeline, vision pipeline, task planning, state management.
- **Embedded (Teensy 4.1):** PID motor control loops (1 kHz), hardware safety ISRs (overcurrent, overtemp, limit switches), SPI Slave receiver, local hardware watchdog.
- **`embedded_interface_node`** is the ONLY point of contact between software and firmware. No other node communicates with hardware directly.
- **In simulation:** The interface talks to Gazebo controllers via `FollowJointTrajectory` action client. No serial port needed.
- **On real hardware:** The interface sends serial commands to Teensy and reads telemetry back over the SPI bus (joint positions, currents, temperatures, gripper force).
- **Safety is enforced INDEPENDENTLY on both sides:**
  - Software: `SafetyNode` monitors LiDAR + telemetry, can trigger ESTOP via `/emergency_stop`
  - Firmware: ISRs cut motor power directly on overcurrent/overtemp — no software involvement needed

### 6.1 Raspberry Pi 5 ↔ Teensy 4.1 SPI Communication Protocol (Planned/Pending)

To ensure high-frequency, reliable data exchange, the system architecture plans to replace serial UART/CAN protocols with a direct **SPI (Serial Peripheral Interface)** link between the Raspberry Pi 5 (Master) and the Teensy 4.1 (Slave).
*(Note: This is currently in the hardware planning stage. The actual deployed code in `embedded_interface_node.py` relies solely on Gazebo simulation `ros2_control` endpoints).*

#### 6.1.1 Hardware Wiring & Pin Configuration
Since both devices run on **3.3V logic levels**, no level translation is required. The connections are wired directly on the Raspberry Pi 5 40-pin GPIO header and the Teensy 4.1 pinout:

| Signal | Raspberry Pi 5 GPIO Pin | Teensy 4.1 Pin | Description |
| :--- | :--- | :--- | :--- |
| **MOSI** | Pin 19 (GPIO 10 / SPI0_MOSI) | Pin 11 (MOSI / LPSPI MOSI) | Master Out, Slave In data line |
| **MISO** | Pin 21 (GPIO 9 / SPI0_MISO) | Pin 12 (MISO / LPSPI MISO) | Master In, Slave Out data line |
| **SCLK** | Pin 23 (GPIO 11 / SPI0_SCLK) | Pin 13 (SCK / LPSPI SCK) | Serial Clock line driven by Pi 5 |
| **CS/SS** | Pin 24 (GPIO 8 / SPI0_CE0) | Pin 10 (CS / LPSPI CS) | Active-Low Chip Select line |
| **ATTN (INT)** | Pin 22 (GPIO 25) | Pin 9 (GPIO Output) | Attention interrupt (Teensy $\to$ Pi) |
| **GND** | Pin 25 (GND) | GND | Common ground reference |

*Note: For noise suppression in clinical environments, signal lines are equipped with 33Ω series termination resistors, and the link is routed via a shielded ribbon cable with interleaved ground wires.*

#### 6.1.2 SPI Bus Settings
*   **Clock Frequency**: 10.0 MHz
*   **Mode**: Mode 0 (CPOL = 0, CPHA = 0) — data setup on falling edge, sampling on rising edge.
*   **Bit Order**: MSB (Most Significant Bit) First.
*   **Transmission Mode**: Full-Duplex synchronous 64-byte frame exchanges.

#### 6.1.3 Data Frame Structure (Fixed 64-Byte Payloads)
To ensure deterministic execution, every transaction exchanges a fixed-size 64-byte frame. The frame fields are structured as follows:

##### Command Frame (Pi 5 → Teensy 4.1) — 64 Bytes
1.  **Header (2 Bytes)**: Start-of-frame bytes `0xAA` and `0x55`.
2.  **Sequence ID (1 Byte)**: Monotonically increasing counter for tracking packet arrival.
3.  **Command Type (1 Byte)**: Instruction code:
    *   `0x01` = MOVE (Joint position tracking mode)
    *   `0x02` = GRASP (Force-controlled gripper closure)
    *   `0x03` = RELEASE (Full gripper opening)
    *   `0x04` = ESTOP (Immediate software-halt trigger)
    *   `0x05` = HEARTBEAT (Keepalive ping)
4.  **Target Joint Positions (24 Bytes)**: 6 x `float32` targets in radians (Joints 1 to 6).
5.  **Velocity Scale (4 Bytes)**: `float32` scaling factor (0.0 to 1.0) for planning velocity profiles.
6.  **Acceleration Limit (4 Bytes)**: `float32` acceleration constraint.
7.  **Gripper Force Target (4 Bytes)**: `float32` force limit in Newtons.
8.  **Global System State (1 Byte)**: Active FSM state enum from `state_manager`.
9.  **Reserved / Padding (23 Bytes)**: Space allocated for future commands and alignment.
10. **CRC32 Checksum (4 Bytes)**: CRC calculation of bytes 0–59 to detect transmission corruption.

##### Telemetry Frame (Teensy 4.1 → Pi 5) — 64 Bytes
1.  **Header (2 Bytes)**: Start-of-frame bytes `0xAA` and `0x55`.
2.  **Echo Sequence ID (1 Byte)**: Returns the sequence ID of the corresponding command packet.
3.  **Teensy State (1 Byte)**: Active embedded FSM status (IDLE, POSITION_CONTROL, GRIPPER_CONTROL, ESTOP, FAULT).
4.  **Fault Code (1 Byte)**: Current error code (0 = OK, non-zero matches spec Section III table).
5.  **Current Joint Positions (24 Bytes)**: 6 x `float32` actual joint angles in radians from encoders.
6.  **Current Joint Velocities (24 Bytes)**: 6 x `float32` actual joint velocities in rad/s.
7.  **Gripper Force (4 Bytes)**: `float32` current gripper load cell force in Newtons.
8.  **IMU Pitch/Roll/Yaw (6 Bytes)**: 3 x `int16` scaled orientation values.
9.  **Reserved / Padding (1 Byte)**: Alignment padding.
10. **CRC32 Checksum (4 Bytes)**: CRC calculation of bytes 0–59.

#### 6.1.4 Handshake, Watchdogs, and Safety Interruption Flow
1.  **Direct Memory Access (DMA)**: Teensy 4.1 implements the `LPSPI0` peripheral combined with DMA channels. When Chip Select falls, data is transferred asynchronously in the background. The Teensy's 1 kHz PID controller reads the latest valid SPI frame from DMA double-buffers, avoiding any blockages.
2.  **Safety Watchdog**: Teensy monitors SPI transaction frequency. If a valid packet is not received for $> 200\text{ ms}$, the Teensy watchdog trips, disables all PWM outputs immediately, engages joint brakes, and transitions to local `ESTOP` state.
3.  **Out-of-Band Safety Attention Pin**: If Teensy detects a safety violation (e.g. limit switch hit, overcurrent, or force threshold exceedance) between scheduled SPI polls, it pulls Pin 9 (ATTN) LOW. The Pi 5 intercepts this signal via edge-triggered GPIO interrupts, triggering the `embedded_interface_node` to execute an immediate SPI read cycle and publish an `/emergency_stop` event across ROS2.


---

## 7. LLM Model Allocation

| Component | Provider | Model | Purpose |
|---|---|---|---|
| Dialogue (conversation) | Groq | `llama-3.3-70b-versatile` | Fast user-facing responses |
| Intent parsing | Groq | `llama-3.1-8b-instant` | Simple JSON extraction |
| Agentic planner (primary) | NVIDIA NIM | `nvidia/llama-3.3-nemotron-super-49b-v1` | Primary task orchestration and reasoning |
| Agentic planner (fallback) | Groq | `llama-3.3-70b-versatile` | If NIM unavailable |
| Deterministic fallback | None | Hardcoded logic | If all LLMs fail |

### Fallback chain:

```
NIM Nemotron-49B → Groq 70B → Deterministic hardcoded logic
```

Every LLM decision is validated by Pydantic schema (`agent_schema.py`) before execution. If validation fails, the deterministic fallback is used. The robot never stops on API failure.

---

## 8. Commands Reference

### SSH into Pi
```bash
ssh acare@192.168.1.2
# Password: acare1234
```

### Find Pi IP (if changed)
```powershell
# Quick check
ping 192.168.1.2

# Full subnet scan (PowerShell)
1..254 | ForEach-Object { ping -n 1 -w 50 192.168.1.$_ > $null }; arp -a
```

### Start camera
```bash
cd ~/acare_ws && ros2 launch ascamera hp60c.launch.py
```

### Launch full system
```bash
cd ~/acare_ws && ros2 launch acare_bringup acare.launch.py
```

### Rebuild workspace
```bash
# Note: --symlink-install fails on Pi (filesystem issue). Use plain colcon build.
cd ~/acare_ws && colcon build && source install/setup.bash
```

### Run voice standalone on laptop (no Pi needed)
```powershell
cd c:\Users\Sonali\Desktop\ACARE\acare_software_final\acare_voice
& "C:\Users\Sonali\Desktop\ACARE\.venv\Scripts\python.exe" -u main.py
```

### Shut down Pi
```bash
sudo shutdown now
# Wait for green LED to go dark, then unplug
```

### Transfer files (laptop → Pi)
```powershell
scp "C:\path\to\file" acare@192.168.1.2:~/
```

### Transfer files (Pi → laptop)
```powershell
scp acare@192.168.1.2:/path/on/pi "C:\destination\"
```

### Add WiFi network (safe method — use netplan, NOT nmcli)
```bash
# nmcli is NOT installed on this Pi (uses systemd-networkd + netplan).
# Add via netplan YAML — see Section 1 warnings.
# Only use nmcli if NetworkManager is manually installed.
```

### Check Pi health
```bash
vcgencmd measure_temp    # Temperature
df -h                    # Disk usage
free -h                  # Memory
top                      # CPU load
```

---

## 9. What's Done vs What's Left

### Done ✓

- All 11 ROS2 packages built and importing cleanly on Pi
- Voice pipeline: VAD + Deepgram STT + Groq intent + Edge-TTS confirmed working on laptop
- Vision: YOLO26 detecting objects on Pi at ~850 ms/frame confirmed
- Camera: HP60C RGB+Depth streaming confirmed (640×480, 12.4 Hz)
- Camera intrinsics: real values read from /camera_info (fx=572.04, fy=571.49, cx=329.27, cy=242.09) — applied to system.yaml + localiser
- Auth: full biometric flow implemented, `demo_mode` bypass working (auto-enrols Demo User, no camera needed)
- Embedded interface: Gazebo bridge (FollowJointTrajectory) + real-hardware stub ready
- State machine: 10-state FSM with all transitions
- Safety: LiDAR + telemetry monitoring, graded alerts
- Logging: SQLite audit trail with batched writes
- Bayesian probability map: persistence + clamping
- Handover: 3-gate protocol (face advisory + palm + voice)
- ESTOP: <200 ms keyword detection on dedicated thread (100 ms collision window)
- **IK solver: full analytical 6-DOF solution implemented and tested (FK/IK round-trip error = 0.0000m)**
- **Arm geometry confirmed: link lengths 352/400/400/236mm, all 6 joint limits set**
- **Planner now checks IK reachability — refuses unreachable targets instead of sending clamped poses**
- **SafetyKernel (safety_kernel.py)**: 6-layer validation class wired as L0 gate in `tool_kernel.execute_tool()` — ESTOP, workspace bounds, joint limits, consecutive failures, LLM call budget, gripper force anomaly. `RetryCounters` per-step retry tracking
- **Agentic planner threading**: Uses `ReentrantCallbackGroup` + `MultiThreadedExecutor` + timer-based polling — no daemon threads, ESTOP preemption works naturally
- **Supervisor**: Converted from standalone `supervisor.py` (subprocess `ros2 node list`) to proper ROS2 node `supervisor_node.py` using `self.get_node_names()` ROS2 graph API
- **State machine timing**: EXECUTING transition moved from task-start to first `arm_move` (in `tool_kernel._tool_arm_move()`). HANDOVER phase transition moved from `gripper_close` to `arm_move(PRESENTATION)`
- **Approach rotation**: `arm_approach(SIDE_LEFT/SIDE_RIGHT)` now correctly passes rotation through to IK solver — side-grasp recovery Rung 2 functional
- **QoS**: StateManager's `/robot_state` publisher uses `TRANSIENT_LOCAL` from `qos_profiles` (was hardcoded `qos=10`)
- **Graceful degradation logging**: Every LLM call records tier (NIM/Groq/Deterministic), error reason, latency_ms. `LLM_FALLBACK` LogEvent published on every fallback. 3+ consecutive deterministic → `LLM_DEGRADED` alert with WARNING severity
- **22 bugs fixed** (8 critical, 8 high, 6 medium) across 3 parallel fix passes (2026-06-09)
- **10 additional bugs fixed** (2026-06-11) from fresh line-by-line audit — demo voice confirm, launch ordering, SafetyKernel target_xyz, zones_searched, motion queue, hand_approaching, config error handling, gripper hardware reject, agent_schema logging, workspace loader guards
- **Demo documentation**: `demo_docs.md` created at project root with pre-demo checklist, demo-day script, auth flow, emergency procedures, quick commands reference
- LLM allocation wired: Groq 70B dialogue, Groq 8B intent, NIM Nemotron-49B planner (Groq 70B fallback)
- Assistant agent upgraded: dynamic time/date context, personality, edge-case handling
- Git: secrets removed from history, .gitignore in place
- **State machine: STANDBY→PROCESSING transition added** (planner skips LISTENING when task arrives — was previously rejected by state_manager)
- **Vision simulation bypass**: In demo_mode + no camera, `vision_node` returns scripted detections at fixed tray positions instead of running YOLO
- **Annotated image generation**: `annotate_images.py` in ACARE root — runs YOLO on all .jpg files, saves annotated copies to `ACARE/annotated/`

### Left to do ✗ (mostly hardware-dependent)

**Hardware team must provide:**
- DH twist angles (alpha) for J4/J5/J6 — IK assumes a clean spherical wrist with vertical tool drop. If the real wrist has 90° mounting offsets, these need adding to `system.yaml` arm.dh_params.
- Gearbox ratios for J4/J5/J6 (J2=22:1, J3=15:1 already known)
- Teensy firmware: SPI slave (752 lines, complete) for `embedded_interface_node` to talk to
- Real arm assembly + motor wiring

**Pending Software Implementations (to be built):**
- Automated LiDAR calibration routine in `admin_cli.py` (baseline laser scan for reference map).
- Voice-driven autonomous registration (P1)
- BehaviorTree integration (P3, optional)

**Calibration (after arm + camera mounted):**
- **Wrist-mounted camera flange offset** `T_flange_camera` — measure the physical offset from the wrist flange to the camera lens centre (default: 40mm forward, 20mm below). Write to `system.yaml camera.T_flange_camera`.
- Camera intrinsics are auto-loaded from the HP60C driver's `/camera_info` topic at runtime — no checkerboard calibration needed.
- Camera-to-robot extrinsics are computed dynamically per arm pose via forward kinematics (`compute_T_for_viewpoint()`), using the known joint angles at each NBV viewpoint or handover pose. The static `T_robot_camera` in `system.yaml` is retained only as a fallback for table-mounted camera setups.
- `safe_drop_zone` and `handover_zone` coordinates (currently estimated)
- `neutral_joint_angles` (home pose)

**Procurement / setup:**
- USB sound card for Pi mic input (3.5 mm analog mic won't work on Pi directly)
- NVIDIA NIM API key (planner falls back to Groq if absent — not blocking)
- Production `.env` with real keys on Pi
- ECAPA-TDNN ONNX export (run `export_ecapa_onnx.py` once on a dev machine with speechbrain)

**Testing:**
- Depth localisation verified with wrist-mounted HP60C (stable mount on gripper assembly — sparse depth issue from hand-holding resolved)
- Full end-to-end integration test with all nodes running simultaneously on Pi

### Tray Placement Constraint (from IK analysis)

The instrument tray must sit **0.40–0.55 m from the base**. Closer than ~0.40m forces the elbow past its -120° limit (the arm can't fold tight enough to drop the tool straight down). Max reach is 0.80m but practical top-down grasp range is 0.40–0.55m.

**Workspace Configuration:**
- **Software limit (system.yaml):** x/y ±0.60m, z 0.0-0.75m
- **IK solver safety envelope:** x/y ±0.85m, z -0.10-0.85m (backstop validation)
- **Practical top-down grasp range:** 0.40-0.55m from base (elbow limit constraint)

---

## 10. Safety Architecture

### ESTOP Keyword Detection
- Always-on dedicated thread (never blocked by other processing)
- 100 ms collision window (debounce)
- <200 ms end-to-end latency from utterance to motor stop
- Uses `pyttsx3` (offline, instant) for emergency speech — never edge-tts

### LiDAR Proximity Zones
| Distance | Zone | Action |
|---|---|---|
| > 600 mm | SAFE | Normal operation |
| 400–600 mm | WARNING | Reduce speed, alert operator |
| < 400 mm | ESTOP | Immediate halt, cut motor power |

### Gripper Force
- Software ESTOP backstop at **15 N**
- Software warns at **10 N** (publishes SafetyAlert)

### Joint Current
- Software ESTOP at **8.0 A**
- Software warns at **6.0 A**

### Joint Temperature
- Software ESTOP at **75.0 °C**
- Software slows motion at **65.0 °C**
- Software warns at **55.0 °C**

### Logout Guard
- Logout rejected from states: `EXECUTING`, `HOLDING`, `HANDOVER`
- Prevents tool drop during active manipulation

### Handover Safety
- Face detection is **advisory only** (never aborts alone)
- Palm detection + voice confirmation are **required** gates
- Both must pass before gripper release

### LLM Safety
- Every LLM proposal validated by Pydantic schema before execution
- Invalid schema → deterministic fallback (hardcoded logic)
- Robot **never stops** on API failure — always falls through to safe behaviour

### Dual-Layer Safety
- **Software layer** (Pi): SafetyNode monitors LiDAR + telemetry, publishes graded alerts
- **Firmware layer** (Teensy): ISRs cut motor power directly on overcurrent/overtemp
- Both layers operate independently — either can trigger ESTOP without the other

---

## 10.5 Edge Cases & Network Failures — System Decisions

**Deepgram API Drop:**
```
voice_node detects WebSocket disconnect.
3 retries: exponential backoff (500ms, 1s, 2s).
All fail:
  TTS (pyttsx3 local): "Voice service unavailable."
  If holding object: safe_deposit() → ESTOP.
  Else: State → STANDBY.
  Log: NETWORK_FAIL.
Session preserved. User does not need to re-login on reconnect.
```

**Groq API / NVIDIA NIM Drop:**
```
planner's _call_llm() catches exception → returns None.
Deterministic fallback activates immediately.
Task continues on deterministic path.
No task abort purely from API failure.
```

**Holding Object When Network Fails:**
```
NETWORK_FAIL_HOLD_THRESHOLD_S = 5.0 (from system.yaml)
Timer starts when network_ok goes False during HOLDING or HANDOVER state.
If restored within 5s: continue normally.
If not restored: safe_deposit() → ESTOP.
TTS (pyttsx3): "Network unavailable. Stopping safely."
Log: NETWORK_FAIL.
```

**Person Enters Danger Zone (< 400mm LiDAR) During Motion:**
```
safety_node publishes SafetyAlert severity=ESTOP.
planner._on_safety_alert() fires.
_handle_estop() called.
If holding: safe_deposit() first (controlled move to drop zone).
Then ESTOP sent to MCU → PWM disabled.
TTS (pyttsx3): "Emergency stop. Person detected in safety zone."
Log: LIDAR_ESTOP.
```

**Tool Placed in Unexpected Position (NBV Search Misses It):**
```
All 3 search attempts fail.
On attempt 2: robot asks "Can you confirm it is on the tray?"
Staff confirms: robot searches once more from scratch (uniform).
Still not found after 3 total: "I was unable to find the {tool}.
Please check the tray or use manual procedure."
State → STANDBY. Probability map not updated.
```

**IK Unsolvable for All Candidates:**
```
All 3 IK attempts fail (alternate orientation + next candidates exhausted).
TTS: "Unable to reach the {tool}. Please reposition it and try again."
Arm returns to neutral.
State → STANDBY.
Log: IK_FAIL.
```

**Handover Timeout (30s Exceeded):**
```
TTS: "No collection detected. Returning {tool} to tray."
Arm moves to SAFE_DROP_ZONE at velocity_scale=0.3.
RELEASE gripper.
Log: HANDOVER_TIMEOUT.
State → STANDBY.
Probability map not updated.
Inactivity timer resets.
```

**Power Failure During Task:**
```
On reboot:
  Check probability_map.yaml.tmp: if exists → incomplete write → delete, load .yaml.
  Read last event_type from SQLite.
  If last state was EXECUTING or HOLDING:
    Move arm slowly to neutral (velocity_scale=0.3).
    TTS: "System recovered from unexpected shutdown. Please verify workspace."
    Log: POWER_RECOVERY.
  Else: normal startup.
```

**Physical ESTOP Button Pressed:**
```
Motor driver enable pin cut at hardware level → immediate PWM off.
No software path. No controlled deposit possible.
Object remains in gripper if held at time of press.
Staff must manually retrieve object.
Pi detects MCU entered ESTOP via status feedback.
TTS (pyttsx3): "Emergency stop. Manual reset required."
Log: HARD_ESTOP.
State → ESTOP.
Admin required to resume.
```

---

*Last updated: 2026-06-09 — Full documentation update reflecting SafetyKernel wiring, agentic planner threading (ReentrantCallbackGroup + MultiThreadedExecutor), supervisor_node.py conversion, state machine timing fixes, approach rotation, QoS fixes, graceful degradation logging, and 22 bug fixes across 3 fix passes.*

---

## 24. Fixed Bugs & Remaining Items
*(All 22 bugs identified in the comprehensive audit have been fixed across 3 parallel fix passes)*

### ✅ Fixed — Critical (8/8)
- [x] **planner_node.py (SyntaxError):** Fix duplicate `joint_angles` keyword arguments when instantiating `ArmCommand`. — **FIXED**
- [x] **planner_node.py (TypeError):** Fix `task_memory.save_outcome()` call to include all 4 required arguments. — **FIXED**
- [x] **voice_ros_node.py (Safety):** Port the ESTOP final-transcript backstop logic from standalone `voice_node.py`. — **FIXED**
- [x] **voice_ros_node.py (Safety):** Trigger offline `pyttsx3` emergency announcement during ESTOP. — **FIXED**
- [x] **auth_node.py (Security Bypass):** Enforce ECAPA-TDNN background embedding similarity check during voice re-verification. — **FIXED**
- [x] **safety_node.py (Throttle Bypass):** Fix throttle dictionary key — rapidly alternating alerts no longer bypass 1-sec throttle. — **FIXED**
- [x] **dialogue_node.py (Loop Trap):** Remove "scalpel" from dialogue prompts. — **FIXED**
- [x] **fast_intent.py (Regex Strictness):** Relax regex anchors so commands like "please stop" are properly matched. — **FIXED**

### ✅ Fixed — High (8/8)
- [x] **embedded_interface_node.py (QoS):** Fix hardcoded QoS depth=10 for `/robot_state` to properly use `TRANSIENT_LOCAL` latching. — **FIXED**
- [x] **state_manager.py (Logout Desync):** Fix desync where saying "logout" clears local ID but FSM rejects transition if holding a tool. — **FIXED**
- [x] **supervisor.py (Race Condition):** Resolved by converting to proper ROS2 node (`supervisor_node.py`) with graph API monitoring. — **FIXED**
- [x] **admin_cli.py (Config Rewrite):** Fix `yaml.dump()` rewriting to preserve inline comments. — **FIXED**
- [x] **vision_node.py (Camera Driver):** Correctly instantiate `HP60CCameraNode` using `__init__`. — **FIXED**
- [x] **Gripper force handling in sim mode:** Properly handles force when running in simulation. — **FIXED**
- [x] **abort non-blocking:** Abort implements 5s timeout for non-blocking exit. — **FIXED**
- [x] **Tool lists unified:** All tool lists now use `ToolRegistry` as single source of truth. — **FIXED**

### ✅ Fixed — Medium (6/6)
- [x] **detect_face fixed:** Properly handles non-demo mode with actual camera. — **FIXED**
- [x] **Silent fallbacks:** Fixed silent fallback paths in LLM pipeline. — **FIXED**
- [x] **ESTOP backstop port:** Final-transcript ESTOP backstop ported to voice_ros_node. — **FIXED**
- [x] **hw_translator validation:** Added input validation to hw_translator. — **FIXED**
- [x] **Camera sync threshold:** Fixed camera synchronization timeout threshold. — **FIXED**
- [x] **sleep→polling:** Replaced blocking sleep loops with polling patterns. — **FIXED**
- [x] **Per-task cleanup:** State is properly reset at task boundaries. — **FIXED**

### 🚧 Remaining Implementation Gaps / To Be Implemented
- [ ] **AUTO Zone Querying:** `planner_node.py` strips the `AUTO` zone argument and passes `[]` to the vision node. Ensure the Bayesian map is actually queried with the LLM's requested zone.
- [ ] **Memory Compression:** Memory compression is implemented in `state_snapshot.py` but missing from `task_memory.py`.
- [ ] **Handover Height Sync:** Standardize variable names (`handover_z_offset` in `task_memory.py` vs `handover_height` in `state_snapshot.py`).
- [ ] **Document Advanced Features:** Officially document the Adaptive Low-Light Enhancement pipeline, asynchronous camera parameter probing, and NBV wrist-offset micro-movements.
- [ ] **Taxonomy Reconciliation:** Ensure the documentation only reflects the actual 6 classes detected by YOLO26, not 8.
- [ ] **LiDAR Thresholds:** Resolve the discrepancy in LiDAR warning distances between code (<600mm) and docs (400-600mm).
- [ ] **Verbal Adjustments:** Document the verbal handover height adjustment ("lower"/"higher") and the verbal enrolment abortion ("cancel") features.

## 11. Pi Hardware & SDK Details

### Camera SDK Location
```
~/HP60C_ROS/EaiCameraSdk_v1.2.28.20241015/demo/linux_ros/
```

### Camera Config Files
```
~/acare_ws/ascamera/configurationfiles/
```
**Important:** The camera launch MUST be run from `~/acare_ws/` so it finds this path.

### Camera Confirmed Specs
- RGB: 640×480 BGR8 @ 12.4 Hz
- Depth: 640×480 16UC1 @ 12.4 Hz
- Valid depth range: 200–4000 mm
- Real intrinsics (from driver): fx=572.04, fy=571.49, cx=329.27, cy=242.09

### Arm Geometry (confirmed from CAD + hardware team)

| Link | Length | Description |
|---|---|---|
| base_height | 352 mm | J1 axis → J2 shoulder |
| upper_arm | 400 mm | J2 shoulder → J3 elbow |
| forearm | 400 mm | J3 elbow → J4 wrist |
| wrist+tool | 236 mm | J4 → tool tip (TCP) |

**Max reach:** 800 mm. **Practical top-down grasp range:** 400–550 mm from base.

| Joint | Limit | Gearbox |
|---|---|---|
| J1 base | ±180° | — |
| J2 shoulder | ±135° | 22:1 |
| J3 elbow | ±120° | 15:1 |
| J4 wrist_1 | ±180° | TBD |
| J5 wrist_2 | ±180° | TBD |
| J6 wrist_3 | ±180° | TBD |

**Motor torque requirements** (from sizing table): J1=10.5, J2=42.5, J3=54.4, J4=156.7, J5=263.65 kg·cm. J5 needs the strongest motor.

**Gripper:** parallel-jaw with rubber pads, linear-actuator driven. HP60C camera mounts on top of the gripper assembly.

### Pi Setup History
- Ubuntu Server 24.04.4 LTS (64-bit, aarch64)
- ROS2 Jazzy (`ros-jazzy-ros-base`)
- All acare_ws packages built (11 acare packages + ascamera)
- Python deps: deepgram-sdk, groq, pyttsx3, mediapipe, onnxruntime, sounddevice, edge-tts, silero-vad, pydantic, PyYAML, opencv-python-headless
- HP60C camera SDK extracted and configured
- `unattended-upgrades` disabled (prevents background apt from dropping SSH)
- `needrestart` masked
- PortAudio + ALSA utils installed

### Pi Mic Situation
- The Pi 5 3.5mm jack is **output only** — no mic input
- A **USB sound card adapter** is required for the 3.5mm condenser mic
- Until then, voice pipeline can be tested standalone on the laptop

### Waveshare 5" HDMI LCD (H) — Using as Monitor
- 800×480 capacitive touch, HDMI + USB connection
- Pi 5 needs a **micro-HDMI to full-size HDMI** cable/adapter
- USB cable provides touch input + power to the screen
- Add to `/boot/firmware/config.txt`:
  ```
  hdmi_force_hotplug=1
  hdmi_group=2
  hdmi_mode=87
  hdmi_cvt=800 480 60 6 0 0 0
  hdmi_drive=1
  ```
- Add `nomodeset` to end of `/boot/firmware/cmdline.txt` (fixes Ubuntu 24.04 black screen)
- Screws/standoffs in the box are for mounting screen directly onto Pi (optional — can use separate)
- Useful for: local terminal access without SSH, admin CLI, status monitoring

---

## 12. Running Voice Pipeline Standalone (Laptop)

For testing without the Pi (no USB mic on Pi yet).

### Prerequisites
```powershell
cd C:\Users\Sonali\Desktop\ACARE
uv pip install silero-vad sounddevice "deepgram-sdk==3.10.1" groq edge-tts pyttsx3 pygame python-dotenv numpy torch torchaudio soundfile
```

### .env file
Must exist at `acare_software_final\.env`:
```
DEEPGRAM_API_KEY=<your_key>
GROQ_API_KEY=<your_key>
NVIDIA_NIM_API_KEY=<your_key>  (optional — planner falls back to Groq if missing)
```

### Run
```powershell
cd c:\Users\Sonali\Desktop\ACARE\acare_software_final\acare_voice
& "C:\Users\Sonali\Desktop\ACARE\.venv\Scripts\python.exe" -u main.py
```

### What it tests
- Silero VAD (voice activity detection from laptop mic)
- Deepgram Nova-2 streaming STT
- Groq Llama 3.3 70B (assistant conversation)
- Edge-TTS (text-to-speech output)
- Keyword monitor (ESTOP detection)
- State machine transitions

### Troubleshooting
- `ModuleNotFoundError` → wrong Python. Must use `.venv` Python, not system.
- Groq 401 error → API key expired. Regenerate at console.groq.com/keys
- `[VAD] SoundDevice Status: input overflow` → normal on first start
- Deepgram timeout → internet connection issue or key expired

---

## 13. Important Warnings

- **⚠️ NEVER edit `/etc/netplan/*.yaml` over SSH.** Previous attempt corrupted the config and required a full reflash.
- **⚠️ Always `sudo shutdown now` before unplugging.** Pulling power corrupts the SD card.
- **⚠️ deepgram-sdk must be pinned to 3.10.1.** Version 4+ changed import paths and breaks `asr.py`.
- **⚠️ numpy must be <2 on Pi.** System matplotlib (used by mediapipe) is built against numpy 1.x.
- **⚠️ colcon build --symlink-install fails on Pi.** Use plain `colcon build`. The symlink flag causes ENFILE errors on the Pi's filesystem.
- **⚠️ nmcli is NOT installed on this Pi.** It runs systemd-networkd + netplan, not NetworkManager. `nmcli` commands will fail with "command not found".
- **⚠️ Elechouse VR V3 voice module is incompatible with ACARE.** It returns pre-trained command IDs via UART, not raw PCM audio. Cannot feed into Deepgram. Requires USB sound card adapter for mic input on Pi.

---

## 14. ACARE Software — Complete Module-by-Module Feature Guide

**Autonomous Clinical Assistance Robot (ACARE)** is a voice-controlled robotic system designed for operating theatre environments. It autonomously fetches sterile surgical instruments for authenticated surgical staff using a 6-DOF robotic arm, AI-driven perception (YOLO object detection, MediaPipe hand tracking, InsightFace face verification, ECAPA-TDNN voice verification), large language models (NVIDIA NIM Nemotron-49B / Groq Llama) for reasoning and recovery, and a ROS2-based distributed architecture with 11 interconnected packages and an 10-state finite state machine.

---

### 14.1 acare_msgs/ — ROS2 Message & Service Definitions

**Type:** CMake package | **Path:** `acare_software_final/acare_msgs/`

Defines the typed contract between every ROS2 node. 18 `.msg` files + 1 `.srv` file.

**Messages (18):**
| Message | Fields | Purpose |
|---|---|---|
| `ArmCommand.msg` | command, joint_angles[6], velocity_scale, accel_limit, blocking | Joint-level arm motion command from planner to embedded interface |
| `AuthRequest.msg` | request_type, transcript, tool, confidence | Authentication/authorisation request from dialogue to auth |
| `AuthResult.msg` | user_id, name, role, success, face_verified, face_confidence, voice_confidence | Authentication result broadcast to all nodes |
| `EmergencySignal.msg` | reason, source | Emergency stop signal — highest priority message |
| `GripperCommand.msg` | command (GRASP/RELEASE), force_target | Gripper open/close/force command |
| `HandStatus.msg` | hand_detected, is_open, palm_up, x, y, z, confidence | Hand detection status for handover (MediaPipe-output) |
| `Intent.msg` | tool, action, destination, confidence | Parsed intent from dialogue/voice pipeline |
| `LogEvent.msg` | event_type, user_id, tool, state, description, timestamp, voice_e2e_ms, vision_search_ms, motion_ms, total_task_ms, safety_severity | Structured audit log entry |
| `MotionFeedback.msg` | success, phase, error, joint_positions[], joint_velocities[], joint_currents[], temperatures[], gripper_force, imu_roll, imu_pitch, imu_yaw | Arm/gripper motion feedback from embedded interface. **Note:** Arrays are not size-constrained; includes joint_velocities field not in original spec. |
| `ProbabilityUpdate.msg` | zone, tool, new_probability | Bayesian probability map update |
| `RobotState.msg` | state (string), active_user_id | Current FSM state broadcast (TRANSIENT_LOCAL) |
| `SafetyAlert.msg` | severity (WARNING/CRITICAL/ESTOP), reason, source | Graded safety alert |
| `StateTransition.msg` | target_state, reason | Requested state transition |
| `Transcript.msg` | text, is_final, pcm16, sample_rate_hz | Raw speech transcript from ASR (includes audio for voice verification) |
| `ValidatedIntent.msg` | tool, action, user_id, name, authenticated | Auth-verified intent ready for planner |
| `VisionResult.msg` | found, tool, x, y, z, confidence, zone, candidates_json[] | Object detection + 3D localisation result |
| `VisionSearchRequest.msg` | tool, reset_probability_map, priority_zones[] | Request to search for a specific tool |
| `VisionStatus.msg` | status (LOADING/READY/ERROR/SEARCHING) | Vision pipeline status |

**Services (1):**
| Service | Request | Response | Purpose |
|---|---|---|---|
| `EnrolStaff.srv` | name, role | success, staff_id, message | Enrol a new staff member with biometric capture |

---

### 14.2 acare_bringup/ — Shared Infrastructure

**Type:** Python package | **Path:** `acare_software_final/acare_bringup/`

Centralised configuration and infrastructure used by every other package.

**Files (6):**

**`paths.py`** — Single source of truth for all file paths:
- `REPO_ROOT`, `CONFIG_DIR`, `LOG_DIR`, `MODEL_DIR`
- `SYSTEM_YAML`, `THRESHOLDS_YAML`, `PROBABILITY_MAP_YAML`, `USERS_DB`
- `ensure_parent()` helper for creating parent directories

**`qos_profiles.py`** — Centralised QoS policies (spec-mandated):
- `TOPIC_SENSOR` — BEST_EFFORT depth=1 (motion feedback, LiDAR scan)
- `TOPIC_COMMAND` — RELIABLE depth=10 (arm/gripper/emergency commands)
- `TOPIC_STATE` — RELIABLE + TRANSIENT_LOCAL depth=1 (robot state, transitions, safety alerts)
- `TOPIC_LOGGING` — BEST_EFFORT depth=10 (log events — loss acceptable)
- `TOPIC_VISION` — RELIABLE depth=10 (vision results, search requests, status)
- `TOPIC_VOICE_PIPELINE` — RELIABLE depth=10 (transcripts, intents, auth results)
- `TOPIC_TTS` — RELIABLE depth=10 (TTS requests)

**`supervisor_node.py`** — ROS2 node for crash recovery & power recovery monitoring:
- Proper ROS2 node using `rclpy` — runs as part of the ROS2 stack alongside all other nodes
- Monitors all 10 ROS2 nodes every 5 seconds via `self.get_node_names()` (ROS2 graph discovery API)
- Auto-restart nodes: `log_node`, `admin_node`, `dialogue_node`, `voice_node`, `auth_node`
- Critical nodes (no auto-restart, triggers ESTOP via `/emergency_stop` publisher): `safety_node`, `embedded_interface_node`, `state_manager`, `planner_node`, `vision_node`
- **Power recovery** (Spec Section XVII): On boot, checks last logged state from SQLite. If last state was EXECUTING/HOLDING/HANDOVER, publishes a safe transition to STANDBY + TTS warning
- **ESTOP trigger** uses direct publisher on `/emergency_stop` topic (no subprocess `ros2 topic pub`)

**Config Files (3):**

**`config/system.yaml`** (109 lines) — Central system configuration:
- `robot.workspace` — Reachable envelope: x/y ±0.60m, z 0–0.75m
- `robot.safe_drop_zone` — (0.0, 0.35, 0.05) [PLACEHOLDER]
- `robot.handover_zone` — (0.0, 0.40, 0.10) [PLACEHOLDER]
- `arm.link_lengths` — base 0.352m, upper_arm 0.400m, forearm 0.400m, wrist 0.236m
- `arm.joint_limits_min/max` — All 6 joints in radians
- `arm.kiosk_rest_joint_angles` — [0.0, 0.15, -0.35, 0.0, 0.10, 0.0]
- `arm.kiosk_interaction_joint_angles` — [0.0, -0.10, -0.05, 0.0, -0.05, 0.0]
- `arm.control_soft_limits` — velocity (90%), current (0.5A margin), temperature (5°C margin), gripper force (90%)
- `camera` — HP60C intrinsics auto-loaded from driver: fx=572.04, fy=571.49, cx=329.27, cy=242.09; wrist-mounted extrinsics computed dynamically via FK + `T_flange_camera` (40mm forward, 20mm below flange); static `T_robot_camera` retained as table-mount fallback
- `vision` — Model path, confidence threshold (0.70), low-light thresholds, gamma correction, capture_settle_ms=120, wrist micro-offsets
- `voice` — TTS engine stack (edge_tts → kokoro_onnx → pyttsx3), estop_keywords, timeout values
- `auth` — voice/threshold (0.85), face threshold (0.78), enrol_voice_samples=3, enrol_face_frames=10, face_verify_z=0.70m
- `demo_mode: true`

*Example configuration:*
```yaml
robot:
  workspace:
    xmin: -0.4  xmax: 0.4
    ymin: -0.3  ymax: 0.3
    zmin:  0.0  zmax: 0.5
  safe_drop_zone: {x: 0.0, y: 0.35, z: 0.05}
  handover_zone: {x: 0.0, y: 0.4, z: 0.1}
  handover_height_adjustment_m: 0.05

vision:
  model_path: '/models/yolo_int8.onnx'
  confidence_threshold: 0.7
  low_light_confidence_threshold: 0.56
  low_light_brightness_cutoff: 80

voice:
  use_groq: true
  use_deepgram: true
  use_edge_tts: true
  edge_tts_voice: 'en-IN-Wavenet-D'
  tts_fallback: kokoro_onnx
  tts_safety: pyttsx3
  network_fail_hold_threshold_seconds: 5
  session_inactivity_timeout_seconds: 300
  session_hard_ttl_seconds: 7200
  handover_timeout_seconds: 30
  estop_keywords: [stop, halt, emergency, abort, ruko, bas]
  tts_rate: 150

auth:
  similarity_threshold: 0.85
  face_similarity_threshold: 0.78
  require_liveness: true
  voice_drift_consecutive_threshold: 3

planner:
  max_retries: 3
  agentic_model: "nvidia/llama-3.3-nemotron-super-49b-v1"        # primary (NVIDIA NIM)
  agentic_fallback_model: "openai/gpt-oss-120b"                   # Groq fallback when NIM unavailable
  intent_model: "llama-3.1-8b-instant"
  assistant_model: "llama-3.1-8b-instant"
```

**`config/thresholds.yaml`** (18 lines) — Safety thresholds:
- current_limit_A: 8.0, current_warning_A: 6.0
- temperature_estop_C: 75.0, temperature_slow_C: 65.0, temperature_warning_C: 55.0
- velocity_limit_degs: 120, velocity_operational_degs: 80
- lidar_caution_mm: 600, lidar_stop_mm: 400
- gripper_force_limit_N: 15.0, gripper_force_warning_N: 10.0
- fake_detection — texture_variance_threshold: 120.0, depth_variance_threshold: 0.002

*Example configuration:*
```yaml
safety:
  current_limit_A: 8.0
  current_warning_A: 6.0
  temperature_slow_C: 65.0
  temperature_estop_C: 75.0
  temperature_warning_C: 55.0
  velocity_limit_degs: 120.0
  velocity_operational_limit_degs: 80.0
  lidar_caution_mm: 600
  lidar_stop_mm: 400
  gripper_force_limit_N: 15.0
  gripper_force_warning_N: 10.0

fake_detection:
  texture_variance_threshold: 120.0  # calibrated empirically
  depth_variance_threshold: 0.002    # calibrated empirically
```

**`config/probability_map.yaml`** (30 lines) — Bayesian priors for tool placement across 3 zones (A=left, B=centre, C=right), 6 tool classes, values sum to 1.0 per zone

*Example admin-defined prior:*
```yaml
zone_A:
  scalpel: 0.4
  scissors: 0.2
zone_B:
  scissors: 0.5
  forceps: 0.3
zone_C:
  gauze: 0.7
  plaster: 0.6
```
All probability values are clamped to [0.05, 0.90] after every Bayesian update to prevent saturation.

**`launch/acare.launch.py`** — Launches **11 ROS2 nodes** (10 core + supervisor_node):
`voice_node` → `dialogue_node` → `auth_node` → `state_manager` → `planner_node` → `embedded_interface_node` → `vision_node` → `safety_node` → `log_node` → `admin_node`

**Note:** The `supervisor_node.py` (crash recovery & power recovery) is a ROS2 node and is launched by `acare.launch.py` alongside the other 10 nodes.

---

### 14.3 acare_voice/ — Voice Pipeline (Speech-to-Intent)

**Type:** Python package | **Path:** `acare_software_final/acare_voice/`

The voice pipeline processes microphone audio through a sequential chain: VAD → ASR → Normaliser → Alias Expansion → Intent Parser → Dialogue Manager → Execution. Also includes TTS output and keyword-based ESTOP detection.

**Files (17):**

| File | Class(es) / Functions | Lines | Purpose |
|---|---|---|---|
| `main.py` | `main()` | 451+ | Entry point — instantiates VoiceNode and runs standalone loop |
| `voice_node.py` | `VoiceNode` | 451 | Master orchestrator: audio state machine, pipeline coordination, callback wiring |
| `voice_ros_node.py` | `VoiceNodeROS` | — | ROS2 wrapper — bridges standalone pipeline to ROS2 topics |
| `vad.py` | `VADListener` | 122 | Silero VAD — 32ms chunks, 0.5s min speech, 0.8s silence timeout → flush |
| `asr.py` | `ASRClient` | 279 | Deepgram Nova-2 streaming WebSocket client with reconnect logic |
| `tts.py` | `speak()`, `speak_urgent()` | 120 | Dual TTS: edge-tts normal, pyttsx3 urgent/fallback |
| `tts_queue.py` | `TTSQueue` | 305 | Priority queue (URGENT/NORMAL/BACKCHANNEL), barge-in, echo avoidance, 3-tier fallback (edge-tts → kokoro_onnx → pyttsx3) |
| `tts_cache.py` | — | — | Disk cache for pre-generated TTS audio |
| `intent_parser.py` | `parse_intent()` | 80 | Groq Llama 3.1 8B intent extraction → structured JSON |
| `fast_intent.py` | `parse_fast_intent()`, `is_simple_command()` | 165 | Regex-based fast intent — ESTOP, resume, confirm, reject, cancel, follow-up, multi-tool detection |
| `normaliser.py` | `normalise()`, `get_multi_tool_prompt()` | 169 | Text cleaning: lowercase, filler strip, punctuation removal, alias expansion, multi-tool detection |
| `alias_expansion.py` | `expand_aliases()`, `detect_aliases_in_transcript()` | 244 | Alias → canonical tool mapping with word-boundary matching and ambiguity detection |
| `keyword_monitor.py` | `KeywordMonitor` | 137 | Always-on ESTOP keyword detection (dedicated thread, 100ms collision window, continuation-word cancellation) |
| `assistant_agent.py` | `AssistantAgent` | 278 | Groq Llama 3.3 70B conversational agent for LOGGED_OUT state |
| `dialogue_manager.py` | `DialogueManager`, `DialogueContext` | 157 | Multi-turn dialogue state, confirmation handling, follow-up resolution, tool history (last 10) |
| `semantic_turn_detector.py` | — | — | Detects turn boundaries using semantic cues |
| `earcons.py` | `play_*()` | 90 | Non-speech audio cues: listen_start (1200Hz beep), turn_ready (ding), confirm (chime), error (buzz), estop (440Hz beep) |
| `state_manager.py` | `StateManager`, `SystemState` | 153 | Standalone voice state machine: IDLE → LISTENING → PROCESSING → RESPONDING → CLARIFYING → CONFIRMED → ASSISTING → ESTOP → ERROR |
| `conversation_eval.py` | — | — | Conversation quality evaluation utility |
| `README.md` | — | — | Package documentation (note: file not present in current repo) |
| `package.xml`, `setup.py`, `setup.cfg` | — | — | ROS2 package metadata |

**Voice Pipeline (end-to-end data flow):**
1. **VAD** (Silero, 32ms chunks, sample rate 16kHz) detects speech → streams audio to ASR
2. **ASR** (Deepgram Nova-2, `en-IN`, `endpointing=300ms`, `utterance_end_ms=1000`) → produces final transcript
3. **Normaliser** strips fillers ("um", "uh"), polite markers ("can you"), punctuation; detects multi-tool requests via conjunction/negation analysis
4. **Alias Expansion** maps user aliases to canonical tools ("blade" → "scalpel", "pulse ox" → "oximeter") with word-boundary regex
5. **Fast Intent** regex engine checks for ESTOP/resume/confirm/reject/cancel/fetch patterns first (bypasses LLM)
6. **Intent Parser** (Groq Llama 3.1 8B, structured JSON output) extracts `{tool, action, confidence}`
7. **Dialogue Manager** handles multi-turn: confirmation loops, follow-up resolution, pronoun resolution
8. **TTS Queue** speaks responses with 3-tier fallback (edge-tts cloud → kokoro_onnx offline → pyttsx3 emergency)

**ESTOP Keyword Detection:**
- 6 keywords: `stop`, `halt`, `emergency`, `abort`, `ruko`, `bas`
- 100ms collision window (debounce) per spec
- Continuation-word cancellation ("stop moving" ≠ ESTOP)
- Backstop ESTOP detection on final transcripts (short utterances ≤2 words)
- Dedicated thread, <200ms end-to-end latency

**TTS Fallback Chain (spec-mandated):**
1. Edge TTS (`en-IN-NeerjaNeural`) — cloud-based, high quality, Indian English
2. Kokoro ONNX INT8 (`af_heart`) — offline fallback, 82M params, local inference
3. pyttsx3 — emergency fallback, offline, always available

---

### 14.4 acare_dialogue/ — ROS2 Dialogue Node

**Type:** Python package | **Path:** `acare_software_final/acare_dialogue/`

**Files (1):**

**`dialogue_node.py`** (187 lines) — `DialogueNode` ROS2 node:
- **Subscribes:** `/raw_transcript` (Transcript), `/robot_state` (RobotState), `/validated_intent` (ValidatedIntent), `/vision_result` (VisionResult)
- **Publishes:** `/intent_result` (Intent), `/auth_request` (AuthRequest - only for login prompts), `/tts_request` (String)
- **Pronoun resolution** — resolves "it", "that", "the same one" from conversation context
- **Session memory** — tools_fetched list, conversation_history (last 20 turns with summarization), current_task tracking
- **Clarification** — ambiguous tool requests prompt user, pending_clarification state with fallback
- **Assistant fallback** — when in LOGGED_OUT state, delegates to AssistantAgent for conversation
- **Multi-tool detection** — detects `and`/`plus`/`then` connected tool names, asks user to choose

---

### 14.5 acare_auth/ — Biometric Authentication

**Type:** Python package | **Path:** `acare_software_final/acare_auth/`

Dual-modal biometric authentication: passive face scan (MediaPipe) + face verification (InsightFace buffalo_sc) + voice verification (ECAPA-TDNN ONNX). Publishes validated intents after auth gate passes.

**Files (8):**

| File | Class(es) | Lines | Purpose |
|---|---|---|---|
| `auth_node.py` | `AuthNode`, `PendingLogin`, `PendingIntent`, `PendingEnrollment` | 691 | Master auth orchestrator — login flow, runtime voice drift check, and a **threaded enrolment loop** that prevents blocking ROS2 execution during user registration. |
| `face_detect.py` | `PassiveFaceDetector` | — | MediaPipe face detection (passive, always-on scan) |
| `verify_face.py` | `FaceVerifier` | — | InsightFace buffalo_sc — 512-D embedding, cosine similarity, threshold=0.78 |
| `verify_voice.py` | `VoiceVerifier` | — | ECAPA-TDNN ONNX — 192-D embedding, cosine similarity, threshold=0.85 |
| `storage.py` | `UserStore`, `UserRecord` | 160 | SQLite user database with face/voice embeddings stored as NPY blobs |
| `export_ecapa_onnx.py` | — | — | One-time script to export ECAPA-TDNN from SpeechBrain to ONNX |

**Auth Flow:**
1. **Passive face scan** (0.5s timer): MediaPipe detects face in camera frame → matches against enrolled users via InsightFace
2. **Login prompt**: `"Welcome Dr. Sharma. Say confirm to log in."`
3. **Voice confirmation**: User says "confirm" → ECAPA-TDNN verifies voice embedding matches stored profile
4. **Session activation**: Publishes AuthResult, transitions to STANDBY, starts 2-hour hard TTL
5. **Runtime voice drift check**: Every transcript verified against stored voice embedding; 3 consecutive failures triggers reconfirmation prompt. Retains `_pending_intent` while prompting for reconfirmation.
6. **Handover face check**: During HANDOVER state, face similarity checked every 0.5s (advisory gate)

**Enrolment Flow:**
- ROS2 service `/enrol_staff` with bi-modal biometric capture
- Captures 10 face frames (via camera) + 3 voice samples (via transcript PCM16 audio)
- Normalises embeddings via mean + L2 normalisation
- Stores in SQLite with NPY serialisation, roles: surgeron/nurse/admin

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

---

### 14.6 acare_planner/ — Task Planner & State Machine

**Type:** Python package | **Path:** `acare_software_final/acare_planner/`

The core planning and execution engine. Contains the 10-state FSM, analytical IK solver, LLM-based agentic planner for primary orchestration, and tool registry.

**Files (6):**

| File | Class(es) | Lines | Purpose |
|---|---|---|---|
| `state_manager.py` | `StateManager` | 222 | 10-state global FSM with all valid transitions |
| `planner_node.py` | `PlannerNode`, `WorldState`, `TaskContext` | 945 | Full task orchestration: vision search → grasp → handover → release. Uses `ReentrantCallbackGroup` + `MultiThreadedExecutor` for concurrent callback processing (no daemon threads). Timer-based polling replaces raw `threading.Thread`. ESTOP preemption works naturally through ROS2 executor interleaving. |
| `agentic_planner.py` | `AgenticPlanner` | 448 | Interfaces with NIM LLM. Provides search strategies (handles **`AUTO`** zone logic by querying Bayesian probability maps), recovery options, and handover pose overrides. Records per-call metadata (tier: NIM/Groq/Deterministic, error reason, latency_ms). Publishes `LLM_FALLBACK` LogEvent on every non-NIM tier use. After 3+ consecutive deterministic fallbacks → `LLM_DEGRADED` alert with WARNING severity. |
| `agent_schema.py` | `ToolCallSchema`, `validate_agentic_decision()` | 20 | Strict schema-validated LLM output |
| `handover.py` | `HandoverProtocol` | 218 | 3-gate handover protocol (async — face + hand + voice) |
| `ik_solver.py` | `IKSolver`, `IKResult` | 337 | Analytical 6-DOF inverse kinematics |
| `tool_registry.py` | All constants + `resolve_alias()` | 91 | Canonical tool → YOLO class mapping (6 tools) |
| `package.xml`, `setup.py`, `setup.cfg` | — | — | ROS2 package metadata |

**Note on handover implementation:** The **active implementation** is inline in `planner_node.py` (3 substates with agentic recovery). The `handover.py` file contains a legacy standalone `HandoverProtocol` class for reference/testing.

**Task Execution via Agentic Planner:**
The PlannerNode routes all intent fulfillment through `AgenticPlanner` which issues commands constrained by `ToolCallSchema`. The traditional rigid deterministic phases (Search → Grasp → Handover) are dynamically orchestrated by the LLM:

- **Agentic Vision Search:** The LLM decides the search strategy, including priority zones and whether to reset the Bayesian probability map. If search fails, it can invoke `re_evaluate_target` or `clarify_with_user`.
- **Agentic Grasp & Recovery:** The LLM evaluates the 3D target. It issues a `move_arm` command to a pre-grasp pose, then descends. If the grasp fails (via `MotionFeedback`), the LLM dynamically sequences a recovery (e.g., repositioning, increasing force up to 10N soft limit, or trying the next YOLO candidate).
- **Handover Protocol:** Handover involves 3 gates (face advisory, palm detect, voice confirm). If face tracking is lost or the user requests a height change, the LLM uses `adjust_handover_height` to recover interactively.

**Agentic Decision Safety Validation:**
The LLM evaluates `StateSnapshot` (current vision, arm limits, prior outcomes). It MUST output a strict JSON payload validated by Pydantic (`agent_schema.py`). If the LLM proposes an unsafe action (e.g., force > 15N) or invalid schema, the `tool_kernel` rejects it. If the API times out, the robot halts safely; it never executes unvalidated steps.

**10-State Finite State Machine:**

```
OFFLINE → LOGGED_OUT → STANDBY → LISTENING → PROCESSING → EXECUTING → HOLDING → HANDOVER → STANDBY
                                                                    ↓           ↓
                                                               ESTOP ←────────+
                                                                   ↓
                                                              STANDBY (on recovery)
ERROR → OFFLINE
```

| State | Description | Allowed Transitions |
|---|---|---|
| `OFFLINE` | System off / booting | LOGGED_OUT |
| `LOGGED_OUT` | No active user session | STANDBY |
| `STANDBY` | User authenticated, waiting | LISTENING, PROCESSING, LOGGED_OUT |
| `LISTENING` | Voice pipeline active | PROCESSING, STANDBY |
| `PROCESSING` | Task execution active (vision search) | EXECUTING, STANDBY |
| `EXECUTING` | Arm moving to grasp | HOLDING, ESTOP |
| `HOLDING` | Tool grasped, moving to handover | HANDOVER, ESTOP |
| `HANDOVER` | Face + hand + voice verification | STANDBY, ESTOP |
| `ESTOP` | Emergency stop — reachable from ANY state | STANDBY |
| `ERROR` | Irrecoverable error | OFFLINE |

**Logout guard:** Rejected from EXECUTING, HOLDING, HANDOVER (prevents tool drop during active manipulation)
**Inactivity timeout:** 5 minutes in STANDBY → auto-logout
**Hard TTL:** 2 hours from login (configurable via system.yaml)


**Analytical IK Solver (ik_solver.py):**
- Geometry: base 0.352m, upper_arm 0.400m, forearm 0.400m, wrist+tool 0.236m, max_reach 0.836m
- J1: base rotation via `atan2(y, x)`
- J2/J3: planar 2-link IK (shoulder + forearm) via law of cosines (elbow-up configuration)
- J4/J5/J6: wrist orientation for top-down grasp (J5 closes chain to vertical)
- Joint limit clamping with reachable flag — never raises, always returns best-effort
- FK self-test verified to 0.0000m round-trip error

**Agentic Planner (agentic_planner.py):**
- Primary: NVIDIA NIM `llama-3.3-nemotron-super-49b-v1` (40 RPM free)
- Fallback: Groq `llama-3.3-70b-versatile` (30 RPM free)
- JSON schema strict mode output with validated Pydantic models
- Decision types: SEARCH_STRATEGY, VISION_RECOVERY, GRASP_RECOVERY, IK_RECOVERY, HANDOVER_RECOVERY, ABORT
- **Learning:** Learns user handover height preferences and time-of-day tool placement patterns
- Every LLM decision validated by `validate_agentic_decision()` before execution
- Invalid proposals → deterministic fallback (robot never acts on unvalidated LLM output)

**Agentic Decision Safety Validation:**
Every agentic proposal is validated by a strict 20-line Pydantic model (`ToolCallSchema`) in `agent_schema.py` with the following constraints:
- Must specify a valid `tool` (e.g. `grasp_tool`, `re_evaluate_target`, etc.)
- Must provide required `parameters` dictionary
- Legacy rigid bounds (like 160-char TTS limits, predefined decision types) were removed to allow the LLM full agentic flexibility, while the safety constraints are enforced natively by the tool execution layers in `tool_kernel.py`.

**Kiosk Mode:**
- **Rest pose:** [0.0, 0.15, -0.35, 0.0, 0.10, 0.0]
- **Interaction pose:** [0.0, -0.10, -0.05, 0.0, -0.05, 0.0]
- **Auto-return:** Returns to rest pose after 12s inactivity (configurable via `kiosk_return_to_rest_seconds`)
- **Reduced motion:** Velocity scale 0.22x, acceleration limit 0.10 (configurable via `kiosk_velocity_scale`, `kiosk_accel_limit`)

**Per-Phase Retry Logic:**
- **Vision search:** 3 attempts with escalation: LLM strategy → uniform search → user confirmation
- **Grasp:** 3 attempts: Base force (3N) → reposition + rotation → force increase (max 10N soft limit)
- **Handover:** 3 face attempts, 2 hand attempts, 2 voice attempts, with agentic Z-height recovery
- All retries use agentic recovery with deterministic fallback on validation failure
- Detection candidates: Multiple YOLO detections are tried if first grasp fails

**Tool Registry (6 tools):**
| Canonical | YOLO Class | Example Aliases |
|---|---|---|
| cream | cream | lotion, ointment, topical |
| scissors | medical scissors | cutting tool, snips |
| forceps | surgical forceps | tweezers, clamps, graspers |
| thermometer | thermometer | temp probe, temperature tool |
| oximeter | oxymeter | pulse ox, spo2, oxygen meter |
| plaster | plaster | bandaid, adhesive strip |

#### 14.6.1 Implemented Software Architecture

##### 1. `SafetyKernel` Class (Deterministic Safety Guardrails) ✓

The `SafetyKernel` acts as the L0 validation gate before any tool execution in `tool_kernel.py`. It operates with absolute veto authority across 6 layers:

| Layer | Check | Action |
|-------|-------|--------|
| L1 | ESTOP active | Reject all non-abort actions while ESTOP is latched |
| L2 | Workspace bounds | Reject targets outside x/y ±0.60m, z 0.0–0.75m (from system.yaml) |
| L3 | Joint limits | Reject IK solutions flagged as unreachable |
| L4 | Consecutive failures | Abort after 3 consecutive tool failures |
| L5 | LLM call budget | Abort when budget (20 calls) is exhausted |
| L6 | Gripper force anomaly | Reject GRASP if force telemetry exceeds 50N anomaly threshold |

- **`evaluate(estop_active, tool_name, target_xyz, ik_reachable, calls_used, gripper_force) -> KernelResult`**
  - Evaluates all 6 layers in order. Short-circuits on first veto.
  - Returns `KernelResult(allowed=True/False, layer, reason)`.
- **`reset_failures()` / `record_failure()` / `record_success()`** — Tracks consecutive failures for L4.
- Wired into `ToolKernel.execute_tool()` as the pre-execution gate, called after schema validation (L2 in tool_kernel) but before the action is dispatched.

##### 2. `RetryCounters` Dataclass (Independent Retry Auditing) ✓

Prevents the agentic loop from entering infinite execution states by tracking failures on a per-action basis. Each failure counter operates independently (e.g., a grasp retry does not consume a vision retry). All counters are capped at `MAX_RETRIES_PER_STEP = 2`, `MAX_TOTAL_RETRIES = 5`.

- **Fields**: `_step_retries: dict[str, int]`, `_total_retries: int`
- **Methods**:
  - **`reset()`** — Clears all retry counters
  - **`record_failure(step_key: str) -> bool`** — Increments step and total counters; returns `True` if either cap is exhausted

---

### 14.7 acare_safety/ — Safety Monitoring

**Type:** Python package | **Path:** `acare_software_final/acare_safety/`

**Files (1):**

**`safety_node.py`** (213 lines) — `SafetyNode` ROS2 node:

Monitors two safety inputs and publishes graded `SafetyAlert`:
1. **LiDAR proximity** (YDLIDAR T-mini Plus on `/scan`, BEST_EFFORT QoS):
   - Front arc = middle third of scan (±60° from forward)
   - >600mm: SAFE (normal operation)
   - 400–600mm: WARNING (reduce speed)
   - <400mm: ESTOP (immediate halt)
2. **MCU telemetry** (on `/motion_feedback`, BEST_EFFORT QoS):
   - 6 joint currents — ESTOP at >8.0A, WARNING at >6.0A
   - 6 joint temperatures — ESTOP at >75°C, CRITICAL at >65°C, WARNING at >55°C
   - Gripper force — ESTOP at >15N, WARNING at >10N

**Alert throttling:** WARNING/CRITICAL suppressed to 1/sec per (severity, source) pair. **ESTOP is NEVER throttled** — every ESTOP published immediately.

---

### 14.8 acare_vision/ — Perception Pipeline

**Type:** Python package | **Path:** `acare_software_final/acare_vision/`

All perception: YOLO object detection, Bayesian next-best-view search, depth-to-3D localisation, MediaPipe hand tracking, fake object detection, HP60C camera interface.

**Files (9):**

| File | Class(es) | Lines | Purpose |
|---|---|---|---|
| `vision_node.py` | `VisionNode` | 609 | Master orchestrator with mode switching (IDLE/SEARCH/HANDOVER), camera health monitoring |
| `yolo_infer.py` | `YOLO26ONNX` | 408 | YOLO26 NMS-free ONNX inference with low-light enhancement (gamma, CLAHE, unsharp mask) |
| `nbv_search.py` | `NBVSearch` | 570 | Bayesian next-best-view: sorts zones by P(tool|zone), captures 3 frames per viewpoint with dynamic wrist-camera T |
| `localiser.py` | `Localiser` | 240 | Pinhole back-projection + wrist-mounted camera FK: pixel + depth + per-pose T_override → robot-frame 3D |
| `hand_tracker.py` | `HandTracker` | 210 | MediaPipe Hands + wrist-camera T override: open palm, 3D palm centre, publishes /hand_status at ~20Hz |
| `fake_detector.py` | `FakeDetector` | 126 | Dual-signal fake object detection: texture variance (Laplacian) + depth variance |
| `hp60c_camera_node.py` | `HP60CCameraNode` | 153 | Camera frame cache — subscribes to ascamera topics, exposes capture() API |
| `camera_probe.py` | — | — | Camera connectivity diagnostic tool |
| `package.xml`, `setup.py`, `setup.cfg` | — | — | ROS2 package metadata |

**Nested Packages:**
- `acare_logging/` — Audit trail: SQLite database, batched writes, auto-rotation at 200 MB. **Note:** Package is nested under acare_vision/ for deployment purposes.

**VisionNode Modes:**
- **IDLE** — no active task, minimal resources
- **SEARCH** — NBV search running, YOLO active, HandTracker stopped
- **HANDOVER** — HandTracker active, YOLO not called
- **YOLO and MediaPipe Hands NEVER run simultaneously**

**YOLO Inference (acare_v26.onnx — YOLO26 NMS-free):**
- Input: 320x320 RGB, output: [1, 300, 6] NMS-free format
- 6 classes: cream, medical scissors, oxymeter, plaster, surgical forceps, thermometer
- ONNX Runtime with CPUExecutionProvider, 4 intra-op threads
- Scene-adaptive: low-light detection via HSV V-channel analysis, gamma correction (1.55/1.85), CLAHE, unsharp mask
- Confidence thresholds: normal=0.70, low-light=0.56
- Multi-frame merging with IoU-based deduplication (threshold 0.5)

**NBV Search (Bayesian):**
- 3 zones (A=left, B=centre, C=right) — defined by viewpoints from calibration
- Wrist micro-offsets (±0.035rad J5, ±0.025rad J6) — 3 frame captures per viewpoint
- **Per-viewpoint dynamic T:** Computes `T_override = localiser.compute_T_for_viewpoint(vp['joint_angles'], arm_link_lengths)` and passes it to `pixel_to_robot()` so that detected tool positions are correctly transformed to robot base frame despite the wrist-mounted camera moving with the arm.
- Bayesian map update: found → *=1.5, not found → *=0.7, passive tools seen → *=1.3
- Normalise → clamp [0.05, 0.90]
- Temporal consistency: object seen within 50px in previous viewpoint → promoted at 0.65 confidence

**3D Localisation (localiser.py):**
- Pinhole camera: X = (u-cx) * Z / fx, Y = (v-cy) * Z / fy
- Real HP60C intrinsics: fx=572.04, fy=571.49, cx=329.27, cy=242.09 (640x480) — auto-updated live from `/camera_info` via `update_intrinsics()`
- Median-of-window fallback (40x40) for sparse depth pixels
- **Wrist-mounted camera (HP60C on gripper assembly):**
  - `T_robot_camera` is NOT static — it changes with every arm pose.
  - `compute_T_for_viewpoint(joint_angles, arm_link_lengths)` computes the full 4×4 transform: `T_robot_flange(FK) × T_flange_camera(fixed offset)`.
  - FK uses arm link lengths (base_height=0.352m, upper_arm=0.400m, forearm=0.400m) from `system.yaml`.
  - `T_flange_camera` is a fixed 4×4 offset: default 40mm forward (X), 20mm below (Z) the wrist flange. Configured via `system.yaml camera.T_flange_camera`.
  - NBV search computes a fresh `T_override` at each viewpoint and passes it to `pixel_to_robot(bbox, depth, T_override=...)`.
  - Hand tracker receives the arm's presentation-pose joints from vision_node (cached via MotionFeedback) and computes a single `T_override` for the HANDOVER phase.
- **Table-mounted camera fallback:** Static `T_robot_camera` in `system.yaml` (identity by default). Only used when `T_override` is not supplied.
- Valid depth range: 200mm–4000mm

**Hand Tracking (hand_tracker.py):**
- MediaPipe Hands: static_image_mode=False, max_num_hands=1, min_detection_confidence=0.70, min_tracking_confidence=0.60
- Open palm detection: 3+ fingers extended (tip y < PIP y)
- Palm-up detection: fingertip mean y < wrist y
- Depth approach tracking: uses X-axis coordinate in robot base frame
- BGR→RGB conversion (critical — MediaPipe requires RGB)
- 3D palm centre: average of WRIST + 4 MCP landmarks projected via localiser
- **Wrist-mounted camera support:** Before `start()`, vision_node calls `set_viewpoint_joints(joint_angles)` with the arm's current pose (cached from MotionFeedback). The hand tracker computes a `T_override` via `localiser.compute_T_for_viewpoint()` and passes it to every `pixel_to_robot()` call, ensuring palm 3D positions are in the correct robot base frame despite the camera moving with the arm.

**Fake Detection (fake_detector.py):**
- Signal 1: Laplacian texture variance (threshold=120)
- Signal 2: Depth variance of ROI (threshold=0.002 m²)
- Both signals below threshold → fake (reject)
- If depth unavailable (<10 pixels) → benefit of the doubt (not fake)

**Wrist-Mounted Camera Architecture (HP60C on Gripper Assembly):**

The HP60C RGBD camera is physically mounted on top of the gripper assembly, meaning it moves with the arm. This has significant implications for 3D localisation:

| Concern | Solution |
|---|---|
| Camera intrinsics | Auto-loaded from HP60C driver's `/camera_info` topic via `localiser.update_intrinsics()` — no checkerboard needed |
| Camera-to-robot transform | Computed dynamically per arm pose via `compute_T_for_viewpoint(joint_angles, arm_link_lengths)` |
| FK chain | `T_robot_camera = T_robot_flange(FK) × T_flange_camera` |
| FK computation | Uses arm link lengths from `system.yaml` (base=0.352m, upper=0.400m, forearm=0.400m) |
| Flange offset | `T_flange_camera` — fixed rigid offset measured once with a ruler (default: 40mm forward, 20mm below flange) |
| NBV search | Computes fresh `T_override` at each viewpoint, passes to `pixel_to_robot(bbox, depth, T_override=...)` |
| Hand tracking | Receives arm's presentation-pose joints from vision_node (cached via MotionFeedback), computes single `T_override` for HANDOVER |
| Table-mount fallback | Static `T_robot_camera` in `system.yaml` (identity default) — used only when `T_override` is not supplied |

**Configuration (system.yaml):**
```yaml
camera:
  T_flange_camera:   # Fixed offset from wrist flange to HP60C lens centre
    [1, 0, 0, 0.040,   # 40mm forward
     0, 1, 0, 0.000,    # no lateral offset
     0, 0, 1,-0.020,    # 20mm below
     0, 0, 0, 1]
```

**Data flow during NBV search:**
```
Arm moves to viewpoint (known joint angles)
  → compute_T_for_viewpoint(joints, link_lengths)
  → FK: flange at (x, y, z) in robot frame
  → × T_flange_camera
  → T_robot_camera for THIS pose
  → YOLO detects tool at pixel (u, v) with depth Z
  → pixel_to_robot(bbox, depth, T_override=T)
  → (x, y, z) in robot base frame — correct!
  → IK solver → arm reaches the actual tool location
```

---

### 14.9 acare_logging/ — Audit Trail

**Type:** Python package | **Path:** `acare_software_final/acare_logging/`

**Files (1):**

**`log_node.py`** (171 lines) — `LogNode` ROS2 node:

- **Subscribes:** `/log_event` (BEST_EFFORT QoS — loss acceptable)
- **Writes to SQLite** at `logs/acare_logs.db`
- **Batched writes:** 10-event batch size, 5-second periodic flush timer
- **Thread-safe:** SQLite lock serialises all DB access
- **Auto-rotation:** When DB exceeds 200MB, oldest 20% archived to gzipped CSV, deleted by timestamp cutoff
- **Table schema:** event_id, timestamp (INTEGER), staff_id, event_type, tool, state, description, safety_severity, voice_e2e_ms, vision_search_ms, motion_ms, total_task_ms
- On shutdown: flushes remaining buffer, closes connection

---

### 14.10 acare_embedded_interface/ — Hardware Bridge

**Type:** Python package | **Path:** `acare_software_final/acare_embedded_interface/`

**Files (1):**

**`embedded_interface_node.py`** (297 lines) — `EmbeddedInterfaceNode` ROS2 node:

The ONLY point of contact between ROS2 software and hardware.

- **Subscribes:** `/arm_command`, `/gripper_command`, `/emergency_stop`, `/robot_state`
- **Publishes:** `/motion_feedback` after every command

**Simulation path (active):**
- Action clients to Gazebo controllers:
  - `/arm_controller/follow_joint_trajectory` — 6 arm joints: base, shoulder, elbow, wrist_1, wrist_2, wrist_3
  - `/gripper_controller/follow_joint_trajectory` — gripper_slider_right
- Async goal sending (NON-BLOCKING — never blocks executor for ESTOP responsiveness)
- Joint trajectory goals with velocity-scaled duration (default 2.5s arm, 0.7s gripper)

**Guards:**
- **LOGGED_OUT arm guard:** Only kiosk poses (rest/interaction) at kiosk velocity/accel limits allowed
- **LOGGED_OUT gripper guard:** GRASP/CLOSE commands rejected — guard on upper-cased command (fail-closed, NOT fail-open)
- **ESTOP latch:** All goals rejected while active; cleared on recovery to STANDBY/LOGGED_OUT
- **MOVE_REL rejection:** Only absolute MOVE supported (no joint state feedback available)

**Real-hardware path (SPI Mode):**
- Real hardware communication uses direct SPI rather than UART/CAN. Selected via `system.yaml interface.mode` set to `"SPI"`.
- Pi 5 acts as SPI Master querying status and sending targets via standard Linux `/dev/spidev0.0`.
- Teensy 4.1 acts as SPI Slave responding with 64-byte double-buffered DMA frames.
- Attention line (ATTN) interrupt provides sub-millisecond hardware fault signaling to the Pi 5.
- Core logic, pin wiring, packet layouts, and safety watchdogs are defined in Section 6.1.

---

---

### 14.11 acare_admin/ — Administration & Calibration

**Type:** Python package | **Path:** `acare_software_final/acare_admin/`

**Files (2):**

**`admin_cli.py`** (312 lines) — Command-line interface:
| Command | Function | Description |
|---|---|---|
| `enrol --name --role` | `cmd_enrol()` | Triggers biometric enrolment via ROS2 service call to auth_node |
| `revoke --id` | `cmd_revoke()` | Marks staff member inactive in SQLite |
| `list-staff` | `cmd_list_staff()` | Lists all enrolled staff with ID, name, role, registration date, active status |
| `set-api-key --service --key` | `cmd_set_api_key()` | Stores encrypted API key (Fernet symmetric encryption at `/etc/acare/api_keys.yaml`) |
| `set-threshold --sensor --value` | `cmd_set_threshold()` | Updates safety thresholds in thresholds.yaml |
| `show-logs --last` | `cmd_show_logs()` | Recent log events from SQLite |
| `export-logs` | `cmd_export_logs()` | All log events → CSV |
| `status` | `cmd_status()` | ROS2 node list + Pi temperature |
| `calibrate` | `cmd_calibrate()` | 7-step calibration procedure |
| `demo-mode --enable / --disable` | `cmd_demo_mode()` | Toggle demo mode in system.yaml |

**7-Step Calibration Procedure & Planned Algorithms:**

1. **Joint Homing**: Teensy moves each joint slowly toward its physical limit switch, zeroing encoder values upon trigger, and setting soft mechanical limits.
2. **Camera Intrinsics**: **NOT required for HP60C.** The HP60C RGBD driver publishes factory-calibrated intrinsics (fx, fy, cx, cy) on its `/camera_info` topic. The vision node subscribes to this topic and calls `localiser.update_intrinsics()` on every message, keeping intrinsics accurate without manual calibration. This step is retained only for non-HP60C cameras.
3. **Workspace Boundary Confirmation**: Prompts the admin to verify the reachability and limits of the coordinates defined in `system.yaml`.
4. **SAFE_DROP_ZONE Definition**: Prompts the admin to manually position the arm over the safety deposit zone. The current joint angles and projected $(x, y, z)$ positions are captured and written to the config.
5. **NBV Viewpoints Definition / Wrist-Camera Flange Offset**: The admin moves the arm to each search viewpoint (looking at tray zones A, B, C) and records the joint angles. These viewpoints are written to `system.yaml vision.viewpoints`. The camera-to-flange offset `T_flange_camera` is measured once with a ruler (distance from wrist flange to HP60C lens centre) and written to `system.yaml camera.T_flange_camera`. The full camera-to-robot-base transform is computed dynamically at runtime via forward kinematics at each viewpoint — no `solvePnP` or checkerboard extrinsics calibration is needed for the wrist-mounted configuration.
6. **Fake Detection Threshold Calibration**: Establishes texture and depth variance thresholds for replica rejection. Admin places 20 real metallic tools and 20 printed paper replicas in front of the camera. The script calculates Laplacian texture variance (`cv2.Laplacian().var()`) and depth map variance for each sample. It computes the separation boundaries and updates `thresholds.yaml` with the calibrated `texture_variance_threshold` and `depth_variance_threshold` values.
7. **LiDAR Baseline Scan**: Clears the workspace and performs a baseline scan using the YDLIDAR on `/scan`. Averaged range arrays are stored to construct a clean reference map, allowing `safety_node` to compute deviations/obstructions during live operation.

**`admin_node.py`** (24 lines) — Minimal ROS2 node with 30-second heartbeat timer

---

### 14.12 Simulation & Support Files

**Path:** `acare_software_final/simulation/` — Gazebo simulation files for WSL Ubuntu 24.04

**Path:** `acare_software_final/scripts/` — Build and validation helpers:
| File | Description |
|---|---|
| `build_workspace.sh` | Colcon build with symlink-install |
| `launch_validate.sh` | Post-launch validation (checks all nodes alive) |
| `validate_ros_graph.py` | Validates ROS2 topic graph matches expected topology |
| `preflight_ros_env.py` | Pre-flight environment check (ROS2 sourced, deps available) |

**Path:** `acare_software_final/models/` — Trained models:
- `acare_v26.onnx` (9.8 MB) — YOLO26 NMS-free, 6 surgical tool classes
- `acare_v11.onnx` — Legacy YOLO11 version
- `model.pt` — Training checkpoint

**Path:** `acare_software_final/camera_configs/` — HP60C encrypted config JSON files

**Path:** `acare_software_final/archive/` — Old prototypes, not deployed

---

### 14.13 ROS2 Topic Map (Full)

| Topic | Type | Publisher(s) | Subscriber(s) | QoS |
|---|---|---|---|---|
| `/robot_state` | RobotState | StateManager | All nodes | TRANSIENT_LOCAL |
| `/state_transition` | StateTransition | AuthNode, PlannerNode | StateManager | RELIABLE |
| `/safety_alert` | SafetyAlert | SafetyNode, VoiceNode | StateManager, PlannerNode | RELIABLE |
| `/emergency_stop` | EmergencySignal | VoiceNode, KeywordMonitor, SupervisorNode | EmbeddedInterface, StateManager | RELIABLE |
| `/raw_transcript` | Transcript | VoiceNodeROS (ASR) | DialogueNode, AuthNode | RELIABLE |
| `/intent_result` | Intent | DialogueNode | AuthNode | RELIABLE |
| `/validated_intent` | ValidatedIntent | AuthNode | PlannerNode, DialogueNode | RELIABLE |
| `/auth_result` | AuthResult | AuthNode | StateManager, PlannerNode | RELIABLE |
| `/auth_request` | AuthRequest | DialogueNode | AuthNode | RELIABLE |
| `/tts_request` | String | StateManager, PlannerNode, AuthNode, DialogueNode | VoiceNodeROS (TTS) | RELIABLE |
| `/vision_search_request` | VisionSearchRequest | PlannerNode | VisionNode | RELIABLE |
| `/vision_result` | VisionResult | VisionNode | PlannerNode, DialogueNode | RELIABLE |
| `/vision_status` | VisionStatus | VisionNode | PlannerNode | RELIABLE |
| `/hand_status` | HandStatus | VisionNode (HandTracker) | PlannerNode | RELIABLE |
| `/arm_command` | ArmCommand | PlannerNode, VisionNode | EmbeddedInterface | RELIABLE |
| `/gripper_command` | GripperCommand | PlannerNode | EmbeddedInterface | RELIABLE |
| `/motion_feedback` | MotionFeedback | EmbeddedInterface | PlannerNode, SafetyNode, VisionNode | BEST_EFFORT depth=1 |
| `/log_event` | LogEvent | PlannerNode, VisionNode, SupervisorNode | LogNode | BEST_EFFORT |
| `/scan` | LaserScan | YDLIDAR driver | SafetyNode | BEST_EFFORT depth=1 |
| `/enrol_staff` (service) | EnrolStaff | AdminCLI | AuthNode | — |

**Camera Topics (from ascamera node):**
| Topic | Type | Rate | Resolution |
|---|---|---|---|
| `/ascamera_hp60c/camera_publisher/rgb0/image` | Image (BGR8) | 12.4 Hz | 640×480 |
| `/ascamera_hp60c/camera_publisher/depth0/image_raw` | Image (16UC1) | 12.4 Hz | 640×480 |
| `/ascamera_hp60c/camera_publisher/rgb0/camera_info` | CameraInfo | — | — |
| `/ascamera_hp60c/camera_publisher/depth0/camera_info` | CameraInfo | — | — |
| `/ascamera_hp60c/camera_publisher/depth0/points` | PointCloud2 | — | — |

---

### 14.14 System Architecture Diagrams

**End-to-End Data Flow (Fetch "scissors"):**
```
┌──────────┐   ┌────────────┐   ┌─────────────┐   ┌─────────────┐   ┌──────────────┐   ┌──────────┐
│ Mic/VAD  │→  │ Deepgram   │→  │ Dialogue-   │→  │ AuthNode    │→  │ PlannerNode  │→  │ Vision-  │
│ (Silero) │   │ Nova-2 ASR │   │ Node        │   │ (voice/face │   │ (NIM Agentic │   │ Node     │
│          │   │            │   │ (intent via │   │ biometric   │   │ Planner +    │   │ (YOLO +  │
│          │   │            │   │ /intent_res)│   │ validation) │   │ execute)     │   │ NBV)     │
└──────────┘   └────────────┘   └─────────────┘   └─────────────┘   └──────┬───────┘   └──────────┘
                                                                    │
                         ┌──────────┐   ┌──────────────┐   ┌───────▼───────┐
                         │ Safety-  │   │ Embedded-    │   │ IK Solver     │
                         │ Node     │←──│ Interface    │←──│ (analytical   │
                         │ (LiDAR + │   │ Node →       │   │ 6-DOF)        │
                         │ telemetry)│  │ Teensy/Gazebo│   └───────────────┘
                         └──────────┘   └───────┬──────┘
                                              │
                              ┌────────────────▼────────────────┐
                              │         LogNode (SQLite)         │
                              │  ← /log_event from all nodes      │
                              └──────────────────────────────────┘
```

**Note:** supervisor_node.py (crash recovery) is a ROS2 node launched by acare.launch.py alongside all other nodes.

**Safety Architecture (Dual-Layer):**
```
Software (Pi 5)                          Firmware (Teensy 4.1)
┌─────────────────────────┐              ┌─────────────────────────┐
│ SafetyNode              │  SPI (Plan)  │ Hardware ISRs           │
│ • LiDAR proximity zones │◄────────────►│ • Overcurrent cutoff    │
│   (600mm=WARNING,      │  ros2_control│ • Overtemp cutoff       │
│    400mm=ESTOP)         │  (Current)   │ • Limit switch stop     │
│ • MCU telemetry check   │              │ • Watchdog heartbeat    │
│   (current, temp,       │              └─────────────────────────┘
│    gripper force)       │                        │
│ • Graded SafetyAlert    │                        │
│ • ESTOP keyword detect  │                        │
└─────────────────────────┘                        │
        │                                           │
        ▼                                           ▼
┌────────────────────────────────────────────────────────────┐
│  ESTOP Signal → StateManager → EmbeddedInterface → Motors   │
│  (Broadcast to all nodes, <200ms latency from utterance)   │
└────────────────────────────────────────────────────────────┘
```

**Supervisor (ROS2 Node):**
```
┌────────────────────────────────────────────────────────────┐
│ supervisor_node.py (ROS2 Node)                               │
│ • Monitors all 10 ROS2 nodes every 5s via graph API         │
│   (self.get_node_names() — no subprocess)                   │
│ • Publishes /emergency_stop directly (no ros2 topic pub)    │
│ • Auto-restarts: log_node, admin_node, dialogue_node,       │
│   voice_node, auth_node                                      │
│ • Critical nodes (no auto-restart, triggers ESTOP):         │
│   safety_node, embedded_interface_node, state_manager,      │
│   planner_node, vision_node                                 │
│ • Power recovery: On boot, checks last DB state. If        │
│   EXECUTING/HOLDING/HANDOVER → safe deposit + STANDBY      │
└────────────────────────────────────────────────────────────┘
```

**State Machine (10 States):**
```
                  ┌─────────┐
                  │ OFFLINE │
                  └────┬────┘
                       │
                  ┌────▼─────┐
          ┌──────►│LOGGED_OUT│◄──────────┐
          │       └────┬─────┘           │
          │            │               │
          │       ┌────▼───┐           │
          │       │ STANDBY ├───┐       │
          │       └───┬─┬──┘   │       │
          │           │ │      │       │
          │     ┌─────┘ └──────┐  │       │
          │     ▼              ▼   │       │
          │ ┌─────────┐  ┌──────────┐ │       │
          │ │LISTENING│  │PROCESSING│ │       │
          │ └────┬────┘  └────┬─────┘ │       │
          │      │            │       │       │
          │      └──────┬─────┘       │       │
          │             ▼             │       │
          │        ┌──────────┐       │       │
          │        │EXECUTING │──┐    │       │
          │        └────┬─────┘  │    │       │
          │             │        │    │       │
          │        ┌────▼──┐     │    │       │
          │        │HOLDING├─────┤    │       │
          │        └────┬──┘     │    │       │
          │             │        │    │       │
          │        ┌────▼───┐    │    │       │
          │        │HANDOVER├────┤    │       │
          │        └────┬───┘    │    │       │
          │             │        │    │       │
          └─────────────┼────────┘    │       │
                        │               │       │
        ┌───────────────────┴───────────┐  │       │
        ▼                                   ▼  │       │
   ┌─────────┐                        ┌───▼────┐ │       │
   │ ESTOP   │◄── from ANY state ───┤ ERROR  │ │       │
   └────┬────┘                        └────┬───┘ │       │
        │                                   │     │
        └──────────────┬────────────────┘     │
                       │                      │
                       ▼                      │
                  ┌─────────┐                │
                  │ STANDBY │◄────────────────┘
                  └─────────┘
```

**Key Properties:**
- **ESTOP:** Reachable from ANY state (safety override) — bypasses transition table
- **ERROR:** Only reachable via unrecoverable fault — transitions to OFFLINE
- **Logout Guard:** Cannot logout from EXECUTING, HOLDING, HANDOVER
- **Auto-logout:** 5 min inactivity in STANDBY
- **Hard TTL:** 2-hour session limit from login

---

*Module-by-module feature guide appended 2026-06-03*

---

## 15. Global Project Rules (LLM Enforcement)
- **Automatic Central Documentation Updates**: Whenever the main AI agent edits any file or folder (e.g. adding a function, modifying logic, or generating new files), the AI must manually update this `ACARE_Documentation.md` file to reflect the change. This guarantees that this centralized documentation consistently contains a complete, up-to-date, LLM-level understanding of the architecture.

---

## 16. Hardware Architecture & Specifications

### 16.1 Mechanical Structure
- **Degrees of Freedom**: 6-DOF serial robotic manipulator.
- **Custom Transmission**: Cycloidal gearboxes (3D printed with PETG high infill) — 22:1 reduction ratio at J2 (shoulder), 15:1 at J3 (elbow).
- **Structural Links**: Constructed using aluminum sheet metal for primary load-bearing links and PETG structures.
- **Wrist & End-Effector**: Parallel jaw gripper actuated via a Bowden line pulley system, with integrated analog force sensors at the fingertips.
- **Safety Zones**:
  - **SAFE_DROP_ZONE**: Predefined flat table surface for safe emergency deposit.
  - **Handover Zone**: Pre-calibrated position for direct delivery to user.

### 16.2 Actuators & Motor Control
- **BLDC Motors**: 1.4 Nm Rhino Planetary Gearbox BLDC motors for Joint 1 (Base), Joint 2 (Shoulder), and Joint 3 (Elbow).
- **Motor Drivers**: RMCS-3002l drivers communicating with Teensy via Modbus ASCII.
- **Gripper Actuation**: Positioned and driven in force control mode.

### 16.3 Joint & Link Sizing Parameters
- **Link Lengths**:
  - Base Height: 352 mm (J1 axis to J2 axis)
  - Upper Arm: 400 mm (J2 axis to J3 axis)
  - Forearm: 400 mm (J3 axis to J4 axis)
  - Wrist + Tool (TCP): 236 mm (J4 axis to gripper tip)
- **Joint Limits**:
  - J1 (Base): ±180°
  - J2 (Shoulder): ±135° (22:1 reduction)
  - J3 (Elbow): ±120° (15:1 reduction)
  - J4 (Wrist 1): ±180°
  - J5 (Wrist 2): ±180°
  - J6 (Wrist 3): ±180°

### 16.4 Complete Sensor Inventory
- **RGBD Camera**: YDLIDAR HP60C (wrist-mounted, 640x480 RGB @ 12.4Hz, 640x480 Depth @ 12.4Hz).
- **Proximity LiDAR**: YDLIDAR T-mini-Plus (base-mounted, Torso-level 2D scan, best-effort at 50Hz).
- **Joint Encoders**: AS5600 Magnetic Encoders (×6, I2C interface via TCA9548A multiplexer).
- **IMU**: Onboard accelerometer/gyroscope on MCU board for base orientation.
- **Current Sensing**: Shunt resistors on motor driver boards.
- **Thermal Sensors**: Thermistors embedded in joint motor housings.
- **Force Sensor**: Analog force-sensing resistor (FSR) at gripper fingertips.
- **Audio I/O**: Cardioid polar pattern microphone (connected via USB sound card to Pi) and active speaker.

### 16.5 Power System
- **Motor Power Rail**: Dedicated 24V supply, isolated with an LC filter and ferrite beads to suppress transients. Equipped with a physical hardware emergency cutoff relay (red button) wired directly to the RMCS-3002l enable pins (cuts 24V logic supply immediately without software traversal).
- **Logic Power Rail**: Regulated 5V supply powering the Raspberry Pi 5.
- **Grounding**: Unified common ground across all logic and power supply rails.
- **Connectors**: High-current XT30 male/female connections for battery/PSU to driver connections.

---

## 17. Embedded Firmware Design (Teensy 4.1)

### 17.1 Control Loop Frequencies
- **Position & Velocity Control Loops**: 200 Hz PID loops running deterministically on Teensy 4.1.
- **Sensor Read Loop**: 100 Hz polling loop for AS5600 encoders, current sensors, and joint thermistors.
- **Status Publishing**: 50 Hz telemetric updates streamed to the high-level Raspberry Pi.
- **Watchdog Heartbeat**: 5 Hz keepalive polling loop.

### 17.2 Encoder Interface & PID Parameters
- **AS5600 I2C Interface**: 400 kHz clock speed on the TCA9548A multiplexer. Joint angles calculated via:
  $$\text{Angle (rad)} = \frac{\text{raw\_count}}{4096} \times 2\pi$$
- **Filters**: Exponential moving average filter applied to raw encoder counts:
  $$\text{Filtered} = 0.7 \times \text{raw} + 0.3 \times \text{prev}$$
- **Zero Positions**: Offsets stored in EEPROM flash during homing.
- **PID Tuning Margins**: Feed-forward gravity compensation terms calculated dynamically for J2/J3. Anti-windup clamping implemented.

### 17.3 Embedded FSM states
- `IDLE`: Powered, motor position holding.
- `POSITION_CONTROL`: Executing active joint trajectory commands.
- `GRIPPER_CONTROL`: Gripper motor operating in force-control loop.
- `ESTOP`: PWM disabled, joint brakes engaged.
- `FAULT`: Local latch state on hardware thresholds exceeded.
- `CALIBRATION`: Executing slow homing routine.

### 17.4 Hardware Fault Protections & Warning Thresholds
- **Current Clamp**: joint_current > 8A for > 100ms triggers `FAULT` code 1 (soft warning warning at 6A reduces velocity by 25%).
- **Thermal Shutdown**: joint_temp > 75°C triggers `FAULT` code 2 (warnings at 55°C scale down velocity 25%, and at 65°C scale down 50%).
- **Encoder Soft Limits**: Encoder count exceeding mechanical constraints triggers `FAULT` code 3.
- **Velocity Limit**: Derivative velocity > 120°/s triggers `FAULT` code 4 (operating limit capped at 80°/s).
- **Gripper Force**: Finger pressure > 15N triggers `FAULT` code 5 (target force 3-5N, warn at 10N).
- **Heartbeat watchdogs**: Absence of valid keepalive frames for > 500ms triggers `FAULT` code 6.

---

## 18. Software ↔ Embedded Integration Boundary

### 18.1 SPI Physical Communication Layer
- **Interface**: SPI0 bus operating at 10.0 MHz.
- **SPI Pins**: MOSI (GPIO 10), MISO (GPIO 9), SCLK (GPIO 11), CE0 (GPIO 8).
- **Attention Line**: GPIO 25 (CE Pin 22) used for edge-triggered Teensy-to-Pi interrupts (ATTN).
- **DMA Buffer**: Double-buffered DMA channel transfers to prevent MCU blockages.
- **Error Control**: CRC32 checksum appended to the final 4 bytes of every 64-byte frame. Packets failing checksum verification are discarded immediately.

### 18.2 Frame Packet Structure (Fixed 64-Byte Payloads)

#### Command Frame (Pi 5 → Teensy 4.1)
1. **Header**: 2 Bytes (`0xAA`, `0x55`)
2. **Sequence ID**: 1 Byte (monotonically increasing)
3. **Command Type**: 1 Byte (`0x01`=MOVE, `0x02`=GRASP, `0x03`=RELEASE, `0x04`=ESTOP, `0x05`=HEARTBEAT)
4. **Target Positions**: 24 Bytes (6 x `float32` joint angles in radians)
5. **Velocity Scale**: 4 Bytes (`float32` scaling factor 0.0 to 1.0)
6. **Acceleration Limit**: 4 Bytes (`float32` joint acceleration limit)
7. **Force Target**: 4 Bytes (`float32` gripper force target)
8. **System FSM State**: 1 Byte (state enum value)
9. **Padding**: 23 Bytes (reserved)
10. **CRC32**: 4 Bytes (CRC checksum of bytes 0–59)

#### Telemetry Frame (Teensy 4.1 → Pi 5)
1. **Header**: 2 Bytes (`0xAA`, `0x55`)
2. **Echo Sequence ID**: 1 Byte
3. **Control State**: 1 Byte (Embedded State Enum)
4. **Fault Code**: 1 Byte (0 = OK, non-zero matches fault list)
5. **Current Positions**: 24 Bytes (6 x `float32` angles in radians)
6. **Current Velocities**: 24 Bytes (6 x `float32` speeds in rad/s)
7. **Gripper Force**: 4 Bytes (`float32` actual load cell force in N)
8. **IMU Orientation**: 6 Bytes (3 x `int16` scaled pitch/roll/yaw)
9. **Padding**: 1 Byte
10. **CRC32**: 4 Bytes (CRC checksum of bytes 0–59)

---

## 19. Detailed Session, Identity & Conversational Logic

### 19.1 Two-Layer Biometric Identity Model
- **Layer 1: Initial Login**:
  - Always-on background MediaPipe FaceDetection scans for human faces.
  - Matches face image against stored profiles using InsightFace `buffalo_sc` (threshold = 0.78).
  - Prompts identified user: `"Welcome, {name}. Say confirm to log in."`
  - User says "confirm" -> voice biometric d-vector extracted using SpeechBrain ECAPA-TDNN ONNX model.
  - Computes cosine similarity (threshold = 0.85). If both checks pass, a session is created with a 2-hour TTL and 5-minute inactivity timer.
- **Layer 2: Active Session Consistency**:
  - Every subsequent spoken command is sampled for speaker identification.
  - Extracts voice d-vector from the current command's audio transcript.
  - Compares embedding against the logged-in user profile only (not all enrolled profiles).
  - If 3 consecutive commands fail this voice consistency check, a re-verification prompt is issued. The pending intent is retained in memory.

### 19.2 Voice & Dialogue Processing Pipeline
- **VAD Processing**: Silero VAD listens on the microphone in 32ms chunks.
- **STT Processing**: Deepgram Nova-2 streaming WebSocket client runs in a background thread. `endpointing=300ms` and `utterance_end_ms=1000` ensure minimal latency.
- **Normaliser & Alias Expansion**:
  - normaliser.py cleans transcripts, stripping filler words ("um", "uh", "please").
  - alias_expansion.py maps aliases ("snips", "cutting tool") to canonical targets ("scissors") using word-boundary regex checks.
- **Intent Parsing**:
  - Bypasses the LLM using regex (`fast_intent.py`) for common operations.
  - Falls back to Groq llama-3.1-8b-instant in JSON mode for complex intents. Confidence scores < 0.8 trigger a clarification dialog loop using `openai/gpt-oss-120b`.
- **Speech Synthesis (TTS)**:
  - Microphone is muted during playback; a 300ms silence buffer follows audio outputs.
  - Cloud Edge-TTS acts as primary engine; Kokoro ONNX acts as local offline fallback; offline `pyttsx3` is reserved for safety/ESTOP messages.

---

## 20. Detailed Vision & Localisation Algorithms

### 20.1 Object Detection & Preprocessing
- **Low-Light Preprocessing**: Converts frames to LAB color space, applies CLAHE (clipLimit=2.0, tileGridSize=(8,8)) to the L channel, and converts back to BGR.
- **Confidence Toggles**: Gray frame average brightness < 80 triggers low-light mode:
  - Confidence threshold drops from 0.70 to 0.60.
  - Temporal consistency viewpoints count increases from 2 to 3.
- **Inference**: runs `YOLO26ONNX` (NMS-free, 320x320 input). Merges detections across 3 viewpoints using IoU-based deduplication (threshold = 0.5).

### 20.2 3D Localisation Calculation
Projecting bounding box 2D center pixels $(u, v)$ to robot base coordinates $(X, Y, Z)$:
1. Read median depth value $Z$ from a 40x40 pixel window around the bounding box center in the depth frame.
2. Back-project using pinhole camera intrinsics:
   $$X = \frac{(u - c_x) \times Z}{f_x}$$
   $$Y = \frac{(v - c_y) \times Z}{f_y}$$
3. Transform the camera coordinate $[X, Y, Z, 1]^T$ to the robot base frame using the 4x4 homogeneous transformation matrix $T_{\text{robot\_camera}}$.

### 20.3 Hand Tracking & Handover Z-offsets
- MediaPipe Hands is active *only* in the `HANDOVER` state (runs sequentially, never concurrently with YOLO).
- Palm center calculated by averaging the wrist and four MCP landmarks.
- Hand approach depth tracked along the base coordinate X-axis.
- Voice commands "lower" and "higher" adjust the handover height by ±5cm, clamping to a ±15cm envelope. User preferences are stored in SQLite `users.db`.

### 20.4 Fake Object Rejection
Dual-signal validation algorithm implemented in `fake_detector.py`:
- **Signal 1**: Laplacian variance of the RGB bounding box grayscale ROI ($V_{\text{texture}} = \text{Var}(\text{Laplacian}(\text{ROI}))$). Rejected if $V_{\text{texture}} < 120.0$.
- **Signal 2**: Variance of the depth frame pixels in the ROI. Rejected if $V_{\text{depth}} < 0.002\text{ m}^2$.
- Both signals must trigger to flag the object as a fake. If depth data is missing, the system falls back to texture validation only.

---

## 21. Detailed Task Planner & Analytical IK Formulations

### 21.1 Analytical Inverse Kinematics
Given target position $(x, y, z)$ and tool orientation in the robot base frame:
1. **Joint 1 (Base Rotation)**:
   $$\theta_1 = \text{atan2}(y, x)$$
2. **Joints 2 and 3 (Planar 2-Link)**:
   Calculated using the law of cosines based on upper arm length $L_2$ (400mm), forearm length $L_3$ (400mm), and base height $L_1$ (352mm). Solved for the elbow-up configuration to prevent table collisions.
3. **Joints 4, 5, and 6 (Spherical Wrist)**:
   Computes roll, pitch, and yaw tool orientation. Joint 5 is locked to align the tool tip vertically for top-down grasps.
4. **Validation**: Analytical solutions are clamped against joint limits. The solver returns `IKResult` containing a reachability flag. Unreachable targets are rejected before commands are sent.

### 21.2 Planner Execution Loop
Orchestrated by `planner_node.py` in a background thread:
1. **Phase 0**: Validate world safety severity, network connectivity, and camera status.
2. **Phase 1**: Send `GRIPPER_OPEN` and verify the gripper force sensor drops to zero.
3. **Phase 2**: Call `AgenticPlanner` to propose a search strategy, dispatch a search request to `vision_node`, and wait for `VisionResult`.
4. **Phase 3**: Solve IK for the pre-grasp position (grasp_point + 5cm in Z). Validate the move with `SafetyKernel.validate_move()` and move the arm (velocity scale $\times$ 0.8).
5. **Phase 4**: Move to the grasp position (velocity scale $\times$ 0.5), close the gripper (`GRASP` at 3.0N), and verify gripper force $\ge$ 1.0N.
6. **Phase 5**: Move to the handover position (velocity scale $\times$ 0.6) and transition to `HANDOVER`.
7. **Phase 6**: Execute the 3-gate handover protocol. Upon validation, command `RELEASE` and wait for force to drop to zero.
8. **Phase 7**: Update the Bayesian probability map, log latency metrics, and return to `STANDBY`.

---

## 22. Detailed Emergency Stop & LiDAR Safety Systems

### 22.1 Emergency Stop (ESTOP) Pipeline
ESTOP interrupts all motion and transitions the robot to the `ESTOP` state.
- **Hardware Button**: Direct hardware cut to motor driver enable lines. Instant PWM stop.
- **Software Traversal (Soft ESTOP)**: Triggered by voice keywords, sensor limits, or network timeouts:
  - If `arm_holding` is active, the planner executes a controlled move to the `SAFE_DROP_ZONE` at velocity scale 0.3.
  - Opens the gripper to deposit the tool.
  - Commands the Teensy to disable motor PWM.
  - Broadcasts `EmergencySignal` and plays an alert using the local `pyttsx3` engine.

### 22.2 LiDAR Torso and Proximity Tracking
- Safety node reads Base LiDAR scans on `/scan` at 50Hz.
- Checks proximity in the front 120° arc:
  - Distance > 600mm: Normal operation (velocity scale = 1.0).
  - Distance 400mm–600mm: Caution zone. Logs a warning, sets velocity scale = 0.5, and publishes a WARNING alert.
  - Distance < 400mm: Danger zone. Triggers an immediate ESTOP.
- During the `HANDOVER` state, LiDAR torso proximity detection acts as a trigger to initiate the camera-based face verification search.

---

## 23. Complete Technology Stack & Performance KPIs

### 23.1 High-Level Component & Model Allocations
- **Intent Parsing**: Groq `llama-3.1-8b-instant` in JSON mode.
- **Conversational Assistant**: Groq `llama-3.3-70b-versatile` (LOGGED_OUT chitchat).
- **Agentic Task Planner**: NVIDIA NIM `nvidia/llama-3.3-nemotron-super-49b-v1` (primary), falling back to Groq `llama-3.3-70b-versatile`.
- **Dialogue Clarification**: Groq `llama-3.3-70b-versatile`.
- **Speech-to-Text (STT)**: Deepgram Nova-2 streaming WebSocket.
- **Text-to-Speech (TTS)**: Microsoft Edge TTS (cloud), Kokoro ONNX INT8 (local fallback), and pyttsx3 (local offline safety).
- **Voice Biometrics**: SpeechBrain ECAPA-TDNN (192-D speaker embedding).
- **Face Detection**: MediaPipe FaceDetection (always-on passive scan).
- **Face Verification**: InsightFace buffalo_sc (512-D embedding, cosine similarity > 0.78).
- **Object Detection**: YOLO26 ONNX INT8 CPU inference.
- **Hand Tracking**: MediaPipe Hands.
- **Voice Activity Detection**: Silero VAD (32ms chunks).

### 23.2 Performance Key Performance Indicators (KPIs) & Operational Thresholds

To guarantee safe and clinically viable operation in surgical environments, the following quantitative performance targets and operational thresholds are enforced across high-level software, embedded firmware, and physical hardware subsystems:

#### 1. System Latency & Processing KPIs
| Metric | Target | Rationale / Method |
|---|---|---|
| **Emergency Stop (ESTOP) Latency** | < 200 ms | From voice keyword detection / sensor limit hit to motor PWM disable |
| **STT Transcription Endpointing** | 300 ms | Silence threshold to finalize Deepgram WebSocket streaming transcript |
| **Biometric Face Verification** | < 500 ms | InsightFace embedding comparison during login and handover states |
| **Biometric Voice Verification** | < 600 ms | SpeechBrain d-vector ECAPA-TDNN ONNX verification loop |
| **YOLO26 Object Inference** | < 850 ms | Single frame CPU inference time on Raspberry Pi 5 |
| **Inverse Kinematics Resolution** | 0.0000 m | FK/IK analytical round-trip precision tolerance |
| **Agentic Recovery Success Rate** | > 80% | Completed fetch tasks following initial phase failures |

#### 2. Biometric & Vision Thresholds
| Parameter | Value | Configuration Location |
|---|---|---|
| **Voice Biometric Similarity** | $\ge 0.85$ (cosine) | `system.yaml` (`auth.voice_similarity_threshold`) |
| **Face Biometric Similarity** | $\ge 0.78$ (cosine) | `system.yaml` (`auth.face_similarity_threshold`) |
| **YOLO26 Confidence (Normal)** | $\ge 0.70$ | `system.yaml` (`vision.confidence_threshold`) |
| **YOLO26 Confidence (Low Light)** | $\ge 0.56$ | `system.yaml` (`vision.low_light_confidence_threshold`) |
| **Scene Brightness Cutoff (CLAHE)**| < 80.0 (V-mean)| `system.yaml` (`vision.low_light_brightness_cutoff`) |
| **Laplacian Texture Variance** | $\ge 120.0$ | `thresholds.yaml` (`fake_detection.texture_variance_threshold`)|
| **Depth ROI Map Variance** | $\ge 0.002\text{ m}^2$ | `thresholds.yaml` (`fake_detection.depth_variance_threshold`) |

#### 3. Control Loops & Telemetry Rates
| Subsystem Loop | Rate / Period | Mechanism |
|---|---|---|
| **Teensy PID Controllers** | 200 Hz | Position and velocity servo loops on Joint 1 to Joint 6 |
| **Sensor Telemetry Reads** | 100 Hz | Polling joint encoders (AS5600), current shunt, and temperature |
| **Pi-MCU Telemetry Stream** | 50 Hz | Command status packets transmitted over the physical SPI link |
| **LiDAR Proximity Scans** | 50 Hz | `safety_node` processing laser readings on the `/scan` topic |
| **Pi-MCU Heartbeat Keepalive** | 5 Hz (200ms) | SPI watchdog ping; triggers local MCU stop after 500ms failure |

#### 4. Hard Safety Limits & Soft Warnings
| Sensor / Parameter | Warning Threshold | Graded Action / ESTOP Threshold |
|---|---|---|
| **Joint Motor Current** | > 6.0 A | > 8.0 A for > 100ms (cuts motor PWM immediately) |
| **Joint Motor Temperature** | > 55.0°C | > 65.0°C (reduce velocity 50%); > 75.0°C (ESTOP shutdown) |
| **Joint Angular Velocity** | > 80.0 deg/s | > 120.0 deg/s (hard encoder-derivative safety cut) |
| **LiDAR Proximity (Base)** | 400–600 mm | < 400 mm (torso-level proximity emergency stop) |
| **Gripper Contact Force** | > 10.0 N | > 15.0 N (finger-tip load cell emergency cutoff) |
| **Session TTL** | — | 2 hours (7200 seconds max active session duration) |
| **Inactivity Logout** | — | 5 minutes (300 seconds of zero commands in STANDBY) |

---

## Appendix A: Post-Demo Handover Checklist

All 22 bugs from the initial audit are fixed. The following items are calibration tasks, hardware bring-up, and enhancements for the college handover.

### A.1 Physical Calibration (Requires Arm Assembly)

| # | Item | What To Do | Why | Effort |
|---|------|-----------|-----|--------|
| C1 | **Measure T_flange_camera** | Disconnect HP60C bracket. Measure with caliper: forward, sideways, vertical offset from wrist flange to camera lens. Write into `system.yaml` as `camera.T_flange_camera` (4×4 matrix). Default `[0.040, 0, -0.020]` is a CAD guess. | Without this, `compute_T_for_viewpoint()` in `localiser.py` uses wrong offset. Arm misses tools by 2-5 mm. | 10 min |
| C2 | **Calibrate camera intrinsics** | Print 9×6 checkerboard. Take ~20 photos. Run OpenCV `calibrateCamera()`. Update `system.yaml` `camera.fx/fy/cx/cy`. | Wrong intrinsics → pixel-to-3D error grows with distance. 1 pixel ≈ 0.7 mm at 400 mm. | 30 min |
| C3 | **Calibrate DH parameters** | All 6 joints `[FILL_AFTER_ASSEMBLY]`. Move each joint individually, record true vs encoder angle, populate `arm.dh_params[]`. | Without DH: correct position but wrong end-effector orientation. 3D-printed parts have axis misalignments. | 2-3 hrs |
| C4 | **Calibrate NBV viewpoints** | Move arm to each tray zone, record 6 joint angles, add to `vision.viewpoints[]`. Minimum 3 zones. | NBV search needs calibrated viewpoints (masked by scripted demo mode). | 30 min |

### A.2 Hardware Bring-Up (Requires Physical Robot)

| # | Item | What To Do | Why | Effort |
|---|------|-----------|-----|--------|
|| H1 | **SPI wiring + Teensy flash (CRITICAL)** | Wire 4 SPI pins + GND between Pi5 GPIO and Teensy 4.1. Flash `ACARE-6DOF-Teensey4.1_RMCS.ino` (SPI slave fix applied). Code + firmware are complete — physical wiring only. | Without SPI: no motors move. | 30 min |
| H2 | **Motor PID tuning** | RMCS-3002 drivers + BLDC. 200 Hz PID in Teensy firmware. Tune P/I/D per joint. | Untuned PID = jerky motion, arm droops, or oscillation. Can damage gears. | 1-2 days |
| H3 | **AS5600 encoder calibration** | 12-bit magnetic encoders via TCA9548A I2C mux. Offset calibration (physical 0° → electrical 0°). | Wrong offsets → wrong joint position → IK computes wrong angle → arm misses. | 1 hr |
| H4 | **Emergency stop hardware test** | Test physical ESTOP button, firmware watchdog (200 ms), voice keyword (<200 ms). Document results. | Safety certification requires documented ESTOP tests. | 1 hr |

### A.3 Software Enhancements (No Hardware Needed)

| # | Item | What To Do | Why | Effort |
|---|------|-----------|-----|--------|
|| S1 | **Wire dynamic FK extrinsics into NBV** | `localiser.py` has `compute_T_for_viewpoint()` but `nbv_search.py` doesn't pass `T_override`. Add the call. | Object positions in camera frame, not robot frame. Arm moves wrong (masked by demo mode). | 30 min |
|| S2 | **Voice-driven registration** | Add registration state machine to `auth_node.py`. Detect "register me" in LOGGED_OUT, prompt via TTS, auto-capture 10 face + 3 voice samples. | Currently requires CLI terminal. | Medium |
|| S3 | **Offline STT fallback** | Add Vosk/whisper.cpp in `asr.py` when Deepgram fails. | No internet = no voice commands. | Medium |
|| S4 | **ActionServer migration** | Replace timer polling with proper ROS2 ActionServer for preemption/feedback. | Production-grade. Current works for demo. | Large |

### A.4 Documentation & Testing

| # | Item | What To Do | Why | Effort |
|---|------|-----------|-----|--------|
| D1 | **Full dry run on hardware** | Run complete demo on actual Pi 5 + arm + camera + mic. | Simulation vs hardware differ — latency, failures. | 2-3 hrs |
| D2 | **EMI / noise test** | Test BLDC motor EMI on SPI, I2C, USB camera, USB audio. Shield cables, add ferrite beads if needed. | EMI corruption mid-demo = unpredictable behaviour. | 1 day |
| D3 | **Power failure recovery** | Test power loss mid-operation. Verify supervisor power recovery and safe arm stop. | Power failure = dropped tool + frozen arm. | 2 hrs |

---

*Document updated 2026-06-09 — All 22 audit bugs fixed, 15 documentation patches applied.*  
*Document updated 2026-06-11 — +10 additional bugs fixed: C1 (auth demo mode guard), C3 (SafetyKernel target_xyz), C4 (voice launch ordering), H1 (workspace bare except), H3 (ik_reachable), H4 (zones_searched), H5 (motion queue 1→10), H7 (hand_approaching 3-axis), M1 (agent_schema logging), M3/M5 (embedded config+gripper). All 32 bugs fixed.*  
*Document updated 2026-06-12 — Full code audit completed. 4 more msg/env bugs fixed (HandStatus.msg, AuthRequest.msg, intent_parser.py, assistant_agent.py). Pi deployed with interface.mode=hardware. SPI Phase 1: Teensy responsive but echo timing fix needed (double-attachInterrupt bug). See skill `acare-demo-audit` for hardware bring-up status.*  
*Document updated 2026-06-13 — 15 additional bugs fixed: dialogue_node.py clarification loop, camera_probe.py/vision_node.py rclpy.parameter_client, normaliser.py/alias_expansion.py triple alias consolidation, main.py EOFError handler, nbv_search.py inline imports, hand_tracker.py warn(), supervisor.py deprecation, preflight_ros_env.py spidev check, demo_docs.md wrong paths.*


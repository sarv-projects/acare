# ACARE — Complete Project Documentation

**Autonomous Clinical Assistance Robot — Software Layer**

---

## 1. Pi Credentials & Known Hosts

### Credentials

| Field | Value |
|---|---|
| Username | `acare` |
| Password | `acare1234` |
| Hostname | `acare` |
| WiFi | `Airtel_Sarsou` |

### Current IPs

| Network | IP |
|---|---|
| Airtel_Sarsou | `192.168.1.2` |
| sarv_wifi (mobile hotspot) | `10.12.133.174` |

### Known Hosts

| Date | IP | Network | Notes |
|---|---|---|---|
| 2026-05-29 | `10.12.133.174` | sarv_wifi (mobile hotspot) | Confirmed working |
| 2026-05-29 | `192.168.1.2` | Airtel_Sarsou | After reflash, DHCP assigned new IP |
| (old) | `192.168.1.72` | Airtel_Sarsou | Original IP before reflash — no longer valid |
| (old) | `192.168.1.73` | Airtel_Sarsou | Alternate old IP — no longer valid |

### Saved WiFi Networks (in netplan — systemd-networkd)

- `Airtel_Sarsou`
- `sarv_wifi`

**Note:** This Pi uses `systemd-networkd` + netplan (NOT NetworkManager). The `nmcli` command only works if NetworkManager is installed. WiFi networks are stored in `/etc/netplan/50-cloud-init.yaml`.

---

## 2. Software Architecture — Package Map

| Package | Type | Purpose |
|---|---|---|
| `acare_msgs/` | CMake | ROS2 message/service definitions (18 `.msg` + 1 `.srv`). Defines the typed contract between all nodes. |
| `acare_bringup/` | Python | Shared infrastructure: `paths.py` (all file paths), `qos_profiles.py` (per-topic QoS), `config/` (system.yaml, thresholds.yaml, probability_map.yaml), `launch/`, `supervisor.py` (power recovery). |
| `acare_voice/` | Python | Voice pipeline: VAD (Silero) → ASR (Deepgram Nova-2 streaming) → normaliser → alias expansion → intent parser (Groq 8B) → fast_intent (regex) → assistant agent (Groq 70B for LOGGED_OUT conversation) → TTS (edge-tts normal, pyttsx3 urgent) → keyword monitor (ESTOP). Also: `voice_ros_node.py` (ROS2 wrapper), `voice_node.py` (standalone orchestrator), `dialogue_manager.py`, `semantic_turn_detector.py`, `tts_queue.py`, `tts_cache.py`, `earcons.py`. |
| `acare_dialogue/` | Python | ROS2 dialogue node: subscribes to `/raw_transcript`, runs intent parsing + assistant agent, publishes `/intent_result`. Handles pronoun resolution, multi-tool detection, session memory. |
| `acare_auth/` | Python | Biometric authentication: passive face scan (MediaPipe), face verification (InsightFace buffalo_sc), voice verification (ECAPA-TDNN via ONNX), user storage (SQLite), enrolment service. Publishes `/validated_intent` after auth gate passes. |
| `acare_planner/` | Python | Task planner: `state_manager.py` (10-state FSM), `planner_node.py` (full task orchestration), `agentic_planner.py` (NIM Nemotron-49B primary + Groq 70B fallback for reasoning), `agent_schema.py` (Pydantic validation), `handover.py` (3-gate protocol), `ik_solver.py`, `tool_registry.py`. |
| `acare_safety/` | Python | Safety monitoring: LiDAR proximity zones (600mm caution, 400mm ESTOP), MCU telemetry (current, temperature, gripper force), publishes graded `SafetyAlert`. |
| `acare_vision/` | Python | Perception: `vision_node.py` (orchestrator), `yolo_infer.py` (YOLO26 NMS-free ONNX), `nbv_search.py` (Bayesian probability map + next-best-view), `localiser.py` (depth→3D), `hand_tracker.py` (MediaPipe Hands for handover), `fake_detector.py`, `hp60c_camera_node.py`. |
| `acare_logging/` | Python | Audit trail: SQLite database, batched writes, auto-rotation at 200 MB. |
| `acare_embedded_interface/` | Python | Bridge between planner commands (`/arm_command`, `/gripper_command`) and hardware. In simulation: FollowJointTrajectory action client to Gazebo controllers. On real hardware: UART/CAN to Teensy 4.1. |
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
| `config/system.yaml` | Global system configuration |
| `config/thresholds.yaml` | Safety and detection thresholds |
| `config/probability_map.yaml` | Bayesian prior for tool locations |
| `launch/acare.launch.py` | Full system launch file |

### acare_voice/

| File | Description |
|---|---|
| `main.py` | Entry point — instantiates VoiceNode and runs standalone loop |
| `voice_node.py` | Master controller: audio state machine, pipeline orchestration |
| `voice_ros_node.py` | ROS2 wrapper — bridges standalone voice pipeline to ROS2 topics |
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
| `dialogue_node.py` | ROS2 node: subscribes `/raw_transcript`, publishes `/intent_result` |
| `__init__.py` | Package init |

### acare_auth/

| File | Description |
|---|---|
| `auth_node.py` | ROS2 auth node: orchestrates face + voice verification |
| `face_detect.py` | MediaPipe face detection (passive scan) |
| `verify_face.py` | InsightFace buffalo_sc face embedding comparison |
| `verify_voice.py` | ECAPA-TDNN ONNX voice embedding comparison |
| `storage.py` | SQLite user database (embeddings, metadata) |
| `export_ecapa_onnx.py` | One-time script to export ECAPA-TDNN to ONNX |
| `__init__.py` | Package init |

### acare_planner/

| File | Description |
|---|---|
| `state_manager.py` | 10-state FSM with all valid transitions |
| `planner_node.py` | ROS2 node: full task orchestration from intent to completion |
| `agentic_planner.py` | LLM-based reasoning (NIM Nemotron-49B primary, Groq 70B fallback) |
| `agent_schema.py` | Pydantic models for validating LLM planner output |
| `handover.py` | 3-gate handover protocol (face + palm + voice) |
| `ik_solver.py` | Inverse kinematics solver (placeholder DH params) |
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
| `localiser.py` | Depth-to-3D projection (camera intrinsics + extrinsics) |
| `hand_tracker.py` | MediaPipe Hands for palm detection during handover |
| `fake_detector.py` | Synthetic detector for testing without camera |
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
| `admin_cli.py` | CLI tool for staff enrolment, key management, calibration |
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
| `/robot_state` | `RobotState` | StateManager | All nodes | RELIABLE + TRANSIENT_LOCAL |
| `/state_transition` | `StateTransition` | AuthNode, PlannerNode | StateManager | RELIABLE |
| `/safety_alert` | `SafetyAlert` | SafetyNode, VoiceNode | StateManager, PlannerNode | RELIABLE + TRANSIENT_LOCAL |
| `/emergency_stop` | `EmergencySignal` | VoiceNode | EmbeddedInterface, StateManager | RELIABLE |
| `/raw_transcript` | `Transcript` | VoiceNodeROS | DialogueNode, AuthNode | RELIABLE |
| `/intent_result` | `Intent` | DialogueNode | AuthNode | RELIABLE |
| `/validated_intent` | `ValidatedIntent` | AuthNode | PlannerNode | RELIABLE |
| `/auth_result` | `AuthResult` | AuthNode | StateManager, PlannerNode | RELIABLE |
| `/tts_request` | `String` | StateManager, PlannerNode, AuthNode, DialogueNode | VoiceNodeROS | RELIABLE |
| `/vision_search_request` | `VisionSearchRequest` | PlannerNode | VisionNode | RELIABLE |
| `/vision_result` | `VisionResult` | VisionNode | PlannerNode, DialogueNode | RELIABLE |
| `/vision_status` | `VisionStatus` | VisionNode | PlannerNode | RELIABLE |
| `/hand_status` | `HandStatus` | VisionNode | PlannerNode | RELIABLE |
| `/arm_command` | `ArmCommand` | PlannerNode | EmbeddedInterface | RELIABLE |
| `/gripper_command` | `GripperCommand` | PlannerNode | EmbeddedInterface | RELIABLE |
| `/motion_feedback` | `MotionFeedback` | EmbeddedInterface | PlannerNode, SafetyNode, VisionNode | BEST_EFFORT |
| `/log_event` | `LogEvent` | PlannerNode, VisionNode | LogNode | BEST_EFFORT |
| `/scan` | `LaserScan` | LiDAR driver | SafetyNode | BEST_EFFORT |

### Camera Topics

| Topic | Type | Source |
|---|---|---|
| `/ascamera_hp60c/camera_publisher/rgb0/image` | `Image` (BGR8) | HP60C driver |
| `/ascamera_hp60c/camera_publisher/depth0/image_raw` | `Image` (16UC1) | HP60C driver |
| `/ascamera_hp60c/camera_publisher/rgb0/camera_info` | `CameraInfo` | HP60C driver |
| `/ascamera_hp60c/camera_publisher/depth0/camera_info` | `CameraInfo` | HP60C driver |

---

## 5. Data Flow — End-to-End Pipeline

**Scenario:** Surgeon says "fetch scissors" → tool delivered to hand.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  1. Mic → VAD (Silero) → Deepgram Nova-2 streaming → raw transcript    │
│  2. Transcript → DialogueNode → normalise → alias expand → intent parse│
│  3. Intent → AuthNode → voice verify → /validated_intent               │
│  4. ValidatedIntent → PlannerNode → state transition to PROCESSING     │
│  5. Planner → /vision_search_request → VisionNode                      │
│  6. VisionNode → YOLO detect → localise 3D → /vision_result            │
│  7. Planner → IK solve → /arm_command → EmbeddedInterface → motors     │
│  8. Planner → /gripper_command → grasp → /motion_feedback confirms     │
│  9. Planner → state HOLDING → HANDOVER                                 │
│ 10. HandoverProtocol: face check + palm detection + voice confirm       │
│ 11. Gripper release → state STANDBY                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step-by-step detail:

1. **Mic → VAD → ASR:** Silero VAD detects speech onset in 32 ms chunks. Audio streams to Deepgram Nova-2 via WebSocket. Final transcript emitted on `/raw_transcript`.

2. **Transcript → Intent:** DialogueNode normalises text (lowercase, strip fillers), expands aliases ("blade" → "scalpel"), then calls Groq 8B for structured intent extraction. If regex fast_intent matches first, LLM call is skipped.

3. **Intent → Auth gate:** AuthNode checks if the speaker is authenticated. If not, triggers voice verification (ECAPA-TDNN cosine similarity). On pass, publishes `/validated_intent`.

4. **Validated intent → Planner:** PlannerNode receives the validated intent, requests state transition to PROCESSING via `/state_transition`.

5. **Planner → Vision search:** PlannerNode publishes a `VisionSearchRequest` with the target tool name. VisionNode begins searching.

6. **Vision detection:** VisionNode runs YOLO26 inference on RGB frames. On detection, `localiser.py` projects the 2D bounding box centre into 3D using depth data and camera intrinsics. Result published on `/vision_result`.

7. **Motion planning:** PlannerNode receives 3D coordinates, runs IK solver to compute joint angles, publishes `ArmCommand` to EmbeddedInterface. The interface sends serial commands to Teensy 4.1 (or Gazebo action in simulation).

8. **Grasp:** PlannerNode sends `GripperCommand` (close). EmbeddedInterface confirms grasp via `/motion_feedback`.

9. **State transitions:** Planner moves through HOLDING → HANDOVER states.

10. **Handover protocol (3 gates):**
    - Gate 1 (advisory): Face detected in front of robot
    - Gate 2 (required): Palm detected open and stable
    - Gate 3 (required): Voice confirmation ("yes" / "ready")

11. **Release:** Gripper opens, tool transferred. State returns to STANDBY.

---

## 6. Where Embedded/Hardware Fits

```
┌──────────────────────────────────────────────────────────────────┐
│                    SOFTWARE (Raspberry Pi 5)                       │
│  All ROS2 nodes, AI inference, voice, vision, planning            │
│                                                                    │
│  embedded_interface_node.py  ←── ONLY point of contact            │
└──────────────────┬───────────────────────────────────────────────┘
                   │  UART / CAN bus
┌──────────────────▼───────────────────────────────────────────────┐
│                   EMBEDDED (Teensy 4.1)                            │
│  PID motor control, safety ISRs, CAN/UART bridge, heartbeat       │
└──────────────────────────────────────────────────────────────────┘
```

### Boundary rules:

- **Software (Pi 5):** All ROS2 nodes, AI inference (YOLO, LLMs, ECAPA-TDNN), voice pipeline, vision pipeline, task planning, state management.
- **Embedded (Teensy 4.1):** PID motor control loops (1 kHz), hardware safety ISRs (overcurrent, overtemp, limit switches), CAN/UART bridge, heartbeat watchdog.
- **`embedded_interface_node`** is the ONLY point of contact between software and firmware. No other node communicates with hardware directly.
- **In simulation:** The interface talks to Gazebo controllers via `FollowJointTrajectory` action client. No serial port needed.
- **On real hardware:** The interface sends serial commands to Teensy and reads telemetry back (joint positions, currents, temperatures, gripper force).
- **Safety is enforced INDEPENDENTLY on both sides:**
  - Software: `SafetyNode` monitors LiDAR + telemetry, can trigger ESTOP via `/emergency_stop`
  - Firmware: ISRs cut motor power directly on overcurrent/overtemp — no software involvement needed

---

## 7. LLM Model Allocation

| Component | Provider | Model | Purpose |
|---|---|---|---|
| Dialogue (conversation) | Groq | `llama-3.3-70b-versatile` | Fast user-facing responses |
| Intent parsing | Groq | `llama-3.1-8b-instant` | Simple JSON extraction |
| Agentic planner (primary) | NVIDIA NIM | `nvidia/llama-3.3-nemotron-super-49b-v1` | Deep reasoning for recovery |
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
cd ~/acare_ws && colcon build --symlink-install && source ~/.bashrc
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

### Add WiFi network (safe method — never edit netplan)
```bash
sudo nmcli connection add \
  type wifi \
  con-name "NetworkName" \
  ssid "SSID" \
  wifi-sec.key-mgmt wpa-psk \
  wifi-sec.psk "Password" \
  connection.autoconnect yes \
  connection.autoconnect-priority 10
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
- Voice pipeline: VAD + Deepgram STT + Groq intent + Edge-TTS confirmed working
- Vision: YOLO26 detecting objects on Pi at ~850 ms/frame confirmed
- Camera: HP60C RGB+Depth streaming confirmed (640×480, 12.4 Hz)
- Auth: full biometric flow implemented, `demo_mode` bypass working
- Embedded interface: Gazebo bridge + real-hardware stub ready
- State machine: 10-state FSM with all transitions
- Safety: LiDAR + telemetry monitoring
- Logging: SQLite audit trail with batched writes
- Bayesian probability map: persistence + clamping
- Handover: 3-gate protocol (face + palm + voice)
- ESTOP: <200 ms keyword detection on dedicated thread

### Left to do ✗

- USB sound card for Pi mic input (3.5 mm mic won't work directly)
- Depth localisation: sparse depth issue (likely hand-holding camera — needs stable mount)
- Camera-to-robot extrinsics calibration (`T_robot_camera` is identity placeholder)
- DH parameters for IK solver (placeholder zeros)
- Teensy firmware integration (UART/CAN protocol)
- Real arm assembly + motor wiring
- NVIDIA NIM API key setup
- ECAPA-TDNN ONNX export (run `export_ecapa_onnx.py` once on a dev machine)
- Production `.env` with real keys on Pi
- Full end-to-end integration test with all nodes running simultaneously

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
- Firmware-limited to **15 N** (hardware safety)
- Software warns at **10 N** (publishes SafetyAlert)

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

*Last updated: 2026-05-30*

---

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
Must exist at `acare_software_final\acare_voice\.env`:
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

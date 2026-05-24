# ACARE
## Autonomous Clinical Assistance Robot with Multimodal Biometric Authentication and Dynamic Human Handover

---

| Field | Details |
|---|---|
| Institution | Ramaiah Institute of Technology, Bengaluru |
| Department | Electronics and Communication Engineering |
| Guide | Dr. Lakshmi Shrinivasan, Associate Professor |
| Team | Sathvik Rao · Sarvesh Bhattacharyya · Shreevanth M · Shreyas S |
| Funding | ₹40,000 — Institutional Grant |
| Status | Active Development — April 2026 |

---

## DOMAIN MAP

| Domain | Scope |
|---|---|
| SOFTWARE | AI pipelines, ROS2 nodes, orchestration, admin CLI |
| HARDWARE | Mechanical, electrical, power, physical components |
| EMBEDDED / FIRMWARE | Teensy 4.1 motor control, sensor ISR loops, PID |
| INTEGRATION BOUNDARY (SOFTWARE + ELECTRONICS/EMBEDDED) | Protocol contracts between software and embedded |

---

## TABLE OF CONTENTS

- Section I — Project Overview
- Section II — Hardware Architecture
- Section III — Embedded Firmware — Teensy 4.1 / Cortex-M4 + ESP32
- Section IV — Software ↔ Embedded Integration Boundary
- Section V — ROS2 Software Architecture
- Section VI — Global Robot State Machine
- Section VII — Identity & Session Management
- Section VIII — Voice Orchestration Layer
- Section IX — Voice Command Pipeline
- Section X — Conversational Layer — LangGraph + Assistant Agent
- Section XI — Vision Pipeline — NBV Search & Detection
- Section XII — Task Planner Pipeline
- Section XIII — Emergency Stop System
- Section XIV — LiDAR Safety System
- Section XV — Response Generator — TTS
- Section XVI — Logging & Audit Trail
- Section XVII — Startup, Shutdown & Power Recovery
- Section XVIII — Admin CLI & Calibration
- Section XIX — Configuration Files
- Section XX — Directory Structure
- Section XXI — Complete Technology Stack
- Section XXII — Performance KPIs
- Section XXIII — Preliminary Work Status — March 2026
- Section XXIV — Supplementary Implementation Details
- Section XXV — Commercial Applications & Future Work
- Section XXVI — Complete System Flow & Final Decisions (Full Operational Reference)

---

## SECTION I — PROJECT OVERVIEW

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

These two layers communicate via CAN bus (preferred) or UART. All AI and software pipelines are isolated from hardware control.

- SOFTWARE — Raspberry Pi 5 + ROS2 + Python AI Nodes
- EMBEDDED / FIRMWARE — Teensy 4.1 / Cortex-M4 + ESP32 + PID + Safety ISR
- HARDWARE — 6-DOF Arm + Sensors + Power System

### Key Differentiation vs Prior Art

Unlike MOXI, TIAGo, TUG, or LIO, ACARE integrates multimodal biometric authentication (voice + face), voice-driven instrument retrieval with structured intent parsing, adaptive probabilistic vision search, and dynamic human-robot handover with real-time palm tracking — all within a layered safety architecture that separates high-level intelligence from deterministic motor control.

### Section I-B — System Assumptions & Prerequisites

**Network**

- ACARE requires stable internet connectivity during operation
- Two cloud services are mandatory: Deepgram Nova-2 (STT streaming WebSocket) and Groq API (intent parsing)
- Microsoft Edge TTS API required for natural voice responses
- If connectivity drops mid-session: voice commands stop processing; system transitions to STANDBY or ESTOP (safe deposit if holding)
- There is no offline fallback mode by design. The system either works fully or stops cleanly. Degraded mode does not exist.
- A stable Wi-Fi connection at the deployment site is a prerequisite. Mobile hotspot recommended as backup for demo.

**Power**

- Continuous 24V motor supply required
- 5V regulated logic supply required
- Power failure triggers recovery sequence on reboot

**Physical**

- Fixed workspace — robot does not navigate
- SAFE_DROP_ZONE and handover zone positions fixed at calibration
- Staff must approach from designated handover direction

### Future Work Preview

Long-term extensions include integration with hospital automation systems, smart operating room orchestration, and expansion to multi-robot clinical assistance fleets. See Section XXV for detailed commercial roadmap.

---

## SECTION II — HARDWARE ARCHITECTURE

> **HARDWARE** — All mechanical design, fabrication, PCB design, power electronics, and physical sensor mounting falls under the Hardware domain.

### Mechanical Structure

- 6-DOF serial robotic arm
- Custom 3D printed cycloidal gearboxes — 22:1 ratio at shoulder, 15:1 at elbow
- Gearbox ratios for wrist joints 4, 5, 6: [PLACEHOLDER — confirm with hardware team]
- Material: PETG high infill for gearbox bodies; aluminium sheet metal for structural load-bearing links
- Radial bearings at all rotating joints
- Precision gripper mechanism with integrated force sensor
- Bowden line pulley system for wrist actuation
- Fixed handover zone — staff approaches and receives tool directly from gripper; position encoded in config
- Fixed SAFE_DROP_ZONE — predefined emergency deposit surface on table; (x, y, z) stored in config
- Base fixation method: [PLACEHOLDER — bolted to table / clamped / weighted base — confirm]

### Joint Parameters — Required from Hardware Team

> **CRITICAL:** IK solver and planner_node cannot be built without these values.

| Joint | Name | Min Angle (rad) | Max Angle (rad) | Max Velocity (rad/s) | Home Position (rad) | Gear Ratio |
|---|---|---|---|---|---|---|
| Joint 1 | Base Rotation | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | 0.0 | [PLACEHOLDER] |
| Joint 2 | Shoulder | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | 20:1 |
| Joint 3 | Elbow | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | 15:1 |
| Joint 4 | Wrist Pitch | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | 0.0 | [PLACEHOLDER] |
| Joint 5 | Wrist Roll | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | 0.0 | [PLACEHOLDER] |
| Joint 6 | Gripper Rotate | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | 0.0 | [PLACEHOLDER] |

### Link Lengths — Required from Hardware Team

| Link | Description | Length (metres) |
|---|---|---|
| Base height | Base to shoulder joint (vertical) | [PLACEHOLDER] |
| Upper arm | Shoulder to elbow | [PLACEHOLDER] |
| Forearm | Elbow to wrist | [PLACEHOLDER] |
| Wrist | Wrist joint to gripper mount | [PLACEHOLDER] |
| Gripper | Gripper mount to fingertips | [PLACEHOLDER] |
| Total reach | Maximum horizontal reach | [PLACEHOLDER] |

### DH Parameters — Required from Hardware Team

Denavit-Hartenberg parameters needed for IK solver. Fill in after assembly.

| Joint | a (m) | alpha (rad) | d (m) | theta offset (rad) |
|---|---|---|---|---|
| 1 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| 2 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| 3 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| 4 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| 5 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| 6 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### Workspace Validation

Defined workspace: xmin: -0.4m to xmax: 0.4m, ymin: -0.3m to ymax: 0.3m, zmin: 0.0m to zmax: 0.5m.

Workspace reachability confirmation: [PLACEHOLDER — verify arm can physically reach all corners of defined workspace after assembly]

### Gripper Specifications

| Parameter | Value |
|---|---|
| Type | Parallel jaw |
| Finger material | [PLACEHOLDER] |
| Maximum jaw opening | [PLACEHOLDER] mm |
| Default grasp width | 25 mm (most tools) |
| Open width | 45 mm |
| Closed width | 0 mm |
| Force control mode | Yes — not simple open/close |
| Force target (normal grasp) | 3–5 N |
| Force warning threshold | 10 N |
| Force ESTOP threshold | 15 N |
| Tool retention during transport | [PLACEHOLDER — friction / mechanical lock / force hold] |
| Open time | ~500 ms |
| Close time | ~500 ms |

### Weight and Load

- Estimated arm weight: [PLACEHOLDER — total arm weight in kg]
- Maximum payload at end-effector: [PLACEHOLDER — kg, confirm motors can handle]
- Per-link weight distribution: [PLACEHOLDER]

### Actuators

- BLDC motors: 1.4 Nm Rhino Planetary Gearbox BLDC — base, shoulder, elbow joints (×3)
- Additional BLDC motors for wrist and gripper actuation
- Gripper motor controlled in force mode — not position mode
- Motor driver: [RMCS-3002l]
- Motor driver communication to Teensy: [Modbus ASCII]
- Current sensing method: [PLACEHOLDER — shunt resistor / hall sensor]

### Sensors — Full List

| Sensor | Model / Type | Location | Domain |
|---|---|---|---|
| RGBD Depth Camera | YDLIDAR HP60C | Wrist-mounted | Hardware / Software |
| Safety LiDAR | YDLIDAR T-mini-Plus | Base-mounted ~80cm | Hardware / Software |
| Joint Encoders | AS5600 Magnetic Encoder ×6 | Each joint | Hardware / Embedded |
| IMU | On MCU board | Arm base | Hardware / Embedded |
| Joint Current Sensors | Per motor phase | Motor driver board | Hardware / Embedded |
| Temperature Sensors | Per joint motor | Joint housings | Hardware / Embedded |
| Gripper Force Sensor | Analog force sensing | Gripper fingertips | Hardware / Embedded |
| Microphone | [PLACEHOLDER — model, polar pattern, USB/3.5mm] | Fixed mount near workspace | Hardware / Software |
| Speaker | [PLACEHOLDER — model, amplifier if any] | [PLACEHOLDER — mounting location] | Hardware / Software |
| I2C Multiplexer | TCA9548A | MCU board | Hardware / Embedded |

### Camera Interface

- YDLIDAR HP60C connection to Pi: [PLACEHOLDER — USB3 / proprietary — confirm interface]
- ROS2 driver package for HP60C: [PLACEHOLDER — confirm package name]
- YDLIDAR T-mini Plus connection to Pi: [PLACEHOLDER — USB / Serial — confirm]
- ROS2 driver package for T-mini Plus: [PLACEHOLDER — confirm package name]

### Microphone Specification

- Model: [PLACEHOLDER]
- Polar pattern: [PLACEHOLDER — cardioid / supercardioid recommended for OT noise rejection]
- Connection type: [PLACEHOLDER — USB / 3.5mm / XLR]
- Distance from speaker: [PLACEHOLDER — ensure sufficient separation to prevent feedback]

### Speaker Specification

- Model: [PLACEHOLDER]
- Amplifier: [PLACEHOLDER — if required]
- Mounting location: [PLACEHOLDER — near workspace, facing staff area]
- Volume requirement: sufficient to be heard in active OT environment over monitor beeps

### Cable Management

- Wrist camera cable routing: [PLACEHOLDER — flex-rated cable required through rotating joints]
- Encoder cable routing: [PLACEHOLDER — per joint, shielded recommended]
- Motor power cable gauge: [PLACEHOLDER — sized for 8A continuous per motor]
- Emergency stop button cable: direct hardwire to motor driver enable pin, no software path

### Power System

- Motor supply: 24V dedicated rail — powers all BLDC motors and motor drivers
- Logic supply: 5V regulated — powers Raspberry Pi 5, isolated from motor rail
- MCU supply: 5V or 3.3V from onboard regulator
- Common ground across all supplies — mandatory for signal integrity
- Fuse on motor supply rail — overcurrent protection
- Reverse polarity protection on all input rails
- Surge protection — motor switching transients isolated from logic supply
- EMI filtering between motor supply and Pi supply — implementation: [PLACEHOLDER — ferrite beads / LC filter / isolated transformer]
- Hardware emergency cutoff relay — physical red button wired directly to motor driver enable pin, cuts 24V immediately, independent of all software
- XT30 male connectors for battery/PSU to motor controller connections

### Connector Specifications

| Connection | Connector Type | Notes |
|---|---|---|
| Motor rail to driver | XT30 male/female | 24V, high current rated |
| Encoder to TCA9548A | [PLACEHOLDER] | I2C, shielded cable |
| Camera (HP60C) to Pi | [PLACEHOLDER] | USB3 / proprietary |
| LiDAR to Pi | [PLACEHOLDER] | USB / Serial |
| ESTOP button | Direct hardwire | To motor driver enable pin |
| Pi to MCU (CAN) | [PLACEHOLDER] | Galvanic isolation between Pi and MCU |
| CAN bus termination | [PLACEHOLDER] | 120 ohm termination resistors at both ends |

### Thermal Management

- Raspberry Pi 5 cooling: active fan required — confirmed risk of thermal throttling under full load
- Pi 5 thermal test: must run under full load (YOLOv11 + SpeechBrain + ROS2 + TTS) for 30 minutes before demo — confirm no throttling
- Motor housing ventilation: [PLACEHOLDER — confirm passive or active cooling per motor]
- Enclosure thermal design: [PLACEHOLDER — if enclosed, ensure airflow]

### Physical Layout Constraints

- SAFE_DROP_ZONE: flat horizontal surface within arm reach, defined during calibration, stored in config as (x, y, z)
- Handover zone: fixed position, staff approaches from designated direction and receives directly from gripper
- LiDAR mounted at approximately 80cm height — scans horizontal plane at torso level
- Camera wrist-mount angle: calibrated during setup, extrinsics stored in config
- Arm base mounting: [PLACEHOLDER — how base is fixed to table/surface]

---

## SECTION III — EMBEDDED FIRMWARE — Teensy 4.1 / Cortex-M4 + ESP32

> **EMBEDDED / FIRMWARE** — All firmware, PID implementation, ISR routines, watchdog logic, and calibration sequences fall under the Embedded domain.

### MCU Selection

Teensy 4.1 selected for current implementation — Cortex-M7 at 600MHz. Final target is a custom PCB integrating Cortex-M4 for motor control and ESP32 for Pi communication only. ESP32 not used for motor control — WiFi jitter is incompatible with deterministic PID.

### PCB Design Specification

- Custom PCB status: [PLACEHOLDER — in progress]
- MCU: Cortex-M4 for motor control
- WiFi/BT: ESP32 for Pi communication only
- Layer count: [PLACEHOLDER]
- Connector types: [PLACEHOLDER]
- Galvanic isolation: [PLACEHOLDER — how implemented between Pi and MCU]
- Schematic reference: [PLACEHOLDER — attach or link schematic]

### Control Loop Architecture

| Loop | Frequency | Responsibility |
|---|---|---|
| Velocity PID | 200 Hz | Motor velocity regulation from position derivative |
| Position PID | 200 Hz | Joint angle tracking from encoder feedback |
| Sensor Read | 100 Hz | Encoder, current, temperature, gripper force, IMU |
| Status Publish to Pi | 50 Hz | JSON status packet over CAN/UART |
| Heartbeat Check | 5 Hz | Verify Pi heartbeat received within 500ms window |

### Per-Joint Control Stack

```
Position PID → Velocity PID → Frequency → Motor driver → BLDC motor
     ↑ Encoder feedback + Current feedback
```

### PID Parameters — Initial Values

> Note: these are starting values for tuning. Final values determined empirically after assembly.

| Joint | Position Kp | Position Ki | Position Kd | Velocity Kp | Velocity Ki | Velocity Kd |
|---|---|---|---|---|---|---|
| Joint 1 (Base) | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Joint 2 (Shoulder) | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Joint 3 (Elbow) | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Joint 4 (Wrist Pitch) | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Joint 5 (Wrist Roll) | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Joint 6 (Gripper) | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

- Anti-windup strategy: [PLACEHOLDER — clamping / back-calculation]
- Feed-forward terms: [PLACEHOLDER — gravity compensation per joint]
- PWM carrier frequency: [PLACEHOLDER — kHz]
- PWM resolution: [PLACEHOLDER — bits]
- FOC switching frequency: [PLACEHOLDER — kHz]
- Dead time for complementary outputs: [PLACEHOLDER — ns]

### Encoder Reading Implementation

- I2C clock speed for AS5600: [PLACEHOLDER — Hz, typically 400kHz]
- Address assignment per TCA9548A channel: [PLACEHOLDER — channel 0 = joint 1, etc.]
- Read method: [PLACEHOLDER — interrupt-driven / polling at 100Hz]
- Encoder count to angle conversion: `angle_rad = (raw_count / 4096) × 2π`
- Zero position calibration storage: [PLACEHOLDER — EEPROM / Flash — location and format]
- Exponential moving average filter on encoder: `filtered = 0.7 × raw + 0.3 × prev`

### Embedded Internal State Machine

| State | Description | Allowed Transitions |
|---|---|---|
| IDLE | Powered, no commands, holding position | → POSITION_CONTROL, → CALIBRATION |
| POSITION_CONTROL | Executing joint position targets from Pi | → GRIPPER_CONTROL, → ESTOP, → FAULT, → IDLE |
| GRIPPER_CONTROL | Force-mode gripper operation | → POSITION_CONTROL, → ESTOP, → FAULT |
| ESTOP | PWM disabled, motors free or braked | → IDLE (only after CLEAR_FAULT from Pi) |
| FAULT | Unrecoverable hardware fault detected | → ESTOP, requires admin reset |
| CALIBRATION | Joint homing sequence | → IDLE on completion |

### Firmware Safety Protections — Non-Negotiable

- Current clamp: if joint_current > 8A for >100ms → ESTOP
- Thermal shutdown: if joint_temp > 65°C → reduce velocity 50%. If temp > 75°C → ESTOP
- Encoder soft limits: if encoder value exceeds mechanical boundary → ESTOP
- Watchdog timer: firmware hang → MCU hardware reset
- Pi heartbeat watchdog: no heartbeat for 500ms → disable all PWM → ESTOP
- Hardware ESTOP pin: physical red button → cuts PWM immediately at hardware level
- Boot calibration timeout: if joint does not reach limit switch within [PLACEHOLDER] seconds → FAULT

### Fault Code Definitions

| fault_code | Meaning | Recovery |
|---|---|---|
| 0 | OK — no fault | — |
| 1 | Overcurrent — joint current > 8A | CLEAR_FAULT after inspection |
| 2 | Overtemperature — joint temp > 75°C | CLEAR_FAULT after cooling |
| 3 | Encoder soft limit exceeded | CLEAR_FAULT after repositioning |
| 4 | Velocity limit exceeded > 120 deg/s | CLEAR_FAULT |
| 5 | Gripper force spike > 15N | CLEAR_FAULT after inspection |
| 6 | Heartbeat timeout — Pi silent > 500ms | Auto-recovers when heartbeat resumes |
| 7 | Firmware watchdog reset | CLEAR_FAULT after admin review |
| 8 | Boot calibration timeout | Admin must manually home joint |

### Pre-Threshold Warning Margins

- Joint current: Warning at 6A (−25% velocity). Hard ESTOP at 8A.
- Joint temperature: Warning at 55°C (−25% velocity). Slowdown at 65°C (−50%). ESTOP at 75°C.
- Gripper force: Target 3–5N. Warning at >10N. ESTOP at >15N.
- Joint velocity: Operational limit 80 deg/s. Hard ESTOP at 120 deg/s.

### Gripper Force Control Logic

- Force control mode — not simple open/close
- Apply increasing current until target force threshold reached, then maintain minimum holding torque
- Force spike > 15N → immediate ESTOP (unexpected contact)
- Object drop detection: force drops to zero during HOLDING → notify planner_node via /motion_feedback
- Gripper fully opens before arm approaches grasp position — GRIPPER_OPEN awaited first

### Boot Calibration Sequence

- Move each joint slowly toward mechanical limit switch, detect contact, zero encoder offset
- Repeat for all 6 joints in defined sequence (joint 1 → 6)
- Set all joint soft-limits from calibrated zeros
- Report CALIBRATION_COMPLETE to Pi
- Timeout per joint: [PLACEHOLDER] seconds — if not reached → fault_code 8

---

## SECTION IV — SOFTWARE ↔ EMBEDDED INTEGRATION BOUNDARY

> **INTEGRATION BOUNDARY** — Protocol contract between embedded_interface_node (software) and Teensy 4.1 firmware. Both teams must implement their side identically.

### Physical Communication Layer

- Primary: UART — recommended for noise immunity and multi-drop support
- Fallback: UART at minimum 1 Mbps
- UART frame format: [PLACEHOLDER — standard 11-bit / extended 29-bit]
- Byte packing: little-endian, float32 IEEE 754
- Do not use I2C or SPI for Pi ↔ MCU communication
- Galvanic isolation: [PLACEHOLDER — implementation between Pi and MCU]
- UART format — framing: [PLACEHOLDER — start byte, length, payload, CRC]

### Startup Handshake

- On boot, MCU waits for first HEARTBEAT from Pi before entering IDLE
- Pi embedded_interface_node waits for CALIBRATION_COMPLETE from MCU before accepting any commands
- If Pi boots before MCU calibration completes: Pi polls, retries every 500ms, max 60 seconds
- If MCU does not send CALIBRATION_COMPLETE within 60 seconds: Pi publishes ESTOP, TTS: 'Calibration failed. Admin required.'

### Pi Heartbeat — Implementation

```cpp
// embedded_interface_node (C++) sends every 200ms:
{ "command":"HEARTBEAT", "timestamp": unix_ms, "robot_state": current_state_string }

// MCU side:
if(millis() - last_heartbeat_ms > 500){ disable_all_pwm(); enter_estop(); }
```

### Pi → MCU Commands

| Command | Fields | Description |
|---|---|---|
| MOVE | joint_angles[6] (float32), velocity_scale (float32), accel_limit (float32) | Move all joints to target positions |
| GRASP | force_target (float32, Newtons) | Close gripper in force control mode |
| RELEASE | — | Open gripper fully |
| MOVE_NEUTRAL | — | Return to predefined neutral position |
| ESTOP | — | Immediate PWM disable |
| CLEAR_FAULT | — | Reset after fault resolution |
| CALIBRATE | — | Trigger boot calibration sequence |
| HEARTBEAT | timestamp (int64), robot_state (string) | 200ms keepalive |

### MCU → Pi Status (50 Hz)

| Field | Type | Description |
|---|---|---|
| joint_positions | float32[6] | Current joint angles in radians |
| joint_velocities | float32[6] | Current joint velocities in rad/s |
| joint_currents | float32[6] | Per-joint motor current in Amperes |
| temperatures | float32[6] | Per-joint temperature in °C |
| gripper_force | float32 | Current gripper contact force in N |
| imu | roll, pitch, yaw (float32) | Arm orientation from IMU |
| fault_code | int32 | 0 = OK, see fault code table for non-zero values |
| control_state | string | IDLE / POSITION_CONTROL / GRIPPER_CONTROL / ESTOP / FAULT |

### Workspace Boundary Contract

Software enforces workspace limits before sending any MOVE command. Embedded enforces joint soft-limits independently. Both layers protect — neither relies solely on the other.

```
workspace: xmin:-0.4  xmax: 0.4  ymin:-0.3  ymax: 0.3  zmin: 0.0  zmax: 0.5  (metres)
```

---

## SECTION V — ROS2 SOFTWARE ARCHITECTURE

> **SOFTWARE** — All ROS2 nodes, topics, message definitions, launch files, and Python AI logic fall under the Software domain.

### Execution Model

- MultiThreadedExecutor runs all nodes concurrently. No monolithic Python process.
- One node per concern. Nodes communicate exclusively via typed ROS2 topics.
- Vision inference (YOLOv11) and speaker verification (SpeechBrain) must not run simultaneously.
- embedded_interface_node runs in a dedicated MutuallyExclusive callback group — heartbeat cannot share thread pool with vision or TTS.

### Node Inventory

| Node | Package | Language | Responsibility |
|---|---|---|---|
| voice_node | acare_voice | Python | Audio I/O, VAD, STT, TTS, emergency keyword thread, assistant agent (LOGGED_OUT) |
| dialogue_node | acare_dialogue | Python | LangGraph, intent clarity, context resolution, interruption, assistant agent routing |
| auth_node | acare_auth | Python | Dual biometric verification, session management, enrolment, scripted auth flow, handover face check |
| vision_node | acare_vision | Python | YOLOv11 ONNX, NBV search, Bayesian probability map, fake detection, 3D localisation, hand tracking |
| planner_node | acare_planner | Python | Full task orchestration, IK, handover protocol (3-check), state transitions, latency tracking, world state snapshot |
| embedded_interface_node | acare_embedded_interface | C++ | CAN/UART bridge, heartbeat, command serialisation — MutuallyExclusive callback group |
| safety_node | acare_safety | Python | LiDAR proximity, sensor threshold monitoring, graded severity (WARNING/CRITICAL/ESTOP) |
| state_manager | acare_planner | Python | Global robot state machine, atomic transition enforcement, graded severity handling |
| log_node | acare_logging | Python | SQLite audit trail, full pipeline latency fields, log rotation |
| admin_node | acare_admin | Python | CLI interface, enrolment, calibration, demo mode, diagnostics |

### Node Crash Recovery

- Lightweight `supervisor.py` (separate from ROS2) monitors node health and auto-restarts non-critical nodes
- Auto-restart (non-critical): log_node, admin_node, dialogue_node
- No auto-restart (critical): safety_node, embedded_interface_node, state_manager, planner_node
- On critical node crash: publish ESTOP, TTS: 'System fault detected. Admin required.', State → ERROR

### ROS2 QoS Policy

| Topic Category | QoS | Rationale |
|---|---|---|
| Sensor data (/motion_feedback, /lidar_scan) | BEST_EFFORT | Drop stale data; always use latest |
| Commands (/arm_command, /gripper_command, /emergency_stop) | RELIABLE | Guaranteed delivery — never drop |
| State topics (/robot_state, /state_transition, /safety_alert) | RELIABLE | All nodes must see state changes |
| Logging (/log_event) | BEST_EFFORT | Log loss acceptable; never block pipeline |

### Topic Structure

| Topic | Message Type | Publisher → Subscriber |
|---|---|---|
| /robot_state | RobotState | state_manager → all nodes |
| /state_transition | StateTransition | any node → state_manager |
| /raw_transcript | Transcript | voice_node → dialogue_node |
| /intent_result | Intent | dialogue_node → auth_node |
| /validated_intent | ValidatedIntent | auth_node → planner_node |
| /emergency_stop | EmergencySignal | voice_node / safety_node → all nodes + embedded_interface |
| /auth_request | AuthRequest | dialogue_node → auth_node |
| /auth_result | AuthResult | auth_node → planner_node |
| /vision_search_request | VisionSearchRequest | planner_node → vision_node |
| /vision_result | VisionResult | vision_node → planner_node |
| /probability_update | ProbabilityUpdate | vision_node → vision_node (internal) |
| /arm_command | ArmCommand | planner_node → embedded_interface_node |
| /gripper_command | GripperCommand | planner_node → embedded_interface_node |
| /motion_feedback | MotionFeedback | embedded_interface_node → planner_node |
| /lidar_scan | LaserScan | safety_node (internal), velocity scale → planner |
| /safety_alert | SafetyAlert | safety_node → planner_node + state_manager |
| /log_event | LogEvent | all nodes → log_node |
| /vision_status | VisionStatus | vision_node → planner_node (LOADING / READY) |
| /hand_status | HandStatus | vision_node → planner_node (handover hand detection) |
| /tts_request | String | dialogue_node, planner_node → voice_node |

### Custom Message Definitions — acare_msgs Package

```
RobotState.msg
string state  # OFFLINE|LOGGED_OUT|STANDBY|LISTENING|PROCESSING|EXECUTING|HOLDING|HANDOVER|ESTOP|ERROR
string active_user_id

Intent.msg
string tool
string action
string destination  # always 'user_handover' — hardcoded in planner
float32 confidence

ValidatedIntent.msg
string tool
string action
string user_id
bool authenticated

SafetyAlert.msg
string reason
string source  # voice|lidar|current|temp|velocity|gripper|network
string severity  # WARNING|CRITICAL|ESTOP

HandStatus.msg
bool hand_detected
bool is_open
bool palm_up
float32 x
float32 y
float32 z
float32 confidence

AuthResult.msg
string user_id
string name
string role
bool success
bool face_verified
float32 face_confidence

VisionResult.msg
bool found
string tool
float32 x
float32 y
float32 z
float32 confidence
string zone
string[] candidates  # alternative detection candidates for IK fallback

ArmCommand.msg
string command  # MOVE|GRASP|RELEASE|MOVE_NEUTRAL|ESTOP|CLEAR_FAULT|CALIBRATE|HEARTBEAT
float32[] joint_angles
float32 velocity_scale  # 0.0–1.0, set by safety_node proximity zone
bool blocking

MotionFeedback.msg
bool success
string phase  # PRE_GRASP|GRASP|HOLDING|HANDOVER|NEUTRAL|VIEWPOINT
string error  # empty if success

LogEvent.msg
string event_type
string user_id
string tool
string state
string description
int64 timestamp
int64 voice_e2e_ms    # VAD trigger → validated_intent published
int64 vision_search_ms  # search start → VisionResult received
int64 motion_ms       # MOVE command → MotionFeedback.success
int64 total_task_ms   # ValidatedIntent → handover complete
string safety_severity  # WARNING|CRITICAL|ESTOP for safety events

EmergencySignal.msg
string reason
string source
```

### Launch File

```python
# ros2 launch acare_bringup acare.launch.py
def generate_launch_description():
    return LaunchDescription([
        Node(package="acare_voice",              executable="voice_node"),
        Node(package="acare_dialogue",           executable="dialogue_node"),
        Node(package="acare_auth",               executable="auth_node"),
        Node(package="acare_vision",             executable="vision_node"),
        Node(package="acare_planner",            executable="planner_node"),
        Node(package="acare_planner",            executable="state_manager"),
        Node(package="acare_safety",             executable="safety_node"),
        Node(package="acare_embedded_interface", executable="interface_node"),
        Node(package="acare_logging",            executable="log_node"),
        Node(package="acare_admin",              executable="admin_node"),
    ])
```

---

## SECTION VI — GLOBAL ROBOT STATE MACHINE

> **SOFTWARE** — Enforced by state_manager node. Embedded firmware has its own independent state machine.

| State | Description | Allowed Transitions |
|---|---|---|
| OFFLINE | System idle, no processes running | → LOGGED_OUT on boot |
| LOGGED_OUT | System running, no active session | → STANDBY on login |
| STANDBY | Session active, awaiting command | → LISTENING on voice, → LOGGED_OUT on logout |
| LISTENING | VAD active, STT processing | → PROCESSING on valid command, → STANDBY on timeout |
| PROCESSING | Intent resolved, vision searching | → EXECUTING on tool found + IK solved, → STANDBY if not found |
| EXECUTING | Arm in motion, approaching grasp | → HOLDING on grasp confirmed, → ESTOP on trigger |
| HOLDING | Object grasped, moving to handover | → HANDOVER on arrival, → ESTOP on trigger |
| HANDOVER | At handover zone, 3-check verification in progress | → STANDBY on collection confirmed, → STANDBY on timeout |
| ESTOP | All motion halted, safe deposit if holding | → STANDBY on authorised resume |
| ERROR | Unrecoverable fault | → OFFLINE on admin reset |
| SAFE_DEPOSIT | Planner-internal transient — controlled move to drop zone. Not externally published. | → ESTOP on deposit confirmed |

### Logout Rules

- Logout command accepted only from STANDBY or ESTOP states
- If state is EXECUTING, HOLDING, or HANDOVER — reject logout with TTS response
- Staff may say 'stop' first → ESTOP with safe deposit → logout proceeds
- Session inactivity timeout: 5 minutes of no command in STANDBY → auto-logout with TTS notification

### Graded Safety Severity — State Manager Integration

| Severity | Trigger Example | State Manager Response |
|---|---|---|
| WARNING | joint_current > 6A, temp > 55°C, person 400–600mm | Notify planner to reduce velocity. Log WARNING. TTS: 'Caution — operating at reduced speed.' |
| CRITICAL | temp > 65°C, velocity near limit | Planner reduces velocity 50%. Continue task. Log CRITICAL. TTS: 'Warning — thermal limit approaching.' |
| ESTOP | current > 8A, lidar < 400mm, voice keyword | Immediate ESTOP — safe deposit if holding. All motion halted. State → ESTOP. |
## SECTION VII — IDENTITY & SESSION MANAGEMENT

> **SOFTWARE** — Registration, login, session lifecycle, runtime checks, and handover verification are Software responsibilities. Biometric models run on Pi. Runtime voice consistency verification ensures commands originate from the authenticated user throughout the session, enabling secure contactless interaction in sterile environments.

> **FINAL DECISION:** Authentication is voice biometric (SpeechBrain d-vector) + face embedding (MobileNet) only. No username, no password, no typing anywhere in the system. Registration requires admin CLI only. No self-registration. Face + voice both enrolled at registration time. Face enrolment requires camera operational.

### Two-Layer Identity Model

Layer 1 is full dual-biometric authentication at login. Layer 2 is a lightweight voice consistency check per command during the session.

### Layer 1 — Registration (Admin Only, One-Time)

```
Admin runs: python admin.py enrol --name "Dr. Sharma" --role surgeon

Step 1 — Voice enrolment:
  Robot says: "Please say the passphrase three times."
  User speaks passphrase × 3.
  SpeechBrain extracts d-vector per utterance.
  Average of 3 d-vectors = voice_embedding (stored).

Step 2 — Face enrolment (camera must be operational):
  Robot says: "Please look at the camera."
  Camera captures 10 frames.
  MobileNet extracts face embedding per frame.
  Average of 10 embeddings = face_embedding (stored).

Step 3 — Storage:
  unique_id = hash(voice_embedding + face_embedding + timestamp)
  Stored in users.db (encrypted):
    { unique_id, name, role, voice_embedding, face_embedding, registered_at, active }

Step 4 — Confirmation:
  TTS: "{name} registered successfully."
```

### Layer 1 — Login Flow

```
State: LOGGED_OUT, robot on standby, arm pointing downward.

Step 1 — Passive face detection (always-on, MediaPipe FaceDetection):
  Robot continuously scans for faces in front arc.
  No TTS, no prompt. Silent background scan.

Step 2 — Face detected:
  MobileNet compares face embedding vs all enrolled users.
  Best match found above threshold (0.78) → candidate_user identified.
  Robot says: "Welcome, {name}. Say confirm to log in."

Step 3 — Voice biometric simultaneously:
  As user says "confirm", Deepgram transcribes.
  SpeechBrain extracts d-vector from that utterance.
  Cosine similarity vs stored voice_embedding of candidate_user.
  Threshold: 0.85.

Step 4 — Both checks pass:
  Session created. active_user_id set in state_manager.
  TTS: "Logged in as {name}. How can I assist?"
  State → STANDBY.

Step 5 — Face check passes, voice fails:
  TTS: "Having trouble recognising your voice. Please try again."
  Retry once. Still fails → TTS: "Identity not confirmed. Please contact admin."
  No session created.

Step 6 — No face match found after 10s passive scan:
  No TTS. Continue passive scan. Robot stays on standby.

Step 7 — Manual fallback (user speaks first):
  assistant_agent (llama-3.1-8b-instant) handles conversation.
  Guides user through auth flow via dialogue.
  TTS: "I am ACARE. Please look at the camera to log in."
```

### Auth Flow — Scripted State Machine (Not Free Conversation)

The auth flow is a scripted state machine coordinated between dialogue_node and auth_node. It is not free conversational AI. Each step is a defined state with a fixed prompt and expected response type.

| Step | System Action | User Expected Response |
|---|---|---|
| 1. Detection | Passive face scan detects face | No response needed |
| 2. Greeting | TTS: 'Welcome {name}. Say confirm to log in.' | 'Confirm' — voice biometric sampled simultaneously |
| 3. Verification | d-vector extracted from confirmation utterance | — |
| 4. Session created | TTS: 'Logged in as {name}. How can I assist?' | Voice command or ACARE query |
| 5. Manual fallback | TTS: 'Please identify yourself.' | Staff says name or passphrase |
| 6. Failure | TTS: 'Identity not recognised. Please contact admin.' | Admin required |

### Layer 2 — Runtime Voice Consistency Check

```
Every command after login:
  Deepgram transcribes utterance.
  SpeechBrain extracts d-vector from that utterance.
  Cosine similarity vs LOGGED-IN user's voice_embedding only (not all enrolled users).
  Threshold: 0.85.

3 consecutive failures:
  TTS: "Having trouble recognising your voice. Please re-confirm identity."
  Lightweight re-verification: say passphrase again.
  Pass → continue, flag in log for re-enrolment suggestion.
  Fail → log VOICE_DRIFT_DETECTED. Session continues (not terminated — too aggressive for OT).
  Hard session kill on voice drift is NOT implemented.
```

- Per command: short d-vector extracted from current utterance
- Cosine similarity against LOGGED-IN user only (not all enrolled users)
- 3 consecutive low-similarity turns: TTS: 'Having trouble recognising your voice. Please re-confirm identity.'
- Lightweight re-verification: Pass → continue, flag for re-enrolment suggestion. Fail → TTS: 'Please re-enrol at your next convenient time. Session continues for now.'
- Log: VOICE_DRIFT_DETECTED — hard session termination on drift is too aggressive for clinical use

### Session Lifecycle

```
Login → session created, active_user_id set, inactivity_timer = 5 minutes.

Every command received → inactivity_timer resets.

Inactivity timer expires (5 min, no command in STANDBY):
  TTS: "Session timeout. Logging out {name}."
  Session terminated. active_user_id cleared.
  State → LOGGED_OUT.
  Deepgram WebSocket closed.
  Passive face detection resumes.

Optional hard TTL: 2 hours of total session time regardless of activity.
  Configurable in system.yaml: session_hard_ttl_seconds (default: 7200).
  On expiry: same as inactivity timeout.
  Recommended for long surgical shifts.
```

### Logout Rules

```
"Logout" accepted only from: STANDBY or ESTOP states.

If state is EXECUTING, HOLDING, or HANDOVER:
  TTS: "Cannot log out during active task."
  Command rejected. Task continues.

If staff needs to leave mid-task:
  Say "stop" → ESTOP → safe deposit → then "logout" accepted.

On logout:
  TTS: "Goodbye, {name}."
  Session terminated.
  Deepgram WebSocket closed.
  probability_map serialised to yaml.
  State → LOGGED_OUT.
  Passive face detection resumes.
```

### Handover — Multi-Modal Verification (Three-Check)

Dynamic Human–Robot Handover: The system performs an incremental approach toward the user's palm while continuously updating the target position based on real-time depth-based palm tracking.

Before releasing tool at handover zone, planner enforces three sequential checks:

**Check 1 — Continuous Face Verification**

- auth_node monitors camera every 0.5s during HANDOVER state
- Cosine similarity against logged-in user embedding, threshold 0.78–0.80
- 3 consecutive failures → hold tool, TTS: 'Please face the camera.'

```
Attempt 1: Default Z. Wait 8s for face.
  Found → proceed to HAND_DETECT.
  Not found → agentic: HANDOVER_Z_UP (+5cm). Move arm up.
Attempt 2: Z+5cm. Wait 8s for face.
  Found → proceed.
  Not found → agentic: HANDOVER_Z_DOWN (-5cm from default). Move arm down.
Attempt 3: Z-5cm. Wait 8s for face.
  Found → proceed.
  Not found → agentic: HANDOVER_VOICE_HAND_ONLY.
    TTS: "Face verification unavailable. Proceeding with voice and hand confirmation only."
    Log: FACE_VERIFY_SKIPPED (admin review required).
    face_verified = False. face_skipped = True.
    Proceed to HAND_DETECT regardless.
```

> Note: Wrist camera is fixed to arm and cannot pan independently. User may be leaning over patient, not facing robot. The Z-height search approach solves this without additional hardware.

**Check 2 — Hand Detection**

- vision_node runs MediaPipe Hands during HANDOVER state
- Publishes /hand_status: {detected, is_open, palm_up, x, y, z, confidence}
- Open palm facing upward in handover zone required before voice prompt
- If hand not detected: TTS: 'Please place your open palm under the gripper.'
- If hand detected but not open: TTS: 'Please open your palm.'
- Dynamic handover: arm makes incremental approach toward palm center using /hand_status (x,y,z) to update target position in real-time. Each position update validated by SafetyKernel.validate_move(). Velocity during palm approach: 0.3 (very slow, contact-safe).
- User says "lower" or "higher" during HAND_DETECT: arm adjusts ±5cm in Z. New pose validated by SafetyKernel. Preference stored in UserProfile.handover_z_offset for next session.

```
Wait for: hand_detected=True AND is_open=True AND palm_up=True.
Timeout: 10s first attempt, 8s second attempt.
If not detected after 2 attempts:
  TTS: "Please open your palm and hold it steady."
  Wait 8s more.
  Still not detected → handover timeout path.
```

**Check 3 — Voice Confirmation**

- TTS: 'Say take to receive.'
- Staff says 'take' or 'yes'
- Runtime voice consistency check against logged-in user passes
- Both must pass (keyword detected AND voice matches)
- Timeout: 5s
- If voice matches but keyword not detected: TTS: "Say 'take' to receive." Retry once.
- If voice does not match: TTS: "Voice not recognised." Hold tool. Retry once.
- After 2 failures: handover timeout path.
- All three checks passed → RELEASE gripper

### SafetyKernel Release Gate

```python
SafetyKernel.validate_release(world, face_verified, hand_detected, voice_confirmed)
# Hand detected AND voice confirmed are BOTH required.
# Face is advisory — if face_verified is False but the other two pass:
#   returns (True, "FACE_SKIPPED — logged")
# If hand or voice fails → returns (False, reason)
```

### Handover Substates (planner-internal)

```
APPROACHING → FACE_VERIFY → HAND_DETECT → VOICE_CONFIRM → RELEASING → COMPLETE
```

### Handover Timeout

- 30 seconds total for all three checks combined
- Timeout expires → TTS: 'No collection detected. Returning {tool} to tray.'
- ArmCommand: MOVE to SAFE_DROP_ZONE → RELEASE → Log: HANDOVER_TIMEOUT → State → STANDBY

### Height Adjustment Per User

- Staff can say 'lower' or 'higher' during handover to adjust arm position
- Adjustment: ±5cm in Z per command
- Clamps to [-0.15, +0.15] (±15cm range)
- Preference stored per user in users.db — applied automatically on next handover

### Multi-User & Unauthorised Voice Handling

- One active session at any time. Second staff approach → TTS: '{staff_A} is currently logged in.'
- Two-staff simultaneous speech: command rejected. TTS: 'Command not processed. Only {name} can issue commands.' Log: UNAUTHORISED_VOICE_ATTEMPT

---

## SECTION VIII — VOICE ORCHESTRATION LAYER

> **SOFTWARE** — voice_node owns all audio hardware access, VAD, STT, TTS, microphone mute logic, and emergency keyword thread.

### TTS Engine — Dual Approach (Finalised)

- ESTOP / critical safety messages: pyttsx3 — zero latency, fully offline, instant, zero dependency
- All other responses (normal commands, assistant agent): Microsoft Edge TTS (switched from initially planned Google Cloud TTS)
- Offline fallback (if no internet): Kokoro ONNX INT8 — local, natural voice, Pi-compatible, Apache 2.0
- 'ACARE' must be replaced with 'A-Care' before all speak() calls to prevent mispronunciation
- On Windows development: reinitialise pyttsx3 engine per speak() call to avoid known Windows single-call bug
- Priority queue: ESTOP and urgent messages jump to front, current audio hard-cut
- Rate: 150 words per minute (slightly deliberate for OT clarity)
- Microphone hard-muted during TTS playback. 300ms buffer after TTS to prevent echo triggering VAD.

### Audio State Machine — Internal to voice_node

| State | Description | Allowed Transitions |
|---|---|---|
| IDLE | Mic off, TTS off | → LISTENING when robot enters STANDBY |
| LISTENING | VAD active, mic open, Deepgram WebSocket open | → TRANSCRIBING on utterance complete |
| TRANSCRIBING | Deepgram processing, mic still open | → SPEAKING when response ready, → LISTENING if no response |
| SPEAKING | TTS playing, mic hard-muted | → LISTENING after TTS complete + 300ms buffer |
| ESTOP_LISTEN | Emergency keyword thread only — always active, never muted | Parallel to all states |

### Assistant Agent — LOGGED_OUT State

- Activates automatically when state = LOGGED_OUT and voice input detected
- Uses Groq llama-3.1-8b-instant, temperature 0.3, max 150 tokens
- Bounded to two contexts only: ACARE self-introduction and guided auth flow
- Professional, clinical tone — 1–3 sentences maximum, no small talk
- Conversation history maintained per session. reset_conversation() called on new session start.
- History capped at last 20 turns — older turns summarized to prevent Pi RAM exhaustion
- If user asks to fetch a tool: TTS: 'Authentication required before I can fetch tools.'

```
Standby behaviours when LOGGED_OUT:
  Handles casual conversation.
  Introduces itself: "I am A-Care. I can assist surgical staff with instrument retrieval.
  You need to be registered to use my features. Are you registered?"
  If user asks to fetch a tool: "Authentication required before I can fetch tools."
  If user asks to register: guides them to call admin.
  If user asks to login: begins login flow (face + voice).
  Bounded to: self-introduction, auth guidance. No small talk beyond 1-3 sentences.
```

### Deepgram WebSocket — Streaming Implementation

- Audio streamed chunk-by-chunk every 32ms — not sent as completed utterance after VAD fires
- send_chunk() called every 32ms from VAD callback — streams raw PCM int16 bytes
- float32 audio × 32767 → int16 bytes → sent via run_coroutine_threadsafe into background async loop
- Background thread hosts its own asyncio event loop — separate from main thread
- Session login → open WebSocket (kept alive for session duration)
- Session logout → close WebSocket cleanly
- Unexpected drop → 3 retries with exponential backoff (500ms, 1s, 2s) → TTS: 'Voice service unavailable.'

### Deepgram Partial vs Final Transcript Handling

```python
on_message(result):
    if not result.is_final:
        keyword_monitor.check_partial(sentence)  # ESTOP detection only
        return
    if result.is_final and result.speech_final:
        if keyword_monitor.estop_active:
            return  # drop silently — ESTOP is active
        pass_to_normaliser(result.transcript)
```

### ESTOP Keyword Monitor — Implementation Details

- Separate always-on thread monitoring Deepgram partial transcripts. Never muted.
- Keywords: stop, halt, emergency, abort, ruko, bas
- Acts on partial transcript — target latency < 200ms from word to ESTOP published
- 100ms collision window via threading.Timer: 'stop, actually bring the scalpel' → timer cancelled
- Word-boundary matching only: text.split() with punctuation stripped — 'stroke', 'stopped' do not trigger
- estop_active flag: once ESTOP confirmed, all transcripts dropped until resume() called
- resume() only callable by authenticated staff in ESTOP state

```
ESTOP Keyword + Normal Command Collision — Decision Tree:

ESTOP keyword detected in partial transcript ↓
  100ms hold window — check if more speech follows
  More speech detected → not ESTOP → pass full utterance to STT pipeline normally
  No more speech → confirm ESTOP, trigger immediately
```

### Mic Mute During TTS

```python
async def speak(text, priority=NORMAL):
    if priority == URGENT:
        tts_queue.clear()
        tts.stop_current()
        mute_microphone()
    await tts.play(text)
    await asyncio.sleep(0.3)  # prevents TTS tail from triggering VAD
    unmute_microphone()
    audio_state → LISTENING
```

---

## SECTION IX — VOICE COMMAND PIPELINE

> **SOFTWARE** — No offline STT or intent fallback. System either works fully or stops cleanly.

### Network Failure Policy — Final

- No fuzzy keyword fallback, no Vosk offline STT, no Whisper fallback
- Deepgram failure → TTS: 'Voice service unavailable.' → STANDBY (or safe deposit if holding)
- Groq failure → TTS: 'Service temporarily unavailable.' → STANDBY (or safe deposit if holding)
- Edge TTS failure → fallback to Kokoro ONNX automatically (local)
- Holding object past 5-second threshold when network fails → safe deposit → ESTOP

### Complete Pipeline Flow

```
Microphone (32ms chunks, 16kHz, float32) ↓ streaming continuously

Silero VAD (every chunk, 512 samples minimum)
  pause < 1.5s → thinking, pipeline waits
  pause > 3s + min 1s speech → utterance complete
  < 1s total speech → ignore (noise/cough) ↓

all chunks also streamed in parallel:
Emergency Keyword Thread (always-on, Deepgram partial transcripts)
  Keywords: stop, halt, emergency, abort, ruko, bas
  Word-boundary match, 100ms collision window
  Target latency: <200ms from word to ESTOP published ↓

(if no ESTOP)
Deepgram Nova-2 Streaming STT (WebSocket, en-IN)
  is_final=false → check_partial() for ESTOP keywords only
  is_final=true AND speech_final=true → pass to normaliser ↓

normaliser.py
  lowercase, filler word removal, punctuation normalisation
  simple alias expansion for clearly unambiguous cases only ↓

Multi-tool detection:
  Multiple tools in transcript → TTS: 'One at a time. Which first — {A} or {B}?' ↓

Groq API Intent Parser (llama-3.1-8b-instant, temperature 0.0, JSON mode)
  output: {tool, action, confidence}
  destination NOT in Groq output — hardcoded 'user_handover' in planner ↓

Intent Clarity Check:
  Clear (confidence >= 0.8) → Runtime voice consistency check → Auth gate
  Ambiguous (confidence < 0.8) → Dialogue Manager (LangGraph) ↓

Runtime Voice Consistency Check
  Lightweight d-vector similarity, logged-in user only ↓

ValidatedIntent published → /validated_intent → planner_node
```

### normaliser.py — Scope

```
Step 1 — Lowercase: 'Bring the SCALPEL' → 'bring the scalpel'
Step 2 — Strip fillers: 'um, can you please bring' → 'bring'
Step 3 — Punctuation strip: 'scissors,' → 'scissors'
Step 4 — Simple alias: 'bandage cloth' → 'bandage' (unambiguous only)
Step 5 — Multi-tool detect: 'scissors and scalpel' → flag for clarification
```

- Full contextual alias expansion ('the sharp one') stays in Groq — not hardcoded
- Multi-tool detection: if 2+ tool names in transcript → flag MULTI_TOOL before Groq call

---

## SECTION X — CONVERSATIONAL LAYER — LangGraph + Assistant Agent

> **SOFTWARE** — LangGraph dialogue management and assistant agent are Software. Bounded agentic layer for intent clarification and pre-auth interaction only.

### dialogue_node Operating Modes

| Mode | Activates When | Behaviour |
|---|---|---|
| ASSISTANT MODE | State = LOGGED_OUT and voice input detected | Groq-powered conversational agent. Handles ACARE self-introduction and guides auth flow. Professional, clinical, 1–3 sentences max. Model: llama-3.1-8b-instant. |
| DIALOGUE MODE | State = STANDBY / LISTENING / PROCESSING | LangGraph multi-node graph for intent clarity, clarification, context resolution, and interruption handling. Model: openai/gpt-oss-120b for complex clarification needing reasoning depth. |

### Session Memory Schema

```json
{
  "tools_fetched": [{"tool", "timestamp", "zone"}],
  "conversation_history": [turns],
  "current_task": {"tool", "status"},
  "pending_clarification": bool,
  "last_command": str
}
```

- conversation_history capped at 20 turns; older turns summarized to prevent Pi RAM exhaustion

### LangGraph Nodes

| Node | Trigger | Action |
|---|---|---|
| Intent Clarity Check | Every intent result | Routes to clear path or ambiguous path based on confidence and pronoun detection |
| Clarification Node | Ambiguous intent | Generates specific follow-up question using Groq LLM |
| Context Resolver | Pronoun or reference in command | Resolves 'it', 'that', 'the smaller one' using session memory |
| Interruption Handler | New command while task active | Safe pause, switch to new command or route to ESTOP |
| Dialogue Manager | All nodes route through | Final routing decision to auth gate |

### Handled Conversational Cases

| Input | Resolution |
|---|---|
| 'bring me something sharp' | Clarification: 'Do you mean a scalpel or scissors?' |
| 'actually bring the forceps instead' | Interruption handler: pause current task, switch target |
| 'bring it back' | Context resolver: 'it' = last tool in tools_fetched |
| 'the smaller one' | Context resolver: resolves against last ambiguous candidate set |
| 'I need that cutting thing' | Alias expansion + clarification if still ambiguous |
| 'bring me scissors and scalpel' | Multi-tool gate: 'One at a time. Which first?' |

---

## SECTION XI — VISION PIPELINE — NBV SEARCH & DETECTION

> **SOFTWARE** — All vision processing, YOLOv11 inference, NBV search, fake detection, 3D localisation, and hand tracking are Software running on Pi.

### Camera

YDLIDAR HP60C RGBD — wrist-mounted. Provides RGB frame and depth frame directly from hardware per capture. No stereo processing. Depth value read directly from depth frame at bounding box center pixel — no Open3D or point cloud processing needed.

### Sensor Roles — Final Assignments

**YDLIDAR HP60C (RGBD Camera, Wrist-Mounted) — Used for:**

- Tool detection during NBV search (YOLOv11 on RGB frames)
- 3D localisation of detected tools (depth pixel → 3D point)
- Fake object detection (texture variance + depth variance)
- Hand tracking during handover (MediaPipe Hands on RGB frames)
- Face detection/verification during login and handover (MediaPipe FaceDetection + MobileNet)

**YDLIDAR HP60C — NOT used for:**

- SLAM or navigation (robot is stationary)
- Person identification by LiDAR
- Continuous streaming (captures on demand, not always streaming)

**Camera capture protocol:**
```
Arm must be fully stationary before capture.
Capture 3 frames per viewpoint at ~2-3cm wrist offsets.
YOLOv11 inference on all 3 frames.
Merge detections via NMS across frames.
```

**YDLIDAR T-mini Plus (2D LiDAR, Base-Mounted at ~80cm) — Used for:**

- Person proximity detection only (torso-level 2D scan)
- Zone detection: > 600mm → Safe zone → velocity_scale = 1.0 / 400–600mm → Caution zone → velocity_scale = 0.5, SafetyAlert WARNING / < 400mm → Danger zone → SafetyAlert ESTOP immediately

**YDLIDAR T-mini Plus — NOT used for:**

- Tool detection (cannot — it's a 2D horizontal scan at 80cm, no colour/texture)
- Face detection or user identification
- NBV search strategy
- Finding the user for handover (it detects A torso, not WHOSE torso)

**LiDAR role at handover specifically:**
```
LiDAR detects "someone is in front of robot" → triggers camera face search.
LiDAR does NOT identify who the person is.
LiDAR does NOT detect hand or face.
During arm motion to handover zone: LiDAR proximity < 400mm → ESTOP immediately.
During actual handover (arm stationary): proximity monitoring continues.
  Person suddenly < 400mm during gripper release → ESTOP, tool held.
```

### Vision Node Startup

```
vision_node starts → publishes /vision_status: LOADING
YOLOv11 ONNX model loads into memory (several seconds on Pi)
Once loaded → publishes /vision_status: READY
planner_node checks /vision_status before accepting any commands
TTS: 'System initialising. Please wait.' if command arrives during LOADING
```

### Low Light Detection — Final Decision

Problem: YOLOv11 trained on well-lit images. Low-light surgical environments cause low confidence detections (thresholds dropping below 0.7).

**Solution (software only, no hardware addition):**

```python
# Step 1 — Preprocessing in vision_node before YOLOv11 inference:
# Apply CLAHE (Contrast Limited Adaptive Histogram Equalisation) to RGB frame.
import cv2
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
# Convert to LAB, apply to L channel, convert back to BGR. Feed to YOLOv11.

# Step 2 — Adaptive confidence threshold:
mean_brightness = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).mean()
if mean_brightness < 80:  # low light threshold, calibrated empirically
    confidence_threshold = 0.60
    temporal_consistency_required = 3  # viewpoints
    low_light_mode = True
else:
    confidence_threshold = 0.70
    temporal_consistency_required = 2  # viewpoints
    low_light_mode = False
```

- Low-light flag logged in every LogEvent when triggered: LogEvent.description includes "LOW_LIGHT_MODE" string
- Low-light threshold (mean_brightness < 80) calibrated empirically during setup

### Workspace Boundary Enforcement

All detections outside the defined workspace volume are discarded before any IK is attempted.

```
workspace: { xmin:-0.4, xmax:0.4, ymin:-0.3, ymax:0.3, zmin:0.0, zmax:0.5 }
```

### NBV Cold Start Strategy

- First boot or probability_map.yaml absent → uniform distribution across all zones
- Admin defines layout profile before exhibition: tool expected zones stored in probability_map.yaml
- Without admin prior, first demo run is slower — robot checks all zones before finding tool
- After first successful detection, the probabilistic map is updated via Bayesian inference, improving search efficiency for subsequent requests.

### NBV Timing Expectation — Per-Step Breakdown

| Step | Duration |
|---|---|
| Arm move + settle | ~1.0s |
| 3 frame captures (2–3cm wrist offsets) | ~0.3s |
| YOLOv11 ONNX inference ×3 | ~0.6–1.5s on Pi 5 |
| Merge + localise | ~0.1s |
| Total per viewpoint | ~2–3 seconds |
| Worst case (6–8 viewpoints, tool in last zone) | ~15–25 seconds |

If inference too slow on Pi 5 in practice, alternative options: reduced input resolution, model distillation to smaller variant, ONNX runtime instead of TFLite. Depends on testing results.

### Complete NBV Search Flow

```
Triggered by: planner_node publishes /vision_search_request
  {tool, reset_probability_map, priority_zones}

vision_node._execute_nbv_search():

1. Load probability_map for requested tool.
   If reset_probability_map == True → use uniform distribution for this search.
   If priority_zones not empty → boost those zones' probabilities × 2.0, normalise.

2. Sort viewpoints by P(tool|zone), highest first.
   Viewpoints are pre-defined arm poses stored in config (set during calibration).

3. For each viewpoint (loop):

   a. planner sends MOVE to embedded_interface_node → arm moves to viewpoint.
      Wait MotionFeedback.success.
      CRITICAL: do NOT capture until arm fully stationary.

   b. Estimate frame brightness (mean pixel value, grayscale).
      If mean < 80: apply CLAHE preprocessing. Set low_light_mode = True.
      Confidence threshold: 0.60 if low_light_mode, else 0.70.
      Temporal consistency required: 3 viewpoints if low_light_mode, else 2.

   c. Capture 3 frames at ~2-3cm wrist Z-offsets (tiny arm movements).
      Each frame: RGB + depth from HP60C.

   d. YOLOv11 ONNX inference on all 3 frames.
      Merge detections: NMS across 3 frames.
      Filter by confidence threshold (0.60 or 0.70 per above).
      Filter by workspace bounds: discard out-of-bounds detections.

   e. Fake object check (see fake object detection below).

   f. Filter to requested tool class only.
      Single detection → proceed.
      Multiple → highest confidence; tiebreak: closest to neutral arm position.

   g. Temporal consistency check:
      Same tool class at approximately same (x,y,z) (within 3cm) in required
      consecutive viewpoints → accepted even at confidence 0.65+.

   h. If found:
      depth_value = depth_frame[bbox_center_y][bbox_center_x]
      Convert to 3D using camera intrinsics + depth_value.
      tool_position_3D = (x, y, z) in robot frame.
      Store all other detections as detection_candidates in VisionResult
      for IK fallback use.
      Bayesian map update: probability[zone][tool] *= 1.5, clamp [0.05, 0.90], normalise.
      Passive update: all detected tools in viewpoint: probability *= 1.3, normalise.
      Publish /vision_result {found: true, tool, x, y, z, confidence, zone, candidates[]}.
      Return.

   i. If not found in this viewpoint:
      Bayesian map update: probability[zone][tool] *= 0.7, normalise, clamp.
      Continue to next viewpoint.

4. All viewpoints exhausted → not found.
   Publish /vision_result {found: false}.
   planner handles retry logic.
```

### Bayesian Probability Map Update — With Clamping

- Tool found in zone: probability[zone][tool] *= 1.5, then normalise
- Tool not found: probability[zone][tool] *= 0.7, then normalise
- Passive map update at every viewpoint for all detected tools: probability *= 1.3, normalise
- Clamping after every update: P = min(max(P, 0.05), 0.90) — prevents saturation, ensures no zone completely ignored
- On clean shutdown: serialise probability_map → probability_map.yaml
- On unclean boot: reload from yaml (may be slightly stale — acceptable)

This adaptive probabilistic mapping enables the system to learn instrument placement patterns over repeated sessions, reducing average search time.

### Fake Object Detection

Two independent signals. Both must trigger to flag as fake — reduces false rejections on shiny real tools.

```python
def is_fake(rgb_frame, depth_frame, bbox):
    x1, y1, x2, y2 = bbox
    roi_gray = cv2.cvtColor(rgb_frame[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
    texture_var = cv2.Laplacian(roi_gray, cv2.CV_64F).var()
    depth_roi = depth_frame[y1:y2, x1:x2]
    depth_var = np.var(depth_roi[depth_roi > 0])
    return texture_var < TEXTURE_THRESHOLD and depth_var < DEPTH_THRESHOLD
```

Thresholds calibrated empirically during setup (20 real + 20 printed samples). Stored in thresholds.yaml — not hardcoded.

```
If depth unavailable:
  Fall back to texture check only.
  Log: DEPTH_UNAVAILABLE.
  Accept if texture_var >= TEXTURE_THRESHOLD (lower trust, logged).

If fake detected:
  TTS: "Object appears to be a reproduction. Command rejected."
  Log: FAKE_REJECTED.
  Skip to next detection candidate or next viewpoint.
```

### Hand Tracking — During Handover

- MediaPipe Hands runs on RGB camera frames during HANDOVER state only (not during vision search)
- Detects: hand_detected, is_open (3+ fingers extended), palm_up (fingers above wrist)
- Position (x, y, z) of palm center converted to robot coordinates
- Publishes /hand_status every camera frame during HANDOVER state
- **MediaPipe Hands and YOLOv11 do NOT run simultaneously** — planner ensures this. vision_node switches mode based on robot state.

### Depth Camera Failure Handling

- Depth unavailable during fake detection → fall back to texture check only; flag lower confidence; Log: DEPTH_UNAVAILABLE
- Depth unavailable during 3D localisation → TTS: 'Camera error. Please retry.'; State → STANDBY; Log: DEPTH_FAILURE

### Tool Not Found — Full Recovery Flow

```
All viewpoints exhausted ↓
TTS: 'Cannot locate {tool}. Can you confirm it is on the tray?'
  'Yes it is there' → re-run NBV once more from scratch
  'Try the left side' → context resolver maps to zone → re-run from that zone only
  'Never mind' → abort → STANDBY ↓

Second search fails:
TTS: 'Still unable to locate {tool}. Please check tray or use manual procedure.'
State → STANDBY
```

### IK Failure Recovery — Full Step-by-Step

```
Grasp point computed ↓ IK solver runs
  Solution found → proceed
  Fail (joint limit violation): Try alternate grasp orientation (rotate approach 90°)
    Solution found → proceed
    Still fails: Try next detection candidate (next highest confidence)
      No candidates left: TTS: 'Unable to reach the {tool}. Please reposition it.'
      State → STANDBY
```

---

## SECTION XII — TASK PLANNER PIPELINE

> **SOFTWARE** — planner_node orchestrates the full pick-and-place sequence. Does not implement motor control — sends commands via embedded_interface_node.

### Planner Architecture — Three Layers

```
Layer 1 — AGENTIC DECISION LAYER:
  Model: openai/gpt-oss-120b via Groq API.
  Reasoning level: "high" for recovery decisions, "low" for search strategy.
  Strict JSON schema output (guaranteed schema compliance, no parse errors).
  Proposes: search strategy, recovery actions, handover pose adjustments.
  CANNOT execute anything directly.
  Has deterministic fallbacks for every decision (LLM failure does not stop the robot).

Layer 2 — DETERMINISTIC SAFETY KERNEL:
  Pure Python, no external calls, no LLM.
  Validates every proposal from Layer 1.
  validate_move(): workspace bounds check + ESTOP check.
  validate_grasp(): force limit check.
  validate_handover(): session + safety severity check.
  validate_release(): 3-check gate (hand + voice required; face advisory).
  velocity_scale(): returns float based on safety severity.
  CANNOT be overridden. No exceptions.

Layer 3 — NODE COORDINATION:
  Publishes ROS2 commands. Subscribes to ROS2 feedback.
  All communication via typed topics (or std_msgs JSON fallback).
  Runs task pipeline in background thread (not blocking ROS2 callbacks).
```

### Retry Policy

```python
MAX_RETRIES = 3  # global constant, per failure type independently

# Failure types and their independent counters:
#   vision_search  — NBV search returned no result
#   grasp          — gripper force confirmation failed
#   ik_solve       — IK solver returned None
#   handover_face  — face verification failed at handover

# Rules:
# Each counter is independent. Grasp fail does not consume vision retry.
# On attempt N == MAX_RETRIES: TTS must warn user ("Last attempt...").
# After MAX_RETRIES exceeded: abort with clear user message, State → STANDBY.
# Exception: handover_face — attempt 3 is VOICE_HAND_ONLY fallback, not abort.
#   Handover never aborts on face failure alone. Voice + hand still required.
```

### Groq API Call Structure

```python
# Every LLM call follows this pattern:
response = groq_client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": PLANNER_SYSTEM_PROMPT + "\n\nReasoning: {high|low}"},
        {"role": "user",   "content": json.dumps(context_dict)}
    ],
    response_format=DECISION_SCHEMA,  # strict JSON schema
    temperature=0.1,                  # near-deterministic
    max_completion_tokens=512
)
decision = json.loads(response.choices[0].message.content)
```

### Decision JSON Schema (Strict Mode)

```json
{
  "type": "json_schema",
  "json_schema": {
    "name": "planner_decision",
    "strict": true,
    "schema": {
      "type": "object",
      "properties": {
        "decision_type": {
          "type": "string",
          "enum": ["SEARCH_STRATEGY","VISION_RECOVERY","GRASP_RECOVERY",
                   "IK_RECOVERY","HANDOVER_RECOVERY","ABORT"]
        },
        "reasoning": {"type": "string"},
        "action": {
          "type": "string",
          "enum": [
            "RETRY_UNIFORM_SEARCH",
            "ASK_USER_CONFIRM_LOCATION",
            "ABORT_TOOL_NOT_FOUND",
            "RETRY_GRASP_REPOSITION",
            "RETRY_GRASP_FORCE_INCREASE",
            "ABORT_GRASP_FAILED",
            "RETRY_IK_ALTERNATE_ORIENTATION",
            "RETRY_IK_NEXT_CANDIDATE",
            "ABORT_IK_FAILED",
            "HANDOVER_Z_UP",
            "HANDOVER_Z_DOWN",
            "HANDOVER_VOICE_HAND_ONLY",
            "SEARCH_PRIORITY_ZONES"
          ]
        },
        "tts_message": {"type": "string"},
        "params": {
          "type": "object",
          "properties": {
            "force_delta_n":         {"type": "number"},
            "z_offset_m":            {"type": "number"},
            "rotation_deg":          {"type": "number"},
            "priority_zones":        {"type": "array", "items": {"type": "string"}},
            "reset_probability_map": {"type": "boolean"}
          },
          "required": ["force_delta_n","z_offset_m","rotation_deg",
                       "priority_zones","reset_probability_map"],
          "additionalProperties": false
        }
      },
      "required": ["decision_type","reasoning","action","tts_message","params"],
      "additionalProperties": false
    }
  }
}
```

### Planner System Prompt

```
You are the agentic decision layer of ACARE — an Autonomous Clinical Assistance Robot
operating in a surgical environment. You orchestrate task recovery and search strategy
for a 6-DOF robotic arm that fetches sterile instruments for authenticated surgical staff.

HARD RULES:
- Never suggest bypassing authentication or safety checks.
- Never suggest moving outside workspace bounds.
- Never suggest gripper force above 10N.
- Only suggest actions from the allowed action enum.
- If uncertain, choose ABORT over unsafe continuation.
- Keep tts_message brief (1-2 sentences), professional, clinical tone.
- On final attempt (attempt == max_retries): tts_message MUST warn staff this is the last try.
- After all retries exhausted: tts_message must clearly state inability and suggest manual procedure.

Reasoning: {high|low}   ← injected per call
```

### CLASS: RetryCounters

```python
@dataclass
class RetryCounters:
    vision_search: int = 0
    grasp: int = 0
    ik_solve: int = 0
    handover_face: int = 0
```

**Methods:**
- `exhausted(failure_type: str) -> bool` — True if counter >= MAX_RETRIES
- `increment(failure_type: str)` — Increment named counter by 1
- `is_last_attempt(failure_type: str) -> bool` — True when current value == MAX_RETRIES - 1 (next is the last)

### CLASS: SafetyKernel — All Methods

#### `validate_move(target_pos, world) -> (bool, str)`

Checks (x,y,z) against workspace bounds. Checks ESTOP state. Returns (False, reason) if any check fails. Returns (True, "CRITICAL — velocity capped at 50%") if severity is CRITICAL but move is geometrically valid. Called by every arm move before the command is sent. Hard limits: xmin=-0.4, xmax=0.4, ymin=-0.3, ymax=0.3, zmin=0.0, zmax=0.5 (metres).

#### `validate_grasp(force_target, world) -> (bool, str)`

Rejects any force > 15N (ESTOP threshold). Warns but approves 10–15N range. Approves < 10N unconditionally. Called by every grasp command before sending. Note: Planner itself caps retry forces at 10N. Safety kernel is the final backstop.

#### `validate_handover(world) -> (bool, str)`

Rejects if no active session (active_user_id empty). Rejects if safety_severity is ESTOP or CRITICAL. Called before moving arm to handover zone.

#### `validate_release(world, face_verified, hand_detected, voice_confirmed) -> (bool, str)`

Hand detected AND voice confirmed are BOTH required. Face is advisory — if face_verified is False but the other two pass, returns (True, "FACE_SKIPPED — logged"). If hand or voice fails → returns (False, reason). Called immediately before RELEASE command is sent.

#### `velocity_scale(world) -> float`

Returns 0.5 if CRITICAL, 0.75 if WARNING, 1.0 if OK. Called by every arm move, multiplied with task_phase_scale before sending velocity_scale to embedded_interface_node.

### CLASS: AgenticPlanner — All Methods

#### `__init__(self, logger)`

Initialises Groq client (GROQ_API_KEY from env). Initialises user_profiles dict (user_id → UserProfile). Initialises time_patterns dict (hour → {tool: preferred_zone}).

#### `_call_llm(self, messages, reasoning_level) -> Optional[Dict]`

**Signature:** `_call_llm(messages: List[Dict], reasoning_level: str = "low") -> Optional[Dict]`

Calls openai/gpt-oss-120b with strict JSON schema. Injects reasoning level into system prompt. Returns parsed dict. Returns None on any exception (network error, parse error). Never raises — robot must not crash on LLM failure.

#### `propose_search_strategy(self, tool, user_id, current_hour, attempt_number) -> Dict`

**Signature:** `propose_search_strategy(tool: str, user_id: str, current_hour: int, attempt_number: int) -> Dict`

Called before the first NBV search attempt. Looks up user's preferred zone for this tool (from UserProfile.preferred_zones). Looks up time-based hint (from time_patterns[current_hour][tool]). Sends both as context to gpt-oss-120b with reasoning: low. Returns decision dict with action=SEARCH_PRIORITY_ZONES and priority_zones list. If LLM fails, returns deterministic fallback (empty priority_zones, use probability map default).

**Fallback (LLM failure):**
```python
{
    "decision_type": "SEARCH_STRATEGY",
    "action": "SEARCH_PRIORITY_ZONES",
    "reasoning": "LLM unavailable — using probability map default",
    "tts_message": f"Searching for {tool}.",
    "params": {"priority_zones": [], "reset_probability_map": False,
               "force_delta_n": 0.0, "z_offset_m": 0.0, "rotation_deg": 0.0}
}
```

#### `propose_vision_recovery(self, tool, attempt, world) -> Optional[Dict]`

**Signature:** `propose_vision_recovery(tool: str, attempt: int, world: WorldState) -> Optional[Dict]`

Called after each failed NBV search. `attempt` is 1, 2, or 3. Returns None if attempt > MAX_RETRIES. Sends context to gpt-oss-120b with reasoning: high. On attempt 3 (final), injects instruction to warn staff in tts_message. Returns None after MAX_RETRIES — planner interprets this as abort.

**Deterministic fallbacks (LLM failure):**
```
attempt 1 → action: RETRY_UNIFORM_SEARCH, reset_probability_map: True
             tts: "Searching again for {tool}."
attempt 2 → action: ASK_USER_CONFIRM_LOCATION
             tts: "I still cannot find the {tool}. Can you confirm it is on the tray?"
attempt 3 → action: ABORT_TOOL_NOT_FOUND (final search attempt before abort)
             tts: "Last attempt — searching one final time for the {tool}."
```
After attempt 3 returns and search still fails: planner calls `_abort_task("I was unable to find the {tool}. Please check the tray or use manual procedure.")`

#### `propose_grasp_recovery(self, tool, attempt, world) -> Optional[Dict]`

**Signature:** `propose_grasp_recovery(tool: str, attempt: int, world: WorldState) -> Optional[Dict]`

Called after each failed gripper force confirmation. Reasoning: high. On attempt 3, tts warns staff. Returns None if attempt > MAX_RETRIES.

**Deterministic fallbacks:**
```
attempt 1 → action: RETRY_GRASP_REPOSITION, rotation_deg: 15.0, force_delta_n: 0.0
             tts: "Adjusting grip on {tool}. Retrying."
attempt 2 → action: RETRY_GRASP_FORCE_INCREASE, force_delta_n: 1.0 (→ 4.0N total)
             tts: "Retrying grasp of {tool} with adjusted force."
attempt 3 → action: RETRY_GRASP_FORCE_INCREASE, force_delta_n: 2.0 (→ 5.0N total, max)
             tts: "Last attempt to grasp the {tool}. Please ensure it is correctly positioned."
```
After attempt 3 fails: planner calls `_abort_task("Unable to grasp the {tool}. Please reposition it and try again.")`

#### `propose_ik_recovery(self, tool, attempt, context, world) -> Optional[Dict]`

**Signature:** `propose_ik_recovery(tool: str, attempt: int, context: TaskContext, world: WorldState) -> Optional[Dict]`

Called after each IK solve failure. Passes `context.alternate_orientation_tried` and `len(context.detection_candidates)` to LLM. Reasoning: high. Returns None if attempt > MAX_RETRIES.

**Deterministic fallbacks:**
```
attempt 1, alternate not tried → action: RETRY_IK_ALTERNATE_ORIENTATION, rotation_deg: 90.0
                                   tts: "Adjusting approach angle for {tool}."
attempt 1/2, has candidates   → action: RETRY_IK_NEXT_CANDIDATE
                                   tts: "Trying alternate position for {tool}."
attempt 3, final              → tts: "Last attempt to reach the {tool}."
no candidates remain          → action: ABORT_IK_FAILED
                                   tts: "Unable to reach the {tool}. Please reposition it and try again."
```

#### `propose_handover_face_recovery(self, user_name, tool, attempt, current_z) -> Dict`

**Signature:** `propose_handover_face_recovery(user_name: str, tool: str, attempt: int, current_z: float) -> Dict`

Called after each face verification failure during handover. Reasoning: low. Returns Dict always (never None — handover never aborts on face failure). On attempt 3 → always returns HANDOVER_VOICE_HAND_ONLY regardless of LLM.

**Deterministic fallbacks:**
```
attempt 1 → action: HANDOVER_Z_UP, z_offset_m: +0.05
             tts: "Please look at the camera."
attempt 2 → action: HANDOVER_Z_DOWN, z_offset_m: -0.05
             tts: "Please face the camera directly."
attempt 3 → action: HANDOVER_VOICE_HAND_ONLY
             tts: "Face verification unavailable. Proceeding with voice and hand confirmation only."
```

#### `learn_from_success(self, context, user_id)`

**Signature:** `learn_from_success(context: TaskContext, user_id: str)`

After successful handover. Updates UserProfile.preferred_zones[tool] = zone_found. Updates time_patterns[current_hour][tool] = zone_found. Both are in-memory only (not persisted across restarts in current implementation — persistence is a future addition).

#### `learn_height_adjustment(self, user_id, command)`

**Signature:** `learn_height_adjustment(user_id: str, command: str)`

Called when user says "lower" or "higher" during handover. Adjusts UserProfile.handover_z_offset by ±0.05m. Clamps to [-0.15, +0.15] (±15cm range). Stored in user_profiles dict (in-memory).

#### `get_handover_pose(self, user_id) -> Tuple[float, float, float]`

**Signature:** `get_handover_pose(user_id: str) -> Tuple[float, float, float]`

Returns (HANDOVER_ZONE.x, HANDOVER_ZONE.y, HANDOVER_ZONE.z + user_z_offset). If no profile for user_id, z_offset = 0.0. SafetyKernel.validate_move() is called by the caller after this returns.

### CLASS: PlannerNode — All Methods

#### `__init__(self)`

Calls super().__init__('planner_node'). Initialises WorldState, TaskContext, AgenticPlanner, SafetyKernel. Creates MutuallyExclusiveCallbackGroup for motion feedback (so heartbeat doesn't share thread with vision/TTS). Creates all publishers and subscribers. Initialises threading.Event for motion and vision wait patterns. Logs startup with model name and MAX_RETRIES.

#### `_on_validated_intent(self, msg)`

Entry point for all fetch commands. Checks world.current_task is None (reject if already tasked). Sets world.current_task = msg.tool. Starts `_execute_fetch_task` in background daemon thread. Returns immediately to not block ROS2 callbacks.

#### `_on_validated_intent_json(self, msg: String)`

Fallback when acare_msgs not available. Parses JSON from std_msgs String. Same logic as above.

#### `_on_vision_result(self, msg)`

Stores vision result in `self._vision_result` dict. Sets `self._vision_event` (threading.Event). Unblocks `_execute_vision_search` which is waiting on this event.

#### `_on_motion_feedback(self, msg)`

Stores `msg.success` in `self._motion_success`. Sets `self._motion_event`. Unblocks `_send_arm_move` which is waiting on this event. Runs in MutuallyExclusiveCallbackGroup.

#### `_on_safety_alert(self, msg)`

Updates `world.safety_severity`. If ESTOP → calls `_handle_estop(msg.reason)`. If CRITICAL or WARNING → logs only (planner adjusts velocity on next move via `SafetyKernel.velocity_scale()`).

#### `_on_hand_status(self, msg)`

Stores latest hand status in `self._latest_hand_status` dict. Used by `_wait_for_hand_detect()` polling loop.

#### `_on_robot_state(self, msg)`

Updates `world.robot_state` and `world.active_user_id` from state_manager.

#### `_execute_fetch_task(self, tool, user_id, user_name)`

**Signature:** `_execute_fetch_task(tool: str, user_id: str, user_name: str)` — runs in background thread

Full task pipeline. Records pipeline_start. Resets TaskContext. Calls each phase in sequence. On any phase failure → calls `_abort_task()`. On full success → calls `learn_from_success()`, logs, speaks, transitions to STANDBY.

**Sequence:**
```python
_check_world_state()           # abort if fail
_send_gripper_open()           # abort if fail
_phase_vision_search()         # abort if all 3 attempts fail
_phase_grasp()                 # abort if all 3 attempts fail
_phase_handover()              # safe_deposit if fail
learn_from_success()
_log_success()
_speak("Handover complete. Is there anything else?")
_transition_state('STANDBY')
```

#### `_check_world_state(self) -> bool`

Returns False (with TTS) if: safety_severity == ESTOP, vision_status == LOADING or ERROR, network_ok == False. Returns True if all clear.

#### `_phase_vision_search(self, tool, user_id) -> bool`

**Signature:** `_phase_vision_search(tool: str, user_id: str) -> bool`

Outer loop for all vision search attempts. Runs up to MAX_RETRIES iterations.

**Loop body:**
```
iteration 1:
  propose_search_strategy() → get priority_zones, reset_probability_map
  _speak(strategy.tts_message)
  _execute_vision_search(tool, reset_probability_map, priority_zones)
  Found → return True

iteration 2:
  propose_vision_recovery(tool, attempt=2, world)
  _speak(recovery.tts_message)
  If action == ASK_USER_CONFIRM_LOCATION: time.sleep(5.0)
  _execute_vision_search(tool, reset_probability_map, priority_zones)
  Found → return True

iteration 3:
  propose_vision_recovery(tool, attempt=3, world)
  _speak(recovery.tts_message)  ← "Last attempt..."
  _execute_vision_search(tool, reset_probability_map, priority_zones)
  Found → return True

All 3 fail → return False
```

#### `_phase_grasp(self, tool) -> bool`

**Signature:** `_phase_grasp(tool: str) -> bool`

Outer loop for all grasp attempts. Runs up to MAX_RETRIES iterations.

**Loop body per iteration:**
```
iteration 1: force_target=3.0, rotation_deg=0.0
iterations 2-3: propose_grasp_recovery() → get force_delta_n, rotation_deg
                force_target = 3.0 + force_delta_n, clamped to 10.0N max
                _speak(recovery.tts_message)

Each iteration:
  SafetyKernel.validate_grasp(force_target, world)
  Compute pregrasp = grasp_point + (0, 0, +0.05)
  SafetyKernel.validate_move(pregrasp, world)
  vel = SafetyKernel.velocity_scale(world) × 0.8
  _send_arm_move(pregrasp, vel)
  SafetyKernel.validate_move(grasp_point, world)
  vel = SafetyKernel.velocity_scale(world) × 0.5
  _send_arm_move(grasp_point, vel, rotation_offset_deg)
  _send_gripper_grasp(force_target)
  time.sleep(0.5)
  Check world.gripper_force >= 1.0N → return True
  Else → continue loop

All 3 fail → return False
```

#### `_resolve_ik(self, target_pos, tool) -> Optional[List[float]]`

**Signature:** `_resolve_ik(target_pos: Tuple[float,float,float], tool: str) -> Optional[List[float]]`

Calls ik_solver.solve(target_pos). On failure, calls propose_ik_recovery() and executes action (alternate orientation, next candidate). Returns joint_angles list or None after MAX_RETRIES.

**Loop body:**
```
call ik_solver.solve(target_pos, rotation_offset_deg)
If solution found → return joint_angles

propose_ik_recovery(tool, attempt, context, world)
_speak(recovery.tts_message)

RETRY_IK_ALTERNATE_ORIENTATION:
  rotation_offset_deg = recovery.params.rotation_deg
  context.alternate_orientation_tried = True
  Retry ik_solver.solve with new rotation

RETRY_IK_NEXT_CANDIDATE:
  Pop next from context.detection_candidates
  target_pos = (candidate.x, candidate.y, candidate.z)
  context.grasp_point = target_pos

ABORT_IK_FAILED:
  return None

After MAX_RETRIES → return None
```

#### `_phase_handover(self, tool, user_id, user_name) -> bool`

**Signature:** `_phase_handover(tool: str, user_id: str, user_name: str) -> bool`

Full handover protocol. Moves arm to handover pose. Runs 3 substates: face verify (with recovery), hand detect, voice confirm. Calls SafetyKernel.validate_release() before release. Returns True on successful handover, False on timeout or safety rejection.

**Sequence:**
```
_transition_state('HOLDING')
get_handover_pose(user_id) → handover_pose
SafetyKernel.validate_handover(world)
SafetyKernel.validate_move(handover_pose, world)
_send_arm_move(handover_pose, velocity_scale)
_transition_state('HANDOVER')
_speak("{tool} ready. Please face the camera.")
handover_start = time.monotonic()
current_z = handover_pose[2]

FACE_VERIFY loop (max 3):
  _wait_for_face_verify(user_id, timeout=8.0)
  If found → face_verified=True, break
  propose_handover_face_recovery(user_name, tool, attempt, current_z)
  _speak(recovery.tts_message)
  Execute Z adjustment (validate + move) or set face_skipped=True

Timeout check: (time.monotonic() - handover_start) > HANDOVER_TIMEOUT_S → return False

HAND_DETECT:
  _speak("Please place your open palm under the gripper.")
  _wait_for_hand_detect(timeout=10.0)
  If not detected: _speak("Please open your palm."), _wait_for_hand_detect(timeout=8.0)
  Dynamic palm tracking: update arm target from /hand_status (x,y,z) in real-time
  Handle "lower"/"higher" voice commands → learn_height_adjustment()

VOICE_CONFIRM:
  _speak("Say 'take' to receive.")
  _wait_for_voice_confirm(user_id, timeout=5.0)

SafetyKernel.validate_release(world, face_verified, hand_ok, voice_ok)
If rejected → _speak("Handover verification failed. Returning tool to tray.") → return False

If face_skipped: _log_event("FACE_VERIFY_SKIPPED", tool)
_send_gripper_release()
time.sleep(0.5)
world.arm_holding = False
return True
```

#### `_execute_vision_search(self, tool, reset_probability_map, priority_zones) -> bool`

**Signature:** `_execute_vision_search(tool: str, reset_probability_map: bool, priority_zones: List[str]) -> bool`

Publishes /vision_search_request. Clears and waits on `_vision_event` (timeout 30s). On result received: checks found=True and confidence >= 0.7. Stores grasp_point and detection_candidates in context. Returns True/False.

#### `_safe_deposit(self, tool)`

**Signature:** `_safe_deposit(tool: str = '')`

Controlled move to SAFE_DROP_ZONE. Always validates move first. velocity_scale=0.3. Releases gripper. Clears world.arm_holding. Transitions to STANDBY. Logs SAFE_DEPOSIT event. Called when: handover fails, ESTOP while holding, network fail while holding.

#### `_handle_estop(self, reason)`

If world.arm_holding → calls `_safe_deposit()` first (controlled deposit). Then transitions to ESTOP state. Clears current_task.

#### `_wait_for_face_verify(self, user_id, timeout) -> bool`

Polls for face verification result from auth_node. In production: subscribes to /auth_result, checks face_verified field and user_id match. Timeout returns False.

#### `_wait_for_hand_detect(self, timeout) -> bool`

Polls `self._latest_hand_status` every 100ms. Returns True when hand_detected=True AND is_open=True AND palm_up=True, all simultaneously. Returns False on timeout.

#### `_wait_for_voice_confirm(self, user_id, timeout) -> bool`

Polls for voice confirmation from voice_node. Checks keyword ("take"/"yes") AND d-vector consistency for user_id. Timeout returns False.

#### `_send_arm_move(self, position, velocity_scale, rotation_offset_deg) -> bool`

**Signature:** `_send_arm_move(position: Tuple[float,float,float], velocity_scale: float = 1.0, rotation_offset_deg: float = 0.0) -> bool`

Calls `_resolve_ik(position)` (activate when hardware params available). Constructs ArmCommand with command="MOVE", joint_angles, velocity_scale. Publishes to /arm_command. Clears _motion_event. Waits on _motion_event (timeout 15s). Returns True if MotionFeedback.success.

**Task phase velocity scales:**
```
Pre-grasp approach: × 0.8
Grasp descent: × 0.5
Move to handover: × 0.6
Safe deposit: × 0.3
All others: × 1.0
```

#### `_send_gripper_open(self) -> bool`

Publishes GripperCommand {command="RELEASE", force_target=0.0}. Waits 600ms for physical open time (~500ms per spec).

#### `_send_gripper_grasp(self, force_target) -> bool`

Publishes GripperCommand {command="GRASP", force_target}. Returns True (force confirmation done by caller after sleep).

#### `_send_gripper_release(self) -> bool`

Publishes GripperCommand {command="RELEASE", force_target=0.0}. Waits 600ms for physical open/drop.

#### `_speak(self, text)`

Publishes text to /tts_request (String). voice_node handles routing to Edge TTS / Kokoro / pyttsx3.

#### `_transition_state(self, target)`

Updates world.robot_state. Publishes StateTransition to /state_transition → state_manager receives and enforces.

#### `_abort_task(self, message)`

Logs error. Speaks message. Logs TASK_ABORTED event. Clears world.current_task. Sends arm to neutral (velocity_scale=0.5). Transitions to STANDBY.

#### `_log_success(self)`

Logs full latency breakdown: vision_search_ms, motion_ms, total_task_ms, all retry counters (vision, grasp, ik, face). Publishes LogEvent to /log_event.

#### `_log_event(self, event_type, tool, description)`

Constructs LogEvent with all fields. Publishes to /log_event → log_node writes to SQLite.

### Complete Task Flow

```
ValidatedIntent {tool, action} + Authenticated Identity ↓
Record pipeline_start_time ↓
Check /vision_status — wait if LOADING, TTS: 'System initialising. Please wait.' ↓
Tool Registry Lookup → map tool name + aliases → YOLOv11 class label ↓
destination = 'user_handover'  # always — not inferred by Groq ↓
get_world_state() — check safety_severity, network_ok, arm_holding ↓
Gripper: send GRIPPER_OPEN, wait for force sensor = 0 ↓
Record vision_start_time
Vision NBV Search → /vision_search_request → wait for /vision_result
Record vision_search_ms = now - vision_start_time ↓
Grasp point received → IK solver (DLS, max 100 iterations)
IK failure → recovery flow (see Vision section) ↓
Record motion_start_time
ArmCommand: MOVE_TO_PREGRASP (5cm above tool) → wait MotionFeedback.success ↓
ArmCommand: GRASP {force_target: 3.0N} → wait MotionFeedback.success ↓
Gripper force sensor confirmation:
  Confirmed → proceed
  Failed after 3 attempts → TTS: 'Grasp failed. Please reposition the {tool}.'
  ArmCommand: MOVE_NEUTRAL → State → STANDBY ↓
ArmCommand: MOVE_TO_HANDOVER_ZONE → wait MotionFeedback.success
Record motion_ms = now - motion_start_time ↓
TTS: '{tool} ready. Please face the camera.' ↓
HANDOVER — Three-Check Verification (managed by handover.py module):
  Substate FACE_VERIFY: continuous face check every 0.5s, threshold 0.78
  Substate HAND_DETECT: wait for open palm in handover zone via MediaPipe
  Substate VOICE_CONFIRM: TTS 'Say take to receive.' → voice check → RELEASE ↓
Force sensor drops to zero → collection confirmed ↓
Record total_task_ms = now - pipeline_start_time
Log event {tool, staff_id, timestamp, zone_found, grasp_attempts, success,
           voice_e2e_ms, vision_search_ms, motion_ms, total_task_ms}
Update probability_map (zone where tool found) ↓
TTS: 'Handover complete. Is there anything else?'
ArmCommand: MOVE_NEUTRAL → State → STANDBY
```

### World State Snapshot — Folded into planner_node

```python
def get_world_state():
    return {
        "robot_state":      current_state,
        "safety_severity":  latest_safety_alert.severity,
        "vision_confidence": latest_vision_result.confidence,
        "network_ok":       deepgram_latency < threshold,
        "arm_holding":      gripper_force > 0
    }
```

Planner calls get_world_state() before every major decision point — before vision search, before grasp, before handover release, after any safety alert.

### Tool Registry — Alias Handling

```python
TOOL_REGISTRY = {
    "cream":        {"yolo_class": "cream",        "aliases": ["lotion", "ointment", "topical"]},
    "scissors":     {"yolo_class": "scissors",     "aliases": ["medical scissors", "surgical scissors", "the smaller one", "cutting tool"]},
    "oximeter":     {"yolo_class": "oximeter",     "aliases": ["oxymeter", "pulse ox", "oxygen monitor", "SPO2"]},
    "plaster":      {"yolo_class": "plaster",      "aliases": ["bandaid", "strip", "adhesive strip"]},
    "forceps":      {"yolo_class": "forceps",      "aliases": ["surgical forceps", "tweezers", "clamps", "graspers"]},
    "thermometer":  {"yolo_class": "thermometer",  "aliases": ["temp probe", "temperature tool"]},
}
```

### IK Solver — Implementation

- Method: Damped Least Squares (DLS) / Levenberg-Marquardt
- DLS handles near-singular configurations without diverging — critical for 6-DOF arm near joint limits
- damping_factor: 0.05, max_iterations: 100, position_tolerance: 1mm, orientation_tolerance: 0.01 rad
- Joint limit enforcement: hard clamp at each iteration
- If solution not found within max_iterations → IK failure → recovery flow

### Complete planner_node.py Reference Implementation

```python
#!/usr/bin/env python3
# acare_planner/planner_node.py
# Spec Reference: Section XII (Task Planner Pipeline)
#
# CENTRAL ORCHESTRATOR — Agentic Task Planner for ACARE
#
# The planner_node is the BRAIN. It owns:
#   - Full task lifecycle (fetch → search → grasp → handover)
#   - World state snapshot (safety, network, vision, arm status)
#   - Agentic decision layer (adaptive search, recovery, learning)
#   - Cross-node coordination (voice, vision, auth, safety, embedded)
#
# SAFETY GUARANTEE: All agentic proposals are validated by the
# DeterministicSafetyKernel before execution. Agentic layer proposes,
# safety kernel approves. No exceptions.
#
# RETRY POLICY (per failure type, max 3 each):
#   Vision search  → 3 attempts, escalating strategy, then abort
#   Grasp          → 3 attempts, repositioning + force adjustment, then abort
#   IK solve       → 3 attempts, orientation + candidate fallback, then abort
#   Handover face  → 3 attempts, Z-height search, then voice+hand fallback (not abort)
#   On final attempt → TTS warns user before attempting ("Last try...")
#   After 3 fails  → clear TTS message, STANDBY
#
# AGENTIC MODEL: gpt-oss-120b via Groq (Reasoning: high for recovery,
#                                        Reasoning: low for strategy hints)
#
# Architecture:
#   ┌─────────────────────────────────────────────┐
#   │  AGENTIC DECISION LAYER (proposes)           │
#   │  • gpt-oss-120b, strict JSON schema          │
#   │  • Adaptive NBV search strategy              │
#   │  • Per-failure-type recovery planning        │
#   │  • User preference learning                  │
#   │  • Reasoning: high/low per decision type     │
#   └─────────────────────────────────────────────┘
#              ↓ (proposals validated)
#   ┌─────────────────────────────────────────────┐
#   │  DETERMINISTIC SAFETY KERNEL (enforces)      │
#   │  • Workspace bounds: HARD CLAMP              │
#   │  • Velocity/force/temp: HARD LIMITS          │
#   │  • ESTOP: IMMEDIATE, NO OVERRIDE             │
#   │  • Auth: MUST PASS, NO BYPASS                │
#   └─────────────────────────────────────────────┘
#              ↓ (validated commands)
#   ┌─────────────────────────────────────────────┐
#   │  NODE COORDINATION (executes)                │
#   │  • Publishes to /arm_command                 │
#   │  • Subscribes to /motion_feedback            │
#   │  • Manages /vision_search_request            │
#   │  • Handles /hand_status, /safety_alert       │
#   └─────────────────────────────────────────────┘

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
import threading
import time
import json
import os
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field
from groq import Groq

# ROS2 messages
try:
    from acare_msgs.msg import (
        ValidatedIntent, VisionResult, VisionSearchRequest,
        ArmCommand, GripperCommand, MotionFeedback,
        HandStatus, SafetyAlert, RobotState, LogEvent,
        StateTransition
    )
    MSGS_OK = True
except ImportError:
    MSGS_OK = False
    print("[planner_node] acare_msgs not available — using std_msgs fallbacks")

from std_msgs.msg import String

# =============================================================================
# CONFIGURATION
# =============================================================================

WORKSPACE = {
    'xmin': -0.4, 'xmax': 0.4,
    'ymin': -0.3, 'ymax': 0.3,
    'zmin': 0.0,  'zmax': 0.5,
}

HANDOVER_ZONE   = {'x': 0.0, 'y': 0.4, 'z': 0.1}
SAFE_DROP_ZONE  = {'x': 0.0, 'y': 0.35, 'z': 0.05}

NETWORK_FAIL_HOLD_THRESHOLD_S   = 5.0
HANDOVER_TIMEOUT_S              = 30.0
SESSION_INACTIVITY_TIMEOUT_S    = 300.0

MAX_RETRIES = 3  # Universal cap — applies per failure type independently

# Groq model for agentic layer
AGENTIC_MODEL = "openai/gpt-oss-120b"

# Groq model for intent parsing (unchanged)
INTENT_MODEL = "llama-3.1-8b-instant"

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class WorldState:
    robot_state: str       = 'STANDBY'
    safety_severity: str   = 'OK'       # OK | WARNING | CRITICAL | ESTOP
    vision_status: str     = 'READY'    # LOADING | READY | ERROR
    network_ok: bool       = True
    arm_holding: bool      = False
    gripper_force: float   = 0.0
    active_user_id: str    = ''
    active_user_name: str  = ''
    last_command_time: float = 0.0
    current_task: Optional[str] = None

@dataclass
class RetryCounters:
    """
    Per-failure-type retry counters.
    Each is independent — a grasp fail does not consume a vision retry.
    All capped at MAX_RETRIES (3).
    """
    vision_search: int   = 0   # NBV search returned no result
    grasp: int           = 0   # Gripper failed to confirm hold
    ik_solve: int        = 0   # IK solver could not find solution
    handover_face: int   = 0   # Face verification failed at handover

    def exhausted(self, failure_type: str) -> bool:
        return getattr(self, failure_type, 0) >= MAX_RETRIES

    def increment(self, failure_type: str):
        current = getattr(self, failure_type, 0)
        setattr(self, failure_type, current + 1)

    def is_last_attempt(self, failure_type: str) -> bool:
        """True when the NEXT attempt will be the final one."""
        return getattr(self, failure_type, 0) == MAX_RETRIES - 1

@dataclass
class TaskContext:
    tool_requested: str  = ''
    tool_canonical: str  = ''
    yolo_class: str      = ''
    search_start_time: float = 0.0
    vision_search_ms: int    = 0
    motion_ms: int           = 0
    total_task_ms: int       = 0
    zone_found: str          = ''
    grasp_point: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    pregrasp_point: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    retries: RetryCounters = field(default_factory=RetryCounters)
    # IK recovery state
    alternate_orientation_tried: bool = False
    detection_candidates: List[Dict]  = field(default_factory=list)

@dataclass
class UserProfile:
    user_id: str            = ''
    name: str               = ''
    handover_z_offset: float = 0.0     # learned from lower/higher
    preferred_zones: Dict[str, str] = field(default_factory=dict)  # tool → zone
    last_login: str         = ''

# =============================================================================
# DETERMINISTIC SAFETY KERNEL — Absolute Authority
# =============================================================================

class SafetyKernel:
    """
    Validates ALL proposals before execution.
    Agentic layer proposes. Safety kernel approves. No exceptions.
    """

    @staticmethod
    def validate_move(target_pos: Tuple[float, float, float],
                      world: WorldState) -> Tuple[bool, str]:
        x, y, z = target_pos
        w = WORKSPACE
        if not (w['xmin'] <= x <= w['xmax']):
            return False, f"X={x:.3f} outside workspace [{w['xmin']}, {w['xmax']}]"
        if not (w['ymin'] <= y <= w['ymax']):
            return False, f"Y={y:.3f} outside workspace [{w['ymin']}, {w['ymax']}]"
        if not (w['zmin'] <= z <= w['zmax']):
            return False, f"Z={z:.3f} outside workspace [{w['zmin']}, {w['zmax']}]"
        if world.safety_severity == 'ESTOP':
            return False, "ESTOP active — all motion frozen"
        if world.safety_severity == 'CRITICAL':
            return True, "CRITICAL — velocity capped at 50%"
        return True, "OK"

    @staticmethod
    def validate_grasp(force_target: float, world: WorldState) -> Tuple[bool, str]:
        if force_target > 15.0:
            return False, f"Force {force_target}N exceeds ESTOP limit 15N"
        if force_target > 10.0:
            return True, "WARNING — force near limit"
        return True, "OK"

    @staticmethod
    def validate_handover(world: WorldState) -> Tuple[bool, str]:
        if not world.active_user_id:
            return False, "No active session — handover rejected"
        if world.safety_severity in ('ESTOP', 'CRITICAL'):
            return False, f"Safety severity {world.safety_severity} — handover rejected"
        return True, "OK"

    @staticmethod
    def validate_release(world: WorldState,
                         face_verified: bool,
                         hand_detected: bool,
                         voice_confirmed: bool) -> Tuple[bool, str]:
        """3-check gate before gripper release."""
        if not hand_detected:
            return False, "Hand not detected"
        if not voice_confirmed:
            return False, "Voice confirmation failed"
        # Face is advisory — voice+hand still required; face adds trust level
        if not face_verified:
            return True, "FACE_SKIPPED — proceeding on voice+hand; logged"
        return True, "OK"

    @staticmethod
    def velocity_scale(world: WorldState) -> float:
        """Returns velocity scale factor based on current safety severity."""
        if world.safety_severity == 'CRITICAL':
            return 0.5
        if world.safety_severity == 'WARNING':
            return 0.75
        return 1.0

# =============================================================================
# AGENTIC DECISION LAYER — gpt-oss-120b via Groq
# =============================================================================

# JSON schema for planner decisions — strict mode
DECISION_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "planner_decision",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "decision_type": {
                    "type": "string",
                    "enum": [
                        "SEARCH_STRATEGY",
                        "VISION_RECOVERY",
                        "GRASP_RECOVERY",
                        "IK_RECOVERY",
                        "HANDOVER_RECOVERY",
                        "ABORT"
                    ]
                },
                "reasoning": {"type": "string"},
                "action": {
                    "type": "string",
                    "enum": [
                        "RETRY_UNIFORM_SEARCH",
                        "ASK_USER_CONFIRM_LOCATION",
                        "ABORT_TOOL_NOT_FOUND",
                        "RETRY_GRASP_REPOSITION",
                        "RETRY_GRASP_FORCE_INCREASE",
                        "ABORT_GRASP_FAILED",
                        "RETRY_IK_ALTERNATE_ORIENTATION",
                        "RETRY_IK_NEXT_CANDIDATE",
                        "ABORT_IK_FAILED",
                        "HANDOVER_Z_UP",
                        "HANDOVER_Z_DOWN",
                        "HANDOVER_VOICE_HAND_ONLY",
                        "SEARCH_PRIORITY_ZONES"
                    ]
                },
                "tts_message": {"type": "string"},
                "params": {
                    "type": "object",
                    "properties": {
                        "force_delta_n": {"type": "number"},
                        "z_offset_m": {"type": "number"},
                        "rotation_deg": {"type": "number"},
                        "priority_zones": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "reset_probability_map": {"type": "boolean"}
                    },
                    "required": [
                        "force_delta_n",
                        "z_offset_m",
                        "rotation_deg",
                        "priority_zones",
                        "reset_probability_map"
                    ],
                    "additionalProperties": False
                }
            },
            "required": ["decision_type", "reasoning", "action", "tts_message", "params"],
            "additionalProperties": False
        }
    }
}

PLANNER_SYSTEM_PROMPT = """You are the agentic decision layer of ACARE — an Autonomous Clinical Assistance Robot
operating in a surgical environment. You orchestrate task recovery and search strategy for a
6-DOF robotic arm that fetches sterile instruments for authenticated surgical staff.

HARD RULES you must never violate:
- Never suggest bypassing authentication or safety checks
- Never suggest moving outside workspace bounds
- Never suggest gripper force above 10N (ESTOP at 15N, you stay well below)
- Only suggest actions from the allowed action enum
- If uncertain, choose ABORT over unsafe continuation
- Keep tts_message brief (1-2 sentences), professional, clinical tone

CONTEXT: You receive the current world state, failure type, attempt number, and task context.
You output a structured decision with the action to take, a TTS message for the staff, and parameters.

For the final attempt (attempt 3 of 3): tts_message MUST include a warning that this is the last try.
Example: "Last attempt — searching one final time for the scalpel."
After 3 failures: tts_message must clearly state inability and suggest manual procedure."""


class AgenticPlanner:
    """
    Proposes adaptive strategies via gpt-oss-120b.
    All proposals validated by SafetyKernel before execution.
    """

    def __init__(self, logger=None):
        self.logger = logger
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
        self.user_profiles: Dict[str, UserProfile] = {}
        self.time_patterns: Dict[int, Dict[str, str]] = {}

    def _call_llm(self, messages: List[Dict], reasoning_level: str = "low") -> Optional[Dict]:
        """
        Call gpt-oss-120b with strict JSON schema.
        reasoning_level: "low" for strategy hints, "high" for recovery decisions.
        Returns parsed decision dict or None on failure.
        """
        try:
            # Inject reasoning level into system prompt
            system = PLANNER_SYSTEM_PROMPT + f"\n\nReasoning: {reasoning_level}"
            full_messages = [{"role": "system", "content": system}] + messages

            response = self.client.chat.completions.create(
                model=AGENTIC_MODEL,
                messages=full_messages,
                response_format=DECISION_SCHEMA,
                temperature=0.1,        # Near-deterministic for robot decisions
                max_completion_tokens=512
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Agentic LLM call failed: {e}")
            return None

    # -------------------------------------------------------------------------
    # Search strategy — reasoning: low (pattern lookup, not complex reasoning)
    # -------------------------------------------------------------------------

    def propose_search_strategy(self, tool: str, user_id: str,
                                 current_hour: int,
                                 attempt_number: int) -> Dict:
        """
        Propose NBV viewpoint ordering before first search.
        Returns decision dict with SEARCH_STRATEGY action.
        """
        profile = self.user_profiles.get(user_id)
        hour_pref = self.time_patterns.get(current_hour, {}).get(tool)
        user_pref = profile.preferred_zones.get(tool) if profile else None

        context_str = json.dumps({
            "tool": tool,
            "attempt_number": attempt_number,
            "current_hour": current_hour,
            "time_based_zone_hint": hour_pref,
            "user_preferred_zone": user_pref,
            "failure_type": "SEARCH_STRATEGY",
            "world_context": "Pre-search — no failures yet"
        })

        decision = self._call_llm(
            [{"role": "user", "content": context_str}],
            reasoning_level="low"
        )

        # Fallback if LLM fails — use default probability map ordering
        if decision is None:
            return {
                "decision_type": "SEARCH_STRATEGY",
                "action": "SEARCH_PRIORITY_ZONES",
                "reasoning": "LLM unavailable — using probability map default",
                "tts_message": f"Searching for {tool}.",
                "params": {
                    "priority_zones": [user_pref or hour_pref or ""],
                    "reset_probability_map": False,
                    "force_delta_n": 0.0,
                    "z_offset_m": 0.0,
                    "rotation_deg": 0.0
                }
            }
        return decision

    # -------------------------------------------------------------------------
    # Recovery decisions — reasoning: high (multi-step causal reasoning)
    # -------------------------------------------------------------------------

    def propose_vision_recovery(self, tool: str, attempt: int,
                                 world: WorldState) -> Optional[Dict]:
        """
        Recovery after vision search found nothing.
        Attempt 1 → uniform retry. Attempt 2 → ask user. Attempt 3 → abort.
        """
        if attempt > MAX_RETRIES:
            return None

        is_last = (attempt == MAX_RETRIES)

        context_str = json.dumps({
            "tool": tool,
            "failure_type": "TOOL_NOT_FOUND",
            "attempt_number": attempt,
            "max_retries": MAX_RETRIES,
            "is_final_attempt": is_last,
            "safety_severity": world.safety_severity,
            "network_ok": world.network_ok,
            "instruction": (
                "This is the FINAL attempt. tts_message must warn staff."
                if is_last else
                "Propose next recovery step."
            )
        })

        decision = self._call_llm(
            [{"role": "user", "content": context_str}],
            reasoning_level="high"
        )

        # Deterministic fallback per attempt number
        if decision is None:
            fallbacks = {
                1: {
                    "decision_type": "VISION_RECOVERY",
                    "action": "RETRY_UNIFORM_SEARCH",
                    "reasoning": "First retry: search all zones uniformly",
                    "tts_message": f"Searching again for {tool}.",
                    "params": {"reset_probability_map": True, "priority_zones": [],
                               "force_delta_n": 0.0, "z_offset_m": 0.0, "rotation_deg": 0.0}
                },
                2: {
                    "decision_type": "VISION_RECOVERY",
                    "action": "ASK_USER_CONFIRM_LOCATION",
                    "reasoning": "Second retry: ask user for guidance",
                    "tts_message": f"I still cannot find the {tool}. Can you confirm it is on the tray?",
                    "params": {"reset_probability_map": False, "priority_zones": [],
                               "force_delta_n": 0.0, "z_offset_m": 0.0, "rotation_deg": 0.0}
                },
                3: {
                    "decision_type": "VISION_RECOVERY",
                    "action": "ABORT_TOOL_NOT_FOUND",
                    "reasoning": "Max retries reached",
                    "tts_message": f"Last attempt — searching one final time for the {tool}.",
                    "params": {"reset_probability_map": True, "priority_zones": [],
                               "force_delta_n": 0.0, "z_offset_m": 0.0, "rotation_deg": 0.0}
                }
            }
            return fallbacks.get(attempt)

        return decision

    def propose_grasp_recovery(self, tool: str, attempt: int,
                                world: WorldState) -> Optional[Dict]:
        """
        Recovery after gripper failed to confirm hold.
        Attempt 1 → reposition approach. Attempt 2 → slight force increase.
        Attempt 3 → final try with max safe force. After 3 → abort.
        """
        if attempt > MAX_RETRIES:
            return None

        is_last = (attempt == MAX_RETRIES)

        context_str = json.dumps({
            "tool": tool,
            "failure_type": "GRASP_FAILED",
            "attempt_number": attempt,
            "max_retries": MAX_RETRIES,
            "is_final_attempt": is_last,
            "current_gripper_force": world.gripper_force,
            "safety_severity": world.safety_severity,
            "instruction": (
                "FINAL attempt. tts_message must warn. Max safe force is 10N — do not exceed."
                if is_last else
                "Propose next grasp recovery. Force must stay below 10N."
            )
        })

        decision = self._call_llm(
            [{"role": "user", "content": context_str}],
            reasoning_level="high"
        )

        if decision is None:
            fallbacks = {
                1: {
                    "decision_type": "GRASP_RECOVERY",
                    "action": "RETRY_GRASP_REPOSITION",
                    "reasoning": "First retry: reposition approach angle",
                    "tts_message": f"Adjusting grip on {tool}. Retrying.",
                    "params": {"force_delta_n": 0.0, "rotation_deg": 15.0,
                               "priority_zones": [], "z_offset_m": 0.0,
                               "reset_probability_map": False}
                },
                2: {
                    "decision_type": "GRASP_RECOVERY",
                    "action": "RETRY_GRASP_FORCE_INCREASE",
                    "reasoning": "Second retry: slight force increase",
                    "tts_message": f"Retrying grasp of {tool} with adjusted force.",
                    "params": {"force_delta_n": 1.0, "rotation_deg": 0.0,
                               "priority_zones": [], "z_offset_m": 0.0,
                               "reset_probability_map": False}
                },
                3: {
                    "decision_type": "GRASP_RECOVERY",
                    "action": "RETRY_GRASP_FORCE_INCREASE",
                    "reasoning": "Final retry: max safe force",
                    "tts_message": f"Last attempt to grasp the {tool}. Please ensure it is correctly positioned.",
                    "params": {"force_delta_n": 2.0, "rotation_deg": 0.0,
                               "priority_zones": [], "z_offset_m": 0.0,
                               "reset_probability_map": False}
                }
            }
            return fallbacks.get(attempt)

        return decision

    def propose_ik_recovery(self, tool: str, attempt: int,
                             context: 'TaskContext',
                             world: WorldState) -> Optional[Dict]:
        """
        Recovery after IK solver failed.
        Attempt 1 → alternate approach orientation (rotate 90°).
        Attempt 2 → try next detection candidate.
        Attempt 3 → final candidate or abort.
        """
        if attempt > MAX_RETRIES:
            return None

        is_last = (attempt == MAX_RETRIES)
        has_candidates = len(context.detection_candidates) > 0

        context_str = json.dumps({
            "tool": tool,
            "failure_type": "IK_FAILED",
            "attempt_number": attempt,
            "max_retries": MAX_RETRIES,
            "is_final_attempt": is_last,
            "alternate_orientation_tried": context.alternate_orientation_tried,
            "remaining_candidates": len(context.detection_candidates),
            "safety_severity": world.safety_severity,
            "instruction": (
                "FINAL attempt. If no candidates remain, action must be ABORT_IK_FAILED."
                if is_last else
                "Propose IK recovery. Prefer alternate orientation first, then next candidate."
            )
        })

        decision = self._call_llm(
            [{"role": "user", "content": context_str}],
            reasoning_level="high"
        )

        if decision is None:
            if attempt == 1 and not context.alternate_orientation_tried:
                return {
                    "decision_type": "IK_RECOVERY",
                    "action": "RETRY_IK_ALTERNATE_ORIENTATION",
                    "reasoning": "First retry: rotate approach 90°",
                    "tts_message": f"Adjusting approach angle for {tool}.",
                    "params": {"rotation_deg": 90.0, "force_delta_n": 0.0,
                               "z_offset_m": 0.0, "priority_zones": [],
                               "reset_probability_map": False}
                }
            elif has_candidates:
                is_last_str = f"Last attempt to reach the {tool}. " if is_last else ""
                return {
                    "decision_type": "IK_RECOVERY",
                    "action": "RETRY_IK_NEXT_CANDIDATE",
                    "reasoning": "Try next detection candidate",
                    "tts_message": f"{is_last_str}Trying alternate position for {tool}.",
                    "params": {"rotation_deg": 0.0, "force_delta_n": 0.0,
                               "z_offset_m": 0.0, "priority_zones": [],
                               "reset_probability_map": False}
                }
            else:
                return {
                    "decision_type": "IK_RECOVERY",
                    "action": "ABORT_IK_FAILED",
                    "reasoning": "No candidates remain — abort",
                    "tts_message": f"Unable to reach the {tool}. Please reposition it and try again.",
                    "params": {"rotation_deg": 0.0, "force_delta_n": 0.0,
                               "z_offset_m": 0.0, "priority_zones": [],
                               "reset_probability_map": False}
                }

        return decision

    def propose_handover_face_recovery(self, user_name: str, tool: str,
                                        attempt: int,
                                        current_z: float) -> Dict:
        """
        Recovery when face verification fails at handover.
        Attempt 1 → Z up +5cm. Attempt 2 → Z down -5cm from default.
        Attempt 3 → proceed on voice+hand only with logged warning.
        This does NOT abort the handover — handover continues with degraded trust.
        """
        # Attempt 3 is voice+hand fallback, not abort — spec section VII
        context_str = json.dumps({
            "user_name": user_name,
            "tool": tool,
            "failure_type": "FACE_VERIFY_FAILED",
            "attempt_number": attempt,
            "max_retries": MAX_RETRIES,
            "current_z_m": current_z,
            "handover_zone_default_z": HANDOVER_ZONE['z'],
            "instruction": (
                "Attempt 3: cannot abort handover. Must use HANDOVER_VOICE_HAND_ONLY as fallback."
                if attempt >= MAX_RETRIES else
                "Adjust Z-height to help find user face."
            )
        })

        decision = self._call_llm(
            [{"role": "user", "content": context_str}],
            reasoning_level="low"
        )

        if decision is None:
            fallbacks = {
                1: {
                    "decision_type": "HANDOVER_RECOVERY",
                    "action": "HANDOVER_Z_UP",
                    "reasoning": "Move arm up to find face",
                    "tts_message": "Please look at the camera.",
                    "params": {"z_offset_m": 0.05, "force_delta_n": 0.0,
                               "rotation_deg": 0.0, "priority_zones": [],
                               "reset_probability_map": False}
                },
                2: {
                    "decision_type": "HANDOVER_RECOVERY",
                    "action": "HANDOVER_Z_DOWN",
                    "reasoning": "Move arm down to find face",
                    "tts_message": "Please face the camera directly.",
                    "params": {"z_offset_m": -0.05, "force_delta_n": 0.0,
                               "rotation_deg": 0.0, "priority_zones": [],
                               "reset_probability_map": False}
                },
            }
            if attempt >= MAX_RETRIES:
                return {
                    "decision_type": "HANDOVER_RECOVERY",
                    "action": "HANDOVER_VOICE_HAND_ONLY",
                    "reasoning": "Face not found after 3 attempts — proceeding on voice+hand with warning log",
                    "tts_message": "Face verification unavailable. Proceeding with voice and hand confirmation only.",
                    "params": {"z_offset_m": 0.0, "force_delta_n": 0.0,
                               "rotation_deg": 0.0, "priority_zones": [],
                               "reset_probability_map": False}
                }
            return fallbacks.get(attempt, fallbacks[1])

        return decision

    # -------------------------------------------------------------------------
    # Learning
    # -------------------------------------------------------------------------

    def learn_from_success(self, context: 'TaskContext', user_id: str):
        profile = self.user_profiles.setdefault(
            user_id, UserProfile(user_id=user_id)
        )
        if context.zone_found:
            profile.preferred_zones[context.tool_canonical] = context.zone_found
        hour = datetime.now().hour
        self.time_patterns.setdefault(hour, {})[context.tool_canonical] = context.zone_found
        if self.logger:
            self.logger.info(
                f"Agentic learned: {context.tool_canonical} → {context.zone_found} "
                f"for user {user_id} at hour {hour}"
            )

    def learn_height_adjustment(self, user_id: str, command: str):
        profile = self.user_profiles.setdefault(
            user_id, UserProfile(user_id=user_id)
        )
        delta = -0.05 if command == 'lower' else 0.05
        profile.handover_z_offset = max(-0.15, min(0.15,
            profile.handover_z_offset + delta
        ))

    def get_handover_pose(self, user_id: str) -> Tuple[float, float, float]:
        profile = self.user_profiles.get(user_id)
        z_offset = profile.handover_z_offset if profile else 0.0
        return (
            HANDOVER_ZONE['x'],
            HANDOVER_ZONE['y'],
            HANDOVER_ZONE['z'] + z_offset
        )

# =============================================================================
# MAIN PLANNER NODE
# =============================================================================

class PlannerNode(Node):

    def __init__(self):
        super().__init__('planner_node')

        self.world   = WorldState()
        self.context = TaskContext()
        self.agentic = AgenticPlanner(logger=self.get_logger())
        self.safety  = SafetyKernel()

        self.cmd_group = MutuallyExclusiveCallbackGroup()

        # --- Publishers ---
        if MSGS_OK:
            self.arm_pub        = self.create_publisher(ArmCommand,           '/arm_command',             10)
            self.gripper_pub    = self.create_publisher(GripperCommand,        '/gripper_command',         10)
            self.vision_req_pub = self.create_publisher(VisionSearchRequest,   '/vision_search_request',   10)
            self.state_pub      = self.create_publisher(StateTransition,       '/state_transition',        10)
            self.log_pub        = self.create_publisher(LogEvent,              '/log_event',               10)
            self.tts_pub        = self.create_publisher(String,                '/tts_request',             10)
        else:
            self.arm_pub        = self.create_publisher(String, '/arm_command_json',            10)
            self.gripper_pub    = self.create_publisher(String, '/gripper_command_json',        10)
            self.vision_req_pub = self.create_publisher(String, '/vision_search_request_json',  10)
            self.tts_pub        = self.create_publisher(String, '/tts_request',                 10)

        # --- Subscribers ---
        if MSGS_OK:
            self.create_subscription(ValidatedIntent,      '/validated_intent',        self._on_validated_intent,  10)
            self.create_subscription(VisionResult,         '/vision_result',           self._on_vision_result,     10)
            self.create_subscription(MotionFeedback,       '/motion_feedback',         self._on_motion_feedback,   10,
                                     callback_group=self.cmd_group)
            self.create_subscription(SafetyAlert,          '/safety_alert',            self._on_safety_alert,      10)
            self.create_subscription(HandStatus,           '/hand_status',             self._on_hand_status,       10)
            self.create_subscription(RobotState,           '/robot_state',             self._on_robot_state,       10)
        else:
            self.create_subscription(String, '/validated_intent_json',
                                     self._on_validated_intent_json, 10)

        # --- Internal events ---
        self._task_thread: Optional[threading.Thread] = None
        self._task_lock   = threading.Lock()
        self._motion_event   = threading.Event()
        self._motion_success = False
        self._vision_event   = threading.Event()
        self._vision_result: Dict = {}
        self._latest_hand_status: Dict = {}

        self.get_logger().info(
            f'PlannerNode ready — agentic model: {AGENTIC_MODEL}, max retries per failure: {MAX_RETRIES}'
        )

    # =====================================================================
    # ROS2 CALLBACKS
    # =====================================================================

    def _on_validated_intent(self, msg):
        if msg.action != 'fetch':
            self._speak("I can only fetch tools right now.")
            return

        with self._task_lock:
            if self.world.current_task:
                self._speak("I am already working on a task. Please wait.")
                return
            self.world.current_task = msg.tool
            self.world.last_command_time = time.monotonic()

        self._task_thread = threading.Thread(
            target=self._execute_fetch_task,
            args=(msg.tool, msg.user_id, msg.user_name),
            daemon=True
        )
        self._task_thread.start()

    def _on_validated_intent_json(self, msg: String):
        try:
            data = json.loads(msg.data)
            if data.get('action') != 'fetch':
                return
            with self._task_lock:
                if self.world.current_task:
                    return
                self.world.current_task = data['tool']
            self._task_thread = threading.Thread(
                target=self._execute_fetch_task,
                args=(data['tool'], data.get('user_id', 'unknown'),
                      data.get('user_name', 'User')),
                daemon=True
            )
            self._task_thread.start()
        except json.JSONDecodeError as e:
            self.get_logger().error(f"Invalid JSON intent: {e}")

    def _on_vision_result(self, msg):
        self._vision_result = {
            'found': msg.found,
            'tool': msg.tool,
            'x': msg.x, 'y': msg.y, 'z': msg.z,
            'confidence': msg.confidence,
            'zone': msg.zone
        }
        self._vision_event.set()

    def _on_motion_feedback(self, msg):
        self._motion_success = msg.success
        self._motion_event.set()

    def _on_safety_alert(self, msg):
        self.world.safety_severity = msg.severity
        if msg.severity == 'ESTOP':
            self.get_logger().error(f"ESTOP: {msg.source} — {msg.reason}")
            self._handle_estop(msg.reason)
        elif msg.severity == 'CRITICAL':
            self.get_logger().warn(f"CRITICAL: {msg.source} — {msg.reason}")
        elif msg.severity == 'WARNING':
            self.get_logger().info(f"WARNING: {msg.source} — {msg.reason}")

    def _on_hand_status(self, msg):
        self._latest_hand_status = {
            'detected': msg.hand_detected,
            'is_open': msg.is_open,
            'palm_up': msg.palm_up,
            'x': msg.x, 'y': msg.y, 'z': msg.z
        }

    def _on_robot_state(self, msg):
        self.world.robot_state    = msg.state
        self.world.active_user_id = msg.active_user_id

    # =====================================================================
    # MAIN TASK PIPELINE
    # =====================================================================

    def _execute_fetch_task(self, tool: str, user_id: str, user_name: str):
        """
        FULL PIPELINE:
        1. Setup + world state check
        2. Open gripper
        3. Vision search (with agentic strategy + per-type retries)
        4. Grasp (with per-type retries)
        5. Handover (3-check: face + hand + voice, with per-type retries on face)
        6. Cleanup + learning
        """
        pipeline_start = time.monotonic()
        self.get_logger().info(f"=== TASK START: fetch '{tool}' for {user_name} ===")

        self._transition_state('PROCESSING')
        self.context = TaskContext(
            tool_requested=tool,
            tool_canonical=tool,
            search_start_time=pipeline_start
        )

        # --- Phase 0: Preconditions ---
        if not self._check_world_state():
            self._abort_task("System not ready to accept commands.")
            return

        # --- Phase 1: Open gripper ---
        self._speak(f"Fetching {tool}. One moment.")
        if not self._send_gripper_open():
            self._abort_task("Gripper could not be opened.")
            return

        # --- Phase 2: Vision search ---
        self._transition_state('EXECUTING')
        vision_start = time.monotonic()

        found = self._phase_vision_search(tool, user_id)

        self.context.vision_search_ms = int((time.monotonic() - vision_start) * 1000)

        if not found:
            self._abort_task(
                f"I was unable to find the {tool}. Please check the tray or use manual procedure."
            )
            return

        # --- Phase 3: Grasp ---
        motion_start = time.monotonic()
        grasped = self._phase_grasp(tool)
        self.context.motion_ms = int((time.monotonic() - motion_start) * 1000)

        if not grasped:
            self._abort_task(
                f"Unable to grasp the {tool}. Please reposition it and try again."
            )
            return

        self.world.arm_holding = True

        # --- Phase 4: Handover ---
        handover_ok = self._phase_handover(tool, user_id, user_name)
        if not handover_ok:
            self._safe_deposit(tool)
            return

        # --- Phase 5: Success ---
        self.context.total_task_ms = int((time.monotonic() - pipeline_start) * 1000)
        self._log_success()
        self.agentic.learn_from_success(self.context, user_id)

        self._speak("Handover complete. Is there anything else?")
        self._transition_state('STANDBY')
        self.world.current_task = None
        self.world.arm_holding  = False

        self.get_logger().info(
            f"=== TASK COMPLETE: '{tool}' — total {self.context.total_task_ms}ms "
            f"(vision {self.context.vision_search_ms}ms, motion {self.context.motion_ms}ms) ==="
        )

    # =====================================================================
    # PHASE: VISION SEARCH — max 3 attempts total
    # =====================================================================

    def _phase_vision_search(self, tool: str, user_id: str) -> bool:
        """
        Attempt 1: Agentic-ordered NBV search.
        Attempt 2: Uniform search (reset probability map).
        Attempt 3: Final search, user warned, last try.
        Returns True if tool found, False after 3 failures.
        """
        current_hour = datetime.now().hour

        for attempt in range(1, MAX_RETRIES + 1):
            self.context.retries.increment('vision_search')

            if attempt == 1:
                # First attempt — get agentic search strategy
                strategy = self.agentic.propose_search_strategy(
                    tool, user_id, current_hour, attempt
                )
                tts = strategy.get('tts_message', f"Searching for {tool}.")
                self._speak(tts)
                reset_map = strategy['params'].get('reset_probability_map', False)
                priority_zones = strategy['params'].get('priority_zones', [])

            else:
                # Subsequent attempts — get recovery decision
                recovery = self.agentic.propose_vision_recovery(
                    tool, attempt, self.world
                )
                if recovery is None:
                    # Shouldn't happen — fallback triggers inside propose_vision_recovery
                    break

                self._speak(recovery['tts_message'])
                action = recovery['action']
                reset_map = recovery['params'].get('reset_probability_map', False)
                priority_zones = recovery['params'].get('priority_zones', [])

                if action == 'ASK_USER_CONFIRM_LOCATION':
                    # Give user 5s to respond, then search again regardless
                    time.sleep(5.0)

                if action == 'ABORT_TOOL_NOT_FOUND':
                    # This is attempt 3 — run the search then check result
                    pass  # Fall through to search below

            # Execute the search
            found = self._execute_vision_search(tool, reset_map, priority_zones)

            if found:
                self.get_logger().info(
                    f"Vision search: found '{tool}' on attempt {attempt} "
                    f"in zone '{self.context.zone_found}'"
                )
                return True

            self.get_logger().warn(
                f"Vision search: attempt {attempt}/{MAX_RETRIES} failed for '{tool}'"
            )

        # All 3 attempts exhausted
        self.get_logger().error(f"Vision search: all {MAX_RETRIES} attempts failed for '{tool}'")
        return False

    # =====================================================================
    # PHASE: GRASP — max 3 attempts total
    # =====================================================================

    def _phase_grasp(self, tool: str) -> bool:
        """
        Move to pre-grasp, then grasp with force confirmation.
        Attempt 1: Normal grasp at 3N.
        Attempt 2: Repositioned approach angle.
        Attempt 3: Force increase (max 5N — well below 10N warning threshold).
        Returns True if grip confirmed.
        """
        base_force = 3.0

        for attempt in range(1, MAX_RETRIES + 1):
            self.context.retries.increment('grasp')

            if attempt == 1:
                force_target = base_force
                rotation_deg = 0.0
            else:
                recovery = self.agentic.propose_grasp_recovery(tool, attempt, self.world)
                if recovery is None:
                    break

                self._speak(recovery['tts_message'])
                force_target = base_force + recovery['params'].get('force_delta_n', 0.0)
                rotation_deg = recovery['params'].get('rotation_deg', 0.0)

                # Safety clamp — never exceed 10N (warning threshold)
                force_target = min(force_target, 10.0)

            # Validate force
            ok, reason = self.safety.validate_grasp(force_target, self.world)
            if not ok:
                self.get_logger().error(f"Grasp force rejected by kernel: {reason}")
                return False

            # Compute and validate pre-grasp position
            x, y, z = self.context.grasp_point
            pregrasp = (x, y, z + 0.05)
            ok, reason = self.safety.validate_move(pregrasp, self.world)
            if not ok:
                self.get_logger().error(f"Pre-grasp move rejected: {reason}")
                return False

            # Move to pre-grasp
            vel = self.safety.velocity_scale(self.world) * 0.8
            if not self._send_arm_move(pregrasp, velocity_scale=vel):
                continue

            # Move to grasp point
            ok, reason = self.safety.validate_move(self.context.grasp_point, self.world)
            if not ok:
                self.get_logger().error(f"Grasp move rejected: {reason}")
                return False

            vel = self.safety.velocity_scale(self.world) * 0.5
            if not self._send_arm_move(self.context.grasp_point, velocity_scale=vel,
                                        rotation_offset_deg=rotation_deg):
                continue

            # Apply grasp
            if not self._send_gripper_grasp(force_target):
                continue

            # Confirm force
            time.sleep(0.5)
            if self.world.gripper_force >= 1.0:
                self.get_logger().info(
                    f"Grasp confirmed on attempt {attempt}: "
                    f"force={self.world.gripper_force:.1f}N"
                )
                return True

            self.get_logger().warn(
                f"Grasp attempt {attempt}/{MAX_RETRIES}: force too low "
                f"({self.world.gripper_force:.1f}N < 1.0N)"
            )

        self.get_logger().error(f"Grasp: all {MAX_RETRIES} attempts failed")
        return False

    # =====================================================================
    # PHASE: IK SOLVE — called inside grasp, max 3 attempts
    # =====================================================================

    def _resolve_ik(self, target_pos: Tuple[float, float, float],
                    tool: str) -> Optional[List[float]]:
        """
        Attempt IK solve. On failure, try alternate orientation then next candidate.
        Returns joint angles list or None after 3 failures.
        """
        for attempt in range(1, MAX_RETRIES + 1):
            self.context.retries.increment('ik_solve')

            # TODO: call ik_solver.solve(target_pos) when hardware params available
            # joint_angles = ik_solver.solve(target_pos)
            joint_angles = None  # Placeholder

            if joint_angles is not None:
                return joint_angles

            # IK failed — get recovery decision
            recovery = self.agentic.propose_ik_recovery(
                tool, attempt, self.context, self.world
            )
            if recovery is None:
                break

            self._speak(recovery['tts_message'])
            action = recovery['action']

            if action == 'ABORT_IK_FAILED':
                break

            if action == 'RETRY_IK_ALTERNATE_ORIENTATION':
                rotation = recovery['params'].get('rotation_deg', 90.0)
                # Apply rotation offset to target — modify target_pos or grasp approach
                # TODO: implement orientation adjustment in IK call
                self.context.alternate_orientation_tried = True
                self.get_logger().info(f"IK retry: alternate orientation {rotation}°")

            elif action == 'RETRY_IK_NEXT_CANDIDATE':
                if self.context.detection_candidates:
                    next_candidate = self.context.detection_candidates.pop(0)
                    target_pos = (
                        next_candidate['x'],
                        next_candidate['y'],
                        next_candidate['z']
                    )
                    self.context.grasp_point = target_pos
                    self.get_logger().info(f"IK retry: next candidate at {target_pos}")
                else:
                    self.get_logger().error("IK: no more detection candidates")
                    break

        self.get_logger().error(f"IK: all {MAX_RETRIES} attempts failed for '{tool}'")
        return None

    # =====================================================================
    # PHASE: HANDOVER — 3-check with face retries
    # =====================================================================

    def _phase_handover(self, tool: str, user_id: str, user_name: str) -> bool:
        """
        Move to handover zone, then run 3-check verification:
          Check 1: Face verify (3 attempts with Z-height recovery, then voice+hand fallback)
          Check 2: Hand detect (open palm, palm up)
          Check 3: Voice confirm ("take" / "yes")
        Returns True if tool handed over, False if timeout or safety rejection.
        """
        self._transition_state('HOLDING')

        # Get handover pose (learned per user)
        handover_pose = self.agentic.get_handover_pose(user_id)

        ok, reason = self.safety.validate_handover(self.world)
        if not ok:
            self.get_logger().error(f"Handover rejected: {reason}")
            return False

        ok, reason = self.safety.validate_move(handover_pose, self.world)
        if not ok:
            self.get_logger().error(f"Handover move rejected: {reason}")
            return False

        vel = self.safety.velocity_scale(self.world) * 0.6
        if not self._send_arm_move(handover_pose, velocity_scale=vel):
            return False

        self._transition_state('HANDOVER')
        self._speak(f"{tool} ready. Please face the camera.")

        handover_start = time.monotonic()
        current_z = handover_pose[2]
        face_verified = False
        face_skipped  = False

        # --- Check 1: Face verification (3 attempts, then degrade gracefully) ---
        for face_attempt in range(1, MAX_RETRIES + 1):
            self.context.retries.increment('handover_face')

            face_ok = self._wait_for_face_verify(user_id, timeout=8.0)
            if face_ok:
                face_verified = True
                break

            recovery = self.agentic.propose_handover_face_recovery(
                user_name, tool, face_attempt, current_z
            )
            self._speak(recovery['tts_message'])
            action = recovery['action']

            if action == 'HANDOVER_VOICE_HAND_ONLY':
                # Attempt 3 reached — degrade to voice+hand only
                face_skipped = True
                self.get_logger().warn(
                    f"FACE_VERIFY_SKIPPED for user {user_id} — "
                    f"proceeding on voice+hand only (logged for admin review)"
                )
                break

            elif action == 'HANDOVER_Z_UP':
                z_offset = recovery['params'].get('z_offset_m', 0.05)
                new_z = current_z + z_offset
                new_pose = (handover_pose[0], handover_pose[1], new_z)
                ok, _ = self.safety.validate_move(new_pose, self.world)
                if ok:
                    self._send_arm_move(new_pose, velocity_scale=0.4)
                    current_z = new_z

            elif action == 'HANDOVER_Z_DOWN':
                z_offset = recovery['params'].get('z_offset_m', -0.05)
                new_z = current_z + z_offset  # z_offset is negative here
                new_pose = (handover_pose[0], handover_pose[1], new_z)
                ok, _ = self.safety.validate_move(new_pose, self.world)
                if ok:
                    self._send_arm_move(new_pose, velocity_scale=0.4)
                    current_z = new_z

        # --- Handover timeout check ---
        if (time.monotonic() - handover_start) > HANDOVER_TIMEOUT_S:
            self.get_logger().warn("Handover timeout — returning tool to tray")
            self._speak(f"No collection detected. Returning {tool} to tray.")
            return False

        # --- Check 2: Hand detection ---
        self._speak("Please place your open palm under the gripper.")
        hand_ok = self._wait_for_hand_detect(timeout=10.0)
        if not hand_ok:
            self._speak("Please open your palm and hold it steady.")
            hand_ok = self._wait_for_hand_detect(timeout=8.0)

        # --- Check 3: Voice confirmation ---
        self._speak("Say 'take' to receive.")
        voice_ok = self._wait_for_voice_confirm(user_id, timeout=5.0)

        # --- Final 3-check gate ---
        ok, reason = self.safety.validate_release(
            self.world, face_verified, hand_ok, voice_ok
        )
        if not ok:
            self.get_logger().error(f"Release gate failed: {reason}")
            self._speak("Handover verification failed. Returning tool to tray.")
            return False

        # Log face skip for admin review if it happened
        if face_skipped:
            self._log_event("FACE_VERIFY_SKIPPED", tool,
                            description=f"Handover to {user_id} completed without face verification")

        # --- Release ---
        if not self._send_gripper_release():
            return False

        time.sleep(0.5)
        self.world.arm_holding  = False
        self.world.gripper_force = 0.0
        return True

    # =====================================================================
    # INTERNAL: VISION SEARCH EXECUTION
    # =====================================================================

    def _execute_vision_search(self, tool: str,
                                reset_probability_map: bool,
                                priority_zones: List[str]) -> bool:
        """Publish vision search request and wait for result."""
        request_payload = {
            'tool': tool,
            'reset_probability_map': reset_probability_map,
            'priority_zones': priority_zones
        }

        if MSGS_OK:
            req = VisionSearchRequest()
            req.tool = tool
            self.vision_req_pub.publish(req)
        else:
            self.vision_req_pub.publish(
                String(data=json.dumps(request_payload))
            )

        self._vision_event.clear()
        if not self._vision_event.wait(timeout=30.0):
            self.get_logger().warn("Vision search timed out (30s)")
            return False

        result = self._vision_result
        if result.get('found') and result.get('confidence', 0.0) >= 0.7:
            self.context.grasp_point = (result['x'], result['y'], result['z'])
            self.context.zone_found  = result.get('zone', '')
            # Store additional candidates for IK fallback
            self.context.detection_candidates = result.get('candidates', [])
            return True

        return False

    # =====================================================================
    # WORLD STATE CHECK
    # =====================================================================

    def _check_world_state(self) -> bool:
        if self.world.safety_severity == 'ESTOP':
            self._speak("System is in emergency stop. Cannot proceed.")
            return False
        if self.world.vision_status == 'LOADING':
            self._speak("Vision system is still loading. Please wait.")
            return False
        if self.world.vision_status == 'ERROR':
            self._speak("Vision system error. Please contact admin.")
            return False
        if not self.world.network_ok:
            self._speak("Network unavailable. Cannot process commands.")
            return False
        return True

    # =====================================================================
    # SAFE DEPOSIT — controlled drop to SAFE_DROP_ZONE on failure/ESTOP
    # =====================================================================

    def _safe_deposit(self, tool: str = ''):
        self.get_logger().warn("Safe deposit initiated")
        self._speak("Returning tool to safe zone.")

        drop = (SAFE_DROP_ZONE['x'], SAFE_DROP_ZONE['y'], SAFE_DROP_ZONE['z'])
        ok, _ = self.safety.validate_move(drop, self.world)
        if ok:
            self._send_arm_move(drop, velocity_scale=0.3)
            self._send_gripper_release()

        self.world.arm_holding   = False
        self.world.gripper_force = 0.0
        self._transition_state('STANDBY')
        self._log_event("SAFE_DEPOSIT", tool, description="Safe deposit executed")

    # =====================================================================
    # WAIT HELPERS
    # (In production: subscribe to real topics; mocked here)
    # =====================================================================

    def _wait_for_face_verify(self, user_id: str, timeout: float) -> bool:
        """Wait for auth_node to publish face match for logged-in user."""
        # TODO: subscribe to /auth_result, check face_verified field
        time.sleep(1.0)
        return True  # Mock

    def _wait_for_hand_detect(self, timeout: float) -> bool:
        """Wait for vision_node to publish open palm in handover zone."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            h = self._latest_hand_status
            if h.get('detected') and h.get('is_open') and h.get('palm_up'):
                return True
            time.sleep(0.1)
        return False

    def _wait_for_voice_confirm(self, user_id: str, timeout: float) -> bool:
        """Wait for voice_node to confirm 'take' or 'yes' from logged-in user."""
        # TODO: subscribe to voice confirm topic from voice_node
        time.sleep(1.0)
        return True  # Mock

    # =====================================================================
    # LOW-LEVEL COMMAND SENDERS
    # =====================================================================

    def _send_arm_move(self, position: Tuple[float, float, float],
                       velocity_scale: float = 1.0,
                       rotation_offset_deg: float = 0.0) -> bool:
        """Send MOVE command. Returns True when motion confirmed."""
        # TODO: call ik_solver.solve(position, rotation_offset_deg) → joint_angles
        self.get_logger().info(
            f"ARM MOVE → {position} @ {velocity_scale*100:.0f}% velocity "
            f"(rotation offset {rotation_offset_deg}°)"
        )

        if MSGS_OK:
            cmd = ArmCommand()
            cmd.command        = 'MOVE'
            cmd.velocity_scale = velocity_scale
            # cmd.joint_angles = ik_solver.solve(position)  # fill when hw params available
            self.arm_pub.publish(cmd)
        else:
            self.arm_pub.publish(String(data=json.dumps({
                'command': 'MOVE',
                'position': position,
                'velocity_scale': velocity_scale,
                'rotation_offset_deg': rotation_offset_deg
            })))

        self._motion_event.clear()
        return self._motion_event.wait(timeout=15.0) and self._motion_success

    def _send_gripper_open(self) -> bool:
        self.get_logger().info("GRIPPER OPEN")
        if MSGS_OK:
            cmd = GripperCommand()
            cmd.command      = 'RELEASE'
            cmd.force_target = 0.0
            self.gripper_pub.publish(cmd)
        else:
            self.gripper_pub.publish(String(data=json.dumps(
                {'command': 'RELEASE', 'force_target': 0.0}
            )))
        time.sleep(0.6)  # Wait for physical open (~500ms per spec)
        return True

    def _send_gripper_grasp(self, force_target: float) -> bool:
        self.get_logger().info(f"GRIPPER GRASP @ {force_target}N")
        if MSGS_OK:
            cmd = GripperCommand()
            cmd.command      = 'GRASP'
            cmd.force_target = force_target
            self.gripper_pub.publish(cmd)
        else:
            self.gripper_pub.publish(String(data=json.dumps(
                {'command': 'GRASP', 'force_target': force_target}
            )))
        return True

    def _send_gripper_release(self) -> bool:
        self.get_logger().info("GRIPPER RELEASE")
        if MSGS_OK:
            cmd = GripperCommand()
            cmd.command      = 'RELEASE'
            cmd.force_target = 0.0
            self.gripper_pub.publish(cmd)
        else:
            self.gripper_pub.publish(String(data=json.dumps(
                {'command': 'RELEASE', 'force_target': 0.0}
            )))
        time.sleep(0.6)
        return True

    # =====================================================================
    # ESTOP HANDLER
    # =====================================================================

    def _handle_estop(self, reason: str):
        if self.world.arm_holding:
            self._safe_deposit()
        self.world.current_task  = None
        self.world.arm_holding   = False
        self._transition_state('ESTOP')

    # =====================================================================
    # HELPERS
    # =====================================================================

    def _speak(self, text: str):
        self.tts_pub.publish(String(data=text))

    def _transition_state(self, target: str):
        self.world.robot_state = target
        if MSGS_OK:
            msg = StateTransition()
            msg.target_state = target
            self.state_pub.publish(msg)

    def _abort_task(self, message: str):
        self.get_logger().error(f"Task aborted: {message}")
        self._speak(message)
        self._log_event("TASK_ABORTED", self.context.tool_canonical,
                        description=message)
        self.world.current_task = None
        self._send_arm_move(  # Return to neutral
            (0.0, 0.0, WORKSPACE['zmax'] * 0.5),
            velocity_scale=0.5
        )
        self._transition_state('STANDBY')

    def _log_success(self):
        self.get_logger().info(
            f"TASK SUCCESS | tool={self.context.tool_canonical} | "
            f"zone={self.context.zone_found} | "
            f"vision={self.context.vision_search_ms}ms | "
            f"motion={self.context.motion_ms}ms | "
            f"total={self.context.total_task_ms}ms | "
            f"retries=vision:{self.context.retries.vision_search} "
            f"grasp:{self.context.retries.grasp} "
            f"ik:{self.context.retries.ik_solve} "
            f"face:{self.context.retries.handover_face}"
        )
        self._log_event("FETCH_SUCCESS", self.context.tool_canonical)

    def _log_event(self, event_type: str, tool: str, description: str = ''):
        if MSGS_OK:
            msg = LogEvent()
            msg.event_type       = event_type
            msg.user_id          = self.world.active_user_id
            msg.tool             = tool
            msg.state            = self.world.robot_state
            msg.description      = description
            msg.timestamp        = int(time.time() * 1000)
            msg.vision_search_ms = self.context.vision_search_ms
            msg.motion_ms        = self.context.motion_ms
            msg.total_task_ms    = self.context.total_task_ms
            self.log_pub.publish(msg)
        else:
            self.get_logger().info(
                f"LOG | {event_type} | tool={tool} | {description}"
            )

# =============================================================================
# ENTRY POINT
# =============================================================================

def main(args=None):
    rclpy.init(args=args)
    node = PlannerNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```


## SECTION XIII — EMERGENCY STOP SYSTEM
 
> **SOFTWARE** — Voice keyword thread and network failure monitoring are Software. Sensor threshold monitoring is Software reading MCU telemetry. Physical ESTOP button is Hardware. PWM disable is Embedded.
 
### Trigger 1 — Voice Keyword
 
- Separate always-on thread with independent audio buffer — never muted by TTS state
- Keywords: stop, halt, emergency, abort, ruko, bas
- Acts on partial transcript — no utterance end wait
- 100ms collision window to distinguish 'stop, actually bring scalpel' from genuine ESTOP
- No auth check — overrides all
- Target latency: <200ms from word to ESTOP published
- The system verifies that the detected emergency keyword is not part of a longer sentence before activating the emergency stop procedure, reducing false triggers during normal conversation.
### ESTOP Keyword + Normal Command Collision — Decision Tree
 
```
ESTOP keyword detected in partial transcript ↓
  100ms hold window — check if more speech follows
  More speech detected → not ESTOP → pass full utterance to STT pipeline normally
  No more speech → confirm ESTOP, trigger immediately
```
 
### Trigger 2 — Sensor Thresholds
 
| Sensor | Severity | Threshold | Source |
|---|---|---|---|
| Joint current | WARNING | > 6A | MCU current sensing |
| Joint current | ESTOP | > 8A for >100ms | MCU current sensing |
| Joint temperature | WARNING | > 55°C | MCU thermal sensors |
| Joint temperature | CRITICAL | 65°C–74°C | MCU thermal sensors |
| Joint temperature | ESTOP | > 75°C | MCU thermal sensors |
| Joint velocity | ESTOP | > 120 deg/s | MCU encoder derivative |
| LiDAR proximity | WARNING | 400–600mm | safety_node |
| LiDAR proximity | ESTOP | < 400mm | safety_node |
| Gripper force | WARNING | > 10N spike | MCU force sensor |
| Gripper force | ESTOP | > 15N spike | MCU force sensor |
 
### Trigger 3 — Network Failure Mid-Task
 
- Network failure while state is EXECUTING or HOLDING
- Timer starts — if holding object past 5-second threshold → safe deposit → ESTOP
- Else → immediate ESTOP. TTS: 'Network unavailable. Stopping safely.'
### ESTOP Behaviour — Deterministic Safe Deposit
 
**SOFT ESTOP (voice, sensor, network):**
 
```
• Planner transitions to SAFE_DEPOSIT state (internal, not published externally)
• If holding object: controlled move to SAFE_DROP_ZONE at reduced velocity → RELEASE
  → gripper force confirms release
• THEN send ESTOP command to MCU → PWM disabled
• TTS: 'Emergency stop. {reason}.' Log event. State → ESTOP
```
 
**HARD ESTOP (physical button):**
 
```
• Motor driver enable pin cut directly — immediate PWM off. No movement possible after.
• If holding object at button press — object remains in gripper. Staff must manually retrieve.
• Pi detects MCU entered ESTOP via status feedback.
• TTS: 'Emergency stop. Manual reset required.' Log event. State → ESTOP
```
 
Hard ESTOP takes priority over everything. Soft ESTOP allows controlled deposit. Never mix the two paths.
 
### TTS Hard Interrupt on ESTOP
 
```python
# ESTOP received:
tts.stop_current()    # hard cut — pyttsx3, instant
tts_queue.clear()
pyttsx3_speak('Emergency stop. {reason}.')  # always pyttsx3 for ESTOP, never cloud TTS
```
 
### Resume Protocol
 
```
Staff: 'Resume'
ACARE: 'Emergency stop was triggered due to {reason}. Confirm it is safe to resume.'
Staff: 'Confirm resume' → Runtime voice consistency check passes → State → STANDBY
No active session → admin required to resume.
```
 
---
 
## SECTION XIV — LIDAR SAFETY SYSTEM
 
> **SOFTWARE** — LiDAR proximity monitoring is Software (safety_node). Physical LiDAR sensor mounting is Hardware.
 
YDLIDAR T-mini Plus is base-mounted at approximately 80cm height — scans horizontal plane at human torso level. Used exclusively for operator proximity detection. SLAM and navigation removed from scope.
 
### Proximity Zones
 
| Zone | Distance | Response |
|---|---|---|
| Safe | > 600mm | Full velocity — velocity_scale = 1.0 |
| Caution | 400–600mm | 50% velocity — velocity_scale = 0.5, SafetyAlert severity=WARNING |
| Danger | < 400mm | Publish SafetyAlert severity=ESTOP immediately |
 
### LiDAR Role at Handover
 
```
LiDAR detects "a torso is within 600mm in front arc" → triggers camera to begin face search.
LiDAR does NOT identify who the person is.
LiDAR does NOT detect hand or face.
During arm motion to handover zone: LiDAR proximity < 400mm → ESTOP immediately.
During actual handover (arm stationary): proximity monitoring continues.
  Person suddenly < 400mm during gripper release → ESTOP, tool held.
```
 
### Known Limitation
 
LiDAR detects upper-body proximity only. A hand entering from below the 80cm scan plane is not detected. Staff must follow workspace clearance protocol before robot executes.
 
---
 
## SECTION XV — RESPONSE GENERATOR — TTS
 
> **SOFTWARE** — TTS engine selection and response generation are Software. Audio hardware (speaker) is Hardware.
 
### TTS Engine Architecture — Final
 
| Message Type | Engine | Reason |
|---|---|---|
| ESTOP / Safety critical | pyttsx3 | Zero latency, offline, instant — cannot use API for safety messages |
| Normal responses (fetch, search, handover) | Microsoft Edge TTS (via edge-tts package) | Most natural voice, 1M free chars/month |
| Offline fallback | Kokoro ONNX INT8 | Local, natural, Pi-compatible, Apache 2.0 — used if no internet |
 
### Complete Response Template Library
 
| Trigger | Response | Engine |
|---|---|---|
| Command received | Fetching {tool} for {name}. One moment. | Microsoft Edge TTS |
| NBV search started | Searching for {tool}. | Microsoft Edge TTS |
| Multi-tool detected | One at a time. Which first — {A} or {B}? | Microsoft Edge TTS |
| Tool not found (1st) | Cannot locate {tool}. Can you confirm it is on the tray? | Microsoft Edge TTS |
| Tool not found (2nd) | Still unable to locate {tool}. Please check tray or use manual procedure. | Microsoft Edge TTS |
| Voice not recognised | Voice not recognised. Command rejected. | Microsoft Edge TTS |
| Fake object detected | Object appears to be a reproduction. Command rejected. | Microsoft Edge TTS |
| Ambiguous intent | Did you mean {A} or {B}? | Microsoft Edge TTS |
| Grasp failed | Grasp failed. Please reposition the {tool}. | Microsoft Edge TTS |
| IK failed | Unable to reach the {tool}. Please reposition it. | Microsoft Edge TTS |
| Handover ready | {tool} ready. Please face the camera. | Microsoft Edge TTS |
| Hand not detected | Please place your open palm under the gripper. | Microsoft Edge TTS |
| Voice confirm prompt | Say take to receive. | Microsoft Edge TTS |
| Handover complete | Handover complete. Is there anything else? | Microsoft Edge TTS |
| Handover timeout | No collection detected. Returning {tool} to tray. | Microsoft Edge TTS |
| ESTOP triggered | Emergency stop. {reason}. | pyttsx3 |
| Safe deposit in progress | Completing safe deposit. | pyttsx3 |
| Resume confirmation | Emergency stop due to {reason}. Confirm it is safe to resume. | pyttsx3 |
| Network failure | Voice service unavailable. | pyttsx3 or Kokoro |
| Camera failure | Camera error. Please retry. | Microsoft Edge TTS |
| Logout rejected | Cannot log out during active task. | Microsoft Edge TTS |
| Unauthorised voice | Command not processed. Only {name} can issue commands. | Microsoft Edge TTS |
| Session timeout | Session timeout. Logging out {name}. | Microsoft Edge TTS |
| Voice drift warning | Having trouble recognising your voice. Please reconfirm identity. | Microsoft Edge TTS |
| System init | A-Care system initialising. Please wait. | pyttsx3 |
| System ready | A-Care system ready. | Microsoft Edge TTS |
| Shutdown | Shutting down. Goodbye. | Microsoft Edge TTS |
| Safety warning | Caution — operating at reduced speed. | pyttsx3 |
| Critical thermal | Warning — thermal limit approaching. | pyttsx3 |
| Auth required | Authentication required before I can fetch tools. | Microsoft Edge TTS |
 
---
 
## SECTION XVI — LOGGING & AUDIT TRAIL
 
> **SOFTWARE** — SQLite logging is Software. Audit trail persists on Pi SD card.
 
### Event Schema — With Full Latency Fields
 
```json
{
  "event_id":        "UUID",
  "timestamp":       "ISO8601",
  "staff_id":        "unique_id",
  "staff_name":      "str",
  "event_type":      "COMMAND | FETCH | HANDOVER | ESTOP | LOGIN | LOGOUT | FAKE_REJECTED |
                      GRASP_FAIL | IK_FAIL | NETWORK_FAIL | DEPTH_FAILURE | HANDOVER_TIMEOUT |
                      VOICE_DRIFT_DETECTED | UNAUTHORISED_VOICE_ATTEMPT | POWER_RECOVERY |
                      SHUTDOWN | SAFETY_WARNING | SAFETY_CRITICAL | FACE_VERIFY_SKIPPED |
                      LIDAR_ESTOP | HARD_ESTOP | TASK_ABORTED | LOW_LIGHT_MODE",
  "tool":            "str",
  "zone_found":      "str",
  "grasp_attempts":  "int",
  "success":         "bool",
  "failure_reason":  "str",
  "sensor_values":   "dict",
  "safety_severity": "str",
  "voice_e2e_ms":    "int",
  "vision_search_ms":"int",
  "motion_ms":       "int",
  "total_task_ms":   "int"
}
```
 
### Storage Policy
 
- Maximum DB size: 200MB
- On exceeding limit: archive oldest logs to CSV, compress, rotate automatically
- No manual intervention required — self-managed
- Clinical traceability: if a tool goes missing, logs show last fetch — who, when, which zone
---
 
## SECTION XVII — STARTUP, SHUTDOWN & POWER RECOVERY
 
### Startup Sequence
 
```
1.  ROS2 core starts
2.  system.yaml loaded → workspace bounds, API config, timeouts
3.  thresholds.yaml loaded → safety limits, fake detection thresholds
4.  probability_map.yaml loaded → NBV priors
5.  users.db loaded → encrypted biometric embeddings
6.  YOLOv11 ONNX model loaded → /vision_status: LOADING → READY
7.  SpeechBrain speaker verification model loaded
8.  Silero VAD loaded
9.  MobileNet face embedding model loaded
10. LiDAR safety monitor starts (separate thread)
11. Emergency keyword monitor starts (separate audio buffer thread, never muted)
12. Passive face detection starts (lightweight, always-on)
13. Embedded communication initialised (CAN/UART)
14. Pi waits for Teensy CALIBRATION_COMPLETE (timeout 60s)
15. Heartbeat loop starts (200ms interval)
16. Check last SQLite state for power recovery
17. Node crash recovery supervisor starts
18. State → LOGGED_OUT
19. Arm moves to standby pose: pointing downward
20. TTS (pyttsx3): 'A-Care system ready.'
```
 
### Shutdown Sequence (Admin Command Only)
 
- State must be STANDBY or LOGGED_OUT
- If EXECUTING → complete safe deposit first
- Serialise probability_map → probability_map.yaml.tmp → verify write → atomic rename to .yaml
- Log SHUTDOWN event
- Flush all SQLite logs to disk
- Stop heartbeat → MCU enters safe idle (IDLE state, holds position)
- ROS2 nodes shutdown gracefully
- TTS: 'Shutting down. Goodbye.'
### Power Failure Recovery
 
```
On reboot, check for probability_map.yaml.tmp:
  If .tmp exists → previous write was incomplete
    → Delete .tmp, load probability_map.yaml (last clean version)
  If neither exists → use uniform distribution
 
Read last event_type from SQLite:
  If last state was EXECUTING or HOLDING:
    Move arm slowly to neutral position (reduced velocity)
    Log: POWER_RECOVERY
    TTS: 'System recovered from unexpected shutdown. Please verify workspace.'
  Else: normal startup, no special action
```
 
---
 
## SECTION XVIII — ADMIN CLI & CALIBRATION
 
> **SOFTWARE** — Admin CLI is Software. Physical calibration target placement is Hardware task.
 
### Admin Commands
 
```bash
# Staff management
python admin.py enrol --name "Dr. Sharma" --role surgeon
python admin.py revoke --id staff_001
python admin.py list-staff
 
# API keys
python admin.py set-api-key --service deepgram --key $KEY
python admin.py set-api-key --service groq --key $KEY
python admin.py set-api-key --service edge-tts --key $KEY
 
# Safety thresholds
python admin.py set-threshold --sensor joint_current --value 8.0
 
# Logs
python admin.py show-logs --last 50
python admin.py show-logs --staff staff_001 --date 2026-03-15
python admin.py export-logs --format csv
 
# System
python admin.py status
python admin.py run-diagnostics
python admin.py calibrate
python admin.py demo-mode --enable
python admin.py demo-mode --disable
```
 
### Calibration Procedure
 
```
python admin.py calibrate
 
Step 1: Joint homing
  Teensy moves each joint to limit switch, zeros encoders.
 
Step 2: Camera calibration
  Intrinsics + extrinsics computed, stored to config.
 
Step 3: Workspace boundary confirmation
  Admin confirms bounds in system.yaml.
 
Step 4: SAFE_DROP_ZONE definition
  Admin positions arm, coordinates captured.
 
Step 5: NBV viewpoints definition
  Admin moves arm to each viewpoint, confirms.
 
Step 6: Fake detection threshold calibration
  20 real + 20 printed samples → thresholds.yaml
 
Step 7: LiDAR baseline scan
  Empty workspace → reference stored.
 
TTS: "Calibration complete. System ready."
```
 
---
 
## SECTION XIX — CONFIGURATION FILES
 
> **SOFTWARE** — All configuration files are Software. No hardcoded parameters in any node.
 
### system.yaml
 
```yaml
robot:
  workspace:
    xmin: -0.4  xmax: 0.4
    ymin: -0.3  ymax: 0.3
    zmin:  0.0  zmax: 0.5
  safe_drop_zone: {x: 0.0, y: 0.35, z: 0.05}
  handover_zone: {x: 0.0, y: 0.4, z: 0.1}
  handover_height_adjustment_m: 0.05  # per 'lower'/'higher' command
 
arm:
  link_lengths:  # fill after assembly
    base_height: [PLACEHOLDER]
    upper_arm:   [PLACEHOLDER]
    forearm:     [PLACEHOLDER]
    wrist:       [PLACEHOLDER]
    gripper:     [PLACEHOLDER]
  neutral_joint_angles: [PLACEHOLDER, PLACEHOLDER, PLACEHOLDER,
                         PLACEHOLDER, PLACEHOLDER, PLACEHOLDER]
 
vision:
  model_path: '/models/yolo_int8.onnx'
  confidence_threshold: 0.7
  low_light_confidence_threshold: 0.60
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
  agentic_model: "openai/gpt-oss-120b"
  intent_model: "llama-3.1-8b-instant"
  assistant_model: "llama-3.1-8b-instant"
```
 
### thresholds.yaml
 
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
 
### probability_map.yaml (example admin-defined prior)
 
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
 
---
 
## SECTION XX — DIRECTORY STRUCTURE
 
```
acare_ws/
  src/
    acare_msgs/                        ← Custom ROS2 message definitions
      msg/
        RobotState.msg
        Intent.msg
        ValidatedIntent.msg
        SafetyAlert.msg
        HandStatus.msg                 ← Hand tracking for handover
        AuthResult.msg
        VisionResult.msg
        ArmCommand.msg
        MotionFeedback.msg
        LogEvent.msg
        EmergencySignal.msg
      CMakeLists.txt
 
    acare_voice/                       ← Audio orchestration (SW) — v2.1 unified package
      voice_node.py                   ← Master orchestrator with unified state machine
      main.py                         ← Entry point
      pyproject.toml
      requirements.txt
      __init__.py
      vad.py                          ← Silero VAD, 32ms chunks
      asr.py                          ← Deepgram Nova-2 streaming STT
      tts.py                          ← Dual TTS (Edge TTS + pyttsx3)
      keyword_monitor.py              ← Always-on emergency keyword thread
      normaliser.py                   ← Lowercase, filler strip, alias expansion
      intent_parser.py                ← Groq llama-3.1-8b-instant JSON mode
      alias_expansion.py              ← Contextual alias resolution
      assistant_agent.py              ← Groq conversational agent (LOGGED_OUT state)
      state_manager.py                ← Voice-internal audio state machine
      fast_intent.py                  ← Fast path intent bypass for common commands
      dialogue_manager.py             ← LangGraph routing + clarification dispatch
      tts_queue.py                    ← Priority TTS queue with hard-cut
      tts_cache.py                    ← LRU cache for frequent TTS phrases
      earcons.py                      ← Non-verbal audio feedback sounds
      semantic_turn_detector.py       ← Pause-based turn boundary detection
      conversation_eval.py            ← Per-session conversation quality logging

    acare_dialogue/                    ← Conversational AI ROS2 node (SW) [TO BUILD]
      dialogue_node.py                ← ROS2 node wrapping dialogue_manager + assistant_agent
      nodes/                          ← LangGraph sub-nodes (clarity, clarification, etc.)
        clarity_check.py
        clarification.py
        context_resolver.py
        interruption_handler.py
 
    acare_auth/                        ← Biometric auth (SW)
      auth_node.py
      enrol.py
      verify_voice.py
      verify_face.py
      face_detect.py
      embeddings/                      ← Encrypted enrolled profiles (users.db)
 
    acare_vision/                      ← Perception (SW)
      vision_node.py
      nbv_search.py
      fake_detector.py
      localiser.py
      hand_tracker.py                  ← MediaPipe Hands for handover
      yolo_infer.py                    ← ONNX inference wrapper
 
    acare_planner/                     ← Task orchestration (SW)
      planner_node.py
      state_machine.py
      state_manager.py
      tool_registry.py
      handover.py                      ← 3-check: face + hand + voice → release
      ik_solver.py                     ← DLS (Levenberg-Marquardt) IK
 
    acare_safety/                      ← Safety monitoring (SW)
      safety_node.py
      lidar_monitor.py
      sensor_monitor.py
 
    acare_embedded_interface/          ← Integration boundary (INT)
      interface_node.cpp
 
    acare_logging/                     ← Audit trail (SW)
      log_node.py
 
    acare_admin/                       ← Admin CLI (SW)
      admin_cli.py
 
    acare_bringup/                     ← Launch + config (SW)
      launch/
        acare.launch.py
      config/
        system.yaml
        thresholds.yaml
        probability_map.yaml
        users.db
        supervisor.py                  ← Node crash recovery
 
  install/                             ← ROS2 build output
```
 
---
 
## SECTION XXI — COMPLETE TECHNOLOGY STACK
 
| Component | Technology | Domain |
|---|---|---|
| Object detection | YOLOv11 ONNX (Pi-optimised export) | SW |
| Model training | Ultralytics Hub (medium variant) | SW |
| Dataset annotation | Roboflow | SW |
| RGBD camera | YDLIDAR HP60C (wrist-mounted) | HW + SW |
| Safety LiDAR | YDLIDAR T-mini Plus (base-mounted) | HW + SW |
| Fake detection | OpenCV Laplacian + RGBD depth variance (dual signal) | SW |
| Low-light preprocessing | CLAHE on LAB L-channel before YOLOv11 inference | SW |
| 3D localisation | Depth pixel → 3D (no Open3D — direct depth read) | SW |
| Hand tracking | MediaPipe Hands (handover verification only) | SW |
| VAD | Silero VAD — lightweight, local, 32ms chunks | SW |
| STT | Deepgram Nova-2 streaming WebSocket (en-IN) | SW |
| Intent parsing | Groq API — llama-3.1-8b-instant, JSON mode, temp 0.0 | SW |
| Speaker auth | SpeechBrain d-vector embeddings | SW |
| Face detection (passive) | MediaPipe FaceDetection (lightweight, always-on) | SW |
| Face verification | MobileNet-based face embedding | SW |
| Conversational AI (assistant) | Groq llama-3.1-8b-instant | SW |
| Conversational AI (dialogue/clarification) | Groq openai/gpt-oss-120b + LangGraph | SW |
| Planner agentic layer | Groq openai/gpt-oss-120b, strict JSON schema, reasoning: high | SW |
| TTS — normal responses | Microsoft Edge TTS (via edge-tts package) | SW |
| TTS — ESTOP / safety | pyttsx3 — local, offline, instant, zero latency | SW |
| TTS — offline fallback | Kokoro ONNX INT8 — local, natural, Pi-compatible | SW |
| Text normalisation | normaliser.py — custom, simple rules only | SW |
| Safety monitoring | YDLIDAR T-mini Plus + MCU telemetry at 50Hz | HW + SW |
| Safety alert severity | WARNING / CRITICAL / ESTOP graded in SafetyAlert.msg | SW |
| ROS2 framework | ROS2 + MultiThreadedExecutor + QoS per topic | SW |
| Language (AI nodes) | Python 3 | SW |
| Language (embedded bridge) | C++ | INT |
| Audit logging | SQLite with full latency fields + auto-rotation | SW |
| Node recovery | supervisor.py — auto-restart non-critical nodes | SW |
| MCU | Teensy 4.1 (Cortex-M7) / custom Cortex-M4 + ESP32 PCB | EMB |
| Motor control | Cascaded PID, position and velocity loops at 200Hz | EMB |
| Motor drivers | [RMCS-3002l] | HW + EMB |
| Communication | CAN bus (preferred) / UART ≥1Mbps | INT |
| Compute platform | Raspberry Pi 5 8GB + active cooling (fan required) | HW |
| Motors | 1.4Nm Rhino Planetary BLDC ×3 + wrist/gripper | HW |
| Encoders | AS5600 magnetic encoders ×6 + TCA9548A I2C mux | HW + EMB |
 
### Groq Rate Limits (Free Tier) — Relevant Models
 
| Model | RPM | RPD | TPM |
|---|---|---|---|
| llama-3.1-8b-instant | 30 | 14,400 | 6,000 |
| openai/gpt-oss-120b | 30 | 1,000 | 8,000 |
 
**gpt-oss-120b RPD of 1,000** is the binding constraint. At ~5 LLM calls per task, that is 200 tasks per day before hitting the daily limit. Sufficient for clinical demo and development.
 
---
 
## SECTION XXII — PERFORMANCE KPIs
 
| KPI | Target | Measurement Method | Notes |
|---|---|---|---|
| Vision mAP | >= 95% | Test set evaluation | Achieved ~95% (scissors 95.1%, forceps 94.8%, oximeter 95%) |
| Vision false positive rate | < 3% | Validation set | In validation |
| Fake object rejection rate | >= 95% | 20 real + 20 printed calibration samples | Texture + depth dual signal |
| Voice intent accuracy | >= 97% | Manual eval on 50 commands | Deepgram Nova-2 + Groq JSON mode |
| Voice E2E latency | < 950ms | voice_e2e_ms in log_node | VAD trigger → validated_intent published |
| ESTOP voice latency | < 200ms | Keyword thread timing | Partial transcript, no auth, threading.Timer |
| Auth verification latency | < 150ms | auth_node timing | Lightweight d-vector per command |
| Grasp success rate | >= 90% | grasp_attempts in logs | Hardware + IK recovery dependent |
| Vision search time | < 25s worst case | vision_search_ms in log_node | Probability map reduces average significantly |
| Total task latency | < 35s typical | total_task_ms in log_node | Voice + vision + motion + handover end-to-end |
| Handover mis-delivery | = 0 | Log audit | Hard requirement — triple biometric enforced |
| TTS naturalness (normal) | Natural voice | Microsoft Edge TTS | Indian English voice |
| TTS latency (ESTOP) | < 50ms | pyttsx3 local timing | Zero API call |
| Agentic recovery success rate | > 80% | log_node task success rate | Task completed despite first failure |
 
---
 
## SECTION XXIII — PRELIMINARY WORK STATUS — MARCH 2026
 
| Item | Status | Notes |
|---|---|---|
| YOLOv11 custom model | Complete | Trained on Ultralytics Hub, 95%+ mAP, ONNX export ready |
| Gazebo simulation | Complete | Robot modelled and validated in virtual hospital environment |
| vad.py | Complete | Silero VAD, 32ms chunks, 512 sample minimum, silence timeout |
| asr.py | Complete | Deepgram Nova-2, streaming chunk-by-chunk, background async loop |
| keyword_monitor.py | Complete | Always-on, 100ms collision window, estop_active flag, word-boundary match |
| intent_parser.py | Complete | Groq llama-3.1-8b-instant, JSON mode, temp 0.0, VALID_TOOLS validation |
| tts.py | Complete | Dual approach (Edge TTS + pyttsx3) implemented |
| assistant_agent.py | Complete | Groq conversational agent, bounded to intro + auth guidance, 20-turn cap |
| main.py (basic wiring) | Complete | VAD + ASR + keyword monitor + intent + TTS end-to-end tested |
| Hardware: base + shoulder | Complete | Assembled and verified |
| Cycloidal gearboxes | Complete | 20:1 and 15:1, validated |
| Elbow / wrist / gripper | In Progress | 1–2 weeks remaining |
| normaliser.py | Complete | Both versions implemented |
| users.db + enrol.py (voice side) | To Build | SpeechBrain d-vector enrolment |
| verify_voice.py | To Build | SpeechBrain d-vector matching |
| dialogue_node (LangGraph) | To Build | Intent clarity, clarification, context resolution, interruption |
| state_manager | Complete | Full state machine with transitions |
| tool_registry.py | Complete | 6-tool mapping done |
| planner_node | To Build | Full agentic version: gpt-oss-120b + SafetyKernel + NodeCoordination |
| ik_solver.py | In Progress | Template built, awaiting hardware params |
| handover.py | Complete | 3-check protocol implemented |
| safety_node | Complete | LiDAR + telemetry monitoring |
| log_node | Complete | SQLite, full latency fields |
| admin_cli.py | Complete | Full CLI with calibration steps |
| face_detect.py | Pending camera | Passive MediaPipe detection |
| verify_face.py | Pending camera | MobileNet face embedding match |
| enrol.py (face side) | Pending camera | Face enrolment |
| fake_detector.py | Complete | Texture + depth dual signal |
| hand_tracker.py | Complete | MediaPipe Hands integration |
| nbv_search.py | Complete | Bayesian probability map |
| localiser.py | Complete | Depth pixel → 3D (placeholder params) |
| Hardware parameters (joint limits, link lengths, DH) | PENDING — URGENT | Required before IK solver can be built — get from hardware team at Google Meet |
| ROS2 wrapping (Shreevanth) | Pending | All nodes wrapped, acare_msgs, QoS, supervisor.py, launch |
| Full software integration | Pending | After hardware + ROS2 completion |
| Calibration and KPI validation | Pending | After integration |
| voice_node.py | Complete | Master voice pipeline orchestration |
| alias_expansion.py | Complete | Contextual alias resolution |
| yolo_infer.py | Complete | ONNX inference wrapper |
 
---
 
## SECTION XXIV — SUPPLEMENTARY IMPLEMENTATION DETAILS
 
### A1. Pi Heartbeat — C++ Implementation
 
```cpp
// embedded_interface_node (C++) sends every 200ms:
{ "command":"HEARTBEAT", "timestamp": unix_ms, "robot_state": current_state_string }
 
// MCU side:
if(millis() - last_heartbeat_ms > 500){ disable_all_pwm(); enter_estop(); }
```
 
### A2. Mic Mute During TTS
 
```python
async def speak(text, priority=NORMAL):
    if priority == URGENT:
        tts_queue.clear()
        tts.stop_current()
        mute_microphone()
    await tts.play(text)
    await asyncio.sleep(0.3)  # prevents TTS tail from triggering VAD
    unmute_microphone()
    audio_state → LISTENING
```
 
### A3. ESTOP Collision Decision Tree
 
```
ESTOP keyword detected in partial transcript ↓
  100ms hold window — check if more speech follows
  More speech → not ESTOP → pass full utterance to STT pipeline normally
  No more speech → confirm ESTOP, trigger immediately
```
 
### A4. TTS Hard Interrupt on ESTOP
 
```python
# ESTOP received:
tts.stop_current()   # hard cut
tts_queue.clear()
pyttsx3_speak('Emergency stop. {reason}.')  # always pyttsx3 for ESTOP
```
 
### A5. Deepgram Partial vs Final
 
```python
on_message(result):
    if not result.is_final:
        keyword_monitor.check_partial(sentence)
        return
    if result.is_final and result.speech_final:
        if keyword_monitor.estop_active:
            return
        pass_to_normaliser(result.transcript)
```
 
### A6. NBV Timing Per-Step
 
```
Arm move + settle: ~1.0s
3 frame captures: ~0.3s
YOLOv11 ONNX INT8 inference ×3: ~0.6–1.5s on Pi 5
Merge + localise: ~0.1s
Total per viewpoint: ~2–3 seconds
Worst case (6–8 viewpoints): ~15–25 seconds
 
If too slow: evaluate reduced resolution, model distillation, or ONNX runtime
```
 
### A7. NBV Cold Start Strategy
 
```
First boot or probability_map.yaml absent → uniform distribution.
Admin defines layout profile before exhibition in probability_map.yaml.
Without admin prior, first run is slower — all zones checked.
After first successful find, Bayesian updates improve immediately.
```
 
### A8. IK Failure Recovery
 
```
Grasp point computed → IK solver runs
  Solution found → proceed
  Fail → Try alternate grasp orientation (rotate 90°)
    Solution found → proceed
    Still fails → Try next detection candidate
      No candidates → TTS: 'Unable to reach the {tool}. Please reposition it.'
      State → STANDBY
```
 
### A9. Vision Node Startup Sequence
 
```
vision_node starts → publishes /vision_status: LOADING
YOLOv11 ONNX model loads (~several seconds on Pi)
Once loaded → publishes /vision_status: READY
planner_node checks /vision_status before accepting commands
TTS: 'System initialising. Please wait.' if command arrives during LOADING
```
 
### A10. Workspace Boundary Enforcement
 
```
All detections outside workspace discarded before IK attempted.
workspace: { xmin:-0.4, xmax:0.4, ymin:-0.3, ymax:0.3, zmin:0.0, zmax:0.5 }
```
 
### A11. normaliser.py — Full Description
 
```
Step 1 — Lowercase: 'Bring the SCALPEL' → 'bring the scalpel'
Step 2 — Strip fillers: 'um, can you please bring' → 'bring'
Step 3 — Punctuation strip: 'scissors,' → 'scissors'
Step 4 — Simple alias: 'bandage cloth' → 'bandage' (unambiguous only)
Step 5 — Multi-tool detect: 'scissors and scalpel' → flag for clarification
Contextual aliases ('the sharp one') pass to Groq intact — not resolved here
```
 
### A12. Inference Speed — Honest Bottleneck Note
 
YOLOv11 ONNX INT8 inference time on Pi 5 is estimated at 0.6–1.5s per frame set. If actual inference time in testing exceeds this, alternative backends must be evaluated. Options if too slow: reduced input resolution, model distillation to smaller variant, ONNX runtime instead of TFLite.
 
### A13. Edge TTS — Setup Note
 
- Free tier: 1 million characters per month — sufficient for ACARE
- API key required: `python admin.py set-api-key --service edge-tts --key $KEY`
- Voice: en-IN-Wavenet-D (Indian English male) or en-IN-Wavenet-A (female) — choose at calibration
- Offline fallback: if Edge TTS unavailable → Kokoro ONNX INT8 activates automatically
- ESTOP responses always bypass Edge TTS — pyttsx3 used directly, zero latency
### A14. Hardware Parameters Needed — Urgent
 
The following parameters are required from the hardware team before planner_node and ik_solver.py can be built. Placeholders exist in this spec — fill in after Google Meet / assembly completion.
 
- Joint limits (min/max angles) for all 6 joints
- Link lengths (base height, upper arm, forearm, wrist, gripper)
- DH parameters for all 6 joints
- Gearbox ratios for joints 4, 5, 6
- Neutral joint angles (home position)
- Confirm CAN or UART and joint numbering order
- 5 test positions for IK validation
- Gripper finger material, maximum jaw opening, tool retention method
- Motor driver model and communication protocol to Teensy
- Base fixation method
---
 
## SECTION XXV — COMMERCIAL APPLICATIONS & FUTURE WORK
 
### Short-Term Applications
 
- Robotic assistant for surgical instrument retrieval in operation theatres.
- Assistance for sterile instrument handling in clinical environments.
- Demonstration platform for human–robot interaction research in healthcare robotics.
### Long-Term Applications
 
- Completely contactless autonomous robotic assistants in hospitals and clinics for instrument and supply handling.
- Integration with hospital automation systems and smart operating rooms.
- Advanced human–robot collaboration platforms for healthcare environments.
- Multi-robot clinical assistance fleets.
### Intellectual Property Position
 
The ACARE architecture — specifically the integration of multimodal biometric authentication, streaming voice intent parsing, adaptive probabilistic vision search, and dynamic handover with real-time palm tracking — constitutes a novel technical solution not disclosed in prior art (MOXI, TIAGo, TUG, LIO). Patent filing recommended for:
 
- Dynamic handover protocol with continuous palm tracking
- Probabilistic NBV search with Bayesian map updates
- Layered safety architecture with software/firmware dual enforcement
---
 
## SECTION XXVI — COMPLETE SYSTEM FLOW & FINAL DECISIONS (FULL OPERATIONAL REFERENCE)
 
> This section is the authoritative operational reference. Every final decision is recorded here. No ambiguity. No "consider this." What is decided, is decided. Cross-references to earlier sections are provided.
 
---
 
### XXVI-A — Full Boot Sequence: OFFLINE → LOGGED_OUT
 
```
1.  ROS2 core starts.
2.  system.yaml loaded.
3.  thresholds.yaml loaded.
4.  probability_map.yaml loaded (or uniform if absent).
5.  users.db loaded (encrypted biometric profiles).
6.  YOLOv11 ONNX model loads → /vision_status: LOADING → READY.
7.  SpeechBrain speaker verification model loaded.
8.  Silero VAD loaded.
9.  MobileNet face embedding model loaded.
10. LiDAR safety monitor starts (separate thread).
11. Emergency keyword monitor starts (separate audio buffer thread, never muted).
12. Passive face detection starts (MediaPipe FaceDetection, lightweight, always-on).
13. Embedded comm initialised (UART).
14. Pi waits for Teensy CALIBRATION_COMPLETE (timeout 60s).
15. Heartbeat loop starts (200ms interval).
16. Check last SQLite state for power recovery.
17. Node crash recovery supervisor starts.
18. State → LOGGED_OUT.
19. Arm moves to standby pose: pointing downward, physically switched on.
20. TTS (pyttsx3): "A-Care system ready."
```
 
---
 
### XXVI-B — State: LOGGED_OUT Standby Behaviour
 
```
- Arm holds standby pose (downward).
- Passive face scan running continuously (MediaPipe FaceDetection).
- Emergency keyword thread running (always-on).
- assistant_agent active (llama-3.1-8b-instant):
    Handles casual conversation.
    Introduces itself: "I am A-Care. I can assist surgical staff with instrument retrieval.
    You need to be registered to use my features. Are you registered?"
    If user asks to fetch a tool: "Authentication required before I can fetch tools."
    If user asks to register: guides them to call admin.
    If user asks to login: begins login flow (face + voice).
    Bounded to: self-introduction, auth guidance. No small talk beyond 1-3 sentences.
    Model: llama-3.1-8b-instant, temperature 0.3, max 150 tokens.
```
 
---
 
### XXVI-C — Login Flow in Full (LOGGED_OUT → STANDBY)
 
```
Step 1 — Passive face detection (always-on, MediaPipe FaceDetection):
  Robot continuously scans for faces in front arc.
  No TTS, no prompt. Silent background scan.
 
Step 2 — Face detected:
  MobileNet compares face embedding vs all enrolled users.
  Best match found above threshold (0.78) → candidate_user identified.
  Robot says: "Welcome, {name}. Say confirm to log in."
 
Step 3 — Voice biometric simultaneously:
  As user says "confirm", Deepgram transcribes.
  SpeechBrain extracts d-vector from that utterance.
  Cosine similarity vs stored voice_embedding of candidate_user.
  Threshold: 0.85.
 
Step 4 — Both checks pass:
  Session created. active_user_id set in state_manager.
  TTS: "Logged in as {name}. How can I assist?"
  State → STANDBY.
 
Step 5 — Face check passes, voice fails:
  TTS: "Having trouble recognising your voice. Please try again."
  Retry once. Still fails → TTS: "Identity not confirmed. Please contact admin."
  No session created.
 
Step 6 — No face match found after 10s passive scan:
  No TTS. Continue passive scan. Robot stays on standby.
 
Step 7 — Manual fallback (user speaks first):
  assistant_agent handles conversation.
  Guides user through auth flow via dialogue.
  TTS: "I am ACARE. Please look at the camera to log in."
 
After login:
- Session active. active_user_id set.
- Inactivity timer starts: 5 minutes.
- Arm remains in standby pose.
- VAD active, Deepgram WebSocket open.
- Robot waits for voice command.
```
 
---
 
### XXVI-D — Receiving a Command in Full (STANDBY → PROCESSING)
 
```
User says: "Fetch the bandage" (or any tool name).
 
1. Silero VAD detects speech onset (32ms chunks, 16kHz, float32).
   Pause < 1.5s → pipeline waits (thinking pause).
   Pause > 3s + minimum 1s speech → utterance complete.
   < 1s total speech → discard (noise/cough).
 
2. Emergency keyword monitor checks every partial transcript:
   Keywords: stop, halt, emergency, abort, ruko, bas.
   Word-boundary match only. 100ms collision window.
   If triggered → ESTOP immediately (< 200ms latency target).
 
3. Deepgram Nova-2 streaming STT (WebSocket, en-IN):
   Audio streamed in 32ms chunks continuously (not batch).
   is_final=false → keyword monitor only.
   is_final=true AND speech_final=true → pass to normaliser.
 
4. normaliser.py:
   Lowercase → strip fillers →
   strip punctuation → simple unambiguous alias expansion only →
   multi-tool detection: 2+ tool names → flag MULTI_TOOL.
 
5. If MULTI_TOOL:
   TTS: "One at a time. Which first — {A} or {B}?"
   Wait for response. Resume from Step 1.
 
6. Groq intent parser (llama-3.1-8b-instant, JSON mode, temperature 0.0):
   Input: normalised transcript.
   Output: { "tool": "bandage", "action": "fetch", "confidence": 0.93 }
   destination is NOT in Groq output — hardcoded "user_handover" in planner.
 
7. Confidence check:
   >= 0.8 → clear intent → proceed to runtime voice consistency check.
   < 0.8 → ambiguous → dialogue_node (LangGraph) clarification (openai/gpt-oss-120b).
 
8. LangGraph clarification (if triggered):
   Intent Clarity Check → Clarification → Context Resolver →
   Interruption Handler → Dialogue Manager → back to auth gate.
 
9. Runtime voice consistency check:
   d-vector from current utterance vs logged-in user's voice_embedding.
   Pass → ValidatedIntent published to /validated_intent.
   Fail → TTS: "Voice not recognised. Command rejected." Log: UNAUTHORISED_VOICE_ATTEMPT.
 
10. ValidatedIntent published:
    { tool, action, user_id, authenticated: true }
    State → PROCESSING.
    planner_node receives on /validated_intent → begins task pipeline.
```
 
---
 
### XXVI-E — Task Pipeline in Full (PROCESSING → EXECUTING → HOLDING → HANDOVER → STANDBY)
 
```
planner_node._execute_fetch_task() called in background thread.
 
Phase 0 — World state check:
  safety_severity != ESTOP → OK.
  vision_status == READY → OK.
  network_ok == True → OK.
  Any fail → abort with TTS, return to STANDBY.
 
Phase 1 — Open gripper:
  Send GRIPPER_OPEN to embedded_interface_node.
  Wait 600ms (physical open time ~500ms per spec).
  Confirm force sensor = 0.
 
Phase 2 — Vision search:
  Record vision_start_time.
  propose_search_strategy() → priority_zones, reset_probability_map (agentic, llm-low)
  planner publishes /vision_search_request → vision_node receives.
  vision_node executes NBV search (full flow per Section XI).
  planner waits on /vision_result (timeout 30s).
  Record vision_search_ms.
  If not found: propose_vision_recovery() → retry up to MAX_RETRIES=3.
 
Phase 3 — IK + pre-grasp move:
  IK solver (DLS, Levenberg-Marquardt) called with grasp_point (x,y,z).
  Pre-grasp = grasp_point + 5cm in Z.
  SafetyKernel.validate_move(pre-grasp, world).
  Send MOVE to embedded_interface_node (pre-grasp position).
  velocity_scale = SafetyKernel.velocity_scale(world) × 0.8
  Wait MotionFeedback.success.
 
Phase 4 — Grasp:
  SafetyKernel.validate_grasp(force_target, world).
  Send MOVE to embedded_interface_node (grasp_point position).
  velocity_scale = SafetyKernel.velocity_scale(world) × 0.5
  Wait MotionFeedback.success.
  Send GRASP {force_target: 3.0N}.
  Wait 500ms for force to stabilise.
  Confirm gripper_force >= 1.0N.
  If fail → propose_grasp_recovery() → retry up to MAX_RETRIES=3.
  State → EXECUTING (arm in motion confirmed).
 
Phase 5 — Move to handover zone:
  Record motion_start_time.
  Get handover pose: get_handover_pose(user_id)
  SafetyKernel.validate_handover(world).
  SafetyKernel.validate_move(handover_pose, world).
  Send MOVE to embedded_interface_node (handover zone).
  velocity_scale = SafetyKernel.velocity_scale(world) × 0.6
  Wait MotionFeedback.success.
  Record motion_ms.
  State → HOLDING.
 
Phase 6 — Handover:
  State → HANDOVER.
  (Full 3-check verification per Section XXVI-F below.)
  On success → RELEASE.
 
Phase 7 — Cleanup:
  Record total_task_ms.
  learn_from_success(context, user_id)  ← update zone preferences, time patterns
  Log event to SQLite (all latency fields).
  Update probability_map (zone where tool found).
  TTS: "Handover complete. Is there anything else?"
  Arm → MOVE_NEUTRAL.
  State → STANDBY.
  Inactivity timer resets.
```
 
---
 
### XXVI-F — Complete Handover in Full (HANDOVER state)
 
```
_transition_state('HOLDING')
get_handover_pose(user_id) → handover_pose (base_zone + user Z-offset)
SafetyKernel.validate_handover(world)
SafetyKernel.validate_move(handover_pose, world)
_send_arm_move(handover_pose, velocity_scale × 0.6)
Wait MotionFeedback.success.
_transition_state('HANDOVER')
_speak("{tool} ready. Please face the camera.")
handover_start = time.monotonic()
current_z = handover_pose[2]
 
─── SUBSTATE 1: FACE_VERIFY ───────────────────────────────────────────────
 
Attempt 1: Default Z. Wait 8s for face (MobileNet vs logged-in user, threshold 0.78).
  Found → face_verified = True. Break to HAND_DETECT.
  Not found → propose_handover_face_recovery(attempt=1) → HANDOVER_Z_UP
    _speak("Please look at the camera.")
    Arm moves Z+5cm (validate first).
 
Attempt 2: Z+5cm. Wait 8s.
  Found → face_verified = True. Break.
  Not found → propose_handover_face_recovery(attempt=2) → HANDOVER_Z_DOWN
    _speak("Please face the camera directly.")
    Arm moves Z-5cm from default (validate first).
 
Attempt 3: Z-5cm. Wait 8s.
  Found → face_verified = True. Break.
  Not found → propose_handover_face_recovery(attempt=3) → HANDOVER_VOICE_HAND_ONLY
    _speak("Face verification unavailable. Proceeding with voice and hand only.")
    face_skipped = True.
    Proceed to HAND_DETECT regardless.
 
Timeout guard: (time.monotonic() - handover_start) > 30s → HANDOVER_TIMEOUT path.
 
─── SUBSTATE 2: HAND_DETECT ───────────────────────────────────────────────
 
vision_node switches to MediaPipe Hands mode (YOLOv11 NOT running simultaneously).
/hand_status published every camera frame.
 
_speak("Please place your open palm under the gripper.")
_wait_for_hand_detect(timeout=10.0)
  Polls every 100ms for: hand_detected=True AND is_open=True AND palm_up=True.
 
If not detected at 10s:
  _speak("Please open your palm and hold it steady.")
  _wait_for_hand_detect(timeout=8.0)
 
If still not detected at 18s total → HANDOVER_TIMEOUT path.
 
If hand detected:
  Dynamic incremental approach toward palm center.
  Each step: get /hand_status (x,y,z) → SafetyKernel.validate_move() → _send_arm_move()
  velocity_scale = 0.3 (very slow, contact-safe).
 
  While tracking palm:
    If voice command "lower": learn_height_adjustment(user_id, "lower")
    If voice command "higher": learn_height_adjustment(user_id, "higher")
    Arm adjusts ±5cm in Z. SafetyKernel validates. Preference stored.
 
Timeout guard: (time.monotonic() - handover_start) > 30s → HANDOVER_TIMEOUT path.
 
─── SUBSTATE 3: VOICE_CONFIRM ─────────────────────────────────────────────
 
_speak("Say 'take' to receive.")
_wait_for_voice_confirm(user_id, timeout=5.0)
  Checks keyword ("take"/"yes") AND d-vector consistency for logged-in user.
 
If voice matches but keyword not detected: retry once.
If voice does not match: _speak("Voice not recognised.") retry once.
After 2 failures → HANDOVER_TIMEOUT path.
 
─── RELEASE GATE ──────────────────────────────────────────────────────────
 
SafetyKernel.validate_release(world, face_verified, hand_ok, voice_ok):
  hand_detected AND voice_confirmed required (BOTH).
  face advisory — if face_skipped: returns (True, "FACE_SKIPPED — logged").
  If hand or voice fails → (False, reason) → _speak("Handover verification failed.
    Returning tool to tray.") → HANDOVER_TIMEOUT path.
 
If approved:
  If face_skipped: _log_event("FACE_VERIFY_SKIPPED", tool)
  _send_gripper_release()
  time.sleep(0.5)
  Force sensor drops to 0 → collection confirmed.
  world.arm_holding = False.
  Log: HANDOVER_SUCCESS.
  → Cleanup (Phase 7 above).
 
─── HANDOVER TIMEOUT PATH ─────────────────────────────────────────────────
 
_speak("No collection detected. Returning {tool} to tray.")
Arm moves to SAFE_DROP_ZONE (velocity_scale=0.3, SafetyKernel validated).
_send_gripper_release()
Log: HANDOVER_TIMEOUT.
State → STANDBY.
Probability map NOT updated.
Inactivity timer resets.
```
 
---
 
### XXVI-G — Session Management: Logout, Timeout, Multi-User
 
```
─── NORMAL LOGOUT ──────────────────────────────────────────────────────────
 
Staff says "logout".
Only accepted from: STANDBY or ESTOP states.
 
If state is EXECUTING, HOLDING, or HANDOVER:
  TTS: "Cannot log out during active task."
  Staff must say "stop" → ESTOP → safe deposit → then logout proceeds.
 
On logout:
  TTS: "Goodbye, {name}."
  Session terminated. active_user_id cleared.
  Deepgram WebSocket closed.
  probability_map serialised to yaml.
  State → LOGGED_OUT.
  Passive face detection resumes.
 
─── INACTIVITY TIMEOUT ─────────────────────────────────────────────────────
 
5 minutes no command in STANDBY:
  TTS: "Session timeout. Logging out {name}."
  Same cleanup as normal logout.
 
Hard TTL (2 hours default, configurable):
  session_hard_ttl_seconds: 7200 in system.yaml.
  Same cleanup as inactivity timeout.
 
─── MULTI-USER HANDLING ────────────────────────────────────────────────────
 
Second person approaches (LiDAR detects, face seen):
  auth_node sees face of person who is NOT active_user_id.
  TTS: "{staff_A} is currently logged in."
  No new session created.
 
Two people speak simultaneously:
  Both voices captured by Deepgram.
  Voice consistency check fails (mixed voices).
  TTS: "Command not processed. Only {name} can issue commands."
  Log: UNAUTHORISED_VOICE_ATTEMPT.
```
 
---
 
### XXVI-H — Edge Cases & Network Failures — Final Decisions
 
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
 
**Groq API Drop:**
```
planner's _call_llm() catches exception → returns None.
Deterministic fallback activates immediately.
Task continues on deterministic path.
No task abort purely from Groq failure.
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
 
### XXVI-I — Model Assignments — Final
 
| Component | Model | Why |
|---|---|---|
| intent_parser.py | llama-3.1-8b-instant | Fast JSON mode, intent parsing is simple classification |
| assistant_agent.py | llama-3.1-8b-instant | Bounded 1-3 sentence responses, conversational only |
| planner_node agentic layer | openai/gpt-oss-120b | Reasoning model, CoT depth for recovery, strict JSON schema |
| dialogue_node clarification | openai/gpt-oss-120b | Complex multi-step clarification needs reasoning depth |
| STT | Deepgram Nova-2 (en-IN) | Streaming WebSocket, en-IN locale |
| TTS normal | Microsoft Edge TTS | Natural voice, Indian English, large free tier |
| TTS ESTOP / safety | pyttsx3 (local) | Zero latency, fully offline, instant |
| TTS offline fallback | Kokoro ONNX INT8 | Local, natural, Pi-compatible, Apache 2.0 |
| Speaker verification | SpeechBrain d-vector | Robust speaker embeddings |
| Face detection (passive) | MediaPipe FaceDetection | Lightweight, always-on background scan |
| Face verification | MobileNet embedding | Fast embedding comparison at handover and login |
| Object detection | YOLOv11 ONNX INT8 | Pi-optimised, 95%+ mAP on 6-tool dataset |
| Hand tracking | MediaPipe Hands | HANDOVER state only |
| VAD | Silero VAD | Lightweight, local, 32ms chunks |
 
---
 
### XXVI-J — Spec Section Update Tracking
 
> The following records all spec changes made between the original specification and the final decisions document. These are fully integrated into their respective sections above.
 
| Section | Change Applied |
|---|---|
| Section VII | Removed all username/password references. Authentication is voice biometric (SpeechBrain d-vector) + face embedding (MobileNet) only. No username, no password, no typing anywhere in the system. |
| Section VII | Registration requires admin CLI only. No self-registration. Face + voice both enrolled at registration time. Face enrolment requires camera operational. |
| Section VII | Added: HANDOVER_VOICE_HAND_ONLY fallback — handover never aborts on face failure alone. Voice + hand still required. |
| Section VII | Added: Dynamic palm tracking during HAND_DETECT substate. Arm incrementally approaches user's palm using real-time /hand_status (x,y,z). |
| Section VII | Added: Session hard TTL (2h default, session_hard_ttl_seconds in system.yaml). |
| Section IX | Groq intent parser model confirmed: llama-3.1-8b-instant |
| Section X | assistant_agent model confirmed: llama-3.1-8b-instant |
| Section X | dialogue_node clarification model confirmed: openai/gpt-oss-120b |
| Section XI | Added CLAHE preprocessing step before YOLOv11 inference. Added adaptive confidence threshold (0.60 in low light, 0.70 normal). Added adaptive temporal consistency (3 viewpoints in low light, 2 normal). Added LOW_LIGHT_MODE flag to LogEvent. |
| Section XI | Added explicit statement: MediaPipe Hands and YOLOv11 do NOT run simultaneously. planner_node enforces this via state. |
| Section XI | Confirmed detection_candidates stored from VisionResult and passed to IK recovery as fallback pool. |
| Section XII | Replaced planner description with three-layer agentic architecture: openai/gpt-oss-120b + SafetyKernel + NodeCoordination. |
| Section XII | Added: RetryCounters dataclass. Per-failure-type retry counters (vision_search, grasp, ik_solve, handover_face). MAX_RETRIES=3. |
| Section XII | Added: Agentic model = openai/gpt-oss-120b. Reasoning: high for recovery, low for strategy. Strict JSON schema. Deterministic fallbacks for all decisions. |
| Section XII | Added: All AgenticPlanner methods, SafetyKernel methods, PlannerNode methods — fully specified with signatures. |
| Section XII | Added: task_phase_scale table for velocity per phase. |
| Section XIV | Added: LiDAR role at handover — detects torso presence, triggers camera face search. Does NOT identify user. Does NOT detect hands. |
| Section XVI | Added: FACE_VERIFY_SKIPPED, LIDAR_ESTOP, HARD_ESTOP, TASK_ABORTED, LOW_LIGHT_MODE to event_type enum. |
| Section XIX | Added: low_light_confidence_threshold, low_light_brightness_cutoff to system.yaml. Added session_hard_ttl_seconds. Added planner model config block. |
| Section XXI | Added: openai/gpt-oss-120b for planner agentic layer and dialogue clarification. Added CLAHE preprocessing entry. Updated intent model string to llama-3.1-8b-instant. |
| Section XXII | Added KPI: Agentic recovery success rate (task completed despite first failure) — target > 80%. |
| Section XXIII | Updated: planner_node status reflects agentic version specification. |
 
---
 
*End of ACARE Integrated Specification — Ramaiah Institute of Technology, Bengaluru — April 2026*

 

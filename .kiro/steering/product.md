# ACARE — Autonomous Clinical Assistance Robot

ACARE is a stationary 6-DOF semi-autonomous robotic arm for clinical environments (plastic surgery departments). It fetches and delivers surgical instruments to authenticated staff via voice commands, eliminating manual tool handling during long surgical shifts.

## Core Capabilities
- Voice-commanded tool retrieval (fetch by name or alias)
- Dual biometric authentication (voice + face) per session
- Emergency stop via keyword detection (<200ms latency)
- Direct handover to authenticated staff's hand
- Single tool per command, single active session at a time

## System Layers
- **Software** — Raspberry Pi 5, ROS2, Python AI nodes (this repo's primary domain)
- **Embedded/Firmware** — Teensy 4.1, PID motor control, safety ISRs
- **Hardware** — 6-DOF arm, sensors, power system

## Current Repo Scope
This workspace contains two sub-projects:
- `acarevoice/` — Standalone voice pipeline (VAD → ASR → NLP → TTS). Runnable without ROS2.
- `acare_camera_test/` — Camera SDK integration tests for YDLIDAR HP60C.

The full ROS2 system (planner, vision, auth, safety nodes) is defined in `acarevoice/acare_spec.md` but not yet implemented here.

## Operational Constraints
- Requires internet (Deepgram STT + Groq LLM — no offline fallback)
- Single tool per command; multi-tool requests trigger clarification dialogue
- Logout rejected during EXECUTING / HOLDING / HANDOVER states
- ESTOP always overrides all other states

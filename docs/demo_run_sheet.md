# ACARE Demo Day — Run Sheet

**Project:** ACARE — Autonomous Clinical Assistance Robot  
**Path:** `ACARE/`  
**Date:** ___________  
**Operator:** ___________  

---

## 1. Pre-Demo Checklist (1 Hour Before Judges Arrive)

### Hardware Setup
- [ ] Pi 5 powered on, SSH accessible (`ssh acare@<pi-ip>`)
- [ ] Robot arm secured on table, all joints free-moving
- [ ] Test objects (scissors, forceps, thermometer, oximeter, plaster, cream) placed in known positions on tray
- [ ] HP60C RGBD camera connected via USB, lens clean
- [ ] T-mini LiDAR connected, no obstructions within 600mm
- [ ] USB sound card + mic + speaker connected
- [ ] 24V power supply connected, ESTOP button accessible
- [ ] Table is stable, robot base is level

### Software Setup
- [ ] ROS2 Jazzy sourced: `source /opt/ros/jazzy/setup.bash`
- [ ] Workspace sourced: `source ~/acare_ws/install/setup.bash`
- [ ] Python venv activated (if used)
- [ ] Sound device test: `python3 -c "import sounddevice; print(sounddevice.query_devices())"`
- [ ] Camera test: `ros2 topic list | grep camera` (should show `/ascamera_hp60c/...`)
- [ ] Internet connectivity confirmed (Deepgram + Groq + Nvidia NIM needed)
- [ ] Voice `.env` file has valid API keys:
  ```
  DEEPGRAM_API_KEY=...
  GROQ_API_KEY=...
  NVIDIA_NIM_API_KEY=...
  ```

### Staff Enrolment
- [ ] Run admin CLI: `ros2 run acare_admin admin_cli`
- [ ] Select "Enrol new staff member"
- [ ] Enter name (e.g. "Dr. Demo") and role (surgeon/nurse/admin)
- [ ] Look at camera — 10 face frames will be captured automatically
- [ ] Speak 3 prompted phrases clearly — 3 voice samples captured
- [ ] Verify enrolment: `admin_cli` → "List enrolled staff"
- [ ] If multiple operators, enrol each one

### System Test (Full Dry Run)
- [ ] Run full launch: `ros2 launch acare_bringup acare.launch.py`
- [ ] Wait 15s for all nodes to initialize
- [ ] Check all nodes running: `ros2 node list`
  - Expected: `/voice_node`, `/dialogue_node`, `/auth_node`, `/state_manager`, `/planner_node`, `/embedded_interface_node`, `/vision_node`, `/safety_node`, `/log_node`, `/admin_node`
- [ ] Stand in front of camera — wait for TTS: "Welcome [name]. Say confirm to log in."
- [ ] Say "confirm" — expect TTS: "[name] authenticated. You may now issue a command."
- [ ] Say "fetch scissors" — robot should search, find, grasp, and hand over
- [ ] Test ESTOP: say "stop" — robot should freeze
- [ ] Test ESTOP recovery: say "resume" — should transition to STANDBY
- [ ] Kill launch: Ctrl+C
- [ ] **Fix any issues before demo**

---

## 2. Demo Day Script (What Judges See)

### Demo Flow (Target: 5-7 minutes)

```
Step 1 — POWER ON (30s)
  Operator: Presses power button on Pi 5
  Judges see: Pi booting, terminal scrolling
  Audio: "ACARE system initializing..."

Step 2 — SYSTEM READY (45s)  
  All nodes start with staggered timers
  Audio: "ACARE system ready. Stand by for authentication." (pyttsx3 offline TTS)
  Judges see: Robot arm at rest position, camera LED on

Step 3 — FACE DETECTION (10s)
  Operator stands in front of camera
  Camera detects face → matches enrolled user
  Audio: "Welcome Dr. Demo. Say confirm to log in."
  Judges see: Robot acknowledges operator by name

Step 4 — VOICE LOGIN (5s)
  Operator says: "Confirm"
  Voice verification matches enrolled voice
  Audio: "Dr. Demo authenticated. You may now issue a command."
  Judges see: Seamless biometric login (face + voice)

Step 5 — FETCH COMMAND (3s)
  Judge or operator says: "Fetch scissors"
  Deepgram STT → Groq intent parsing
  Audio: "Searching for scissors."
  Judges see: Robot processes natural language command

Step 6 — VISION SEARCH (15-30s)
  Arm moves to viewpoint positions
  Camera scans tray, YOLO detects scissors
  Audio: "Scissors located. Approaching."
  Judges see: Arm moves deliberately, camera scanning

Step 7 — GRASP (10s)
  Arm descends to grasp position
  Gripper closes on scissors
  Audio: "Tool acquired."
  Judges see: Precise pick-up, gripper holds tool securely

Step 8 — HANDOVER (20s)
  Arm moves to face-level position
  Face re-verification
  Arm presents tool at handover zone
  Audio: "Please reach for the tool."
  Judge reaches hand → hand detected
  Audio: "Say take to receive."
  Judge says: "Take"
  Gripper releases
  Audio: "Task complete."
  Judges see: Safe, multi-step handover with voice confirmation
```

### What To Say If Something Goes Wrong

| Problem | Recovery Script |
|---------|----------------|
| Voice not recognized | "The microphone needs a moment. Let me try again." (step closer) |
| Vision can't find tool | "Let me check the tray alignment." (adjust objects slightly) |
| Arm stops mid-motion | "The safety system detected something. Let me resume." (check ESTOP, say "resume") |
| Login fails | "The lighting angle may have shifted." (adjust position, try again) |
| Gripper slips | "Let me try a firmer grip." (system auto-retries) |
| Network timeout | "The system has offline fallback. One moment." (wait for deterministic mode) |

---

## 3. Key Technical Details

### Network Dependencies (Must Have Internet)

| Service | Purpose | Fallback |
|---------|---------|----------|
| Deepgram | Speech-to-text (Nova-2) | ❌ No fallback — voice pipeline dead without it |
| Groq | Intent parsing (8B) + dialogue (70B) + fallback planner | ❌ No fallback — commands won't be parsed |
| Nvidia NIM | Agentic planner | ✅ Falls back to Groq → deterministic |
| Edge TTS | Text-to-speech | ✅ pyttsx3 (offline, robotic voice) |

### Critical API Keys (in `.env`)
```
DEEPGRAM_API_KEY=<required>
GROQ_API_KEY=<required>
NVIDIA_NIM_API_KEY=<optional but recommended>
```

### Camera Info
- HP60C RGBD: 640×480 @ ~12.4Hz
- Depth range: 200mm – 4000mm
- Camera topics: `/ascamera_hp60c/camera_publisher/rgb0/image`, `/depth0/image_raw`
- Intrinsics auto-loaded from `/camera_info` topic

### Arm Specs
- 6-DOF serial manipulator
- Links: 352mm (base) + 400mm (shoulder→elbow) + 400mm (elbow→wrist) + 236mm (wrist→TCP)
- Workspace: x: ±0.6m, y: ±0.6m, z: 0.0–0.75m
- Tray zone: 0.40–0.55m from base
- Joint limits: J1 ±180°, J2 ±135°, J3 ±120°, J4-6 ±180°

### Recognition Thresholds
- Face similarity: ≥ 0.78
- Voice similarity: ≥ 0.85
- YOLO confidence: ≥ 0.70 (normal light), ≥ 0.56 (low light)

### Timing
- Inactivity auto-logout: 5 minutes in STANDBY
- Hard session TTL: 2 hours
- Handover timeout: 30 seconds → safe deposit
- ESTOP keyword detection: <200ms
- Default kiosk velocity scale: 0.22 (slow, safe for demo)

---

## 4. Emergency Procedures

### If ESTOP triggers
1. Check what caused it: LiDAR proximity? Voice keyword? Overcurrent?
2. Say "resume" or manually publish: `ros2 topic pub --once /emergency_stop acare_msgs/msg/EmergencySignal "{reason: 'cleared', source: 'manual'}"`
3. Robot returns to STANDBY
4. Resume demo: say "fetch [tool]" again

### If a node crashes
- Supervisor auto-restarts: log_node, admin_node, dialogue_node, voice_node, auth_node
- Critical nodes (safety, interface, state_manager, planner, vision) → ESTOP if they crash
- Check terminal output for error messages

### If voice pipeline fails
- Check `.env` has valid API keys
- Check internet connectivity: `ping api.deepgram.com`
- Test mic: `python3 -c "import sounddevice; print(sounddevice.query_devices())"`
- Verify sounddevice can record: `python3 -c "import sounddevice as sd; sd.rec(int(16000), samplerate=16000, channels=1)"`

### Power recovery (if system shuts down mid-task)
1. Reboot Pi
2. Launch system
3. Supervisor auto-detects last state from SQLite logs
4. If last state was EXECUTING/HOLDING/HANDOVER → publishes safe state + TTS warning
5. Verify workspace is clear before continuing

---

## 5. Quick Commands Reference

```bash
# Launch everything
ros2 launch acare_bringup acare.launch.py

# Check nodes
ros2 node list

# Check topics
ros2 topic list

# See robot state
ros2 topic echo /robot_state --once

# See camera feed
ros2 topic echo /ascamera_hp60c/camera_publisher/rgb0/image --once

# Test admin CLI
ros2 run acare_admin admin_cli

# Manual ESTOP
ros2 topic pub --once /emergency_stop acare_msgs/msg/EmergencySignal "{reason: 'manual_test', source: 'cli'}"

# Clear ESTOP (transition back to STANDBY)
ros2 topic pub --once /state_transition acare_msgs/msg/StateTransition "{target_state: 'STANDBY', reason: 'manual_clear'}"

# Enrol staff via service
ros2 service call /enrol_staff acare_msgs/srv/EnrolStaff "{name: 'Dr. Demo', role: 'surgeon'}"

# Check logs
ros2 topic echo /log_event

# Kill all
Ctrl+C
```

---

## 6. Post-Demo
- [ ] Power off Pi: `sudo shutdown now`
- [ ] Disconnect 24V power
- [ ] Clean camera lens
- [ ] Charge batteries (if any)
- [ ] Save logs: `cp -r ~/.ros/log/ ~/acare_demo_logs/`

---

*Generated by Hermes Agent — ACARE Demo Audit skill*

# ACARE — Raspberry Pi 5 Setup & Progress Log

**Date completed:** May 10, 2026  
**Pi:** Raspberry Pi 5 8GB  
**OS:** Ubuntu Server 24.04.4 LTS (aarch64)  
**Kernel:** Linux 6.8.0-1052-raspi  
**IP:** 192.168.1.72  
**Username:** acare / Password: acare1234  
**WiFi:** Airtel_Sarsou

---

## 1. OS & System Setup

- Flashed Ubuntu Server 24.04.4 LTS (64-bit) using Raspberry Pi Imager v2.0.7
- SSH enabled with password authentication from first boot
- WiFi pre-configured in Imager (Airtel_Sarsou)
- Passwordless SSH set up from laptop (SSH key installed)
- `unattended-upgrades` disabled — prevents background apt from dropping SSH
- `needrestart` masked — prevents service restarts mid-apt-session
- System updated: `sudo apt update && sudo apt upgrade -y`

---

## 2. ROS2 Jazzy Installation

ROS2 Jazzy installed on Ubuntu 24.04 (Noble) ARM64.

**Dependency conflict fix required:**
Ubuntu 24.04 security updates bump library patch versions higher than ROS2 Jazzy expects.
Fixed by downgrading: `liblz4-1`, `libzstd1`, `zlib1g`, `libbz2-1.0` to exact versions ROS2 needs.

```bash
sudo apt install -y --allow-downgrades \
  liblz4-1=1.9.4-1build1 libzstd1=1.5.5+dfsg2-2build1 \
  "zlib1g=1:1.3.dfsg-3.1ubuntu2" libbz2-1.0=1.0.8-5.1
sudo apt install -y ros-jazzy-ros-base
```

**Verified working:**
```
ros2 topic list -> /parameter_events /rosout
ROS_DISTRO = jazzy
```

---

## 3. ROS2 Workspace — acare_ws

```
~/acare_ws/
├── src/
│   ├── acare_msgs/          <- Custom messages (14 msgs + 1 srv) — BUILT
│   ├── acare_vision/        <- Vision pipeline — BUILT
│   ├── acare_voice/         <- Voice pipeline (partial) — BUILT
│   ├── acare_planner/       <- Planner nodes (partial) — BUILT
│   ├── acare_safety/        <- Safety monitoring — BUILT
│   ├── acare_logging/       <- SQLite audit trail — BUILT
│   ├── acare_admin/         <- Admin CLI — BUILT
│   ├── acare_auth/          <- Biometric auth (Shreevanth) — BUILT
│   ├── acare_dialogue/      <- Custom State/Slots dialogue (Shreevanth) — BUILT
│   ├── acare_embedded_interface/ <- C++ UART bridge (empty) — BUILT
│   ├── acare_bringup/       <- Config + launch + supervisor — BUILT
│   └── ascamera/            <- YDLIDAR HP60C SDK ROS2 node — BUILT
├── logs/
│   └── acare_logs.db        <- SQLite audit log
└── install/                 <- Built packages
```

**Build command:**
```bash
source /opt/ros/jazzy/setup.bash
cd ~/acare_ws && colcon build --symlink-install
```

All 12 packages build successfully.

---

## 4. Python Dependencies Installed

```bash
pip install --break-system-packages \
  speechbrain deepgram-sdk groq pyttsx3 mediapipe onnxruntime

sudo apt install -y python3-colcon-common-extensions python3-pip \
  python3-opencv unzip ros-jazzy-pcl-conversions ros-jazzy-pcl-ros \
  build-essential
```

---

## 5. YDLIDAR HP60C Camera

Camera confirmed working on Pi 5.

- SDK: EaiCameraSdk_v1.2.28 (extracted from HP60C ROS_V1.2.28.zip)
- SDK libraries installed to /usr/local/lib/
- udev rules installed — camera accessible without root
- ascamera ROS2 node built and tested

**Camera specs confirmed:**
- RGB: 640x480 BGR8 @ 12.4 Hz
- Depth: 640x480 16UC1 (uint16, millimetres) @ 12.4 Hz
- Depth range: 489mm – 1330mm (tested)
- 98.6% valid depth pixel coverage

**To start camera:**
```bash
cd ~/acare_ws && ros2 launch ascamera hp60c.launch.py
```

**Topics published:**
```
/ascamera_hp60c/camera_publisher/rgb0/image
/ascamera_hp60c/camera_publisher/depth0/image_raw
/ascamera_hp60c/camera_publisher/depth0/points
/ascamera_hp60c/camera_publisher/rgb0/camera_info
/ascamera_hp60c/camera_publisher/depth0/camera_info
```

---

## 6. YOLOv11 ONNX Model

- Model: YOLOv11m trained on Ultralytics Hub
- Dataset: 1095 images, 6 classes
- Export: ONNX FP32, 320x320 input, opset 12
- Location on Pi: /home/acare/models/yolo_acare.onnx (76.6 MB)

**Classes (6):**

| ID | Model Class | Canonical Name |
|----|-------------|----------------|
| 0 | cream | cream |
| 1 | medical scissors | scissors |
| 2 | oxymeter | oximeter |
| 3 | plaster | plaster |
| 4 | surgical forceps | forceps |
| 5 | thermometer | thermometer |

Performance on Pi 5: ~414ms/frame (YOLOv11m FP32 at 320x320)

**Export command (run on laptop):**
```python
from ultralytics import YOLO
model = YOLO('best.pt')
model.export(format='onnx', imgsz=320, simplify=True, opset=12, dynamic=False)
```

---

## 7. acare_msgs — Custom ROS2 Messages

All 14 messages and 1 service built and verified importable.

**Messages:** RobotState, StateTransition, Intent, ValidatedIntent, SafetyAlert,
HandStatus, AuthResult, VisionResult, VisionSearchRequest, ArmCommand,
GripperCommand, MotionFeedback, LogEvent, EmergencySignal

**Service:** EnrolStaff (name, role -> success, staff_id, message)

---

## 8. Vision Pipeline — acare_vision

All 7 files deployed and tested.

| File | Purpose | Status |
|------|---------|--------|
| yolo_infer.py | ONNX inference wrapper, 6 classes, NMS, multi-frame | Tested |
| hp60c_camera_node.py | Subscribes to ascamera topics, exposes capture() | Deployed |
| fake_detector.py | Dual-signal fake detection (Laplacian + depth variance) | Deployed |
| localiser.py | Depth pixel to 3D robot frame (placeholder intrinsics) | Deployed |
| hand_tracker.py | MediaPipe Hands, 20Hz, HANDOVER state only | Deployed |
| nbv_search.py | Bayesian NBV search, probability map, temporal consistency | Deployed |
| vision_node.py | ROS2 orchestrator, MultiThreadedExecutor, mode switching | Deployed |

Notes:
- localiser.py uses placeholder intrinsics — real values needed after calibration
- nbv_search.py viewpoints list is empty until arm calibration

---

## 9. Configuration Files

Location: /home/acare/acare_ws/src/acare_bringup/config/

- system.yaml — workspace bounds, arm DH params (placeholders), camera intrinsics (placeholders), voice/auth config
- thresholds.yaml — safety thresholds (current 8A, temp 75C, LiDAR 400mm, gripper 15N)
- probability_map.yaml — Bayesian prior for tool placement (3 zones, 6 tools each)

---

## 10. Software Nodes Deployed

| Node | Package | Run Command | Status |
|------|---------|-------------|--------|
| state_manager.py | acare_planner | ros2 run acare_planner state_manager | Tested |
| normaliser.py | acare_voice | library | 5/5 tests |
| tool_registry.py | acare_planner | library | All assertions pass |
| log_node.py | acare_logging | ros2 run acare_logging log_node | SQLite working |
| safety_node.py | acare_safety | ros2 run acare_safety safety_node | Tested |
| handover.py | acare_planner | library, used by planner_node | Tested |
| admin_cli.py | acare_admin | python3 admin_cli.py cmd | Tested |
| supervisor.py | acare_bringup | python3 supervisor.py | Tested |

---

## 11. What's Remaining

### Blocked on Hardware Team (URGENT)
- DH parameters for all 6 joints
- Joint limits (min/max angles)
- Link lengths
- Gearbox ratios for joints 4, 5, 6
- Motor driver model

These are required before ik_solver.py and planner_node.py can be built.

### To Build (Software)
- ik_solver.py — DLS IK, blocked on hardware params
- planner_node.py — full orchestrator, blocked on IK solver
- embedded_interface_node.cpp — UART bridge to Teensy
- acare.launch.py — full system launch file

### Shreevanth's Work (Voice + Auth)
- vad.py, asr.py, keyword_monitor.py — Complete (in acarevoice/)
- tts.py — In progress
- assistant_agent.py — Complete
- dialogue_node.py, auth_node.py, verify_voice.py, enrol.py — To build
- verify_face.py, face_detect.py — To build (placeholder for vision)

### After Hardware Assembly
- Camera intrinsics calibration (checkerboard, OpenCV)
- Camera extrinsics calibration (T_robot_camera)
- NBV viewpoints definition (admin.py calibrate Step 5)
- Fake detection threshold calibration (20 real + 20 fake tools)
- IK solver validation (5 test positions)
- Full system integration test

---

## 12. Daily Use Commands

```bash
# SSH in
ssh acare@192.168.1.72   # password: acare1234

# Start camera
cd ~/acare_ws && ros2 launch ascamera hp60c.launch.py

# Check camera topics
ros2 topic list
ros2 topic hz /ascamera_hp60c/camera_publisher/rgb0/image

# Build workspace
source /opt/ros/jazzy/setup.bash
cd ~/acare_ws && colcon build --symlink-install

# Check Pi health
vcgencmd measure_temp
free -h

# Shutdown
sudo shutdown now
```

---

*Generated: May 10, 2026*

---

## 13. Restore from Backup

If the SD card fails or you need to set up a new Pi, follow these steps exactly.

### Step 1 — Flash new SD card
Use Raspberry Pi Imager on your laptop:
- Device: Raspberry Pi 5
- OS: Ubuntu Server 24.04.4 LTS (64-bit)
- Settings:
  - Hostname: `acare`
  - Username: `acare`, Password: `acare1234`
  - Enable SSH: password authentication
  - WiFi SSID: `Airtel_Sarsou`, Password: `MyAirtel@79`, Country: `IN`
  - Timezone: Asia/Kolkata, Keyboard: us

### Step 2 — First boot and SSH in
```bash
# Wait 2 minutes after powering on, then:
ssh acare@192.168.1.72   # IP may vary — check with arp -a if needed
```

### Step 3 — Disable auto-updaters (do this FIRST before anything else)
```bash
sudo systemctl disable --now unattended-upgrades
sudo systemctl disable --now apt-daily.timer apt-daily-upgrade.timer
sudo apt remove -y needrestart
```

### Step 4 — System update
```bash
sudo apt update && sudo apt upgrade -y
```

### Step 5 — Install ROS2 Jazzy
```bash
sudo apt install -y software-properties-common curl
sudo add-apt-repository -y universe
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update

# Fix Ubuntu 24.04 dependency conflict
sudo apt install -y --allow-downgrades \
  liblz4-1=1.9.4-1build1 libzstd1=1.5.5+dfsg2-2build1 \
  "zlib1g=1:1.3.dfsg-3.1ubuntu2"
sudo apt-mark hold liblz4-1 libzstd1 zlib1g
sudo apt install -y --allow-downgrades \
  liblz4-dev=1.9.4-1build1 libzstd-dev=1.5.5+dfsg2-2build1 \
  "zlib1g-dev=1:1.3.dfsg-3.1ubuntu2"
sudo apt-mark hold liblz4-dev libzstd-dev zlib1g-dev
sudo apt install -y ros-jazzy-ros-base

# Fix build-essential
sudo apt-mark unhold liblz4-1 liblz4-dev libzstd1 libzstd-dev zlib1g zlib1g-dev
sudo apt install -y --allow-downgrades libbz2-1.0=1.0.8-5.1 bzip2 build-essential
```

### Step 6 — Install tools and Python deps
```bash
sudo apt install -y python3-colcon-common-extensions python3-pip \
  python3-opencv unzip ros-jazzy-pcl-conversions ros-jazzy-pcl-ros

pip install --break-system-packages \
  speechbrain deepgram-sdk groq pyttsx3 mediapipe onnxruntime
```

### Step 7 — Transfer and restore backup from laptop
Run on your **laptop** PowerShell:
```powershell
scp "C:\Users\Sonali\Desktop\ACARE\completed\acare_pi_backup_20260510.tar.gz" acare@192.168.1.72:~/
```

Then on the **Pi**:
```bash
cd ~ && tar -xzf acare_pi_backup_20260510.tar.gz
echo "Backup restored"
ls ~/acare_ws/src/
```

### Step 8 — Transfer ONNX model (if not in backup)
Run on **laptop**:
```powershell
scp "C:\Users\Sonali\Desktop\ACARE\model_- 10 may 2025 16_42 (1).onnx" acare@192.168.1.72:~/models/yolo_acare.onnx
```

### Step 9 — Transfer HP60C SDK (if not in backup)
Run on **laptop**:
```powershell
scp "C:\Users\Sonali\Downloads\EaiCameraSdk_v1.2.28.zip" acare@192.168.1.72:~/
scp "C:\Users\Sonali\Downloads\HP60C ROS_V1.2.28.zip" acare@192.168.1.72:~/
```

Then on the **Pi**:
```bash
cd ~ && unzip EaiCameraSdk_v1.2.28.zip -d EaiCameraSdk
unzip "HP60C ROS_V1.2.28.zip" -d HP60C_ROS
cd ~/HP60C_ROS/EaiCameraSdk_v1.2.28.20241015/demo/ && bash unpack_linux_ros.sh
sudo cp ~/HP60C_ROS/EaiCameraSdk_v1.2.28.20241015/demo/linux_ros/ros2/ascamera/libs/lib/aarch64-linux-gnu/*.so /usr/local/lib/
sudo ldconfig
sudo bash ~/HP60C_ROS/EaiCameraSdk_v1.2.28.20241015/demo/linux_ros/ros2/ascamera/scripts/create_udev_rules.sh
sudo systemctl daemon-reload
```

### Step 10 — Build the workspace
```bash
source /opt/ros/jazzy/setup.bash
cd ~/acare_ws && colcon build --symlink-install
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
echo "source ~/acare_ws/install/setup.bash" >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Step 11 — Verify everything works
```bash
# Check ROS2
ros2 topic list

# Check all packages built
ros2 pkg list | grep acare

# Check ONNX model
python3 -c "import onnxruntime as ort; s=ort.InferenceSession('/home/acare/models/yolo_acare.onnx'); print('Model OK:', s.get_inputs()[0].shape)"

# Check acare_msgs
python3 -c "from acare_msgs.msg import RobotState, VisionResult, SafetyAlert; print('Messages OK')"

# Check Pi health
vcgencmd measure_temp
free -h
```

Expected output:
```
/parameter_events
/rosout
Model OK: [1, 3, 320, 320]
Messages OK
temp=~50C
Mem: 7.8Gi total, ~350Mi used
```

---

## 14. Running the System

### Start camera only (for vision testing)
```bash
# Terminal 1 — start camera
cd ~/acare_ws && ros2 launch ascamera hp60c.launch.py

# Terminal 2 — verify streaming
ros2 topic hz /ascamera_hp60c/camera_publisher/rgb0/image
# Expected: ~12 Hz
```

### Run individual nodes (for testing)
```bash
source ~/.bashrc

# State manager
ros2 run acare_planner state_manager

# Safety node (requires LiDAR connected)
ros2 run acare_safety safety_node

# Log node
ros2 run acare_logging log_node

# Vision node (requires camera running first)
ros2 run acare_vision vision_node
```

### Check state machine is working
```bash
# In one terminal, run state_manager
ros2 run acare_planner state_manager

# In another terminal, trigger a transition
ros2 topic pub --once /state_transition acare_msgs/msg/StateTransition \
  '{target_state: "STANDBY", reason: "test"}'

# Check state was published
ros2 topic echo /robot_state --once
# Expected: state: STANDBY
```

### Check log node is working
```bash
# Run log node
ros2 run acare_logging log_node

# Publish a test log event
ros2 topic pub --once /log_event acare_msgs/msg/LogEvent \
  '{event_type: "TEST", user_id: "test", tool: "scissors", state: "STANDBY", description: "manual test"}'

# Check DB
sqlite3 ~/acare_ws/logs/acare_logs.db "SELECT event_type, tool, state FROM events ORDER BY rowid DESC LIMIT 3;"
```

### Admin CLI usage
```bash
# Check system status
python3 ~/acare_ws/src/acare_admin/acare_admin/admin_cli.py status

# Show recent logs
python3 ~/acare_ws/src/acare_admin/acare_admin/admin_cli.py show-logs --last 10

# Set API keys
python3 ~/acare_ws/src/acare_admin/acare_admin/admin_cli.py set-api-key --service deepgram --key YOUR_KEY
python3 ~/acare_ws/src/acare_admin/acare_admin/admin_cli.py set-api-key --service groq --key YOUR_KEY

# Enable demo mode (disables biometric checks for exhibition)
python3 ~/acare_ws/src/acare_admin/acare_admin/admin_cli.py demo-mode --enable
```

### Run supervisor (starts and monitors all nodes)
```bash
source ~/.bashrc
python3 ~/acare_ws/src/acare_bringup/supervisor.py
```

---

## 15. Troubleshooting

### SSH times out
```bash
# Find Pi IP
1..254 | ForEach-Object { ping -n 1 -w 50 192.168.1.$_ > $null }; arp -a
# Look for new 192.168.1.x entry
```

### SSH says "REMOTE HOST IDENTIFICATION HAS CHANGED"
```bash
ssh-keygen -R 192.168.1.72
# Then SSH again normally
```

### colcon build fails with "ament_package not found"
```bash
# Always source ROS2 before building
source /opt/ros/jazzy/setup.bash
cd ~/acare_ws && colcon build --symlink-install
```

### Camera not found after reboot
```bash
# Check camera is detected
lsusb | grep -i novatek
# Should show: Bus 004 Device 002: ID 3482:6723 NOVATEK ASJ ZNX_NVT

# Check udev rules are applied
ls /etc/udev/rules.d/ | grep angstrong
# Should show: angstrong-camera.rules

# Reload udev if needed
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### acare_msgs import fails
```bash
# Rebuild msgs and source workspace
source /opt/ros/jazzy/setup.bash
cd ~/acare_ws && colcon build --packages-select acare_msgs
source ~/acare_ws/install/setup.bash
```

### Pi temperature too high (>70C)
```bash
vcgencmd measure_temp
# If >70C, check active cooling fan is running
# Reduce load: stop unnecessary nodes
```

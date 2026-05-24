# ACARE — Pi Setup & Daily Use Reference

---

## Pi Credentials

| Field | Value |
|---|---|
| Username | `acare` |
| Password | `acare1234` |
| Hostname | `acare` |
| WiFi | `Airtel_Sarsou` |
| IP (typical) | `192.168.1.72` or `192.168.1.73` |

---

## Every Day — Starting Up

### 1. Power on the Pi
Plug in the USB-C power cable. Wait 2 minutes for boot.

### 2. Find the Pi's IP
Run this in PowerShell on your laptop:
```
1..254 | ForEach-Object { ping -n 1 -w 50 192.168.1.$_ > $null }; arp -a
```
Look for a `192.168.1.x` entry that wasn't there before. That's the Pi.

### 3. SSH in
```
ssh acare@192.168.1.72
```
Replace `192.168.1.72` with whatever IP you found. Password: `acare1234`

If you get "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED", run:
```
ssh-keygen -R 192.168.1.72
```
Then SSH again.

---

## Every Day — Starting the Camera

The camera node must be running before any vision code can use it.

### Start the camera (from acare_ws directory)
```bash
cd ~/acare_ws && ros2 launch ascamera hp60c.launch.py
```

### Verify camera is streaming (in a second SSH session)
```bash
ros2 topic list
```
You should see `/ascamera_hp60c/camera_publisher/rgb0/image` and `/ascamera_hp60c/camera_publisher/depth0/image_raw`.

Check frame rate:
```bash
ros2 topic hz /ascamera_hp60c/camera_publisher/rgb0/image
```
Expected: ~12 Hz.

---

## Every Day — Shutting Down

**Always shut down properly. Never just unplug — it can corrupt the SD card.**

### Stop the camera node
Press `Ctrl+C` in the terminal running the camera launch.

### Shut down the Pi
```bash
sudo shutdown now
```
Wait for the green LED to go dark (~10 seconds), then unplug the power.

---

## Opening a Second SSH Session

Open a new PowerShell window on your laptop and SSH in again with the same command:
```
ssh acare@192.168.1.72
```
You can have as many SSH sessions open simultaneously as you need.

---

## Adding a New WiFi Network

To add your mobile hotspot or a teammate's WiFi so the Pi connects automatically:
```bash
sudo nmcli dev wifi connect "NetworkName" password "NetworkPassword"
```

Or edit the netplan config directly:
```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```
Add the new network under `access-points:`, then apply:
```bash
sudo netplan apply
```

---

## Checking Pi Health

```bash
# Temperature
vcgencmd measure_temp

# Disk usage
df -h

# Memory usage
free -h

# CPU load
top
```

---

## ROS2 Workspace

### Rebuild after code changes
```bash
cd ~/acare_ws && colcon build --symlink-install && source ~/.bashrc
```

### Check all packages are built
```bash
ros2 pkg list | grep acare
```

### Source the workspace manually (if needed)
```bash
source /opt/ros/jazzy/setup.bash
source ~/acare_ws/install/setup.bash
```

---

## Camera SDK Location

The HP60C SDK is extracted at:
```
~/HP60C_ROS/EaiCameraSdk_v1.2.28.20241015/demo/linux_ros/
```

Config files for the camera are at:
```
~/acare_ws/ascamera/configurationfiles/
```
The camera launch must be run from `~/acare_ws/` so it finds this path.

---

## Transferring Files to/from Pi

### Laptop → Pi
```
scp "C:\path\to\file" acare@192.168.1.72:~/
```

### Pi → Laptop
```
scp acare@192.168.1.72:/path/on/pi "C:\destination\on\laptop"
```

---

## If the Pi Won't Connect to WiFi

1. Unplug and replug power, wait 2 minutes
2. Run the network scan command again
3. If still not showing up, the Pi may have gotten a different IP — scan the full range

If it still won't connect after a reboot, the netplan config may be corrupted. Pull the SD card, put it in the card reader, and check `/etc/netplan/50-cloud-init.yaml` on the `writable` partition (requires a Linux machine or WSL to read ext4).

---

## If SSH Says "Connection Refused"

SSH service may not have started. Wait 1 more minute and try again. If it persists after 5 minutes, reboot the Pi.

## If SSH Says "Connection Timed Out"

The Pi is not on the network. Run the IP scan again — it may have a different IP.

---

## Pi Setup History (for reference)

The Pi was set up with:
- Ubuntu Server 24.04.4 LTS (64-bit, aarch64)
- ROS2 Jazzy (ros-jazzy-ros-base)
- All acare_ws packages built (11 acare packages + ascamera)
- Python deps: speechbrain, deepgram-sdk, groq, langgraph, pyttsx3, mediapipe, onnxruntime
- HP60C camera SDK extracted and configured
- unattended-upgrades disabled (prevents background apt from dropping SSH)
- needrestart masked

**Camera confirmed working:** RGB 640×480 BGR8 @ 12.4 Hz, Depth 640×480 16UC1 @ 12.4 Hz, range 489–1330mm validated.

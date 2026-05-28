#!/bin/bash
# ============================================================
# ACARE FULL SIMULATION SETUP
# Run this ONCE to install everything needed for Level 3 sim.
# Re-run after pulling code changes — it's idempotent.
# After this, just run: ~/acare_sim_ws/launch_full_sim.sh
# ============================================================
set -e

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/ros/jazzy/bin

SIM_FILES="/mnt/c/Users/Sonali/Desktop/ACARE/sim_files"
ACARE_SRC="/mnt/c/Users/Sonali/Desktop/ACARE/acare_software_final"
WS=~/acare_sim_ws
MOVEIT_CFG="$WS/src/urdf_assembly_6dof_moveit_config"
DESC_PKG="$WS/src/urdf_assembly_6dof_description"

echo "============================================================"
echo " ACARE Full Simulation Setup"
echo "============================================================"

# 1. Install system dependencies
echo "[1/8] Installing system dependencies..."
sudo apt-get install -y \
    ros-jazzy-gz-ros2-control \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-controller-manager \
    python3-pip \
    portaudio19-dev \
    pulseaudio-utils \
    alsa-utils \
    rsync \
    2>&1 | tail -3

# 2. Install Python dependencies for voice / vision pipeline
# numpy is pinned <2 so system matplotlib (used transitively by mediapipe)
# can load. opencv pinned to a numpy-1.x compatible version for the same reason.
echo "[2/8] Installing Python dependencies..."
pip3 install --break-system-packages \
    'deepgram-sdk==3.10.1' \
    sounddevice 'numpy<2' torch torchaudio silero-vad \
    edge-tts pyttsx3 pygame groq python-dotenv \
    onnxruntime 'opencv-python-headless<4.10' mediapipe \
    pydantic 'PyYAML>=6.0' \
    2>&1 | tail -5

# 3. Sync ACARE source packages from Windows mount into WS
echo "[3/8] Syncing ACARE packages..."
for pkg in acare_bringup acare_msgs acare_planner acare_safety acare_logging acare_vision acare_voice acare_auth acare_dialogue acare_embedded_interface acare_admin; do
    if [ -d "$ACARE_SRC/$pkg" ]; then
        rm -rf "$WS/src/$pkg"
        mkdir -p "$WS/src/$pkg"
        rsync -a \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            --exclude='pyproject.toml' \
            --exclude='requirements.txt' \
            --exclude='uv.lock' \
            --exclude='.env' \
            --exclude='tests/' \
            "$ACARE_SRC/$pkg/" "$WS/src/$pkg/"
    fi
done

# Preserve voice .env between syncs (kept outside rsync)
VOICE_ENV="$WS/src/acare_voice/.env"

# 4. Copy Gazebo ros2_control xacro
echo "[4/8] Installing Gazebo ros2_control plugin config..."
cp "$SIM_FILES/gz_ros2_control.xacro" "$MOVEIT_CFG/config/urdf_assembly_6dof.ros2_control.xacro"
sed -i 's/filename="gz_ros2_control-system"/filename="libgz_ros2_control-system.so"/' \
    "$MOVEIT_CFG/config/urdf_assembly_6dof.ros2_control.xacro"

# 5. Copy bridge config
echo "[5/8] Installing ros_gz_bridge config..."
mkdir -p "$DESC_PKG/config"
cp "$SIM_FILES/gz_bridge.yaml" "$DESC_PKG/config/gz_bringup.yaml" 2>/dev/null || true
cp "$SIM_FILES/gz_bridge.yaml" "$DESC_PKG/config/gz_bridge.yaml"

# 6. Copy launch files
echo "[6/8] Installing launch files..."
cp "$SIM_FILES/acare_sim.launch.py" "$MOVEIT_CFG/launch/acare_sim.launch.py"
cp "$SIM_FILES/launch_full_sim.sh" "$WS/launch_full_sim.sh"
chmod +x "$WS/launch_full_sim.sh"

# 7. Create .env file for voice pipeline (API keys) — only if missing
echo "[7/8] Setting up voice pipeline .env..."
if [ ! -f "$VOICE_ENV" ]; then
    cat > "$VOICE_ENV" <<EOF
DEEPGRAM_API_KEY=
GROQ_API_KEY=
EOF
    echo ""
    echo "  ⚠️  IMPORTANT: Edit $VOICE_ENV and add your API keys!"
    echo "     nano $VOICE_ENV"
    echo ""
fi

# 8. Rebuild workspace from a clean state for the affected packages
echo "[8/8] Rebuilding workspace..."
source /opt/ros/jazzy/setup.bash
cd "$WS"
rm -rf build/acare_voice build/acare_planner build/acare_safety build/acare_logging build/acare_vision build/acare_bringup build/acare_msgs build/acare_auth build/acare_dialogue build/acare_embedded_interface build/acare_admin
rm -rf install/acare_voice install/acare_planner install/acare_safety install/acare_logging install/acare_vision install/acare_bringup install/acare_msgs install/acare_auth install/acare_dialogue install/acare_embedded_interface install/acare_admin

colcon build --merge-install \
    --packages-select acare_msgs acare_bringup acare_planner acare_safety acare_logging acare_vision acare_voice acare_auth acare_dialogue acare_embedded_interface acare_admin \
    2>&1 | tail -25

echo ""
echo "============================================================"
echo " SETUP COMPLETE"
echo "============================================================"
echo ""
echo " Before first run, add your API keys:"
echo "   nano $VOICE_ENV"
echo ""
echo " Then launch the full simulation:"
echo "   ~/acare_sim_ws/launch_full_sim.sh"
echo ""
echo "============================================================"

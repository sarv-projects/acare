#!/bin/bash
# ============================================================
# ACARE FULL SIMULATION SETUP
# Run this ONCE to install everything needed for Level 3 sim.
# After this, just run: ~/acare_sim_ws/launch_full_sim.sh
# ============================================================
set -e

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/ros/jazzy/bin

SIM_FILES="/mnt/c/Users/Sonali/Desktop/ACARE/sim_files"
WS=~/acare_sim_ws
MOVEIT_CFG="$WS/src/urdf_assembly_6dof_moveit_config"
DESC_PKG="$WS/src/urdf_assembly_6dof_description"
VOICE_PKG="$WS/src/acare_voice"

echo "============================================================"
echo " ACARE Full Simulation Setup"
echo "============================================================"

# 1. Install system dependencies
echo "[1/7] Installing system dependencies..."
sudo apt-get install -y \
    ros-jazzy-gz-ros2-control \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-joint-state-publisher-gui \
    python3-pip \
    portaudio19-dev \
    2>&1 | tail -3

# 2. Install Python dependencies for voice pipeline
echo "[2/7] Installing Python dependencies for voice..."
pip3 install --break-system-packages \
    deepgram-sdk sounddevice numpy torch silero-vad \
    edge-tts pyttsx3 pygame groq python-dotenv \
    2>&1 | tail -5

# 3. Copy Gazebo ros2_control xacro
echo "[3/7] Installing Gazebo ros2_control plugin config..."
cp "$SIM_FILES/gz_ros2_control.xacro" "$MOVEIT_CFG/config/urdf_assembly_6dof.ros2_control.xacro"
# Fix plugin filename
sed -i 's/filename="gz_ros2_control-system"/filename="libgz_ros2_control-system.so"/' \
    "$MOVEIT_CFG/config/urdf_assembly_6dof.ros2_control.xacro"

# 4. Copy bridge config
echo "[4/7] Installing ros_gz_bridge config..."
mkdir -p "$DESC_PKG/config"
cp "$SIM_FILES/gz_bridge.yaml" "$DESC_PKG/config/gz_bridge.yaml"

# 5. Copy launch files
echo "[5/7] Installing launch files..."
cp "$SIM_FILES/acare_sim.launch.py" "$MOVEIT_CFG/launch/acare_sim.launch.py"
cp "$SIM_FILES/launch_full_sim.sh" "$WS/launch_full_sim.sh"
chmod +x "$WS/launch_full_sim.sh"

# 6. Create .env file for voice pipeline (API keys)
echo "[6/7] Setting up voice pipeline .env..."
if [ ! -f "$VOICE_PKG/.env" ]; then
    echo "DEEPGRAM_API_KEY=" > "$VOICE_PKG/.env"
    echo "GROQ_API_KEY=" >> "$VOICE_PKG/.env"
    echo ""
    echo "  ⚠️  IMPORTANT: Edit $VOICE_PKG/.env and add your API keys!"
    echo "     nano $VOICE_PKG/.env"
    echo ""
fi

# 7. Rebuild workspace
echo "[7/7] Rebuilding workspace..."
source /opt/ros/jazzy/setup.bash
cd "$WS"
colcon build --merge-install 2>&1 | tail -10

echo ""
echo "============================================================"
echo " SETUP COMPLETE"
echo "============================================================"
echo ""
echo " Before first run, add your API keys:"
echo "   nano ~/acare_sim_ws/src/acare_voice/.env"
echo ""
echo " Add these lines:"
echo "   DEEPGRAM_API_KEY=your_key_here"
echo "   GROQ_API_KEY=your_key_here"
echo ""
echo " Then launch the full simulation:"
echo "   ~/acare_sim_ws/launch_full_sim.sh"
echo ""
echo "============================================================"

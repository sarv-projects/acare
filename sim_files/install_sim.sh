#!/bin/bash
# Run this in WSL to install Level 3 simulation files
set -e
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/ros/jazzy/bin

SIM_FILES="/mnt/c/Users/Sonali/Desktop/ACARE/sim_files"
WS=~/acare_sim_ws
MOVEIT_CFG="$WS/src/urdf_assembly_6dof_moveit_config"
DESC_PKG="$WS/src/urdf_assembly_6dof_description"

echo "=== Installing Level 3 Simulation Files ==="

# 1. Replace ros2_control xacro with Gazebo version
echo "[1/5] Installing Gazebo ros2_control xacro..."
cp "$SIM_FILES/gz_ros2_control.xacro" "$MOVEIT_CFG/config/urdf_assembly_6dof.ros2_control.xacro"

# 2. Install bridge config
echo "[2/5] Installing ros_gz_bridge config..."
mkdir -p "$DESC_PKG/config"
cp "$SIM_FILES/gz_bridge.yaml" "$DESC_PKG/config/gz_bridge.yaml"

# 3. Install launch file
echo "[3/5] Installing simulation launch file..."
cp "$SIM_FILES/acare_sim.launch.py" "$MOVEIT_CFG/launch/acare_sim.launch.py"

# 4. Install gz_ros2_control package
echo "[4/5] Installing gz_ros2_control..."
sudo apt-get install -y ros-jazzy-gz-ros2-control ros-jazzy-ros-gz-sim ros-jazzy-ros-gz-bridge 2>&1 | tail -3

# 5. Rebuild workspace
echo "[5/5] Rebuilding workspace..."
source /opt/ros/jazzy/setup.bash
cd "$WS"
colcon build --merge-install --packages-select urdf_assembly_6dof_moveit_config urdf_assembly_6dof_description 2>&1 | tail -5

echo ""
echo "=== Installation Complete ==="
echo ""
echo "To launch the full simulation:"
echo "  export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/ros/jazzy/bin"
echo "  source /opt/ros/jazzy/setup.bash"
echo "  source ~/acare_sim_ws/install/setup.bash"
echo "  ros2 launch urdf_assembly_6dof_moveit_config acare_sim.launch.py"

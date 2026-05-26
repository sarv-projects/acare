#!/bin/bash
set -e
echo "=== ACARE ROS2 Jazzy Installation ==="
echo "Started at: $(date)"

# Step 1: Add ROS2 repo
echo "[1/4] Adding ROS2 repository..."
sudo apt-get update -qq
sudo apt-get install -y -qq software-properties-common curl > /dev/null 2>&1
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu noble main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt-get update -qq
echo "[1/4] DONE"

# Step 2: Install ROS2 Jazzy Desktop
echo "[2/4] Installing ROS2 Jazzy Desktop (this takes ~10 min)..."
sudo apt-get install -y ros-jazzy-desktop > /dev/null 2>&1
echo "[2/4] DONE"

# Step 3: Install simulation dependencies
echo "[3/4] Installing MoveIt2 + Gazebo + controllers..."
sudo apt-get install -y \
    ros-jazzy-moveit \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controllers \
    ros-jazzy-gazebo-ros-pkgs \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-xacro \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-controller-manager \
    ros-jazzy-joint-trajectory-controller \
    ros-jazzy-joint-state-broadcaster \
    ros-dev-tools \
    python3-colcon-common-extensions \
    python3-pip > /dev/null 2>&1
echo "[3/4] DONE"

# Step 4: Verify
echo "[4/4] Verifying..."
source /opt/ros/jazzy/setup.bash
ros2 --version
echo ""
echo "=== INSTALLATION COMPLETE ==="
echo "Finished at: $(date)"
echo "Disk usage:"
df -h / | tail -1

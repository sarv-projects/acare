#!/bin/bash
# ============================================================
# ACARE FULL LEVEL 3 SIMULATION
# One script to launch everything.
# ============================================================
set -e

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/ros/jazzy/bin
source /opt/ros/jazzy/setup.bash
source ~/acare_sim_ws/install/setup.bash

# Gazebo needs to find the ros2_control plugin
export GZ_SIM_SYSTEM_PLUGIN_PATH=/opt/ros/jazzy/lib

# Gazebo needs to find robot meshes
export GZ_SIM_RESOURCE_PATH=$(ros2 pkg prefix urdf_assembly_6dof_description)/share/urdf_assembly_6dof_description/meshes:$GZ_SIM_RESOURCE_PATH

# For voice pipeline audio in WSL
export PULSE_SERVER=unix:/mnt/wslg/PulseServer

echo "========================================================"
echo " ACARE — Full Level 3 Simulation"
echo "========================================================"
echo ""
echo " Launching: Gazebo + Arm + Camera + LiDAR + Bridge"
echo "            + State Manager + Planner + Safety + Voice"
echo ""
echo " Auth: demo_mode (say 'confirm' to login)"
echo " Then: say 'fetch scissors' (or any tool)"
echo "========================================================"
echo ""

# --- Launch the ROS2 simulation (Gazebo + controllers + bridge + ACARE nodes) ---
ros2 launch urdf_assembly_6dof_moveit_config acare_sim.launch.py &
SIM_PID=$!

# Wait for Gazebo and controllers to be ready
echo "[ACARE] Waiting for simulation to initialize (15s)..."
sleep 15

# --- Launch voice pipeline in background ---
echo "[ACARE] Starting voice pipeline..."
cd ~/acare_sim_ws/src/acare_voice
python3 voice_ros_node.py &
VOICE_PID=$!
cd ~/acare_sim_ws

echo ""
echo "========================================================"
echo " SIMULATION RUNNING"
echo "========================================================"
echo ""
echo " Gazebo: table with instruments visible"
echo " RViz:   arm visualization"
echo " Voice:  listening on your microphone"
echo ""
echo " Say 'confirm' to login (demo mode)"
echo " Then say 'fetch scissors' or 'fetch forceps' etc."
echo ""
echo " Press Ctrl+C to stop everything"
echo "========================================================"

# Wait for either process to exit
wait $SIM_PID $VOICE_PID

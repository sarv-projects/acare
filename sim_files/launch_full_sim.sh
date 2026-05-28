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

# For voice pipeline audio in WSL — WSLg pulse audio passthrough
export PULSE_SERVER=unix:/mnt/wslg/PulseServer

# Load voice API keys (Deepgram, Groq) into environment if .env present
VOICE_ENV=~/acare_sim_ws/src/acare_voice/.env
if [ -f "$VOICE_ENV" ]; then
    set -a
    source "$VOICE_ENV"
    set +a
fi

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

# --- Sanity check: voice API keys ---
if [ -z "$DEEPGRAM_API_KEY" ] || [ -z "$GROQ_API_KEY" ]; then
    echo "[WARN] DEEPGRAM_API_KEY or GROQ_API_KEY not set."
    echo "       Voice pipeline will not work without them."
    echo "       Edit: $VOICE_ENV"
    echo ""
fi

if [ -z "$NVIDIA_NIM_API_KEY" ]; then
    echo "[INFO] NVIDIA_NIM_API_KEY not set — agentic planner will use Groq fallback."
    echo ""
fi

# --- Launch the full simulation in one ros2 launch invocation ---
# (Voice node is included in acare_sim.launch.py — no separate process)
exec ros2 launch urdf_assembly_6dof_moveit_config acare_sim.launch.py

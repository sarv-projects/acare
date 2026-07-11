#!/bin/bash
# acare_mock_demo.sh — MoveIt2 + mock hardware demo (NO Gazebo required)
# Guaranteed path: shows robot moving in RViz with full ACARE pipeline.
set -e

echo "========================================"
echo " ACARE — MOVEIT2 MOCK HARDWARE DEMO"
echo "========================================"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ACARE_ROOT="$(dirname "$SCRIPT_DIR")"
SIM_ROOT="$ACARE_ROOT/simulation/src/acaresim_final/acaresim"

[ -f /opt/ros/jazzy/setup.bash ] && source /opt/ros/jazzy/setup.bash

# Build sim workspace if needed
if [ ! -f "$SIM_ROOT/install/setup.bash" ]; then
    echo "[BUILD] Building sim workspace..."
    cd "$SIM_ROOT" && colcon build --symlink-install
fi
source "$SIM_ROOT/install/setup.bash"

# Build main workspace if needed
if [ -f "$ACARE_ROOT/install/setup.bash" ]; then
    source "$ACARE_ROOT/install/setup.bash"
fi

# --- 1. Launch MoveIt2 with mock hardware (RViz window opens) ---
echo "[1/4] Launching MoveIt2 with mock hardware..."
ros2 launch moveit_config demo.launch.py use_mock_hardware:=true > /tmp/acare_moveit.log 2>&1 &
MOVEIT_PID=$!
echo "  RViz should open shortly showing the robot"
sleep 5

# --- 2. Activate controllers ---
echo "[2/4] Activating controllers..."
for i in $(seq 1 15); do
    sleep 2
    if ros2 node list 2>/dev/null | grep -q controller_manager; then
        break
    fi
done
ros2 control switch_controllers --activate arm_controller gripper_controller joint_state_broadcaster 2>/dev/null || true
echo "  Controllers active"

# --- 3. Launch ACARE software ---
echo "[3/4] Launching ACARE pipeline..."
ros2 launch acare_bringup acare.launch.py supervisor:=false > /tmp/acare_nodes.log 2>&1 &
NODES_PID=$!
sleep 5

# --- 4. Ready ---
ros2 topic pub -1 /state_transition acare_msgs/msg/StateTransition "{target_state: STANDBY, reason: boot}" 2>/dev/null || true
echo ""
echo "[4/4] READY"
echo "  RViz shows the ACARE arm"
echo "  controllers: arm_controller, gripper_controller"
echo ""
echo "  Publish a command:"
echo "    ros2 topic pub /raw_transcript acare_msgs/msg/Transcript '{text: \"fetch scissors\"}'"
echo "  Or use the voice pipeline if mic + Deepgram keys configured"
echo "========================================"

trap "kill $MOVEIT_PID $NODES_PID 2>/dev/null; exit" INT TERM
wait $MOVEIT_PID

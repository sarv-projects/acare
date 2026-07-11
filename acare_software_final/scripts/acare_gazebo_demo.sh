#!/bin/bash
# acare_gazebo_demo.sh — Unified Gazebo + ACARE launch for demo
# Works from any machine. Uses main codebase + simulation URDF assets.
set -e

echo "========================================"
echo " ACARE — GAZEBO SIMULATION DEMO LAUNCH"
echo "========================================"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ACARE_ROOT="$(dirname "$SCRIPT_DIR")"                 # acare_software_final/
SIM_ROOT="$ACARE_ROOT/simulation/src/acaresim_final/acaresim"
URDF_DESC="$SIM_ROOT/src/urdf_assembly_6dof_description"

# --- Check environment ---
if [ -z "$ROS_DISTRO" ]; then
    if [ -f /opt/ros/jazzy/setup.bash ]; then
        source /opt/ros/jazzy/setup.bash
    elif [ -f /opt/ros/humble/setup.bash ]; then
        source /opt/ros/humble/setup.bash
    else
        echo "ERROR: ROS2 not found. Source your ROS2 setup.bash first."
        exit 1
    fi
fi

# Build sim workspace if needed
if [ ! -f "$SIM_ROOT/install/setup.bash" ]; then
    echo "[BUILD] Building simulation workspace..."
    cd "$SIM_ROOT"
    colcon build --symlink-install
    echo "[BUILD] Done."
fi

source "$SIM_ROOT/install/setup.bash"

# Build main workspace if needed
MAIN_WS="$ACARE_ROOT"
if [ ! -f "$MAIN_WS/install/setup.bash" ] && [ ! -f "$MAIN_WS/build" ]; then
    echo "[BUILD] Building main ACARE workspace..."
    cd "$MAIN_WS"
    colcon build --symlink-install --packages-skip irb120_ros2_gazebo irb120_ros2_moveit2 urdf_assembly_6dof_moveit_config
    echo "[BUILD] Done."
fi

if [ -f "$MAIN_WS/install/setup.bash" ]; then
    source "$MAIN_WS/install/setup.bash"
else
    echo "NOTE: Main workspace not colcon-built. Using python3 directly."
fi

# --- 1. Launch Gazebo with robot model ---
echo "[1/6] Launching Gazebo with robot model..."
ros2 launch urdf_assembly_6dof_description gazebo.launch.py > /tmp/acare_gazebo.log 2>&1 &
GAZEBO_PID=$!
echo "  Gazebo PID=$GAZEBO_PID"

# --- 2. Wait for controller manager ---
echo "[2/6] Waiting for controllers (up to 60s)..."
for i in $(seq 1 30); do
    sleep 2
    if ros2 node list 2>/dev/null | grep -q controller_manager; then
        echo "  Controller manager ready after ${i}x2s"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "  WARNING: Controller manager not detected. Continuing anyway..."
    fi
done

# Wait a bit more for action servers to come up
sleep 3

# --- 3. Activate controllers ---
echo "[3/6] Activating controllers..."
if ros2 control list_controllers 2>/dev/null | grep -q arm_controller; then
    ros2 control switch_controllers --activate arm_controller gripper_controller joint_state_broadcaster 2>/dev/null || true
    echo "  Controllers activated"
else
    echo "  Using controller_manager spawner (controllers auto-activated)"
fi

# --- 4. Launch ACARE software nodes ---
echo "[4/6] Launching ACARE software pipeline..."
if [ -f "$MAIN_WS/install/setup.bash" ]; then
    ros2 launch acare_bringup acare.launch.py sim_mode:=true supervisor:=false > /tmp/acare_nodes.log 2>&1 &
else
    # Fallback: run nodes individually as python scripts
    python3 "$ACARE_ROOT/acare_planner/state_manager.py" > /tmp/state_mgr.log 2>&1 &
    sleep 1
    python3 "$ACARE_ROOT/acare_safety/safety_node.py" > /tmp/safety.log 2>&1 &
    python3 "$ACARE_ROOT/acare_logging/log_node.py" > /tmp/log_node.log 2>&1 &
    python3 "$ACARE_ROOT/acare_embedded_interface/embedded_interface_node.py" > /tmp/embedded.log 2>&1 &
    python3 "$ACARE_ROOT/acare_auth/auth_node.py" > /tmp/auth.log 2>&1 &
    python3 "$ACARE_ROOT/acare_dialogue/dialogue_node.py" > /tmp/dialogue.log 2>&1 &
    python3 "$ACARE_ROOT/acare_planner/planner_node.py" > /tmp/planner.log 2>&1 &
    python3 "$ACARE_ROOT/acare_vision/vision_node.py" > /tmp/vision.log 2>&1 &
    python3 "$ACARE_ROOT/acare_voice/voice_ros_node.py" > /tmp/voice.log 2>&1 &
fi
NODES_PID=$!
echo "  ACARE nodes PID=$NODES_PID"
sleep 5

# --- 5. Set initial state ---
echo "[5/6] Setting initial state to STANDBY..."
ros2 topic pub -1 /state_transition acare_msgs/msg/StateTransition "{target_state: STANDBY, reason: boot}" 2>/dev/null || true

# --- Status ---
echo ""
echo "[6/6] STATUS"
echo "--- Active ROS2 Nodes ---"
ros2 node list 2>/dev/null | sort -u || echo "(no nodes detected)"
echo ""
echo "--- Controllers ---"
ros2 control list_controllers 2>/dev/null || echo "(no controllers detected)"
echo ""
echo "========================================"
echo " READY — Gazebo should show the robot"
echo ""
echo " In a new terminal, say 'fetch scissors'"
echo " or publish manually:"
echo "   ros2 topic pub /raw_transcript acare_msgs/msg/Transcript '{text: \"fetch scissors\"}'"
echo ""
echo " Debug logs:"
echo "   tail -f /tmp/acare_gazebo.log"
echo "   tail -f /tmp/planner.log"
echo "========================================"

# Keep running until Ctrl+C
trap "kill $GAZEBO_PID $NODES_PID 2>/dev/null; exit" INT TERM
wait $GAZEBO_PID

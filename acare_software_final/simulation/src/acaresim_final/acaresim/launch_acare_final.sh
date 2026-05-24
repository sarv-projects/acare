#!/bin/bash
echo "========================================"
echo " ACARE — FINAL SIMULATION LAUNCH"
echo "========================================"

source /opt/ros/jazzy/setup.bash
source /home/shreevanth-m/acare_demo_ws/install/setup.bash
source /home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/install/setup.bash
ACARE_ROOT="/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim"

# --- 1. MoveIt2 Simulation (with RViz window) ---
echo "[1/7] MoveIt2 Simulation..."
ros2 launch moveit_config demo.launch.py > /tmp/acare_sim.log 2>&1 &
echo "  Started — RViz window should open (may take a moment)"

# --- 2. Wait for simulation ---
echo "[2/7] Waiting for controllers..."
for i in $(seq 1 15); do
  sleep 2
  if ros2 node list 2>/dev/null | grep -q arm_controller; then
    echo "  Controllers ready (${i}x2s)"
    break
  fi
done

# --- 3. Activate controllers ---
echo "[3/7] Activating controllers..."
ros2 control switch_controllers --activate arm_controller gripper_controller joint_state_broadcaster > /dev/null 2>&1
echo "  Activated"

# --- 4. Pipeline nodes ---
echo "[4/7] Starting pipeline nodes..."
python3 "$ACARE_ROOT/src/acare_planner/state_manager.py" > /tmp/state_mgr.log 2>&1 &
sleep 2

python3 "$ACARE_ROOT/src/acare_planner/embedded_interface_node.py" > /tmp/embedded_interface.log 2>&1 &
sleep 2

python3 "$ACARE_ROOT/src/acare_planner/planner_node.py" > /tmp/planner.log 2>&1 &

python3 "$ACARE_ROOT/src/acare_logging/log_node.py" > /tmp/log_node.log 2>&1 &

python3 "$ACARE_ROOT/src/acare_safety/safety_node.py" > /tmp/safety.log 2>&1 &
sleep 3

# Set initial state
ros2 topic pub -1 /state_transition acare_msgs/msg/StateTransition "{target_state: STANDBY, reason: boot}" > /dev/null 2>&1

# --- 5. Voice node ---
echo "[5/7] Starting voice node..."
cd "$ACARE_ROOT/src/acare_voice"
python3 -m voice.voice_node &
VOICE_PID=$!
cd "$ACARE_ROOT"
sleep 2
echo "  Voice PID=$VOICE_PID — you should hear the greeting"

# --- Status ---
echo ""
echo "[6/7] STATUS"
echo "--- All Active Nodes ---"
ros2 node list 2>/dev/null | sort -u
echo ""
echo "--- Controllers ---"
ros2 control list_controllers 2>/dev/null
echo ""
echo "[7/7] READY"
echo "========================================"
echo "  RViz should show the robot"
echo "  You should hear: 'A-Care system ready'"
echo "  Say: 'fetch scissors' (or scalpel, forceps, etc.)"
echo ""
echo "  For troubleshooting logs:"
echo "    tail -f /tmp/planner.log"
echo "    tail -f /tmp/state_mgr.log"
echo "========================================"

wait $VOICE_PID

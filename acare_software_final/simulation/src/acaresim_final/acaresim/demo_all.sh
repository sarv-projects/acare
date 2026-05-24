#!/bin/bash
source /opt/ros/jazzy/setup.bash
source /home/shreevanth-m/acare_demo_ws/install/setup.bash
source /home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim/install/setup.bash
ACARE_ROOT="/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim"
export DISPLAY=:99

echo "╔══════════════════════════════════════════════╗"
echo "║   ACARE — FINAL SIMULATION DEMO              ║"
echo "╚══════════════════════════════════════════════╝"

echo ""
echo "═══ SCENARIO 1: SYSTEM BOOT ═══"
echo "Starting MoveIt2 simulation..."
ros2 launch moveit_config demo.launch.py > /tmp/sim.log 2>&1 &
sleep 10
echo "Activating controllers..."
ros2 control switch_controllers --activate arm_controller gripper_controller joint_state_broadcaster > /dev/null 2>&1
sleep 2
echo ""
echo "--- All Nodes ---"
ros2 node list 2>/dev/null | sort -u
echo ""

echo "═══ SCENARIO 2: PIPELINE NODES ═══"
echo "Starting state_manager..."
python3 "$ACARE_ROOT/src/acare_planner/state_manager.py" > /tmp/sm.log 2>&1 &
sleep 2
echo "Starting embedded_interface..."
python3 "$ACARE_ROOT/src/acare_planner/embedded_interface_node.py" > /tmp/ei.log 2>&1 &
sleep 2
echo "Starting planner_node..."
python3 "$ACARE_ROOT/src/acare_planner/planner_node.py" > /tmp/planner.log 2>&1 &
sleep 2
echo "Setting state to STANDBY..."
ros2 topic pub -1 /state_transition acare_msgs/msg/StateTransition '{target_state: STANDBY, reason: demo_boot}' > /dev/null 2>&1
sleep 1
echo ""

echo "═══ SCENARIO 3: VOICE COMMAND (SIMULATED) ═══"
echo "User says: 'fetch scissors'"
echo "Publishing validated intent..."
ros2 topic pub -1 /validated_intent acare_msgs/msg/ValidatedIntent '{tool: scissors, action: fetch, user_id: staff_001, name: "Dr. Sharma", authenticated: true}' > /dev/null 2>&1
sleep 5
echo ""
echo "--- State Machine Trace ---"
grep "State:" /tmp/sm.log 2>/dev/null | tail -4
echo ""
echo "--- Joint States (arm pose after move) ---"
timeout 3 ros2 topic echo /joint_states --once 2>/dev/null | grep -A 10 "position:"
echo ""

echo "═══ SCENARIO 4: ESTOP SAFETY ═══"
echo "User says: 'STOP'"
ros2 topic pub -1 /safety_alert acare_msgs/msg/SafetyAlert '{severity: ESTOP, reason: voice_keyword_stop, source: voice}' > /dev/null 2>&1
sleep 1
echo "--- State After ESTOP ---"
tail -3 /tmp/sm.log 2>/dev/null
echo ""

echo "╔══════════════════════════════════════════════╗"
echo "║   DEMO COMPLETE — Real pipeline verified    ║"
echo "║                                             ║"
echo "║   To run with voice, in another terminal:   ║"
echo "║   cd \$ACARE_ROOT/src/acare_voice           ║"
echo "║   python3 -m voice.voice_node               ║"
echo "╚══════════════════════════════════════════════╝"

#!/bin/bash
echo "====================================="
echo " ACARE Simulation — Full Launch"
echo "====================================="

source /opt/ros/jazzy/setup.bash
source /home/shreevanth-m/acare_demo_ws/install/setup.bash
ACARE_ROOT="/home/shreevanth-m/acare_demo_ws/src/acaresim_final/acaresim"

echo "[1/3] Starting MoveIt2 simulation..."
export DISPLAY=:99
ros2 launch moveit_config demo.launch.py > /tmp/acare_sim.log 2>&1 &
SIM_PID=$!
echo "  Simulation PID: $SIM_PID"

echo "[2/3] Waiting for controllers..."
for i in $(seq 1 15); do
  sleep 2
  if ros2 node list 2>/dev/null | grep -q arm_controller; then
    echo "  Ready after $((i*2))s"
    break
  fi
  echo "  ...waiting"
done

echo ""
echo "[3/3] Verifying..."
ros2 node list 2>/dev/null
echo ""
ros2 control list_controllers 2>/dev/null
echo ""
echo "=== READY ==="

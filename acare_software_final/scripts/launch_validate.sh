#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -z "${ROS_DISTRO:-}" ]]; then
  source /opt/ros/jazzy/setup.bash
fi

source "${ROOT_DIR}/install/setup.bash"

ros2 launch acare_bringup acare.launch.py >/tmp/acare_launch.log 2>&1 &
LAUNCH_PID=$!

cleanup() {
  kill "${LAUNCH_PID}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

sleep 10

# Verify launch process is still alive before validation
if ! kill -0 "${LAUNCH_PID}" 2>/dev/null; then
  echo "ERROR: ros2 launch process died during startup. Check /tmp/acare_launch.log"
  exit 1
fi

python3 "${ROOT_DIR}/scripts/validate_ros_graph.py"

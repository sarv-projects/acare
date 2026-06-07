#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -z "${ROS_DISTRO:-}" ]]; then
  source /opt/ros/jazzy/setup.bash
fi

python3 -m pip install -r "${ROOT_DIR}/requirements_ros2_runtime.txt"
python3 "${ROOT_DIR}/scripts/preflight_ros_env.py"

cd "${ROOT_DIR}"
colcon build --symlink-install

echo ""
echo "============================================"
echo "Build complete. Run this to source the workspace:"
echo "  source \"${ROOT_DIR}/install/setup.bash\""
echo "============================================"

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -z "${ROS_DISTRO:-}" ]]; then
  source /opt/ros/jazzy/setup.bash
fi

python3 -m pip install -r "${ROOT_DIR}/requirements_ros2_runtime.txt"
python3 "${ROOT_DIR}/scripts/preflight_ros_env.py"

cd "${ROOT_DIR}"
colcon build --symlink-install --packages-up-to acare_bringup

source "${ROOT_DIR}/install/setup.bash"
echo "Workspace build complete."

from __future__ import annotations

import importlib
import shutil
import sys
from pathlib import Path


REQUIRED_COMMANDS = ["ros2", "colcon"]
REQUIRED_MODULES = [
    "rclpy",
    "pydantic",
    "numpy",
    "yaml",
    "deepgram",
    "sounddevice",
    "speechbrain",
    "torch",
    "mediapipe",
    "insightface",
    "onnxruntime",
    "cv2",
    "cryptography",
]
ROOT = Path(__file__).resolve().parents[1]
SYSTEM_YAML = ROOT / "acare_bringup" / "config" / "system.yaml"


def _warn_config_gaps():
    try:
        import yaml

        cfg = yaml.safe_load(SYSTEM_YAML.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        print(f"WARN config system.yaml unreadable: {type(exc).__name__}: {exc}")
        return

    viewpoints = cfg.get("vision", {}).get("viewpoints", [])
    if not viewpoints:
        print("WARN config vision.viewpoints is empty; NBV search cannot run on hardware until calibration step 5 is completed.")

    joint_limits_min = cfg.get("arm", {}).get("joint_limits_min", [])
    joint_limits_max = cfg.get("arm", {}).get("joint_limits_max", [])
    if joint_limits_min and joint_limits_max:
        try:
            flat = [float(v) for v in joint_limits_min] + [float(v) for v in joint_limits_max]
            if all(abs(v) < 1e-9 for v in flat):
                print("WARN config arm joint limits are still all zeros; wrist-offset sampling and arm safety bounds are not calibrated.")
        except Exception:
            print("WARN config arm joint limits could not be parsed.")

    transform = cfg.get("camera", {}).get("T_robot_camera", [])
    identity = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    if list(transform) == identity:
        print("WARN config camera T_robot_camera is still identity; 3D localisation is using placeholder extrinsics.")

    if bool(cfg.get("demo_mode", False)):
        print("WARN config demo_mode is enabled; biometric and safety behavior is intentionally downgraded.")


def main() -> int:
    failed = False

    for command in REQUIRED_COMMANDS:
        path = shutil.which(command)
        if path:
            print(f"OK command {command}: {path}")
        else:
            failed = True
            print(f"FAIL command {command}: not found")

    for module_name in REQUIRED_MODULES:
        try:
            importlib.import_module(module_name)
            print(f"OK module {module_name}")
        except Exception as exc:
            failed = True
            print(f"FAIL module {module_name}: {type(exc).__name__}: {exc}")

    _warn_config_gaps()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

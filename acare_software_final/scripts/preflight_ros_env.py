from __future__ import annotations

import importlib
import shutil
import sys


REQUIRED_COMMANDS = ["ros2", "colcon"]
REQUIRED_MODULES = [
    "rclpy",
    "pydantic",
    "numpy",
    "yaml",
    "deepgram",
    "sounddevice",
    "speechbrain",
    "mediapipe",
    "onnxruntime",
    "cv2",
]


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

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

"""ACARE Voice System — standalone (non-ROS) entry point.

Used for live mic testing and developer iteration on the voice pipeline
without bringing up the full ROS graph. The deployed graph entry point is
``acare_voice.voice_ros_node:main``.
"""

import sys
import time

# C3 fix: the package is `acare_voice`, not `voice`. The previous
# `from voice.voice_node import …` line would fail under both `python -m
# acare_voice.main` and `ros2 run`.
from .voice_node import VoiceNode, main  # noqa: F401  (re-export)


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        # If terminal closes stdin, just wait indefinitely so logic threads
        # can keep running (useful when the dev harness is detached).
        print("[System] Terminal input detached. Voice node remains active...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[System] Shutdown requested.")
        sys.exit(0)

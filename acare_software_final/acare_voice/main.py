"""
ACARE Voice System — Standalone Entry Point (no ROS2)
Run from this directory: python main.py
"""
import time
import sys
import os

# Set up package so relative imports work when running standalone.
# This makes Python treat acare_voice/ as a package even without colcon.
_dir = os.path.dirname(os.path.abspath(__file__))
_parent = os.path.dirname(_dir)
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from acare_voice.voice_node import VoiceNode, main

if __name__ == "__main__":
    try:
        main()
    except EOFError:
        print("[System] Terminal input detached. System remaining active in background...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[System] Shutdown requested.")
            sys.exit(0)
    except KeyboardInterrupt:
        print("\n[System] Shutdown requested.")
        sys.exit(0)
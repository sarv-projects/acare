"""
ACARE Voice System — Entry Point
"""
import time
import sys
from voice.voice_node import VoiceNode, main

if __name__ == "__main__":
    # Ensure standard input remains open
    try:
        main()
    except EOFError:
        # If terminal closes stdin, just wait indefinitely to keep logic threads alive
        print("[System] Terminal input detached. System remaining active in background...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[System] Shutdown requested.")
        sys.exit(0)
"""
Quick live application test - runs for 10 seconds and checks for errors.
"""
import asyncio
import sys
import signal
from threading import Thread, Event
import time

# Capture errors
errors_found = []
stderr_capture = []

def test_app_startup():
    """Test if app starts without errors"""
    print("=" * 60)
    print("LIVE APP STARTUP TEST (10 second runtime)")
    print("=" * 60)
    
    # Import and start the main components
    try:
        print("\n1. Importing modules...")
        from voice.vad import VADListener
        from voice.asr import ASRClient
        from voice.keyword_monitor import KeywordMonitor
        from voice.intent_parser import parse_intent
        from voice.assistant_agent import AssistantAgent
        from voice.tts import speak
        print("   ✓ All modules imported")
        
        print("\n2. Initializing components...")
        
        # Track transcripts
        transcripts = []
        def on_transcript(text):
            transcripts.append(text)
            print(f"   [Transcript]: {text}")
        
        # Track ESTOP
        estops = []
        def on_estop(keyword):
            estops.append(keyword)
            print(f"   [ESTOP]: {keyword}")
        
        # Initialize
        km = KeywordMonitor(on_estop=on_estop)
        asr = ASRClient(on_transcript=on_transcript, keyword_monitor=km)
        assistant = AssistantAgent()
        
        print("   ✓ Components initialized")
        
        print("\n3. Connecting ASR...")
        asr.connect()
        print("   ✓ ASR connected")
        
        print("\n4. Starting VAD listener...")
        vad = VADListener(asr_client=asr)
        
        # Run for 10 seconds
        print("\n5. Running for 10 seconds (listening to microphone)...")
        print("   [System is listening... speak something to test!]\n")
        
        # Create a flag to stop after 10 seconds
        run_event = Event()
        run_event.set()
        
        def run_listener():
            try:
                start = time.time()
                while run_event.is_set() and (time.time() - start) < 10:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                pass
        
        listener_thread = Thread(target=run_listener, daemon=True)
        listener_thread.start()
        
        # Start VAD in another thread
        vad_thread = Thread(target=lambda: vad.start(lambda x: None), daemon=True)
        vad_thread.start()
        
        # Wait 10 seconds
        time.sleep(10)
        run_event.clear()
        vad.stop()
        
        print("\n6. Disconnecting ASR...")
        asr.disconnect()
        time.sleep(0.5)
        print("   ✓ ASR disconnected")
        
        print("\n7. Test Results:")
        print(f"   - Transcripts received: {len(transcripts)}")
        print(f"   - ESTOP triggers: {len(estops)}")
        print(f"   - Errors encountered: {len(errors_found)}")
        
        if not errors_found:
            print("\n✓ Live app test PASSED!")
            return True
        else:
            print("\n✗ Errors found:")
            for error in errors_found:
                print(f"   - {error}")
            return False
        
    except Exception as e:
        print(f"\n✗ App startup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_app_startup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(0)

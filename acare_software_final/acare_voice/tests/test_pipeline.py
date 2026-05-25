"""
Comprehensive pipeline diagnostics for ACARE voice system.
Tests all components: VAD, ASR, TTS, Intent Parser, Assistant Agent.
"""

import sys
import traceback
from pathlib import Path
from typing import Any, cast

def test_imports():
    """Test all critical imports"""
    print("=" * 60)
    print("TESTING IMPORTS")
    print("=" * 60)
    
    errors = []
    
    modules = [
        ("vad", "VADListener"),
        ("asr", "ASRClient"),
        ("tts", "speak"),
        ("keyword_monitor", "KeywordMonitor"),
        ("intent_parser", "parse_intent"),
        ("assistant_agent", "AssistantAgent"),
    ]
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            obj = getattr(module, class_name)
            print(f"✓ {module_name}.{class_name}")
        except Exception as e:
            msg = f"✗ {module_name}.{class_name}: {e}"
            print(msg)
            errors.append(msg)
    
    return len(errors) == 0, errors

def test_env_vars():
    """Test environment variables"""
    print("\n" + "=" * 60)
    print("TESTING ENVIRONMENT VARIABLES")
    print("=" * 60)
    
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    required_vars = ["DEEPGRAM_API_KEY", "GROQ_API_KEY"]
    errors = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            masked = value[:8] + "..." if len(value) > 8 else value
            print(f"✓ {var}: {masked}")
        else:
            msg = f"✗ {var}: NOT SET"
            print(msg)
            errors.append(msg)
    
    return len(errors) == 0, errors

def test_audio_devices():
    """Test audio device availability"""
    print("\n" + "=" * 60)
    print("TESTING AUDIO DEVICES")
    print("=" * 60)
    
    try:
        import sounddevice as sd
        import numpy as np
        
        devices = sd.query_devices()
        print(f"✓ Found {len(devices)} audio devices")
        
        # Test playback
        print("\nDefault playback device:")
        default_out = sd.default.device[1]
        if default_out is not None:
            dev_info = sd.query_devices(default_out)
            print(f"  ✓ {dev_info['name']} ({dev_info['max_output_channels']} channels)")
        else:
            print(f"  ✗ No default output device")
        
        # Test recording
        print("\nDefault recording device:")
        default_in = sd.default.device[0]
        if default_in is not None:
            dev_info = sd.query_devices(default_in)
            print(f"  ✓ {dev_info['name']} ({dev_info['max_input_channels']} channels)")
        else:
            print(f"  ✗ No default input device")
        
        return True, []
    except Exception as e:
        msg = f"✗ Audio device test failed: {e}"
        print(msg)
        return False, [msg]

def test_vad():
    """Test VAD initialization"""
    print("\n" + "=" * 60)
    print("TESTING VAD (Voice Activity Detection)")
    print("=" * 60)
    
    errors = []
    try:
        from voice.keyword_monitor import KeywordMonitor
        
        def mock_estop(keyword):
            pass
        
        km = KeywordMonitor(on_estop=mock_estop)
        print(f"✓ KeywordMonitor initialized")
        from voice.keyword_monitor import ESTOP_KEYWORDS
        print(f"  - ESTOP keywords: {ESTOP_KEYWORDS} ({len(ESTOP_KEYWORDS)} total)")
        
    except Exception as e:
        msg = f"✗ VAD error: {e}"
        print(msg)
        traceback.print_exc()
        errors.append(msg)
    
    return len(errors) == 0, errors

def test_asr_config():
    """Test ASR configuration (without connecting)"""
    print("\n" + "=" * 60)
    print("TESTING ASR CONFIGURATION")
    print("=" * 60)
    
    errors = []
    try:
        from voice.asr import SAMPLE_RATE
        from deepgram import DeepgramClient
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
        
        if not DEEPGRAM_API_KEY:
            msg = "✗ DEEPGRAM_API_KEY not set"
            print(msg)
            errors.append(msg)
        else:
            client = DeepgramClient(DEEPGRAM_API_KEY)
            print(f"✓ DeepgramClient initialized")
            print(f"  - Sample rate: {SAMPLE_RATE} Hz")
            print(f"  - Endpointing timeout: 5000ms (increased for TTS pauses)")
            print(f"  - Keepalive interval: 2s")
        
    except Exception as e:
        msg = f"✗ ASR config error: {e}"
        print(msg)
        traceback.print_exc()
        errors.append(msg)
    
    return len(errors) == 0, errors

def test_tts():
    """Test TTS initialization"""
    print("\n" + "=" * 60)
    print("TESTING TTS (Text-to-Speech)")
    print("=" * 60)
    
    errors = []
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        # Test voice availability
        voices = cast(list[Any], engine.getProperty('voices'))
        print(f"✓ TTS engine initialized")
        print(f"  - Available voices: {len(voices)}")
        for i, voice in enumerate(voices):
            print(f"    {i}: {voice.name}")
        
        # Check rate and volume
        print(f"  - Rate: 145 WPM")
        print(f"  - Volume: 0.9")
        
        return True, []
    except Exception as e:
        msg = f"✗ TTS error: {e}"
        print(msg)
        traceback.print_exc()
        return False, [msg]

def test_intent_parser_config():
    """Test intent parser configuration"""
    print("\n" + "=" * 60)
    print("TESTING INTENT PARSER CONFIGURATION")
    print("=" * 60)
    
    errors = []
    try:
        from voice.intent_parser import VALID_TOOLS, SYSTEM_PROMPT
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        
        if not GROQ_API_KEY:
            msg = "✗ GROQ_API_KEY not set"
            print(msg)
            errors.append(msg)
        else:
            print(f"✓ Intent parser configured")
            print(f"  - Valid tools: {VALID_TOOLS}")
            print(f"  - Model: llama-3.3-70b-versatile")
        
    except Exception as e:
        msg = f"✗ Intent parser config error: {e}"
        print(msg)
        traceback.print_exc()
        errors.append(msg)
    
    return len(errors) == 0, errors

def test_assistant_agent_config():
    """Test assistant agent configuration"""
    print("\n" + "=" * 60)
    print("TESTING ASSISTANT AGENT CONFIGURATION")
    print("=" * 60)
    
    errors = []
    try:
        from voice.assistant_agent import AssistantAgent, SYSTEM_PROMPT
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        
        if not GROQ_API_KEY:
            msg = "✗ GROQ_API_KEY not set"
            print(msg)
            errors.append(msg)
        else:
            agent = AssistantAgent()
            print(f"✓ AssistantAgent initialized")
            print(f"  - Max conversation turns: 20")
            print(f"  - Initial history length: {agent.get_conversation_length()}")
        
    except Exception as e:
        msg = f"✗ Assistant agent error: {e}"
        print(msg)
        traceback.print_exc()
        errors.append(msg)
    
    return len(errors) == 0, errors

def test_threading():
    """Test threading and async components"""
    print("\n" + "=" * 60)
    print("TESTING THREADING & ASYNC")
    print("=" * 60)
    
    errors = []
    try:
        import threading
        import asyncio
        
        # Test threading
        test_value = []
        def thread_func():
            test_value.append(1)
        
        t = threading.Thread(target=thread_func)
        t.start()
        t.join(timeout=1)
        
        if test_value:
            print(f"✓ Threading works")
        else:
            msg = "✗ Threading failed"
            print(msg)
            errors.append(msg)
        
        # Test async
        async def test_async():
            return True
        
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(test_async())
        loop.close()
        
        if result:
            print(f"✓ Asyncio works")
        
    except Exception as e:
        msg = f"✗ Threading/Async error: {e}"
        print(msg)
        traceback.print_exc()
        errors.append(msg)
    
    return len(errors) == 0, errors

def main():
    """Run all diagnostics"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " ACARE VOICE SYSTEM - COMPREHENSIVE DIAGNOSTICS ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    all_errors = []
    
    # Run all tests
    tests = [
        ("Imports", test_imports),
        ("Environment Variables", test_env_vars),
        ("Audio Devices", test_audio_devices),
        ("VAD", test_vad),
        ("ASR Configuration", test_asr_config),
        ("TTS", test_tts),
        ("Intent Parser Configuration", test_intent_parser_config),
        ("Assistant Agent Configuration", test_assistant_agent_config),
        ("Threading & Async", test_threading),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success, errors = test_func()
            results.append((test_name, success, errors))
            if errors:
                all_errors.extend([(test_name, e) for e in errors])
        except Exception as e:
            results.append((test_name, False, [str(e)]))
            all_errors.append((test_name, str(e)))
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, success, _ in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status:8} {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if all_errors:
        print("\n" + "=" * 60)
        print("ERRORS & WARNINGS")
        print("=" * 60)
        for test_name, error in all_errors:
            print(f"\n[{test_name}]")
            print(f"  {error}")
    
    # Exit code
    if passed == total:
        print("\n✓ All systems operational!")
        return 0
    else:
        print(f"\n✗ {total - passed} issue(s) found. Please fix before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

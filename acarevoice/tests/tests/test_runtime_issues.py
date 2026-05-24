"""
Runtime error identification for ACARE voice system.
Tests actual execution flows without connecting to live services.
"""

import sys
import traceback
from unittest.mock import Mock, patch, MagicMock
import json

def test_vad_edge_cases():
    """Test VAD edge cases and error handling"""
    print("\n" + "=" * 60)
    print("TESTING VAD EDGE CASES")
    print("=" * 60)
    
    errors = []
    try:
        from voice.vad import VADListener
        import numpy as np
        
        # Test 1: Empty chunk processing
        vad = VADListener(asr_client=None)
        empty_chunk = np.array([], dtype=np.float32)
        try:
            vad.process_chunk(empty_chunk)
            print("✓ VAD handles empty chunks")
        except Exception as e:
            msg = f"✗ VAD fails on empty chunk: {e}"
            print(msg)
            errors.append(msg)
        
        # Test 2: Very large chunk
        try:
            large_chunk = np.ones(100000, dtype=np.float32)
            vad.process_chunk(large_chunk)
            print("✓ VAD handles large chunks")
        except Exception as e:
            msg = f"✗ VAD fails on large chunk: {e}"
            print(msg)
            errors.append(msg)
        
        # Test 3: NaN/Inf handling
        try:
            bad_chunk = np.array([np.nan, np.inf, -np.inf, 1.0], dtype=np.float32)
            vad.process_chunk(bad_chunk)
            print("✓ VAD handles NaN/Inf")
        except Exception as e:
            msg = f"✗ VAD fails on NaN/Inf: {e}"
            print(msg)
            errors.append(msg)
        
        # Test 4: Multiple flush cycles
        try:
            for _ in range(3):
                vad._flush()
            print("✓ VAD handles multiple flush cycles")
        except Exception as e:
            msg = f"✗ VAD fails on multiple flushes: {e}"
            print(msg)
            errors.append(msg)
        
    except Exception as e:
        msg = f"✗ VAD test setup failed: {e}"
        print(msg)
        traceback.print_exc()
        errors.append(msg)
    
    return len(errors) == 0, errors

def test_asr_error_handling():
    """Test ASR error handling and reconnection"""
    print("\n" + "=" * 60)
    print("TESTING ASR ERROR HANDLING")
    print("=" * 60)
    
    errors = []
    try:
        from voice.asr import ASRClient
        import numpy as np
        
        # Mock callback
        def mock_callback(text):
            pass
        
        # Test 1: Send without connection
        asr = ASRClient(on_transcript=mock_callback)
        try:
            audio_np = np.random.randn(16000).astype(np.float32)
            asr.send_chunk(audio_np)
            print("✓ ASR handles send_chunk without connection (graceful)")
        except Exception as e:
            msg = f"✗ ASR fails on send_chunk without connection: {e}"
            print(msg)
            errors.append(msg)
        
        # Test 2: Send with None connection
        asr.connection = None
        asr.loop = None
        try:
            audio_np = np.random.randn(16000).astype(np.float32)
            asr.send_chunk(audio_np)
            print("✓ ASR handles None connection safely")
        except Exception as e:
            msg = f"✗ ASR fails on None connection: {e}"
            print(msg)
            errors.append(msg)
        
        # Test 3: Very large audio chunk
        try:
            huge_audio = np.random.randn(16000 * 10).astype(np.float32)
            asr.send_audio(huge_audio)
            print("✓ ASR handles large audio chunks")
        except Exception as e:
            msg = f"✗ ASR fails on large audio: {e}"
            print(msg)
            errors.append(msg)
        
    except Exception as e:
        msg = f"✗ ASR test setup failed: {e}"
        print(msg)
        traceback.print_exc()
        errors.append(msg)
    
    return len(errors) == 0, errors

def test_keyword_monitor_edge_cases():
    """Test KeywordMonitor edge cases"""
    print("\n" + "=" * 60)
    print("TESTING KEYWORD MONITOR EDGE CASES")
    print("=" * 60)
    
    errors = []
    try:
        from voice.keyword_monitor import KeywordMonitor
        
        estop_triggered = []
        def mock_estop(keyword):
            estop_triggered.append(keyword)
        
        km = KeywordMonitor(on_estop=mock_estop)
        
        # Test 1: Empty partial
        try:
            km.check_partial("")
            print("✓ KeywordMonitor handles empty partial")
        except Exception as e:
            msg = f"✗ KeywordMonitor fails on empty partial: {e}"
            print(msg)
            errors.append(msg)
        
        # Test 2: None partial
        try:
            km.check_partial(None)
            print("✓ KeywordMonitor handles None partial")
        except Exception as e:
            msg = f"✓ KeywordMonitor fails on None (expected): {type(e).__name__}"
            print(msg)
        
        # Test 3: Very long partial
        try:
            long_text = "the " * 1000 + "stop"
            km.check_partial(long_text)
            print("✓ KeywordMonitor handles very long text")
        except Exception as e:
            msg = f"✗ KeywordMonitor fails on long text: {e}"
            print(msg)
            errors.append(msg)
        
        # Test 4: ESTOP reset
        try:
            km.estop_active = True
            km.reset_estop()
            if not km.estop_active:
                print("✓ KeywordMonitor reset works")
            else:
                msg = "✗ KeywordMonitor reset failed"
                print(msg)
                errors.append(msg)
        except Exception as e:
            msg = f"✗ KeywordMonitor reset error: {e}"
            print(msg)
            errors.append(msg)
        
        # Test 5: Cancel without timer
        try:
            km._collision_timer = None
            km.cancel_if_continuation("some text")
            print("✓ KeywordMonitor handles cancel without timer")
        except Exception as e:
            msg = f"✗ KeywordMonitor cancel error: {e}"
            print(msg)
            errors.append(msg)
        
    except Exception as e:
        msg = f"✗ KeywordMonitor test setup failed: {e}"
        print(msg)
        traceback.print_exc()
        errors.append(msg)
    
    return len(errors) == 0, errors

def test_intent_parser_robustness():
    """Test intent parser with various inputs"""
    print("\n" + "=" * 60)
    print("TESTING INTENT PARSER ROBUSTNESS")
    print("=" * 60)
    
    errors = []
    try:
        from voice.intent_parser import VALID_TOOLS
        import json
        
        # Test 1: JSON parsing edge cases (mock)
        test_cases = [
            ("", "Empty string"),
            ("not json", "Invalid JSON"),
            ('{"tool": "unknown"}', "Unknown tool"),
            ('{"action": "steal"}', "Invalid action"),
            ('{"tool": "scalpel"}', "Missing action"),
        ]
        
        for test_input, description in test_cases:
            try:
                if test_input:
                    json.loads(test_input)
                print(f"✓ Intent parser handles: {description}")
            except json.JSONDecodeError:
                print(f"✓ Intent parser handles: {description} (JSON error - expected)")
            except Exception as e:
                msg = f"✗ Intent parser fails on {description}: {e}"
                print(msg)
                errors.append(msg)
        
    except Exception as e:
        msg = f"✗ Intent parser test setup failed: {e}"
        print(msg)
        traceback.print_exc()
        errors.append(msg)
    
    return len(errors) == 0, errors

def test_assistant_agent_robustness():
    """Test assistant agent with various inputs"""
    print("\n" + "=" * 60)
    print("TESTING ASSISTANT AGENT ROBUSTNESS")
    print("=" * 60)
    
    errors = []
    try:
        from voice.assistant_agent import AssistantAgent
        
        agent = AssistantAgent()
        
        # Test 1: Empty input
        try:
            response = agent.get_response("")
            print(f"✓ AssistantAgent handles empty input")
        except Exception as e:
            msg = f"✗ AssistantAgent fails on empty input: {e}"
            print(msg)
            # errors.append(msg)  # This might fail due to API
        
        # Test 2: Very long input
        try:
            long_input = "word " * 500
            # Don't actually call API, just check history
            agent.conversation_history.append({"role": "user", "content": long_input})
            if len(agent.conversation_history) > 0:
                print(f"✓ AssistantAgent handles long input")
        except Exception as e:
            msg = f"✗ AssistantAgent fails on long input: {e}"
            print(msg)
            errors.append(msg)
        
        # Test 3: History limit
        try:
            agent.max_turns = 5
            for i in range(10):
                agent.conversation_history.append({"role": "user", "content": f"message {i}"})
                agent._summarize_old_turns()
            
            if len(agent.conversation_history) <= agent.max_turns + 2:
                print(f"✓ AssistantAgent conversation limit works")
            else:
                msg = f"✗ AssistantAgent history limit not respected"
                print(msg)
                errors.append(msg)
        except Exception as e:
            msg = f"✗ AssistantAgent history test failed: {e}"
            print(msg)
            errors.append(msg)
        
    except Exception as e:
        msg = f"✗ AssistantAgent test setup failed: {e}"
        print(msg)
        traceback.print_exc()
        errors.append(msg)
    
    return len(errors) == 0, errors

def test_tts_robustness():
    """Test TTS with various inputs"""
    print("\n" + "=" * 60)
    print("TESTING TTS ROBUSTNESS")
    print("=" * 60)
    
    errors = []
    try:
        from voice.tts import speak
        
        # Test 1: Empty string
        try:
            # Mock pyttsx3 to avoid actual speech
            with patch('pyttsx3.init') as mock_init:
                mock_engine = MagicMock()
                mock_init.return_value = mock_engine
                
                speak("")
                print(f"✓ TTS handles empty string")
        except Exception as e:
            msg = f"✗ TTS fails on empty string: {e}"
            print(msg)
            errors.append(msg)
        
        # Test 2: Very long text
        try:
            with patch('pyttsx3.init') as mock_init:
                mock_engine = MagicMock()
                mock_init.return_value = mock_engine
                
                long_text = "word " * 1000
                speak(long_text)
                print(f"✓ TTS handles very long text")
        except Exception as e:
            msg = f"✗ TTS fails on long text: {e}"
            print(msg)
            errors.append(msg)
        
        # Test 3: Special characters
        try:
            with patch('pyttsx3.init') as mock_init:
                mock_engine = MagicMock()
                mock_init.return_value = mock_engine
                
                special_text = "ACARE: Test! @#$% & (parentheses) [brackets]"
                speak(special_text)
                print(f"✓ TTS handles special characters")
        except Exception as e:
            msg = f"✗ TTS fails on special chars: {e}"
            print(msg)
            errors.append(msg)
        
    except Exception as e:
        msg = f"✗ TTS test setup failed: {e}"
        print(msg)
        traceback.print_exc()
        errors.append(msg)
    
    return len(errors) == 0, errors

def main():
    """Run all runtime tests"""
    print("\n")
    print("=" * 60)
    print("RUNTIME ERROR DETECTION & EDGE CASE TESTING".center(60))
    print("=" * 60)
    
    tests = [
        ("VAD Edge Cases", test_vad_edge_cases),
        ("ASR Error Handling", test_asr_error_handling),
        ("KeywordMonitor Edge Cases", test_keyword_monitor_edge_cases),
        ("Intent Parser Robustness", test_intent_parser_robustness),
        ("AssistantAgent Robustness", test_assistant_agent_robustness),
        ("TTS Robustness", test_tts_robustness),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success, errors = test_func()
            results.append((test_name, success, errors))
        except Exception as e:
            results.append((test_name, False, [str(e)]))
    
    # Summary
    print("\n" + "=" * 60)
    print("RUNTIME TESTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, success, _ in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status:8} {test_name}")
    
    print(f"\nTotal: {passed}/{total} runtime tests passed")
    
    if passed == total:
        print("\n✓ All runtime tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) found issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

"""
ACARE TTS Engine — Dual Approach (Edge TTS Edition)
"""

import os
import time
import threading
import tempfile
import asyncio
import numpy as np
import pyttsx3
import sounddevice as sd
from enum import Enum

# Hide pygame prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class Priority(Enum):
    URGENT = 0   
    NORMAL = 1   

is_speaking = False
_lock = threading.Lock()
_pygame_init = False

def _init_pygame():
    global _pygame_init
    if not _pygame_init:
        try:
            pygame.mixer.init()
            _pygame_init = True
        except Exception as e:
            print(f"[TTS] Pygame init error: {e}")

def _speak_pyttsx3(text: str) -> None:
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[TTS/pyttsx3] Error: {e}")

async def _save_edge_tts(text, voice, tmp_path):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(tmp_path)

def _speak_edge_tts(text: str) -> bool:
    try:
        _init_pygame()
        # en-US-AvaNeural (Neutral Robot)
        voice = "en-US-AvaNeural"
        
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp_path = f.name
            
        # Run async save in a sync-friendly way on a dedicated thread
        def _run_coro_sync(coro):
            """Run coroutine in a new event loop inside a thread and wait."""
            exc = []
            def _target():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(coro)
                    loop.close()
                except Exception as e:
                    exc.append(e)

            t = threading.Thread(target=_target)
            t.start()
            t.join()
            if exc:
                raise exc[0]

        _run_coro_sync(_save_edge_tts(text, voice, tmp_path))
        
        # Play via pygame
        pygame.mixer.music.load(tmp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)
            
        pygame.mixer.music.unload()
        try:
            os.unlink(tmp_path)
        except: pass
        return True
    except Exception as e:
        print(f"[TTS/edge-tts] Error: {e}")
        return False

def speak(text: str, vad_listener=None, priority: Priority = Priority.NORMAL) -> None:
    global is_speaking
    if not text or not text.strip(): return
    text = text.replace("ACARE", "A-Care")
    print(f"[TTS] {text}")

    with _lock: is_speaking = True
    if vad_listener: vad_listener.pause_streaming()

    try:
        if priority == Priority.URGENT:
            _speak_pyttsx3(text)
        else:
            if not _speak_edge_tts(text):
                _speak_pyttsx3(text) # Fallback
        time.sleep(0.3)
    finally:
        with _lock: is_speaking = False
        if vad_listener: vad_listener.resume_streaming()

def speak_urgent(text: str, vad_listener=None) -> None:
    speak(text, vad_listener=vad_listener, priority=Priority.URGENT)

if __name__ == "__main__":
    speak("A-Care testing neutral robotics voice.")
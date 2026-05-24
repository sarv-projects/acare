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
import soundfile as sf
from enum import Enum

class Priority(Enum):
    URGENT = 0   
    NORMAL = 1   

is_speaking = False
_lock = threading.Lock()

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

_tts_loop = None
_tts_loop_ready = threading.Event()

def _get_tts_loop():
    global _tts_loop
    if _tts_loop is None:
        def _run_loop():
            global _tts_loop
            _tts_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(_tts_loop)
            _tts_loop_ready.set()
            _tts_loop.run_forever()
        t = threading.Thread(target=_run_loop, daemon=True)
        t.start()
        _tts_loop_ready.wait()
    return _tts_loop

def _speak_edge_tts(text: str) -> bool:
    try:
        voice = "en-US-AvaNeural"

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp_path = f.name

        loop = _get_tts_loop()
        future = asyncio.run_coroutine_threadsafe(_save_edge_tts(text, voice, tmp_path), loop)
        future.result()

        audio, sr = sf.read(tmp_path, dtype="float32")
        sd.play(audio, sr)
        sd.wait()

        try:
            os.unlink(tmp_path)
        except: pass
        return True
    except Exception as e:
        print(f"[TTS/edge-tts] Error: {e}")
        return False

def _speak_sync(text: str, vad_listener=None, priority: Priority = Priority.NORMAL) -> None:
    global is_speaking
    with _lock: is_speaking = True
    if vad_listener: vad_listener.pause_streaming()
    try:
        if priority == Priority.URGENT:
            _speak_pyttsx3(text)
        else:
            if not _speak_edge_tts(text):
                _speak_pyttsx3(text)
        time.sleep(1.5)
    finally:
        with _lock: is_speaking = False
        if vad_listener: vad_listener.resume_streaming()

def speak(text: str, vad_listener=None, priority: Priority = Priority.NORMAL) -> None:
    if not text or not text.strip(): return
    text = text.replace("ACARE", "A-Care")
    print(f"[TTS] {text}")
    t = threading.Thread(target=_speak_sync, args=(text, vad_listener, priority), daemon=True)
    t.start()

def speak_urgent(text: str, vad_listener=None) -> None:
    speak(text, vad_listener=vad_listener, priority=Priority.URGENT)

if __name__ == "__main__":
    speak("A-Care testing neutral robotics voice.")
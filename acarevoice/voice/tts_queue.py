import os
import time
import threading
import queue
import tempfile
import asyncio
import numpy as np
import sounddevice as sd
from enum import Enum
from typing import Optional, Callable, List

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class Priority(Enum):
    URGENT = 0
    NORMAL = 1
    BACKCHANNEL = 2


class TTSQueue:

    def __init__(self, vad_listener=None):
        self.vad_listener = vad_listener
        self._queue = queue.PriorityQueue()
        self._current_item = None
        self._is_speaking = False
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._barge_in_triggered = threading.Event()
        self._tts_active = threading.Event()
        self._last_utterance = ""
        self._last_utterance_time = 0.0
        self._min_repeat_interval = 5.0

        self._tts_rms_history: List[float] = []
        self._echo_threshold = 0.15

        self._pygame_init = False
        self._init_pygame()

        self._tts_loop = None
        self._tts_loop_ready = threading.Event()

        self._processor_thread = threading.Thread(target=self._process_queue, daemon=True)
        self._processor_thread.start()

        self._barge_thread = threading.Thread(target=self._monitor_barge_in, daemon=True)
        self._barge_thread.start()

    def _init_pygame(self):
        if not self._pygame_init:
            try:
                pygame.mixer.init()
                self._pygame_init = True
            except Exception as e:
                print(f"[TTSQueue] Pygame init error: {e}")

    def _get_tts_loop(self):
        if self._tts_loop is None:
            def _run_loop():
                self._tts_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._tts_loop)
                self._tts_loop_ready.set()
                self._tts_loop.run_forever()
            t = threading.Thread(target=_run_loop, daemon=True)
            t.start()
            self._tts_loop_ready.wait()
        return self._tts_loop

    async def _save_edge_tts(self, text, voice, tmp_path):
        import edge_tts
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(tmp_path)

    def _speak_pyttsx3(self, text: str) -> None:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", 160)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"[TTSQueue/pyttsx3] Error: {e}")

    def _speak_edge_tts(self, text: str) -> bool:
        try:
            voice = "en-US-AvaNeural"
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                tmp_path = f.name

            loop = self._get_tts_loop()
            future = asyncio.run_coroutine_threadsafe(
                self._save_edge_tts(text, voice, tmp_path), loop
            )
            future.result(timeout=10)

            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()

            self._tts_active.set()
            start_time = time.time()

            while pygame.mixer.music.get_busy():
                if self._barge_in_triggered.is_set():
                    pygame.mixer.music.stop()
                    self._barge_in_triggered.clear()
                    print("[TTSQueue] Barge-in detected, stopping TTS")
                    break
                time.sleep(0.02)

            duration = time.time() - start_time
            self._tts_active.clear()

            pygame.mixer.music.unload()
            try:
                os.unlink(tmp_path)
            except:
                pass
            return True

        except Exception as e:
            print(f"[TTSQueue/edge-tts] Error: {e}")
            self._tts_active.clear()
            return False

    def _process_queue(self):
        while not self._stop_event.is_set():
            try:
                priority, seq, text, use_pyttsx3 = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            with self._lock:
                if self._barge_in_triggered.is_set():
                    self._barge_in_triggered.clear()
                    if priority > Priority.URGENT.value:
                        print(f"[TTSQueue] Skipping due to barge-in: {text[:50]}")
                        self._queue.task_done()
                        continue

                self._current_item = (priority, text)
                self._is_speaking = True

            if self.vad_listener:
                self.vad_listener.pause_streaming()

            try:
                print(f"[TTS] {text}")

                if use_pyttsx3 or priority == Priority.URGENT.value:
                    self._speak_pyttsx3(text)
                else:
                    if not self._speak_edge_tts(text):
                        self._speak_pyttsx3(text)

                if priority > Priority.URGENT.value:
                    time.sleep(0.6)

            finally:
                with self._lock:
                    self._is_speaking = False
                    self._current_item = None

                if self.vad_listener:
                    self.vad_listener.resume_streaming()

                self._queue.task_done()

    def _monitor_barge_in(self):
        while not self._stop_event.is_set():
            time.sleep(0.1)

    def speak(self, text: str, priority: Priority = Priority.NORMAL,
              use_pyttsx3: bool = False, allow_repeat: bool = False) -> None:
        if not text or not text.strip():
            return

        text = text.strip().replace("ACARE", "A-Care")

        now = time.time()
        if not allow_repeat and text == self._last_utterance:
            if (now - self._last_utterance_time) < self._min_repeat_interval:
                print(f"[TTSQueue] Suppressing duplicate: {text[:50]}")
                return

        self._last_utterance = text
        self._last_utterance_time = now

        if priority == Priority.URGENT:
            self._clear_queue()
            self.trigger_barge_in()

        if priority == Priority.BACKCHANNEL and self.is_speaking:
            return

        seq = int(time.time() * 1000)
        self._queue.put((priority.value, seq, text, use_pyttsx3))

    def speak_urgent(self, text: str) -> None:
        self.speak(text, priority=Priority.URGENT, use_pyttsx3=True)

    def speak_backchannel(self, text: str) -> None:
        self.speak(text, priority=Priority.BACKCHANNEL)

    def trigger_barge_in(self):
        self._barge_in_triggered.set()
        try:
            pygame.mixer.music.stop()
        except:
            pass

    def _clear_queue(self):
        try:
            while True:
                self._queue.get_nowait()
                self._queue.task_done()
        except queue.Empty:
            pass

    @property
    def is_speaking(self) -> bool:
        with self._lock:
            return self._is_speaking

    @property
    def is_tts_active(self) -> bool:
        return self._tts_active.is_set()

    def stop(self):
        self._stop_event.set()
        self.trigger_barge_in()
        self._clear_queue()
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass

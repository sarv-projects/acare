import os
import hashlib
import tempfile
import asyncio
import threading
from typing import Dict, Optional
from collections import OrderedDict
import numpy as np

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class TTSCache:

    def __init__(self, capacity: int = 50, preload: bool = True):
        self.capacity = capacity
        self._cache: OrderedDict[str, str] = OrderedDict()
        self._lock = threading.RLock()
        self._tts_loop = None
        self._tts_loop_ready = threading.Event()

        self.COMMON_PHRASES = [
            "Processing.",
            "I didn't catch that. Could you say it again?",
            "One at a time. Which first?",
            "Authentication required before I can fetch tools.",
            "Did you mean the scalpel? Say yes to confirm.",
            "Did you mean the scissors? Say yes to confirm.",
            "Did you mean the forceps? Say yes to confirm.",
            "Did you mean the bandage? Say yes to confirm.",
            "Did you mean the gauze? Say yes to confirm.",
            "Did you mean the thermometer? Say yes to confirm.",
            "Did you mean the oximeter? Say yes to confirm.",
            "Did you mean the plaster? Say yes to confirm.",
            "Cancelled.",
            "System resumed. Ready for commands.",
            "Emergency stop. Keyword detected: stop.",
            "I'm listening.",
            "Logged out. A-Care standing by.",
            "Logged in. How can I assist?",
            "Cannot log out during active task.",
            "Nothing to confirm right now.",
            "Alright, what would you like instead?",
            "I'll wait for your command.",
        ]

        if preload:
            self._init_tts_loop()
            self._prewarm_cache()

    def _init_tts_loop(self):
        def _run_loop():
            self._tts_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._tts_loop)
            self._tts_loop_ready.set()
            self._tts_loop.run_forever()
        t = threading.Thread(target=_run_loop, daemon=True)
        t.start()
        self._tts_loop_ready.wait()

    def _get_text_hash(self, text: str) -> str:
        return hashlib.md5(text.lower().strip().encode()).hexdigest()[:12]

    def _prewarm_cache(self):
        print("[TTSCache] Prewarming cache...")
        for phrase in self.COMMON_PHRASES:
            if len(self._cache) >= self.capacity:
                break
            self._generate_and_cache(phrase)
        print(f"[TTSCache] Cache prewarmed with {len(self._cache)} phrases")

    def _generate_and_cache(self, text: str) -> Optional[str]:
        try:
            import edge_tts
            voice = "en-US-AvaNeural"

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                tmp_path = f.name

            async def _save():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(tmp_path)

            if self._tts_loop:
                future = asyncio.run_coroutine_threadsafe(_save(), self._tts_loop)
                future.result(timeout=15)
            else:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(_save())
                loop.close()

            key = self._get_text_hash(text)
            with self._lock:
                if key in self._cache:
                    del self._cache[key]
                self._cache[key] = tmp_path

                while len(self._cache) > self.capacity:
                    old_key, old_path = self._cache.popitem(last=False)
                    try:
                        os.unlink(old_path)
                    except:
                        pass

            return tmp_path

        except Exception as e:
            print(f"[TTSCache] Generation error for '{text[:30]}': {e}")
            return None

    def get(self, text: str) -> Optional[str]:
        key = self._get_text_hash(text)
        with self._lock:
            if key in self._cache:
                path = self._cache.pop(key)
                self._cache[key] = path
                return path
        return None

    def put(self, text: str) -> Optional[str]:
        existing = self.get(text)
        if existing:
            return existing
        return self._generate_and_cache(text)

    def play_cached(self, text: str) -> bool:
        path = self.get(text)
        if not path:
            return False

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                import time
                time.sleep(0.02)
            pygame.mixer.music.unload()
            return True
        except Exception as e:
            print(f"[TTSCache] Playback error: {e}")
            return False

    def is_cached(self, text: str) -> bool:
        key = self._get_text_hash(text)
        with self._lock:
            return key in self._cache

    def get_stats(self) -> Dict:
        with self._lock:
            return {
                "size": len(self._cache),
                "capacity": self.capacity,
                "utilization": len(self._cache) / self.capacity,
                "cached_phrases": list(self._cache.keys())
            }

    def clear(self):
        with self._lock:
            for path in self._cache.values():
                try:
                    os.unlink(path)
                except:
                    pass
            self._cache.clear()

    def __del__(self):
        self.clear()

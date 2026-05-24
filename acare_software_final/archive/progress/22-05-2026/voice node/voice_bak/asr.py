import threading
import asyncio
import numpy as np
import time
import inspect
from typing import Any, cast
from dotenv import load_dotenv
import os
from .keyword_monitor import KeywordMonitor
from deepgram import DeepgramClient
from deepgram.clients.live.v1 import LiveTranscriptionEvents, LiveOptions

load_dotenv()

def _require_env_str(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"{key} not found in .env file")
    return value

DEEPGRAM_API_KEY: str = _require_env_str("DEEPGRAM_API_KEY")

SAMPLE_RATE = 16000

class ASRClient:
    def __init__(self, on_transcript, keyword_monitor=None):
        self.on_transcript = on_transcript
        self.keyword_monitor = keyword_monitor
        self.client = DeepgramClient(DEEPGRAM_API_KEY)
        self.connection: Any = None
        self.loop = None
        self._ready = threading.Event()
        self.keepalive_active = False
        self.keepalive_thread = None
        self._last_final_text = ""
        self._last_final_at = 0.0
        self._connection_died = False
        self._last_send_error_time = 0.0

    def connect(self):
        t = threading.Thread(target=self._run_loop, daemon=True)
        t.start()
        self._ready.wait()
        # Start keepalive after connection confirmed open
        self.start_keepalive()

    def _run_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._connect())

    async def _connect(self):
        connection = cast(Any, self.client.listen.asynclive.v("1"))
        self.connection = connection
        connection.on(LiveTranscriptionEvents.Transcript, self._on_transcript)
        connection.on(LiveTranscriptionEvents.Error, self._on_error)

        live_options_ctor = cast(Any, LiveOptions)
        options = live_options_ctor(
            model="nova-2",
            language="en-IN",
            sample_rate=SAMPLE_RATE,
            channels=1,
            encoding="linear16",
            punctuate=True,
            interim_results=True,
            endpointing=15000,  # 15s endpointing timeout (safe headroom for TTS pause/resume)
            vad_events=False,  # Disable server-side VAD (we use Silero client-side)
        )

        started = connection.start(options)
        if inspect.isawaitable(started):
            await started
        self._ready.set()
        print("[ASR] Deepgram Streaming Active. Speak now.")

        while True:
            await asyncio.sleep(0.1)

    def _send_to_deepgram_safe(self, data):
        """Send data to Deepgram and suppress SDK error output."""
        try:
            if self.connection and self.loop:
                sent = self.connection.send(data)
                if inspect.iscoroutine(sent):
                    # Wrap the future to suppress exceptions
                    future = asyncio.run_coroutine_threadsafe(sent, self.loop)
                    # Don't wait for result to avoid blocking; exceptions are silently caught by SDK
                    return True
        except Exception:
            pass
        return False

    def start_keepalive(self):
        """
        Sends silent audio to Deepgram every 1.0 seconds.
        Prevents timeout when audio streaming is paused (e.g., during TTS).
        """
        def keepalive_loop():
            # Create silent audio: 512 samples at 16kHz = 32ms of silence
            silence = np.zeros(512, dtype=np.int16).tobytes()
            while self.keepalive_active:
                if not self._send_to_deepgram_safe(silence):
                    if not self._connection_died:
                        self._connection_died = True
                        print(f"[ASR] Deepgram connection unavailable (will retry on next activity)")
                time.sleep(1.0)  # Send every 1.0 seconds (well within 15s timeout)

        self.keepalive_active = True
        self.keepalive_thread = threading.Thread(
            target=keepalive_loop, daemon=True
        )
        self.keepalive_thread.start()

    def stop_keepalive(self):
        self.keepalive_active = False

    async def _on_transcript(self, self2, result, **kwargs):
        sentence = ""
        try:
            sentence = result.channel.alternatives[0].transcript
        except Exception:
            return

        if not sentence:
            return

        is_final = bool(getattr(result, "is_final", False))
        speech_final = bool(getattr(result, "speech_final", False))

        if not is_final:
            if self.keyword_monitor:
                self.keyword_monitor.check_partial(sentence)
            return

        # Deepgram can emit valid final chunks with speech_final=False.
        # Process all finals, but suppress immediate duplicates.
        now = time.time()
        if sentence == self._last_final_text and (now - self._last_final_at) < 0.75:
            return
        self._last_final_text = sentence
        self._last_final_at = now

        if self.keyword_monitor:
            self.keyword_monitor.cancel_if_continuation(sentence)
        if self.keyword_monitor and self.keyword_monitor.estop_active:
            return
        self.on_transcript(sentence)

    async def _on_error(self, self2, error, **kwargs):
        # Log only once if connection closed; suppress flood
        if isinstance(error, dict) and "ConnectionClosed" in str(error.get("description", "")):
            if not self._connection_died:
                self._connection_died = True
                print(f"[ASR] Deepgram connection closed (timeout or network issue)")
        else:
            print(f"[ASR] Deepgram error: {error}")

    def send_chunk(self, audio_np):
        audio_int16 = (audio_np * 32767).astype(np.int16)
        raw_bytes = audio_int16.tobytes()
        if self._send_to_deepgram_safe(raw_bytes):
            self._last_send_error_time = 0
        else:
            now = time.time()
            if not self._connection_died and (now - self._last_send_error_time > 10.0):
                print(f"[ASR] Audio not reachable; connection may have timed out")
                self._last_send_error_time = now

    def send_audio(self, audio_np):
        audio_int16 = (audio_np * 32767).astype(np.int16)
        raw_bytes = audio_int16.tobytes()
        if self._send_to_deepgram_safe(raw_bytes):
            self._last_send_error_time = 0
        else:
            now = time.time()
            if not self._connection_died and (now - self._last_send_error_time > 10.0):
                print(f"[ASR] Audio not reachable; connection may have timed out")
                self._last_send_error_time = now

    def disconnect(self):
        self.stop_keepalive()
        if self.connection and self.loop:
            finished = self.connection.finish()
            if inspect.iscoroutine(finished):
                asyncio.run_coroutine_threadsafe(finished, self.loop)
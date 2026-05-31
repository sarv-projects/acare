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
    MAX_RECONNECT_ATTEMPTS = 3
    RECONNECT_BACKOFFS = [0.5, 1.0, 2.0]   # seconds — spec Section IX

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
        self._reconnect_attempts = 0
        self._reconnecting = False
        self._last_send_error_time = 0.0
        self._on_network_failure_cb = None   # injected by voice_node for TTS alert

    def set_network_failure_callback(self, cb):
        """Called after all reconnect attempts fail. cb() → triggers TTS + ESTOP."""
        self._on_network_failure_cb = cb

    def connect(self):
        t = threading.Thread(target=self._run_loop, daemon=True)
        t.start()
        self._ready.wait()
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
            # 300ms of silence → finalize. Conversational sweet spot.
            # Was 15000 (15s!) which made every command take 15s to finalize.
            endpointing=300,
            # utterance_end_ms gives a clean end-of-speech signal independent
            # of endpointing, useful for turn-taking.
            utterance_end_ms=1000,
            vad_events=False,
        )

        started = connection.start(options)
        if inspect.isawaitable(started):
            await started

        self._connection_died = False
        self._reconnect_attempts = 0
        self._reconnecting = False
        self._ready.set()
        print("[ASR] Deepgram Streaming Active. Speak now.")

        while True:
            await asyncio.sleep(0.1)

    def _reconnect_in_background(self):
        """
        Spec Section IX: 3 retries with exponential backoff (500ms, 1s, 2s).
        Runs in a daemon thread so it doesn't block the ASR loop.
        Calls _on_network_failure_cb if all retries exhausted.
        """
        if self._reconnecting:
            return
        self._reconnecting = True

        def _do_reconnect():
            for attempt_idx, delay in enumerate(self.RECONNECT_BACKOFFS):
                attempt_num = attempt_idx + 1
                print(f"[ASR] Reconnect attempt {attempt_num}/{self.MAX_RECONNECT_ATTEMPTS} "
                      f"in {delay}s...")
                time.sleep(delay)
                try:
                    # Stop old keepalive
                    self.keepalive_active = False

                    # Create fresh connection
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
                        endpointing=300,
                        utterance_end_ms=1000,
                        vad_events=False,
                    )
                    if self.loop and self.loop.is_running():
                        future = asyncio.run_coroutine_threadsafe(
                            self._start_connection(connection, options), self.loop
                        )
                        future.result(timeout=10.0)
                    self._connection_died = False
                    self._reconnecting = False
                    self._reconnect_attempts = 0
                    print(f"[ASR] Reconnected successfully on attempt {attempt_num}.")
                    self.start_keepalive()
                    return
                except Exception as e:
                    print(f"[ASR] Reconnect attempt {attempt_num} failed: {e}")

            # All retries exhausted
            self._reconnecting = False
            print("[ASR] All reconnect attempts failed — voice service unavailable.")
            if self._on_network_failure_cb:
                try:
                    self._on_network_failure_cb()
                except Exception:
                    pass

        threading.Thread(target=_do_reconnect, daemon=True).start()

    async def _start_connection(self, connection, options):
        started = connection.start(options)
        if inspect.isawaitable(started):
            await started

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
        On consecutive send failures, triggers reconnect logic.
        """
        def keepalive_loop():
            silence = np.zeros(512, dtype=np.int16).tobytes()
            consecutive_failures = 0
            while self.keepalive_active:
                if not self._send_to_deepgram_safe(silence):
                    consecutive_failures += 1
                    if consecutive_failures >= 3 and not self._connection_died and not self._reconnecting:
                        self._connection_died = True
                        print("[ASR] Deepgram keepalive failed — triggering reconnect.")
                        self._reconnect_in_background()
                else:
                    consecutive_failures = 0
                time.sleep(1.0)

        self.keepalive_active = True
        self.keepalive_thread = threading.Thread(target=keepalive_loop, daemon=True)
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
        if isinstance(error, dict) and "ConnectionClosed" in str(error.get("description", "")):
            if not self._connection_died:
                self._connection_died = True
                print("[ASR] Deepgram connection closed — attempting reconnect...")
                self._reconnect_in_background()
        else:
            print(f"[ASR] Deepgram error: {error}")
            if not self._connection_died:
                self._connection_died = True
                self._reconnect_in_background()

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
from __future__ import annotations

from collections import deque
import threading
import time
from typing import Deque

import numpy as np

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from acare_msgs.msg import EmergencySignal, SafetyAlert, Transcript


class VoiceNodeROS(Node):
    AUDIO_PAIRING_WINDOW_MS = 8000
    TRANSCRIPT_GRACE_MS = 1500
    SAMPLE_RATE_HZ = 16000

    def __init__(self):
        super().__init__("voice_node")
        self.raw_pub = self.create_publisher(Transcript, "/raw_transcript", 10)
        self.tts_sub = self.create_subscription(String, "/tts_request", self._on_tts, 10)
        self.estop_pub = self.create_publisher(EmergencySignal, "/emergency_stop", 10)
        self.alert_pub = self.create_publisher(SafetyAlert, "/safety_alert", 10)

        self._audio_stack_ready = False
        self._startup_error = ""
        self._vad = None
        self._asr = None
        self._tts = None
        self._running = True
        self._pair_lock = threading.Lock()
        self._pending_audio: Deque[tuple[int, np.ndarray]] = deque()
        self._pending_transcripts: Deque[tuple[int, str]] = deque()
        self.create_timer(0.25, self._flush_stale_pairs)
        self._start_audio_stack()

    def _start_audio_stack(self):
        try:
            from .keyword_monitor import KeywordMonitor
            from .asr import ASRClient
            from .vad import VADListener
            from .tts_queue import TTSQueue, Priority

            self._priority_cls = Priority
            self._keyword_monitor = KeywordMonitor(
                on_estop=self._on_estop_keyword,
                on_resume=self._on_resume_keyword,
            )
            self._asr = ASRClient(self._on_transcript, keyword_monitor=self._keyword_monitor)
            self._asr.connect()
            self._vad = VADListener(asr_client=self._asr)
            self._tts = TTSQueue(vad_listener=self._vad)
            threading.Thread(
                target=self._vad.start,
                args=(self._on_audio_flush,),
                daemon=True,
            ).start()
            self._audio_stack_ready = True
            self.get_logger().info("Voice audio stack ready")
        except Exception as exc:
            self._startup_error = str(exc)
            self.get_logger().warn(
                f"Voice audio stack unavailable; TTS/transcript live I/O disabled: {exc}"
            )

    def _on_audio_flush(self, _audio_np):
        try:
            audio_np = np.asarray(_audio_np, dtype=np.float32)
        except Exception:
            return
        if audio_np.size == 0 or not np.isfinite(audio_np).all():
            return
        ts_ms = int(time.time() * 1000)
        with self._pair_lock:
            self._pending_audio.append((ts_ms, audio_np.copy()))
            self._drain_pairs_locked()

    def _on_transcript(self, text: str):
        text = (text or "").strip()
        if not text:
            return
        ts_ms = int(time.time() * 1000)
        with self._pair_lock:
            self._pending_transcripts.append((ts_ms, text))
            self._drain_pairs_locked()

    def _drain_pairs_locked(self):
        while self._pending_transcripts and self._pending_audio:
            transcript_ts, text = self._pending_transcripts[0]
            audio_ts, audio_np = self._pending_audio[0]
            if abs(transcript_ts - audio_ts) > self.AUDIO_PAIRING_WINDOW_MS:
                if audio_ts < transcript_ts:
                    self._pending_audio.popleft()
                    continue
                break
            self._pending_transcripts.popleft()
            self._pending_audio.popleft()
            self._publish_turn(text, transcript_ts, audio_np)

    def _flush_stale_pairs(self):
        now_ms = int(time.time() * 1000)
        with self._pair_lock:
            self._drain_pairs_locked()
            while self._pending_transcripts and (now_ms - self._pending_transcripts[0][0]) >= self.TRANSCRIPT_GRACE_MS:
                transcript_ts, text = self._pending_transcripts.popleft()
                self._publish_turn(text, transcript_ts, None)
            while self._pending_audio and (now_ms - self._pending_audio[0][0]) >= self.AUDIO_PAIRING_WINDOW_MS:
                self._pending_audio.popleft()

    def _publish_turn(self, text: str, ts_ms: int, audio_np: np.ndarray | None):
        msg = Transcript()
        msg.text = text
        msg.is_final = True
        msg.timestamp = ts_ms
        if audio_np is not None:
            pcm16 = np.clip(audio_np, -1.0, 1.0)
            pcm16 = (pcm16 * 32767.0).astype(np.int16)
            msg.sample_rate_hz = self.SAMPLE_RATE_HZ
            msg.pcm16 = pcm16.tolist()
        else:
            msg.sample_rate_hz = 0
            msg.pcm16 = []
        self.raw_pub.publish(msg)
        self.get_logger().info(f"Transcript: {text} | audio={'yes' if audio_np is not None else 'no'}")

    def _on_tts(self, msg: String):
        if self._tts is not None:
            self._tts.speak(msg.data, priority=self._priority_cls.NORMAL)
        else:
            self.get_logger().info(f"TTS request: {msg.data}")

    def _on_estop_keyword(self, keyword: str):
        estop = EmergencySignal()
        estop.reason = f"voice_keyword_{keyword}"
        estop.source = "voice"
        self.estop_pub.publish(estop)

        alert = SafetyAlert()
        alert.severity = "ESTOP"
        alert.reason = estop.reason
        alert.source = estop.source
        self.alert_pub.publish(alert)

    def _on_resume_keyword(self, _keyword: str):
        self.get_logger().info("Resume keyword detected")

    def destroy_node(self):
        self._running = False
        if self._vad is not None:
            self._vad.stop()
        if self._asr is not None:
            self._asr.disconnect()
        if self._tts is not None:
            self._tts.stop()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = VoiceNodeROS()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

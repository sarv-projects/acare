"""
acare_voice/voice_ros_node.py

ROS2 wrapper around the streaming voice stack (VAD + ASR + TTS).

This module is the canonical voice node for the deployed ROS graph. The
older ``voice_node.py`` is the standalone (non-ROS) variant kept for unit
testing and live mic tooling.

Responsibilities
----------------
* Subscribe to ``/tts_request`` and play TTS audio.
* Publish raw transcripts on ``/raw_transcript`` paired with their PCM16
  audio so the auth node can perform voice biometric matching.
* Publish ``/emergency_stop`` and ``/safety_alert`` when an ESTOP keyword
  is detected; publish a CLEAR-severity ``SafetyAlert`` when the operator
  speaks a recovery keyword (resume / continue / proceed / clear / reset).
* Track the global robot state via ``/robot_state`` and run a small audio
  state machine (IDLE / LISTENING / TRANSCRIBING / SPEAKING / ESTOP_LISTEN)
  that mutes the streaming pipeline whenever the arm is in motion or in a
  HOLDING/HANDOVER substate where stray transcripts could re-trigger
  intents.

Audio FSM (spec design.md §VIII / voice.md §AudioStateMachine)
--------------------------------------------------------------
::

    IDLE  --(robot LOGGED_OUT|STANDBY)--> LISTENING
    LISTENING --(VAD speech)--> TRANSCRIBING
    TRANSCRIBING --(final)--> LISTENING
    LISTENING --(robot EXECUTING|HOLDING|HANDOVER)--> IDLE
    *  --(estop keyword)--> ESTOP_LISTEN
    ESTOP_LISTEN --(resume keyword)--> LISTENING
    LISTENING --(TTS playing)--> SPEAKING --(TTS done)--> LISTENING
"""

from __future__ import annotations

from collections import deque
from enum import Enum
import threading
import time
from typing import Deque, Optional, Tuple

import numpy as np

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from acare_msgs.msg import EmergencySignal, RobotState, SafetyAlert, Transcript


# ---------------------------------------------------------------------------
# Audio state machine
# ---------------------------------------------------------------------------

class AudioState(Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    TRANSCRIBING = "TRANSCRIBING"
    SPEAKING = "SPEAKING"
    ESTOP_LISTEN = "ESTOP_LISTEN"


# Robot states that mean "do not accept new voice intents". The mic is
# still hot under ESTOP_LISTEN, but normal transcripts are dropped.
ROBOT_STATES_REQUIRING_MUTE = {"EXECUTING", "HOLDING", "HANDOVER"}
# Robot states where the mic should be live and ready for normal speech.
ROBOT_STATES_LISTENING_OK = {"LOGGED_OUT", "STANDBY", "LISTENING", "PROCESSING"}


class AudioStateMachine:
    """Tiny finite-state machine for the voice node's audio plane.

    This is intentionally a plain-Python class — not a ROS node — so the
    lifecycle is easy to test offline and the main node owns the lock.
    """

    def __init__(self, on_change=None):
        self._state = AudioState.IDLE
        self._lock = threading.Lock()
        self._on_change = on_change

    @property
    def state(self) -> AudioState:
        with self._lock:
            return self._state

    def _set(self, new: AudioState, reason: str) -> bool:
        with self._lock:
            if new is self._state:
                return False
            old = self._state
            self._state = new
        if self._on_change is not None:
            try:
                self._on_change(old, new, reason)
            except Exception:
                pass
        return True

    # Public transition triggers ----------------------------------------- #

    def on_robot_state(self, robot_state: str) -> AudioState:
        rs = (robot_state or "").upper()
        # ESTOP override stays in ESTOP_LISTEN until the operator clears it.
        if self.state is AudioState.ESTOP_LISTEN and rs != "ESTOP":
            # Robot has left ESTOP — drop back to LISTENING.
            self._set(AudioState.LISTENING, f"robot_state:{rs}")
        elif rs == "ESTOP":
            self._set(AudioState.ESTOP_LISTEN, f"robot_state:{rs}")
        elif rs in ROBOT_STATES_REQUIRING_MUTE:
            self._set(AudioState.IDLE, f"robot_state:{rs}")
        elif rs in ROBOT_STATES_LISTENING_OK and self.state is AudioState.IDLE:
            self._set(AudioState.LISTENING, f"robot_state:{rs}")
        return self.state

    def on_estop_keyword(self):
        self._set(AudioState.ESTOP_LISTEN, "estop_keyword")

    def on_resume_keyword(self):
        if self.state is AudioState.ESTOP_LISTEN:
            self._set(AudioState.LISTENING, "resume_keyword")

    def on_speech_start(self):
        if self.state is AudioState.LISTENING:
            self._set(AudioState.TRANSCRIBING, "speech_start")

    def on_speech_final(self):
        if self.state is AudioState.TRANSCRIBING:
            self._set(AudioState.LISTENING, "speech_final")

    def on_tts_start(self):
        if self.state in (AudioState.LISTENING, AudioState.TRANSCRIBING):
            self._set(AudioState.SPEAKING, "tts_start")

    def on_tts_end(self):
        if self.state is AudioState.SPEAKING:
            self._set(AudioState.LISTENING, "tts_end")

    def accepts_normal_transcript(self) -> bool:
        return self.state in (AudioState.LISTENING, AudioState.TRANSCRIBING)


# ---------------------------------------------------------------------------
# ROS node
# ---------------------------------------------------------------------------

class VoiceNodeROS(Node):
    AUDIO_PAIRING_WINDOW_MS = 8000
    # If a transcript has been waiting longer than this, give up on the audio
    # buffer match and publish what we have. Voice biometric verification
    # will degrade gracefully (the auth node already handles pcm16=[]).
    TRANSCRIPT_GRACE_MS = 1500
    SAMPLE_RATE_HZ = 16000

    def __init__(self):
        super().__init__("voice_node")
        self.raw_pub = self.create_publisher(Transcript, "/raw_transcript", 10)
        self.tts_sub = self.create_subscription(String, "/tts_request", self._on_tts, 10)
        self.estop_pub = self.create_publisher(EmergencySignal, "/emergency_stop", 10)
        self.alert_pub = self.create_publisher(SafetyAlert, "/safety_alert", 10)
        # C1: track global robot state to mute mic during motion phases.
        self.create_subscription(RobotState, "/robot_state", self._on_robot_state, 10)

        self._audio_stack_ready = False
        self._startup_error = ""
        self._vad = None
        self._asr = None
        self._tts = None
        self._priority_cls = None
        self._keyword_monitor = None
        self._running = True
        self._pair_lock = threading.Lock()
        self._pending_audio: Deque[Tuple[int, np.ndarray]] = deque()
        self._pending_transcripts: Deque[Tuple[int, str]] = deque()

        # Optional helpers — wired up if the modules import cleanly.
        self._earcons = self._try_import_earcons()
        self._turn_detector = self._try_import_turn_detector()

        # Audio state machine — drives mic mute / earcon playback.
        self._fsm = AudioStateMachine(on_change=self._on_audio_state_change)
        self._robot_state = "OFFLINE"

        self.create_timer(0.25, self._flush_stale_pairs)
        self._start_audio_stack()

    # ------------------------------------------------------------------ #
    # Lazy module wiring                                                 #
    # ------------------------------------------------------------------ #

    def _try_import_earcons(self):
        try:
            from . import earcons  # type: ignore
            return earcons
        except Exception as exc:
            self.get_logger().info(f"Earcons unavailable ({exc}); continuing without")
            return None

    def _try_import_turn_detector(self):
        try:
            from .semantic_turn_detector import get_turn_detector
            return get_turn_detector()
        except Exception as exc:
            self.get_logger().info(f"SemanticTurnDetector unavailable ({exc})")
            return None

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

    # ------------------------------------------------------------------ #
    # Audio state callbacks                                              #
    # ------------------------------------------------------------------ #

    def _on_audio_state_change(self, old: AudioState, new: AudioState, reason: str):
        self.get_logger().info(f"AudioFSM {old.value} -> {new.value} ({reason})")
        # Mute / unmute the streaming pipeline so we don't waste tokens
        # on Deepgram while the mic shouldn't be transcribing.
        if new is AudioState.IDLE:
            self._pause_streaming()
        elif old is AudioState.IDLE:
            self._resume_streaming()

        if self._earcons is None:
            return
        # Earcons (G): give the operator audible feedback for state moves.
        try:
            if new is AudioState.LISTENING and old in (AudioState.IDLE, AudioState.SPEAKING):
                self._earcons.play_listen_start()
            elif new is AudioState.ESTOP_LISTEN:
                self._earcons.play_estop()
            elif new is AudioState.SPEAKING:
                # No earcon — TTSQueue is about to play synthesized voice.
                pass
        except Exception:
            pass

    def _pause_streaming(self):
        try:
            if self._vad is not None:
                self._vad.pause_streaming()
        except Exception:
            pass

    def _resume_streaming(self):
        try:
            if self._vad is not None:
                self._vad.resume_streaming()
        except Exception:
            pass

    # ------------------------------------------------------------------ #
    # Subscriptions                                                      #
    # ------------------------------------------------------------------ #

    def _on_robot_state(self, msg: RobotState):
        self._robot_state = (msg.state or "").upper()
        self._fsm.on_robot_state(self._robot_state)

        # Reset ESTOP keyword latch when the global FSM has left ESTOP.
        if self._robot_state != "ESTOP" and self._keyword_monitor is not None:
            try:
                if getattr(self._keyword_monitor, "estop_active", False):
                    self._keyword_monitor.reset_estop()
            except Exception:
                pass

    # ------------------------------------------------------------------ #
    # Audio pipeline callbacks                                           #
    # ------------------------------------------------------------------ #

    def _on_audio_flush(self, _audio_np):
        try:
            audio_np = np.asarray(_audio_np, dtype=np.float32)
        except Exception:
            return
        if audio_np.size == 0 or not np.isfinite(audio_np).all():
            return
        ts_ms = int(time.time() * 1000)
        self._fsm.on_speech_start()
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
        """C5: pair audio with transcripts; never lose a transcript silently.

        The previous implementation hit ``break`` whenever a transcript
        arrived before its audio (very short utterances), holding the
        transcript in the queue until the 1.5 s grace flush ran with
        ``pcm16=[]``. That broke voice biometric verification for the turn
        because :meth:`auth_node._transcript_to_audio_tensor` returned
        None.

        New behaviour:

        * If transcript and audio are within the pairing window, publish
          paired.
        * If audio is older than the transcript by more than the window,
          drop the audio (it belonged to a turn we never transcribed).
        * If the transcript is old enough that we are inside the grace
          period and there is no matching audio yet, publish the
          transcript without audio rather than block forever.
        """
        now_ms = int(time.time() * 1000)
        while self._pending_transcripts and self._pending_audio:
            transcript_ts, text = self._pending_transcripts[0]
            audio_ts, audio_np = self._pending_audio[0]
            delta = transcript_ts - audio_ts

            if abs(delta) <= self.AUDIO_PAIRING_WINDOW_MS:
                self._pending_transcripts.popleft()
                self._pending_audio.popleft()
                self._publish_turn(text, transcript_ts, audio_np)
                continue

            if delta > 0:
                # transcript is much newer — older audio is orphaned.
                self._pending_audio.popleft()
                continue

            # transcript is much older than the head-of-queue audio. If we
            # are inside the grace window, publish without audio so we
            # don't drop the transcript on the floor.
            if (now_ms - transcript_ts) >= self.TRANSCRIPT_GRACE_MS:
                self._pending_transcripts.popleft()
                self._publish_turn(text, transcript_ts, None)
                continue

            # Wait — the matching audio may still arrive before the
            # grace period elapses. The flush timer will handle it.
            break

    def _flush_stale_pairs(self):
        now_ms = int(time.time() * 1000)
        with self._pair_lock:
            self._drain_pairs_locked()
            while self._pending_transcripts and (now_ms - self._pending_transcripts[0][0]) >= self.TRANSCRIPT_GRACE_MS:
                transcript_ts, text = self._pending_transcripts.popleft()
                self._publish_turn(text, transcript_ts, None)
            while self._pending_audio and (now_ms - self._pending_audio[0][0]) >= self.AUDIO_PAIRING_WINDOW_MS:
                self._pending_audio.popleft()

    def _publish_turn(self, text: str, ts_ms: int, audio_np: Optional[np.ndarray]):
        # Drop normal transcripts while the FSM says the mic should be muted
        # (during EXECUTING / HOLDING / HANDOVER). ESTOP keywords are still
        # routed through the keyword monitor and will fire a separate path.
        if not self._fsm.accepts_normal_transcript():
            self.get_logger().info(
                f"Dropping transcript while audio_state={self._fsm.state.value}: {text!r}"
            )
            self._fsm.on_speech_final()
            return

        # Optional: only publish transcripts that look like complete turns
        # so half-formed mid-utterance segments don't trigger downstream
        # LLM calls. The SemanticTurnDetector returns a (complete, conf)
        # tuple; we err on the side of publishing if it isn't sure.
        if self._turn_detector is not None and audio_np is not None:
            try:
                duration = float(audio_np.shape[-1]) / float(self.SAMPLE_RATE_HZ)
                complete, conf = self._turn_detector.predict(text, duration)
            except Exception:
                complete, conf = (True, 1.0)
            if not complete and conf >= 0.7:
                self.get_logger().info(
                    f"Held back partial transcript (conf={conf:.2f}): {text!r}"
                )
                # Re-queue at front so a later, more-complete transcript
                # supersedes it via duplicate suppression in ASR.
                self._fsm.on_speech_final()
                return

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
        self._fsm.on_speech_final()
        self.get_logger().info(
            f"Transcript: {text} | audio={'yes' if audio_np is not None else 'no'}"
        )

    # ------------------------------------------------------------------ #
    # TTS                                                                #
    # ------------------------------------------------------------------ #

    def _on_tts(self, msg: String):
        if self._tts is None or self._priority_cls is None:
            self.get_logger().info(f"TTS request: {msg.data}")
            return
        self._fsm.on_tts_start()
        try:
            self._tts.speak(msg.data, priority=self._priority_cls.NORMAL)
        finally:
            # TTSQueue plays asynchronously; mark TTS end after a short
            # delay so the FSM doesn't block the mic forever if the audio
            # backend is silently failing. The TTSQueue's own pause/resume
            # of the VAD streamer handles the real audio gating.
            threading.Timer(0.5, self._fsm.on_tts_end).start()

    # ------------------------------------------------------------------ #
    # Keyword callbacks                                                  #
    # ------------------------------------------------------------------ #

    def _on_estop_keyword(self, keyword: str):
        self._fsm.on_estop_keyword()
        estop = EmergencySignal()
        estop.reason = f"voice_keyword_{keyword}"
        estop.source = "voice"
        self.estop_pub.publish(estop)

        alert = SafetyAlert()
        alert.severity = "ESTOP"
        alert.reason = estop.reason
        alert.source = estop.source
        self.alert_pub.publish(alert)

    def _on_resume_keyword(self, keyword: str):
        """C2: voice-side ESTOP clear.

        Publish a CLEAR-severity SafetyAlert that the global state_manager
        listens for. state_manager will flip ESTOP -> STANDBY (or
        LOGGED_OUT if no user was active) and the rest of the graph
        resumes normally.
        """
        self.get_logger().info(f"Resume keyword detected: {keyword}")
        self._fsm.on_resume_keyword()
        if self._keyword_monitor is not None:
            try:
                self._keyword_monitor.reset_estop()
            except Exception:
                pass
        alert = SafetyAlert()
        alert.severity = "CLEAR"
        alert.reason = f"voice_resume_{keyword}"
        alert.source = "voice"
        self.alert_pub.publish(alert)

    # ------------------------------------------------------------------ #
    # Lifecycle                                                          #
    # ------------------------------------------------------------------ #

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

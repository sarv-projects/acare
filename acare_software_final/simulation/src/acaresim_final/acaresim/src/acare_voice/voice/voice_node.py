"""
ACARE Voice Node
Spec Reference: Section V, VIII, IX, XIII

This is the voice_node — the top-level audio orchestration module that owns:
  - Audio state machine (IDLE / LISTENING / TRANSCRIBING / SPEAKING / ESTOP_LISTEN)
  - VAD (Silero, 32ms chunks)
  - Deepgram Nova-2 streaming STT WebSocket
  - Emergency keyword thread (always-on, never muted)
  - Text normaliser + alias expansion
  - Groq intent parser
  - Assistant agent (LOGGED_OUT conversational mode)
  - TTS (dual: Google Cloud / pyttsx3 / Kokoro)

In standalone mode (run as __main__), this wires everything together and runs.
When ROS2-wrapped, this module's on_intent_resolved() callback will publish to
/validated_intent instead of printing.

Deployment note:
  - vision_node integration points are clearly marked as stubs.
  - Session/auth integration stubs are also marked for auth_node.
"""

import sys
import os
import threading
import time
from enum import Enum
from typing import Callable, Optional

if __package__ is None:
    _voice_dir = os.path.dirname(os.path.abspath(__file__))
    _parent = os.path.dirname(_voice_dir)
    if _parent not in sys.path:
        sys.path.insert(0, _parent)
    from voice.vad import VADListener
    from voice.asr import ASRClient
    from voice.keyword_monitor import KeywordMonitor
    from voice.normaliser import normalise, get_multi_tool_prompt
    from voice.alias_expansion import expand_aliases
    from voice.intent_parser import parse_intent
    from voice.assistant_agent import AssistantAgent
    from voice.tts import speak, speak_urgent, Priority
else:
    from .vad import VADListener
    from .asr import ASRClient
    from .keyword_monitor import KeywordMonitor
    from .normaliser import normalise, get_multi_tool_prompt
    from .alias_expansion import expand_aliases
    from .intent_parser import parse_intent
    from .assistant_agent import AssistantAgent
    from .tts import speak, speak_urgent, Priority


# ---------------------------------------------------------------------------
# Audio state machine
# ---------------------------------------------------------------------------
class AudioState(Enum):
    IDLE         = "IDLE"          # Mic off, TTS off
    LISTENING    = "LISTENING"     # VAD active, mic open, Deepgram WebSocket open
    TRANSCRIBING = "TRANSCRIBING"  # Deepgram processing, mic still open
    SPEAKING     = "SPEAKING"      # TTS playing, mic hard-muted
    ESTOP_LISTEN = "ESTOP_LISTEN"  # Emergency keyword thread only — always active


# ---------------------------------------------------------------------------
# Robot state (simplified — full state_manager is a separate node in ROS2)
# ---------------------------------------------------------------------------
class RobotState(Enum):
    LOGGED_OUT  = "LOGGED_OUT"   # No active session — assistant agent active
    STANDBY     = "STANDBY"      # Session active, awaiting command
    LISTENING   = "LISTENING"    # Voice command in flight
    PROCESSING  = "PROCESSING"   # Intent parsed, vision searching (stub)
    EXECUTING   = "EXECUTING"    # Arm in motion (stub)
    HOLDING     = "HOLDING"      # Object grasped (stub)
    HANDOVER    = "HANDOVER"     # At handover zone (stub)
    ESTOP       = "ESTOP"        # All motion halted


# ---------------------------------------------------------------------------
# Voice Node
# ---------------------------------------------------------------------------
class VoiceNode:
    """
    Voice Node — full audio pipeline orchestration.

    Callbacks (register to receive events):
      on_intent_resolved(intent: dict)  — clear intent ready for planner
      on_estop_triggered(keyword: str)  — ESTOP keyword detected
      on_transcript(text: str)          — raw final transcript (for logging)

    Stubs (to be implemented when auth_node / planner_node exist):
      on_logged_in(user_id, name)       — call to start a session
      on_logged_out()                   — call to end a session
      on_resume()                       — call to clear ESTOP and resume
    """

    def __init__(
        self,
        on_intent_resolved: Optional[Callable] = None,
        on_estop_triggered: Optional[Callable] = None,
        on_transcript: Optional[Callable] = None,
    ):
        self.on_intent_resolved_cb = on_intent_resolved
        self.on_estop_triggered_cb = on_estop_triggered
        self.on_transcript_cb = on_transcript

        self.robot_state = RobotState.LOGGED_OUT
        self.audio_state = AudioState.IDLE
        self.session_user_id: Optional[str] = None
        self.session_name: Optional[str] = None

        # Components
        self.assistant = AssistantAgent()
        self.km = KeywordMonitor(on_estop=self._on_estop)
        self.asr = ASRClient(on_transcript=self._on_transcript, keyword_monitor=self.km)
        self.vad: Optional[VADListener] = None

        # VAD runs in its own thread
        self._vad_thread: Optional[threading.Thread] = None
        self._running = False

    # ------------------------------------------------------------------
    # Public lifecycle API
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Start the full voice pipeline."""
        self._running = True
        self.asr.connect()
        self.vad = VADListener(asr_client=self.asr)

        self.robot_state = RobotState.LOGGED_OUT
        self.audio_state = AudioState.LISTENING

        self._vad_thread = threading.Thread(
            target=self.vad.start, args=(self._on_audio_flush,), daemon=True
        )
        self._vad_thread.start()
        time.sleep(0.1)
        speak("A-Care system ready. Please authenticate to start.", self.vad)

        print(f"[VoiceNode] Running in {self.robot_state.value} mode. Listening...")

    def stop(self) -> None:
        """Graceful shutdown."""
        self._running = False
        speak("Shutting down. Goodbye.", self.vad)
        time.sleep(0.5)
        try:
            if self.vad:
                self.vad.stop()
        except Exception:
            pass
        self.asr.disconnect()
        print("[VoiceNode] Stopped.")

    # ------------------------------------------------------------------
    # Session management stubs (called by auth_node in ROS2)
    # ------------------------------------------------------------------

    def on_logged_in(self, user_id: str, name: str) -> None:
        """
        AUTH_NODE calls this when a user successfully logs in.
        Transitions robot to STANDBY, starts command-ready state.
        """
        self.session_user_id = user_id
        self.session_name = name
        self.robot_state = RobotState.STANDBY
        self.assistant.reset_conversation()
        speak(f"Logged in as {name}. How can I assist?", self.vad)
        print(f"[VoiceNode] Session started for {name} ({user_id})")

    def on_logged_out(self) -> None:
        """
        Session ended — back to LOGGED_OUT, assistant agent reactivates.
        Rejected if state is EXECUTING / HOLDING / HANDOVER (spec requirement).
        """
        if self.robot_state in (
            RobotState.EXECUTING, RobotState.HOLDING, RobotState.HANDOVER
        ):
            speak("Cannot log out during active task.", self.vad)
            return
        self.session_user_id = None
        self.session_name = None
        self.robot_state = RobotState.LOGGED_OUT
        self.assistant.reset_conversation()
        speak("Logged out. A-Care standing by.", self.vad)
        print("[VoiceNode] Session ended.")

    def on_resume(self) -> None:
        """
        Called by authenticated staff to clear ESTOP and return to STANDBY.
        In ROS2, this publishes a StateTransition event to state_manager.
        """
        if self.robot_state != RobotState.ESTOP:
            return
        self.robot_state = RobotState.STANDBY
        self.km.reset_estop()
        speak("System resumed. Ready for commands.", self.vad)
        print("[VoiceNode] ESTOP cleared. Resumed.")

    # ------------------------------------------------------------------
    # Internal callbacks
    # ------------------------------------------------------------------

    def _on_audio_flush(self, audio_np) -> None:
        pass

    def _on_estop(self, keyword: str) -> None:
        """
        Emergency keyword confirmed (after 100ms collision window).
        Spec: <200ms from keyword detection to ESTOP published.
        """
        self.robot_state = RobotState.ESTOP
        self.audio_state = AudioState.ESTOP_LISTEN

        # Hard-cut current TTS, then speak urgently — spec A4
        speak_urgent(f"Emergency stop. Keyword detected: {keyword}.", self.vad)

        print(f"[VoiceNode] *** ESTOP triggered by: '{keyword}' ***")

        if self.on_estop_triggered_cb:
            self.on_estop_triggered_cb(keyword)

    def _check_estop_in_final(self, text: str) -> bool:
        """Backstop: check ESTOP keywords on final Deepgram transcripts
        in case the keyword_monitor (partial transcript) missed them."""
        lowered = text.lower().strip()
        words = [w.strip(".,!?;:'\"") for w in lowered.split()]
        if not words:
            return False
        from acare_bringup.constants import ESTOP_KEYWORDS
        for kw in ESTOP_KEYWORDS:
            if kw in words:
                if len(words) <= 2:
                    self._on_estop(kw)
                    return True
        return False

    def _on_transcript(self, text: str) -> None:
        """
        Final, speech_final=True transcript from Deepgram.
        Full pipeline:
          normalise → alias_expand → multi-tool check → intent parse → callback
        """
        if not text or not text.strip():
            return

        # Backstop: final transcript ESTOP check before state check
        if self._check_estop_in_final(text):
            return

        # ESTOP active — drop all transcripts until resume()
        if self.robot_state == RobotState.ESTOP:
            return

        print(f"[VoiceNode] Transcript: {text}")

        if self.on_transcript_cb:
            self.on_transcript_cb(text)

        # ---- LOGGED_OUT: assistant agent handles conversation ----
        if self.robot_state == RobotState.LOGGED_OUT:
            response = self.assistant.get_response(text)
            speak(response, self.vad)
            if "confirm" in text.lower() and "logged in" in response.lower():
                self.on_logged_in(user_id="voice_user", name="User")
            return

        # ---- LOGGED_IN: full command pipeline ----
        self._process_command(text)

    def _process_command(self, text: str) -> None:
        """
        Logged-in command pipeline:
          1. Normalise (lowercase / filler strip / punctuation)
          2. Alias expand (simple unambiguous aliases)
          3. Multi-tool check
          4. Groq intent parse
          5. Confidence gate → clarification or validated intent
        """
        # Step 1: Normalise
        cleaned, multi_tool, found_tools = normalise(text)
        print(f"[VoiceNode] Normalised: {repr(cleaned)}")

        if not cleaned:
            return

        # Step 2: Multi-tool check (before alias expansion or Groq)
        if multi_tool:
            prompt = get_multi_tool_prompt(found_tools)
            speak(prompt, self.vad)
            print(f"[VoiceNode] Multi-tool detected: {found_tools}")
            return

        # Step 3: Alias expansion
        expanded, canonical, needs_clarify = expand_aliases(cleaned)
        if needs_clarify:
            # Ambiguous alias — let Groq / dialogue_node resolve
            # For now we pass through to Groq with original text
            expanded = cleaned
        print(f"[VoiceNode] Alias expanded: {repr(expanded)}")

        # Step 4: Groq intent parse
        speak("Processing.", self.vad)  # Immediate acknowledgement
        intent = parse_intent(expanded)
        print(f"[VoiceNode] Intent: {intent}")

        if intent is None:
            speak("I did not understand that command. Please try again.", self.vad)
            return

        # Step 5: Multi-tool check from Groq response (secondary guard)
        if intent.get("multi_tool"):
            speak("One at a time. Which tool would you like first?", self.vad)
            return

        # Step 6: Confidence gate
        confidence = intent.get("confidence", 0.0)
        tool = intent.get("tool", "")

        if confidence < 0.6:
            speak(f"Did you mean {tool}? Please repeat the command.", self.vad)
            return

        if confidence < 0.8:
            # Ambiguous — would route to dialogue_node in ROS2
            # In standalone: ask for confirmation
            speak(f"Did you mean fetch the {tool}? Say yes to confirm.", self.vad)
            # NOTE: In ROS2 this publishes to /intent_result for dialogue_node
            return

        # Clear intent — validated
        speak(f"Fetching {tool}. Please wait.", self.vad)
        print(f"[VoiceNode] ✓ Validated intent: fetch {tool} (confidence={confidence:.2f})")

        if self.on_intent_resolved_cb:
            self.on_intent_resolved_cb(intent)
        # NOTE: In ROS2 this publishes ValidatedIntent to /validated_intent


# ---------------------------------------------------------------------------
# Standalone entry point — runs full voice pipeline without ROS2
# ---------------------------------------------------------------------------
def main():
    import sys
    has_rclpy = False
    intent_pub = None
    try:
        import rclpy
        from acare_msgs.msg import ValidatedIntent
        rclpy.init()
        has_rclpy = True
        node = rclpy.create_node('voice_standalone')
        intent_pub = node.create_publisher(ValidatedIntent, '/validated_intent', 10)
        estop_pub = node.create_publisher(SafetyAlert, '/safety_alert', 10)
    except Exception:
        pass

    print("=" * 60)
    print("ACARE Voice Pipeline — Standalone Mode")
    print("=" * 60)
    print()
    print("State: LOGGED_OUT — Assistant agent active.")
    if has_rclpy:
        print("ROS2 integration: active (publishing /validated_intent)")
    else:
        print("Commands: type 'login' to simulate login, 'logout' to log out,")
        print("          'estop' to simulate ESTOP, 'resume' to clear, 'quit' to exit.")
    print()

    def on_intent(intent):
        print(f"\n[MAIN] *** Intent resolved → {intent['tool']} ***")
        if has_rclpy and intent_pub:
            from acare_msgs.msg import ValidatedIntent
            msg = ValidatedIntent()
            msg.tool = intent.get('tool', '')
            msg.action = intent.get('action', 'fetch')
            msg.user_id = ''
            msg.name = ''
            msg.authenticated = True
            intent_pub.publish(msg)
            print(f"         Published to /validated_intent: {msg.tool}")
        else:
            print(f"         (no ROS2 — would publish to /validated_intent)")

    def on_estop(keyword):
        print(f"\n[MAIN] *** ESTOP triggered: {keyword} ***\n")
        if has_rclpy and estop_pub:
            from acare_msgs.msg import SafetyAlert
            alert = SafetyAlert()
            alert.severity = "ESTOP"
            alert.reason = f"voice_keyword_{keyword}"
            alert.source = "voice"
            estop_pub.publish(alert)

    node = VoiceNode(
        on_intent_resolved=on_intent,
        on_estop_triggered=on_estop,
    )

    node.start()

    _rclpy_node = rclpy.create_node('voice_standalone') if has_rclpy else None

    try:
        while True:
            if has_rclpy and _rclpy_node:
                rclpy.spin_once(_rclpy_node, timeout_sec=0.0)
            try:
                cmd = input().strip().lower()
            except EOFError:
                cmd = ""
            if cmd == "quit":
                break
            elif cmd == "login":
                node.on_logged_in(user_id="staff_001", name="Dr. Sharma")
            elif cmd == "logout":
                node.on_logged_out()
            elif cmd == "estop":
                node._on_estop("stop")
            elif cmd == "resume":
                node.on_resume()
            elif cmd and cmd not in ("", "quit"):
                print("[MAIN] Unknown command. Use: login / logout / estop / resume / quit")
            if not cmd:
                time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        if has_rclpy:
            try:
                rclpy.shutdown()
            except Exception:
                pass


if __name__ == "__main__":
    main()

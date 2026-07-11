import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional, Dict

from .vad import VADListener
from .asr import ASRClient
from .keyword_monitor import KeywordMonitor
from .normaliser import normalise, get_multi_tool_prompt
from .alias_expansion import expand_aliases
from .intent_parser import parse_intent
from .assistant_agent import AssistantAgent
from .tts import speak, speak_urgent
from .state_manager import get_state_manager, SystemState
from .fast_intent import parse_fast_intent, is_simple_command
from .dialogue_manager import DialogueManager
from .tts_queue import TTSQueue, Priority
from .earcons import play_turn_ready, play_listen_start, play_estop, play_barge_in
from acare_bringup.constants import ESTOP_KEYWORDS


class VoiceNode:

    def __init__(
        self,
        on_intent_resolved: Optional[Callable] = None,
        on_estop_triggered: Optional[Callable] = None,
        on_transcript: Optional[Callable] = None,
    ):
        self.on_intent_resolved_cb = on_intent_resolved
        self.on_estop_triggered_cb = on_estop_triggered
        self.on_transcript_cb = on_transcript

        self.state_mgr = get_state_manager()
        self.dialogue = DialogueManager()

        self.assistant = AssistantAgent()
        self.km = KeywordMonitor(
            on_estop=self._on_estop,
            on_resume=self._on_resume_keyword
        )

        self.tts: Optional[TTSQueue] = None

        self.asr = ASRClient(
            on_transcript=self._on_transcript,
            keyword_monitor=self.km
        )

        self.vad: Optional[VADListener] = None

        self._barge_in_buffer = []
        self._barge_in_lock = threading.Lock()
        self._last_speech_time = 0.0
        self._backchannel_threshold = 1.5

        self._vad_thread: Optional[threading.Thread] = None
        self._return_to_listen_pool = ThreadPoolExecutor(max_workers=1)
        self._running = False

        self._register_state_callbacks()

    def _register_state_callbacks(self):
        self.state_mgr.on_state(SystemState.LISTENING, self._on_listening_state)
        self.state_mgr.on_state(SystemState.RESPONDING, self._on_responding_state)
        self.state_mgr.on_state(SystemState.ESTOP, self._on_estop_state)
        self.state_mgr.on_state(SystemState.CLARIFYING, self._on_clarifying_state)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        self._running = True

        self.asr.connect()

        self.vad = VADListener(asr_client=self.asr)

        self.tts = TTSQueue(vad_listener=self.vad)

        self._vad_thread = threading.Thread(
            target=self.vad.start,
            args=(self._on_audio_flush,),
            daemon=True
        )
        self._vad_thread.start()

        self.state_mgr.transition(SystemState.LISTENING, "System startup")

        time.sleep(0.5)
        self.tts.speak("A-Care system ready. Please authenticate to start.")

        print(f"[VoiceNode] Running. State: {self.state_mgr.state.value}")

    def stop(self) -> None:
        self._running = False
        self._return_to_listen_pool.shutdown(wait=False)
        if self.tts:
            self.tts.speak_urgent("Shutting down. Goodbye.")
        if self.vad:
            self.vad.stop()
        self.asr.disconnect()
        if self.tts:
            self.tts.stop()
        print("[VoiceNode] Stopped.")

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def on_logged_in(self, user_id: str, name: str) -> None:
        if not self.state_mgr.transition(SystemState.LISTENING, f"Login: {name}"):
            return

        self.state_mgr.set_session(user_id, name)
        self.dialogue.reset()
        self.assistant.reset_conversation()

        self.tts.speak(f"Logged in as {name}. How can I assist?")
        print(f"[VoiceNode] Session started for {name} ({user_id})")

    def _schedule_return_to_listen(self, delay: float):
        def task():
            time.sleep(delay)
            self.state_mgr.transition(SystemState.LISTENING, "Return to listen")
            play_turn_ready()
        self._return_to_listen_pool.submit(task)

    def on_logged_out(self) -> None:
        if self.state_mgr.state == SystemState.ESTOP:
            self.tts.speak("Cannot log out during emergency stop.")
            return
        if self.state_mgr.state in (SystemState.CONFIRMED, SystemState.PROCESSING):
            self.tts.speak("Cannot log out during active task.")
            return

        self.state_mgr.transition(SystemState.LISTENING, "Logout")
        self.state_mgr.reset_context()
        self.dialogue.reset()
        self.assistant.reset_conversation()

        self.tts.speak("Logged out. A-Care standing by.")
        print("[VoiceNode] Session ended.")

    def on_resume(self) -> None:
        if self.state_mgr.state != SystemState.ESTOP:
            return

        self.km.reset_estop()
        self.state_mgr.transition(SystemState.LISTENING, "Resume command")
        self.tts.speak("System resumed. Ready for commands.")
        print("[VoiceNode] ESTOP cleared. Resumed.")

    # ------------------------------------------------------------------
    # State callbacks
    # ------------------------------------------------------------------

    def _on_listening_state(self, old_state, new_state, context):
        play_listen_start()
        print(f"[VoiceNode] Now listening...")

    def _on_responding_state(self, old_state, new_state, context):
        print(f"[VoiceNode] Responding...")

    def _on_estop_state(self, old_state, new_state, context):
        play_estop()
        print(f"[VoiceNode] *** ESTOP ACTIVE ***")

    def _on_clarifying_state(self, old_state, new_state, context):
        print(f"[VoiceNode] Awaiting clarification...")

    # ------------------------------------------------------------------
    # Internal callbacks
    # ------------------------------------------------------------------

    def _on_audio_flush(self, audio_np) -> None:
        duration = len(audio_np) / 16000
        self._last_speech_time = time.time()

        if self.state_mgr.state == SystemState.LISTENING:
            self.state_mgr.transition(SystemState.PROCESSING, "VAD speech detected")
            # H5: Start processing watchdog — if no transcript arrives within
            # 10s (ASR failure / network drop), return to LISTENING.
            self._processing_timer = threading.Timer(10.0, self._processing_timeout)
            self._processing_timer.daemon = True
            self._processing_timer.start()

    def _on_estop(self, keyword: str) -> None:
        self.state_mgr.transition(SystemState.ESTOP, f"Keyword: {keyword}")
        self.tts.speak_urgent(f"Emergency stop. Keyword detected: {keyword}.")

        if self.on_estop_triggered_cb:
            self.on_estop_triggered_cb(keyword)

    def _on_resume_keyword(self, keyword: str) -> None:
        if self.state_mgr.state == SystemState.ESTOP:
            self.on_resume()

    def _processing_timeout(self):
        """Watchdog: if stuck in PROCESSING for 10s without transcript, reset."""
        if self.state_mgr.state == SystemState.PROCESSING:
            print("[VoiceNode] Processing timeout — ASR may have failed. Returning to LISTENING.")
            self.state_mgr.transition(SystemState.LISTENING, "Processing timeout")

    def _on_transcript(self, text: str) -> None:
        # Cancel processing watchdog (transcript arrived)
        if hasattr(self, '_processing_timer') and self._processing_timer:
            self._processing_timer.cancel()
            self._processing_timer = None

        if not text or not text.strip():
            return

        # SAFETY: check ESTOP keywords on the FINAL transcript too, not just
        # partials. Deepgram partials can be missed (network jitter, short
        # utterances), so a final-transcript ESTOP check is a critical
        # backstop. This runs BEFORE any state routing so "stop" always wins.
        if self._check_estop_in_final(text):
            return

        if self.state_mgr.state == SystemState.ESTOP:
            # While in ESTOP, only a resume keyword can get us out.
            return

        print(f"[VoiceNode] Transcript: {text}")

        if self.on_transcript_cb:
            self.on_transcript_cb(text)

        if not self.state_mgr.is_logged_in():
            self._handle_assistant_mode(text)
            return

        self._handle_command_mode(text)

    def _check_estop_in_final(self, text: str) -> bool:
        """
        Backstop ESTOP detection on final transcripts.
        Returns True if an ESTOP keyword was found and handled.

        Only triggers on SHORT utterances dominated by the keyword — so
        "stop" or "stop now" fire, but "stop asking me that" does not
        (that's conversation, handled by the continuation-word logic in
        KeywordMonitor for partials; here we keep it strict on finals).
        """
        if self.km.estop_active:
            return False
        lowered = text.lower().strip()
        words = [w.strip(".,!?;:'\"") for w in lowered.split()]
        if not words:
            return False
        for kw in ESTOP_KEYWORDS:
            if kw in words:
                # Strict: the utterance must be short (<=2 words) so we don't
                # fire on conversational uses like "stop asking me questions".
                if len(words) <= 2:
                    self.km.force_estop(kw)
                    return True
        return False

    def _handle_assistant_mode(self, text: str) -> None:
        self.state_mgr.transition(SystemState.ASSISTING, "Assistant mode")

        response = self.assistant.get_response(text)
        self.tts.speak(response)

        self._schedule_return_to_listen(0.5)

    def _handle_command_mode(self, text: str) -> None:
        fast_intent = parse_fast_intent(text, self.dialogue.get_last_tool())

        if fast_intent:
            print(f"[VoiceNode] Fast intent: {fast_intent}")
            self._process_fast_intent(fast_intent, text)
            return

        cleaned, multi_tool, found_tools = normalise(text)
        print(f"[VoiceNode] Normalised: {repr(cleaned)}")

        if not cleaned:
            self.state_mgr.transition(SystemState.LISTENING, "Empty transcript")
            return

        if multi_tool:
            self._handle_multi_tool(found_tools)
            return

        expanded, canonical, needs_clarify = expand_aliases(cleaned)
        if needs_clarify:
            expanded = cleaned
        print(f"[VoiceNode] Alias expanded: {repr(expanded)}")

        intent = parse_intent(expanded)
        print(f"[VoiceNode] Groq intent: {intent}")

        if intent is None:
            self.tts.speak("I didn't catch that. Could you say it again?")
            self.state_mgr.transition(SystemState.LISTENING, "Intent parse failed")
            return

        processed = self.dialogue.process_intent(intent, text)
        self._execute_intent(processed)

    def _process_fast_intent(self, intent: Dict, text: str) -> None:
        intent_type = intent.get("type")

        if intent_type == "estop":
            self._on_estop(intent.get("action", "stop"))
            return

        if intent_type == "resume":
            self.on_resume()
            return

        if intent_type == "cancel":
            self.dialogue.context.clear_pending()
            self.tts.speak("Cancelled.")
            self.state_mgr.transition(SystemState.LISTENING, "User cancelled")
            return

        if intent_type == "confirm":
            if self.dialogue.is_awaiting_confirmation():
                processed = self.dialogue.process_intent(intent, text)
                self._execute_intent(processed)
            else:
                self.tts.speak("Nothing to confirm right now.")
                self.state_mgr.transition(SystemState.LISTENING, "No pending confirmation")
            return

        if intent_type == "reject":
            if self.dialogue.is_awaiting_confirmation():
                processed = self.dialogue.process_intent(intent, text)
                self._execute_intent(processed)
            else:
                self.tts.speak("Alright, what would you like instead?")
                self.state_mgr.transition(SystemState.LISTENING, "Rejection without pending")
            return

        if intent_type == "multi_tool":
            tools = intent.get("detected_tools", [])
            self._handle_multi_tool(tools)
            return

        if intent_type in ("command", "follow_up"):
            processed = self.dialogue.process_intent(intent, text)
            self._execute_intent(processed)
            return

        self.tts.speak("I didn't understand. Could you repeat that?")
        self.state_mgr.transition(SystemState.LISTENING, "Fast intent unhandled")

    def _execute_intent(self, intent: Dict) -> None:
        intent_type = intent.get("type", "command")

        if intent_type == "multi_tool_clarify":
            self.state_mgr.transition(SystemState.CLARIFYING, "Multi-tool detected")
            self.tts.speak(intent["message"])
            return

        if intent_type == "clarification_rejected":
            self.tts.speak(intent.get("message", "What would you like instead?"))
            self.state_mgr.transition(SystemState.LISTENING, "Clarification rejected")
            return

        if intent_type == "error":
            self.tts.speak(intent.get("message", "I didn't understand that."))
            self.state_mgr.transition(SystemState.LISTENING, "Error state")
            return

        confidence = intent.get("confidence", 0.0)
        tool = intent.get("tool", "")

        if not tool:
            self.tts.speak("I didn't catch which tool you need. Could you repeat?")
            self.state_mgr.transition(SystemState.LISTENING, "No tool identified")
            return

        if confidence < 0.6:
            prompt = self.dialogue.get_clarification_prompt(tool, confidence)
            self.dialogue.set_pending_confirmation(intent)
            self.state_mgr.transition(SystemState.CLARIFYING, "Low confidence")
            self.tts.speak(prompt)
            return

        if confidence < 0.8 and not intent.get("confirmed"):
            self.dialogue.set_pending_confirmation(intent)
            self.state_mgr.transition(SystemState.CLARIFYING, "Medium confidence")
            self.tts.speak(f"Fetching {tool}. Is that correct?")
            return

        self.state_mgr.transition(SystemState.CONFIRMED, f"Execute: {tool}")
        self.tts.speak(f"Fetching {tool}. Please wait.")

        print(f"[VoiceNode] Validated intent: fetch {tool} (confidence={confidence:.2f})")

        if self.on_intent_resolved_cb:
            self.on_intent_resolved_cb(intent)

        self._schedule_return_to_listen(1.0)

    def _handle_multi_tool(self, tools: list) -> None:
        if len(tools) == 2:
            msg = f"One at a time. Which first \u2014 {tools[0]} or {tools[1]}?"
        else:
            listed = ", ".join(tools[:-1]) + f" or {tools[-1]}"
            msg = f"One at a time. Which first \u2014 {listed}?"

        self.state_mgr.transition(SystemState.CLARIFYING, "Multi-tool clarification")
        self.tts.speak(msg)

    def trigger_barge_in(self):
        if self.tts and self.tts.is_speaking:
            print("[VoiceNode] Barge-in triggered")
            self.tts.trigger_barge_in()
            play_barge_in()
            self.state_mgr.transition(SystemState.LISTENING, "Barge-in detected")


def main():
    print("=" * 60)
    print("ACARE Voice Pipeline v2 \u2014 Conversational Flow")
    print("=" * 60)
    print()
    print("State: LOGGED_OUT \u2014 Assistant agent active.")
    print("Commands: 'login' / 'logout' / 'estop' / 'resume' / 'quit'")
    print("           'barge' \u2014 simulate barge-in during TTS")
    print()

    def on_intent(intent):
        print(f"\n[MAIN] Intent resolved:")
        print(f"         Tool: {intent.get('tool')}")
        print(f"         Action: {intent.get('action')}")
        print(f"         Confidence: {intent.get('confidence', 0):.2f}")
        print()

    def on_estop(keyword):
        print(f"\n[MAIN] ESTOP triggered: {keyword}\n")

    node = VoiceNode(
        on_intent_resolved=on_intent,
        on_estop_triggered=on_estop,
    )

    node.start()

    try:
        while True:
            cmd = input().strip().lower()
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
            elif cmd == "barge":
                node.trigger_barge_in()
            else:
                print("[MAIN] Unknown command.")
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()


if __name__ == "__main__":
    main()

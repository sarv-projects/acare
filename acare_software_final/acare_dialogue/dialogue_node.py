from __future__ import annotations

import time
from dataclasses import dataclass, field

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from acare_msgs.msg import AuthRequest, Intent, RobotState, Transcript, ValidatedIntent, VisionResult

from acare_voice.assistant_agent import AssistantAgent
from acare_voice.fast_intent import parse_fast_intent
from acare_voice.normaliser import get_multi_tool_prompt, normalise


@dataclass
class SessionMemory:
    tools_fetched: list[dict] = field(default_factory=list)
    conversation_history: list[dict] = field(default_factory=list)
    current_task: dict = field(default_factory=dict)
    pending_clarification: bool = False
    last_command: str = ""
    last_ambiguous_tools: list[str] = field(default_factory=list)


class DialogueNode(Node):
    def __init__(self):
        super().__init__("dialogue_node")
        self.intent_pub = self.create_publisher(Intent, "/intent_result", 10)
        self.auth_req_pub = self.create_publisher(AuthRequest, "/auth_request", 10)
        self.tts_pub = self.create_publisher(String, "/tts_request", 10)
        self.create_subscription(Transcript, "/raw_transcript", self._on_transcript, 10)
        self.create_subscription(RobotState, "/robot_state", self._on_robot_state, 10)
        self.create_subscription(ValidatedIntent, "/validated_intent", self._on_validated_intent, 10)
        self.create_subscription(VisionResult, "/vision_result", self._on_vision_result, 10)
        self._assistant = self._build_assistant()
        self._robot_state = "LOGGED_OUT"
        self._memory = SessionMemory()
        self._max_history = 20
        self._active_user_id = ""
        self.get_logger().info("Dialogue node ready")

    def _build_assistant(self):
        try:
            return AssistantAgent()
        except Exception as exc:
            self.get_logger().warn(f"Assistant backend unavailable; using fixed responses: {exc}")
            return None

    def _say(self, text: str):
        self.tts_pub.publish(String(data=text))

    def _record_turn(self, role: str, content: str):
        self._memory.conversation_history.append({"role": role, "content": content, "timestamp": time.time()})
        if len(self._memory.conversation_history) > self._max_history:
            summary = " ".join(turn["content"][:30] for turn in self._memory.conversation_history[:10])
            self._memory.conversation_history = [{"role": "system", "content": f"Summary: {summary}"}] + self._memory.conversation_history[10:]

    def _publish_intent(self, tool: str, action: str, confidence: float):
        msg = Intent()
        msg.tool = tool or ""
        msg.action = action
        msg.destination = "user_handover"
        msg.confidence = float(confidence)
        self.intent_pub.publish(msg)

    def _publish_auth_request(self, request_type: str, transcript: str = "", tool: str = "", confidence: float = 0.0):
        msg = AuthRequest()
        msg.request_type = request_type
        msg.transcript = transcript
        msg.tool = tool
        msg.confidence = float(confidence)
        self.auth_req_pub.publish(msg)

    def _on_robot_state(self, msg: RobotState):
        self._robot_state = msg.state
        self._active_user_id = msg.active_user_id
        if msg.state == "LOGGED_OUT":
            self._memory = SessionMemory()

    def _on_validated_intent(self, msg: ValidatedIntent):
        self._memory.current_task = {"tool": msg.tool, "status": "validated"}
        self._memory.last_command = f"fetch {msg.tool}"

    def _on_vision_result(self, msg: VisionResult):
        if msg.found:
            self._memory.tools_fetched.append({"tool": msg.tool, "timestamp": time.time(), "zone": msg.zone})
            self._memory.current_task = {"tool": msg.tool, "status": "vision_found"}

    def _resolve_pronoun(self, text: str) -> str | None:
        """Resolve ``it``/``that``/``smaller``/``bigger`` references to a tool.

        H1 fix: use word-boundary matching so substrings inside other
        words (``kit``, ``split``, ``thermometer``) don't accidentally
        trigger pronoun resolution. The previous ``"it" in lowered``
        check would match ``"give me the kit"`` and resolve to the last
        fetched tool instead of failing through to normal parsing.
        """
        import re

        lowered = text.lower()

        def has_word(*words: str) -> bool:
            pattern = r"\b(" + "|".join(re.escape(w) for w in words) + r")\b"
            return re.search(pattern, lowered) is not None

        if has_word("it", "that", "this", "one"):
            if self._memory.current_task.get("tool"):
                return self._memory.current_task["tool"]
            if self._memory.tools_fetched:
                return self._memory.tools_fetched[-1]["tool"]
        if has_word("smaller", "bigger"):
            if self._memory.last_ambiguous_tools:
                return self._memory.last_ambiguous_tools[0]
        return None

    def _clarify_ambiguous(self, text: str, tools: list[str]):
        self._memory.pending_clarification = True
        self._memory.last_ambiguous_tools = tools
        if len(tools) >= 2:
            self._say(get_multi_tool_prompt(tools))
        elif "sharp" in text:
            self._say("Do you mean a scalpel or scissors?")
        elif "cutting" in text:
            self._say("Do you mean scissors or scalpel?")
        else:
            self._say("Which tool do you mean?")

    def _assistant_reply(self, text: str):
        if self._assistant is None:
            self._say("I am ACARE. Please look at the camera to log in.")
            return
        response = self._assistant.get_response(text)
        self._say(response)

    def _on_transcript(self, msg: Transcript):
        text = (msg.text or "").strip()
        if not text:
            return

        self._record_turn("user", text)
        self._memory.last_command = text

        if self._robot_state == "LOGGED_OUT":
            self._publish_auth_request("login_candidate", transcript=text)
            self._assistant_reply(text)
            return

        fast = parse_fast_intent(text, self._memory.current_task.get("tool"))
        if fast:
            if fast.get("type") == "multi_tool":
                tools = fast.get("detected_tools", [])
                self._clarify_ambiguous(text.lower(), tools)
                return
            tool = fast.get("tool") or self._resolve_pronoun(text) or ""
            self._publish_intent(tool, fast.get("action", "fetch"), fast.get("confidence", 0.95))
            if fast.get("action") == "fetch":
                self._publish_auth_request("validate_intent", transcript=text, tool=tool, confidence=fast.get("confidence", 0.95))
            return

        cleaned, multi_tool, found_tools = normalise(text)
        resolved_tool = self._resolve_pronoun(cleaned)
        if resolved_tool:
            self._publish_intent(resolved_tool, "fetch", 0.85)
            self._publish_auth_request("validate_intent", transcript=text, tool=resolved_tool, confidence=0.85)
            return

        if multi_tool:
            self._clarify_ambiguous(cleaned, found_tools)
            return

        if any(token in cleaned for token in ("sharp", "cutting thing")):
            self._clarify_ambiguous(cleaned, ["scalpel", "scissors"])
            return

        if found_tools:
            self._publish_intent(found_tools[0], "fetch", 0.72)
            self._publish_auth_request("validate_intent", transcript=text, tool=found_tools[0], confidence=0.72)
            return

        if self._memory.pending_clarification and self._memory.last_ambiguous_tools:
            for tool in self._memory.last_ambiguous_tools:
                if tool in cleaned:
                    self._memory.pending_clarification = False
                    self._publish_intent(tool, "fetch", 0.9)
                    self._publish_auth_request("validate_intent", transcript=text, tool=tool, confidence=0.9)
                    return

        self._assistant_reply(text)


def main(args=None):
    rclpy.init(args=args)
    node = DialogueNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

from typing import Optional, Dict, List
from dataclasses import dataclass, field
import time


@dataclass
class DialogueContext:
    last_intent: Optional[Dict] = None
    last_tool: Optional[str] = None
    last_transcript: str = ""
    pending_intent: Optional[Dict] = None
    turn_count: int = 0
    session_start_time: float = field(default_factory=time.time)
    tool_history: List[str] = field(default_factory=list)
    clarification_mode: bool = False
    awaiting_confirmation: bool = False

    def add_tool(self, tool: str):
        self.tool_history.append(tool)
        self.last_tool = tool
        if len(self.tool_history) > 10:
            self.tool_history = self.tool_history[-10:]

    def clear_pending(self):
        self.pending_intent = None
        self.clarification_mode = False
        self.awaiting_confirmation = False


class DialogueManager:

    def __init__(self):
        self.context = DialogueContext()
        self._max_turns = 30
        self._timeout_seconds = 10.0

    def process_intent(self, intent: Dict, transcript: str) -> Dict:
        self.context.turn_count += 1
        self.context.last_transcript = transcript

        intent_type = intent.get("type", "command")

        if self.context.awaiting_confirmation:
            return self._handle_confirmation_response(intent)

        if intent_type == "follow_up":
            return self._resolve_follow_up(intent)

        if intent_type == "multi_tool":
            return self._handle_multi_tool(intent)

        if intent_type == "command":
            tool = intent.get("tool")
            if tool:
                self.context.add_tool(tool)
                self.context.last_intent = intent
            return intent

        if intent_type in ("estop", "resume", "cancel"):
            return intent

        return intent

    def _handle_confirmation_response(self, intent: Dict) -> Dict:
        action = intent.get("action", "")

        if action == "confirm":
            if self.context.pending_intent:
                confirmed_intent = self.context.pending_intent.copy()
                confirmed_intent["confidence"] = 0.95
                confirmed_intent["confirmed"] = True
                self.context.clear_pending()
                tool = confirmed_intent.get("tool")
                if tool:
                    self.context.add_tool(tool)
                return confirmed_intent
            else:
                return {"type": "error", "message": "No pending command to confirm."}

        elif action == "reject":
            self.context.clear_pending()
            return {"type": "clarification_rejected", "message": "What would you like instead?"}

        else:
            self.context.clear_pending()
            return intent

    def _resolve_follow_up(self, intent: Dict) -> Dict:
        tool = intent.get("tool")

        if not tool and self.context.last_tool:
            tool = self.context.last_tool
            intent["tool"] = tool
            intent["resolved_from_context"] = True

        if tool:
            self.context.add_tool(tool)
            self.context.last_intent = intent

        return intent

    def _handle_multi_tool(self, intent: Dict) -> Dict:
        tools = intent.get("detected_tools", [])

        if len(tools) == 2:
            first_tool = tools[0]
            pending = {
                "tool": first_tool,
                "action": "fetch",
                "confidence": 0.9,
                "next_tools": tools[1:]
            }
            self.context.pending_intent = pending
            self.context.awaiting_confirmation = True

            return {
                "type": "multi_tool_clarify",
                "message": f"One at a time. Which first \u2014 {tools[0]} or {tools[1]}?",
                "detected_tools": tools,
                "requires_clarification": True
            }
        else:
            return {
                "type": "multi_tool_clarify",
                "message": "One at a time. Which tool would you like first?",
                "detected_tools": tools,
                "requires_clarification": True
            }

    def set_pending_confirmation(self, intent: Dict):
        self.context.pending_intent = intent
        self.context.awaiting_confirmation = True
        self.context.clarification_mode = True

    def get_clarification_prompt(self, tool: str, confidence: float) -> str:
        if confidence >= 0.5:
            return f"Did you mean the {tool}? Say yes to confirm."
        else:
            return f"I heard something about a {tool}. Could you repeat that?"

    def get_context_summary(self) -> str:
        return {
            "turn_count": self.context.turn_count,
            "last_tool": self.context.last_tool,
            "tool_history": self.context.tool_history,
            "awaiting_confirmation": self.context.awaiting_confirmation,
            "pending_intent": self.context.pending_intent
        }

    def reset(self):
        self.context = DialogueContext()

    def is_awaiting_confirmation(self) -> bool:
        return self.context.awaiting_confirmation

    def get_last_tool(self) -> Optional[str]:
        return self.context.last_tool

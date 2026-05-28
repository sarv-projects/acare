# acare_planner/agentic_planner.py
# Spec Reference: Section XII (Task Planner Pipeline — Agentic Decision Layer)
#
# Agentic decision layer using NVIDIA NIM (primary) with Groq fallback.
# Proposes adaptive search strategies and recovery actions.
# ALL proposals are validated by SafetyKernel before execution.
#
# Primary: nvidia/llama-3.3-nemotron-super-49b-v1 via NIM (40 RPM free)
#   - Strong reasoning, tool-calling fine-tuned, 128K context
#   - OpenAI-compatible endpoint at integrate.api.nvidia.com
#
# Fallback: llama-3.3-70b-versatile via Groq (30 RPM free, 300+ tok/s)
#   - Used when NIM is unavailable or rate-limited
#
# Deterministic fallbacks exist for EVERY decision.
# LLM failure NEVER stops the robot — fallback activates immediately.
#
# Rate limit awareness:
#   NIM: 40 RPM (no daily cap documented)
#   Groq 70B: 30 RPM, 14,400 RPD
#   At ~3-5 calls/task → well within both budgets.

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple

MAX_RETRIES = 3

# ---------------------------------------------------------------------------
# Decision JSON schema — strict mode (spec Section XII)
# ---------------------------------------------------------------------------
DECISION_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "planner_decision",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "decision_type": {
                    "type": "string",
                    "enum": [
                        "SEARCH_STRATEGY", "VISION_RECOVERY", "GRASP_RECOVERY",
                        "IK_RECOVERY", "HANDOVER_RECOVERY", "ABORT"
                    ]
                },
                "reasoning": {"type": "string"},
                "action": {
                    "type": "string",
                    "enum": [
                        "RETRY_UNIFORM_SEARCH", "ASK_USER_CONFIRM_LOCATION",
                        "ABORT_TOOL_NOT_FOUND", "RETRY_GRASP_REPOSITION",
                        "RETRY_GRASP_FORCE_INCREASE", "ABORT_GRASP_FAILED",
                        "RETRY_IK_ALTERNATE_ORIENTATION", "RETRY_IK_NEXT_CANDIDATE",
                        "ABORT_IK_FAILED", "HANDOVER_Z_UP", "HANDOVER_Z_DOWN",
                        "HANDOVER_VOICE_HAND_ONLY", "SEARCH_PRIORITY_ZONES"
                    ]
                },
                "tts_message": {"type": "string"},
                "params": {
                    "type": "object",
                    "properties": {
                        "force_delta_n":         {"type": "number"},
                        "z_offset_m":            {"type": "number"},
                        "rotation_deg":          {"type": "number"},
                        "priority_zones":        {"type": "array", "items": {"type": "string"}},
                        "reset_probability_map": {"type": "boolean"}
                    },
                    "required": ["force_delta_n", "z_offset_m", "rotation_deg",
                                 "priority_zones", "reset_probability_map"],
                    "additionalProperties": False
                }
            },
            "required": ["decision_type", "reasoning", "action", "tts_message", "params"],
            "additionalProperties": False
        }
    }
}

PLANNER_SYSTEM_PROMPT = """You are the agentic decision layer of ACARE — an Autonomous Clinical Assistance Robot
operating in a surgical environment. You orchestrate task recovery and search strategy for a
6-DOF robotic arm that fetches sterile instruments for authenticated surgical staff.

HARD RULES you must never violate:
- Never suggest bypassing authentication or safety checks
- Never suggest moving outside workspace bounds
- Never suggest gripper force above 10N
- Only suggest actions from the allowed action enum
- If uncertain, choose ABORT over unsafe continuation
- Keep tts_message brief (1-2 sentences), professional, clinical tone

For the final attempt (attempt == max_retries): tts_message MUST warn staff this is the last try.
After all retries exhausted: tts_message must clearly state inability and suggest manual procedure."""


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class UserProfile:
    user_id: str = ""
    name: str = ""
    handover_z_offset: float = 0.0
    preferred_zones: Dict[str, str] = field(default_factory=dict)
    last_login: str = ""


@dataclass
class TaskContext:
    tool_requested: str = ""
    tool_canonical: str = ""
    zone_found: str = ""
    grasp_point: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    alternate_orientation_tried: bool = False
    detection_candidates: List[Dict] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Agentic Planner
# ---------------------------------------------------------------------------

class AgenticPlanner:
    """
    Proposes adaptive strategies via NVIDIA NIM (primary) or Groq (fallback).
    All proposals validated by SafetyKernel before execution.
    Falls back to deterministic decisions on any LLM failure.
    """

    # Primary: NVIDIA NIM — strong reasoning, tool-calling fine-tuned
    NIM_MODEL = "nvidia/llama-3.3-nemotron-super-49b-v1"
    NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"

    # Fallback: Groq — fast, reliable
    GROQ_MODEL = "llama-3.3-70b-versatile"

    def __init__(self, logger=None):
        self.logger = logger
        self._nim_client = None
        self._groq_client = None
        self._init_clients()
        self.user_profiles: Dict[str, UserProfile] = {}
        self.time_patterns: Dict[int, Dict[str, str]] = {}  # hour → {tool: zone}

    def _init_clients(self):
        """Initialize NIM (primary) and Groq (fallback) clients."""
        # NIM client — uses OpenAI SDK with custom base_url
        try:
            from openai import OpenAI
            nim_key = os.environ.get("NVIDIA_NIM_API_KEY", "")
            if nim_key:
                self._nim_client = OpenAI(
                    base_url=self.NIM_BASE_URL,
                    api_key=nim_key,
                )
        except Exception as e:
            if self.logger:
                self.logger.info(f"AgenticPlanner: NIM client init skipped: {e}")

        # Groq fallback client
        try:
            from groq import Groq
            groq_key = os.environ.get("GROQ_API_KEY", "")
            if groq_key:
                self._groq_client = Groq(api_key=groq_key)
        except Exception as e:
            if self.logger:
                self.logger.info(f"AgenticPlanner: Groq client init skipped: {e}")

        if self._nim_client is None and self._groq_client is None:
            if self.logger:
                self.logger.warn("AgenticPlanner: No LLM client available — using deterministic fallbacks only")

    def _call_llm(self, messages: List[Dict], reasoning_level: str = "low") -> Optional[Dict]:
        """
        Calls NIM (primary) or Groq (fallback) with JSON schema output.
        Returns parsed dict or None on any failure.
        Never raises — robot must not crash on LLM failure.
        """
        system = PLANNER_SYSTEM_PROMPT + f"\n\nReasoning: {reasoning_level}"
        full_messages = [{"role": "system", "content": system}] + messages

        # Try NIM first (stronger reasoning)
        if self._nim_client is not None:
            try:
                response = self._nim_client.chat.completions.create(
                    model=self.NIM_MODEL,
                    messages=full_messages,
                    response_format={"type": "json_object"},
                    temperature=0.1,
                    max_tokens=512,
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                if self.logger:
                    self.logger.info(f"AgenticPlanner NIM call failed: {e} — trying Groq fallback")

        # Groq fallback (fast, reliable)
        if self._groq_client is not None:
            try:
                response = self._groq_client.chat.completions.create(
                    model=self.GROQ_MODEL,
                    messages=full_messages,
                    response_format={"type": "json_object"},
                    temperature=0.1,
                    max_tokens=512,
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                if self.logger:
                    self.logger.warn(f"AgenticPlanner Groq fallback also failed: {e} — using deterministic")

        return None

    # -----------------------------------------------------------------------
    # Search strategy (reasoning: low)
    # -----------------------------------------------------------------------

    def propose_search_strategy(self, tool: str, user_id: str,
                                 current_hour: int, attempt_number: int) -> Dict:
        profile = self.user_profiles.get(user_id)
        hour_pref = self.time_patterns.get(current_hour, {}).get(tool)
        user_pref = profile.preferred_zones.get(tool) if profile else None

        context = json.dumps({
            "tool": tool, "attempt_number": attempt_number,
            "current_hour": current_hour,
            "time_based_zone_hint": hour_pref,
            "user_preferred_zone": user_pref,
            "failure_type": "SEARCH_STRATEGY",
        })
        decision = self._call_llm([{"role": "user", "content": context}], "low")
        if decision is None:
            priority_zones = [z for z in [user_pref, hour_pref] if z]
            return {
                "decision_type": "SEARCH_STRATEGY",
                "action": "SEARCH_PRIORITY_ZONES",
                "reasoning": "LLM unavailable — using probability map default",
                "tts_message": f"Searching for {tool}.",
                "params": {
                    "priority_zones": priority_zones,
                    "reset_probability_map": False,
                    "force_delta_n": 0.0, "z_offset_m": 0.0, "rotation_deg": 0.0,
                }
            }
        return decision

    # -----------------------------------------------------------------------
    # Vision recovery (reasoning: high)
    # -----------------------------------------------------------------------

    def propose_vision_recovery(self, tool: str, attempt: int,
                                 safety_severity: str, network_ok: bool) -> Optional[Dict]:
        if attempt > MAX_RETRIES:
            return None
        is_last = (attempt == MAX_RETRIES)
        context = json.dumps({
            "tool": tool, "failure_type": "TOOL_NOT_FOUND",
            "attempt_number": attempt, "max_retries": MAX_RETRIES,
            "is_final_attempt": is_last,
            "safety_severity": safety_severity, "network_ok": network_ok,
            "instruction": (
                "FINAL attempt. tts_message must warn staff."
                if is_last else "Propose next recovery step."
            )
        })
        decision = self._call_llm([{"role": "user", "content": context}], "high")
        if decision is None:
            fallbacks = {
                1: {"decision_type": "VISION_RECOVERY", "action": "RETRY_UNIFORM_SEARCH",
                    "reasoning": "First retry: search all zones uniformly",
                    "tts_message": f"Searching again for {tool}.",
                    "params": {"reset_probability_map": True, "priority_zones": [],
                               "force_delta_n": 0.0, "z_offset_m": 0.0, "rotation_deg": 0.0}},
                2: {"decision_type": "VISION_RECOVERY", "action": "ASK_USER_CONFIRM_LOCATION",
                    "reasoning": "Second retry: ask user",
                    "tts_message": f"I still cannot find the {tool}. Can you confirm it is on the tray?",
                    "params": {"reset_probability_map": False, "priority_zones": [],
                               "force_delta_n": 0.0, "z_offset_m": 0.0, "rotation_deg": 0.0}},
                3: {"decision_type": "VISION_RECOVERY", "action": "ABORT_TOOL_NOT_FOUND",
                    "reasoning": "Max retries reached",
                    "tts_message": f"Last attempt — searching one final time for the {tool}.",
                    "params": {"reset_probability_map": True, "priority_zones": [],
                               "force_delta_n": 0.0, "z_offset_m": 0.0, "rotation_deg": 0.0}},
            }
            return fallbacks.get(attempt)
        return decision

    # -----------------------------------------------------------------------
    # Grasp recovery (reasoning: high)
    # -----------------------------------------------------------------------

    def propose_grasp_recovery(self, tool: str, attempt: int,
                                gripper_force: float, safety_severity: str) -> Optional[Dict]:
        if attempt > MAX_RETRIES:
            return None
        is_last = (attempt == MAX_RETRIES)
        context = json.dumps({
            "tool": tool, "failure_type": "GRASP_FAILED",
            "attempt_number": attempt, "max_retries": MAX_RETRIES,
            "is_final_attempt": is_last,
            "current_gripper_force": gripper_force,
            "safety_severity": safety_severity,
            "instruction": "FINAL attempt. Force must stay below 10N." if is_last else "Force must stay below 10N."
        })
        decision = self._call_llm([{"role": "user", "content": context}], "high")
        if decision is None:
            fallbacks = {
                1: {"decision_type": "GRASP_RECOVERY", "action": "RETRY_GRASP_REPOSITION",
                    "reasoning": "First retry: reposition approach",
                    "tts_message": f"Adjusting grip on {tool}. Retrying.",
                    "params": {"force_delta_n": 0.0, "rotation_deg": 15.0,
                               "priority_zones": [], "z_offset_m": 0.0,
                               "reset_probability_map": False}},
                2: {"decision_type": "GRASP_RECOVERY", "action": "RETRY_GRASP_FORCE_INCREASE",
                    "reasoning": "Second retry: slight force increase",
                    "tts_message": f"Retrying grasp of {tool} with adjusted force.",
                    "params": {"force_delta_n": 1.0, "rotation_deg": 0.0,
                               "priority_zones": [], "z_offset_m": 0.0,
                               "reset_probability_map": False}},
                3: {"decision_type": "GRASP_RECOVERY", "action": "RETRY_GRASP_FORCE_INCREASE",
                    "reasoning": "Final retry: max safe force",
                    "tts_message": f"Last attempt to grasp the {tool}. Please ensure it is correctly positioned.",
                    "params": {"force_delta_n": 2.0, "rotation_deg": 0.0,
                               "priority_zones": [], "z_offset_m": 0.0,
                               "reset_probability_map": False}},
            }
            return fallbacks.get(attempt)
        return decision

    # -----------------------------------------------------------------------
    # IK recovery (reasoning: high)
    # -----------------------------------------------------------------------

    def propose_ik_recovery(self, tool: str, attempt: int,
                             alternate_tried: bool,
                             candidate_count: int,
                             safety_severity: str) -> Optional[Dict]:
        if attempt > MAX_RETRIES:
            return None
        is_last = (attempt == MAX_RETRIES)
        context = json.dumps({
            "tool": tool, "failure_type": "IK_FAILED",
            "attempt_number": attempt, "max_retries": MAX_RETRIES,
            "is_final_attempt": is_last,
            "alternate_orientation_tried": alternate_tried,
            "remaining_candidates": candidate_count,
            "safety_severity": safety_severity,
            "instruction": "FINAL attempt. If no candidates remain, action must be ABORT_IK_FAILED." if is_last else ""
        })
        decision = self._call_llm([{"role": "user", "content": context}], "high")
        if decision is None:
            if attempt == 1 and not alternate_tried:
                return {"decision_type": "IK_RECOVERY",
                        "action": "RETRY_IK_ALTERNATE_ORIENTATION",
                        "reasoning": "Try 90° rotation",
                        "tts_message": f"Adjusting approach angle for {tool}.",
                        "params": {"rotation_deg": 90.0, "force_delta_n": 0.0,
                                   "z_offset_m": 0.0, "priority_zones": [],
                                   "reset_probability_map": False}}
            if candidate_count > 0:
                prefix = f"Last attempt to reach the {tool}. " if is_last else ""
                return {"decision_type": "IK_RECOVERY",
                        "action": "RETRY_IK_NEXT_CANDIDATE",
                        "reasoning": "Try next candidate",
                        "tts_message": f"{prefix}Trying alternate position for {tool}.",
                        "params": {"rotation_deg": 0.0, "force_delta_n": 0.0,
                                   "z_offset_m": 0.0, "priority_zones": [],
                                   "reset_probability_map": False}}
            return {"decision_type": "IK_RECOVERY",
                    "action": "ABORT_IK_FAILED",
                    "reasoning": "No candidates remain",
                    "tts_message": f"Unable to reach the {tool}. Please reposition it and try again.",
                    "params": {"rotation_deg": 0.0, "force_delta_n": 0.0,
                               "z_offset_m": 0.0, "priority_zones": [],
                               "reset_probability_map": False}}
        return decision

    # -----------------------------------------------------------------------
    # Handover face recovery (reasoning: low)
    # -----------------------------------------------------------------------

    def propose_handover_face_recovery(self, user_name: str, tool: str,
                                        attempt: int, current_z: float) -> Dict:
        """Always returns a dict — handover never aborts on face failure alone."""
        context = json.dumps({
            "user_name": user_name, "tool": tool,
            "failure_type": "FACE_VERIFY_FAILED",
            "attempt_number": attempt, "max_retries": MAX_RETRIES,
            "current_z_m": current_z,
            "instruction": "Attempt 3: must use HANDOVER_VOICE_HAND_ONLY." if attempt >= MAX_RETRIES else ""
        })
        decision = self._call_llm([{"role": "user", "content": context}], "low")
        if decision is None or attempt >= MAX_RETRIES:
            if attempt >= MAX_RETRIES:
                return {"decision_type": "HANDOVER_RECOVERY",
                        "action": "HANDOVER_VOICE_HAND_ONLY",
                        "reasoning": "3 face attempts failed — voice+hand fallback",
                        "tts_message": "Face verification unavailable. Proceeding with voice and hand confirmation only.",
                        "params": {"z_offset_m": 0.0, "force_delta_n": 0.0,
                                   "rotation_deg": 0.0, "priority_zones": [],
                                   "reset_probability_map": False}}
            fallbacks = {
                1: {"decision_type": "HANDOVER_RECOVERY", "action": "HANDOVER_Z_UP",
                    "reasoning": "Move arm up to find face",
                    "tts_message": "Please look at the camera.",
                    "params": {"z_offset_m": 0.05, "force_delta_n": 0.0,
                               "rotation_deg": 0.0, "priority_zones": [],
                               "reset_probability_map": False}},
                2: {"decision_type": "HANDOVER_RECOVERY", "action": "HANDOVER_Z_DOWN",
                    "reasoning": "Move arm down to find face",
                    "tts_message": "Please face the camera directly.",
                    "params": {"z_offset_m": -0.05, "force_delta_n": 0.0,
                               "rotation_deg": 0.0, "priority_zones": [],
                               "reset_probability_map": False}},
            }
            return fallbacks.get(attempt, fallbacks[1])
        return decision

    # -----------------------------------------------------------------------
    # Learning
    # -----------------------------------------------------------------------

    def learn_from_success(self, context: TaskContext, user_id: str):
        profile = self.user_profiles.setdefault(user_id, UserProfile(user_id=user_id))
        if context.zone_found:
            profile.preferred_zones[context.tool_canonical] = context.zone_found
        hour = datetime.now().hour
        self.time_patterns.setdefault(hour, {})[context.tool_canonical] = context.zone_found
        if self.logger:
            self.logger.info(
                f"AgenticPlanner learned: {context.tool_canonical} → "
                f"{context.zone_found} for user {user_id} at hour {hour}"
            )

    def learn_height_adjustment(self, user_id: str, command: str):
        profile = self.user_profiles.setdefault(user_id, UserProfile(user_id=user_id))
        delta = 0.05 if command == "higher" else -0.05
        profile.handover_z_offset = max(-0.15, min(0.15, profile.handover_z_offset + delta))

    def get_handover_z_offset(self, user_id: str) -> float:
        profile = self.user_profiles.get(user_id)
        return profile.handover_z_offset if profile else 0.0

# acare_planner/agentic_planner.py
import json
import os
import time
from typing import Optional

from acare_bringup.paths import load_env

load_env()

from .state_snapshot import TaskSnapshot
from .agent_schema import validate_agentic_decision, ToolCallSchema

# Degradation logging
from acare_msgs.msg import LogEvent

PLANNER_SYSTEM_PROMPT = """You are the task executor for ACARE, a surgical instrument fetch robot.
You receive a state snapshot and return exactly ONE tool call as JSON.
HARD RULES:
* Return ONLY a JSON object. No markdown. No explanation outside JSON.
* Call exactly one tool per turn. Never plan ahead.
* Never repeat an action that appears in tried_and_failed.
* Never fabricate tools or parameters not in available_tools.
* If budget.calls_remaining <= 2 and task is not near completion, call abort_task.
* Speech must be brief (<20 words), clinical, professional. No medical advice.
* NEVER move the arm to a position not listed in available arm positions.
* Follow the recovery ladders EXACTLY. Do not improvise or skip rungs.
TASK SEQUENCE:
1. vision_scan -> find the tool
2. arm_move(PREGRASP) -> above tool
3. arm_move(GRASP_POINT) -> descend to tool
4. gripper_close(NORMAL) -> grasp
5. arm_move(FACE_HEIGHT) -> face user
6. detect_face -> verify identity
7. arm_move(PRESENTATION) -> present tool
8. speak -> instruct user
9. detect_hand -> user reaches
10. ask_user(expect=CONFIRM) -> voice confirm
11. gripper_open -> release
12. complete_task
RECOVERY LADDERS — follow in strict order, never skip rungs:
VISION FAILURE (vision_scan returns NOT_FOUND):
  Rung 1: If user_prior.preferred_zone exists and not yet tried -> vision_scan({'zone': preferred_zone})
  Rung 2: vision_scan({'zone': 'AUTO'}) — queries Bayesian probability map
  Rung 3: If AUTO fails -> ask_user("I cannot find the [tool]. Is it on the tray?")
  Rung 4: If user responds with location -> vision_scan({'zone': that_zone})
  Rung 5: If user says no or timeout -> abort_task("Unable to locate [tool]")
GRASP FAILURE (gripper_close returns SLIP_DETECTED):
  Rung 1: gripper_close(FIRM) — same position, more force
  Rung 2: arm_approach(SIDE_LEFT) then arm_move(PREGRASP) then arm_move(GRASP_POINT) then gripper_close(FIRM) — different angle
  Rung 3: If detection_candidates exist in snapshot -> arm_move to next candidate, repeat grasp
  Rung 4: abort_task("Unable to grasp [tool]")
ARM UNREACHABLE (arm_move returns UNREACHABLE):
  Rung 1: arm_approach(SIDE_LEFT) then retry arm_move
  Rung 2: arm_approach(SIDE_RIGHT) then retry arm_move
  Rung 3: If detection_candidates exist -> arm_move to next candidate
  Rung 4: abort_task("[tool] is out of reach")
FACE DETECTION FAILURE (detect_face returns NO_FACE or WRONG_FACE):
  Rung 1: speak("Please look at the camera") then detect_face
  Rung 2: speak("Please face the camera directly") then detect_face
  Rung 3: Skip face. Proceed to arm_move(PRESENTATION). Face is advisory.
HAND DETECTION FAILURE (detect_hand returns NO_HAND):
  Rung 1: speak("Please reach for the tool") then detect_hand
  Rung 2: speak("Hold your hand near the gripper") then detect_hand
  Rung 3: abort_task("Handover failed - no hand detected")
VOICE CONFIRM FAILURE (ask_user returns TIMEOUT):
  Rung 1: speak("Say take to receive") then ask_user(expect=CONFIRM)
  Rung 2: abort_task("No voice confirmation received")
ESTOP (any tool returns ESTOP):
  -> abort_task("ESTOP") immediately. No recovery. No retry.
RESPONSE FORMAT:
{
  "thought": "brief reason, max 1 sentence",
  "tool": "tool_name",
  "params": {"param1": "value1"},
  "speak": "optional tts message or null"
}
EXAMPLES:
State: task_phase=SEARCHING, zones_searched=[], user_prior.preferred_zone=C
Response: {"thought":"User prefers zone C, start there","tool":"vision_scan","params":{"zone":"C"},"speak":null}
State: task_phase=SEARCHING, last_action=vision_scan(A) NOT_FOUND, zones_searched=[A,B]
Response: {"thought":"A and B failed, try C","tool":"vision_scan","params":{"zone":"C"},"speak":null}
State: task_phase=GRASPING, last_action=gripper_close(NORMAL) SLIP_DETECTED
Response: {"thought":"Normal grip slipped, increase firmness","tool":"gripper_close","params":{"firmness":"FIRM"},"speak":"Adjusting grip. One moment."}
State: task_phase=HANDOVER, last_action=detect_face() NO_FACE, action_history has 2 face failures
Response: {"thought":"Face failed twice, skip and proceed to present","tool":"arm_move","params":{"position":"PRESENTATION"},"speak":"Proceeding with voice and hand verification."}
"""

class AgenticPlanner:
    def __init__(self, logger=None, cfg=None):
        self.logger = logger
        self._nim_client = None
        self._groq_client = None
        self._init_clients()
        # Degradation tracking
        self._last_call_info = {}        # tier, error, latency_ms, tool_called
        self._consecutive_deterministic = 0
        # Circuit breaker for repeated API failures (M12)
        self._api_failure_count = 0
        self._circuit_open = False
        self._circuit_open_until = 0.0
        # Adaptive task timeout (M6) — load from config, default 180s
        cfg = cfg or {}
        self.task_timeout = cfg.get('planner', {}).get('task_timeout_s', 180.0)

    def _init_clients(self):
        try:
            from openai import OpenAI
            nim_key = os.environ.get("NVIDIA_NIM_API_KEY") or os.environ.get("NVIDIA_API_KEY", "")
            if nim_key:
                self._nim_client = OpenAI(
                    base_url="https://integrate.api.nvidia.com/v1",
                    api_key=nim_key,
                    timeout=4.0
                )
        except Exception as e:
            if self.logger: self.logger.info(f"NIM client init skipped: {e}")

        try:
            from openai import OpenAI
            groq_key = os.environ.get("GROQ_API_KEY", "")
            if groq_key:
                self._groq_client = OpenAI(
                    base_url="https://api.groq.com/openai/v1",
                    api_key=groq_key,
                    timeout=4.0
                )
        except Exception as e:
            if self.logger: self.logger.info(f"Groq client init skipped: {e}")

    def _call_llm(self, snapshot: TaskSnapshot) -> Optional[ToolCallSchema]:
        messages = [
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            snapshot.to_message()
        ]
        start_t = time.monotonic()

        # Circuit breaker (M12): skip LLM if open and within cooldown
        if self._circuit_open:
            if time.monotonic() < self._circuit_open_until:
                if self.logger:
                    self.logger.info("Circuit breaker open, skipping LLM")
                decision = self._deterministic_next_step(snapshot)
                elapsed_ms = int((time.monotonic() - start_t) * 1000)
                self._last_call_info = {'tier': 'Deterministic', 'error': 'Circuit breaker open',
                                        'latency_ms': elapsed_ms,
                                        'tool_called': decision.tool if decision else ''}
                return decision
            else:
                # Cooldown expired, close circuit
                self._circuit_open = False
                self._api_failure_count = 0

        if self._nim_client:
            try:
                response = self._nim_client.chat.completions.create(
                    model="nvidia/llama-3.3-nemotron-super-49b-v1",
                    messages=messages,
                    response_format={"type": "json_object"},
                    temperature=0.1,
                    max_tokens=256
                )
                decision = validate_agentic_decision(json.loads(response.choices[0].message.content))
                elapsed_ms = int((time.monotonic() - start_t) * 1000)
                self._last_call_info = {'tier': 'NIM', 'error': '', 'latency_ms': elapsed_ms,
                                        'tool_called': decision.tool if decision else ''}
                # Circuit breaker (M12): reset on NIM success
                self._api_failure_count = 0
                self._circuit_open = False
                return decision
            except Exception as e:
                err_msg = str(e)
                if self.logger: self.logger.info(f"NIM call failed: {e}")

        if self._groq_client:
            try:
                response = self._groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    response_format={"type": "json_object"},
                    temperature=0.1,
                    max_tokens=256
                )
                decision = validate_agentic_decision(json.loads(response.choices[0].message.content))
                elapsed_ms = int((time.monotonic() - start_t) * 1000)
                self._last_call_info = {'tier': 'Groq', 'error': f'NIM->Groq: {err_msg}',
                                        'latency_ms': elapsed_ms,
                                        'tool_called': decision.tool if decision else ''}
                # Circuit breaker (M12): reset on Groq success
                self._api_failure_count = 0
                self._circuit_open = False
                return decision
            except Exception as e:
                err_msg = str(e)
                if self.logger: self.logger.warning(f"Groq call failed: {e}")

        # Tier 3: Deterministic fallback
        decision = self._deterministic_next_step(snapshot)
        elapsed_ms = int((time.monotonic() - start_t) * 1000)
        self._last_call_info = {'tier': 'Deterministic', 'error': f'Groq->Det: {err_msg}',
                                'latency_ms': elapsed_ms,
                                'tool_called': decision.tool if decision else ''}
        return decision

    def _deterministic_next_step(self, snapshot: TaskSnapshot) -> ToolCallSchema:
        """Zero-LLM fallback logic based on the happy-path / recovery ladders."""
        phase = snapshot.objective.task_phase
        last_action = snapshot.last_action.tool_call
        last_result = snapshot.last_action.result
        
        # Simplified deterministic ladder
        if phase == "SEARCHING":
            if last_result == "SUCCESS":
                return validate_agentic_decision({"thought": "Found", "tool": "arm_move", "params": {"position": "PREGRASP"}, "speak": ""})
            zones = ['A', 'B', 'C']
            for z in zones:
                if f"vision_scan({{'zone': '{z}'}})" not in snapshot.tried_and_failed:
                    return validate_agentic_decision({"thought": f"Scan {z}", "tool": "vision_scan", "params": {"zone": z}, "speak": ""})
            return validate_agentic_decision({"thought": "All zones failed", "tool": "abort_task", "params": {"reason": "Could not find tool"}, "speak": ""})
            
        if phase == "GRASPING":
            if "arm_move" in last_action and last_result == "SUCCESS":
                if "PREGRASP" in last_action:
                    return validate_agentic_decision({"thought": "Move to grasp", "tool": "arm_move", "params": {"position": "GRASP_POINT"}, "speak": ""})
                if "GRASP_POINT" in last_action:
                    return validate_agentic_decision({"thought": "Close gripper", "tool": "gripper_close", "params": {"firmness": "NORMAL"}, "speak": ""})
                if "FACE_HEIGHT" in last_action:
                    return validate_agentic_decision({"thought": "Verify face", "tool": "detect_face", "params": {}, "speak": ""})
            if "gripper_close" in last_action:
                if last_result == "SUCCESS":
                    return validate_agentic_decision({"thought": "Grasp success, to face", "tool": "arm_move", "params": {"position": "FACE_HEIGHT"}, "speak": ""})
                if last_result == "SLIP_DETECTED":
                    return validate_agentic_decision({"thought": "Retry firm", "tool": "gripper_close", "params": {"firmness": "FIRM"}, "speak": ""})
            if "detect_face" in last_action:
                return validate_agentic_decision({"thought": "Present", "tool": "arm_move", "params": {"position": "PRESENTATION"}, "speak": ""})
            return validate_agentic_decision({"thought": "Grasp failed", "tool": "abort_task", "params": {"reason": "Grasp failed"}, "speak": ""})
            
        if phase == "HANDOVER":
            if "arm_move" in last_action and "PRESENTATION" in last_action and last_result == "SUCCESS":
                return validate_agentic_decision({"thought": "Wait hand", "tool": "detect_hand", "params": {}, "speak": ""})
            if "detect_hand" in last_action:
                if last_result == "SUCCESS":
                    return validate_agentic_decision({"thought": "Ask voice", "tool": "ask_user", "params": {"question": "Take it", "expect": "CONFIRM"}, "speak": ""})
                else:
                    return validate_agentic_decision({"thought": "Hand fail", "tool": "abort_task", "params": {"reason": "No hand"}, "speak": ""})
            if "ask_user" in last_action:
                if last_result == "SUCCESS":
                    return validate_agentic_decision({"thought": "Release", "tool": "gripper_open", "params": {}, "speak": ""})
                else:
                    return validate_agentic_decision({"thought": "Voice fail", "tool": "abort_task", "params": {"reason": "No confirm"}, "speak": ""})
            if "gripper_open" in last_action and last_result == "SUCCESS":
                return validate_agentic_decision({"thought": "Done", "tool": "complete_task", "params": {}, "speak": ""})
                
        return validate_agentic_decision({"thought": "Fallback abort", "tool": "abort_task", "params": {"reason": "Deterministic fallback failed"}, "speak": ""})

    def run_task(self, node, tool_kernel, snapshot: TaskSnapshot):
        """The main agentic loop with degradation logging."""
        # Adaptive task deadline (M6) — compute budget based on remaining work
        phase = snapshot.objective.task_phase
        zones_searched = len(getattr(snapshot, 'zones_searched', []))
        num_searches = max(1, 3 - zones_searched) if phase == "SEARCHING" else 0
        if phase == "SEARCHING":
            num_moves = 4  # PREGRASP, GRASP_POINT, FACE_HEIGHT, PRESENTATION
        elif phase == "GRASPING":
            num_moves = 3
        elif phase == "HANDOVER":
            num_moves = 1
        else:
            num_moves = 0
        adaptive_budget = (num_searches * 60) + (num_moves * 30) + 30
        final_timeout = max(adaptive_budget, self.task_timeout)
        task_deadline = time.monotonic() + final_timeout
        while snapshot.budget.calls_remaining > 0:
            if time.monotonic() > task_deadline:
                node._speak("Task timed out. Aborting.")
                try:
                    node.log_pub.publish(LogEvent(
                        event_type='TASK_TIMEOUT',
                        user_id='',
                        tool=snapshot.objective.tool,
                        state=snapshot.objective.task_phase,
                        description='Task exceeded 120s deadline',
                        timestamp=int(time.time() * 1000),
                        safety_severity='WARNING'
                    ))
                except Exception:
                    pass
                if node.world.arm_holding:
                    tool_kernel._tool_abort_task("task_timeout")
                break

            if node._estop_active.is_set():
                break

            decision = self._call_llm(snapshot)
            if node._estop_active.is_set():
                break
                
            if not decision:
                break

            # Degradation logging: publish LogEvent for non-NIM tiers
            tier = self._last_call_info.get('tier', 'Unknown')
            if tier != 'NIM':
                try:
                    node.log_pub.publish(LogEvent(
                        event_type='LLM_FALLBACK',
                        user_id='',
                        tool=self._last_call_info.get('tool_called', ''),
                        state=snapshot.objective.task_phase,
                        description=self._last_call_info.get('error', ''),
                        timestamp=int(time.time() * 1000),
                        safety_severity='OK'
                    ))
                except Exception:
                    pass

            # Circuit breaker (M12): track API failures, open circuit after 3 consecutive
            if tier == 'Deterministic':
                self._api_failure_count += 1
                self._consecutive_deterministic += 1
                if self._api_failure_count >= 3 and not self._circuit_open:
                    self._circuit_open = True
                    self._circuit_open_until = time.monotonic() + 60.0
                    try:
                        node.log_pub.publish(LogEvent(
                            event_type='LLM_CIRCUIT_OPEN',
                            user_id='',
                            tool=self._last_call_info.get('tool_called', ''),
                            state=snapshot.objective.task_phase,
                            description='Circuit breaker opened: 3+ consecutive API failures. Skipping LLM for 60s.',
                            timestamp=int(time.time() * 1000),
                            safety_severity='WARNING'
                        ))
                    except Exception:
                        pass
                    if self.logger:
                        self.logger.warning('LLM circuit breaker opened: 3+ deterministic fallbacks')
            elif tier == 'NIM':
                self._consecutive_deterministic = 0
                # Counter reset on NIM success handled in _call_llm

            if decision.speak:
                node._speak(decision.speak)

            snapshot.budget.calls_remaining -= 1
            snapshot.budget.calls_used += 1

            try:
                success, reason, obs = tool_kernel.execute_tool(decision.tool, decision.params)
            except Exception as e:
                success, reason, obs = False, "EXECUTION_ERROR", str(e)
                if self.logger: self.logger.error(f"Tool {decision.tool} crashed: {e}")
            
            action_sig = f"{decision.tool}({decision.params})"
            snapshot.last_action.tool_call = action_sig
            snapshot.last_action.result = reason
            snapshot.last_action.reason = obs
            
            snapshot.action_history.append({"call": action_sig, "result": reason, "n": snapshot.budget.calls_used})
            
            if not success and reason != "ESTOP":
                snapshot.tried_and_failed.append(action_sig)

            if decision.tool == "vision_scan" and success:
                snapshot.objective.task_phase = "GRASPING"
            elif decision.tool == "vision_scan":
                # Track searched zones so the LLM snapshot reflects actual progress
                zone = decision.params.get('zone', 'ALL') if decision.params else 'ALL'
                if zone not in snapshot.zones_searched:
                    snapshot.zones_searched.append(zone)
            elif decision.tool == "arm_move" and success and decision.params.get('position') == 'PRESENTATION':
                snapshot.objective.task_phase = "HANDOVER"

            if decision.tool == "complete_task" or decision.tool == "abort_task":
                break

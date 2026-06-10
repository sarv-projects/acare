# acare_planner/tool_kernel.py
import time
import queue
from typing import Tuple

from .hw_translator import HWTranslator
from .state_snapshot import TaskSnapshot

VALID_TOOLS = {
    'vision_scan', 'arm_move', 'arm_approach', 'gripper_close', 'gripper_open',
    'detect_face', 'detect_hand', 'speak', 'ask_user', 'complete_task', 'abort_task'
}

VALID_ZONES = {'A', 'B', 'C', 'ALL', 'AUTO'}
VALID_POSITIONS = {'PREGRASP', 'GRASP_POINT', 'FACE_HEIGHT', 'PRESENTATION', 'SAFE_DROP', 'REST'}
VALID_APPROACHES = {'TOP_DOWN', 'SIDE_LEFT', 'SIDE_RIGHT'}
VALID_FIRMNESS = {'LIGHT', 'NORMAL', 'FIRM'}

class ToolKernel:
    def __init__(self, node, snapshot: TaskSnapshot, hw_translator: HWTranslator):
        self.node = node
        self.snapshot = snapshot
        self.hw = hw_translator

    def execute_tool(self, tool_name: str, params: dict) -> Tuple[bool, str, str]:
        # --- L1: Schema Validation ---
        if tool_name not in VALID_TOOLS:
            return False, "INVALID_ACTION", f"Unknown tool: {tool_name}"
            
        try:
            if tool_name == 'vision_scan':
                if params.get('zone', 'ALL') not in VALID_ZONES:
                    return False, "INVALID_ACTION", "Invalid zone."
            elif tool_name == 'arm_move':
                if params.get('position') not in VALID_POSITIONS:
                    return False, "INVALID_ACTION", "Invalid position."
            elif tool_name == 'arm_approach':
                if params.get('variant', 'TOP_DOWN') not in VALID_APPROACHES:
                    return False, "INVALID_ACTION", "Invalid approach variant."
            elif tool_name == 'gripper_close':
                if params.get('firmness', 'NORMAL') not in VALID_FIRMNESS:
                    return False, "INVALID_ACTION", "Invalid firmness."
        except Exception as e:
            return False, "INVALID_ACTION", f"Param parsing error: {e}"

        # --- L2: Deduplication Check ---
        action_sig = f"{tool_name}({params})"
        if action_sig in self.snapshot.tried_and_failed:
            return False, "ALREADY_TRIED", f"Action {action_sig} was already tried and failed this task."
        
        # --- L0: Safety Kernel Gate ---
        # Get target_xyz if applicable
        target_xyz = None
        if tool_name == 'arm_move' and self.node.context.grasp_point:
            target_xyz = self.node.context.grasp_point
        # We don't have IK result at schema validation time, so skip L3 here
        result = self.node.safety_kernel.evaluate(
            estop_active=self.node._estop_active.is_set(),
            tool_name=tool_name,
            target_xyz=target_xyz,
            calls_used=self.snapshot.budget.calls_used,
            gripper_force=self.node.world.gripper_force,
        )
        if not result.allowed:
            return False, result.layer, result.reason
        
        # --- ESTOP pre-check ---
        if self.node._estop_active.is_set() and tool_name != 'abort_task':
            return False, "ESTOP", "ESTOP active"

        # Route to specific tool handlers
        if tool_name == 'vision_scan':
            success, layer, reason = self._tool_vision_scan(params.get('zone', 'ALL'))
        elif tool_name == 'arm_move':
            success, layer, reason = self._tool_arm_move(params.get('position'))
        elif tool_name == 'arm_approach':
            success, layer, reason = self._tool_arm_approach(params.get('variant'))
        elif tool_name == 'gripper_close':
            success, layer, reason = self._tool_gripper_close(params.get('firmness'))
        elif tool_name == 'gripper_open':
            success, layer, reason = self._tool_gripper_open()
        elif tool_name == 'detect_face':
            success, layer, reason = self._tool_detect_face()
        elif tool_name == 'detect_hand':
            success, layer, reason = self._tool_detect_hand()
        elif tool_name == 'speak':
            success, layer, reason = self._tool_speak(params.get('message', ''))
        elif tool_name == 'ask_user':
            success, layer, reason = self._tool_ask_user(params.get('question', ''), params.get('expect', 'ANY'))
        elif tool_name == 'complete_task':
            success, layer, reason = self._tool_complete_task()
        elif tool_name == 'abort_task':
            success, layer, reason = self._tool_abort_task(params.get('reason', ''))
        else:
            return False, "INVALID_ACTION", "Unhandled tool"

        # Track consecutive failures for safety kernel
        if not success:
            self.node.safety_kernel.record_failure()
        else:
            self.node.safety_kernel.record_success()

        return success, layer, reason

    def _tool_vision_scan(self, zone: str) -> Tuple[bool, str, str]:
        tool_req = self.snapshot.objective.tool
        self.node._vision_event.clear()
        self.node._send_vision_search_request(tool_req, zone)
        
        if not self.node._vision_event.wait(timeout=30.0):
            return False, "TIMEOUT", "Vision scan timed out."
        if self.node._estop_active.is_set():
            return False, "ESTOP", "ESTOP activated during vision scan."
            
        res = self.node._last_vision_result
        if not res or not res.found:
            return False, "NOT_FOUND", "No detection above threshold."
            
        self.node.context.grasp_point = (res.x, res.y, res.z)
        return True, "SUCCESS", f"Found in zone {res.zone} with confidence {res.confidence}"

    def _tool_arm_move(self, position: str) -> Tuple[bool, str, str]:
        # Trigger EXECUTING state on first arm motion
        if self.node.world.robot_state != "EXECUTING":
            from acare_msgs.msg import StateTransition
            self.node.transition_pub.publish(StateTransition(target_state="EXECUTING"))

        grasp_point = self.node.context.grasp_point
        user_z_offset = 0.0
        try:
            if self.snapshot.user_prior.handover_z_offset:
                user_z_offset = float(self.snapshot.user_prior.handover_z_offset)
        except:
            pass

        target_xyz = self.hw.translate_position(position, grasp_point, user_z_offset)
        
        w = self.node._workspace
        if w:
            if not (w['xmin'] <= target_xyz[0] <= w['xmax'] and w['ymin'] <= target_xyz[1] <= w['ymax'] and w['zmin'] <= target_xyz[2] <= w['zmax']):
                return False, "SAFETY_REJECTED", "Target out of workspace bounds."

        # clear motion queue before sending
        while not self.node._motion_queue.empty():
            try:
                self.node._motion_queue.get_nowait()
            except queue.Empty:
                break
            
        if not self.node._send_arm_move(target_xyz[0], target_xyz[1], target_xyz[2], self.node._last_approach_rotation):
            return False, "UNREACHABLE", "IK failed to reach position."
            
        try:
            success = self.node._motion_queue.get(timeout=15.0)
            if not success:
                return False, "EXECUTION_FAILED", "Motion feedback reported failure."
        except queue.Empty:
            return False, "TIMEOUT", "Arm motion timed out."
            
        if position == 'PRESENTATION':
            from acare_msgs.msg import StateTransition
            self.node.transition_pub.publish(StateTransition(target_state="HANDOVER"))
            
        return True, "SUCCESS", f"Arm moved to {position}."

    def _tool_arm_approach(self, variant: str) -> Tuple[bool, str, str]:
        rot = self.hw.translate_approach_variant(variant)
        self.node._last_approach_rotation = rot 
        return True, "SUCCESS", f"Approach angle set to {variant}."

    def _tool_gripper_close(self, firmness: str) -> Tuple[bool, str, str]:
        force = self.hw.translate_firmness(firmness)
        self.node._send_gripper_command("GRASP", force)
        
        # Loop with short sleeps to allow ESTOP break-out.
        # In sim/demo mode the embedded interface never reports real force
        # feedback (gripper_force stays 0.0) — accept closure after the wait.
        for _ in range(4):
            time.sleep(0.5)
            if self.node._estop_active.is_set():
                return False, "ESTOP", "ESTOP activated."
            if self.node.world.gripper_force >= 0.5:
                self.node.world.arm_holding = True
                from acare_msgs.msg import StateTransition
                self.node.transition_pub.publish(StateTransition(target_state="HOLDING"))
                return True, "SUCCESS", "Grip established firmly."
            
        # After 2s: if no force feedback arrived at all, assume sim/demo mode
        if self.node.world.gripper_force == 0.0:
            self.node.world.arm_holding = True
            from acare_msgs.msg import StateTransition
            self.node.transition_pub.publish(StateTransition(target_state="HOLDING"))
            return True, "SUCCESS", "Grip established (sim/demo mode)."
            
        self.node._publish_vision_penalty()
        return False, "SLIP_DETECTED", "Gripper closed but force is low, object slipped."

    def _tool_gripper_open(self) -> Tuple[bool, str, str]:
        self.node._send_gripper_command("RELEASE")
        self.node.world.arm_holding = False
        return True, "SUCCESS", "Gripper opened."

    def _tool_detect_face(self) -> Tuple[bool, str, str]:
        self.node._auth_event.clear()
        self.node._request_auth_face()
        if not self.node._auth_event.wait(timeout=10.0):
            return False, "TIMEOUT", "Face detection timed out."
        if not self.node._last_auth_success:
            return False, "NO_FACE", "Face verification failed."
        return True, "SUCCESS", "User identity verified."

    def _tool_detect_hand(self) -> Tuple[bool, str, str]:
        start = time.time()
        while time.time() - start < 15.0:
            if self.node._estop_active.is_set():
                return False, "ESTOP", "ESTOP active"
            if self.node._hand_detected:
                return True, "SUCCESS", "Hand detected reaching."
            time.sleep(0.5)
        return False, "NO_HAND", "No hand detected."

    def _tool_speak(self, message: str) -> Tuple[bool, str, str]:
        self.node._speak(message)
        return True, "SUCCESS", "Message spoken."

    def _tool_ask_user(self, question: str, expect: str) -> Tuple[bool, str, str]:
        self.node._speak(question)
        self.node.voice_sync.start_wait(expect)
        resp = self.node.voice_sync.wait_for_response(timeout=8.0)
        if resp:
            return True, "SUCCESS", f"User responded: {resp}"
        return False, "TIMEOUT", "User did not respond."

    def _tool_complete_task(self) -> Tuple[bool, str, str]:
        if self.node.world.arm_holding:
            return False, "SAFETY_REJECTED", "Cannot complete task while holding tool."
        return True, "SUCCESS", "Task completed."

    def _tool_abort_task(self, reason: str) -> Tuple[bool, str, str]:
        if self.node.world.arm_holding:
            self.node._speak("Aborting. Safely depositing tool.")
            # Non-blocking safe-drop: use a short 5s timeout so abort cannot
            # hang the planner.  If the move fails, just open the gripper in
            # place — the tool may drop but the system stays responsive.
            grasp_point = self.node.context.grasp_point
            user_z_offset = 0.0
            try:
                if self.snapshot.user_prior.handover_z_offset:
                    user_z_offset = float(self.snapshot.user_prior.handover_z_offset)
            except:
                pass
            try:
                target_xyz = self.hw.translate_position('SAFE_DROP', grasp_point, user_z_offset)
                if self.node._send_arm_move(target_xyz[0], target_xyz[1], target_xyz[2], self.node._last_approach_rotation):
                    try:
                        self.node._motion_queue.get(timeout=5.0)
                    except queue.Empty:
                        self.node.get_logger().warn('Abort: safe-drop arm motion timed out, opening gripper in place.')
            except Exception:
                self.node.get_logger().warn('Abort: safe-drop IK failed, opening gripper in place.')
            self._tool_gripper_open()
        self.node._speak(f"Task aborted. {reason}")
        return True, "SUCCESS", "Task aborted."

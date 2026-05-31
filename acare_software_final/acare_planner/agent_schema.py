from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .tool_registry import is_valid_tool


class PlannerAction(str, Enum):
    SPEAK = "speak"
    TRANSITION = "transition"
    VISION_SEARCH = "vision_search"
    ARM_MOVE = "arm_move"
    GRIPPER = "gripper"
    SAFE_DEPOSIT = "safe_deposit"
    ABORT = "abort"


class SpeechCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: PlannerAction = PlannerAction.SPEAK
    text: str = Field(min_length=1, max_length=160)


class TransitionCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: PlannerAction = PlannerAction.TRANSITION
    target_state: str
    reason: str = Field(min_length=1, max_length=120)

    @field_validator("target_state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        allowed = {
            "LOGGED_OUT",
            "STANDBY",
            "LISTENING",
            "PROCESSING",
            "EXECUTING",
            "HOLDING",
            "HANDOVER",
            "ESTOP",
        }
        if value not in allowed:
            raise ValueError(f"Unsupported target_state: {value}")
        return value


class VisionSearchCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: PlannerAction = PlannerAction.VISION_SEARCH
    tool: str
    reset_probability_map: bool = False
    priority_zones: list[str] = Field(default_factory=list)

    @field_validator("tool")
    @classmethod
    def validate_tool(cls, value: str) -> str:
        if not is_valid_tool(value):
            raise ValueError(f"Unsupported tool request: {value}")
        return value


class ArmMoveCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: PlannerAction = PlannerAction.ARM_MOVE
    x: float
    y: float
    z: float
    velocity_scale: float = Field(ge=0.1, le=1.0)
    rotation_offset_deg: float = Field(ge=-180.0, le=180.0, default=0.0)

    @model_validator(mode="after")
    def validate_workspace(self):
        for axis_name in ("x", "y", "z"):
            axis_value = getattr(self, axis_name)
            if not float("-inf") < axis_value < float("inf"):
                raise ValueError(f"Non-finite {axis_name}: {axis_value}")
        # Coarse outer safety envelope based on the arm's 0.8 m max reach.
        # This is a backstop only — the real per-target reachability gate is
        # the IK solver in planner_node._send_arm_move (which loads the exact
        # workspace from system.yaml and checks joint limits).
        if not (-0.85 <= self.x <= 0.85 and -0.85 <= self.y <= 0.85 and -0.10 <= self.z <= 0.85):
            raise ValueError("Arm move target outside software safety envelope")
        return self


class SafeLimitSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    velocity_hard_deg_s: float = Field(gt=0.0)
    velocity_soft_deg_s: float = Field(gt=0.0)
    current_hard_a: float = Field(gt=0.0)
    current_soft_a: float = Field(gt=0.0)
    temperature_hard_c: float = Field(gt=0.0)
    temperature_soft_c: float = Field(gt=0.0)
    gripper_force_hard_n: float = Field(gt=0.0)
    gripper_force_soft_n: float = Field(gt=0.0)
    max_command_velocity_scale: float = Field(gt=0.05, le=1.0)
    max_command_accel_limit: float = Field(gt=0.01, le=1.0)
    kiosk_velocity_scale: float = Field(gt=0.05, le=1.0)
    kiosk_accel_limit: float = Field(gt=0.01, le=1.0)

    @model_validator(mode="after")
    def validate_prethresholds(self):
        pairs = [
            ("velocity_soft_deg_s", self.velocity_soft_deg_s, "velocity_hard_deg_s", self.velocity_hard_deg_s),
            ("current_soft_a", self.current_soft_a, "current_hard_a", self.current_hard_a),
            ("temperature_soft_c", self.temperature_soft_c, "temperature_hard_c", self.temperature_hard_c),
            ("gripper_force_soft_n", self.gripper_force_soft_n, "gripper_force_hard_n", self.gripper_force_hard_n),
        ]
        for soft_name, soft_value, hard_name, hard_value in pairs:
            if soft_value >= hard_value:
                raise ValueError(f"{soft_name} must stay below {hard_name}")
        if self.kiosk_velocity_scale > self.max_command_velocity_scale:
            raise ValueError("kiosk_velocity_scale must stay below max_command_velocity_scale")
        if self.kiosk_accel_limit > self.max_command_accel_limit:
            raise ValueError("kiosk_accel_limit must stay below max_command_accel_limit")
        return self


class GripperMode(str, Enum):
    GRASP = "GRASP"
    RELEASE = "RELEASE"


class GripperCommandSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: PlannerAction = PlannerAction.GRIPPER
    command: GripperMode
    force_target: float = Field(ge=0.0, le=10.0, default=0.0)


class SafeDepositCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: PlannerAction = PlannerAction.SAFE_DEPOSIT
    tool: str = ""


class AbortCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: PlannerAction = PlannerAction.ABORT
    message: str = Field(min_length=1, max_length=160)


# =============================================================================
# AGENTIC DECISION VALIDATION
# =============================================================================
# Validates every proposal from the agentic layer (gpt-oss-120b) before
# the planner acts on it. Catches malformed LLM output, out-of-range values,
# and invalid action/decision_type combinations.
#
# If validation fails → the planner uses the deterministic fallback instead.
# The robot NEVER executes an unvalidated agentic proposal.

class AgenticDecisionType(str, Enum):
    SEARCH_STRATEGY = "SEARCH_STRATEGY"
    VISION_RECOVERY = "VISION_RECOVERY"
    GRASP_RECOVERY = "GRASP_RECOVERY"
    IK_RECOVERY = "IK_RECOVERY"
    HANDOVER_RECOVERY = "HANDOVER_RECOVERY"
    ABORT = "ABORT"


class AgenticAction(str, Enum):
    RETRY_UNIFORM_SEARCH = "RETRY_UNIFORM_SEARCH"
    ASK_USER_CONFIRM_LOCATION = "ASK_USER_CONFIRM_LOCATION"
    ABORT_TOOL_NOT_FOUND = "ABORT_TOOL_NOT_FOUND"
    RETRY_GRASP_REPOSITION = "RETRY_GRASP_REPOSITION"
    RETRY_GRASP_FORCE_INCREASE = "RETRY_GRASP_FORCE_INCREASE"
    ABORT_GRASP_FAILED = "ABORT_GRASP_FAILED"
    RETRY_IK_ALTERNATE_ORIENTATION = "RETRY_IK_ALTERNATE_ORIENTATION"
    RETRY_IK_NEXT_CANDIDATE = "RETRY_IK_NEXT_CANDIDATE"
    ABORT_IK_FAILED = "ABORT_IK_FAILED"
    HANDOVER_Z_UP = "HANDOVER_Z_UP"
    HANDOVER_Z_DOWN = "HANDOVER_Z_DOWN"
    HANDOVER_VOICE_HAND_ONLY = "HANDOVER_VOICE_HAND_ONLY"
    SEARCH_PRIORITY_ZONES = "SEARCH_PRIORITY_ZONES"


class AgenticParams(BaseModel):
    """Parameters proposed by the agentic layer. All values are safety-clamped."""
    model_config = ConfigDict(extra="forbid")

    force_delta_n: float = Field(ge=-5.0, le=7.0, default=0.0)
    z_offset_m: float = Field(ge=-0.20, le=0.20, default=0.0)
    rotation_deg: float = Field(ge=-180.0, le=180.0, default=0.0)
    priority_zones: list[str] = Field(default_factory=list, max_length=10)
    reset_probability_map: bool = False

    @field_validator("priority_zones")
    @classmethod
    def validate_zones(cls, v: list[str]) -> list[str]:
        # Zone names must be short strings, no injection
        return [z[:32] for z in v if isinstance(z, str)]


class AgenticDecision(BaseModel):
    """
    Validates a complete agentic decision from gpt-oss-120b.

    Safety invariants enforced:
    - force_delta_n clamped to [-5, +7] → total force never exceeds 10N (base 3N + 7N max)
    - z_offset_m clamped to [-0.20, +0.20] → arm stays within workspace
    - rotation_deg clamped to [-180, +180]
    - tts_message max 160 chars (prevents LLM from generating essays)
    - decision_type and action must be valid enum values
    - params must pass AgenticParams validation
    """
    model_config = ConfigDict(extra="forbid")

    decision_type: AgenticDecisionType
    reasoning: str = Field(min_length=1, max_length=500)
    action: AgenticAction
    tts_message: str = Field(min_length=1, max_length=160)
    params: AgenticParams

    @model_validator(mode="after")
    def validate_action_matches_decision_type(self):
        """Ensure the action is appropriate for the decision type."""
        valid_actions_per_type = {
            AgenticDecisionType.SEARCH_STRATEGY: {
                AgenticAction.SEARCH_PRIORITY_ZONES,
            },
            AgenticDecisionType.VISION_RECOVERY: {
                AgenticAction.RETRY_UNIFORM_SEARCH,
                AgenticAction.ASK_USER_CONFIRM_LOCATION,
                AgenticAction.ABORT_TOOL_NOT_FOUND,
                AgenticAction.SEARCH_PRIORITY_ZONES,
            },
            AgenticDecisionType.GRASP_RECOVERY: {
                AgenticAction.RETRY_GRASP_REPOSITION,
                AgenticAction.RETRY_GRASP_FORCE_INCREASE,
                AgenticAction.ABORT_GRASP_FAILED,
            },
            AgenticDecisionType.IK_RECOVERY: {
                AgenticAction.RETRY_IK_ALTERNATE_ORIENTATION,
                AgenticAction.RETRY_IK_NEXT_CANDIDATE,
                AgenticAction.ABORT_IK_FAILED,
            },
            AgenticDecisionType.HANDOVER_RECOVERY: {
                AgenticAction.HANDOVER_Z_UP,
                AgenticAction.HANDOVER_Z_DOWN,
                AgenticAction.HANDOVER_VOICE_HAND_ONLY,
            },
        }
        allowed = valid_actions_per_type.get(self.decision_type)
        if allowed and self.action not in allowed:
            raise ValueError(
                f"Action {self.action.value} is not valid for "
                f"decision_type {self.decision_type.value}"
            )
        return self

    @model_validator(mode="after")
    def validate_force_safety(self):
        """Ensure force proposals stay well below ESTOP threshold."""
        if self.params.force_delta_n > 7.0:
            raise ValueError(
                f"force_delta_n={self.params.force_delta_n} would exceed 10N "
                f"(base 3N + delta). Max allowed: 7.0N"
            )
        return self


def validate_agentic_decision(raw_dict: dict) -> AgenticDecision | None:
    """
    Validates a raw dict from the agentic LLM layer.

    Returns:
        AgenticDecision if valid, None if validation fails.

    Usage in planner_node:
        decision = agentic.propose_vision_recovery(...)
        validated = validate_agentic_decision(decision)
        if validated is None:
            # Use deterministic fallback
            ...
        else:
            # Safe to use validated.params.force_delta_n, etc.
            ...
    """
    if raw_dict is None:
        return None
    try:
        return AgenticDecision(**raw_dict)
    except Exception:
        return None

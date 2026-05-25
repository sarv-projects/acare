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
        if not (-1.0 <= self.x <= 1.0 and -1.0 <= self.y <= 1.0 and -0.2 <= self.z <= 1.0):
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

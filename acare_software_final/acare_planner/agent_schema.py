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

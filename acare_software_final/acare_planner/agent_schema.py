from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

class ToolCallSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    thought: str = Field(min_length=1, max_length=500)
    tool: str = Field(min_length=1, max_length=64)
    params: dict = Field(default_factory=dict)
    speak: str | None = Field(default=None, max_length=160)

def validate_agentic_decision(raw_dict: dict) -> ToolCallSchema | None:
    if raw_dict is None:
        return None
    try:
        return ToolCallSchema(**raw_dict)
    except Exception:
        return None

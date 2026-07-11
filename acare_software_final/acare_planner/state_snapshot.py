# acare_planner/state_snapshot.py
import json
from typing import List, Optional
from pydantic import BaseModel, Field

class TaskObjective(BaseModel):
    tool: str = ""
    user: str = ""
    task_phase: str = "SEARCHING"

class WorldState(BaseModel):
    arm_at: str = "REST"
    gripper: str = "OPEN"
    safety: str = "OK"
    holding_tool: bool = False
    vision_ready: bool = True

class ActionHistoryItem(BaseModel):
    call: str
    result: str
    n: int

class LastAction(BaseModel):
    tool_call: str = ""
    result: str = ""
    reason: str = ""

class Budget(BaseModel):
    calls_used: int = 0
    calls_remaining: int = 20

class UserPrior(BaseModel):
    preferred_zone: Optional[str] = None
    handover_z_offset: Optional[float] = None   # G3: fixed from str to float

class TaskSnapshot(BaseModel):
    objective: TaskObjective = Field(default_factory=TaskObjective)
    world: WorldState = Field(default_factory=WorldState)
    last_action: LastAction = Field(default_factory=LastAction)
    action_history: List[ActionHistoryItem] = Field(default_factory=list)
    budget: Budget = Field(default_factory=Budget)
    tried_and_failed: List[str] = Field(default_factory=list)
    zones_searched: List[str] = Field(default_factory=list)
    user_prior: UserPrior = Field(default_factory=UserPrior)
    available_tools: List[str] = Field(default_factory=list)

    def to_message(self) -> dict:
        """Serializes the snapshot to an LLM message."""
        # Ensure action history doesn't grow beyond 3
        if len(self.action_history) > 3:
            self.action_history = self.action_history[-3:]
            
        # Truncate string bloat
        if self.last_action.reason and len(self.last_action.reason) > 150:
            self.last_action.reason = self.last_action.reason[:147] + "..."
            
        # Summarize tried_and_failed
        failed_summary = {}
        for action in self.tried_and_failed:
            tool = action.split('(')[0]
            failed_summary[tool] = failed_summary.get(tool, 0) + 1
        
        dumped = self.model_dump(exclude_none=True)
        dumped['tried_and_failed'] = [f"{k} failed {v} times" for k, v in failed_summary.items()]
        
        return {
            "role": "user",
            "content": f"Current State Snapshot:\n```json\n{json.dumps(dumped, indent=2)}\n```\nAnalyze the state and propose the next tool call."
        }

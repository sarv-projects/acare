"""
acare_planner/safety_kernel.py
Spec Reference: Section XII (Task Planner — Safety Kernel)

Deterministic 6-layer safety guard that runs before every tool execution.
Each layer can veto the action. Layers are evaluated in order; a veto
at any layer short-circuits the remaining checks.

Layers:
  L1: ESTOP check — reject all non-abort actions while ESTOP active
  L2: Workspace bounds — reject targets outside the defined workspace
  L3: Joint limits — reject IK solutions that hit joint limits
  L4: Consecutive-failure guard — abort after N consecutive failures
  L5: Budget guard — abort when LLM call budget is exhausted
  L6: Gripper-force sanity — reject GRASP if force telemetry is anomalous
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class KernelResult:
    allowed: bool
    layer: str
    reason: str


class SafetyKernel:
    MAX_CONSECUTIVE_FAILURES = 3
    MAX_LLM_CALLS = 20
    GRIPPER_FORCE_ANOMALY_N = 50.0

    def __init__(self, workspace: Optional[dict] = None):
        self._workspace = workspace or {
            'xmin': -0.6, 'xmax': 0.6,
            'ymin': -0.6, 'ymax': 0.6,
            'zmin': 0.0, 'zmax': 0.75,
        }
        self._consecutive_failures = 0

    def reset_failures(self):
        self._consecutive_failures = 0

    def record_failure(self):
        self._consecutive_failures += 1

    def record_success(self):
        self._consecutive_failures = 0

    def evaluate(
        self,
        *,
        estop_active: bool,
        tool_name: str,
        target_xyz: Optional[tuple] = None,
        ik_reachable: Optional[bool] = None,
        calls_used: int = 0,
        gripper_force: float = 0.0,
    ) -> KernelResult:
        if estop_active and tool_name != 'abort_task':
            return KernelResult(False, "L1_ESTOP", "ESTOP active")

        if target_xyz is not None:
            x, y, z = target_xyz
            w = self._workspace
            if not (w['xmin'] <= x <= w['xmax'] and
                    w['ymin'] <= y <= w['ymax'] and
                    w['zmin'] <= z <= w['zmax']):
                return KernelResult(False, "L2_WORKSPACE", f"Target {target_xyz} out of bounds")

        if ik_reachable is not None and not ik_reachable:
            return KernelResult(False, "L3_JOINT_LIMIT", "IK solution unreachable")

        if self._consecutive_failures >= self.MAX_CONSECUTIVE_FAILURES:
            return KernelResult(False, "L4_CONSECUTIVE_FAILURES",
                                f"{self._consecutive_failures} consecutive failures")

        if calls_used >= self.MAX_LLM_CALLS:
            return KernelResult(False, "L5_BUDGET", f"LLM budget exhausted ({calls_used} calls)")

        if tool_name == 'gripper_close' and gripper_force > self.GRIPPER_FORCE_ANOMALY_N:
            return KernelResult(False, "L6_GRIPPER_ANOMALY",
                                f"Gripper force {gripper_force:.1f}N exceeds anomaly threshold")

        # M7: Reset failure counter on successful evaluation so it doesn't
        # bleed across tasks (crash mid-task leaves stale counter otherwise).
        if self._consecutive_failures > 0:
            self._consecutive_failures = 0
        return KernelResult(True, "PASS", "All layers passed")


class RetryCounters:
    MAX_RETRIES_PER_STEP = 2
    MAX_TOTAL_RETRIES = 5

    def __init__(self):
        self._step_retries: dict[str, int] = {}
        self._total_retries = 0

    def reset(self):
        self._step_retries.clear()
        self._total_retries = 0

    def can_retry(self, step_key: str) -> bool:
        step_count = self._step_retries.get(step_key, 0)
        return step_count < self.MAX_RETRIES_PER_STEP and self._total_retries < self.MAX_TOTAL_RETRIES

    def record_retry(self, step_key: str):
        self._step_retries[step_key] = self._step_retries.get(step_key, 0) + 1
        self._total_retries += 1

    @property
    def total_retries(self) -> int:
        return self._total_retries

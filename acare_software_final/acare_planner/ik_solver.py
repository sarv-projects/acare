from __future__ import annotations

from typing import Iterable


class IKSolver:
    """Lightweight placeholder until calibrated DH parameters are available."""

    def solve_pregrasp(self, xyz: Iterable[float]) -> list[float]:
        x, y, z = [float(v) for v in xyz]
        return [x, y, z + 0.05, 0.0, 0.0, 0.0]

    def solve_grasp(self, xyz: Iterable[float]) -> list[float]:
        x, y, z = [float(v) for v in xyz]
        return [x, y, z, 0.0, 0.0, 0.0]

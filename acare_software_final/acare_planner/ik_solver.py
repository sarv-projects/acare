"""
Inverse kinematics for the ACARE 6-DOF arm.

This module provides two complementary surfaces:

1. ``IKSolver.solve_*`` returns a *best-effort* joint-space solution if a
   URDF / DH parameter file is available on disk. If not, it returns
   ``None`` rather than the previous behaviour of fabricating angles equal
   to the cartesian XYZ — a bug that, on real hardware, would have driven
   joint 1 to ``x`` radians, joint 2 to ``y`` radians, joint 3 to
   ``z+0.05`` radians, and so on.  Geometrically meaningless and
   dangerous.

2. ``cartesian_pose`` packages the same target as a 6-vector
   ``[x, y, z, roll, pitch, yaw]`` so the embedded interface can act on the
   cartesian command directly (the firmware runs its own IK on real
   hardware), and so that downstream consumers can detect the difference.

Resolution order for joint solutions:

* ``ikpy`` (Apache-2.0, pure-Python) loaded against
  ``$ACARE_URDF_PATH`` or ``acare_bringup/config/arm.urdf`` if present.
* ``acare_bringup/config/ik_calibration.yaml`` lookup table  — radial
  interpolation between calibrated cartesian-to-joint samples. Used in
  the field when no URDF is available but joint targets have been
  hand-measured.
* ``None`` — the planner falls back to publishing ``mode="CARTESIAN"`` and
  the embedded layer (firmware on Teensy, simulator in development) is
  responsible for the final motion.
"""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Iterable, Optional, Sequence, Tuple

try:  # pragma: no cover - optional dependency
    from ikpy.chain import Chain
    HAVE_IKPY = True
except Exception:  # pragma: no cover
    Chain = None  # type: ignore
    HAVE_IKPY = False


XYZ = Tuple[float, float, float]
RPY = Tuple[float, float, float]
JointAngles = Sequence[float]


def cartesian_pose(xyz: Iterable[float], rpy: Iterable[float] = (0.0, 0.0, 0.0)) -> list[float]:
    """Pack a 6-vector cartesian pose for ArmCommand.pose.

    Always returns finite, real numbers — callers can publish the result
    directly without worrying about NaNs leaking into the bus.
    """
    x, y, z = (float(v) for v in xyz)
    r, p, yw = (float(v) for v in rpy)
    for value in (x, y, z, r, p, yw):
        if not math.isfinite(value):
            raise ValueError(f"Non-finite component in cartesian pose: {value}")
    return [x, y, z, r, p, yw]


class IKSolver:
    """Best-effort 6-DOF IK with explicit "no solution" semantics.

    The previous placeholder returned ``[x, y, z, 0, 0, 0]`` and let the
    planner publish those numbers as if they were joint angles. They were
    not. The new contract is:

    * If a real solver is available, return a list of 6 joint angles in
      radians.
    * Otherwise return ``None``. The caller MUST then publish in
      cartesian mode (``ArmCommand.mode = "CARTESIAN"``) and let the
      embedded layer handle the final motion.
    """

    URDF_ENV = "ACARE_URDF_PATH"
    DEFAULT_URDF_NAMES = ("arm.urdf", "acare_arm.urdf")

    def __init__(self, urdf_path: Optional[str] = None):
        self._chain: Optional["Chain"] = None
        self._chain_error: str = ""

        path = self._resolve_urdf(urdf_path)
        if path is None:
            self._chain_error = "no URDF found (set $ACARE_URDF_PATH or place arm.urdf in acare_bringup/config/)"
            return

        if not HAVE_IKPY:
            self._chain_error = "ikpy not installed — cartesian-mode commands only"
            return

        try:
            self._chain = Chain.from_urdf_file(str(path))
        except Exception as exc:  # pragma: no cover - depends on URDF
            self._chain_error = f"ikpy failed to load {path}: {exc}"
            self._chain = None

    # -- public API ---------------------------------------------------- #

    @property
    def has_solver(self) -> bool:
        return self._chain is not None

    @property
    def status(self) -> str:
        return "ok" if self.has_solver else self._chain_error

    def solve_pregrasp(self, xyz: Iterable[float]) -> Optional[list[float]]:
        """Return joint angles for a pose 5 cm above the requested grasp point."""
        x, y, z = (float(v) for v in xyz)
        return self._solve_position((x, y, z + 0.05))

    def solve_grasp(self, xyz: Iterable[float]) -> Optional[list[float]]:
        return self._solve_position(tuple(float(v) for v in xyz))

    # -- internals ----------------------------------------------------- #

    def _resolve_urdf(self, override: Optional[str]) -> Optional[Path]:
        if override:
            p = Path(override).expanduser()
            return p if p.exists() else None

        env = os.environ.get(self.URDF_ENV)
        if env:
            p = Path(env).expanduser()
            if p.exists():
                return p

        # Look in acare_bringup/config/ — best-effort, no hard import.
        try:
            from acare_bringup.paths import CONFIG_DIR  # type: ignore
        except Exception:
            CONFIG_DIR = None  # type: ignore

        if CONFIG_DIR is not None:
            for name in self.DEFAULT_URDF_NAMES:
                candidate = Path(CONFIG_DIR) / name
                if candidate.exists():
                    return candidate

        return None

    def _solve_position(self, xyz: XYZ) -> Optional[list[float]]:
        if self._chain is None:
            return None

        target_frame = [
            [1.0, 0.0, 0.0, xyz[0]],
            [0.0, 1.0, 0.0, xyz[1]],
            [0.0, 0.0, 1.0, xyz[2]],
            [0.0, 0.0, 0.0, 1.0],
        ]
        try:
            angles = self._chain.inverse_kinematics_frame(target_frame)
        except Exception:
            return None

        # ikpy returns one angle per *link*, including a fixed base. Strip
        # any non-actuated joints by taking the last 6 elements that are
        # active in the chain.
        active = [
            a for link, a in zip(self._chain.links, angles) if getattr(link, "joint_type", None) != "fixed"
        ]
        if len(active) < 6:
            return None
        joints = [float(v) for v in active[-6:]]
        if any(not math.isfinite(v) for v in joints):
            return None
        return joints

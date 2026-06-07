"""
acare_planner/ik_solver.py
Spec Reference: Section XII (Task Planner — Inverse Kinematics)

Analytical inverse kinematics for the ACARE 6-DOF arm.

Arm geometry (confirmed from CAD assembly):
    base_height : 352 mm   (J1 vertical rotation axis → J2 shoulder)
    upper_arm   : 400 mm   (J2 shoulder → J3 elbow)
    forearm     : 400 mm   (J3 elbow → J4 wrist)
    wrist+tool  : 236 mm   (J4 → tool tip / gripper TCP)

Joint configuration:
    J1 (base)     : vertical axis rotation     [-180, +180]°
    J2 (shoulder) : horizontal pitch axis      [-135, +135]°
    J3 (elbow)    : horizontal pitch axis      [-120, +120]°
    J4 (wrist_1)  : wrist roll                 [-180, +180]°
    J5 (wrist_2)  : wrist pitch                [-180, +180]°
    J6 (wrist_3)  : wrist yaw / gripper roll   [-180, +180]°

Method: This is a classic anthropomorphic arm with a 3-axis wrist.
We solve the position with a geometric (planar 2-link) solution for
J1/J2/J3, then orient the wrist (J4/J5/J6) for a top-down grasp by
default. Returns joint angles in RADIANS (the convention ros2_control
and Gazebo expect).

All link lengths and joint limits are loaded from system.yaml so they
can be corrected without code changes. Sensible defaults (the CAD values
above) are used if the config is missing.

The solver NEVER raises on unreachable targets — it clamps to joint
limits and returns the best-effort pose plus a `reachable` flag via
solve_with_status(). The planner's safety layer validates the result
before any motion command is issued.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Optional

try:
    import yaml
    from acare_bringup.paths import SYSTEM_YAML
    _CONFIG_AVAILABLE = True
except Exception:
    _CONFIG_AVAILABLE = False


# --- Default geometry from CAD (metres) ---
DEFAULT_BASE_HEIGHT = 0.352
DEFAULT_UPPER_ARM   = 0.400
DEFAULT_FOREARM     = 0.400
DEFAULT_WRIST_TOOL  = 0.236

# --- Default joint limits (radians) ---
DEFAULT_LIMITS_MIN = [
    math.radians(-180),  # J1 base
    math.radians(-135),  # J2 shoulder
    math.radians(-120),  # J3 elbow
    math.radians(-180),  # J4 wrist_1
    math.radians(-180),  # J5 wrist_2
    math.radians(-180),  # J6 wrist_3
]
DEFAULT_LIMITS_MAX = [
    math.radians(180),
    math.radians(135),
    math.radians(120),
    math.radians(180),
    math.radians(180),
    math.radians(180),
]

PREGRASP_APPROACH_M = 0.05   # 5 cm above target before descending


@dataclass
class IKResult:
    joint_angles: list[float]   # radians, length 6
    reachable: bool
    reason: str = ""


class IKSolver:
    """
    Analytical IK for the ACARE 6-DOF arm.

    Public interface (unchanged from the placeholder so planner_node
    needs no edits):
        solve_pregrasp(xyz) -> list[float]   # 6 joint angles (rad)
        solve_grasp(xyz)    -> list[float]   # 6 joint angles (rad)

    Extended interface for callers that want reachability info:
        solve_with_status(xyz, top_down=True) -> IKResult
    """

    def __init__(self):
        self.base_height = DEFAULT_BASE_HEIGHT
        self.upper_arm   = DEFAULT_UPPER_ARM
        self.forearm     = DEFAULT_FOREARM
        self.wrist_tool  = DEFAULT_WRIST_TOOL
        self.limits_min  = list(DEFAULT_LIMITS_MIN)
        self.limits_max  = list(DEFAULT_LIMITS_MAX)
        self._load_config()

        # Max planar reach (shoulder + forearm). Targets beyond this are
        # unreachable and get clamped.
        self.max_reach = self.upper_arm + self.forearm

    # ------------------------------------------------------------------
    # Config
    # ------------------------------------------------------------------
    def _load_config(self):
        if not _CONFIG_AVAILABLE or not SYSTEM_YAML.exists():
            return
        try:
            with open(SYSTEM_YAML, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            arm = cfg.get("arm", {}) or {}

            links = arm.get("link_lengths", {}) or {}
            # Only override defaults if a real (non-zero) value is present.
            if float(links.get("base_height", 0.0)) > 0:
                self.base_height = float(links["base_height"])
            if float(links.get("upper_arm", 0.0)) > 0:
                self.upper_arm = float(links["upper_arm"])
            if float(links.get("forearm", 0.0)) > 0:
                self.forearm = float(links["forearm"])
            if float(links.get("wrist", 0.0)) > 0:
                self.wrist_tool = float(links["wrist"])

            lmin = arm.get("joint_limits_min", [])
            lmax = arm.get("joint_limits_max", [])
            # Config limits are in radians. Only use if they look real
            # (not the placeholder all-zeros).
            if len(lmin) == 6 and any(abs(v) > 1e-6 for v in lmin):
                self.limits_min = [float(v) for v in lmin]
            if len(lmax) == 6 and any(abs(v) > 1e-6 for v in lmax):
                self.limits_max = [float(v) for v in lmax]
        except Exception:
            pass  # keep CAD defaults

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _clamp_joint(self, idx: int, angle: float) -> tuple[float, bool]:
        """Clamp a joint angle to its limits. Returns (clamped, within_limits)."""
        lo, hi = self.limits_min[idx], self.limits_max[idx]
        if angle < lo:
            return lo, False
        if angle > hi:
            return hi, False
        return angle, True

    # ------------------------------------------------------------------
    # Core IK
    # ------------------------------------------------------------------
    def solve_with_status(self, xyz: Iterable[float], top_down: bool = True) -> IKResult:
        """
        Solve IK for a target TCP position (metres) in the robot base frame.

        top_down=True orients the gripper pointing straight down (the normal
        grasp approach for tools lying on a tray). The wrist joints are set
        so the tool axis is vertical regardless of base rotation.

        Returns an IKResult with joint angles (radians) and a reachable flag.
        Never raises.
        """
        try:
            x, y, z = (float(v) for v in xyz)
        except Exception:
            return IKResult(self._safe_neutral(), False, "invalid_xyz")

        reachable = True
        reasons = []

        # --- J1: base rotation to face the target in the XY plane ---
        j1 = math.atan2(y, x)

        # --- Reduce to the arm plane (the vertical plane containing the target) ---
        # Horizontal distance from base axis to target:
        r = math.hypot(x, y)

        # For a top-down grasp, the wrist+tool segment drops straight down to
        # the tool. So the WRIST CENTRE sits wrist_tool ABOVE the target.
        # The 2-link (shoulder+forearm) problem solves for the wrist centre.
        if top_down:
            wrist_z = z + self.wrist_tool
            wrist_r = r
        else:
            # Side approach: wrist centre is offset horizontally instead.
            wrist_z = z
            wrist_r = max(0.0, r - self.wrist_tool)

        # --- Planar 2-link IK (shoulder + forearm) in the (dr, dz) plane ---
        # dr/dz are the wrist-centre coordinates relative to the shoulder joint.
        L1 = self.upper_arm
        L2 = self.forearm
        dr = wrist_r
        dz = wrist_z - self.base_height
        planar_sq = dr * dr + dz * dz
        planar = math.sqrt(planar_sq)

        # --- Reach check ---
        if planar > (L1 + L2):
            reachable = False
            reasons.append("target_too_far")
            planar = (L1 + L2) - 1e-4
            planar_sq = planar * planar
        if planar < abs(L1 - L2):
            reachable = False
            reasons.append("target_too_close")
            planar = abs(L1 - L2) + 1e-4
            planar_sq = planar * planar

        # --- J3 (elbow joint angle) via law of cosines ---
        # cos(j3) = (dr² + dz² - L1² - L2²) / (2 L1 L2)
        # j3 = 0 → arm straight; |j3| grows as arm folds.
        cos_j3 = (planar_sq - L1 * L1 - L2 * L2) / (2.0 * L1 * L2)
        cos_j3 = max(-1.0, min(1.0, cos_j3))
        # Elbow-up configuration (negative elbow) keeps the elbow raised so the
        # forearm descends onto the tool — the natural tray-pick posture.
        j3 = -math.acos(cos_j3)

        # --- J2 (shoulder) ---
        # j2 = atan2(dz, dr) - atan2(L2·sin(j3), L1 + L2·cos(j3))
        j2 = math.atan2(dz, dr) - math.atan2(
            L2 * math.sin(j3),
            L1 + L2 * math.cos(j3),
        )

        # --- Wrist (J4, J5, J6) ---
        # For a top-down grasp the tool must point straight down (-Z, i.e.
        # -90° from horizontal). The forearm's absolute pitch is (j2 + j3);
        # J5 (wrist pitch) closes the chain to vertical.
        if top_down:
            j5 = -(math.pi / 2.0) - (j2 + j3)
            j4 = 0.0
            j6 = 0.0
        else:
            j5 = -(j2 + j3)
            j4 = 0.0
            j6 = 0.0

        raw = [j1, j2, j3, j4, j5, j6]

        # --- Clamp all joints to limits ---
        clamped = []
        for i, a in enumerate(raw):
            ca, ok = self._clamp_joint(i, self._wrap_angle(a))
            clamped.append(ca)
            if not ok:
                reachable = False
                reasons.append(f"j{i+1}_limit")

        return IKResult(clamped, reachable, ",".join(reasons))

    # ------------------------------------------------------------------
    # Public interface (matches the old placeholder signature)
    # ------------------------------------------------------------------
    def solve_grasp(self, xyz: Iterable[float]) -> list[float]:
        """Joint angles (rad) to place the gripper AT the target, pointing down."""
        return self.solve_with_status(xyz, top_down=True).joint_angles

    def solve_pregrasp(self, xyz: Iterable[float]) -> list[float]:
        """Joint angles (rad) for a pose 5 cm ABOVE the target (approach pose)."""
        x, y, z = (float(v) for v in xyz)
        return self.solve_with_status((x, y, z + PREGRASP_APPROACH_M), top_down=True).joint_angles

    def solve_pregrasp_with_status(self, xyz: Iterable[float]) -> IKResult:
        """Like solve_pregrasp but returns the full IKResult with reachable flag."""
        x, y, z = (float(v) for v in xyz)
        return self.solve_with_status((x, y, z + PREGRASP_APPROACH_M), top_down=True)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    @staticmethod
    def _wrap_angle(a: float) -> float:
        """Wrap to [-pi, pi]."""
        while a > math.pi:
            a -= 2.0 * math.pi
        while a < -math.pi:
            a += 2.0 * math.pi
        return a

    def _safe_neutral(self) -> list[float]:
        """A safe fallback pose (all zeros, within limits)."""
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def forward_kinematics(self, joints: Iterable[float]) -> tuple[float, float, float]:
        """
        Compute TCP position (metres) from joint angles (radians).
        Used for verification/testing. Returns (x, y, z) in base frame.

        Simplified planar FK for the position-carrying joints (J1, J2, J3)
        plus the fixed wrist+tool drop. Wrist orientation joints (J4-J6)
        don't change TCP position in the top-down configuration.
        """
        j = [float(v) for v in joints]
        j1, j2, j3 = j[0], j[1], j[2]
        # Planar reach of shoulder + forearm:
        # shoulder contributes L1 at angle j2 from horizontal,
        # elbow adds L2 at angle (j2 + j3).
        r = self.upper_arm * math.cos(j2) + self.forearm * math.cos(j2 + j3)
        zr = self.base_height + self.upper_arm * math.sin(j2) + self.forearm * math.sin(j2 + j3)
        # Tool drops straight down by wrist_tool in top-down config:
        z = zr - self.wrist_tool
        x = r * math.cos(j1)
        y = r * math.sin(j1)
        return (x, y, z)


# ---------------------------------------------------------------------------
# Self-test — run with: python3 -m acare_planner.ik_solver
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    solver = IKSolver()
    print(f"Geometry: base={solver.base_height} upper={solver.upper_arm} "
          f"forearm={solver.forearm} wrist={solver.wrist_tool} "
          f"max_reach={solver.max_reach:.3f}m")
    print()

    test_targets = [
        ("tray-far",   (0.55, 0.0, 0.05)),
        ("tray-mid",   (0.45, 0.0, 0.05)),
        ("tray-left",  (0.40, 0.20, 0.05)),
        ("tray-right", (0.40, -0.20, 0.05)),
        ("tray-near",  (0.35, 0.0, 0.05)),
        ("too-far",    (1.50, 0.0, 0.10)),
    ]

    for name, target in test_targets:
        res = solver.solve_with_status(target)
        degs = [round(math.degrees(a), 1) for a in res.joint_angles]
        fk = solver.forward_kinematics(res.joint_angles)
        err = math.dist(target, fk) if res.reachable else float("nan")
        status = "OK" if res.reachable else f"UNREACHABLE ({res.reason})"
        print(f"{name:12s} target={target}")
        print(f"   joints(deg)={degs}")
        print(f"   FK={tuple(round(v,3) for v in fk)}  err={err:.4f}m  [{status}]")
        print()

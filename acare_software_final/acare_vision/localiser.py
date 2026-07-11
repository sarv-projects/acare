# acare_vision/localiser.py
# Spec Reference: Section XI (3D Localisation)
#
# Converts a bounding box centre pixel + depth value into (x, y, z)
# in the robot base frame. No Open3D, no point cloud — direct depth read.
#
# Camera intrinsics (fx, fy, cx, cy) and extrinsics (T_robot_camera)
# are loaded from system.yaml. These are PLACEHOLDERS until the camera
# is physically mounted on the arm and calibrated.
#
# Calibration steps (admin.py calibrate):
#   Step 2: Camera intrinsics — OpenCV calibrateCamera() with 9x6 checkerboard
#   Step 5: Extrinsics — cv2.solvePnP with known robot-frame target positions
#
# HP60C depth range: 200mm – 4000mm (0.2m – 4.0m)
# Depth values are uint16 in millimetres.

import logging
import math
import numpy as np
import yaml
from pathlib import Path

from acare_bringup.paths import SYSTEM_YAML

logger = logging.getLogger(__name__)

# Default intrinsics — real HP60C values (read from /camera_info, 2026-05-30).
# These are overridden live by update_intrinsics() from the camera_info topic.
PLACEHOLDER_FX = 572.04   # focal length x in pixels
PLACEHOLDER_FY = 571.49   # focal length y in pixels
PLACEHOLDER_CX = 329.27   # principal point x
PLACEHOLDER_CY = 242.09   # principal point y

# Placeholder extrinsics — identity transform (camera = robot base frame)
# MUST be replaced with calibrated T_robot_camera after arm assembly
PLACEHOLDER_T = np.eye(4, dtype=np.float64)


class Localiser:
    """
    Converts a 2D bounding box + depth frame into a 3D position in the
    robot base frame using the pinhole camera model.

    Intrinsics (fx, fy, cx, cy) define the camera's optical properties.
    Extrinsics (T_robot_camera) is the 4x4 rigid transform from camera
    frame to robot base frame — set during calibration after arm assembly.

    Until calibration is done, placeholder values are used. The 3D positions
    will be in camera frame (not robot frame) with approximate scale.
    """

    def __init__(self):
        self.fx = PLACEHOLDER_FX
        self.fy = PLACEHOLDER_FY
        self.cx = PLACEHOLDER_CX
        self.cy = PLACEHOLDER_CY
        self.T  = PLACEHOLDER_T.copy()
        self._calibrated = False
        # Fixed offset from wrist flange to camera lens (metres).
        # Default: camera is ~40mm forward and ~20mm below the flange,
        # with optical axis pointing down (-Z robot when looking straight down).
        # Override via camera.T_flange_camera in system.yaml.
        self._T_flange_camera = np.eye(4, dtype=np.float64)
        self._T_flange_camera[0, 3] =  0.040   # 40 mm forward from flange
        self._T_flange_camera[2, 3] = -0.020   # 20 mm below flange
        self._load_config()

    def _load_config(self):
        if not SYSTEM_YAML.exists():
            return
        try:
            with open(SYSTEM_YAML) as f:
                cfg = yaml.safe_load(f)
            cam = cfg.get('camera', {})
            # T_flange_camera: wrist-mounted camera offset from flange.
            # Only translation matters for the simplified FK model; rotation
            # is handled by compute_T_for_viewpoint() from joint angles.
            if 'T_flange_camera' in cam:
                Tfc = np.array(cam['T_flange_camera'], dtype=np.float64).reshape(4, 4)
                self._T_flange_camera = Tfc
            if all(k in cam for k in ('fx', 'fy', 'cx', 'cy', 'T_robot_camera')):
                fx, fy, cx, cy = (float(cam['fx']), float(cam['fy']),
                                  float(cam['cx']), float(cam['cy']))
                # Guard against bad/zero intrinsics that would cause div-by-zero
                # in pixel_to_robot. Only accept positive focal lengths.
                if fx > 0.0 and fy > 0.0:
                    self.fx, self.fy, self.cx, self.cy = fx, fy, cx, cy
                    T_flat = cam['T_robot_camera']
                    self.T = np.array(T_flat, dtype=np.float64).reshape(4, 4)
                    self._calibrated = True
                    # Check if extrinsics are STILL placeholder (identity).
                    # If so, 3D positions will be in CAMERA frame, not robot
                    # base frame, which breaks arm-coordinated fetching.
                    if np.allclose(self.T, np.eye(4), atol=1e-6):
                        logger.warning(
                            "T_robot_camera is IDENTITY (not yet calibrated). "
                            "3D positions will be in CAMERA frame, NOT robot base "
                            "frame — arm movements will be incorrect. "
                            "Run 'admin.py calibrate' Step 5 to set real extrinsics."
                        )
        except Exception:
            pass  # use placeholders

    def update_intrinsics(self, fx: float, fy: float, cx: float, cy: float):
        """
        Update camera intrinsics from a live CameraInfo topic.
        This lets the system use the driver's calibrated values immediately
        without waiting for system.yaml to be rewritten.
        """
        values = [fx, fy, cx, cy]
        if not all(np.isfinite(v) and float(v) > 0.0 for v in values):
            return
        self.fx = float(fx)
        self.fy = float(fy)
        self.cx = float(cx)
        self.cy = float(cy)

    def pixel_to_robot(self, bbox: tuple, depth_frame: np.ndarray,
                      T_override: np.ndarray | None = None):
        """
        Converts a bounding box centre pixel + depth to 3D robot-frame coordinates.

        Inputs:
            bbox        — (x1, y1, x2, y2) pixel coordinates
            depth_frame — H x W uint16 array, values in millimetres
            T_override  — optional 4x4 camera-to-robot transform.  Use this for
                          wrist-mounted cameras where T changes with every arm
                          pose.  When None, falls back to self.T (static / table-
                          mounted camera path).

        Returns:
            (x, y, z) tuple in metres in robot base frame,
            or None if depth is invalid (zero, out of range, or no data).

        HP60C valid depth range: 200mm – 4000mm.
        Pixels outside this range are treated as invalid.
        """
        x1, y1, x2, y2 = bbox
        u = (x1 + x2) // 2   # bbox centre x
        v = (y1 + y2) // 2   # bbox centre y

        # Clamp to frame bounds
        h, w = depth_frame.shape[:2]
        u = int(min(max(u, 0), w - 1))
        v = int(min(max(v, 0), h - 1))

        # Read depth at the centre pixel. If it's a hole (0 or out of range),
        # fall back to the median of valid depths in a window around the centre.
        # HP60C depth can be sparse (reflective surfaces, IR shadows), so a
        # single-pixel read often misses. The window makes localisation robust.
        depth_mm = float(depth_frame[v, u])
        if depth_mm < 200 or depth_mm > 4000:
            half = 20  # 40x40 window
            u1 = max(0, u - half); u2 = min(w, u + half)
            v1 = max(0, v - half); v2 = min(h, v + half)
            window = depth_frame[v1:v2, u1:u2].astype(np.float32)
            valid = window[(window >= 200) & (window <= 4000)]
            if valid.size == 0:
                return None
            depth_mm = float(np.median(valid))

        # H9: Guard against NaN/Inf depth values
        if not np.isfinite(depth_mm):
            return None

        depth_m = depth_mm / 1000.0

        # Pinhole back-projection: pixel → camera frame
        X_cam = (u - self.cx) * depth_m / self.fx
        Y_cam = (v - self.cy) * depth_m / self.fy
        Z_cam = depth_m

        # H9: Guard against NaN/Inf from camera parameters
        if not all(np.isfinite(v) for v in [X_cam, Y_cam, Z_cam]):
            return (0.0, 0.0, 0.0)

        # Transform to robot base frame
        T = T_override if T_override is not None else self.T
        P_cam   = np.array([X_cam, Y_cam, Z_cam, 1.0])
        P_robot = T @ P_cam

        return (float(P_robot[0]), float(P_robot[1]), float(P_robot[2]))

    def compute_pregrasp(self, grasp_point: tuple, approach_dist_m: float = 0.05) -> tuple:
        """
        Returns a pre-grasp point 5cm above the grasp point in robot Z.
        The arm moves to pre-grasp first, then descends to grasp.

        Input:  (x, y, z) grasp point in robot frame (metres)
        Output: (x, y, z + 0.05) pre-grasp point
        """
        x, y, z = grasp_point
        return (x, y, z + approach_dist_m)

    def is_calibrated(self) -> bool:
        """Returns True if real calibration data was loaded from system.yaml."""
        return self._calibrated

    # ------------------------------------------------------------------
    # Wrist-mounted camera helpers
    # ------------------------------------------------------------------

    def compute_T_for_viewpoint(
        self,
        joint_angles: list[float],
        arm_link_lengths: dict | None = None,
        T_flange_camera: np.ndarray | None = None,
    ) -> np.ndarray:
        """
        Computes the 4x4 camera-to-robot-base transform for a wrist-mounted
        camera at a given arm pose.

        T_robot_camera = T_robot_flange(joints) × T_flange_camera

        Parameters:
            joint_angles     — 6 joint angles (radians) at the current viewpoint
            arm_link_lengths — dict with keys: base_height, upper_arm, forearm.
                               If None, falls back to defaults from the arm spec.
            T_flange_camera  — 4x4 fixed offset from wrist flange to camera lens.
                               If None, uses self._T_flange_camera (loaded from
                               system.yaml) or a sensible default.

        Returns:
            4x4 numpy array (T_robot_camera).
        """
        if T_flange_camera is None:
            T_flange_camera = self._T_flange_camera
        if arm_link_lengths is None:
            arm_link_lengths = {}

        L1     = float(arm_link_lengths.get('upper_arm',  0.400))
        L2     = float(arm_link_lengths.get('forearm',    0.400))
        base_h = float(arm_link_lengths.get('base_height', 0.352))

        j = [float(v) for v in joint_angles]
        j1, j2, j3, j4, j5, j6 = j

        # --- Flange position from FK (position-carrying joints J1-J3) ---
        r = L1 * math.cos(j2) + L2 * math.cos(j2 + j3)
        zr = base_h + L1 * math.sin(j2) + L2 * math.sin(j2 + j3)

        fx = r * math.cos(j1)
        fy = r * math.sin(j1)
        fz = zr

        # --- Flange orientation ---
        # The forearm absolute pitch is (j2 + j3).  J4 is wrist roll, J5 is
        # wrist pitch, J6 is wrist yaw.  For the NBV viewpoints the wrist is
        # configured for a top-down look (J5 closes the chain to vertical).
        # We build the rotation as R = Rz(j1) · Ry(-(j2+j3)) · Rz(j4) · Ry(j5) · Rz(j6)
        # but simplify using the fact that at calibrated viewpoints J4≈0, J6≈0.
        c1, s1 = math.cos(j1), math.sin(j1)
        # Forearm direction in the arm plane:
        abs_pitch = j2 + j3 + j5   # absolute pitch including wrist
        cp, sp = math.cos(abs_pitch), math.sin(abs_pitch)

        # Rotation matrix: camera Z points along the forearm direction,
        # camera X is roughly "forward" in the horizontal plane, Y completes.
        # This is a simplified but correct parameterisation for the top-down
        # viewpoints where the camera looks straight down.
        R = np.array([
            [ c1 * cp, -s1,  c1 * sp],
            [ s1 * cp,  c1,  s1 * sp],
            [   -sp,    0.0,    cp   ],
        ])

        T_robot_flange = np.eye(4)
        T_robot_flange[:3, :3] = R
        T_robot_flange[:3, 3] = [fx, fy, fz]

        return T_robot_flange @ T_flange_camera

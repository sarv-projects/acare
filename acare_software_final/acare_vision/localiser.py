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

import numpy as np
import yaml
from pathlib import Path

from acare_bringup.paths import SYSTEM_YAML

# Placeholder intrinsics — typical values for a 640x480 camera at ~60° FOV
# MUST be replaced with calibrated values before deployment
PLACEHOLDER_FX = 554.0   # focal length x in pixels
PLACEHOLDER_FY = 554.0   # focal length y in pixels
PLACEHOLDER_CX = 320.0   # principal point x (image centre)
PLACEHOLDER_CY = 240.0   # principal point y (image centre)

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
        self._load_config()

    def _load_config(self):
        if not SYSTEM_YAML.exists():
            return
        try:
            with open(SYSTEM_YAML) as f:
                cfg = yaml.safe_load(f)
            cam = cfg.get('camera', {})
            if all(k in cam for k in ('fx', 'fy', 'cx', 'cy', 'T_robot_camera')):
                self.fx = float(cam['fx'])
                self.fy = float(cam['fy'])
                self.cx = float(cam['cx'])
                self.cy = float(cam['cy'])
                T_flat  = cam['T_robot_camera']
                self.T  = np.array(T_flat, dtype=np.float64).reshape(4, 4)
                self._calibrated = True
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

    def pixel_to_robot(self, bbox: tuple, depth_frame: np.ndarray):
        """
        Converts a bounding box centre pixel + depth to 3D robot-frame coordinates.

        Inputs:
            bbox        — (x1, y1, x2, y2) pixel coordinates
            depth_frame — H x W uint16 array, values in millimetres

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

        depth_mm = float(depth_frame[v, u])

        # HP60C valid range: 200mm – 4000mm
        if depth_mm < 200 or depth_mm > 4000:
            return None

        depth_m = depth_mm / 1000.0

        # Pinhole back-projection: pixel → camera frame
        X_cam = (u - self.cx) * depth_m / self.fx
        Y_cam = (v - self.cy) * depth_m / self.fy
        Z_cam = depth_m

        # Transform to robot base frame
        P_cam   = np.array([X_cam, Y_cam, Z_cam, 1.0])
        P_robot = self.T @ P_cam

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

# acare_vision/fake_detector.py
# Spec Reference: Section XI (Fake Object Detection)
#
# Dual-signal fake object detector.
# Both signals must be below threshold to reject as fake.
# This prevents false rejection of shiny real surgical tools
# (which have low texture but high depth variance).
#
# Thresholds are loaded from thresholds.yaml.
# Default values are starting estimates — MUST be calibrated empirically
# using 20 real tools + 20 printed replicas (admin.py calibrate Step 6).

import cv2
import numpy as np
import yaml
from acare_bringup.paths import THRESHOLDS_YAML

# Default thresholds — overridden by thresholds.yaml if present
DEFAULT_TEXTURE_THRESH = 120.0   # Laplacian variance
DEFAULT_DEPTH_THRESH   = 0.002   # depth variance in metres^2

THRESHOLDS_PATH = THRESHOLDS_YAML


class FakeDetector:
    """
    Detects whether a detected object is a real surgical tool or a fake/printed replica.

    Uses two independent signals:
      Signal 1 — Texture variance: Laplacian of the ROI grayscale image.
                 Real tools have surface texture; printed replicas are flat.
      Signal 2 — Depth variance: variance of depth values within the ROI.
                 Real 3D objects have depth variation; flat replicas do not.

    Both signals must be below their thresholds to flag as fake.
    If only one is low, the object is NOT rejected (reduces false positives
    on shiny tools like scalpels which have low texture but real 3D shape).

    If depth data is unavailable for the ROI (< 10 valid pixels), the detector
    returns False (benefit of the doubt) and logs DEPTH_UNAVAILABLE.
    """

    def __init__(self):
        self.texture_thresh = DEFAULT_TEXTURE_THRESH
        self.depth_thresh   = DEFAULT_DEPTH_THRESH
        self._load_thresholds()

    def _load_thresholds(self):
        if THRESHOLDS_PATH.exists():
            try:
                with open(THRESHOLDS_PATH) as f:
                    cfg = yaml.safe_load(f)
                fd = cfg.get('fake_detection', {})
                self.texture_thresh = fd.get('texture_variance_threshold', DEFAULT_TEXTURE_THRESH)
                self.depth_thresh   = fd.get('depth_variance_threshold',   DEFAULT_DEPTH_THRESH)
            except Exception:
                pass  # use defaults if file is malformed

    def is_fake(self, rgb_frame: np.ndarray, depth_frame: np.ndarray, bbox: tuple) -> bool:
        """
        Inputs:
            rgb_frame   — H x W x 3 uint8, BGR or RGB (Laplacian is colour-agnostic)
            depth_frame — H x W uint16, values in millimetres (HP60C native format)
            bbox        — (x1, y1, x2, y2) pixel coordinates of the detection bounding box

        Returns:
            True  — object is likely a fake/printed replica → reject
            False — object appears real → proceed with grasp
        """
        x1, y1, x2, y2 = bbox

        # Guard: empty or degenerate bounding box
        if x2 <= x1 or y2 <= y1:
            return False

        # Clamp to frame bounds
        h, w = rgb_frame.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)

        if x2 <= x1 or y2 <= y1:
            return False

        # --- Signal 1: Texture variance via Laplacian ---
        roi_gray = cv2.cvtColor(rgb_frame[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
        texture_var = float(cv2.Laplacian(roi_gray, cv2.CV_64F).var())

        # --- Signal 2: Depth variance ---
        depth_roi = depth_frame[y1:y2, x1:x2].astype(np.float32)
        depth_roi_m = depth_roi / 1000.0   # mm → metres
        valid_depth = depth_roi_m[depth_roi_m > 0]

        if len(valid_depth) < 10:
            # Depth unavailable — cannot make a reliable fake determination
            # Return False (benefit of the doubt) — caller should log DEPTH_UNAVAILABLE
            return False

        depth_var = float(np.var(valid_depth))

        # Both signals below threshold → fake
        return (texture_var < self.texture_thresh) and (depth_var < self.depth_thresh)

    def compute_signals(self, rgb_frame: np.ndarray, depth_frame: np.ndarray, bbox: tuple) -> dict:
        """
        Returns the raw signal values for a bounding box — useful for calibration.
        Run this on 20 real tools and 20 fakes to determine correct thresholds.
        """
        x1, y1, x2, y2 = bbox
        h, w = rgb_frame.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        if x2 <= x1 or y2 <= y1:
            return {
                'texture_variance': -1.0,
                'depth_variance': -1.0,
                'texture_thresh': self.texture_thresh,
                'depth_thresh': self.depth_thresh,
                'is_fake': False,
            }

        roi_gray = cv2.cvtColor(rgb_frame[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
        texture_var = float(cv2.Laplacian(roi_gray, cv2.CV_64F).var())

        depth_roi = depth_frame[y1:y2, x1:x2].astype(np.float32) / 1000.0
        valid = depth_roi[depth_roi > 0]
        depth_var = float(np.var(valid)) if len(valid) >= 10 else -1.0

        return {
            'texture_variance': texture_var,
            'depth_variance':   depth_var,
            'texture_thresh':   self.texture_thresh,
            'depth_thresh':     self.depth_thresh,
            'is_fake':          self.is_fake(rgb_frame, depth_frame, bbox),
        }

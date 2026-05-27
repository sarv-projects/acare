"""Passive face detection helper used by auth_node for the always-on
login scan.

The HP60C camera publishes BGR8 frames. MediaPipe expects RGB. The
previous implementation took the parameter name ``rgb_frame`` at face
value and passed BGR straight to ``FaceDetection.process``, which works
just well enough for the bug to go unnoticed but degrades detection
quality especially under warm lighting (the red and blue channels swap
brightness). This module now normalises the colour ordering before
inference and accepts either layout.
"""

from __future__ import annotations

import numpy as np


class PassiveFaceDetector:
    def __init__(self):
        self._detector = None
        try:
            import mediapipe as mp

            self._detector = mp.solutions.face_detection.FaceDetection(
                model_selection=0,
                min_detection_confidence=0.6,
            )
        except Exception:
            self._detector = None

    @property
    def available(self) -> bool:
        return self._detector is not None

    @staticmethod
    def _ensure_rgb(frame: np.ndarray) -> np.ndarray:
        """Convert a BGR frame to RGB. Pass-through for non-3-channel frames."""
        if frame is None:
            return frame
        if frame.ndim != 3 or frame.shape[2] != 3:
            return frame
        # Cheap channel swap; cv2.cvtColor would also work but adds a hard
        # OpenCV dep. ``ascontiguousarray`` keeps MediaPipe happy.
        return np.ascontiguousarray(frame[:, :, ::-1])

    def face_present(self, frame: np.ndarray) -> bool:
        """Return True if at least one face is visible.

        ``frame`` may be either BGR (HP60C native) or RGB; we normalise
        before inference. The historical kwarg name ``rgb_frame`` is kept
        as an alias for callers that already pass it that way.
        """
        if self._detector is None or frame is None:
            return False
        rgb = self._ensure_rgb(frame)
        results = self._detector.process(rgb)
        return bool(results.detections)

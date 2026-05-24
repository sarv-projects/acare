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

    def face_present(self, rgb_frame: np.ndarray) -> bool:
        if self._detector is None or rgb_frame is None:
            return False
        results = self._detector.process(rgb_frame)
        return bool(results.detections)

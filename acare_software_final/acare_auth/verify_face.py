from __future__ import annotations

import numpy as np


class FaceVerifier:
    THRESHOLD = 0.78

    def __init__(self):
        self._backend = None
        try:
            import insightface

            app = insightface.app.FaceAnalysis(
                name="buffalo_sc",
                providers=["CPUExecutionProvider"],
            )
            app.prepare(ctx_id=-1, det_size=(320, 320))
            self._backend = app
        except Exception:
            self._backend = None

    @property
    def available(self) -> bool:
        return self._backend is not None

    def embed(self, bgr_frame: np.ndarray) -> np.ndarray | None:
        if self._backend is None:
            return None
        faces = self._backend.get(bgr_frame)
        if not faces:
            return None
        largest = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
        return np.asarray(largest.normed_embedding, dtype=np.float32)

    def verify(self, bgr_frame: np.ndarray, stored_embedding: np.ndarray) -> tuple[bool, float]:
        emb = self.embed(bgr_frame)
        if emb is None or stored_embedding is None:
            return False, 0.0
        sim = float(np.dot(emb, stored_embedding))
        return sim >= self.THRESHOLD, sim

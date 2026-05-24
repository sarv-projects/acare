from __future__ import annotations

import numpy as np


class VoiceVerifier:
    THRESHOLD = 0.85

    def __init__(self):
        self._classifier = None
        try:
            from speechbrain.inference.speaker import EncoderClassifier

            self._classifier = EncoderClassifier.from_hparams(
                source="speechbrain/spkrec-ecapa-voxceleb",
                savedir="models/ecapa_tdnn",
                run_opts={"device": "cpu"},
            )
        except Exception:
            self._classifier = None

    @property
    def available(self) -> bool:
        return self._classifier is not None

    def embed(self, audio_tensor) -> np.ndarray | None:
        if self._classifier is None:
            return None
        import torch

        with torch.no_grad():
            emb = self._classifier.encode_batch(audio_tensor.unsqueeze(0))
        return emb.squeeze().cpu().numpy().astype(np.float32)

    def verify(self, audio_tensor, stored_embedding: np.ndarray) -> tuple[bool, float]:
        emb = self.embed(audio_tensor)
        if emb is None or stored_embedding is None:
            return False, 0.0
        sim = float(np.dot(emb, stored_embedding) / (np.linalg.norm(emb) * np.linalg.norm(stored_embedding) + 1e-8))
        return sim >= self.THRESHOLD, sim

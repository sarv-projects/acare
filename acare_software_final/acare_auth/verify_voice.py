"""
ECAPA-TDNN speaker verification — ONNX runtime path (lightweight)
with SpeechBrain fallback (heavyweight, dev convenience).

Spec Reference: Section VII, XXIII (speaker verification, threshold 0.85).

Why ONNX-first?
  SpeechBrain pulls torch + transformers + hyperpyyaml + sentencepiece
  (~500 MB on disk, slow cold start). The ECAPA-TDNN checkpoint itself
  is only ~17 MB. Running it through onnxruntime (already in our stack
  for YOLO) is ~3x faster on Pi 5 CPU and adds zero new runtime weight.

Embedding format:
  192-D float32, L2-normalised. Same dimensionality whether inferred
  via ONNX or SpeechBrain — existing enrolled embeddings remain valid.

Audio format:
  16 kHz mono float32 in [-1.0, 1.0]. The auth_node already converts
  Transcript.pcm16 (int16) into a torch tensor at 16 kHz.

Model file:
  models/ecapa_tdnn.onnx
  Exported once with: scripts/export_ecapa_onnx.py
  (or supplied pre-exported in models/).
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np

from acare_bringup.paths import MODEL_DIR

LOG = logging.getLogger("acare_auth.verify_voice")

ECAPA_ONNX_PATH = MODEL_DIR / "ecapa_tdnn.onnx"
SAMPLE_RATE = 16_000


def _l2_normalise(vec: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(vec))
    if not np.isfinite(norm) or norm < 1e-8:
        return vec
    return (vec / norm).astype(np.float32)


def _to_numpy_audio(audio_tensor: Any) -> np.ndarray | None:
    """Accept torch tensor or numpy array. Return float32 1-D in [-1, 1]."""
    if audio_tensor is None:
        return None
    try:
        if hasattr(audio_tensor, "detach"):
            arr = audio_tensor.detach().cpu().numpy()
        else:
            arr = np.asarray(audio_tensor)
    except Exception:
        return None
    arr = np.asarray(arr, dtype=np.float32).reshape(-1)
    if arr.size == 0 or not np.isfinite(arr).all():
        return None
    return arr


class _ONNXBackend:
    """Lightweight onnxruntime path. Preferred when the .onnx export exists."""

    def __init__(self, onnx_path: Path):
        self._session = None
        self._input_name = ""
        try:
            import onnxruntime as ort

            providers = ["CPUExecutionProvider"]
            sess_opts = ort.SessionOptions()
            sess_opts.intra_op_num_threads = 1
            sess_opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            self._session = ort.InferenceSession(str(onnx_path), sess_opts, providers=providers)
            self._input_name = self._session.get_inputs()[0].name
        except Exception as exc:
            LOG.info("ECAPA ONNX backend unavailable: %s", exc)
            self._session = None

    @property
    def available(self) -> bool:
        return self._session is not None

    def embed(self, audio: np.ndarray) -> np.ndarray | None:
        if self._session is None:
            return None
        # Model expects shape (batch, samples) at 16 kHz, float32.
        feats = audio.reshape(1, -1).astype(np.float32)
        try:
            out = self._session.run(None, {self._input_name: feats})[0]
        except Exception as exc:
            LOG.warning("ECAPA ONNX inference failed: %s", exc)
            return None
        emb = np.asarray(out, dtype=np.float32).reshape(-1)
        return _l2_normalise(emb)


class _SpeechBrainBackend:
    """Fallback: full speechbrain runtime. Used only when no ONNX export is present."""

    def __init__(self):
        self._classifier = None
        try:
            from speechbrain.inference.speaker import EncoderClassifier

            self._classifier = EncoderClassifier.from_hparams(
                source="speechbrain/spkrec-ecapa-voxceleb",
                savedir=str(MODEL_DIR / "ecapa_tdnn_sb"),
                run_opts={"device": "cpu"},
            )
        except Exception as exc:
            LOG.info("SpeechBrain backend unavailable: %s", exc)
            self._classifier = None

    @property
    def available(self) -> bool:
        return self._classifier is not None

    def embed(self, audio: np.ndarray) -> np.ndarray | None:
        if self._classifier is None:
            return None
        try:
            import torch

            tensor = torch.from_numpy(audio).unsqueeze(0)
            with torch.no_grad():
                emb_t = self._classifier.encode_batch(tensor)
            emb = emb_t.squeeze().cpu().numpy().astype(np.float32)
            return _l2_normalise(emb)
        except Exception as exc:
            LOG.warning("SpeechBrain inference failed: %s", exc)
            return None


class VoiceVerifier:
    """Speaker verification — ONNX runtime preferred, SpeechBrain fallback."""

    THRESHOLD = 0.85

    def __init__(self):
        self._backend = None
        if ECAPA_ONNX_PATH.exists():
            onnx = _ONNXBackend(ECAPA_ONNX_PATH)
            if onnx.available:
                self._backend = onnx
                LOG.info("VoiceVerifier: using ECAPA-TDNN ONNX (%s)", ECAPA_ONNX_PATH)
        if self._backend is None:
            sb = _SpeechBrainBackend()
            if sb.available:
                self._backend = sb
                LOG.info("VoiceVerifier: ECAPA ONNX missing, using SpeechBrain fallback")

    @property
    def available(self) -> bool:
        return self._backend is not None

    def embed(self, audio_tensor) -> np.ndarray | None:
        if self._backend is None:
            return None
        audio = _to_numpy_audio(audio_tensor)
        if audio is None:
            return None
        return self._backend.embed(audio)

    def verify(self, audio_tensor, stored_embedding: np.ndarray) -> tuple[bool, float]:
        emb = self.embed(audio_tensor)
        if emb is None or stored_embedding is None:
            return False, 0.0
        ref = _l2_normalise(np.asarray(stored_embedding, dtype=np.float32))
        sim = float(np.dot(emb, ref))
        return sim >= self.THRESHOLD, sim

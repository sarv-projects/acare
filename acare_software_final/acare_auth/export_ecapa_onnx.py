"""
One-shot script: export SpeechBrain ECAPA-TDNN to ONNX.

Run this ONCE on any machine (laptop or Colab) that has speechbrain + torch.
Output goes to acare_software_final/models/ecapa_tdnn.onnx (~17 MB).
After that, the Pi only needs onnxruntime — no torch, no speechbrain.

Usage:
    python -m acare_auth.export_ecapa_onnx
"""
from __future__ import annotations

from pathlib import Path

from acare_bringup.paths import MODEL_DIR

OUTPUT_PATH = MODEL_DIR / "ecapa_tdnn.onnx"


def main() -> int:
    try:
        import torch
        from speechbrain.inference.speaker import EncoderClassifier
    except ImportError as exc:
        print(f"[export_ecapa_onnx] missing dependency: {exc}")
        print("Install with: pip install speechbrain torch")
        return 1

    print("[export_ecapa_onnx] downloading speechbrain/spkrec-ecapa-voxceleb...")
    classifier = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir=str(MODEL_DIR / "ecapa_tdnn_sb"),
        run_opts={"device": "cpu"},
    )

    encoder = classifier.mods.embedding_model.eval()

    class Wrapper(torch.nn.Module):
        """Thin wrapper: raw audio (B, T) at 16 kHz → 192-D embedding."""

        def __init__(self, classifier_, encoder_):
            super().__init__()
            self.compute_features = classifier_.mods.compute_features
            self.mean_var_norm = classifier_.mods.mean_var_norm
            self.encoder = encoder_

        def forward(self, audio: torch.Tensor) -> torch.Tensor:
            feats = self.compute_features(audio)
            wav_lens = torch.ones(audio.shape[0], device=audio.device)
            feats = self.mean_var_norm(feats, wav_lens)
            emb = self.encoder(feats)            # (B, 1, 192)
            return emb.squeeze(1)                # (B, 192)

    model = Wrapper(classifier, encoder).eval()
    dummy = torch.randn(1, 16_000 * 3)            # 3 s of audio at 16 kHz

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"[export_ecapa_onnx] exporting → {OUTPUT_PATH}")
    torch.onnx.export(
        model,
        dummy,
        str(OUTPUT_PATH),
        input_names=["audio"],
        output_names=["embedding"],
        dynamic_axes={"audio": {0: "batch", 1: "samples"}, "embedding": {0: "batch"}},
        opset_version=17,
        do_constant_folding=True,
    )
    size_mb = OUTPUT_PATH.stat().st_size / (1024 * 1024)
    print(f"[export_ecapa_onnx] done — {size_mb:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

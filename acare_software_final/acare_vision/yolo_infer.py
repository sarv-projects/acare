from __future__ import annotations

import cv2
import numpy as np
import onnxruntime as ort
import yaml

from acare_bringup.paths import SYSTEM_YAML


DEFAULT_CLASS_SETS = {
    8: [
        "scalpel",
        "scissors",
        "forceps",
        "bandage",
        "gauze",
        "thermometer",
        "oximeter",
        "plaster",
    ],
    6: [
        "cream",
        "scissors",
        "oximeter",
        "plaster",
        "forceps",
        "thermometer",
    ],
}


class YOLOv11ONNX:
    def __init__(self, model_path: str, conf_thresh: float = 0.70):
        opts = ort.SessionOptions()
        opts.intra_op_num_threads = 4
        opts.inter_op_num_threads = 1
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.session = ort.InferenceSession(
            model_path,
            sess_options=opts,
            providers=["CPUExecutionProvider"],
        )
        self.input_name = self.session.get_inputs()[0].name
        _, _, self.H, self.W = self.session.get_inputs()[0].shape
        self.conf_thresh = conf_thresh
        output_shape = self.session.get_outputs()[0].shape
        output_channels = output_shape[1] if len(output_shape) >= 2 and isinstance(output_shape[1], int) else 12
        self.num_classes = max(1, int(output_channels) - 4)
        self.class_names = DEFAULT_CLASS_SETS.get(
            self.num_classes,
            [f"class_{idx}" for idx in range(self.num_classes)],
        )
        cfg = self._load_vision_config()
        self.low_light_v_mean_threshold = float(cfg.get("low_light_v_mean_threshold", 75.0))
        self.very_low_light_v_mean_threshold = float(cfg.get("very_low_light_v_mean_threshold", 52.0))
        self.low_light_conf_thresh = float(cfg.get("low_light_confidence_threshold", max(0.50, conf_thresh - 0.12)))
        self.low_light_enable_tta = bool(cfg.get("low_light_enable_tta", True))
        self.gamma_dark = float(cfg.get("low_light_gamma_dark", 1.55))
        self.gamma_very_dark = float(cfg.get("low_light_gamma_very_dark", 1.85))
        self.enable_unsharp_mask = bool(cfg.get("low_light_enable_unsharp_mask", True))

    def _load_vision_config(self) -> dict:
        try:
            with open(SYSTEM_YAML, "r", encoding="utf-8") as handle:
                cfg = yaml.safe_load(handle) or {}
            return cfg.get("vision", {}) or {}
        except Exception:
            return {}

    def _scene_profile(self, bgr_frame: np.ndarray) -> dict:
        hsv = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)
        v_channel = hsv[:, :, 2]
        v_mean = float(np.mean(v_channel))
        v_std = float(np.std(v_channel))
        saturation_mean = float(np.mean(hsv[:, :, 1]))
        lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        is_very_dark = v_mean < self.very_low_light_v_mean_threshold
        is_low_light = v_mean < self.low_light_v_mean_threshold
        is_low_contrast = v_std < 28.0
        return {
            "v_mean": v_mean,
            "v_std": v_std,
            "s_mean": saturation_mean,
            "lap_var": lap_var,
            "is_low_light": is_low_light,
            "is_very_dark": is_very_dark,
            "is_low_contrast": is_low_contrast,
        }

    def preprocess(self, bgr_frame: np.ndarray) -> np.ndarray:
        enhanced = self._enhance_for_low_light(bgr_frame, self._scene_profile(bgr_frame))
        img = cv2.resize(enhanced, (self.W, self.H))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        return np.expand_dims(img, axis=0)

    def _apply_gamma(self, bgr_frame: np.ndarray, gamma: float) -> np.ndarray:
        if gamma <= 0.0:
            return bgr_frame
        inv_gamma = 1.0 / gamma
        table = np.array([(i / 255.0) ** inv_gamma * 255.0 for i in range(256)], dtype=np.float32)
        return cv2.LUT(bgr_frame, table.astype(np.uint8))

    def _apply_unsharp_mask(self, bgr_frame: np.ndarray) -> np.ndarray:
        blurred = cv2.GaussianBlur(bgr_frame, (0, 0), 1.2)
        return cv2.addWeighted(bgr_frame, 1.25, blurred, -0.25, 0)

    def _enhance_for_low_light(self, bgr_frame: np.ndarray, profile: dict | None = None) -> np.ndarray:
        profile = profile or self._scene_profile(bgr_frame)
        if not profile["is_low_light"]:
            return bgr_frame

        working = cv2.fastNlMeansDenoisingColored(bgr_frame, None, 3, 3, 7, 21)
        gamma = self.gamma_very_dark if profile["is_very_dark"] else self.gamma_dark
        working = self._apply_gamma(working, gamma)

        lab = cv2.cvtColor(working, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        clip_limit = 3.2 if profile["is_very_dark"] else 2.4
        tile_grid = (6, 6) if profile["is_low_contrast"] else (8, 8)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid)
        l_channel = clahe.apply(l_channel)
        enhanced = cv2.merge((l_channel, a_channel, b_channel))
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        if self.enable_unsharp_mask:
            enhanced = self._apply_unsharp_mask(enhanced)
        return enhanced

    def _prepare_input(self, bgr_frame: np.ndarray) -> np.ndarray:
        img = cv2.resize(bgr_frame, (self.W, self.H))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        return np.expand_dims(img, axis=0)

    def _make_inference_variants(self, bgr_frame: np.ndarray, profile: dict) -> list[tuple[str, np.ndarray]]:
        variants = [("base", bgr_frame)]
        if not profile["is_low_light"]:
            return variants

        enhanced = self._enhance_for_low_light(bgr_frame, profile)
        variants.append(("enhanced", enhanced))

        if self.low_light_enable_tta:
            gamma = 1.95 if profile["is_very_dark"] else 1.65
            brighter = self._apply_gamma(bgr_frame, gamma)
            if self.enable_unsharp_mask:
                brighter = self._apply_unsharp_mask(brighter)
            variants.append(("bright", brighter))

        return variants

    def _postprocess_single(
        self,
        output: np.ndarray,
        orig_h: int,
        orig_w: int,
        score_threshold: float,
        variant_name: str,
    ) -> list[dict]:
        preds = output[0].T
        boxes_xywh = preds[:, :4]
        scores = preds[:, 4:]
        class_ids = np.argmax(scores, axis=1)
        confidences = scores[np.arange(len(scores)), class_ids]
        mask = confidences >= score_threshold
        boxes_xywh = boxes_xywh[mask]
        class_ids = class_ids[mask]
        confidences = confidences[mask]
        if len(boxes_xywh) == 0:
            return []

        scale_x = orig_w / self.W
        scale_y = orig_h / self.H
        cx = boxes_xywh[:, 0] * self.W * scale_x
        cy = boxes_xywh[:, 1] * self.H * scale_y
        bw = boxes_xywh[:, 2] * self.W * scale_x
        bh = boxes_xywh[:, 3] * self.H * scale_y
        x1 = (cx - bw / 2).astype(int)
        y1 = (cy - bh / 2).astype(int)
        x2 = (cx + bw / 2).astype(int)
        y2 = (cy + bh / 2).astype(int)

        results = []
        for i in range(len(x1)):
            class_name = self.class_names[int(class_ids[i])]
            results.append(
                {
                    "class_id": int(class_ids[i]),
                    "class_name": class_name,
                    "canonical_name": class_name,
                    "confidence": float(confidences[i]),
                    "bbox": (int(x1[i]), int(y1[i]), int(x2[i]), int(y2[i])),
                    "variant": variant_name,
                }
            )
        return results

    def postprocess(self, output: np.ndarray, orig_h: int, orig_w: int) -> list[dict]:
        detections = self._postprocess_single(output, orig_h, orig_w, self.conf_thresh, "base")
        return self._merge_detections(detections, self.conf_thresh)

    def _merge_detections(self, detections: list[dict], score_threshold: float) -> list[dict]:
        if not detections:
            return []

        boxes_for_nms = []
        confidences = []
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            boxes_for_nms.append([int(x1), int(y1), int(x2 - x1), int(y2 - y1)])
            confidences.append(float(det["confidence"]))

        indices = cv2.dnn.NMSBoxes(
            boxes_for_nms,
            confidences,
            score_threshold=score_threshold,
            nms_threshold=0.45,
        )
        if len(indices) == 0:
            return []
        return [detections[int(i)] for i in indices.flatten()]

    def infer(self, bgr_frame: np.ndarray) -> list[dict]:
        h, w = bgr_frame.shape[:2]
        profile = self._scene_profile(bgr_frame)
        variants = self._make_inference_variants(bgr_frame, profile)
        score_threshold = self.low_light_conf_thresh if profile["is_low_light"] else self.conf_thresh
        detections = []
        for variant_name, variant_frame in variants:
            inp = self._prepare_input(variant_frame)
            outputs = self.session.run(None, {self.input_name: inp})
            detections.extend(
                self._postprocess_single(outputs[0], h, w, score_threshold, variant_name)
            )
        merged = self._merge_detections(detections, score_threshold)
        for det in merged:
            det["scene_low_light"] = bool(profile["is_low_light"])
            det["scene_very_dark"] = bool(profile["is_very_dark"])
            det["scene_v_mean"] = float(profile["v_mean"])
        return merged

    def infer_multi_frame(self, frames: list[np.ndarray]) -> list[dict]:
        all_boxes = []
        all_scores = []
        all_class_ids = []
        all_names = []
        all_variants = []
        low_light_scores = []
        for frame in frames:
            if frame is None:
                continue
            for detection in self.infer(frame):
                x1, y1, x2, y2 = detection["bbox"]
                all_boxes.append([x1, y1, x2 - x1, y2 - y1])
                all_scores.append(detection["confidence"])
                all_class_ids.append(detection["class_id"])
                all_names.append(detection["class_name"])
                all_variants.append(detection.get("variant", "base"))
                low_light_scores.append(bool(detection.get("scene_low_light", False)))
        if not all_boxes:
            return []

        score_threshold = self.low_light_conf_thresh if any(low_light_scores) else self.conf_thresh
        indices = cv2.dnn.NMSBoxes(
            all_boxes,
            all_scores,
            score_threshold=score_threshold,
            nms_threshold=0.45,
        )
        if len(indices) == 0:
            return []

        merged = []
        for i in indices.flatten():
            x, y, w, h = all_boxes[i]
            merged.append(
                {
                    "class_id": all_class_ids[i],
                    "class_name": all_names[i],
                    "canonical_name": all_names[i],
                    "confidence": all_scores[i],
                    "bbox": (x, y, x + w, y + h),
                    "variant": all_variants[i],
                    "scene_low_light": low_light_scores[i],
                }
            )
        return merged

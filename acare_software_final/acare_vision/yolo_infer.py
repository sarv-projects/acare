from __future__ import annotations

import cv2
import numpy as np
import onnxruntime as ort


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

    def preprocess(self, bgr_frame: np.ndarray) -> np.ndarray:
        enhanced = self._enhance_for_low_light(bgr_frame)
        img = cv2.resize(enhanced, (self.W, self.H))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        return np.expand_dims(img, axis=0)

    def _enhance_for_low_light(self, bgr_frame: np.ndarray) -> np.ndarray:
        hsv = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)
        v_mean = float(np.mean(hsv[:, :, 2]))
        if v_mean >= 70.0:
            return bgr_frame
        lab = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_channel = clahe.apply(l_channel)
        enhanced = cv2.merge((l_channel, a_channel, b_channel))
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

    def postprocess(self, output: np.ndarray, orig_h: int, orig_w: int) -> list[dict]:
        preds = output[0].T
        boxes_xywh = preds[:, :4]
        scores = preds[:, 4:]
        class_ids = np.argmax(scores, axis=1)
        confidences = scores[np.arange(len(scores)), class_ids]
        mask = confidences >= self.conf_thresh
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

        boxes_for_nms = [
            [int(x1[i]), int(y1[i]), int(x2[i] - x1[i]), int(y2[i] - y1[i])]
            for i in range(len(x1))
        ]
        indices = cv2.dnn.NMSBoxes(
            boxes_for_nms,
            confidences.tolist(),
            score_threshold=self.conf_thresh,
            nms_threshold=0.45,
        )
        if len(indices) == 0:
            return []

        results = []
        for i in indices.flatten():
            class_name = self.class_names[int(class_ids[i])]
            results.append(
                {
                    "class_id": int(class_ids[i]),
                    "class_name": class_name,
                    "canonical_name": class_name,
                    "confidence": float(confidences[i]),
                    "bbox": (int(x1[i]), int(y1[i]), int(x2[i]), int(y2[i])),
                }
            )
        return results

    def infer(self, bgr_frame: np.ndarray) -> list[dict]:
        h, w = bgr_frame.shape[:2]
        inp = self.preprocess(bgr_frame)
        outputs = self.session.run(None, {self.input_name: inp})
        return self.postprocess(outputs[0], h, w)

    def infer_multi_frame(self, frames: list[np.ndarray]) -> list[dict]:
        all_boxes = []
        all_scores = []
        all_class_ids = []
        all_names = []
        for frame in frames:
            if frame is None:
                continue
            for detection in self.infer(frame):
                x1, y1, x2, y2 = detection["bbox"]
                all_boxes.append([x1, y1, x2 - x1, y2 - y1])
                all_scores.append(detection["confidence"])
                all_class_ids.append(detection["class_id"])
                all_names.append(detection["class_name"])
        if not all_boxes:
            return []

        indices = cv2.dnn.NMSBoxes(
            all_boxes,
            all_scores,
            score_threshold=self.conf_thresh,
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
                }
            )
        return merged

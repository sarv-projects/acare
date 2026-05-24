# acare_vision/yolo_infer.py
# Spec Reference: Section XI (Vision Pipeline — YOLOv11 Inference)
#
# Wraps the ONNX YOLOv11m model for inference on Pi 5 CPU.
# Model: trained on 6 surgical tool classes, 320x320 input, FP32 ONNX.
#
# CLASS NAMES — must match training dataset exactly:
#   0: cream
#   1: medical scissors
#   2: oxymeter
#   3: plaster
#   4: surgical forceps
#   5: thermometer
#
# Note: spec listed 8 classes but model was trained on 6.
# Missing from model: scalpel, bandage, gauze.
# Update CLASS_NAMES if/when model is retrained with more classes.

import onnxruntime as ort
import numpy as np
import cv2

CLASS_NAMES = [
    'cream',
    'medical scissors',
    'oxymeter',
    'plaster',
    'surgical forceps',
    'thermometer',
]

# Map model class names to canonical tool names used in the rest of the system
# (intent_parser, normaliser, planner all use these canonical names)
CANONICAL_NAME = {
    'cream':            'cream',
    'medical scissors': 'scissors',
    'oxymeter':         'oximeter',
    'plaster':          'plaster',
    'surgical forceps': 'forceps',
    'thermometer':      'thermometer',
}


class YOLOv11ONNX:
    """
    Wraps the ONNX YOLOv11m model for inference on Pi 5 CPU.

    Initialisation:
        model_path  — path to .onnx file on Pi (e.g. /home/acare/models/yolo_acare.onnx)
        conf_thresh — minimum confidence to accept a detection (default 0.70)

    Uses all 4 Pi 5 CPU cores via intra_op_num_threads=4.
    Graph optimisation enabled for maximum CPU throughput.
    """

    def __init__(self, model_path: str, conf_thresh: float = 0.70):
        opts = ort.SessionOptions()
        opts.intra_op_num_threads = 4
        opts.inter_op_num_threads = 1
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        self.session = ort.InferenceSession(
            model_path,
            sess_options=opts,
            providers=['CPUExecutionProvider']
        )
        self.input_name = self.session.get_inputs()[0].name
        # Input shape is [1, 3, H, W] — fixed at export time (320x320)
        _, _, self.H, self.W = self.session.get_inputs()[0].shape
        self.conf_thresh = conf_thresh

    def preprocess(self, bgr_frame: np.ndarray) -> np.ndarray:
        """
        Prepares a BGR uint8 frame for model input.
        Steps: resize to 320x320 → BGR to RGB → normalise [0,1] → HWC to CHW → add batch dim.
        Returns float32 array of shape [1, 3, 320, 320].
        """
        img = cv2.resize(bgr_frame, (self.W, self.H))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        return img

    def postprocess(self, output: np.ndarray, orig_h: int, orig_w: int) -> list:
        """
        Converts raw model output to a list of detection dicts.

        Model output shape: [1, 10, 2100]
            10 = 4 box coords (cx, cy, w, h normalised) + 6 class scores
            2100 = number of anchor predictions at 320x320

        Steps:
        1. Transpose to [2100, 10]
        2. Extract box coords and class scores
        3. Find best class per anchor, filter by conf_thresh
        4. Scale boxes from 320x320 back to original frame size
        5. Apply NMS (threshold 0.45) to remove duplicate boxes
        6. Return list of dicts with class_id, class_name, canonical_name,
           confidence, and bbox (x1, y1, x2, y2) in original pixel coords
        """
        preds = output[0].T  # [2100, 10]

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

        boxes_xyxy = np.stack([x1, y1, x2, y2], axis=1).tolist()
        indices = cv2.dnn.NMSBoxes(
            boxes_xyxy,
            confidences.tolist(),
            score_threshold=self.conf_thresh,
            nms_threshold=0.45
        )
        if len(indices) == 0:
            return []

        results = []
        for i in indices.flatten():
            name = CLASS_NAMES[int(class_ids[i])]
            results.append({
                'class_id':      int(class_ids[i]),
                'class_name':    name,
                'canonical_name': CANONICAL_NAME.get(name, name),
                'confidence':    float(confidences[i]),
                'bbox':          (int(x1[i]), int(y1[i]), int(x2[i]), int(y2[i]))
            })
        return results

    def infer(self, bgr_frame: np.ndarray) -> list:
        """
        Run inference on a single BGR frame.
        Returns list of detection dicts (may be empty).
        Typical latency on Pi 5: 80-120ms per frame at 320x320 FP32.
        """
        h, w = bgr_frame.shape[:2]
        inp = self.preprocess(bgr_frame)
        outputs = self.session.run(None, {self.input_name: inp})
        return self.postprocess(outputs[0], h, w)

    def infer_multi_frame(self, frames: list) -> list:
        """
        Run inference on multiple frames (e.g. 3 frames at slightly different
        wrist angles during NBV search), merge all detections with cross-frame NMS.

        Input:  list of BGR numpy arrays (all same shape)
        Output: merged list of detection dicts after NMS

        This reduces false negatives from partial occlusion — if a tool is
        visible in any of the 3 frames, it will be detected.
        """
        all_boxes, all_scores, all_class_ids, all_names = [], [], [], []

        for frame in frames:
            for d in self.infer(frame):
                all_boxes.append(list(d['bbox']))
                all_scores.append(d['confidence'])
                all_class_ids.append(d['class_id'])
                all_names.append(d['class_name'])

        if not all_boxes:
            return []

        indices = cv2.dnn.NMSBoxes(
            all_boxes, all_scores,
            score_threshold=self.conf_thresh,
            nms_threshold=0.45
        )
        if len(indices) == 0:
            return []

        merged = []
        for i in indices.flatten():
            name = all_names[i]
            merged.append({
                'class_id':       all_class_ids[i],
                'class_name':     name,
                'canonical_name': CANONICAL_NAME.get(name, name),
                'confidence':     all_scores[i],
                'bbox':           tuple(all_boxes[i])
            })
        return merged


if __name__ == '__main__':
    # Quick smoke test — run with: python3 yolo_infer.py
    import time
    model = YOLOv11ONNX('/home/acare/models/yolo_acare.onnx', conf_thresh=0.50)
    dummy = np.zeros((480, 640, 3), dtype=np.uint8)

    # Warmup
    model.infer(dummy)

    # Benchmark
    times = []
    for _ in range(10):
        t = time.monotonic()
        model.infer(dummy)
        times.append((time.monotonic() - t) * 1000)

    print(f'Inference latency: avg={sum(times)/len(times):.1f}ms  '
          f'min={min(times):.1f}ms  max={max(times):.1f}ms')
    print(f'Classes: {CLASS_NAMES}')
    print('yolo_infer.py OK')

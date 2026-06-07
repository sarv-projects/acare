"""
Runs YOLO26 on all .jpg images in the ACARE root folder and saves
annotated versions with bounding boxes, class labels, and confidence scores.

Output folder: ACARE/annotated/

Run from the ACARE root:
    & "C:/Users/Sonali/Desktop/ACARE/.venv/Scripts/python.exe" annotate_images.py
"""
import os
import sys
import glob

import cv2
import numpy as np
import onnxruntime as ort

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT        = r"C:\Users\Sonali\Desktop\ACARE"
MODEL_PATH  = os.path.join(ROOT, r"acare_software_final\models\acare_v26.onnx")
OUTPUT_DIR  = os.path.join(ROOT, "annotated")
IMAGE_GLOB  = os.path.join(ROOT, "*.jpg")

# ── Model config ───────────────────────────────────────────────────────────
CLASS_NAMES = ["cream", "medical scissors", "oxymeter", "plaster", "surgical forceps", "thermometer"]
CONF_THRESH = 0.40          # lower than production so we catch everything in photos
INPUT_SIZE  = 640           # YOLO26 trained at 640

# ── Colour palette (BGR) ───────────────────────────────────────────────────
COLOURS = [
    (0,   200, 255),   # cream         — amber
    (0,   255,   0),   # scissors      — green
    (255, 100,   0),   # oxymeter      — blue
    (0,   100, 255),   # plaster       — orange
    (200,   0, 255),   # forceps       — purple
    (0,   255, 200),   # thermometer   — cyan
]


def load_model(model_path: str):
    opts = ort.SessionOptions()
    opts.intra_op_num_threads = 4
    opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    session = ort.InferenceSession(model_path, sess_options=opts,
                                   providers=["CPUExecutionProvider"])
    input_name   = session.get_inputs()[0].name
    output_shape = session.get_outputs()[0].shape
    # YOLO26 NMS-free: output [1, 300, 6]
    nms_free = len(output_shape) == 3 and output_shape[2] == 6
    return session, input_name, nms_free


def preprocess(bgr: np.ndarray, size: int) -> tuple[np.ndarray, int, int, float]:
    """
    Letterbox pad to square — preserves aspect ratio so tall/wide images
    don't get distorted. Returns (input_tensor, pad_x, pad_y, scale).
    """
    h, w = bgr.shape[:2]
    scale = size / max(h, w)
    nh, nw = int(h * scale), int(w * scale)
    resized = cv2.resize(bgr, (nw, nh))
    canvas = np.full((size, size, 3), 114, dtype=np.uint8)
    py, px = (size - nh) // 2, (size - nw) // 2
    canvas[py:py + nh, px:px + nw] = resized

    rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    return np.expand_dims(np.transpose(rgb, (2, 0, 1)), axis=0), px, py, scale


def postprocess_nms_free(output: np.ndarray, orig_h: int, orig_w: int,
                          conf_thresh: float, input_size: int,
                          pad_x: int = 0, pad_y: int = 0, scale: float = 1.0) -> list[dict]:
    detections = output[0]
    valid = detections[detections[:, 4] >= conf_thresh]
    results = []
    for det in valid:
        x1, y1, x2, y2, conf, cls_id = det
        # Map from padded space back to original image coords
        x1 = (x1 - pad_x) / scale
        y1 = (y1 - pad_y) / scale
        x2 = (x2 - pad_x) / scale
        y2 = (y2 - pad_y) / scale
        x1, y1 = max(0, int(x1)), max(0, int(y1))
        x2, y2 = min(orig_w, int(x2)), min(orig_h, int(y2))
        cls_id = int(cls_id)
        name = CLASS_NAMES[cls_id] if cls_id < len(CLASS_NAMES) else f"class_{cls_id}"
        results.append({
            "class_id": cls_id, "class_name": name, "confidence": float(conf),
            "bbox": (x1, y1, x2, y2)
        })
    return results


def draw_detections(bgr: np.ndarray, detections: list[dict]) -> np.ndarray:
    img = bgr.copy()
    h, w = img.shape[:2]
    for d in detections:
        x1, y1, x2, y2 = d["bbox"]
        # Clamp to image bounds
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w - 1, x2), min(h - 1, y2)
        col  = COLOURS[d["class_id"] % len(COLOURS)]
        label = f"{d['class_name']}  {d['confidence']:.0%}"

        # Box
        cv2.rectangle(img, (x1, y1), (x2, y2), col, 3)

        # Label background
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.75, 2)
        by = max(y1 - 10, th + 5)
        cv2.rectangle(img, (x1, by - th - 8), (x1 + tw + 6, by + 4), col, -1)
        cv2.putText(img, label, (x1 + 3, by - 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2, cv2.LINE_AA)
    return img


def annotate_image(img_path: str, session, input_name: str, nms_free: bool) -> tuple[np.ndarray, list]:
    bgr   = cv2.imread(img_path)
    if bgr is None:
        print(f"  ⚠ Could not read: {img_path}")
        return None, []
    h, w  = bgr.shape[:2]
    inp, px, py, scale = preprocess(bgr, INPUT_SIZE)
    out   = session.run(None, {input_name: inp})[0]
    if nms_free:
        dets = postprocess_nms_free(out, h, w, CONF_THRESH, INPUT_SIZE, px, py, scale)
    else:
        print("  ⚠ Legacy YOLO11 output format — skipping (use acare_v26.onnx)")
        return bgr, []
    return draw_detections(bgr, dets), dets


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    images = sorted(glob.glob(IMAGE_GLOB))
    if not images:
        print("No .jpg images found in ACARE root.")
        return

    print(f"Loading model: {MODEL_PATH}")
    session, input_name, nms_free = load_model(MODEL_PATH)
    print(f"  NMS-free: {nms_free}  classes: {CLASS_NAMES}\n")

    for img_path in images:
        fname   = os.path.splitext(os.path.basename(img_path))[0]
        out_path = os.path.join(OUTPUT_DIR, f"{fname}_annotated.jpg")
        print(f"Processing: {os.path.basename(img_path)}")
        annotated, dets = annotate_image(img_path, session, input_name, nms_free)
        if annotated is None:
            continue
        if dets:
            for d in dets:
                print(f"  ✓ {d['class_name']:20s}  conf={d['confidence']:.0%}  bbox={d['bbox']}")
        else:
            print("  — nothing detected above threshold")
        cv2.imwrite(out_path, annotated, [cv2.IMWRITE_JPEG_QUALITY, 95])
        print(f"  → saved: {out_path}\n")

    print(f"Done. Annotated images in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

# ACARE — Implementation Guide & Spec Validation

> **Scope:** Perception pipeline (full) + Software pipeline (full) + Spec corrections.  
> Voice node (`voice_node.py`, VAD, ASR, keyword monitor) is excluded from this document.  
> Hardware is fixed. Raspberry Pi 5 (8 GB) is the compute platform.

---

## Table of Contents

1. [Spec Validation Summary](#1-spec-validation-summary)
2. [Perception Pipeline](#2-perception-pipeline)
   - [P0 — hp60c_camera_node.py (Camera Driver)](#p0--hp60c_camera_nodepy-camera-driver)
   - [P1 — vision_node.py (Orchestrator)](#p1--vision_nodepy-orchestrator)
   - [P2 — YOLOv11 ONNX INT8 Inference](#p2--yolov11-onnx-int8-inference)
   - [P3 — NBV Search (nbv_search.py)](#p3--nbv-search-nbv_searchpy)
   - [P4 — Fake Object Detection (fake_detector.py)](#p4--fake-object-detection-fake_detectorpy)
   - [P5 — 3D Localisation (localiser.py)](#p5--3d-localisation-localiserpy)
   - [P6 — Hand Tracking (hand_tracker.py)](#p6--hand-tracking-hand_trackerpy)
   - [P7 — Bayesian Probability Map](#p7--bayesian-probability-map)
3. [Software Pipeline](#3-software-pipeline)
   - [S1 — normaliser.py](#s1--normaliserpy)
   - [S2 — auth_node.py](#s2--auth_nodepy)
   - [S3 — dialogue_node.py (LangGraph)](#s3--dialogue_nodepy-langgraph)
   - [S4 — planner_node.py](#s4--planner_nodepy)
   - [S5 — ik_solver.py](#s5--ik_solverpy)
   - [S6 — handover.py](#s6--handoverpy)
   - [S7 — state_manager.py](#s7--state_managerpy)
   - [S8 — safety_node.py](#s8--safety_nodepy)
   - [S9 — embedded_interface_node (C++)](#s9--embedded_interface_node-c)
   - [S10 — log_node.py](#s10--log_nodepy)
   - [S11 — admin_cli.py](#s11--admin_clipy)
   - [S12 — supervisor.py](#s12--supervisorpy)
4. [Configuration Files](#4-configuration-files)
5. [ROS2 Package Structure & acare_msgs](#5-ros2-package-structure--acare_msgs)
6. [Full Dependencies](#6-full-dependencies)

---

## 1. Spec Validation Summary

The table below lists every issue found in the original spec, what is wrong, and what the correct implementation must be.

| # | Location in Spec | Issue | Correction |
|---|---|---|---|
| 1 | Section VIII, XV, XXI | TTS listed as **Google Cloud TTS WaveNet** for normal responses | **Wrong.** Use `edge-tts` (`pip install edge-tts`). Microsoft Edge TTS — free, no API key, no quota. Indian English voices: `en-IN-NeerjaNeural` (female) or `en-IN-PrabhatNeural` (male). Section VIII correctly says Edge TTS — Section XV contradicts it. Section XV is the error. |
| 2 | Section VII, XXIII | Speaker verification described as **"d-vector embeddings"** | **Wrong terminology.** d-vectors/x-vectors are the older TDNN architecture. Use SpeechBrain **ECAPA-TDNN**: `speechbrain/spkrec-ecapa-voxceleb`. EER ~0.8% vs 3.2% for x-vector. More robust to OT background noise. ~17 MB model. Same `cosine_similarity` interface. |
| 3 | Section XI, XXI | YOLOv11 described as **TFLite INT8** | **Suboptimal.** Benchmarks on Pi 5 show ONNX Runtime INT8 achieves ~77 ms/frame (13 FPS) for YOLOv11n at 640×640. TFLite INT8 is comparable in speed but ONNX tooling is cleaner, better debuggable, and the Ultralytics export pipeline produces cleaner ONNX. Use `onnxruntime` with ONNX INT8. Export: `model.export(format='onnx', int8=True, imgsz=320)`. Use 320×320 not 640×640 on Pi 5. |
| 4 | Section VII | Face verification described as **"MobileNet-based face embedding"** — vague | Use **InsightFace `buffalo_sc`** bundle: MobileNet RetinaFace detection + MobileFaceNet ArcFace. 512-D embeddings, ~24 ms on CPU, `pip install insightface`. For passive always-on face detection (not recognition), keep MediaPipe FaceDetection — it is lighter and sufficient for triggering the login flow. |
| 5 | Section XI | HP60C described as having a **ROS2 driver via ydlidar_ros2_driver** | `ydlidar_ros2_driver` is for LiDAR devices only. The HP60C is a depth camera and needs the **YDLIDAR HP60C SDK** with a custom ROS2 wrapper that publishes `sensor_msgs/Image` for RGB and depth. Write `hp60c_camera_node.py` using the SDK's Python bindings. |
| 6 | Section XV | **pyttsx3 listed for safety but also "reinitialise per call on Windows"** | The Windows reinitialisation bug is a dev-machine issue only. On Pi (Linux), pyttsx3 works without reinitialisation. Keep the Windows workaround in dev environment only — do not carry it into Pi deployment code. |
| 7 | Section XIX, admin_cli | Google TTS API key command in admin_cli | Remove `set-api-key --service google-tts`. Replace with nothing — `edge-tts` requires no key. Keep `--service deepgram` and `--service groq` only. |
| 8 | Section XXIII status | YOLO listed as **"TFLite INT8 export ready"** | Re-export as ONNX INT8 instead. Run export on training machine, copy `.onnx` to Pi. |
| 9 | Section II | Shoulder gearbox ratio listed as **20:1** in some spec versions | **Confirmed 22:1** (hardware team). The correct ratio is **22:1 shoulder, 15:1 elbow**. Use 22:1 in all DH parameter calculations and system.yaml comments. |

**Items that are correct and validated:**
- Silero VAD — correct, still best lightweight local VAD.
- Deepgram Nova-2 streaming WebSocket — correct, best accuracy for en-IN.
- Groq `llama3-8b-8192` JSON mode at temperature 0.0 — correct for intent parsing.
- MediaPipe Hands for handover — correct, best free option.
- MediaPipe FaceDetection for passive detection — correct.
- LangGraph for dialogue — correct.
- DLS/Levenberg-Marquardt IK — correct method.
- Bayesian probability map with clamping — correct.
- Fake detection dual-signal (Laplacian + depth variance) — correct.
- YDLIDAR T-mini Plus for safety LiDAR via `ydlidar_ros2_driver` — correct (this IS a LiDAR device).
- pyttsx3 for ESTOP/safety TTS — correct (zero latency, offline).
- Kokoro ONNX INT8 as offline TTS fallback — correct.
- SQLite for audit logging — correct.
- CAN/UART for Pi ↔ Teensy — correct.

---

## 2. Perception Pipeline

All perception code lives in `acare_vision/`. The five files are:
`vision_node.py`, `nbv_search.py`, `fake_detector.py`, `localiser.py`, `hand_tracker.py`.

---

### P0 — hp60c_camera_node.py (Camera Driver)

> ⚠️ **MISSING FROM ORIGINAL GUIDE.** This is the first thing needed for all vision work. Without it, `vision_node.py` has no camera to call.

The HP60C is a depth camera — **not** a LiDAR. `ydlidar_ros2_driver` does not support it. You need a custom ROS2 node that wraps the YDLIDAR HP60C SDK and publishes RGB + depth frames as ROS2 topics.

**What it publishes:**
- `/camera/rgb` (`sensor_msgs/Image`, BGR8) — RGB frame
- `/camera/depth` (`sensor_msgs/Image`, 16UC1, values in mm) — depth frame
- `/camera/camera_info` (`sensor_msgs/CameraInfo`) — intrinsics (after calibration)

```python
# acare_vision/hp60c_camera_node.py
# Spec Reference: Section XI (Camera Interface)
#
# Wraps the YDLIDAR HP60C SDK Python bindings and publishes
# RGB + depth frames as ROS2 sensor_msgs/Image topics.
#
# SDK install: follow YDLIDAR HP60C SDK README — copy .so/.dll to system path
# Python bindings: from the SDK's python/ directory
#
# NOTE: The HP60C SDK Python bindings are not on PyPI.
# You must build them from the SDK source on the Pi.

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import Header
import numpy as np
import threading
import time

# HP60C SDK import — adjust path after SDK installation on Pi
# The SDK provides a Python wrapper around the C++ library
try:
    import hp60c_sdk as sdk   # [FILL_AFTER_SDK_INSTALL — actual module name from SDK]
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False

class HP60CCameraNode(Node):
    """
    ROS2 wrapper for YDLIDAR HP60C RGBD camera.
    Publishes RGB and depth frames at the camera's native rate (~30 FPS).
    vision_node.py calls capture() directly via node reference — this node
    also publishes to topics for any other subscribers.
    """

    def __init__(self):
        super().__init__('hp60c_camera_node')

        # Publishers
        self.rgb_pub   = self.create_publisher(Image, '/camera/rgb',   10)
        self.depth_pub = self.create_publisher(Image, '/camera/depth', 10)
        self.info_pub  = self.create_publisher(CameraInfo, '/camera/camera_info', 10)

        # Latest frames — held in memory for direct capture() calls
        self._latest_rgb   = None
        self._latest_depth = None
        self._lock = threading.Lock()

        if not SDK_AVAILABLE:
            self.get_logger().error('HP60C SDK not found. Camera node running in stub mode.')
            self._stub_mode = True
        else:
            self._stub_mode = False
            self._init_camera()

        # Publish loop at ~30 FPS
        self.create_timer(1.0 / 30.0, self._publish_frame)
        self.get_logger().info('HP60C camera node started')

    def _init_camera(self):
        """Open the HP60C device via SDK."""
        # [FILL_AFTER_SDK_INSTALL — exact API depends on SDK version]
        # Typical pattern:
        #   self.camera = sdk.HP60C()
        #   self.camera.open(device_index=0)
        #   self.camera.set_resolution(640, 480)   # or 1280x720 — check SDK docs
        #   self.camera.start_stream()
        self.camera = None   # placeholder
        self.get_logger().warn('HP60C SDK init: [FILL_AFTER_SDK_INSTALL]')

    def _publish_frame(self):
        """Capture one frame pair and publish to ROS2 topics."""
        rgb, depth = self._capture_raw()
        if rgb is None or depth is None:
            return

        with self._lock:
            self._latest_rgb   = rgb
            self._latest_depth = depth

        stamp = self.get_clock().now().to_msg()
        header = Header()
        header.stamp = stamp
        header.frame_id = 'camera_link'

        # Publish RGB
        rgb_msg = Image()
        rgb_msg.header = header
        rgb_msg.height, rgb_msg.width = rgb.shape[:2]
        rgb_msg.encoding = 'bgr8'
        rgb_msg.step = rgb_msg.width * 3
        rgb_msg.data = rgb.tobytes()
        self.rgb_pub.publish(rgb_msg)

        # Publish depth (uint16, mm)
        depth_msg = Image()
        depth_msg.header = header
        depth_msg.height, depth_msg.width = depth.shape[:2]
        depth_msg.encoding = '16UC1'
        depth_msg.step = depth_msg.width * 2
        depth_msg.data = depth.astype(np.uint16).tobytes()
        self.depth_pub.publish(depth_msg)

    def _capture_raw(self) -> tuple:
        """
        Capture one RGB + depth frame pair from the HP60C.
        Returns (rgb_bgr_uint8, depth_uint16_mm) numpy arrays, or (None, None) on error.
        """
        if self._stub_mode or self.camera is None:
            # Stub: return blank frames for testing without hardware
            rgb   = np.zeros((480, 640, 3), dtype=np.uint8)
            depth = np.zeros((480, 640),    dtype=np.uint16)
            return rgb, depth

        try:
            # [FILL_AFTER_SDK_INSTALL — exact API from SDK docs]
            # Typical pattern:
            #   frame = self.camera.get_frame()
            #   rgb   = frame.rgb    # H×W×3 uint8 BGR
            #   depth = frame.depth  # H×W uint16 in mm
            #   return rgb, depth
            return None, None   # placeholder
        except Exception as e:
            self.get_logger().warn(f'Camera capture error: {e}')
            return None, None

    def capture(self) -> tuple:
        """
        Direct capture call used by vision_node.py (not via ROS2 topic).
        Returns (rgb_bgr_uint8, depth_uint16_mm) — latest cached frame pair.
        Thread-safe.
        """
        with self._lock:
            if self._latest_rgb is None:
                return self._capture_raw()   # first call — capture fresh
            return self._latest_rgb.copy(), self._latest_depth.copy()

    def destroy_node(self):
        if not self._stub_mode and self.camera is not None:
            # [FILL_AFTER_SDK_INSTALL — close camera stream]
            # self.camera.stop_stream()
            # self.camera.close()
            pass
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = HP60CCameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

**SDK installation on Pi (once SSH works):**
```bash
# 1. Download HP60C SDK from YDLIDAR website or ask hardware team for the package
# 2. Build Python bindings:
cd hp60c_sdk/python
pip install .
# 3. Verify:
python -c "import hp60c_sdk; print('SDK OK')"
```

**Integration with vision_node.py:**
`vision_node.py` holds a reference to the `HP60CCameraNode` instance and calls `camera.capture()` directly — no topic subscription needed for the vision pipeline. The topic publications are for debugging and any future nodes that need camera data.

---

### P1 — vision_node.py (Orchestrator)

This is the ROS2 node that owns all perception. It does NOT do inference directly — it delegates to the sub-modules and manages which mode is active.

**Subscribes to:**
- `/vision_search_request` (VisionSearchRequest) — from planner_node
- `/robot_state` (RobotState) — to know when to switch to HANDOVER mode

**Publishes to:**
- `/vision_status` (String: `LOADING` | `READY`) — startup status
- `/vision_result` (VisionResult) — tool found or not found
- `/hand_status` (HandStatus) — during HANDOVER state only
- `/log_event` (LogEvent) — search events

**Startup sequence:**

```python
# vision_node.py
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from acare_msgs.msg import VisionSearchRequest, VisionResult, HandStatus, RobotState, LogEvent
from std_msgs.msg import String
from .yolo_infer import YOLOv11ONNX
from .nbv_search import NBVSearch
from .hand_tracker import HandTracker
import threading

class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')
        self.mode = 'IDLE'  # 'IDLE', 'SEARCH', 'HANDOVER'
        self.yolo_ready = False
        self.lock = threading.Lock()

        # Publishers
        self.status_pub = self.create_publisher(String, '/vision_status', 10)
        self.result_pub = self.create_publisher(VisionResult, '/vision_result', 10)
        self.hand_pub = self.create_publisher(HandStatus, '/hand_status', 10)
        self.log_pub = self.create_publisher(LogEvent, '/log_event', 10)

        # Subscribers
        self.create_subscription(VisionSearchRequest, '/vision_search_request',
                                 self.on_search_request, 10)
        self.create_subscription(RobotState, '/robot_state',
                                 self.on_robot_state, 10)

        # Publish LOADING immediately
        self.status_pub.publish(String(data='LOADING'))
        self.get_logger().info('Vision node: loading YOLO model...')

        # Load model in a background thread so ROS2 stays alive
        threading.Thread(target=self._load_models, daemon=True).start()

    def _load_models(self):
        self.yolo = YOLOv11ONNX('/models/yolo_int8.onnx', conf_thresh=0.70)
        self.nbv = NBVSearch(self.yolo)
        self.hand_tracker = HandTracker()
        self.yolo_ready = True
        self.status_pub.publish(String(data='READY'))
        self.get_logger().info('Vision node: READY')

    def on_robot_state(self, msg: RobotState):
        with self.lock:
            if msg.state == 'HANDOVER':
                self.mode = 'HANDOVER'
                self.hand_tracker.start()
            elif self.mode == 'HANDOVER':
                self.mode = 'IDLE'
                self.hand_tracker.stop()

    def on_search_request(self, msg: VisionSearchRequest):
        if not self.yolo_ready:
            # Planner should have checked /vision_status — but guard here too
            self.get_logger().warn('Search request arrived before YOLO ready')
            return
        with self.lock:
            self.mode = 'SEARCH'
        # Run in executor thread — this blocks while arm moves + captures
        result = self.nbv.search(
            tool_name=msg.tool,
            publish_hand_cb=None  # hand_tracker not active during search
        )
        self.result_pub.publish(result)
        with self.lock:
            self.mode = 'IDLE'

    # HandTracker runs its own thread, publishing /hand_status directly
```

**Critical rule:** YOLOv11 inference and MediaPipe Hands NEVER run simultaneously. `self.mode` enforces this — when `SEARCH`, `HandTracker` is stopped. When `HANDOVER`, YOLO is not called.

---

### P2 — YOLOv11 ONNX INT8 Inference

> ⚠️ **SPEC CORRECTION:** The spec says TFLite INT8. Use **ONNX INT8** with `onnxruntime` instead. Better tooling, easier debugging, identical accuracy. Benchmarked at ~77 ms/frame on Pi 5 at 640×640 with INT8; use 320×320 for ~40 ms.

**Step 1 — Export (run on your training machine, not Pi):**

```python
# run on laptop/desktop where you trained
from ultralytics import YOLO

model = YOLO('runs/detect/train/weights/best.pt')  # your trained model
model.export(
    format='onnx',
    int8=True,          # INT8 post-training quantisation
    imgsz=320,          # 320×320 for Pi 5 speed — sufficient for table-top
    simplify=True,      # remove unused ONNX ops
    opset=12,           # max compatibility with onnxruntime on Pi
    dynamic=False,      # fixed input shape for edge deployment
)
# Output: best.onnx  — copy this to Pi at /models/yolo_int8.onnx
```

**Step 2 — Inference class (`yolo_infer.py`):**

```python
# acare_vision/yolo_infer.py
import onnxruntime as ort
import numpy as np
import cv2

CLASS_NAMES = [
    'scalpel', 'scissors', 'forceps', 'bandage',
    'gauze', 'thermometer', 'oximeter', 'plaster'
]

class YOLOv11ONNX:
    """
    Wraps an ONNX INT8 YOLOv11 model for inference on Pi 5 CPU.
    """
    def __init__(self, model_path: str, conf_thresh: float = 0.70):
        opts = ort.SessionOptions()
        opts.intra_op_num_threads = 4   # use all Pi 5 cores
        opts.inter_op_num_threads = 1
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.session = ort.InferenceSession(
            model_path,
            sess_options=opts,
            providers=['CPUExecutionProvider']
        )
        self.input_name = self.session.get_inputs()[0].name
        # Shape: [1, 3, H, W]
        _, _, self.H, self.W = self.session.get_inputs()[0].shape
        self.conf_thresh = conf_thresh

    def preprocess(self, bgr_frame: np.ndarray) -> np.ndarray:
        img = cv2.resize(bgr_frame, (self.W, self.H))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0          # normalise [0,1]
        img = np.transpose(img, (2, 0, 1))             # HWC → CHW
        img = np.expand_dims(img, axis=0)              # add batch dim
        return img

    def postprocess(self, output: np.ndarray, orig_h: int, orig_w: int):
        """
        YOLOv11 ONNX output shape: [1, 4+num_classes, num_anchors]
        For 320×320 input: [1, 12, 2100] (8 classes + 4 box coords)
        """
        preds = output[0]                              # [4+C, N]
        preds = preds.T                                # [N, 4+C]

        boxes_xywh = preds[:, :4]                     # cx, cy, w, h (normalised)
        scores = preds[:, 4:]                          # [N, num_classes]

        class_ids = np.argmax(scores, axis=1)
        confidences = scores[np.arange(len(scores)), class_ids]

        # Filter by confidence
        mask = confidences >= self.conf_thresh
        boxes_xywh = boxes_xywh[mask]
        class_ids = class_ids[mask]
        confidences = confidences[mask]

        if len(boxes_xywh) == 0:
            return []

        # Convert cx,cy,w,h (normalised) → x1,y1,x2,y2 (pixel)
        scale_x, scale_y = orig_w / self.W, orig_h / self.H
        cx = boxes_xywh[:, 0] * self.W * scale_x
        cy = boxes_xywh[:, 1] * self.H * scale_y
        bw = boxes_xywh[:, 2] * self.W * scale_x
        bh = boxes_xywh[:, 3] * self.H * scale_y
        x1 = (cx - bw / 2).astype(int)
        y1 = (cy - bh / 2).astype(int)
        x2 = (cx + bw / 2).astype(int)
        y2 = (cy + bh / 2).astype(int)

        # NMS
        boxes_xyxy = np.stack([x1, y1, x2, y2], axis=1).tolist()
        indices = cv2.dnn.NMSBoxes(
            boxes_xyxy, confidences.tolist(),
            score_threshold=self.conf_thresh,
            nms_threshold=0.45
        )
        if len(indices) == 0:
            return []

        results = []
        for i in indices.flatten():
            results.append({
                'class_id': int(class_ids[i]),
                'class_name': CLASS_NAMES[int(class_ids[i])],
                'confidence': float(confidences[i]),
                'bbox': (int(x1[i]), int(y1[i]), int(x2[i]), int(y2[i]))
            })
        return results

    def infer(self, bgr_frame: np.ndarray) -> list:
        h, w = bgr_frame.shape[:2]
        inp = self.preprocess(bgr_frame)
        outputs = self.session.run(None, {self.input_name: inp})
        return self.postprocess(outputs[0], h, w)

    def infer_multi_frame(self, frames: list) -> list:
        """
        Infer on 3 frames (wrist offsets), merge with NMS, return merged detections.
        frames: list of BGR numpy arrays (all same shape)
        """
        all_boxes, all_scores, all_class_ids = [], [], []
        for frame in frames:
            h, w = frame.shape[:2]
            dets = self.infer(frame)
            for d in dets:
                x1, y1, x2, y2 = d['bbox']
                all_boxes.append([x1, y1, x2, y2])
                all_scores.append(d['confidence'])
                all_class_ids.append(d['class_id'])

        if not all_boxes:
            return []

        # Cross-frame NMS
        indices = cv2.dnn.NMSBoxes(
            all_boxes, all_scores,
            score_threshold=self.conf_thresh,
            nms_threshold=0.45
        )
        merged = []
        for i in indices.flatten():
            merged.append({
                'class_id': all_class_ids[i],
                'class_name': CLASS_NAMES[all_class_ids[i]],
                'confidence': all_scores[i],
                'bbox': tuple(all_boxes[i])
            })
        return merged
```

**Performance on Pi 5:**
- 320×320 INT8: ~40–50 ms/frame → sufficient (NBV moves arm ~1 s between frames anyway)
- 640×640 INT8: ~77–150 ms/frame → acceptable but slower
- Use 320×320 as default. If 320×320 accuracy is insufficient for small tools like oximeter, bump to 416×416.

**Temporal consistency check** (inside nbv_search.py, not here):  
If the same class is detected at approximately the same (x, y) pixel location across 2+ consecutive viewpoints, accept it even at confidence ≥ 0.65. This handles partially occluded tools.

---

### P3 — NBV Search (nbv_search.py)

The NBV (Next-Best-View) search is the algorithm that decides which arm pose to move to next when searching for a tool, prioritised by learned probability.

**Data structures:**

```python
# probability_map: dict[zone_name → dict[tool_class → float]]
# All values clamped to [0.05, 0.90]. Sum per zone normalised to 1.0.
probability_map = {
    'zone_A': {'scalpel': 0.4, 'scissors': 0.2, 'forceps': 0.15, ...},
    'zone_B': {'scissors': 0.5, 'forceps': 0.3, ...},
    ...
}

# viewpoints: list of dicts — arm poses corresponding to each zone
# joint_angles filled after hardware assembly and calibration
viewpoints = [
    {'zone': 'zone_A', 'joint_angles': [0.0, 0.5, -0.8, 0.0, 0.3, 0.0]},  # [FILL_AFTER_ASSEMBLY]
    {'zone': 'zone_B', 'joint_angles': [0.4, 0.5, -0.8, 0.0, 0.3, 0.0]},  # [FILL_AFTER_ASSEMBLY]
    {'zone': 'zone_C', 'joint_angles': [-0.4, 0.5, -0.8, 0.0, 0.3, 0.0]}, # [FILL_AFTER_ASSEMBLY]
]
```

**Full NBV search implementation:**

```python
# acare_vision/nbv_search.py
import yaml, time, numpy as np
from pathlib import Path
from .fake_detector import FakeDetector
from .localiser import Localiser
from acare_msgs.msg import VisionResult, ArmCommand, MotionFeedback
import rclpy

PROB_MAP_PATH = Path('/acare_ws/src/acare_bringup/config/probability_map.yaml')
WORKSPACE = {'xmin': -0.4, 'xmax': 0.4, 'ymin': -0.3, 'ymax': 0.3, 'zmin': 0.0, 'zmax': 0.5}

class NBVSearch:
    def __init__(self, yolo_model, node):
        self.yolo = yolo_model
        self.node = node   # parent vision_node for publishing arm commands
        self.fake_detector = FakeDetector()
        self.localiser = Localiser()
        self.probability_map = self._load_map()
        self.viewpoints = self._load_viewpoints()
        # Track last viewpoint's detections for temporal consistency
        self.prev_detections = {}  # class_name → approx pixel centre

    def _load_map(self) -> dict:
        ALL_TOOLS = ['scalpel','scissors','forceps','bandage','gauze','thermometer','oximeter','plaster']
        zones = ['zone_A', 'zone_B', 'zone_C']
        if PROB_MAP_PATH.exists():
            with open(PROB_MAP_PATH) as f:
                loaded = yaml.safe_load(f) or {}
            # Fill in any tools missing from a partial admin-written yaml
            # so normalisation always covers all 8 tools per zone
            for zone in zones:
                if zone not in loaded:
                    loaded[zone] = {}
                for tool in ALL_TOOLS:
                    if tool not in loaded[zone]:
                        loaded[zone][tool] = 0.05   # minimum prior for unlisted tools
            return loaded
        # Cold start: uniform distribution
        return {z: {t: 1.0/len(ALL_TOOLS) for t in ALL_TOOLS} for z in zones}

    def _load_viewpoints(self) -> list:
        # Loaded from system.yaml after calibration. Hardcoded here as placeholder.
        # [FILL_AFTER_ASSEMBLY via python admin.py calibrate]
        return []

    def _sort_zones(self, tool_name: str) -> list:
        """Sort zones by P(tool|zone), highest first."""
        scored = []
        for vp in self.viewpoints:
            zone = vp['zone']
            prob = self.probability_map.get(zone, {}).get(tool_name, 0.05)
            scored.append((prob, vp))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [vp for _, vp in scored]

    def _move_arm_to(self, joint_angles: list) -> bool:
        """Send MOVE command and wait for MotionFeedback.success."""
        cmd = ArmCommand()
        cmd.command = 'MOVE'
        cmd.joint_angles = joint_angles
        cmd.velocity_scale = 0.8
        cmd.blocking = True
        self.node.arm_cmd_pub.publish(cmd)
        # Wait for feedback (blocking via threading.Event set by motion_feedback callback)
        success = self.node.wait_for_motion_feedback(timeout=10.0)
        return success

    def _capture_frames(self, camera) -> tuple:
        """
        Capture 3 RGB+depth frame pairs at small wrist offsets (~2-3 cm).
        Returns list of (rgb_frame, depth_frame).
        CRITICAL: arm must be fully stationary before capture.
        """
        frames = []
        wrist_offsets = [0.0, 0.02, -0.02]   # ±2 cm wrist pitch offset in radians (approx)
        for offset in wrist_offsets:
            # Apply tiny wrist offset via incremental joint 4 adjustment
            # (exact mapping depends on arm kinematics — [FILL_AFTER_ASSEMBLY])
            rgb, depth = camera.capture()      # HP60C SDK call
            frames.append((rgb, depth))
            time.sleep(0.05)                   # 50 ms settle between micro-captures
        return frames

    def _check_temporal_consistency(self, dets: list) -> list:
        """Promote detections to 0.65 threshold if seen at same location in prev viewpoint."""
        promoted = []
        for d in dets:
            cx = (d['bbox'][0] + d['bbox'][2]) // 2
            cy = (d['bbox'][1] + d['bbox'][3]) // 2
            prev = self.prev_detections.get(d['class_name'])
            if prev is not None:
                dist = ((cx - prev[0])**2 + (cy - prev[1])**2) ** 0.5
                if dist < 50 and d['confidence'] >= 0.65:   # within 50px → same object
                    promoted.append(d)
                    continue
            if d['confidence'] >= 0.70:
                promoted.append(d)
        return promoted

    def _update_map(self, zone: str, tool_name: str, found: bool, all_dets: list):
        """Bayesian update with clamping."""
        if zone not in self.probability_map:
            self.probability_map[zone] = {}

        # Primary update for requested tool
        current = self.probability_map[zone].get(tool_name, 0.125)
        self.probability_map[zone][tool_name] = current * (1.5 if found else 0.7)

        # Passive update for all detected tools at this viewpoint
        for det in all_dets:
            t = det['class_name']
            if t != tool_name:
                v = self.probability_map[zone].get(t, 0.125)
                self.probability_map[zone][t] = v * 1.3

        # Normalise
        total = sum(self.probability_map[zone].values())
        if total > 0:
            for t in self.probability_map[zone]:
                self.probability_map[zone][t] /= total

        # Clamp to [0.05, 0.90]
        for t in self.probability_map[zone]:
            self.probability_map[zone][t] = min(max(self.probability_map[zone][t], 0.05), 0.90)

    def save_map(self):
        """Atomic write. Called on clean shutdown."""
        tmp = Path(str(PROB_MAP_PATH) + '.tmp')
        with open(tmp, 'w') as f:
            yaml.dump(self.probability_map, f)
        tmp.rename(PROB_MAP_PATH)   # atomic rename

    def search(self, tool_name: str, camera) -> VisionResult:
        sorted_viewpoints = self._sort_zones(tool_name)
        result = VisionResult()
        result.found = False
        result.tool = tool_name

        for vp in sorted_viewpoints:
            zone = vp['zone']

            # Move arm to viewpoint — wait until stationary
            ok = self._move_arm_to(vp['joint_angles'])
            if not ok:
                continue   # arm error — skip viewpoint

            # Capture 3 frames
            frame_pairs = self._capture_frames(camera)

            # Run YOLO on all 3 frames, merge
            rgb_frames = [p[0] for p in frame_pairs]
            depth_frames = [p[1] for p in frame_pairs]
            all_dets = self.yolo.infer_multi_frame(rgb_frames)

            # Temporal consistency check
            all_dets = self._check_temporal_consistency(all_dets)

            # Update prev detections for next viewpoint
            self.prev_detections = {}
            for d in all_dets:
                cx = (d['bbox'][0] + d['bbox'][2]) // 2
                cy = (d['bbox'][1] + d['bbox'][3]) // 2
                self.prev_detections[d['class_name']] = (cx, cy)

            # Filter to requested tool only
            tool_dets = [d for d in all_dets if d['class_name'] == tool_name]

            # Fake check + workspace filter
            valid = []
            ref_depth = depth_frames[1]  # middle frame depth
            ref_rgb = rgb_frames[1]
            for d in tool_dets:
                from .fake_detector import FakeDetector
                if FakeDetector().is_fake(ref_rgb, ref_depth, d['bbox']):
                    self.node.get_logger().warn(f'Fake object rejected: {d["class_name"]}')
                    continue
                pos = self.localiser.pixel_to_robot(d['bbox'], ref_depth)
                if pos is None:
                    continue  # depth unavailable
                if not self._in_workspace(pos):
                    continue
                d['position_3d'] = pos
                valid.append(d)

            # Bayesian map update
            self._update_map(zone, tool_name, found=len(valid) > 0, all_dets=all_dets)

            if valid:
                # Pick best: highest confidence, tiebreak = closest to neutral arm position
                valid.sort(key=lambda d: d['confidence'], reverse=True)
                best = valid[0]
                result.found = True
                result.x, result.y, result.z = best['position_3d']
                result.confidence = best['confidence']
                result.zone = zone
                return result

        return result   # found=False

    def _in_workspace(self, pos: tuple) -> bool:
        x, y, z = pos
        w = WORKSPACE
        return w['xmin'] <= x <= w['xmax'] and w['ymin'] <= y <= w['ymax'] and w['zmin'] <= z <= w['zmax']
```

---

### P4 — Fake Object Detection (fake_detector.py)

Dual-signal approach: Laplacian texture variance + depth variance. **Both** must be below threshold to reject as fake. This prevents false rejection of shiny real surgical tools (which have low texture but high depth variance).

```python
# acare_vision/fake_detector.py
import cv2
import numpy as np
import yaml
from pathlib import Path

THRESHOLDS_PATH = Path('/acare_ws/src/acare_bringup/config/thresholds.yaml')

class FakeDetector:
    def __init__(self):
        with open(THRESHOLDS_PATH) as f:
            cfg = yaml.safe_load(f)
        fd = cfg.get('fake_detection', {})
        self.texture_thresh = fd.get('texture_variance_threshold', 120.0)
        self.depth_thresh   = fd.get('depth_variance_threshold', 0.002)

    def is_fake(self, rgb_frame: np.ndarray, depth_frame: np.ndarray, bbox: tuple) -> bool:
        """
        Returns True if object is likely a fake/printed replica.
        rgb_frame : H×W×3 uint8
        depth_frame: H×W float32 or uint16 (metres or mm — see note)
        bbox       : (x1, y1, x2, y2) pixel coords
        """
        x1, y1, x2, y2 = bbox
        # Guard against empty ROI
        if x2 <= x1 or y2 <= y1:
            return False

        # --- Signal 1: Texture variance via Laplacian ---
        roi_gray = cv2.cvtColor(rgb_frame[y1:y2, x1:x2], cv2.COLOR_RGB2GRAY)
        texture_var = cv2.Laplacian(roi_gray, cv2.CV_64F).var()

        # --- Signal 2: Depth variance ---
        depth_roi = depth_frame[y1:y2, x1:x2].astype(np.float32)
        # HP60C depth is in mm — convert to metres for consistent threshold
        depth_roi_m = depth_roi / 1000.0
        valid_depth = depth_roi_m[depth_roi_m > 0]

        if len(valid_depth) < 10:
            # Depth unavailable — fall back to texture only, mark as uncertain
            # Do NOT reject on texture alone (too many false positives on shiny tools)
            return False   # give benefit of the doubt; log DEPTH_UNAVAILABLE separately

        depth_var = np.var(valid_depth)

        # Both signals below threshold → fake
        is_fake = (texture_var < self.texture_thresh) and (depth_var < self.depth_thresh)
        return is_fake
```

**Calibration procedure** (run `python admin.py calibrate`, Step 6):
1. Place 20 real surgical tools one at a time → record texture_var and depth_var for each.
2. Place 20 3D-printed replicas → record same.
3. Find threshold that separates the two distributions cleanly.
4. Write to `thresholds.yaml`. The defaults (120.0, 0.002) are starting estimates — **must be calibrated on real hardware**.

---

### P5 — 3D Localisation (localiser.py)

Converts a bounding box centre pixel + depth value into (x, y, z) in robot base frame. No Open3D. No point cloud. Direct depth pixel read.

```python
# acare_vision/localiser.py
import numpy as np
import yaml
from pathlib import Path

SYSTEM_YAML = Path('/acare_ws/src/acare_bringup/config/system.yaml')

class Localiser:
    def __init__(self):
        with open(SYSTEM_YAML) as f:
            cfg = yaml.safe_load(f)
        cam = cfg['camera']
        # Intrinsics — set during calibration
        self.fx = cam['fx']           # focal length x (pixels)   [FILL_AFTER_ASSEMBLY]
        self.fy = cam['fy']           # focal length y (pixels)   [FILL_AFTER_ASSEMBLY]
        self.cx = cam['cx']           # principal point x         [FILL_AFTER_ASSEMBLY]
        self.cy = cam['cy']           # principal point y         [FILL_AFTER_ASSEMBLY]
        # Extrinsics: 4×4 transform from camera frame to robot base frame
        # Stored as flat list [r00,r01,...r33] in system.yaml
        T_flat = cam['T_robot_camera']    # [FILL_AFTER_ASSEMBLY]
        self.T = np.array(T_flat).reshape(4, 4)

    def pixel_to_robot(self, bbox: tuple, depth_frame: np.ndarray) -> tuple | None:
        """
        bbox       : (x1, y1, x2, y2)
        depth_frame: H×W uint16 or float32, values in mm (HP60C native)
        Returns (x, y, z) in robot base frame in metres, or None if depth invalid.
        """
        x1, y1, x2, y2 = bbox
        u = (x1 + x2) // 2   # bbox centre pixel x
        v = (y1 + y2) // 2   # bbox centre pixel y

        # Clamp to frame bounds
        h, w = depth_frame.shape[:2]
        u = min(max(u, 0), w - 1)
        v = min(max(v, 0), h - 1)

        depth_mm = float(depth_frame[v, u])
        if depth_mm <= 0 or depth_mm > 4000:   # HP60C range: 0.2–4.0 m = 200–4000 mm
            return None

        depth_m = depth_mm / 1000.0

        # Pixel (u, v) + depth → 3D in camera frame
        X_cam = (u - self.cx) * depth_m / self.fx
        Y_cam = (v - self.cy) * depth_m / self.fy
        Z_cam = depth_m

        # Transform to robot base frame
        P_cam = np.array([X_cam, Y_cam, Z_cam, 1.0])
        P_robot = self.T @ P_cam

        return (float(P_robot[0]), float(P_robot[1]), float(P_robot[2]))

    def compute_pregrasp(self, grasp_point: tuple, approach_dist_m: float = 0.05) -> tuple:
        """Return a point 5 cm above the grasp point (in robot Z)."""
        x, y, z = grasp_point
        return (x, y, z + approach_dist_m)
```

**Camera intrinsics calibration:** Use OpenCV `calibrateCamera()` with a checkerboard pattern (9×6 squares) before deployment. Run via `admin.py calibrate` Step 2. Store `fx, fy, cx, cy` in `system.yaml`.

**Extrinsics calibration:** Mount calibration target at known robot-frame coordinates, capture from camera, compute T_robot_camera using `cv2.solvePnP`. Store as flat 16-element list in `system.yaml`.

---

### P6 — Hand Tracking (hand_tracker.py)

Runs **only during HANDOVER state**. Detects open palm, computes 3D palm position for dynamic arm approach. MediaPipe Hands.

```python
# acare_vision/hand_tracker.py
import mediapipe as mp
import numpy as np
import threading
import time
from acare_msgs.msg import HandStatus

mp_hands = mp.solutions.hands

# Landmark indices
WRIST         = 0
INDEX_MCP     = 5;  INDEX_TIP  = 8
MIDDLE_MCP    = 9;  MIDDLE_TIP = 12
RING_MCP      = 13; RING_TIP   = 16
PINKY_MCP     = 17; PINKY_TIP  = 20
THUMB_TIP     = 4;  THUMB_IP   = 3

class HandTracker:
    def __init__(self, localiser, camera, hand_pub, log_pub):
        self.localiser = localiser
        self.camera    = camera
        self.hand_pub  = hand_pub
        self.log_pub   = log_pub
        self.running   = False
        self._thread   = None
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.70,
            min_tracking_confidence=0.60
        )

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=2.0)

    def _loop(self):
        while self.running:
            rgb, depth = self.camera.capture()
            msg = self._process(rgb, depth)
            self.hand_pub.publish(msg)
            time.sleep(0.05)   # ~20 FPS

    def _process(self, rgb_frame: np.ndarray, depth_frame: np.ndarray) -> HandStatus:
        msg = HandStatus()
        msg.hand_detected = False
        msg.is_open       = False
        msg.palm_up       = False
        msg.confidence    = 0.0

        results = self.hands.process(rgb_frame)
        if not results.multi_hand_landmarks:
            return msg

        h, w = rgb_frame.shape[:2]
        lm = results.multi_hand_landmarks[0].landmark

        msg.hand_detected = True
        msg.confidence = 0.8   # MediaPipe doesn't expose per-frame confidence directly

        # --- is_open: 3+ fingers extended ---
        fingers_extended = 0
        for tip_idx, pip_idx in [
            (INDEX_TIP, 6), (MIDDLE_TIP, 10), (RING_TIP, 14), (PINKY_TIP, 18)
        ]:
            # Tip y < PIP y means finger is extended (y increases downward in image)
            if lm[tip_idx].y < lm[pip_idx].y:
                fingers_extended += 1
        # Thumb: compare tip x vs IP x (lateral direction)
        if abs(lm[THUMB_TIP].x - lm[THUMB_IP].x) > 0.04:
            fingers_extended += 1
        msg.is_open = fingers_extended >= 3

        # --- palm_up: mean fingertip y < wrist y ---
        fingertip_y_mean = np.mean([lm[INDEX_TIP].y, lm[MIDDLE_TIP].y,
                                     lm[RING_TIP].y,  lm[PINKY_TIP].y])
        msg.palm_up = fingertip_y_mean < lm[WRIST].y

        # --- 3D palm centre ---
        palm_lm_indices = [WRIST, INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP]
        px = int(np.mean([lm[i].x for i in palm_lm_indices]) * w)
        py = int(np.mean([lm[i].y for i in palm_lm_indices]) * h)
        pos = self.localiser.pixel_to_robot((px-5, py-5, px+5, py+5), depth_frame)
        if pos:
            msg.x, msg.y, msg.z = pos

        return msg
```

---

### P7 — Bayesian Probability Map

This is not a separate file — it lives inside `nbv_search.py` (the `_update_map` and `save_map` methods above). Key rules:

**Update multipliers:**
- Tool found in zone: `× 1.5`
- Tool NOT found in zone: `× 0.7`
- Passive update (other tools seen): `× 1.3`

**Normalisation:** After every update, sum all tool probabilities in the zone and divide each by the sum.

**Clamping:** `P = min(max(P, 0.05), 0.90)` — after normalise. Prevents any zone/tool from reaching 0 (always searched) or 1 (monopolises all searches).

**Persistence:**
- Clean shutdown → atomic write to `probability_map.yaml` (`.tmp` → rename).
- Boot with `.tmp` present → incomplete write → delete `.tmp`, load `.yaml`.
- Boot with neither file → uniform distribution (cold start).

**Admin prior:** Before a demo, admin runs `python admin.py calibrate` Step 5 to define viewpoints and sets `probability_map.yaml` manually to reflect expected tool placement. This makes the first demo run fast.

---

## 3. Software Pipeline

---

### S1 — normaliser.py

Called in the voice pipeline after Deepgram STT, before Groq intent parsing. Cleans and normalises raw transcripts.

```python
# acare_voice/normaliser.py
import re

FILLER_WORDS = {
    'um', 'uh', 'er', 'ah', 'hmm', 'please', 'kindly',
    'can you', 'could you', 'would you', 'can you please',
    'could you please', 'would you please'
}

# Simple unambiguous aliases ONLY — contextual ones go to Groq
SIMPLE_ALIASES = {
    'bandage cloth': 'bandage',
    'gauze pad':     'gauze',
    'gauze swab':    'gauze',
    'pulse ox':      'oximeter',
    'spo2':          'oximeter',
    'temp probe':    'thermometer',
    'band aid':      'plaster',
    'band-aid':      'plaster',
    'adhesive strip':'plaster',
}

TOOL_NAMES = {
    'scalpel','scissors','forceps','bandage',
    'gauze','thermometer','oximeter','plaster'
}

def normalise(raw: str) -> dict:
    """
    Returns:
        {
            'text': str,           # cleaned text
            'multi_tool': bool,    # True if 2+ tools detected
            'tools_found': list    # list of tool names if multi_tool
        }
    """
    text = raw.lower().strip()

    # Step 1: Strip punctuation (keep spaces)
    text = re.sub(r"[^\w\s']", '', text)

    # Step 2: Strip filler words/phrases (longest first to avoid partial matches)
    for filler in sorted(FILLER_WORDS, key=len, reverse=True):
        text = text.replace(filler, ' ')
    text = ' '.join(text.split())   # collapse multiple spaces

    # Step 3: Simple alias expansion
    for alias, canonical in SIMPLE_ALIASES.items():
        text = text.replace(alias, canonical)

    # Step 4: Multi-tool detection
    found_tools = [t for t in TOOL_NAMES if re.search(r'\b' + t + r'\b', text)]
    multi_tool = len(found_tools) >= 2

    return {
        'text': text,
        'multi_tool': multi_tool,
        'tools_found': found_tools
    }
```

---

### S2 — auth_node.py

> ⚠️ **SPEC CORRECTION:** Spec says "d-vector embeddings". Use **SpeechBrain ECAPA-TDNN** (`speechbrain/spkrec-ecapa-voxceleb`). This is the current recommended model. EER ~0.8% vs x-vector's 3.2%. Significantly more robust to noisy OT environments.

> ⚠️ **SPEC CORRECTION:** Spec says "MobileNet-based face embedding" — vague. Use **InsightFace `buffalo_sc`**: combines MobileNet RetinaFace detection + MobileFaceNet ArcFace recognition. ~24 ms CPU. 512-D embeddings.

**Models used:**
1. **Speaker verification:** `speechbrain/spkrec-ecapa-voxceleb` (ECAPA-TDNN, ~17 MB)
2. **Face verification:** InsightFace `buffalo_sc` (~40 MB bundle)
3. **Passive face detection (always-on):** MediaPipe FaceDetection (lightweight, ~3 MB)

```python
# acare_auth/verify_voice.py
from speechbrain.inference.speaker import EncoderClassifier
import torch, numpy as np

class VoiceVerifier:
    """ECAPA-TDNN speaker verification."""
    THRESHOLD = 0.85   # cosine similarity — from system.yaml

    def __init__(self):
        self.classifier = EncoderClassifier.from_hparams(
            source='speechbrain/spkrec-ecapa-voxceleb',
            savedir='/models/ecapa_tdnn',
            run_opts={'device': 'cpu'}
        )

    def embed(self, audio_tensor: torch.Tensor) -> np.ndarray:
        """audio_tensor: 1D torch float32 at 16 kHz"""
        with torch.no_grad():
            emb = self.classifier.encode_batch(audio_tensor.unsqueeze(0))
        return emb.squeeze().numpy()  # shape: (192,)

    def verify(self, audio_tensor: torch.Tensor, stored_embedding: np.ndarray) -> tuple:
        emb = self.embed(audio_tensor)
        # Cosine similarity
        sim = float(np.dot(emb, stored_embedding) /
                    (np.linalg.norm(emb) * np.linalg.norm(stored_embedding) + 1e-8))
        return sim >= self.THRESHOLD, sim
```

```python
# acare_auth/verify_face.py
import insightface
import numpy as np

class FaceVerifier:
    """InsightFace buffalo_sc: RetinaFace detection + MobileFaceNet ArcFace."""
    THRESHOLD = 0.78    # cosine similarity — from system.yaml

    def __init__(self):
        self.app = insightface.app.FaceAnalysis(
            name='buffalo_sc',
            providers=['CPUExecutionProvider']
        )
        self.app.prepare(ctx_id=-1, det_size=(320, 320))

    def embed(self, bgr_frame: np.ndarray) -> np.ndarray | None:
        """Returns 512-D ArcFace embedding, or None if no face detected."""
        faces = self.app.get(bgr_frame)
        if not faces:
            return None
        # Take the largest face (most likely the authenticated user)
        largest = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0]) * (f.bbox[3]-f.bbox[1]))
        return largest.normed_embedding  # 512-D, already L2 normalised

    def verify(self, bgr_frame: np.ndarray, stored_embedding: np.ndarray) -> tuple:
        emb = self.embed(bgr_frame)
        if emb is None:
            return False, 0.0
        sim = float(np.dot(emb, stored_embedding))   # both L2 normalised → dot = cosine sim
        return sim >= self.THRESHOLD, sim
```

```python
# acare_auth/face_detect.py
# Passive always-on detection — NOT recognition. Just detects presence.
import mediapipe as mp

class PassiveFaceDetector:
    """Lightweight face presence detector — triggers login flow."""
    def __init__(self):
        self.detector = mp.solutions.face_detection.FaceDetection(
            model_selection=0,           # 0 = short-range model (< 2m) — suits OT workspace
            min_detection_confidence=0.6
        )

    def face_present(self, rgb_frame) -> bool:
        results = self.detector.process(rgb_frame)
        return results.detections is not None and len(results.detections) > 0
```

**users.db schema:**

```python
# acare_auth/enrol.py — SQLite schema
import sqlite3, numpy as np, io
from cryptography.fernet import Fernet

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id            TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    role          TEXT NOT NULL,
    voice_emb     BLOB NOT NULL,    -- ECAPA-TDNN 192-D float32 as bytes
    face_emb      BLOB NOT NULL,    -- ArcFace 512-D float32 as bytes
    registered_at TEXT NOT NULL,
    active        INTEGER DEFAULT 1,
    handover_z_offset REAL DEFAULT 0.0   -- per-user height preference in metres
)
"""

def emb_to_blob(arr: np.ndarray) -> bytes:
    buf = io.BytesIO()
    np.save(buf, arr)
    return buf.getvalue()

def blob_to_emb(blob: bytes) -> np.ndarray:
    return np.load(io.BytesIO(blob))
```

**Login state machine (scripted — not free conversation):**

```
IDLE
  └─ face detected by PassiveFaceDetector
       └─ FACE_DETECTED
            └─ lookup face embedding in users.db → match found?
                 ├─ YES → TTS "Welcome {name}. Say confirm to log in."
                 │         → GREETING_SENT
                 │              └─ voice sample captured simultaneously with "confirm"
                 │                   └─ ECAPA embed → cosine sim ≥ 0.85?
                 │                        ├─ YES → session created → LOGGED_IN
                 │                        └─ NO  → TTS "Identity not recognised." → IDLE
                 └─ NO  → TTS "Please identify yourself." → MANUAL_FALLBACK
```

---

### S3 — dialogue_node.py (LangGraph)

Two operating modes controlled by `/robot_state`:

| Mode | Active When | Behaviour |
|---|---|---|
| ASSISTANT MODE | `state == LOGGED_OUT` | Groq conversational agent — ACARE intro + auth guidance only |
| DIALOGUE MODE | `state == STANDBY / LISTENING / PROCESSING` | LangGraph intent clarity + clarification + context + interruption |

**LangGraph graph structure:**

```python
# acare_dialogue/dialogue_node.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

class DialogueState(TypedDict):
    raw_text:       str
    intent:         Optional[dict]     # {tool, action, confidence} from Groq
    tool_resolved:  Optional[str]
    confidence:     float
    clarification:  Optional[str]
    pronoun_found:  bool
    multi_tool:     bool
    interrupted:    bool
    session_memory: dict

def intent_clarity_check(state: DialogueState) -> DialogueState:
    """Route based on confidence and pronoun presence."""
    conf = state['intent']['confidence'] if state['intent'] else 0.0
    text = state['raw_text']
    pronouns = ['it', 'that', 'the one', 'the smaller', 'the bigger', 'that one']
    state['pronoun_found'] = any(p in text for p in pronouns)
    if conf >= 0.80 and not state['pronoun_found']:
        state['tool_resolved'] = state['intent']['tool']
    return state

def route_after_clarity(state: DialogueState) -> str:
    if state.get('multi_tool'):
        return 'clarification'
    if state.get('pronoun_found'):
        return 'context_resolver'
    if state['intent'] and state['intent']['confidence'] >= 0.80:
        return 'auth_gate'
    return 'clarification'

def clarification_node(state: DialogueState) -> DialogueState:
    """Generate clarification question via Groq."""
    from groq import Groq
    client = Groq()
    prompt = f"The user said: '{state['raw_text']}'. Generate a short clarification question (max 10 words) to resolve the ambiguous tool request."
    resp = client.chat.completions.create(
        model='llama3-8b-8192',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.3,
        max_tokens=30
    )
    state['clarification'] = resp.choices[0].message.content.strip()
    return state

def context_resolver(state: DialogueState) -> DialogueState:
    """Resolve pronouns using session memory."""
    mem = state['session_memory']
    text = state['raw_text']
    if 'it' in text or 'that' in text:
        if mem.get('current_task') and mem['current_task'].get('tool'):
            state['tool_resolved'] = mem['current_task']['tool']
        elif mem.get('tools_fetched'):
            state['tool_resolved'] = mem['tools_fetched'][-1]['tool']
    return state

def interruption_handler(state: DialogueState) -> DialogueState:
    """New command arrived while task active — set interrupted flag."""
    state['interrupted'] = True
    return state

def build_graph() -> StateGraph:
    g = StateGraph(DialogueState)
    g.add_node('intent_clarity', intent_clarity_check)
    g.add_node('clarification',  clarification_node)
    g.add_node('context_resolver', context_resolver)
    g.add_node('interruption',   interruption_handler)
    g.add_node('auth_gate',      lambda s: s)   # pass-through; planner takes over

    g.set_entry_point('intent_clarity')
    g.add_conditional_edges('intent_clarity', route_after_clarity, {
        'clarification':    'clarification',
        'context_resolver': 'context_resolver',
        'auth_gate':        'auth_gate',
    })
    g.add_edge('clarification',    END)   # TTS clarification, wait for reply
    g.add_edge('context_resolver', 'auth_gate')
    g.add_edge('auth_gate',        END)
    return g.compile()
```

**Session memory** (reset on logout):

```python
session_memory = {
    'tools_fetched': [],           # [{'tool': str, 'timestamp': float, 'zone': str}]
    'conversation_history': [],    # capped at 20 turns
    'current_task': {},            # {'tool': str, 'status': str}
    'pending_clarification': False,
    'last_command': ''
}
```

History cap: if `len(history) > 20`, summarise oldest 10 turns via Groq into one summary turn.

---

### S4 — planner_node.py

The master orchestrator. Owns the full pick-and-place sequence. Does NOT do motor control — sends commands via embedded_interface_node.

**Internal task states (not published externally):**

```
IDLE → VISION_SEARCH → PRE_GRASP → GRASPING → HOLDING →
MOVING_TO_HANDOVER → HANDOVER → COMPLETE
```

**get_world_state():**

```python
def get_world_state(self) -> dict:
    return {
        'robot_state':      self.current_robot_state,
        'safety_severity':  self.latest_safety_severity,   # '' | 'WARNING' | 'CRITICAL' | 'ESTOP'
        'vision_ready':     self.vision_ready,
        'network_ok':       self.network_ok,
        'arm_holding':      self.latest_gripper_force > 0.5,  # N
        'gripper_force':    self.latest_gripper_force,
    }
```

**Full task execution (simplified skeleton):**

```python
async def execute_task(self, intent: ValidatedIntent):
    pipeline_start = time.monotonic()

    # 0. World state check
    ws = self.get_world_state()
    if not ws['network_ok']:
        await self.tts('Voice service unavailable.', urgent=True)
        return

    # 1. Vision ready check
    if not ws['vision_ready']:
        await self.tts('System initialising. Please wait.')
        await self.wait_for_vision_ready(timeout=30.0)

    # 2. Open gripper
    self.publish_gripper_cmd('RELEASE')
    await self.wait_for_gripper_force_zero(timeout=3.0)

    # 3. NBV search
    vision_start = time.monotonic()
    search_req = VisionSearchRequest(tool=intent.tool)
    self.vision_search_pub.publish(search_req)
    vision_result = await self.wait_for_vision_result(timeout=30.0)
    vision_ms = int((time.monotonic() - vision_start) * 1000)

    if not vision_result.found:
        await self.tts(f'Cannot locate {intent.tool}. Can you confirm it is on the tray?')
        # ... retry flow (see spec Section XI)
        return

    # 4. IK solve
    grasp_pt = (vision_result.x, vision_result.y, vision_result.z)
    pregrasp_pt = self.localiser.compute_pregrasp(grasp_pt)
    joint_angles = self.ik_solver.solve(pregrasp_pt)
    if joint_angles is None:
        await self.tts(f'Unable to reach the {intent.tool}. Please reposition it.')
        return

    # 5. Motion: pre-grasp → grasp
    motion_start = time.monotonic()
    await self.tts(f'Fetching {intent.tool} for {intent.name}. One moment.')

    ok = await self.send_arm_cmd('MOVE', joint_angles, blocking=True)
    if not ok: return

    grasp_angles = self.ik_solver.solve(grasp_pt)
    ok = await self.send_arm_cmd('MOVE', grasp_angles, blocking=True)
    if not ok: return

    ok = await self.send_gripper_cmd('GRASP', force_target=3.0, blocking=True)
    if not ok or self.latest_gripper_force < 0.5:
        # Grasp failed
        await self.tts(f'Grasp failed. Please reposition the {intent.tool}.')
        await self.send_arm_cmd('MOVE_NEUTRAL', blocking=True)
        return

    # 6. Move to handover zone
    handover_angles = self.ik_solver.solve(self.handover_zone_pos)
    await self.send_arm_cmd('MOVE', handover_angles, blocking=True)
    motion_ms = int((time.monotonic() - motion_start) * 1000)

    # 7. Three-check handover
    await self.tts(f'{intent.tool} ready. Please face the camera.')
    handover_ok = await self.handover_protocol.run(intent, timeout=30.0)

    if not handover_ok:
        # Timeout — safe deposit
        await self.tts(f'No collection detected. Returning {intent.tool} to tray.')
        await self.send_arm_cmd('MOVE', self.safe_drop_angles, blocking=True)
        await self.send_gripper_cmd('RELEASE')
        return

    # 8. Complete
    total_ms = int((time.monotonic() - pipeline_start) * 1000)
    await self.tts('Handover complete. Is there anything else?')
    await self.send_arm_cmd('MOVE_NEUTRAL', blocking=True)
    self.log(intent, vision_ms, motion_ms, total_ms, vision_result.zone)
    self.nbv_search.save_map()
```

---

### S5 — ik_solver.py

> ⚠️ Cannot be built until hardware team provides DH parameters and joint limits. All DH values below are `[FILL_AFTER_ASSEMBLY]`.

**Method:** Damped Least Squares (DLS). Handles near-singular configurations without diverging.

```python
# acare_planner/ik_solver.py
import numpy as np
import yaml
from pathlib import Path

class IKSolver:
    """
    6-DOF DLS IK solver.
    DH parameters and joint limits loaded from system.yaml after assembly.
    """
    DAMPING      = 0.05
    MAX_ITER     = 100
    POS_TOL      = 0.001  # 1 mm
    ORI_TOL      = 0.01   # rad

    def __init__(self, system_yaml_path: str):
        with open(system_yaml_path) as f:
            cfg = yaml.safe_load(f)
        arm = cfg['arm']
        # DH: list of {a, alpha, d, theta_offset} per joint [FILL_AFTER_ASSEMBLY]
        self.dh = arm['dh_params']
        # Joint limits [FILL_AFTER_ASSEMBLY]
        self.q_min = np.array(arm['joint_limits_min'])
        self.q_max = np.array(arm['joint_limits_max'])
        # Home position
        self.q_home = np.array(arm['neutral_joint_angles'])

    def _dh_transform(self, a, alpha, d, theta) -> np.ndarray:
        """Compute 4×4 DH transform matrix for one joint."""
        ct, st = np.cos(theta), np.sin(theta)
        ca, sa = np.cos(alpha), np.sin(alpha)
        return np.array([
            [ct,  -st*ca,  st*sa,  a*ct],
            [st,   ct*ca, -ct*sa,  a*st],
            [0,    sa,     ca,     d   ],
            [0,    0,      0,      1   ]
        ])

    def forward_kinematics(self, q: np.ndarray) -> np.ndarray:
        """Compute 4×4 end-effector transform from joint angles q[6]."""
        T = np.eye(4)
        for i, p in enumerate(self.dh):
            T = T @ self._dh_transform(p['a'], p['alpha'], p['d'], q[i] + p['theta_offset'])
        return T

    def _numerical_jacobian(self, q: np.ndarray, eps: float = 1e-4) -> np.ndarray:
        """6×6 Jacobian via finite differences. Rows: [dx,dy,dz,drx,dry,drz]."""
        T0 = self.forward_kinematics(q)
        p0 = T0[:3, 3]
        J = np.zeros((6, 6))
        for i in range(6):
            q2 = q.copy(); q2[i] += eps
            T2 = self.forward_kinematics(q2)
            # Position rows
            J[:3, i] = (T2[:3, 3] - p0) / eps
            # Orientation rows (axis-angle approximation)
            R_delta = T2[:3, :3] @ T0[:3, :3].T
            J[3, i] = R_delta[2, 1] / eps
            J[4, i] = R_delta[0, 2] / eps
            J[5, i] = R_delta[1, 0] / eps
        return J

    def solve(self, target_pos: tuple, target_ori: np.ndarray = None,
              q_init: np.ndarray = None) -> np.ndarray | None:
        """
        Solve IK for target_pos (x,y,z) in robot base frame.
        target_ori: optional 3×3 rotation matrix. If None, only position is controlled.
        Returns joint_angles[6] or None if no solution found.
        """
        q = q_init if q_init is not None else self.q_home.copy()
        target_p = np.array(target_pos)

        for _ in range(self.MAX_ITER):
            T = self.forward_kinematics(q)
            e_pos = target_p - T[:3, 3]

            if target_ori is not None:
                R_err = target_ori @ T[:3, :3].T
                e_ori = np.array([R_err[2,1], R_err[0,2], R_err[1,0]])
                e = np.concatenate([e_pos, e_ori])
            else:
                e = e_pos
                # Use only position rows of Jacobian
            
            if np.linalg.norm(e_pos) < self.POS_TOL:
                if target_ori is None or np.linalg.norm(e[3:]) < self.ORI_TOL:
                    return q

            J = self._numerical_jacobian(q)
            if target_ori is None:
                J = J[:3, :]

            # DLS update: Δq = J^T (J J^T + λ²I)^{-1} e
            lam2 = self.DAMPING ** 2
            A = J @ J.T + lam2 * np.eye(J.shape[0])
            dq = J.T @ np.linalg.solve(A, e)
            q = q + dq

            # Clamp to joint limits
            q = np.clip(q, self.q_min, self.q_max)

        return None   # did not converge

    def solve_with_fallback(self, target_pos: tuple) -> np.ndarray | None:
        """Try solve, then try 90° rotated approach, then fail."""
        sol = self.solve(target_pos)
        if sol is not None:
            return sol
        # Try rotated approach orientation (90° around Z)
        R90 = np.array([[0,-1,0],[1,0,0],[0,0,1]], dtype=float)
        sol = self.solve(target_pos, target_ori=R90)
        return sol  # None if still failed
```

---

### S6 — handover.py

The three-check sequential handover verification protocol.

```python
# acare_planner/handover.py
import asyncio, time
from acare_msgs.msg import HandStatus, AuthResult

class HandoverProtocol:
    FACE_CHECK_INTERVAL = 0.5   # seconds
    FACE_SIM_THRESHOLD  = 0.78
    FACE_FAIL_MAX       = 3
    TOTAL_TIMEOUT       = 30.0  # seconds

    def __init__(self, auth_node_ref, voice_node_ref, gripper_pub, tts_fn):
        self.auth   = auth_node_ref
        self.voice  = voice_node_ref
        self.tts    = tts_fn
        self.gripper_pub = gripper_pub
        self.latest_hand: HandStatus = HandStatus()
        self.voice_confirm_received = False

    async def run(self, intent, hand_status_sub, timeout: float = 30.0) -> bool:
        deadline = time.monotonic() + timeout

        # --- CHECK 1: Continuous face verification ---
        face_fails = 0
        while time.monotonic() < deadline:
            sim = self.auth.get_current_face_similarity()   # runs every 0.5s in auth_node
            if sim >= self.FACE_SIM_THRESHOLD:
                face_fails = 0
                break
            face_fails += 1
            if face_fails >= self.FACE_FAIL_MAX:
                await self.tts('Please face the camera.')
                face_fails = 0
            await asyncio.sleep(self.FACE_CHECK_INTERVAL)
        else:
            return False   # timeout

        # --- CHECK 2: Hand detection ---
        await self.tts('Please place your open palm under the gripper.')
        while time.monotonic() < deadline:
            hs = self.latest_hand
            if hs.hand_detected:
                if not hs.is_open:
                    await self.tts('Please open your palm.')
                elif not hs.palm_up:
                    await self.tts('Please turn your palm upward.')
                else:
                    break   # hand OK
            await asyncio.sleep(0.1)
        else:
            return False

        # --- CHECK 3: Voice confirmation ---
        await self.tts('Say take to receive.')
        self.voice_confirm_received = False
        while time.monotonic() < deadline:
            if self.voice_confirm_received:
                break
            await asyncio.sleep(0.05)
        else:
            return False

        # All three checks passed → release
        from acare_msgs.msg import GripperCommand
        cmd = GripperCommand(); cmd.command = 'RELEASE'
        self.gripper_pub.publish(cmd)
        await asyncio.sleep(1.0)   # wait for force to drop

        # Height preference update
        # (stored back to users.db via auth_node if user said 'lower'/'higher')
        return True

    def on_voice_confirm(self, word: str):
        if word.strip().lower() in ('take', 'yes', 'got it'):
            self.voice_confirm_received = True

    def on_hand_status(self, msg: HandStatus):
        self.latest_hand = msg
```

---

### S7 — state_manager.py

```python
# acare_planner/state_manager.py
import rclpy, threading, time
from rclpy.node import Node
from acare_msgs.msg import RobotState, StateTransition, SafetyAlert
from std_msgs.msg import String

VALID_TRANSITIONS = {
    'OFFLINE':    {'LOGGED_OUT'},
    'LOGGED_OUT': {'STANDBY'},
    'STANDBY':    {'LISTENING', 'LOGGED_OUT'},
    'LISTENING':  {'PROCESSING', 'STANDBY'},
    'PROCESSING': {'EXECUTING', 'STANDBY'},
    'EXECUTING':  {'HOLDING', 'ESTOP'},
    'HOLDING':    {'HANDOVER', 'ESTOP'},
    'HANDOVER':   {'STANDBY', 'ESTOP'},
    'ESTOP':      {'STANDBY'},
    'ERROR':      {'OFFLINE'},
}

LOGOUT_ALLOWED_FROM = {'STANDBY', 'ESTOP', 'LOGGED_OUT'}
NO_LOGOUT_FROM      = {'EXECUTING', 'HOLDING', 'HANDOVER'}

class StateManager(Node):
    def __init__(self):
        super().__init__('state_manager')
        self.state = 'OFFLINE'
        self.active_user_id = ''
        self._lock = threading.Lock()
        self._inactivity_timer = None

        self.state_pub = self.create_publisher(RobotState, '/robot_state', 10)
        self.create_subscription(StateTransition, '/state_transition', self.on_transition, 10)
        self.create_subscription(SafetyAlert, '/safety_alert', self.on_safety_alert, 10)

        self._transition('LOGGED_OUT')   # boot

    def on_transition(self, msg: StateTransition):
        with self._lock:
            target = msg.target_state
            # Logout guard
            if target == 'LOGGED_OUT' and self.state in NO_LOGOUT_FROM:
                self.get_logger().warn(f'Logout rejected from {self.state}')
                return
            self._transition(target)

    def _transition(self, target: str):
        allowed = VALID_TRANSITIONS.get(self.state, set())
        if target not in allowed and target != self.state:
            self.get_logger().error(f'Invalid transition {self.state} → {target}')
            return
        self.state = target
        msg = RobotState()
        msg.state = target
        msg.active_user_id = self.active_user_id
        self.state_pub.publish(msg)
        self.get_logger().info(f'State → {target}')
        self._reset_inactivity_timer()

    def _reset_inactivity_timer(self):
        if self._inactivity_timer:
            self._inactivity_timer.cancel()
        if self.state == 'STANDBY':
            self._inactivity_timer = threading.Timer(300.0, self._auto_logout)
            self._inactivity_timer.start()

    def _auto_logout(self):
        with self._lock:
            self.get_logger().info('Session timeout — auto-logout')
            # TTS via topic
            self._transition('LOGGED_OUT')

    def on_safety_alert(self, msg: SafetyAlert):
        if msg.severity == 'ESTOP':
            with self._lock:
                self._transition('ESTOP')
```

---

### S8 — safety_node.py

```python
# acare_safety/safety_node.py
import rclpy, yaml
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from acare_msgs.msg import MotionFeedback, SafetyAlert
from pathlib import Path

THRESHOLDS_PATH = Path('/acare_ws/src/acare_bringup/config/thresholds.yaml')

class SafetyNode(Node):
    def __init__(self):
        super().__init__('safety_node')
        with open(THRESHOLDS_PATH) as f:
            cfg = yaml.safe_load(f)['safety']
        self.T = cfg   # shorthand

        self.alert_pub = self.create_publisher(SafetyAlert, '/safety_alert', 10)
        self.create_subscription(LaserScan, '/scan', self.on_lidar, 10)
        self.create_subscription(MotionFeedback, '/motion_feedback', self.on_telemetry, 10)

    def _publish_alert(self, severity: str, reason: str, source: str):
        msg = SafetyAlert()
        msg.severity = severity
        msg.reason   = reason
        msg.source   = source
        self.alert_pub.publish(msg)
        self.get_logger().warn(f'[{severity}] {source}: {reason}')

    def on_lidar(self, msg: LaserScan):
        """Check proximity in ±60° arc (front of robot)."""
        import math
        n = len(msg.ranges)
        # Front arc: roughly middle third of scan
        front = msg.ranges[n//3 : 2*n//3]
        valid = [r for r in front if msg.range_min < r < msg.range_max]
        if not valid:
            return
        min_dist_mm = min(valid) * 1000   # metres → mm

        if min_dist_mm < self.T['lidar_stop_mm']:
            self._publish_alert('ESTOP', f'Person {min_dist_mm:.0f}mm from robot', 'lidar')
        elif min_dist_mm < self.T['lidar_caution_mm']:
            self._publish_alert('WARNING', f'Person {min_dist_mm:.0f}mm — reduced speed', 'lidar')

    def on_telemetry(self, msg: MotionFeedback):
        """Check MCU sensor values from 50 Hz telemetry."""
        # Joint currents
        for i, curr in enumerate(msg.joint_currents):
            if curr > self.T['current_limit_A']:
                self._publish_alert('ESTOP', f'Joint {i+1} overcurrent {curr:.1f}A', 'current')
            elif curr > self.T['current_warning_A']:
                self._publish_alert('WARNING', f'Joint {i+1} current {curr:.1f}A', 'current')

        # Temperatures
        for i, temp in enumerate(msg.temperatures):
            if temp > self.T['temperature_estop_C']:
                self._publish_alert('ESTOP', f'Joint {i+1} overtemp {temp:.1f}°C', 'temp')
            elif temp > self.T['temperature_slow_C']:
                self._publish_alert('CRITICAL', f'Joint {i+1} temp {temp:.1f}°C', 'temp')
            elif temp > self.T['temperature_warning_C']:
                self._publish_alert('WARNING', f'Joint {i+1} temp {temp:.1f}°C', 'temp')

        # Gripper force
        if msg.gripper_force > self.T['gripper_force_limit_N']:
            self._publish_alert('ESTOP', f'Gripper force spike {msg.gripper_force:.1f}N', 'gripper')
        elif msg.gripper_force > self.T['gripper_force_warning_N']:
            self._publish_alert('WARNING', f'Gripper force {msg.gripper_force:.1f}N', 'gripper')
```

---

### S9 — embedded_interface_node (C++)

This is a C++ ROS2 node with a `MutuallyExclusiveCallbackGroup` for the heartbeat so it never competes with command processing.

```cpp
// acare_embedded_interface/interface_node.cpp
#include <rclcpp/rclcpp.hpp>
#include <serial/serial.h>   // ROS serial library
#include <acare_msgs/msg/arm_command.hpp>
#include <acare_msgs/msg/gripper_command.hpp>
#include <acare_msgs/msg/motion_feedback.hpp>
#include <acare_msgs/msg/emergency_signal.hpp>
#include <std_msgs/msg/string.hpp>
#include <nlohmann/json.hpp>
#include <chrono>

using json = nlohmann::json;
using namespace std::chrono_literals;

class EmbeddedInterfaceNode : public rclcpp::Node {
public:
    EmbeddedInterfaceNode() : Node("embedded_interface_node") {
        // MutuallyExclusive callback group for heartbeat
        hb_group_ = create_callback_group(
            rclcpp::CallbackGroupType::MutuallyExclusive);
        cmd_group_ = create_callback_group(
            rclcpp::CallbackGroupType::MutuallyExclusive);

        // Open UART
        serial_.setPort("/dev/ttyS0");
        serial_.setBaudrate(1000000);  // 1 Mbps
        serial_.open();

        // Publishers
        feedback_pub_ = create_publisher<acare_msgs::msg::MotionFeedback>(
            "/motion_feedback", rclcpp::QoS(10).best_effort());

        // Subscribers
        auto cmd_opts = rclcpp::SubscriptionOptions();
        cmd_opts.callback_group = cmd_group_;
        arm_sub_ = create_subscription<acare_msgs::msg::ArmCommand>(
            "/arm_command", rclcpp::QoS(10).reliable(),
            std::bind(&EmbeddedInterfaceNode::on_arm_command, this, std::placeholders::_1),
            cmd_opts);
        gripper_sub_ = create_subscription<acare_msgs::msg::GripperCommand>(
            "/gripper_command", rclcpp::QoS(10).reliable(),
            std::bind(&EmbeddedInterfaceNode::on_gripper_command, this, std::placeholders::_1),
            cmd_opts);
        estop_sub_ = create_subscription<acare_msgs::msg::EmergencySignal>(
            "/emergency_stop", rclcpp::QoS(10).reliable(),
            std::bind(&EmbeddedInterfaceNode::on_estop, this, std::placeholders::_1),
            cmd_opts);

        // Heartbeat timer — MutuallyExclusive group
        heartbeat_timer_ = create_wall_timer(
            200ms,
            std::bind(&EmbeddedInterfaceNode::send_heartbeat, this),
            hb_group_);

        // Status reader timer at 50 Hz
        status_timer_ = create_wall_timer(
            20ms,
            std::bind(&EmbeddedInterfaceNode::read_status, this));

        RCLCPP_INFO(get_logger(), "EmbeddedInterface: UART open at 1 Mbps");
    }

private:
    void send_heartbeat() {
        json cmd;
        cmd["command"]     = "HEARTBEAT";
        cmd["timestamp"]   = std::chrono::system_clock::now().time_since_epoch().count();
        cmd["robot_state"] = current_robot_state_;
        send_json(cmd);
    }

    void on_arm_command(const acare_msgs::msg::ArmCommand::SharedPtr msg) {
        json cmd;
        cmd["command"] = msg->command;
        if (!msg->joint_angles.empty())
            cmd["joint_angles"] = msg->joint_angles;
        cmd["velocity_scale"] = msg->velocity_scale;
        cmd["accel_limit"]    = msg->accel_limit;
        send_json(cmd);
    }

    void on_gripper_command(const acare_msgs::msg::GripperCommand::SharedPtr msg) {
        json cmd;
        cmd["command"]      = msg->command;   // "GRASP" or "RELEASE"
        cmd["force_target"] = msg->force_target;
        send_json(cmd);
    }

    void on_estop(const acare_msgs::msg::EmergencySignal::SharedPtr) {
        json cmd; cmd["command"] = "ESTOP";
        send_json(cmd);   // bypasses all queues — sent immediately
    }

    void send_json(const json& j) {
        std::string s = j.dump() + "\n";
        if (serial_.isOpen())
            serial_.write(s);
    }

    void read_status() {
        if (!serial_.available()) return;
        std::string line = serial_.readline();
        try {
            auto j = json::parse(line);
            acare_msgs::msg::MotionFeedback fb;
            // Populate feedback from MCU JSON
            auto ja = j["joint_positions"].get<std::vector<float>>();
            fb.joint_positions.assign(ja.begin(), ja.end());
            auto jv = j["joint_velocities"].get<std::vector<float>>();
            fb.joint_velocities.assign(jv.begin(), jv.end());
            auto jc = j["joint_currents"].get<std::vector<float>>();
            fb.joint_currents.assign(jc.begin(), jc.end());
            auto jt = j["temperatures"].get<std::vector<float>>();
            fb.temperatures.assign(jt.begin(), jt.end());
            fb.gripper_force = j["gripper_force"].get<float>();
            fb.imu_roll      = j["imu"]["roll"].get<float>();
            fb.imu_pitch     = j["imu"]["pitch"].get<float>();
            fb.imu_yaw       = j["imu"]["yaw"].get<float>();
            fb.success       = (j["fault_code"].get<int>() == 0);
            feedback_pub_->publish(fb);
        } catch (...) {
            RCLCPP_WARN(get_logger(), "Failed to parse MCU status line");
        }
    }

    serial::Serial serial_;
    std::string current_robot_state_ = "LOGGED_OUT";
    rclcpp::CallbackGroup::SharedPtr hb_group_, cmd_group_;
    rclcpp::TimerBase::SharedPtr heartbeat_timer_, status_timer_;
    rclcpp::Publisher<acare_msgs::msg::MotionFeedback>::SharedPtr feedback_pub_;
    rclcpp::Subscription<acare_msgs::msg::ArmCommand>::SharedPtr arm_sub_;
    rclcpp::Subscription<acare_msgs::msg::GripperCommand>::SharedPtr gripper_sub_;
    rclcpp::Subscription<acare_msgs::msg::EmergencySignal>::SharedPtr estop_sub_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<EmbeddedInterfaceNode>();
    rclcpp::executors::MultiThreadedExecutor exec;
    exec.add_node(node);
    exec.spin();
    rclcpp::shutdown();
}
```

---

### S10 — log_node.py

```python
# acare_logging/log_node.py
import rclpy, sqlite3, uuid, gzip, csv, io, os, time
from rclpy.node import Node
from acare_msgs.msg import LogEvent
from pathlib import Path

DB_PATH      = Path('/acare_ws/logs/acare_logs.db')
MAX_SIZE_MB  = 200
BATCH_SIZE   = 10

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS events (
    event_id        TEXT PRIMARY KEY,
    timestamp       TEXT,
    staff_id        TEXT,
    staff_name      TEXT,
    event_type      TEXT,
    tool            TEXT,
    zone_found      TEXT,
    grasp_attempts  INTEGER,
    success         INTEGER,
    failure_reason  TEXT,
    sensor_values   TEXT,
    safety_severity TEXT,
    voice_e2e_ms    INTEGER,
    vision_search_ms INTEGER,
    motion_ms       INTEGER,
    total_task_ms   INTEGER
)
"""

class LogNode(Node):
    def __init__(self):
        super().__init__('log_node')
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self.conn.execute(CREATE_SQL)
        self.conn.commit()
        self.buffer = []

        self.create_subscription(LogEvent, '/log_event', self.on_log, 10)
        self.get_logger().info('LogNode ready')

    def on_log(self, msg: LogEvent):
        self.buffer.append((
            str(uuid.uuid4()),
            str(msg.timestamp),
            msg.user_id,
            '',   # name looked up if needed
            msg.event_type,
            msg.tool,
            '',   # zone_found
            0,    # grasp_attempts
            1 if msg.state else 0,
            msg.description,
            '{}',
            msg.safety_severity,
            msg.voice_e2e_ms,
            msg.vision_search_ms if hasattr(msg, 'vision_search_ms') else 0,
            msg.motion_ms if hasattr(msg, 'motion_ms') else 0,
            msg.total_task_ms if hasattr(msg, 'total_task_ms') else 0,
        ))
        if len(self.buffer) >= BATCH_SIZE:
            self._flush()

    def _flush(self):
        self.conn.executemany(
            "INSERT OR IGNORE INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            self.buffer
        )
        self.conn.commit()
        self.buffer.clear()
        self._check_rotation()

    def _check_rotation(self):
        size_mb = DB_PATH.stat().st_size / (1024 * 1024)
        if size_mb < MAX_SIZE_MB:
            return
        # Archive oldest 20% rows to gzipped CSV
        rows = self.conn.execute(
            "SELECT * FROM events ORDER BY timestamp ASC LIMIT "
            f"(SELECT COUNT(*) FROM events) * 20 / 100"
        ).fetchall()
        archive_path = DB_PATH.parent / f'archive_{int(time.time())}.csv.gz'
        with gzip.open(archive_path, 'wt') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        ids = [r[0] for r in rows]
        self.conn.execute(
            f"DELETE FROM events WHERE event_id IN ({','.join('?'*len(ids))})", ids)
        self.conn.commit()
        self.get_logger().info(f'Log rotation: archived {len(rows)} rows → {archive_path.name}')
```

---

### S11 — admin_cli.py

```python
# acare_admin/admin_cli.py
"""
Usage examples:
  python admin.py enrol --name "Dr. Sharma" --role surgeon
  python admin.py revoke --id staff_001
  python admin.py list-staff
  python admin.py set-api-key --service deepgram --key YOUR_KEY
  python admin.py set-api-key --service groq --key YOUR_KEY
  python admin.py set-threshold --sensor joint_current --value 8.0
  python admin.py show-logs --last 50
  python admin.py export-logs --format csv
  python admin.py status
  python admin.py calibrate
  python admin.py demo-mode --enable
  python admin.py demo-mode --disable
"""
import argparse, sqlite3, yaml, json, sys
from pathlib import Path
from cryptography.fernet import Fernet

DB_PATH       = Path('/acare_ws/logs/acare_logs.db')
KEY_PATH      = Path('/etc/acare/key.bin')
API_KEYS_PATH = Path('/etc/acare/api_keys.yaml')
THRESHOLDS    = Path('/acare_ws/src/acare_bringup/config/thresholds.yaml')

def get_fernet() -> Fernet:
    if not KEY_PATH.exists():
        key = Fernet.generate_key()
        KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
        KEY_PATH.write_bytes(key)
    return Fernet(KEY_PATH.read_bytes())

def cmd_enrol(args):
    """Trigger enrolment — calls auth_node enrolment service via ROS2."""
    import subprocess
    subprocess.run([
        'ros2', 'service', 'call', '/enrol_staff',
        'acare_msgs/srv/EnrolStaff',
        f'{{"name": "{args.name}", "role": "{args.role}"}}'
    ])

def cmd_set_api_key(args):
    f = get_fernet()
    keys = {}
    if API_KEYS_PATH.exists():
        keys = yaml.safe_load(API_KEYS_PATH.read_text()) or {}
    keys[args.service] = f.encrypt(args.key.encode()).decode()
    API_KEYS_PATH.parent.mkdir(parents=True, exist_ok=True)
    API_KEYS_PATH.write_text(yaml.dump(keys))
    print(f'API key for {args.service} saved (encrypted).')

def cmd_set_threshold(args):
    with open(THRESHOLDS) as f:
        cfg = yaml.safe_load(f)
    sensor_map = {
        'joint_current': ('safety', 'current_limit_A'),
        'joint_temp':    ('safety', 'temperature_estop_C'),
        'gripper_force': ('safety', 'gripper_force_limit_N'),
    }
    if args.sensor not in sensor_map:
        print(f'Unknown sensor. Valid: {list(sensor_map)}')
        return
    section, key = sensor_map[args.sensor]
    cfg[section][key] = float(args.value)
    with open(THRESHOLDS, 'w') as f:
        yaml.dump(cfg, f)
    print(f'Threshold {args.sensor} set to {args.value}')

def cmd_show_logs(args):
    conn = sqlite3.connect(str(DB_PATH))
    rows = conn.execute(
        f"SELECT timestamp, staff_id, event_type, tool, success FROM events "
        f"ORDER BY timestamp DESC LIMIT {args.last}"
    ).fetchall()
    for r in rows:
        print(r)

def cmd_demo_mode(args):
    """Demo mode: disable biometric checks for exhibition."""
    cfg_path = Path('/acare_ws/src/acare_bringup/config/system.yaml')
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    cfg['demo_mode'] = args.enable
    with open(cfg_path, 'w') as f:
        yaml.dump(cfg, f)
    print(f"Demo mode {'ENABLED' if args.enable else 'DISABLED'}")

def cmd_calibrate(args):
    """7-step calibration procedure."""
    print("=== ACARE Calibration Procedure ===")
    print("Step 1: Joint homing (Teensy will move each joint to limit switch)")
    input("  Press ENTER to start joint homing...")
    import subprocess
    subprocess.run(['ros2', 'service', 'call', '/calibrate',
                    'std_srvs/srv/Trigger', '{}'])
    print("Step 2: Camera calibration — place checkerboard in workspace")
    input("  Press ENTER when checkerboard is in place...")
    # ... (each step triggers the appropriate ROS2 service)
    print("Calibration complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='admin')
    sub = parser.add_subparsers(dest='cmd')

    p_enrol = sub.add_parser('enrol')
    p_enrol.add_argument('--name', required=True)
    p_enrol.add_argument('--role', required=True)

    p_key = sub.add_parser('set-api-key')
    p_key.add_argument('--service', required=True, choices=['deepgram','groq'])
    p_key.add_argument('--key', required=True)

    p_thresh = sub.add_parser('set-threshold')
    p_thresh.add_argument('--sensor', required=True)
    p_thresh.add_argument('--value', required=True)

    p_logs = sub.add_parser('show-logs')
    p_logs.add_argument('--last', type=int, default=20)

    p_demo = sub.add_parser('demo-mode')
    p_demo.add_argument('--enable', action='store_true')
    p_demo.add_argument('--disable', dest='enable', action='store_false')
    p_demo.set_defaults(enable=False)

    sub.add_parser('calibrate')

    args = parser.parse_args()
    dispatch = {
        'enrol':         cmd_enrol,
        'set-api-key':   cmd_set_api_key,
        'set-threshold': cmd_set_threshold,
        'show-logs':     cmd_show_logs,
        'demo-mode':     cmd_demo_mode,
        'calibrate':     cmd_calibrate,
    }
    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        parser.print_help()
```

---

### S12 — supervisor.py

Standalone Python script — NOT a ROS2 node. Launched separately from the ROS2 stack.

```python
# acare_bringup/supervisor.py
import subprocess, time, sys

# Nodes that will be auto-restarted on crash
AUTO_RESTART = ['log_node', 'admin_node', 'dialogue_node']
# Nodes that will NOT be restarted — trigger ESTOP instead
CRITICAL     = ['safety_node', 'embedded_interface_node', 'state_manager', 'planner_node']

# ROS2 node names as they appear in `ros2 node list`
NODE_ROS_NAMES = {
    'log_node':                '/log_node',
    'admin_node':              '/admin_node',
    'dialogue_node':           '/dialogue_node',
    'safety_node':             '/safety_node',
    'embedded_interface_node': '/embedded_interface_node',
    'state_manager':           '/state_manager',
    'planner_node':            '/planner_node',
}

NODE_CMDS = {
    'log_node':               ['ros2', 'run', 'acare_logging',           'log_node'],
    'admin_node':             ['ros2', 'run', 'acare_admin',             'admin_node'],
    'dialogue_node':          ['ros2', 'run', 'acare_dialogue',          'dialogue_node'],
    'safety_node':            ['ros2', 'run', 'acare_safety',            'safety_node'],
    'embedded_interface_node':['ros2', 'run', 'acare_embedded_interface','interface_node'],
    'state_manager':          ['ros2', 'run', 'acare_planner',           'state_manager'],
    'planner_node':           ['ros2', 'run', 'acare_planner',           'planner_node'],
}

processes = {}

def start_node(name: str):
    cmd = NODE_CMDS[name]
    processes[name] = subprocess.Popen(cmd)
    print(f'[supervisor] Started {name} (PID {processes[name].pid})')

def is_node_alive(ros_name: str) -> bool:
    """
    Check if a ROS2 node is alive using `ros2 node list`.
    This is reliable — it queries the ROS2 graph directly rather than
    checking the launcher process exit code, which can be misleading.
    """
    try:
        result = subprocess.run(
            ['ros2', 'node', 'list'],
            capture_output=True, text=True, timeout=5.0
        )
        return ros_name in result.stdout
    except subprocess.TimeoutExpired:
        return True   # assume alive if we can't check — avoid false ESTOP

def trigger_estop():
    subprocess.run([
        'ros2', 'topic', 'pub', '--once', '/emergency_stop',
        'acare_msgs/msg/EmergencySignal', '{reason: "Critical node crash"}'
    ])

def monitor():
    while True:
        time.sleep(5)
        for name in list(NODE_CMDS.keys()):
            ros_name = NODE_ROS_NAMES[name]
            if not is_node_alive(ros_name):
                print(f'[supervisor] {name} not found in ROS2 graph — crashed')
                if name in AUTO_RESTART:
                    print(f'[supervisor] Restarting {name}...')
                    time.sleep(1)
                    start_node(name)
                elif name in CRITICAL:
                    print(f'[supervisor] CRITICAL node {name} crashed — triggering ESTOP')
                    trigger_estop()

if __name__ == '__main__':
    for name in NODE_CMDS:
        start_node(name)
    monitor()
```

---

## 4. Configuration Files

### system.yaml (corrected — edge-tts, no Google Cloud TTS)

```yaml
robot:
  workspace:
    xmin: -0.4
    xmax:  0.4
    ymin: -0.3
    ymax:  0.3
    zmin:  0.0
    zmax:  0.5
  safe_drop_zone:  {x: 0.0, y: 0.35, z: 0.05}   # [FILL_AFTER_ASSEMBLY]
  handover_zone:   {x: 0.0, y: 0.40, z: 0.10}   # [FILL_AFTER_ASSEMBLY]
  handover_height_adjustment_m: 0.05

arm:
  dh_params:   # [FILL_AFTER_ASSEMBLY — required for IK solver]
    # Gearbox ratios (confirmed): Joint 2 (Shoulder) = 22:1, Joint 3 (Elbow) = 15:1
    # Joints 4,5,6 ratios: [FILL_AFTER_ASSEMBLY — confirm with hardware team]
    - {a: 0.0, alpha: 0.0, d: 0.0, theta_offset: 0.0}  # Joint 1 placeholder
    - {a: 0.0, alpha: 0.0, d: 0.0, theta_offset: 0.0}  # Joint 2 placeholder
    - {a: 0.0, alpha: 0.0, d: 0.0, theta_offset: 0.0}  # Joint 3 placeholder
    - {a: 0.0, alpha: 0.0, d: 0.0, theta_offset: 0.0}  # Joint 4 placeholder
    - {a: 0.0, alpha: 0.0, d: 0.0, theta_offset: 0.0}  # Joint 5 placeholder
    - {a: 0.0, alpha: 0.0, d: 0.0, theta_offset: 0.0}  # Joint 6 placeholder
  joint_limits_min: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]    # [FILL_AFTER_ASSEMBLY]
  joint_limits_max: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]    # [FILL_AFTER_ASSEMBLY]
  neutral_joint_angles: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # [FILL_AFTER_ASSEMBLY]
  link_lengths:
    base_height: 0.0   # [FILL_AFTER_ASSEMBLY]
    upper_arm:   0.0   # [FILL_AFTER_ASSEMBLY]
    forearm:     0.0   # [FILL_AFTER_ASSEMBLY]
    wrist:       0.0   # [FILL_AFTER_ASSEMBLY]
    gripper:     0.0   # [FILL_AFTER_ASSEMBLY]

camera:
  fx: 0.0    # [FILL_AFTER_CALIBRATION]
  fy: 0.0    # [FILL_AFTER_CALIBRATION]
  cx: 0.0    # [FILL_AFTER_CALIBRATION]
  cy: 0.0    # [FILL_AFTER_CALIBRATION]
  T_robot_camera:  # 4×4 as flat 16-element list [FILL_AFTER_CALIBRATION]
    [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]

vision:
  model_path: '/models/yolo_int8.onnx'
  confidence_threshold: 0.70
  input_size: 320

voice:
  # TTS engines — NOTE: Google Cloud TTS is NOT used. Use edge-tts.
  tts_normal:   edge_tts                 # Microsoft Edge TTS (free, pip install edge-tts)
  tts_safety:   pyttsx3                  # offline, zero latency, for ESTOP/critical
  tts_fallback: kokoro_onnx              # offline fallback if no internet
  edge_tts_voice: 'en-IN-NeerjaNeural'  # or 'en-IN-PrabhatNeural' (male)
  tts_rate: 150                          # words per minute
  use_deepgram: true
  use_groq: true
  network_fail_hold_threshold_seconds: 5
  session_inactivity_timeout_seconds: 300
  handover_timeout_seconds: 30
  estop_keywords: [stop, halt, emergency, abort, ruko, bas]

auth:
  voice_similarity_threshold: 0.85
  face_similarity_threshold:  0.78
  voice_drift_consecutive_threshold: 3
  face_check_interval_s: 0.5
  enrol_voice_samples: 3
  enrol_face_frames:   10

demo_mode: false
```

### thresholds.yaml

```yaml
safety:
  current_limit_A:            8.0
  current_warning_A:          6.0
  temperature_estop_C:       75.0
  temperature_slow_C:        65.0
  temperature_warning_C:     55.0
  velocity_limit_degs:      120.0
  velocity_operational_degs: 80.0
  lidar_caution_mm:          600
  lidar_stop_mm:             400
  gripper_force_limit_N:     15.0
  gripper_force_warning_N:   10.0

fake_detection:
  texture_variance_threshold: 120.0  # MUST calibrate empirically — this is a starting estimate
  depth_variance_threshold:   0.002  # MUST calibrate empirically — this is a starting estimate
```

### probability_map.yaml (example admin-defined prior)

```yaml
# Set this before a demo to reflect expected tool placement.
# All values clamped to [0.05, 0.90] on every Bayesian update.
zone_A:                   # left side of tray
  scalpel:  0.50
  scissors: 0.20
  forceps:  0.15
  bandage:  0.05
  gauze:    0.05
  thermometer: 0.05
zone_B:                   # centre of tray
  scissors: 0.45
  forceps:  0.30
  scalpel:  0.10
  gauze:    0.05
  bandage:  0.05
  thermometer: 0.05
zone_C:                   # right side / sterile tray
  gauze:    0.55
  plaster:  0.30
  bandage:  0.10
  oximeter: 0.05
```

---

## 5. ROS2 Package Structure & acare_msgs

### Directory tree

```
acare_ws/
├── src/
│   ├── acare_msgs/
│   │   ├── msg/
│   │   │   ├── RobotState.msg
│   │   │   ├── StateTransition.msg
│   │   │   ├── Intent.msg
│   │   │   ├── ValidatedIntent.msg
│   │   │   ├── SafetyAlert.msg
│   │   │   ├── HandStatus.msg
│   │   │   ├── AuthResult.msg
│   │   │   ├── VisionResult.msg
│   │   │   ├── VisionSearchRequest.msg
│   │   │   ├── ArmCommand.msg
│   │   │   ├── GripperCommand.msg
│   │   │   ├── MotionFeedback.msg
│   │   │   ├── LogEvent.msg
│   │   │   └── EmergencySignal.msg
│   │   ├── srv/
│   │   │   └── EnrolStaff.srv
│   │   ├── CMakeLists.txt
│   │   └── package.xml
│   ├── acare_voice/
│   │   ├── voice_node.py
│   │   ├── vad.py
│   │   ├── asr.py
│   │   ├── tts.py             # edge-tts + pyttsx3 + kokoro fallback
│   │   ├── keyword_monitor.py
│   │   └── normaliser.py
│   ├── acare_dialogue/
│   │   ├── dialogue_node.py
│   │   ├── assistant_agent.py
│   │   └── nodes/
│   │       ├── clarity_check.py
│   │       ├── clarification.py
│   │       ├── context_resolver.py
│   │       ├── interruption_handler.py
│   │       └── dialogue_manager.py
│   ├── acare_auth/
│   │   ├── auth_node.py
│   │   ├── enrol.py
│   │   ├── verify_voice.py    # ECAPA-TDNN
│   │   ├── verify_face.py     # InsightFace buffalo_sc
│   │   ├── face_detect.py     # MediaPipe FaceDetection (passive)
│   │   └── embeddings/        # users.db (encrypted)
│   ├── acare_vision/
│   │   ├── vision_node.py
│   │   ├── yolo_infer.py      # ONNX INT8 (not TFLite)
│   │   ├── nbv_search.py
│   │   ├── fake_detector.py
│   │   ├── localiser.py
│   │   └── hand_tracker.py
│   ├── acare_planner/
│   │   ├── planner_node.py
│   │   ├── state_machine.py
│   │   ├── state_manager.py
│   │   ├── tool_registry.py
│   │   ├── handover.py
│   │   └── ik_solver.py
│   ├── acare_safety/
│   │   ├── safety_node.py
│   │   ├── lidar_monitor.py
│   │   └── sensor_monitor.py
│   ├── acare_embedded_interface/
│   │   ├── interface_node.cpp
│   │   ├── CMakeLists.txt
│   │   └── package.xml
│   ├── acare_logging/
│   │   └── log_node.py
│   ├── acare_admin/
│   │   └── admin_cli.py
│   └── acare_bringup/
│       ├── launch/
│       │   └── acare.launch.py
│       ├── config/
│       │   ├── system.yaml
│       │   ├── thresholds.yaml
│       │   └── probability_map.yaml
│       └── supervisor.py
├── logs/
│   └── acare_logs.db
└── install/
```

### Key .msg definitions

```
# RobotState.msg
string state
string active_user_id

# StateTransition.msg
string target_state
string reason

# VisionSearchRequest.msg
string tool

# VisionResult.msg
bool found
string tool
float32 x
float32 y
float32 z
float32 confidence
string zone

# HandStatus.msg
bool hand_detected
bool is_open
bool palm_up
float32 x
float32 y
float32 z
float32 confidence

# ArmCommand.msg
string command
float32[] joint_angles
float32 velocity_scale
float32 accel_limit
bool blocking

# GripperCommand.msg
string command
float32 force_target

# MotionFeedback.msg
bool success
string phase
string error
float32[] joint_positions
float32[] joint_velocities
float32[] joint_currents
float32[] temperatures
float32 gripper_force
float32 imu_roll
float32 imu_pitch
float32 imu_yaw

# SafetyAlert.msg
string severity
string reason
string source

# LogEvent.msg
string event_type
string user_id
string tool
string state
string description
int64 timestamp
int64 voice_e2e_ms
int64 vision_search_ms
int64 motion_ms
int64 total_task_ms
string safety_severity

# EmergencySignal.msg
string reason
string source

# EnrolStaff.srv
string name
string role
---
bool success
string staff_id
string message
```

### acare_msgs/CMakeLists.txt (key parts)

```cmake
cmake_minimum_required(VERSION 3.8)
project(acare_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotState.msg"
  "msg/StateTransition.msg"
  "msg/Intent.msg"
  "msg/ValidatedIntent.msg"
  "msg/SafetyAlert.msg"
  "msg/HandStatus.msg"
  "msg/AuthResult.msg"
  "msg/VisionResult.msg"
  "msg/VisionSearchRequest.msg"
  "msg/ArmCommand.msg"
  "msg/GripperCommand.msg"
  "msg/MotionFeedback.msg"
  "msg/LogEvent.msg"
  "msg/EmergencySignal.msg"
  "srv/EnrolStaff.srv"
)

ament_package()
```

---

## 6. Full Dependencies

### requirements.txt (Pi 5 — Python packages)

```
# Inference
onnxruntime>=1.18.0          # ONNX Runtime for YOLOv11 — NOT tflite-runtime

# Vision / Perception
opencv-python-headless>=4.9  # headless (no GUI) for Pi
mediapipe>=0.10.14            # Hands + FaceDetection
insightface>=0.7.3            # buffalo_sc: ArcFace face verification

# Speaker verification
speechbrain>=1.0.0            # ECAPA-TDNN (spkrec-ecapa-voxceleb)
torch>=2.2.0                  # CPU-only — required by SpeechBrain

# VAD
silero-vad                    # Silero VAD v5

# STT
deepgram-sdk>=3.5.0           # Deepgram Nova-2 streaming

# Intent parsing + conversational AI
groq>=0.9.0                   # Groq API (llama3-8b-8192)
langchain-groq>=0.1.0
langgraph>=0.2.0

# TTS — Microsoft Edge TTS (replaces Google Cloud TTS)
edge-tts>=7.2.7               # pip install edge-tts — FREE, no API key
pyttsx3>=2.90                 # ESTOP/safety TTS — offline, zero latency
# Kokoro ONNX for offline TTS fallback (install separately — not on PyPI mainstream)

# Utilities
numpy>=1.26
scipy>=1.12
PyYAML>=6.0
cryptography>=42.0            # Fernet encryption for users.db and API keys
pyserial>=3.5                 # UART to Teensy

# ROS2 Python deps (installed via apt, not pip)
# sudo apt install python3-rclpy python3-std-msgs ros-jazzy-sensor-msgs

# C++ node deps (install via apt)
# sudo apt install ros-jazzy-serial-driver libserial-dev nlohmann-json3-dev

# Admin CLI
argparse                      # stdlib — no install needed

# Export (development machine only — NOT on Pi)
# pip install ultralytics      # only for ONNX export on training machine
```

### API Keys Required

| Service | Free Tier | How to Set |
|---|---|---|
| Deepgram Nova-2 | 12,000 min/year free | `python admin.py set-api-key --service deepgram --key YOUR_KEY` |
| Groq | Generous free tier (rate limited) | `python admin.py set-api-key --service groq --key YOUR_KEY` |
| Microsoft Edge TTS | Completely free, no key | No setup needed — `edge-tts` uses Edge's public endpoint |

### ROS2 Packages (apt)

```bash
sudo apt install ros-jazzy-rclpy ros-jazzy-std-msgs ros-jazzy-sensor-msgs \
     ros-jazzy-geometry-msgs ros-jazzy-launch ros-jazzy-launch-ros
# YDLIDAR T-mini Plus driver:
git clone -b humble https://github.com/YDLIDAR/ydlidar_ros2_driver.git
# HP60C: use YDLIDAR HP60C SDK Python bindings — write custom ROS2 wrapper node
```

---

*End of ACARE Implementation Guide.*  
*Hardware parameters marked `[FILL_AFTER_ASSEMBLY]` must be obtained from the hardware team before `ik_solver.py` and `planner_node.py` can be finalised.*

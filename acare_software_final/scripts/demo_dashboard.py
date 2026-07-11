"""
ACARE Final Demo Dashboard — Multi-screen with camera PIP
Optimized for Waveshare 5" 800×480, touch navigation.

Run:  python3 scripts/demo_dashboard.py
Open: http://localhost:8000
"""

import asyncio
import json
import logging
import os
import time
import threading
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ── Config ──────────────────────────────────────────────────────────────
CAMERA_ID = int(os.getenv("ACARE_CAMERA", 0))
MJPEG_QUALITY = int(os.getenv("MJPEG_QUALITY", "65"))
MJPEG_FPS = int(os.getenv("MJPEG_FPS", "10"))
STATE_POLL_INTERVAL = 0.25

# ── Shared state ────────────────────────────────────────────────────────
state_lock = threading.Lock()
shared_state = {
    "system_state": "OFFLINE",
    "user": "",
    "auth_face_score": 0.0,
    "auth_voice_score": 0.0,
    "auth_status": "",
    "intent_tool": "",
    "intent_action": "",
    "intent_confidence": 0.0,
    "intent_status": "",
    "safety_layers": {f"L{i}": "✓" for i in range(7)},
    "ik_solution": [0.0] * 6,
    "phase": "",
    "transcript": "",
    "logs": [],
    "fps": 0,
    "detections": [],
    "estop_active": False,
    # Per-screen detail data
    "voice_vad": False,
    "voice_asr_latency": 0,
    "voice_intent_latency": 0,
    "voice_tts": "",
    "auth_history": [],
    "vision_tools": [],
    "vision_nbv_zone": "",
    "vision_nbv_prob": 0.0,
    "planner_action": "",
    "planner_zone": "",
    "planner_budget": 0,
    "safety_thresholds": [],
    "safety_triggers": [],
    "node_health": {},
}

MAX_LOG_LINES = 20


def add_log(source: str, message: str):
    ts = datetime.now().strftime("%H:%M:%S")
    with state_lock:
        shared_state["logs"].append({"ts": ts, "source": source, "msg": message})
        if len(shared_state["logs"]) > MAX_LOG_LINES:
            shared_state["logs"] = shared_state["logs"][-MAX_LOG_LINES:]


# ── Camera / detection ──────────────────────────────────────────────────
camera: Optional[cv2.VideoCapture] = None
_frame = None
_frame_lock = threading.Lock()
_frame_ready = threading.Event()

yolo_model = None
yolo_available = False
FONT = cv2.FONT_HERSHEY_SIMPLEX

DETECTION_COLORS = {
    "cream": (255, 255, 255), "scissors": (0, 255, 0), "forceps": (255, 0, 0),
    "thermometer": (0, 255, 255), "oximeter": (255, 255, 0), "plaster": (255, 0, 255),
    "face": (0, 200, 255),
}


def _load_yolo():
    global yolo_model, yolo_available
    try:
        import sys
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        from acare_vision.yolo_infer import YOLO26ONNX
        from acare_bringup.paths import MODEL_DIR
        model_path = str(MODEL_DIR / 'acare_v26.onnx')
        yolo_model = YOLO26ONNX(model_path)
        yolo_available = True
        add_log("YOLO", f"Loaded YOLO26 ONNX ({yolo_model.num_classes} classes)")
    except Exception as e:
        yolo_available = False
        import traceback
        traceback.print_exc()
        add_log("YOLO", f"Failed to load: {e}")


def _detect_objects(frame: np.ndarray):
    dets = []
    if yolo_available and yolo_model is not None:
        try:
            results = yolo_model.infer(frame)
            for d in results:
                x1, y1, x2, y2 = d["bbox"]
                label = d["class_name"]
                conf = d["confidence"]
                dets.append({"label": label, "confidence": round(conf, 3),
                             "bbox": [int(x1), int(y1), int(x2), int(y2)]})
                color = DETECTION_COLORS.get(label, (0, 255, 0))
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                text = f"{label} {conf:.2f}"
                (tw, th), _ = cv2.getTextSize(text, FONT, 0.5, 2)
                cv2.rectangle(frame, (int(x1), int(y1) - th - 6),
                              (int(x1) + tw + 6, int(y1)), color, -1)
                cv2.putText(frame, text, (int(x1) + 3, int(y1) - 3),
                            FONT, 0.5, (0, 0, 0), 2)
                # Show coordinates below bbox
                coord_text = f"({int(x1)},{int(y1)}) ({int(x2)},{int(y2)})"
                cv2.putText(frame, coord_text, (int(x1), int(y2) + 14),
                            FONT, 0.4, color, 1)
        except Exception:
            pass
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 255), 2)
            cv2.putText(frame, "Face", (x, y - 10), FONT, 0.6, (0, 200, 255), 2)
            dets.append({"label": "face", "confidence": 0.9, "bbox": [int(x), int(y), int(x + w), int(y + h)]})
    return dets, frame


def camera_loop():
    global camera, _frame
    
    # Check if running on a Raspberry Pi
    is_pi = False
    if os.path.exists('/proc/device-tree/model'):
        try:
            with open('/proc/device-tree/model', 'r') as f:
                if 'Raspberry Pi' in f.read():
                    is_pi = True
        except Exception:
            pass

    # Try ROS2 subscription first
    ros2_success = False
    try:
        import rclpy
        from sensor_msgs.msg import Image as ROSImage
        
        if not rclpy.ok():
            rclpy.init()
            
        node = rclpy.create_node('dashboard_cam_subscriber')
        frames_received = 0
        active_source = None
        
        def on_image(msg: ROSImage, source_name: str):
            nonlocal frames_received, active_source
            frames_received += 1
            active_source = source_name
            try:
                channels = 3
                if msg.encoding == 'mono8':
                    channels = 1
                arr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, channels)
                if msg.encoding == 'rgb8':
                    arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
                elif msg.encoding == 'mono8':
                    arr = cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
                
                dets, annotated = _detect_objects(arr)
                with state_lock:
                    shared_state["detections"] = dets
                    if dets:
                        shared_state["vision_tools"] = [{"label": d["label"], "conf": d["confidence"]} for d in dets]
                with _frame_lock:
                    global _frame
                    _frame = annotated
                _frame_ready.set()
            except Exception:
                pass
                
        # Subscribe to both potential namespaces for robustness
        node.create_subscription(ROSImage, '/ascamera_hp60c/camera_publisher/rgb0/image', lambda m: on_image(m, "hp60c"), 10)
        node.create_subscription(ROSImage, '/ascamera_hp60cn/camera_publisher/rgb0/image', lambda m: on_image(m, "hp60cn"), 10)
        
        # Check for active frames for 3 seconds
        start_t = time.time()
        while time.time() - start_t < 3.0:
            rclpy.spin_once(node, timeout_sec=0.1)
            if frames_received > 0:
                ros2_success = True
                break
                
        if ros2_success:
            add_log("CAM", f"Active ROS2 stream detected: {active_source}")
            fps_c, fps_t = 0, time.time()
            while rclpy.ok():
                last_count = frames_received
                rclpy.spin_once(node, timeout_sec=0.1)
                if frames_received > last_count:
                    fps_c += (frames_received - last_count)
                if time.time() - fps_t >= 1.0:
                    with state_lock:
                        shared_state["fps"] = fps_c
                    fps_c, fps_t = 0, time.time()
            return
        else:
            if is_pi:
                add_log("CAM", "ROS2 topics silent. Running on Pi: OpenCV fallback disabled to prevent UVC lock.")
                # Indefinitely spin ROS2 to pick up camera if it starts later
                fps_c, fps_t = 0, time.time()
                while rclpy.ok():
                    last_count = frames_received
                    rclpy.spin_once(node, timeout_sec=0.5)
                    if frames_received > last_count:
                        fps_c += (frames_received - last_count)
                    if time.time() - fps_t >= 1.0:
                        with state_lock:
                            shared_state["fps"] = fps_c
                        fps_c, fps_t = 0, time.time()
                return
            else:
                add_log("CAM", "ROS2 camera topic silent, falling back to OpenCV")
                node.destroy_node()
    except Exception as e:
        if is_pi:
            add_log("CAM", f"ROS2 subscriber error on Pi: {e}")
            return

    # OpenCV fallback (index 0)
    add_log("CAM", f"Opening OpenCV camera {CAMERA_ID}")
    camera = cv2.VideoCapture(CAMERA_ID)
    if not camera.isOpened():
        add_log("CAM", "No camera found")
        return
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FPS, 30)
    fps_c, fps_t = 0, time.time()
    while True:
        ret, frame = camera.read()
        if not ret:
            time.sleep(0.01); continue
        frame = cv2.flip(frame, 1)
        dets, annotated = _detect_objects(frame)
        with state_lock:
            shared_state["detections"] = dets
            if dets:
                shared_state["vision_tools"] = [{"label": d["label"], "conf": d["confidence"]} for d in dets]
        with _frame_lock:
            _frame = annotated
        _frame_ready.set()
        fps_c += 1
        if time.time() - fps_t >= 1.0:
            with state_lock: shared_state["fps"] = fps_c
            fps_c, fps_t = 0, time.time()


def _get_jpeg() -> Optional[bytes]:
    with _frame_lock:
        if _frame is None:
            # Generate a temporary placeholder frame so the stream remains active during startup
            placeholder = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(placeholder, "Camera starting...", (180, 240), FONT, 0.8, (255, 255, 255), 2)
            ret, jpeg = cv2.imencode(".jpg", placeholder, [cv2.IMWRITE_JPEG_QUALITY, MJPEG_QUALITY])
            return jpeg.tobytes() if ret else None
        ret, jpeg = cv2.imencode(".jpg", _frame, [cv2.IMWRITE_JPEG_QUALITY, MJPEG_QUALITY])
        return jpeg.tobytes() if ret else None


async def mjpeg_generator():
    while True:
        jpeg = _get_jpeg()
        if jpeg is None:
            await asyncio.sleep(0.05); continue
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n"
        await asyncio.sleep(1.0 / MJPEG_FPS)


# ── Demo scenario ───────────────────────────────────────────────────────
class DemoScenario:
    def __init__(self):
        self._step = 0
        self._timer = time.monotonic()
        self._t = 3.0

    def tick(self):
        if time.monotonic() - self._timer < self._t: return
        self._timer = time.monotonic()
        self._step += 1
        with state_lock:
            s = shared_state
            if self._step == 1:
                s["system_state"] = "LOGGED_OUT"; s["auth_status"] = "Scanning..."
                add_log("SYS", "System ready")
            elif self._step == 2:
                s["system_state"] = "STANDBY"; s["user"] = "Dr. Demo"
                s["auth_face_score"] = 0.82; s["auth_voice_score"] = 0.91
                s["auth_status"] = "Authenticated"
                s["auth_history"] = [
                    {"t": "Face detect", "v": "0.82", "p": "pass"},
                    {"t": "Voice match", "v": "0.91", "p": "pass"},
                    {"t": "Login", "v": "Dr. Demo", "p": "pass"},
                ]
                add_log("AUTH", "Face 0.82  Voice 0.91")
            elif self._step == 3:
                s["transcript"] = "fetch scissors"
                s["voice_vad"] = True; s["voice_asr_latency"] = 340
                s["system_state"] = "PROCESSING"
                add_log("VAD", "Speech detected"); add_log("ASR", "\"fetch scissors\"")
            elif self._step == 4:
                s["intent_tool"] = "scissors"; s["intent_action"] = "fetch"
                s["intent_confidence"] = 0.94; s["intent_status"] = "parsed"
                s["voice_intent_latency"] = 280; s["voice_tts"] = "Fetching scissors"
                add_log("INT", "tool=scissors conf=0.94")
            elif self._step == 5:
                s["system_state"] = "EXECUTING"; s["phase"] = "SEARCH"
                s["planner_zone"] = "A"; s["planner_budget"] = 180
                s["vision_nbv_zone"] = "Zone A"; s["vision_nbv_prob"] = 0.72
                add_log("PLAN", "SEARCH — zone A")
            elif self._step == 6:
                s["phase"] = "GRASPING"
                s["ik_solution"] = [-0.32, 0.87, -1.24, 0.15, 0.42, -0.08]
                s["intent_status"] = "IK solved"
                s["planner_action"] = "arm_move(GRASP_POINT)"
                s["planner_zone"] = "A✓"
                s["vision_tools"] = [{"label": "scissors", "conf": 0.94}, {"label": "forceps", "conf": 0.12}]
                add_log("IK", "6 joint angles")
            elif self._step == 7:
                s["safety_layers"] = {f"L{i}": "✓" for i in range(7)}
                s["safety_thresholds"] = [
                    ("LiDAR", "0.40m", "0.40m", "OK"),
                    ("Current", "8.0A", "6.2A", "OK"),
                    ("Temp", "75°C", "42°C", "OK"),
                    ("Force", "50N", "3.2N", "OK"),
                ]
                add_log("SFT", "L0-L6 ALL PASS")
            elif self._step == 8:
                s["phase"] = "HANDOVER"; s["system_state"] = "HANDOVER"
                s["planner_action"] = "handover_present()"
                add_log("PLAN", "HANDOVER phase")
            elif self._step == 9:
                s["system_state"] = "STANDBY"; s["phase"] = "DONE"
                s["intent_status"] = "completed"
                s["node_health"] = {
                    "safety": "✓", "planner": "✓", "vision": "✓",
                    "voice": "✓", "auth": "✓", "supervisor": "✓",
                }
                add_log("SYS", "Task complete")
            elif self._step >= 12:
                self._step = 0
                for k in ("intent_tool","intent_action","transcript","phase","planner_action",
                          "planner_zone","vision_nbv_zone","voice_tts"):
                    s[k] = ""
                s["intent_confidence"] = 0; s["intent_status"] = ""
                s["auth_face_score"] = 0; s["auth_voice_score"] = 0
                s["auth_status"] = ""; s["user"] = ""
                s["ik_solution"] = [0.0]*6; s["vision_nbv_prob"] = 0
                s["voice_vad"] = False; s["voice_asr_latency"] = 0; s["voice_intent_latency"] = 0
                s["safety_thresholds"] = []
                s["vision_tools"] = []
                s["auth_history"] = []
                s["safety_layers"] = {f"L{i}": "✓" for i in range(7)}
                s["system_state"] = "LOGGED_OUT"; s["logs"] = []
                s["node_health"] = {n: "✓" for n in ["safety","planner","vision","voice","auth","supervisor","dialogue","logging"]}
                add_log("SYS", "Demo restart")


demo_scenario = DemoScenario()

# ── FastAPI app ──────────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=800,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>ACARE Demo</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:100%;height:100vh;overflow:hidden;background:#0a0e17;color:#e0e6f0;font-family:'Segoe UI',system-ui,sans-serif;-webkit-user-select:none;user-select:none}

/* Main container */
#app{position:relative;width:100%;height:100vh;display:flex;flex-direction:column;overflow:hidden}

/* ═══ Top bar ═══ */
#topbar{height:32px;background:#0d1520;border-bottom:1px solid #1e3a5f;display:flex;align-items:center;padding:0 8px;gap:6px;font-size:11px;flex-shrink:0}
#topbar .logo{font-weight:700;font-size:13px;background:linear-gradient(90deg,#4fc3f7,#00e676);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
#topbar .sep{color:#2a3a4a}
#st-badge{padding:1px 8px;border-radius:8px;font-size:10px;font-weight:600}
.st-online{background:#00e67622;color:#00e676;border:1px solid #00e67644}
.st-busy{background:#ffd54f22;color:#ffd54f;border:1px solid #ffd54f44}
.st-estop{background:#ff174422;color:#ff1744;border:1px solid #ff174444}
#topbar .hl{color:#4fc3f7;font-weight:600}
#topbar .lb{color:#5a7a9a}

/* ═══ Main content ═══ */
#main{height:calc(100vh - 70px);position:relative;overflow:hidden}

/* Screens: all position:absolute, toggle via opacity/pointer-events */
.screen{position:absolute;top:0;left:0;width:100%;height:100%;overflow-y:auto;overflow-x:hidden;padding:6px 8px;opacity:0;pointer-events:none;transition:opacity 0.15s}
.screen.active{opacity:1;pointer-events:auto}
.screen::-webkit-scrollbar{width:3px}
.screen::-webkit-scrollbar-thumb{background:#1e3a5f;border-radius:2px}

/* ═══ Camera PIP ═══ */
#camera-pip{position:absolute;top:4px;right:4px;width:140px;height:105px;border-radius:6px;overflow:hidden;border:1px solid #1e3a5f;z-index:20;background:#000;cursor:pointer}
#camera-pip img{width:100%;height:100%;object-fit:cover}
#camera-pip .label{position:absolute;bottom:0;left:0;right:0;background:rgba(0,0,0,0.6);font-size:7px;text-align:center;padding:1px;color:#5a7a9a}
#camera-pip-full{display:none;position:absolute;top:0;left:0;width:100%;height:100%;z-index:25;background:#000}
#camera-pip-full img{width:100%;height:100%;object-fit:contain}
#camera-pip-full .close{position:absolute;top:8px;right:8px;background:rgba(0,0,0,0.6);color:#fff;border:none;border-radius:4px;padding:4px 12px;font-size:14px;cursor:pointer;z-index:26}

/* ═══ Bottom nav ═══ */
#navbar{height:38px;background:#0d1520;border-top:1px solid #1e3a5f;display:flex;align-items:stretch;flex-shrink:0}
.nav-btn{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:9px;color:#5a7a9a;border:none;background:transparent;cursor:pointer;padding:2px 0;border-right:1px solid #0a1018;transition:0.15s;gap:1px}
.nav-btn:last-child{border-right:none}
.nav-btn .icon{font-size:14px;line-height:1}
.nav-btn.active{color:#4fc3f7;background:#111d2e}
.nav-btn:active{background:#1a2d44}

/* ═══ Card components ═══ */
.card{background:#111d2e;border:1px solid #1a2d44;border-radius:6px;padding:6px 8px;margin-bottom:5px}
.card-title{font-size:9px;text-transform:uppercase;letter-spacing:0.8px;color:#5a7a9a;margin-bottom:4px}
.row{display:flex;justify-content:space-between;align-items:center;padding:2px 0;font-size:11px}
.row .l{color:#8899aa}
.row .r{color:#e0e6f0;font-weight:500}
.big-val{font-size:28px;font-weight:700}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:4px}
.bar-bg{height:6px;border-radius:3px;background:#0a1525;overflow:hidden;margin-top:3px}
.bar-fill{height:100%;border-radius:3px;transition:width 0.3s}
.green{color:#00e676}
.yellow{color:#ffd54f}
.red{color:#ff1744}
.blue{color:#4fc3f7}
.grey{color:#5a7a9a}
.tag{display:inline-block;padding:1px 6px;border-radius:3px;font-size:9px;margin:1px}
.tag-green{background:#00e67622;color:#00e676}
.tag-red{background:#ff174422;color:#ff1744}
.tag-blue{background:#4fc3f722;color:#4fc3f7}
.tag-yellow{background:#ffd54f22;color:#ffd54f}
.mono{font-family:'Cascadia Code','Fira Code',monospace}
.mt-1{margin-top:4px}

/* Overview screen specific */
#scr-overview .big{font-size:16px;font-weight:600;margin-bottom:2px}
#scr-overview .sub{font-size:10px;color:#5a7a9a}
</style>
</head>
<body>
<div id="app">
  <!-- ═══ Top bar ═══ -->
  <div id="topbar">
    <span class="logo">⚡ACARE</span>
    <span class="sep">|</span>
    <span id="st-badge" class="st-online">OFFLINE</span>
    <span class="sep">|</span>
    <span class="lb">User:</span><span class="hl" id="tb-user">--</span>
    <span class="sep">|</span>
    <span class="lb">Face:</span><span class="hl" id="tb-face">--</span>
    <span class="sep">|</span>
    <span class="lb">Voice:</span><span class="hl" id="tb-voice">--</span>
    <span class="sep">|</span>
    <span class="lb">FPS:</span><span class="hl" id="tb-fps">--</span>
    <span style="flex:1"></span>
    <span class="lb" id="tb-det" style="font-size:9px"></span>
    <button onclick="sendCommand('estop')" style="padding:2px 8px;border:1px solid #ff174466;background:#ff174422;color:#ff1744;border-radius:4px;font-size:10px;cursor:pointer;margin:0 2px">✕ESTOP</button>
    <button onclick="sendCommand('reset')" style="padding:2px 8px;border:1px solid #00e67644;background:#00e67622;color:#00e676;border-radius:4px;font-size:10px;cursor:pointer;margin:0 2px">↺RESET</button>
    <button onclick="toggleFullscreen()" style="padding:2px 8px;border:1px solid rgba(79,195,247,0.3);background:rgba(79,195,247,0.1);color:#4fc3f7;border-radius:4px;font-size:10px;cursor:pointer;margin:0 2px">⛶FULL</button>
  </div>

  <!-- ═══ Camera PIP (always visible) ═══ -->
  <div id="camera-pip" onclick="toggleCamFull()">
    <img id="cam-thumb" src="/video_feed" alt="cam">
    <div class="label">● LIVE</div>
  </div>
  <div id="camera-pip-full" onclick="toggleCamFull()">
    <img id="cam-full" src="/video_feed" alt="cam">
    <button class="close" onclick="event.stopPropagation();toggleCamFull()">✕</button>
  </div>

  <!-- ═══ Main content: 8 screens ═══ -->
  <div id="main">

  <!-- SCREEN 0: OVERVIEW -->
  <div class="screen active" id="scr-overview">
    <div class="card">
      <div class="card-title">Live Camera</div>
      <div style="display:flex;gap:8px;align-items:center">
        <img src="/video_feed" style="width:100%;border-radius:6px;max-height:200px;object-fit:cover" alt="feed">
      </div>
    </div>
    <div class="card">
      <div class="card-title">Current Intent</div>
      <div class="big" id="ov-tool">--</div>
      <div class="row" style="margin-top:4px"><span class="l">Confidence</span><span class="r blue" id="ov-conf">--</span></div>
      <div class="row"><span class="l">Action</span><span class="r" id="ov-action">--</span></div>
    </div>
    <div class="card">
      <div class="card-title">Voice Transcript</div>
      <div style="font-size:14px;font-weight:500;padding:4px 0" id="ov-transcript">--</div>
    </div>
    <div class="card">
      <div class="card-title">Detections</div>
      <div class="row"><span class="l">Objects</span><span class="r blue" id="ov-dets">0</span></div>
    </div>
  </div>

  <!-- SCREEN 1: VOICE -->
  <div class="screen" id="scr-voice">
    <div class="card">
      <div class="card-title">Voice Pipeline</div>
      <div class="row"><span class="l">VAD</span><span class="r" id="vo-vad">Inactive</span></div>
      <div class="row"><span class="l">ASR Latency</span><span class="r" id="vo-asr">--</span></div>
      <div class="row"><span class="l">Intent Parse</span><span class="r" id="vo-intent-lat">--</span></div>
      <div class="row"><span class="l">TTS</span><span class="r" id="vo-tts">--</span></div>
    </div>
    <div class="card">
      <div class="card-title">Transcript</div>
      <div style="font-size:16px;font-weight:500;padding:4px 0" id="vo-transcript">--</div>
    </div>
    <div class="card">
      <div class="card-title">Parsed Intent</div>
      <div class="row"><span class="l">Tool</span><span class="r blue" id="vo-tool">--</span></div>
      <div class="row"><span class="l">Action</span><span class="r" id="vo-action">--</span></div>
      <div class="row"><span class="l">Confidence</span><span class="r" id="vo-conf">--</span></div>
    </div>
  </div>

  <!-- SCREEN 3: VISION -->
  <div class="screen" id="scr-vision">
    <div class="card">
      <div class="card-title">Object Detection</div>
      <div class="row"><span class="l">Model</span><span class="r">YOLO26 ONNX</span></div>
      <div class="row"><span class="l">FPS</span><span class="r blue" id="vi-fps">--</span></div>
      <div class="row"><span class="l">Detections</span><span class="r" id="vi-count">0</span></div>
    </div>
    <div class="card">
      <div class="card-title">Detected Objects</div>
      <div id="vi-list" style="font-size:11px;max-height:120px;overflow-y:auto"></div>
    </div>
    <div class="card">
      <div class="card-title">NBV Search</div>
      <div class="row"><span class="l">Zone</span><span class="r blue" id="vi-zone">--</span></div>
      <div class="row"><span class="l">Probability</span><span class="r" id="vi-prob">--</span></div>
    </div>
  </div>

  <!-- SCREEN 4: CAMERA FULL -->
  <div class="screen" id="scr-cam">
    <div style="width:100%;height:100%;background:#000;display:flex;align-items:center;justify-content:center">
      <img src="/video_feed" style="width:100%;height:100%;object-fit:contain" alt="camera">
    </div>
  </div>
  </div>

  <!-- ═══ Bottom nav ═══ -->
  <div id="navbar">
    <button class="nav-btn active" data-scr="0"><span class="icon">◉</span>Overview</button>
    <button class="nav-btn" data-scr="1"><span class="icon">♪</span>Voice</button>
    <button class="nav-btn" data-scr="2"><span class="icon">◈</span>Vision</button>
    <button class="nav-btn" data-scr="3"><span class="icon">▣</span>Camera</button>
  </div>
</div>

<script>
// ── Screen navigation ──
const screens = document.querySelectorAll('.screen');
const navBtns = document.querySelectorAll('.nav-btn');

// Touch control functions
function sendCommand(cmd) {
  fetch('/command/' + cmd).then(r => r.json()).then(d => console.log(d));
}
function toggleFullscreen() {
  if (!document.fullscreenElement) { document.documentElement.requestFullscreen(); }
  else { document.exitFullscreen(); }
}

navBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const idx = parseInt(btn.dataset.scr);
    screens.forEach(s => s.classList.remove('active'));
    navBtns.forEach(b => b.classList.remove('active'));
    screens[idx].classList.add('active');
    btn.classList.add('active');
    // Hide PIP on camera full-screen
    document.getElementById('camera-pip').style.display = (idx === 7) ? 'none' : 'block';
  });
});

// ── Camera PIP toggle ──
function toggleCamFull() {
  const pip = document.getElementById('camera-pip');
  const full = document.getElementById('camera-pip-full');
  if (full.style.display === 'block') {
    full.style.display = 'none';
    pip.style.display = 'block';
  } else {
    full.style.display = 'block';
    pip.style.display = 'none';
  }
}

// ── WebSocket ──
const ws = new WebSocket((location.protocol==='https'?'wss:':'ws:')+'//'+location.host+'/ws');
ws.onmessage = e => { try { update(JSON.parse(e.data)); } catch(err) {} };
ws.onclose = () => setTimeout(() => window.location.reload(), 3000);

// ── Phase map ──
const PHASE_MAP = {'IDLE':0,'SEARCH':1,'SCAN':1,'GRASPING':2,'GRASP':2,'HANDOVER':3,'HAND':3,'DONE':4,'COMPLETE':4};

function update(s) {
  // State badge
  const badge = document.getElementById('st-badge');
  badge.textContent = s.system_state || 'OFFLINE';
  badge.className = 'st-' + ((s.system_state==='ESTOP'||s.system_state==='OFFLINE')?'estop':
    (s.system_state==='STANDBY'||s.system_state==='LISTENING')?'online':'busy');

  // Top bar
  document.getElementById('tb-user').textContent = s.user||'--';
  document.getElementById('tb-face').textContent = s.auth_face_score ? s.auth_face_score.toFixed(2) : '--';
  document.getElementById('tb-voice').textContent = s.auth_voice_score ? s.auth_voice_score.toFixed(2) : '--';
  document.getElementById('tb-fps').textContent = s.fps||'--';
  document.getElementById('tb-det').textContent = s.detections ? s.detections.length+' det' : '';

  // ── Screen 0: Overview ──
  doc('ov-tool').textContent = s.intent_tool || '--';
  doc('ov-conf').textContent = s.intent_confidence ? (s.intent_confidence*100).toFixed(0)+'%' : '--';
  doc('ov-action').textContent = s.intent_action || '--';
  doc('ov-transcript').textContent = s.transcript ? '"'+s.transcript+'"' : 'Waiting...';
  doc('ov-dets').textContent = s.detections ? s.detections.length : 0;

  // ── Screen 1: Voice ──
  doc('vo-vad').textContent = s.voice_vad ? '🔴 Active' : '○ Inactive';
  doc('vo-vad').style.color = s.voice_vad ? '#ff1744' : '#5a7a9a';
  doc('vo-asr').textContent = s.voice_asr_latency ? s.voice_asr_latency+'ms' : '--';
  doc('vo-intent-lat').textContent = s.voice_intent_latency ? s.voice_intent_latency+'ms' : '--';
  doc('vo-tts').textContent = s.voice_tts||'--';
  doc('vo-transcript').textContent = s.transcript ? '"'+s.transcript+'"' : '--';
  doc('vo-tool').textContent = s.intent_tool||'--';
  doc('vo-action').textContent = s.intent_action||'--';
  doc('vo-conf').textContent = s.intent_confidence ? (s.intent_confidence*100).toFixed(0)+'%' : '--';

  // ── Screen 2: Auth ──
  doc('au-user').textContent = s.user||'--';
  const fs = s.auth_face_score||0;
  const vs = s.auth_voice_score||0;
  doc('au-face').textContent = fs ? fs.toFixed(2)+(fs>=0.78?' ✓':'') : '--';
  doc('au-voice').textContent = vs ? vs.toFixed(2)+(vs>=0.85?' ✓':'') : '--';
  doc('au-face-bar').style.width = (fs*100)+'%';
  doc('au-voice-bar').style.width = (vs*100)+'%';
  doc('au-status').textContent = s.auth_status||'--';
  // Auth timeline
  const tl = doc('au-timeline');
  if (s.auth_history && s.auth_history.length) {
    tl.innerHTML = s.auth_history.map(h =>
      '<div style="display:flex;gap:6px;padding:2px 0"><span style="color:#5a7a9a">▸</span>'+
      '<span style="color:#8899aa">'+h.t+'</span>'+
      '<span style="flex:1"></span>'+
      '<span class="'+(h.p==='pass'?'green':'red')+'">'+h.v+'</span></div>'
    ).join('');
  } else { tl.innerHTML = '<span class="grey">No auth history</span>'; }

  // ── Screen 3: Vision ──
  doc('vi-fps').textContent = s.fps||'--';
  doc('vi-count').textContent = s.detections?s.detections.length:'0';
  const viList = doc('vi-list');
  const tools = s.vision_tools || s.detections || [];
  if (tools.length) {
    viList.innerHTML = tools.map(d =>
      '<div style="display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid #0a1525">'+
      '<span class="blue">'+d.label+'</span><span>'+(d.conf?d.conf.toFixed(2):'--')+'</span></div>'
    ).join('');
  } else {
    viList.innerHTML = '<span class="grey">No detections</span>';
  }
  doc('vi-zone').textContent = s.vision_nbv_zone||'--';
  doc('vi-prob').textContent = s.vision_nbv_prob ? (s.vision_nbv_prob*100).toFixed(0)+'%' : '--';

  // ── Screen 4: Planner ──
  doc('pl-phase').textContent = s.phase||'--';
  doc('pl-action').textContent = s.planner_action||'--';
  doc('pl-zone').textContent = s.planner_zone||'--';
  doc('pl-budget').textContent = s.planner_budget ? s.planner_budget+'s' : '--';
  // Phase progress
  const pidx = PHASE_MAP[s.phase] !== undefined ? PHASE_MAP[s.phase] : -1;
  document.querySelectorAll('.ph-step').forEach(el => {
    const p = parseInt(el.dataset.p);
    el.style.background = p<pidx ? '#00e67633' : p===pidx ? '#4fc3f733' : '#0a1525';
    el.style.color = p<pidx ? '#00e676' : p===pidx ? '#4fc3f7' : '#5a7a9a';
  });
  // IK
  doc('pl-ik').innerHTML = (s.ik_solution && s.ik_solution.some(v=>v!==0))
    ? s.ik_solution.map((v,i)=>'<span class="blue">J'+(i+1)+'</span>: <span class="e0e6f0">'+v.toFixed(3)+'</span>').join(' | ')
    : '<span class="grey">No IK solution</span>';

  // ── Screen 5: Safety ──
  const saGrid = doc('sa-grid');
  if (s.safety_layers) {
    const layerNames = ['L0: ESTOP Gate','L1: Tool Gate','L2: Workspace','L3: Joint Limits','L4: Fail Counter','L5: LLM Budget','L6: Gripper Force'];
    saGrid.innerHTML = Object.entries(s.safety_layers).map(([k,v],i) =>
      '<div style="text-align:center;padding:4px;border-radius:4px;background:'+(v==='✓'?'#00e67611':'#ff174411')+
      ';border:1px solid '+(v==='✓'?'#00e67633':'#ff174433')+'">'+
      '<div style="font-size:11px;font-weight:600;color:'+(v==='✓'?'#00e676':'#ff1744')+'">'+(v==='✓'?'✓':'✕')+'</div>'+
      '<div style="font-size:7px;color:#5a7a9a;margin-top:2px">'+layerNames[i]+'</div></div>'
    ).join('');
  }
  // Thresholds
  const thEl = doc('sa-thresholds');
  if (s.safety_thresholds && s.safety_thresholds.length) {
    thEl.innerHTML = s.safety_thresholds.map(t =>
      '<div style="display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid #0a1525;font-size:10px">'+
      '<span style="color:#8899aa">'+t[0]+'</span>'+
      '<span style="color:#5a7a9a">Limit: '+t[1]+'</span>'+
      '<span style="color:#e0e6f0">Actual: '+t[2]+'</span>'+
      '<span class="green">'+t[3]+'</span></div>'
    ).join('');
  } else {
    thEl.innerHTML = '<span class="grey">Monitor inactive</span>';
  }

  // ── Screen 6: System ──
  const sysNodes = doc('sys-nodes');
  if (s.node_health && Object.keys(s.node_health).length) {
    sysNodes.innerHTML = Object.entries(s.node_health).map(([name,status]) =>
      '<div style="display:flex;justify-content:space-between;padding:2px 4px;background:#0a1525;border-radius:3px">'+
      '<span>'+name+'</span><span class="'+(status==='✓'?'green':'red')+'">'+status+'</span></div>'
    ).join('');
  } else {
    sysNodes.innerHTML = '<span class="grey">No node data</span>';
  }
  // Event log
  const logEl = doc('sys-log');
  if (s.logs && s.logs.length) {
    logEl.innerHTML = s.logs.map(l =>
      '<div><span style="color:#5a7a9a">'+l.ts+'</span> <span style="color:#4fc3f7">['+l.source+']</span> '+l.msg+'</div>'
    ).join('');
  }
}

function doc(id){return document.getElementById(id);}
</script>
</body>
</html>
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=camera_loop, daemon=True).start()
    threading.Thread(target=_load_yolo, daemon=True).start()
    asyncio.create_task(broadcast_state())
    yield


app = FastAPI(title="ACARE Demo", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML


@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(mjpeg_generator(), media_type="multipart/x-mixed-replace; boundary=frame")


@app.get("/state")
async def get_state():
    with state_lock:
        return JSONResponse(dict(shared_state))


@app.get("/command/{cmd}")
async def handle_command(cmd: str):
    with state_lock:
        s = shared_state
        if cmd == "estop":
            s["system_state"] = "ESTOP"
            s["estop_active"] = True
            add_log("SYS", "ESTOP via touch")
        elif cmd == "reset":
            s["system_state"] = "STANDBY"
            s["estop_active"] = False
            add_log("SYS", "Reset via touch")
    return JSONResponse({"status": "ok", "command": cmd})


connected_websockets: set[WebSocket] = set()


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connected_websockets.add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        connected_websockets.discard(ws)


async def broadcast_state():
    while True:
        demo_scenario.tick()
        with state_lock:
            payload = json.dumps(dict(shared_state))
        dead = set()
        for ws in connected_websockets:
            try:
                await ws.send_text(payload)
            except Exception:
                dead.add(ws)
        connected_websockets -= dead
        await asyncio.sleep(STATE_POLL_INTERVAL)


if __name__ == "__main__":
    print("=" * 55)
    print("  ACARE Demo Dashboard")
    print("  800x480 | 8 screens | touch nav")
    print()
    print("  Open http://localhost:8000 on the Waveshare LCD")
    print("  Tap nav buttons to switch screens")
    print("  Tap camera PIP to enlarge")
    print("=" * 55)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")

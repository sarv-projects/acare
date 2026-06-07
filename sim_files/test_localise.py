"""
Live detection + 3D localisation test.
Grabs RGB + depth frame, runs YOLO, then computes 3D position
of each detected object using the HP60C depth data.

Coordinates are in CAMERA frame (not robot frame yet — extrinsics
T_robot_camera is identity until arm is calibrated).

Run on Pi: python3 test_localise.py
"""
import sys
import os
import time

sys.path.insert(0, os.path.expanduser('~/acare_ws/install/lib/python3.12/site-packages'))

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
import numpy as np

MODEL_PATH = os.path.expanduser('~/acare_ws/src/models/acare_v26.onnx')
INTERVAL_S = 3.0


class LocaliseTest(Node):
    def __init__(self):
        super().__init__('localise_test')
        self._rgb = None
        self._depth = None
        self._model = None
        self._localiser = None

        self.create_subscription(Image, '/ascamera_hp60c/camera_publisher/rgb0/image', self._on_rgb, 1)
        self.create_subscription(Image, '/ascamera_hp60c/camera_publisher/depth0/image_raw', self._on_depth, 1)
        self.create_subscription(CameraInfo, '/ascamera_hp60c/camera_publisher/rgb0/camera_info', self._on_info, 1)

        # Load YOLO
        try:
            from acare_vision.yolo_infer import YOLO26ONNX
            self._model = YOLO26ONNX(MODEL_PATH, conf_thresh=0.60)
            print(f'YOLO loaded. Classes: {self._model.class_names}')
        except Exception as e:
            print(f'YOLO load failed: {e}')

        # Load localiser
        try:
            from acare_vision.localiser import Localiser
            self._localiser = Localiser()
            print(f'Localiser loaded. Calibrated: {self._localiser.is_calibrated()}')
            print(f'  fx={self._localiser.fx:.1f} fy={self._localiser.fy:.1f} cx={self._localiser.cx:.1f} cy={self._localiser.cy:.1f}')
        except Exception as e:
            print(f'Localiser load failed: {e}')

        print(f'\nRunning every {INTERVAL_S}s — Ctrl+C to stop\n')
        self.create_timer(INTERVAL_S, self._run)

    def _on_rgb(self, msg: Image):
        arr = np.frombuffer(msg.data, dtype=np.uint8)
        if msg.encoding == 'bgr8':
            self._rgb = arr.reshape(msg.height, msg.width, 3)
        elif msg.encoding == 'rgb8':
            self._rgb = arr.reshape(msg.height, msg.width, 3)[:, :, ::-1]

    def _on_depth(self, msg: Image):
        arr = np.frombuffer(msg.data, dtype=np.uint16)
        self._depth = arr.reshape(msg.height, msg.width)

    def _on_info(self, msg: CameraInfo):
        if self._localiser and msg.k[0] > 0:
            self._localiser.update_intrinsics(
                fx=msg.k[0], fy=msg.k[4],
                cx=msg.k[2], cy=msg.k[5]
            )

    def _run(self):
        if self._model is None or self._localiser is None:
            return
        if self._rgb is None:
            print('  [waiting for RGB...]')
            return
        if self._depth is None:
            print('  [waiting for depth...]')
            return

        t0 = time.time()
        detections = self._model.infer(self._rgb)
        infer_ms = (time.time() - t0) * 1000

        ts = time.strftime('%H:%M:%S')
        print(f'[{ts}] YOLO {infer_ms:.0f}ms — {len(detections)} detection(s)')

        for d in detections:
            bbox = d['bbox']
            conf = d['confidence']
            name = d['class_name']

            pos = self._localiser.pixel_to_robot(bbox, self._depth)

            if pos is None:
                # Try median depth in a padded region around bbox centre
                x1, y1, x2, y2 = bbox
                cx_b = (x1 + x2) // 2
                cy_b = (y1 + y2) // 2
                pad = 40  # sample 80x80 region around centre
                h, w = self._depth.shape
                x1c = max(0, cx_b - pad); x2c = min(w-1, cx_b + pad)
                y1c = max(0, cy_b - pad); y2c = min(h-1, cy_b + pad)
                region = self._depth[y1c:y2c, x1c:x2c]
                valid = region[(region >= 200) & (region <= 4000)]
                if valid.size > 0:
                    median_depth_mm = float(np.median(valid))
                    u = (x1 + x2) // 2
                    v = (y1 + y2) // 2
                    d_m = median_depth_mm / 1000.0
                    X = (u - self._localiser.cx) * d_m / self._localiser.fx
                    Y = (v - self._localiser.cy) * d_m / self._localiser.fy
                    pos = (X, Y, d_m)
                    depth_note = f'depth={median_depth_mm:.0f}mm (median)'
                else:
                    depth_note = 'depth=invalid'
            else:
                x1, y1, x2, y2 = bbox
                u = (x1 + x2) // 2
                v = (y1 + y2) // 2
                depth_note = f'depth={self._depth[min(v, self._depth.shape[0]-1), min(u, self._depth.shape[1]-1)]}mm'

            if pos:
                x, y, z = pos
                print(f'  {name:20s} conf={conf:.0%}  '
                      f'X={x:+.3f}m  Y={y:+.3f}m  Z={z:.3f}m  '
                      f'({depth_note})')
            else:
                print(f'  {name:20s} conf={conf:.0%}  position=UNKNOWN (no valid depth)')

        print()


def main():
    rclpy.init()
    node = LocaliseTest()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('\nStopped.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

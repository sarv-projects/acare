"""
Continuous live detection — grabs a new frame every 3 seconds
and runs YOLO26 inference. Press Ctrl+C to stop.
Run on Pi: python3 test_detect.py
"""
import sys
import os
import time

sys.path.insert(0, os.path.expanduser('~/acare_ws/install/lib/python3.12/site-packages'))

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np

MODEL_PATH = os.path.expanduser('~/acare_ws/src/models/acare_v26.onnx')
INTERVAL_S = 3.0   # run detection every N seconds


class ContinuousDetect(Node):
    def __init__(self):
        super().__init__('continuous_detect')
        self._latest_frame = None
        self._model = None
        self._last_detect_t = 0.0

        self.create_subscription(
            Image,
            '/ascamera_hp60c/camera_publisher/rgb0/image',
            self._on_image,
            1
        )

        # Load model once
        try:
            from acare_vision.yolo_infer import YOLOv11ONNX
            self._model = YOLOv11ONNX(MODEL_PATH, conf_thresh=0.50)
            print(f'Model loaded. Classes: {self._model.class_names}')
            print(f'Running detection every {INTERVAL_S}s — Ctrl+C to stop\n')
        except Exception as e:
            print(f'Model load failed: {e}')

        self.create_timer(INTERVAL_S, self._detect)

    def _on_image(self, msg: Image):
        arr = np.frombuffer(msg.data, dtype=np.uint8)
        if msg.encoding == 'bgr8':
            self._latest_frame = arr.reshape(msg.height, msg.width, 3)
        elif msg.encoding == 'rgb8':
            self._latest_frame = arr.reshape(msg.height, msg.width, 3)[:, :, ::-1]

    def _detect(self):
        if self._model is None or self._latest_frame is None:
            print('  [waiting for camera...]')
            return

        t0 = time.time()
        detections = self._model.infer(self._latest_frame)
        elapsed_ms = (time.time() - t0) * 1000

        ts = time.strftime('%H:%M:%S')
        print(f'[{ts}] {elapsed_ms:.0f}ms — ', end='')
        if not detections:
            print('nothing detected')
        else:
            for d in detections:
                print(f"{d['class_name']} ({d['confidence']:.0%})", end='  ')
            print()


def main():
    rclpy.init()
    node = ContinuousDetect()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('\nStopped.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

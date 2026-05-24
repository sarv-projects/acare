# acare_vision/hp60c_camera_node.py
# Spec Reference: Section XI (Camera Interface)
#
# Bridges the YDLIDAR ascamera ROS2 node to the rest of the vision pipeline.
# The ascamera node (from YDLIDAR SDK) publishes raw camera data.
# This node subscribes to those topics and exposes a clean capture() interface.
#
# Confirmed working on Pi 5:
#   RGB:   /ascamera_hp60c/camera_publisher/rgb0/image   640x480 bgr8 @ 12.4 Hz
#   Depth: /ascamera_hp60c/camera_publisher/depth0/image_raw  640x480 16UC1 @ 12.4 Hz
#
# To start the camera before running this node:
#   cd ~/acare_ws && ros2 launch ascamera hp60c.launch.py

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image, PointCloud2
import numpy as np
import threading
import time


class HP60CCameraNode(Node):
    """
    Subscribes to the YDLIDAR ascamera ROS2 topics and caches the latest
    RGB and depth frames. Exposes a thread-safe capture() method for use
    by vision_node.py and hand_tracker.py.

    Does NOT open the camera directly — that is handled by the ascamera node
    launched separately via: ros2 launch ascamera hp60c.launch.py
    """

    RGB_TOPIC   = '/ascamera_hp60c/camera_publisher/rgb0/image'
    DEPTH_TOPIC = '/ascamera_hp60c/camera_publisher/depth0/image_raw'
    RGB_INFO_TOPIC = '/ascamera_hp60c/camera_publisher/rgb0/camera_info'
    DEPTH_INFO_TOPIC = '/ascamera_hp60c/camera_publisher/depth0/camera_info'
    POINTS_TOPIC = '/ascamera_hp60c/camera_publisher/depth0/points'

    def __init__(self):
        super().__init__('hp60c_camera_node')

        self._latest_rgb   = None   # H x W x 3 uint8 BGR
        self._latest_depth = None   # H x W uint16 mm
        self._rgb_info = None
        self._depth_info = None
        self._pointcloud_seen = False
        self._pointcloud_width = 0
        self._last_rgb_at = 0.0
        self._last_depth_at = 0.0
        self._lock = threading.Lock()
        self._frame_count = 0

        self.create_subscription(Image, self.RGB_TOPIC,   self._on_rgb,   10)
        self.create_subscription(Image, self.DEPTH_TOPIC, self._on_depth, 10)
        self.create_subscription(CameraInfo, self.RGB_INFO_TOPIC, self._on_rgb_info, 10)
        self.create_subscription(CameraInfo, self.DEPTH_INFO_TOPIC, self._on_depth_info, 10)
        self.create_subscription(PointCloud2, self.POINTS_TOPIC, self._on_points, 10)
        self.create_timer(5.0, self._health_tick)

        self.get_logger().info('HP60C camera node started — waiting for ascamera topics...')

    def _on_rgb(self, msg: Image):
        arr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)
        with self._lock:
            self._latest_rgb = arr.copy()
            self._frame_count += 1
            self._last_rgb_at = time.monotonic()

    def _on_depth(self, msg: Image):
        arr = np.frombuffer(msg.data, dtype=np.uint16).reshape(msg.height, msg.width)
        with self._lock:
            self._latest_depth = arr.copy()
            self._last_depth_at = time.monotonic()

    def _on_rgb_info(self, msg: CameraInfo):
        with self._lock:
            self._rgb_info = msg

    def _on_depth_info(self, msg: CameraInfo):
        with self._lock:
            self._depth_info = msg

    def _on_points(self, msg: PointCloud2):
        with self._lock:
            self._pointcloud_seen = True
            self._pointcloud_width = int(getattr(msg, "width", 0))

    def capture(self) -> tuple:
        """
        Returns the latest (rgb_bgr_uint8, depth_uint16_mm) frame pair.
        Thread-safe. Returns (None, None) if no frames received yet.

        rgb   shape: (480, 640, 3) uint8  BGR
        depth shape: (480, 640)    uint16 millimetres
        """
        with self._lock:
            if self._latest_rgb is None or self._latest_depth is None:
                return None, None
            return self._latest_rgb.copy(), self._latest_depth.copy()

    def is_ready(self) -> bool:
        """Returns True once at least one frame pair has been received."""
        with self._lock:
            return self._latest_rgb is not None and self._latest_depth is not None

    def frame_count(self) -> int:
        with self._lock:
            return self._frame_count

    def stats(self) -> dict:
        with self._lock:
            return {
                "frame_count": self._frame_count,
                "rgb_info": self._rgb_info is not None,
                "depth_info": self._depth_info is not None,
                "pointcloud_seen": self._pointcloud_seen,
                "pointcloud_width": self._pointcloud_width,
            }

    def _health_tick(self):
        now = time.monotonic()
        with self._lock:
            rgb_age = (now - self._last_rgb_at) if self._last_rgb_at else None
            depth_age = (now - self._last_depth_at) if self._last_depth_at else None
            info_ready = self._rgb_info is not None
            points_ready = self._pointcloud_seen
        if rgb_age is None or depth_age is None:
            self.get_logger().warn('HP60C waiting for RGB/depth frames...')
            return
        if rgb_age > 2.0 or depth_age > 2.0:
            self.get_logger().warn(
                f'HP60C stream stale rgb_age={rgb_age:.2f}s depth_age={depth_age:.2f}s'
            )
            return
        self.get_logger().info(
            f'HP60C healthy camera_info={info_ready} pointcloud={points_ready}'
        )


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

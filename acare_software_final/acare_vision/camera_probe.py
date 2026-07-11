from __future__ import annotations

import time

import rclpy
from rclpy.node import Node
# AsyncParameterClient import — handles ROS2 Jazzy differences
_AsyncParameterClient = None
_client_fallback = False
try:
    from rclpy.parameter_client import AsyncParameterClient as _AsyncParameterClient
except (ImportError, ModuleNotFoundError):
    try:
        from rclpy.parameter import AsyncParameterClient as _AsyncParameterClient
    except (ImportError, ModuleNotFoundError):
        _client_fallback = True

if _client_fallback:
    _AsyncParameterClient = None


class CameraProbe(Node):
    def __init__(self):
        super().__init__("camera_probe")
        if _AsyncParameterClient is None:
            self.get_logger().error(
                "AsyncParameterClient not available in this ROS2 distribution. "
                "Cannot probe camera parameters."
            )
            self._client = None
        else:
            self._client = _AsyncParameterClient(self, "/ascamera_hp60c")

    def run(self) -> int:
        if self._client is None:
            return 2

        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            if self._client.service_is_ready():
                break
            time.sleep(0.5)
        if not self._client.service_is_ready():
            self.get_logger().error("ascamera parameter services not ready on /ascamera_hp60c")
            return 2

        future = self._client.list_parameters([], depth=10)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        result = future.result()
        if result is None:
            self.get_logger().error("Failed to list ascamera parameters")
            return 1

        names = sorted(result.names)
        if not names:
            self.get_logger().warn("ascamera reported no parameters")
            return 0

        keywords = ("exposure", "gain", "white", "balance", "fps", "frame", "auto", "laser", "depth", "rgb")
        interesting = [name for name in names if any(k in name.lower() for k in keywords)]

        print("All ascamera parameters:")
        for name in names:
            print(name)

        print("\nLikely imaging controls:")
        for name in interesting:
            print(name)
        return 0


def main(args=None):
    rclpy.init(args=args)
    node = CameraProbe()
    try:
        raise SystemExit(node.run())
    finally:
        node.destroy_node()
        rclpy.shutdown()


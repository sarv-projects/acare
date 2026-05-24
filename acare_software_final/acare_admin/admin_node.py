import rclpy
from rclpy.node import Node


class AdminNode(Node):
    def __init__(self):
        super().__init__("admin_node")
        self.create_timer(30.0, self._heartbeat)
        self.get_logger().info("Admin node ready")

    def _heartbeat(self):
        self.get_logger().debug("Admin heartbeat")


def main(args=None):
    rclpy.init(args=args)
    node = AdminNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

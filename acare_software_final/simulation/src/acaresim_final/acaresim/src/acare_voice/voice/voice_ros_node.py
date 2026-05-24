import threading
import time
import rclpy
from rclpy.node import Node
from acare_msgs.msg import ValidatedIntent, RobotState, StateTransition, SafetyAlert

class VoiceROSNode(Node):
    def __init__(self):
        super().__init__('voice_node')
        self._intent_pub = self.create_publisher(ValidatedIntent, '/validated_intent', 10)
        self._estop_pub = self.create_publisher(SafetyAlert, '/safety_alert', 10)
        self._transition_pub = self.create_publisher(StateTransition, '/state_transition', 10)
        self._state_sub = self.create_subscription(RobotState, '/robot_state', self._on_state, 10)

        self.current_robot_state = "LOGGED_OUT"
        self._voice = None
        self._voice_thread = None
        self._running = False
        self._voice_stop_event = threading.Event()

    def _on_state(self, msg):
        self.current_robot_state = msg.state
        self.get_logger().debug(f"Robot state: {msg.state}")

    def _on_intent_resolved(self, intent: dict):
        msg = ValidatedIntent()
        msg.tool = intent.get('tool', '')
        msg.action = intent.get('action', 'fetch')
        msg.user_id = intent.get('user_id', '')
        msg.name = intent.get('name', '')
        msg.authenticated = True
        self._intent_pub.publish(msg)
        self.get_logger().info(f"Published validated intent: {msg.tool}")

    def _on_estop_triggered(self, keyword: str):
        alert = SafetyAlert()
        alert.severity = "ESTOP"
        alert.reason = f"voice_keyword_{keyword}"
        alert.source = "voice"
        self._estop_pub.publish(alert)
        self.get_logger().warn(f"ESTOP triggered: {keyword}")

    def _run_voice(self):
        from voice.voice_node import VoiceNode
        self._voice = VoiceNode(
            on_intent_resolved=self._on_intent_resolved,
            on_estop_triggered=self._on_estop_triggered,
        )
        self._voice.start()
        while not self._voice_stop_event.is_set():
            time.sleep(0.5)
        self._voice.stop()

    def start(self):
        self._running = True
        self._voice_stop_event.clear()
        self._voice_thread = threading.Thread(target=self._run_voice, daemon=True)
        self._voice_thread.start()
        self.get_logger().info("Voice node started")

    def stop(self):
        self._running = False
        self._voice_stop_event.set()
        if self._voice_thread:
            self._voice_thread.join(timeout=5)
        self.get_logger().info("Voice node stopped")


def main():
    rclpy.init()
    node = VoiceROSNode()
    node.start()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.stop()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

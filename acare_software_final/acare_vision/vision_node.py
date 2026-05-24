# acare_vision/vision_node.py
# Spec Reference: Section XI (Vision Pipeline)
# Section V (ROS2 Software Architecture — vision_node)
#
# Master ROS2 node for all perception. Owns the camera, YOLO model,
# NBV search, fake detection, localisation, and hand tracking.
# Does NOT do inference directly — delegates to sub-modules.
#
# Startup sequence:
#   1. Publishes /vision_status: LOADING
#   2. Loads YOLO model in background thread (keeps ROS2 alive)
#   3. Publishes /vision_status: READY
#   4. Waits for /vision_search_request or HANDOVER state
#
# Mode switching:
#   IDLE     — no active task
#   SEARCH   — NBV search running (YOLO active, HandTracker stopped)
#   HANDOVER — HandTracker active (YOLO not called)
#   YOLO and MediaPipe Hands NEVER run simultaneously.
#
# Topics subscribed:
#   /vision_search_request (VisionSearchRequest) — from planner_node
#   /robot_state           (RobotState)           — to detect HANDOVER state
#   /ascamera_hp60c/camera_publisher/rgb0/image   — from ascamera node
#   /ascamera_hp60c/camera_publisher/depth0/image_raw — from ascamera node
#
# Topics published:
#   /vision_status  (String)        — LOADING | READY
#   /vision_result  (VisionResult)  — tool found or not found
#   /hand_status    (HandStatus)    — during HANDOVER state only
#   /log_event      (LogEvent)      — search events

import threading
import time
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from acare_bringup.paths import MODEL_DIR

try:
    from acare_msgs.msg import (
        VisionSearchRequest, VisionResult,
        HandStatus, RobotState, LogEvent, MotionFeedback, VisionStatus
    )
    ACARE_MSGS_AVAILABLE = True
except ImportError:
    ACARE_MSGS_AVAILABLE = False

from sensor_msgs.msg import Image

from .yolo_infer import YOLOv11ONNX
from .nbv_search import NBVSearch
from .fake_detector import FakeDetector
from .localiser import Localiser
from .hand_tracker import HandTracker
from .hp60c_camera_node import HP60CCameraNode

MODEL_PATH = str(MODEL_DIR / 'yolo_acare.onnx')
CONF_THRESH = 0.70


class VisionNode(Node):
    """
    Master perception node. Orchestrates all vision sub-modules.

    The node runs with a MultiThreadedExecutor so that:
      - ROS2 callbacks (subscriptions) are always responsive
      - NBV search (which blocks for seconds) runs in a separate thread
      - Hand tracking runs in its own daemon thread

    Thread safety:
      self._mode_lock protects self.mode transitions.
      Camera access is protected inside HP60CCameraNode._lock.
    """

    def __init__(self):
        super().__init__('vision_node')
        self.mode = 'IDLE'   # 'IDLE', 'SEARCH', 'HANDOVER'
        self._mode_lock = threading.Lock()
        self._yolo_ready = False
        self._motion_event = threading.Event()
        self._motion_success = False

        # --- Publishers ---
        self.status_pub = self.create_publisher(VisionStatus, '/vision_status', 10)
        if ACARE_MSGS_AVAILABLE:
            self.result_pub = self.create_publisher(VisionResult, '/vision_result', 10)
            self.hand_pub   = self.create_publisher(HandStatus,   '/hand_status',   10)
            self.log_pub    = self.create_publisher(LogEvent,     '/log_event',     10)
        else:
            self.result_pub = self.hand_pub = self.log_pub = None
            self.get_logger().warn('acare_msgs not built — running in standalone test mode')

        # --- Subscribers ---
        if ACARE_MSGS_AVAILABLE:
            self.create_subscription(
                VisionSearchRequest, '/vision_search_request',
                self._on_search_request, 10)
            self.create_subscription(
                RobotState, '/robot_state',
                self._on_robot_state, 10)
            self.create_subscription(
                MotionFeedback, '/motion_feedback',
                self._on_motion_feedback, 10)

        # Publish LOADING immediately so planner knows we're starting
        self._publish_status('LOADING')
        self.get_logger().info('Vision node: loading YOLO model...')

        # Load model in background thread — keeps ROS2 spinning
        threading.Thread(target=self._load_models, daemon=True).start()

    # -------------------------------------------------------------------------
    # Model loading
    # -------------------------------------------------------------------------

    def _load_models(self):
        """
        Loads YOLO model and initialises all sub-modules.
        Runs in a background thread so ROS2 stays alive during load.
        """
        try:
            self.yolo      = YOLOv11ONNX(MODEL_PATH, conf_thresh=CONF_THRESH)
            self.camera    = HP60CCameraNode.__new__(HP60CCameraNode)
            # Initialise camera node as a component (shares this node's executor)
            # by subscribing to ascamera topics directly
            self._init_camera_subscriptions()

            self.localiser = Localiser()
            self.nbv       = NBVSearch(self.yolo, self)
            self.hand_tracker = HandTracker(
                localiser=self.localiser,
                camera=self.camera,
                hand_pub=self.hand_pub,
                logger=self.get_logger(),
            )
            self._yolo_ready = True
            self._publish_status('READY')
            self.get_logger().info('Vision node: READY')

            if not self.localiser.is_calibrated():
                self.get_logger().warn(
                    'Camera not calibrated — using placeholder intrinsics. '
                    'Run admin.py calibrate Step 2 after arm assembly.')

        except Exception as e:
            self.get_logger().error(f'Vision node failed to load: {e}')
            self._publish_status('ERROR')

    def _publish_status(self, status: str):
        msg = VisionStatus()
        msg.status = status
        self.status_pub.publish(msg)

    def _init_camera_subscriptions(self):
        """
        Sets up the camera frame cache by subscribing to ascamera topics.
        Reuses HP60CCameraNode logic but within this node's context.
        """
        import numpy as np

        self._latest_rgb   = None
        self._latest_depth = None
        self._cam_lock     = threading.Lock()

        def on_rgb(msg: Image):
            arr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)
            with self._cam_lock:
                self._latest_rgb = arr.copy()

        def on_depth(msg: Image):
            arr = np.frombuffer(msg.data, dtype=np.uint16).reshape(msg.height, msg.width)
            with self._cam_lock:
                self._latest_depth = arr.copy()

        self.create_subscription(
            Image,
            '/ascamera_hp60c/camera_publisher/rgb0/image',
            on_rgb, 10)
        self.create_subscription(
            Image,
            '/ascamera_hp60c/camera_publisher/depth0/image_raw',
            on_depth, 10)

        # Expose capture() on self so sub-modules can call self.camera.capture()
        node_self = self

        class _CameraProxy:
            def capture(self):
                with node_self._cam_lock:
                    if node_self._latest_rgb is None or node_self._latest_depth is None:
                        return None, None
                    return node_self._latest_rgb.copy(), node_self._latest_depth.copy()

            def is_ready(self):
                with node_self._cam_lock:
                    return (node_self._latest_rgb is not None and
                            node_self._latest_depth is not None)

        self.camera = _CameraProxy()

    # -------------------------------------------------------------------------
    # ROS2 callbacks
    # -------------------------------------------------------------------------

    def _on_robot_state(self, msg):
        """
        Switches between SEARCH and HANDOVER modes based on robot state.
        YOLO and MediaPipe Hands never run simultaneously.
        """
        with self._mode_lock:
            if msg.state == 'HANDOVER' and self.mode != 'HANDOVER':
                self.mode = 'HANDOVER'
                if self._yolo_ready:
                    self.hand_tracker.start()
                    self.get_logger().info('Vision: switched to HANDOVER mode')
            elif msg.state != 'HANDOVER' and self.mode == 'HANDOVER':
                self.hand_tracker.stop()
                self.mode = 'IDLE'
                self.get_logger().info('Vision: switched to IDLE mode')

    def _on_search_request(self, msg):
        """
        Handles a vision search request from planner_node.
        Runs NBV search in a separate thread to avoid blocking ROS2 callbacks.
        """
        if not self._yolo_ready:
            self.get_logger().warn('Search request arrived before YOLO ready — ignoring')
            return

        with self._mode_lock:
            if self.mode == 'SEARCH':
                self.get_logger().warn('Search already in progress — ignoring duplicate request')
                return
            self.mode = 'SEARCH'

        tool_name = msg.tool
        self.get_logger().info(f'Vision: starting NBV search for {tool_name}')

        threading.Thread(
            target=self._run_search,
            args=(tool_name,),
            daemon=True
        ).start()

    def _run_search(self, tool_name: str):
        """
        Runs NBV search and publishes the result.
        Called in a background thread.
        """
        start_time = time.monotonic()

        try:
            result_dict = self.nbv.search(tool_name, self.camera)
        except Exception as e:
            self.get_logger().error(f'NBV search error: {e}')
            result_dict = {'found': False, 'tool': tool_name,
                           'x': 0.0, 'y': 0.0, 'z': 0.0,
                           'confidence': 0.0, 'zone': '', 'candidates': []}

        search_ms = int((time.monotonic() - start_time) * 1000)
        self.get_logger().info(
            f'Vision: search complete — found={result_dict["found"]} '
            f'tool={tool_name} zone={result_dict["zone"]} '
            f'time={search_ms}ms'
        )

        if ACARE_MSGS_AVAILABLE and self.result_pub:
            msg = VisionResult()
            msg.found      = result_dict['found']
            msg.tool       = result_dict['tool']
            msg.x          = float(result_dict['x'])
            msg.y          = float(result_dict['y'])
            msg.z          = float(result_dict['z'])
            msg.confidence = float(result_dict['confidence'])
            msg.zone       = result_dict['zone']
            msg.candidates_json = list(result_dict.get('candidates', []))
            self.result_pub.publish(msg)

        with self._mode_lock:
            self.mode = 'IDLE'

    # -------------------------------------------------------------------------
    # Arm command interface (called by NBVSearch)
    # -------------------------------------------------------------------------

    def move_arm_to(self, joint_angles: list) -> bool:
        """
        Sends a MOVE command to the arm via /arm_command topic.
        Waits for MotionFeedback.success (blocking, timeout 10s).
        Returns True on success, False on timeout or error.

        This method is called by NBVSearch._move_arm_to().
        When no arm is connected (testing), returns True immediately.
        """
        if not ACARE_MSGS_AVAILABLE:
            time.sleep(0.1)   # simulate arm move in testing
            return True

        try:
            from acare_msgs.msg import ArmCommand
            if not hasattr(self, '_arm_cmd_pub'):
                self._arm_cmd_pub = self.create_publisher(ArmCommand, '/arm_command', 10)

            cmd = ArmCommand()
            cmd.command        = 'MOVE'
            cmd.joint_angles   = [float(a) for a in joint_angles]
            cmd.velocity_scale = 0.8
            cmd.accel_limit    = 0.5
            cmd.blocking       = True

            self._motion_event.clear()
            self._arm_cmd_pub.publish(cmd)

            # Wait for motion feedback (set by _on_motion_feedback callback)
            got_feedback = self._motion_event.wait(timeout=10.0)
            return got_feedback and self._motion_success

        except Exception as e:
            self.get_logger().error(f'move_arm_to error: {e}')
            return False

    def _on_motion_feedback(self, msg):
        """Receives MotionFeedback from embedded_interface_node."""
        self._motion_success = msg.success
        self._motion_event.set()

    # -------------------------------------------------------------------------
    # Shutdown
    # -------------------------------------------------------------------------

    def destroy_node(self):
        """Save probability map on clean shutdown."""
        if self._yolo_ready and hasattr(self, 'nbv'):
            self.nbv.save_map()
            self.get_logger().info('Vision: probability map saved')
        if hasattr(self, 'hand_tracker'):
            self.hand_tracker.stop()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = VisionNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

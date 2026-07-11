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

import queue
import threading
import time
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.parameter import Parameter

# AsyncParameterClient import — handles ROS2 Jazzy differences
try:
    from rclpy.parameter_client import AsyncParameterClient
except (ImportError, ModuleNotFoundError):
    from rclpy.parameter import AsyncParameterClient
from acare_bringup.paths import MODEL_DIR
from acare_bringup.qos_profiles import (
    TOPIC_VISION,
    TOPIC_STATE,
    TOPIC_COMMAND,
    TOPIC_SENSOR,
    TOPIC_LOGGING,
)

try:
    from acare_msgs.msg import (
        VisionSearchRequest, VisionResult,
        HandStatus, RobotState, LogEvent, MotionFeedback, VisionStatus
    )
    ACARE_MSGS_AVAILABLE = True
except ImportError:
    ACARE_MSGS_AVAILABLE = False

from sensor_msgs.msg import CameraInfo, Image, PointCloud2

from .yolo_infer import YOLO26ONNX
from .nbv_search import NBVSearch
from .fake_detector import FakeDetector
from .localiser import Localiser
from .hand_tracker import HandTracker
from .hp60c_camera_node import HP60CCameraNode

MODEL_PATH = str(MODEL_DIR / 'acare_v26.onnx')
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
        self._camera_control_keywords = ("exposure", "gain", "white", "balance", "fps", "frame", "auto", "laser", "depth", "rgb")
        self._camera_control_overrides = self._load_camera_control_overrides()
        self._camera_control_probe_started = False
        self._last_camera_health_state = ""

        # --- Publishers ---
        self.status_pub = self.create_publisher(VisionStatus, '/vision_status', TOPIC_VISION)
        if ACARE_MSGS_AVAILABLE:
            self.result_pub = self.create_publisher(VisionResult, '/vision_result', TOPIC_VISION)
            self.hand_pub   = self.create_publisher(HandStatus,   '/hand_status',   TOPIC_VISION)
            self.log_pub    = self.create_publisher(LogEvent,     '/log_event',     TOPIC_LOGGING)
        else:
            self.result_pub = self.hand_pub = self.log_pub = None
            self.get_logger().warn('acare_msgs not built — running in standalone test mode')

        # --- Subscribers ---
        if ACARE_MSGS_AVAILABLE:
            self.create_subscription(
                VisionSearchRequest, '/vision_search_request',
                self._on_search_request, TOPIC_VISION)
            self.create_subscription(
                RobotState, '/robot_state',
                self._on_robot_state, TOPIC_STATE)
            self.create_subscription(
                MotionFeedback, '/motion_feedback',
                self._on_motion_feedback, TOPIC_SENSOR)

        # Thread-safe result publishing queue (drained by _publish_results timer)
        self._result_queue = queue.Queue(maxsize=100)
        self.create_timer(0.1, self._publish_results)

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
            self.yolo      = YOLO26ONNX(MODEL_PATH, conf_thresh=CONF_THRESH)
            self.localiser = Localiser()

            # Initialise camera node as a component (shares this node's executor)
            # by subscribing to ascamera topics directly
            self._init_camera_subscriptions()

            self.nbv       = NBVSearch(self.yolo, self, localiser=self.localiser)
            self.hand_tracker = HandTracker(
                localiser=self.localiser,
                camera=self.camera,
                hand_pub=self.hand_pub,
                logger=self.get_logger(),
                arm_link_lengths=self.nbv.arm_link_lengths,
            )
            self._yolo_ready = True
            self._publish_status('READY')
            self.get_logger().info('Vision node: READY')
            self._start_camera_control_probe()
            self.create_timer(5.0, self._camera_health_tick)

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

    def _load_camera_control_overrides(self) -> dict[str, object]:
        try:
            import yaml
            from acare_bringup.paths import SYSTEM_YAML

            with open(SYSTEM_YAML, "r", encoding="utf-8") as handle:
                cfg = yaml.safe_load(handle) or {}
            raw = cfg.get("camera", {}).get("control_overrides", {}) or {}
            return raw if isinstance(raw, dict) else {}
        except Exception:
            return {}

    def _init_camera_subscriptions(self):
        """
        Sets up the camera frame cache by subscribing to ascamera topics.
        Reuses HP60CCameraNode logic but within this node's context.
        """
        import numpy as np

        self._latest_rgb   = None
        self._latest_depth = None
        self._cam_lock     = threading.Lock()
        self._rgb_info = None
        self._depth_info = None
        self._pointcloud_seen = False
        self._pointcloud_width = 0
        self._last_rgb_at = 0.0
        self._last_depth_at = 0.0
        self._last_info_at = 0.0
        self._last_points_at = 0.0
        self._rgb_frame_count = 0
        self._depth_frame_count = 0

        def on_rgb(msg: Image):
            arr = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)
            with self._cam_lock:
                self._latest_rgb = arr.copy()
                self._rgb_frame_count += 1
                self._last_rgb_at = time.monotonic()

        def on_depth(msg: Image):
            arr = np.frombuffer(msg.data, dtype=np.uint16).reshape(msg.height, msg.width)
            with self._cam_lock:
                self._latest_depth = arr.copy()
                self._depth_frame_count += 1
                self._last_depth_at = time.monotonic()

        def on_rgb_info(msg: CameraInfo):
            with self._cam_lock:
                self._rgb_info = msg
                self._last_info_at = time.monotonic()
            if len(msg.k) >= 6 and hasattr(self, "localiser"):
                self.localiser.update_intrinsics(msg.k[0], msg.k[4], msg.k[2], msg.k[5])

        def on_depth_info(msg: CameraInfo):
            with self._cam_lock:
                self._depth_info = msg
                self._last_info_at = time.monotonic()

        def on_points(msg: PointCloud2):
            with self._cam_lock:
                self._pointcloud_seen = True
                self._pointcloud_width = int(getattr(msg, "width", 0))
                self._last_points_at = time.monotonic()

        self.create_subscription(
            Image,
            '/ascamera_hp60c/camera_publisher/rgb0/image',
            on_rgb, TOPIC_SENSOR)
        self.create_subscription(
            Image,
            '/ascamera_hp60c/camera_publisher/depth0/image_raw',
            on_depth, TOPIC_SENSOR)
        self.create_subscription(
            CameraInfo,
            '/ascamera_hp60c/camera_publisher/rgb0/camera_info',
            on_rgb_info, TOPIC_SENSOR)
        self.create_subscription(
            CameraInfo,
            '/ascamera_hp60c/camera_publisher/depth0/camera_info',
            on_depth_info, TOPIC_SENSOR)
        self.create_subscription(
            PointCloud2,
            '/ascamera_hp60c/camera_publisher/depth0/points',
            on_points, TOPIC_SENSOR)

        # Expose capture() on self so sub-modules can call self.camera.capture()
        node_self = self

        class _CameraProxy:
            def capture(self):
                with node_self._cam_lock:
                    if node_self._latest_rgb is None or node_self._latest_depth is None:
                        return None, None
                    # Ensure frames were received within 200ms of each other to prevent lunges
                    if abs(node_self._last_rgb_at - node_self._last_depth_at) > 0.2:
                        return None, None
                    return node_self._latest_rgb.copy(), node_self._latest_depth.copy()

            def is_ready(self):
                with node_self._cam_lock:
                    return (node_self._latest_rgb is not None and
                            node_self._latest_depth is not None)

            def stats(self):
                with node_self._cam_lock:
                    return {
                        "rgb_frames": node_self._rgb_frame_count,
                        "depth_frames": node_self._depth_frame_count,
                        "rgb_info": node_self._rgb_info is not None,
                        "depth_info": node_self._depth_info is not None,
                        "pointcloud_seen": node_self._pointcloud_seen,
                        "pointcloud_width": node_self._pointcloud_width,
                    }

        self.camera = _CameraProxy()

    def _camera_health_tick(self):
        now = time.monotonic()
        with self._cam_lock:
            rgb_age = (now - self._last_rgb_at) if self._last_rgb_at else None
            depth_age = (now - self._last_depth_at) if self._last_depth_at else None
            info_ready = self._rgb_info is not None
            points_ready = self._pointcloud_seen
            rgb_frames = self._rgb_frame_count
            depth_frames = self._depth_frame_count

        if rgb_age is None or depth_age is None:
            state = 'waiting_for_streams'
            if state != self._last_camera_health_state:
                self.get_logger().warn('Vision: waiting for HP60C RGB/depth streams.')
                self._last_camera_health_state = state
            return
        if rgb_age > 2.0 or depth_age > 2.0:
            state = 'stale_streams'
            if state != self._last_camera_health_state:
                self.get_logger().warn(
                    f'Vision: HP60C stream appears stale rgb_age={rgb_age:.2f}s depth_age={depth_age:.2f}s'
                )
                self._last_camera_health_state = state
        elif not info_ready:
            state = 'missing_camera_info'
            if state != self._last_camera_health_state:
                self.get_logger().warn('Vision: HP60C CameraInfo topic not observed yet; using config intrinsics.')
                self._last_camera_health_state = state
        elif not points_ready:
            state = 'missing_pointcloud'
            if state != self._last_camera_health_state:
                self.get_logger().warn('Vision: HP60C point cloud topic not observed yet.')
                self._last_camera_health_state = state
        else:
            state = 'healthy'
            if state != self._last_camera_health_state:
                self.get_logger().info(
                    f'Vision: HP60C healthy rgb_frames={rgb_frames} depth_frames={depth_frames} '
                    f'pointcloud=yes intrinsics=live'
                )
                self._last_camera_health_state = state

    def _wait_future(self, future, timeout_s: float):
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            if future.done():
                return future.result()
            time.sleep(0.05)
        future.cancel()
        return None

    def _start_camera_control_probe(self):
        if self._camera_control_probe_started:
            return
        self._camera_control_probe_started = True
        threading.Thread(target=self._probe_and_apply_camera_controls, daemon=True).start()

    def _probe_and_apply_camera_controls(self):
        try:
            self._async_client = getattr(self, '_async_client', None) or AsyncParameterClient(self, '/ascamera_hp60c')
            client = self._async_client
            deadline = time.monotonic() + 12.0
            while time.monotonic() < deadline:
                if client.service_is_ready():
                    break
                time.sleep(0.5)
            if not client.service_is_ready():
                self.get_logger().warn('Vision: ascamera parameter services not ready; exact camera controls not discoverable yet.')
                return

            future = client.list_parameters([], depth=10)
            list_result = self._wait_future(future, 5.0)
            if list_result is None:
                self.get_logger().warn('Vision: failed to list ascamera parameters.')
                return
            names = list(getattr(list_result, 'names', []))
            if not names:
                self.get_logger().warn('Vision: ascamera reported no parameters.')
                return

            interesting = [
                name for name in names
                if any(keyword in name.lower() for keyword in self._camera_control_keywords)
            ]
            if interesting:
                self.get_logger().info(
                    'Vision: discovered ascamera controls/topics via parameters: ' + ', '.join(sorted(interesting))
                )
            else:
                self.get_logger().warn('Vision: ascamera parameters exposed, but no obvious imaging controls were found.')

            overrides = []
            for name, value in self._camera_control_overrides.items():
                if name not in names:
                    self.get_logger().warn(f'Vision: camera control override skipped; ascamera has no parameter named {name}.')
                    continue
                if isinstance(value, bool):
                    param_type = Parameter.Type.BOOL
                elif isinstance(value, int) and not isinstance(value, bool):
                    param_type = Parameter.Type.INTEGER
                elif isinstance(value, float):
                    param_type = Parameter.Type.DOUBLE
                else:
                    param_type = Parameter.Type.STRING
                overrides.append(Parameter(name=name, type_=param_type, value=value))

            if overrides:
                set_future = client.set_parameters(overrides)
                result = self._wait_future(set_future, 5.0)
                if result is None:
                    self.get_logger().warn('Vision: camera control override request returned no result.')
                else:
                    failures = [r.reason for r in result.results if not r.successful]
                    if failures:
                        self.get_logger().warn('Vision: some camera control overrides failed: ' + '; '.join(failures))
                    else:
                        self.get_logger().info('Vision: configured camera control overrides applied to ascamera.')
        except Exception as exc:
            self.get_logger().warn(f'Vision: camera control probe failed: {exc}')

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
                    # Provide the arm's current joint angles so that
                    # pixel_to_robot() uses the correct wrist-camera transform.
                    if hasattr(self, '_last_joint_positions') and self._last_joint_positions:
                        self.hand_tracker.set_viewpoint_joints(self._last_joint_positions)
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

        # Extract priority_zones — pass first non-AUTO zone, or None
        zones = getattr(msg, 'priority_zones', None)
        zone = None
        if zones and len(zones) > 0:
            first = zones[0]
            if first.upper() != 'AUTO':
                zone = first

        self.get_logger().info(
            f'Vision: starting NBV search for {tool_name}'
            + (f' zone={zone}' if zone else ''))

        threading.Thread(
            target=self._run_search,
            args=(tool_name, zone),
            daemon=True
        ).start()

    def _run_search(self, tool_name: str, zone: str | None = None):
        """
        Runs NBV search and enqueues the result for thread-safe publishing.

        Called in a background thread.  The result is placed onto a
        thread-safe queue and published from the ROS2 executor thread via
        the _publish_results() timer callback.
        """
        start_time = time.monotonic()

        try:
            result_dict = self.nbv.search(tool_name, self.camera, zone=zone)
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

        # Enqueue result for publishing from the executor thread
        self._result_queue.put((result_dict, search_ms, tool_name))

        with self._mode_lock:
            self.mode = 'IDLE'

    def _publish_results(self):
        """
        Timer callback (0.1s) that drains the result queue and publishes
        from the ROS2 executor thread.  This avoids publishing from a
        non-Executor daemon thread (ROS2 constraint).
        """
        while not self._result_queue.empty():
            try:
                result_dict, search_ms, tool_name = self._result_queue.get_nowait()
            except queue.Empty:
                break

            if not (ACARE_MSGS_AVAILABLE and self.result_pub):
                continue

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

            if self.log_pub:
                log_msg = LogEvent()
                log_msg.event_type = 'VISION_SEARCH'
                log_msg.tool = tool_name
                log_msg.description = f"Found in {result_dict['zone']}" if result_dict['found'] else "Tool not found"
                log_msg.vision_search_ms = search_ms
                log_msg.timestamp = int(time.time())
                self.log_pub.publish(log_msg)

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
                self._arm_cmd_pub = self.create_publisher(ArmCommand, '/arm_command', TOPIC_COMMAND)

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
        # Cache latest joint positions for wrist-mounted camera T computation
        if msg.joint_positions and len(msg.joint_positions) >= 6:
            self._last_joint_positions = list(msg.joint_positions[:6])
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

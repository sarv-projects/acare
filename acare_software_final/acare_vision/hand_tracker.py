# acare_vision/hand_tracker.py
# Spec Reference: Section XI (Hand Tracking — During Handover)
# Section VII (Handover — Multi-Modal Verification, Check 2)
#
# Runs ONLY during HANDOVER state. Detects open palm and computes
# 3D palm position for dynamic arm approach.
#
# Uses MediaPipe Hands (single hand, max 1).
# Publishes /hand_status at ~20 Hz while active.
# Stopped during vision search — YOLO and MediaPipe never run simultaneously.
#
# HandStatus fields:
#   hand_detected — bool: at least one hand visible
#   is_open       — bool: 3+ fingers extended
#   palm_up       — bool: fingertips above wrist (palm facing up)
#   x, y, z       — float32: 3D palm centre in robot base frame (metres)
#   confidence    — float32: detection confidence (0.0–1.0)

import threading
import time
import numpy as np

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False


# MediaPipe hand landmark indices
WRIST      = 0
THUMB_IP   = 3;  THUMB_TIP  = 4
INDEX_MCP  = 5;  INDEX_PIP  = 6;  INDEX_TIP  = 8
MIDDLE_MCP = 9;  MIDDLE_PIP = 10; MIDDLE_TIP = 12
RING_MCP   = 13; RING_PIP   = 14; RING_TIP   = 16
PINKY_MCP  = 17; PINKY_PIP  = 18; PINKY_TIP  = 20


class HandTracker:
    """
    Runs MediaPipe Hands in a background thread during HANDOVER state.
    Publishes HandStatus messages at ~20 Hz.

    Lifecycle:
        start() — called when robot enters HANDOVER state
        stop()  — called when HANDOVER state exits

    The tracker reads frames directly from the camera node via camera.capture()
    and publishes results to the hand_pub publisher provided at init.
    """

    def __init__(self, localiser, camera, hand_pub, logger=None,
                 arm_link_lengths=None):
        """
        localiser        — Localiser instance for pixel → robot frame conversion
        camera           — HP60CCameraNode instance with capture() method
        hand_pub         — ROS2 publisher for HandStatus messages
        logger           — ROS2 node logger (optional, for debug output)
        arm_link_lengths — dict {base_height, upper_arm, forearm} for FK.
                           Needed for wrist-mounted camera T computation.
        """
        self.localiser = localiser
        self.camera    = camera
        self.hand_pub  = hand_pub
        self.logger    = logger
        self.running   = False
        self._thread   = None
        self._arm_link_lengths = arm_link_lengths or {'base_height': 0.352, 'upper_arm': 0.400, 'forearm': 0.400}
        # Joint angles of the arm during HANDOVER (presentation pose).
        # Set via set_viewpoint_joints() before start() so that
        # pixel_to_robot() can use a wrist-mounted camera T override.
        self._current_joints = None
        self._T_override     = None

        if MEDIAPIPE_AVAILABLE:
            self._hands = mp.solutions.hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.70,
                min_tracking_confidence=0.60,
            )
        else:
            self._hands = None
            if logger:
                logger.warning('MediaPipe not available — hand tracking disabled')

    def set_viewpoint_joints(self, joint_angles: list[float]):
        """
        Called before start() with the arm's current joint angles so that
        pixel_to_robot() can compute a correct wrist-mounted camera transform.
        """
        self._current_joints = [float(a) for a in joint_angles]
        if hasattr(self.localiser, 'compute_T_for_viewpoint'):
            self._T_override = self.localiser.compute_T_for_viewpoint(
                self._current_joints, self._arm_link_lengths,
            )

    def start(self):
        """Start the hand tracking background thread."""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the hand tracking background thread and wait for it to exit."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

    def _loop(self):
        while self.running:
            rgb, depth = self.camera.capture()
            if rgb is None:
                time.sleep(0.05)
                continue
            msg = self._process(rgb, depth)
            if self.hand_pub is not None:
                self.hand_pub.publish(msg)
            time.sleep(0.05)   # ~20 Hz

    def _process(self, rgb_frame: np.ndarray, depth_frame: np.ndarray):
        """
        Processes one RGB+depth frame pair and returns a HandStatus message.

        Detection logic:
          hand_detected — MediaPipe found at least one hand
          is_open       — 3 or more fingers are extended (tip y < PIP y in image coords)
                          Thumb uses lateral distance instead of y comparison
          palm_up       — mean fingertip y < wrist y (fingertips above wrist in image)
          x, y, z       — 3D position of palm centre (average of wrist + 4 MCP landmarks)
                          converted to robot frame via Localiser.pixel_to_robot()
        """
        # Import here to avoid issues if mediapipe not installed
        from acare_msgs.msg import HandStatus
        msg = HandStatus()
        msg.hand_detected = False
        msg.is_open       = False
        msg.palm_up       = False
        msg.hand_approaching = False
        msg.confidence    = 0.0
        msg.x = msg.y = msg.z = 0.0

        if not MEDIAPIPE_AVAILABLE or self._hands is None:
            return msg

        # HP60C delivers BGR frames; MediaPipe Hands requires RGB.
        # Convert before processing or detection is degraded/broken.
        try:
            import cv2
            mp_input = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)
        except Exception:
            mp_input = rgb_frame

        results = self._hands.process(mp_input)
        if not results.multi_hand_landmarks:
            return msg

        h, w = rgb_frame.shape[:2]
        lm = results.multi_hand_landmarks[0].landmark

        msg.hand_detected = True
        msg.confidence    = 0.8   # MediaPipe doesn't expose per-frame confidence

        # --- is_open: count extended fingers ---
        fingers_extended = 0
        for tip_idx, pip_idx in [
            (INDEX_TIP,  INDEX_PIP),
            (MIDDLE_TIP, MIDDLE_PIP),
            (RING_TIP,   RING_PIP),
            (PINKY_TIP,  PINKY_PIP),
        ]:
            # In image coords, y increases downward.
            # Tip y < PIP y means finger is pointing up (extended).
            if lm[tip_idx].y < lm[pip_idx].y:
                fingers_extended += 1

        # Thumb: extended if tip is laterally far from IP joint
        if abs(lm[THUMB_TIP].x - lm[THUMB_IP].x) > 0.04:
            fingers_extended += 1

        msg.is_open = fingers_extended >= 3

        # --- palm_up: fingertips above wrist in image ---
        fingertip_y_mean = np.mean([
            lm[INDEX_TIP].y, lm[MIDDLE_TIP].y,
            lm[RING_TIP].y,  lm[PINKY_TIP].y
        ])
        msg.palm_up = fingertip_y_mean < lm[WRIST].y

        # --- 3D palm centre ---
        palm_indices = [WRIST, INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP]
        px = int(np.mean([lm[i].x for i in palm_indices]) * w)
        py = int(np.mean([lm[i].y for i in palm_indices]) * h)

        # Use a small 10x10 bbox around palm centre for depth lookup
        bbox = (px - 5, py - 5, px + 5, py + 5)
        if depth_frame is not None:
            pos = self.localiser.pixel_to_robot(bbox, depth_frame,
                                                T_override=self._T_override)
            if pos:
                msg.x, msg.y, msg.z = pos

        # --- hand_approaching: hand is open and palm centre is within a
        # reasonable reachable volume in front of the robot (0.1m < x < 0.65m,
        # |y| < 0.4m, z > 0.0m).  x is forward depth in robot frame.
        msg.hand_approaching = bool(
            msg.hand_detected and msg.is_open
            and 0.10 < msg.x < 0.65
            and abs(msg.y) < 0.40
            and msg.z > 0.0
        )

        return msg

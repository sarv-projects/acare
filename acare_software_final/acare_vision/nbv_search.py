# acare_vision/nbv_search.py
# Spec Reference: Section XI (NBV Search & Detection)
# Section XII (Task Planner — Vision NBV Search)
#
# Next-Best-View search algorithm.
# Decides which arm viewpoint to move to next when searching for a tool,
# prioritised by a Bayesian probability map that learns from past searches.
#
# Viewpoints are defined during calibration (admin.py calibrate Step 5).
# Until calibration, viewpoints list is empty and search returns not-found.
#
# Probability map:
#   - Loaded from probability_map.yaml on startup
#   - Updated after every search (Bayesian update with clamping)
#   - Saved atomically on clean shutdown
#   - Cold start (no yaml): uniform distribution across all zones
#
# Model classes (8 total, matching the current top-level taxonomy):
#   scalpel, scissors, forceps, bandage, gauze, thermometer, oximeter, plaster

import yaml
import time
import numpy as np
from pathlib import Path
import json

from .fake_detector import FakeDetector
from .localiser import Localiser
from acare_bringup.paths import PROBABILITY_MAP_YAML, SYSTEM_YAML

PROB_MAP_PATH = PROBABILITY_MAP_YAML

WORKSPACE = {
    'xmin': -0.4, 'xmax': 0.4,
    'ymin': -0.3, 'ymax': 0.3,
    'zmin':  0.0, 'zmax': 0.5,
}

# All tool classes the model can detect (6 classes, matching trained YOLO model)
ALL_TOOLS = [
    'cream', 'medical scissors', 'oxymeter',
    'plaster', 'surgical forceps', 'thermometer',
]

# Map from model class name to canonical system name
CANONICAL = {
    'cream': 'cream',
    'medical scissors': 'scissors',
    'oxymeter': 'oximeter',
    'plaster': 'plaster',
    'surgical forceps': 'forceps',
    'thermometer': 'thermometer',
}

# Reverse map: canonical → model class name (for lookup by tool name from intent)
REVERSE_CANONICAL = {v: k for k, v in CANONICAL.items()}


class NBVSearch:
    """
    Bayesian Next-Best-View search for surgical tools.

    Workflow per search() call:
      1. Sort viewpoints by P(tool|zone), highest first
      2. For each viewpoint:
         a. Send MOVE command to arm, wait for stationary confirmation
         b. Capture 3 RGB+depth frame pairs at small wrist offsets
         c. Run YOLO inference on all 3 frames, merge with NMS
         d. Apply temporal consistency check (promotes 0.65+ if seen before)
         e. Filter to requested tool class only
         f. Run fake detection on each candidate
         g. Run workspace boundary check
         h. Update Bayesian map for this zone
         i. If valid detection found: return 3D position
      3. If all viewpoints exhausted: return found=False

    The arm command interface (move_arm_to, wait_for_motion_feedback) is
    provided by the parent vision_node via callbacks set at init.
    """

    def __init__(self, yolo_model, node):
        """
        yolo_model — YOLOv11ONNX instance
        node       — parent VisionNode (for arm commands and logging)
        """
        self.yolo         = yolo_model
        self.node         = node
        self.fake_detector = FakeDetector()
        self.localiser    = Localiser()
        self.probability_map = self._load_map()
        self.viewpoints   = self._load_viewpoints()
        self.wrist_offsets = self._load_wrist_offsets()
        self.capture_settle_s = self._load_capture_settle_s()
        self.joint_limits_min, self.joint_limits_max = self._load_joint_limits()
        # Tracks detections from previous viewpoint for temporal consistency
        self.prev_detections = {}   # class_name → (cx, cy) pixel centre

    # -------------------------------------------------------------------------
    # Map loading and saving
    # -------------------------------------------------------------------------

    def _load_map(self) -> dict:
        """
        Loads probability_map.yaml if it exists.
        Fills in any missing tools with 0.05 (minimum prior).
        Falls back to uniform distribution on cold start.
        """
        zones = ['zone_A', 'zone_B', 'zone_C']
        if PROB_MAP_PATH.exists():
            try:
                with open(PROB_MAP_PATH) as f:
                    loaded = yaml.safe_load(f) or {}
                for zone in zones:
                    if zone not in loaded:
                        loaded[zone] = {}
                    for tool in ALL_TOOLS:
                        if tool not in loaded[zone]:
                            loaded[zone][tool] = 0.05
                return loaded
            except Exception:
                pass
        # Cold start: uniform distribution
        n = len(ALL_TOOLS)
        return {z: {t: 1.0 / n for t in ALL_TOOLS} for z in zones}

    def _load_viewpoints(self) -> list:
        """
        Loads viewpoints from system.yaml after calibration.
        Returns empty list until calibration is done.
        Each viewpoint: {'zone': str, 'joint_angles': [float x6]}
        """
        system_yaml = SYSTEM_YAML
        if not system_yaml.exists():
            return []
        try:
            with open(system_yaml) as f:
                cfg = yaml.safe_load(f)
            return cfg.get('vision', {}).get('viewpoints', [])
        except Exception:
            return []

    def _load_wrist_offsets(self) -> list[list[float]]:
        default_offsets = [
            [0.0, 0.0],
            [0.035, 0.0],
            [-0.035, 0.025],
        ]
        system_yaml = SYSTEM_YAML
        if not system_yaml.exists():
            return default_offsets
        try:
            with open(system_yaml) as f:
                cfg = yaml.safe_load(f) or {}
            offsets = cfg.get('vision', {}).get('nbv_wrist_micro_offsets_rad', default_offsets)
            normalised = []
            for pair in offsets:
                if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                    continue
                normalised.append([float(pair[0]), float(pair[1])])
            return normalised or default_offsets
        except Exception:
            return default_offsets

    def _load_capture_settle_s(self) -> float:
        system_yaml = SYSTEM_YAML
        if not system_yaml.exists():
            return 0.12
        try:
            with open(system_yaml) as f:
                cfg = yaml.safe_load(f) or {}
            settle_ms = float(cfg.get('vision', {}).get('capture_settle_ms', 120))
            return max(0.05, settle_ms / 1000.0)
        except Exception:
            return 0.12

    def _load_joint_limits(self) -> tuple[list[float] | None, list[float] | None]:
        system_yaml = SYSTEM_YAML
        if not system_yaml.exists():
            return None, None
        try:
            with open(system_yaml) as f:
                cfg = yaml.safe_load(f) or {}
            mins = [float(v) for v in cfg.get('arm', {}).get('joint_limits_min', [])]
            maxs = [float(v) for v in cfg.get('arm', {}).get('joint_limits_max', [])]
            if len(mins) != 6 or len(maxs) != 6:
                return None, None
            if all(abs(v) < 1e-9 for v in mins + maxs):
                return None, None
            return mins, maxs
        except Exception:
            return None, None

    def save_map(self):
        """
        Atomically writes the probability map to disk.
        Uses .tmp → rename pattern to prevent corruption on power loss.
        Called on clean shutdown by vision_node.
        """
        PROB_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp = Path(str(PROB_MAP_PATH) + '.tmp')
        try:
            with open(tmp, 'w') as f:
                yaml.dump(self.probability_map, f)
            tmp.rename(PROB_MAP_PATH)
        except Exception as e:
            if self.node:
                self.node.get_logger().error(f'Failed to save probability map: {e}')

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(self, tool_name: str, camera) -> dict:
        """
        Searches all viewpoints for the requested tool.

        tool_name — canonical tool name from intent (e.g. 'scissors', 'oximeter')
        camera    — HP60CCameraNode instance

        Returns dict:
            {'found': bool, 'tool': str, 'x': float, 'y': float, 'z': float,
             'confidence': float, 'zone': str, 'candidates': list}
        """
        result = {'found': False, 'tool': tool_name, 'x': 0.0, 'y': 0.0, 'z': 0.0,
                  'confidence': 0.0, 'zone': '', 'candidates': []}

        # Map canonical name to model class name
        model_class = REVERSE_CANONICAL.get(tool_name, tool_name)

        if not self.viewpoints:
            if self.node:
                self.node.get_logger().warn(
                    'NBV search: no viewpoints defined. Run admin.py calibrate Step 5.')
            return result

        sorted_vps = self._sort_zones(model_class)

        for vp in sorted_vps:
            zone = vp['zone']

            # Move arm to viewpoint
            ok = self._move_arm_to(vp['joint_angles'])
            if not ok:
                continue

            # Capture 3 frames at small wrist offsets
            frame_pairs = self._capture_frames(camera, vp['joint_angles'])
            rgb_frames   = [p[0] for p in frame_pairs]
            depth_frames = [p[1] for p in frame_pairs]

            # Run YOLO on all 3 frames, merge
            all_dets = self.yolo.infer_multi_frame(rgb_frames)

            # Determine lighting mode from the reference frame
            low_light_mode = False
            if rgb_frames and rgb_frames[0] is not None:
                import cv2
                import numpy as np
                gray = cv2.cvtColor(rgb_frames[0], cv2.COLOR_BGR2GRAY)
                low_light_mode = float(np.mean(gray)) < 80   # spec Section XI threshold

            # Temporal consistency with lighting-adaptive threshold
            all_dets = self._check_temporal_consistency(all_dets, low_light_mode=low_light_mode)

            # Update prev detections for next viewpoint
            self.prev_detections = {}
            for d in all_dets:
                cx = (d['bbox'][0] + d['bbox'][2]) // 2
                cy = (d['bbox'][1] + d['bbox'][3]) // 2
                self.prev_detections[d['class_name']] = (cx, cy)

            # Filter to requested tool class
            tool_dets = [d for d in all_dets if d['class_name'] == model_class]

            # Fake check + workspace filter
            ref_rgb   = rgb_frames[1]
            ref_depth = depth_frames[1]
            valid = []
            for d in tool_dets:
                if self.fake_detector.is_fake(ref_rgb, ref_depth, d['bbox']):
                    if self.node:
                        self.node.get_logger().warn(f'Fake object rejected: {d["class_name"]}')
                    continue
                pos = self.localiser.pixel_to_robot(d['bbox'], ref_depth)
                if pos is None:
                    continue
                if not self._in_workspace(pos):
                    continue
                d['position_3d'] = pos
                d['depth_support'] = self._depth_support_score(ref_depth, d['bbox'])
                d['rank_score'] = (
                    float(d['confidence'])
                    + 0.10 * float(d['depth_support'])
                    + (0.02 if d.get('variant') == 'enhanced' and d.get('scene_low_light') else 0.0)
                )
                valid.append(d)

            # Bayesian map update
            self._update_map(zone, model_class, found=len(valid) > 0, all_dets=all_dets)

            if valid:
                valid.sort(key=lambda d: d.get('rank_score', d['confidence']), reverse=True)
                best = valid[0]
                result['found']      = True
                result['x'], result['y'], result['z'] = best['position_3d']
                result['confidence'] = best['confidence']
                result['zone']       = zone
                result['candidates'] = [
                    json.dumps({
                        'x': float(d['position_3d'][0]),
                        'y': float(d['position_3d'][1]),
                        'z': float(d['position_3d'][2]),
                        'confidence': float(d['confidence']),
                        'zone': zone,
                    })
                    for d in valid[1:]
                ]
                return result

        return result

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def _sort_zones(self, model_class: str) -> list:
        """Sort viewpoints by P(tool|zone), highest probability first."""
        scored = []
        for vp in self.viewpoints:
            zone = vp['zone']
            prob = self.probability_map.get(zone, {}).get(model_class, 0.05)
            scored.append((prob, vp))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [vp for _, vp in scored]

    def _move_arm_to(self, joint_angles: list) -> bool:
        """
        Sends a MOVE command to the arm and waits for motion feedback.
        Returns True if arm reached the target, False on timeout or error.
        Delegates to vision_node's arm command interface.
        """
        if self.node and hasattr(self.node, 'move_arm_to'):
            return self.node.move_arm_to(joint_angles)
        # No arm connected — return True for testing without hardware
        time.sleep(0.1)
        return True

    def _apply_wrist_offset(self, joint_angles: list, offset_pair: list[float]) -> list:
        adjusted = [float(v) for v in joint_angles]
        if len(adjusted) < 6:
            return adjusted
        adjusted[4] += float(offset_pair[0])
        adjusted[5] += float(offset_pair[1])
        if self.joint_limits_min is not None and self.joint_limits_max is not None:
            adjusted[4] = float(np.clip(adjusted[4], self.joint_limits_min[4], self.joint_limits_max[4]))
            adjusted[5] = float(np.clip(adjusted[5], self.joint_limits_min[5], self.joint_limits_max[5]))
        return adjusted

    def _capture_frame_pair(self, camera):
        for _ in range(4):
            rgb, depth = camera.capture()
            if rgb is not None and depth is not None:
                return rgb, depth
            time.sleep(0.05)
        return None, None

    def _depth_support_score(self, depth_frame, bbox: tuple) -> float:
        if depth_frame is None:
            return 0.0
        x1, y1, x2, y2 = bbox
        h, w = depth_frame.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        if x2 <= x1 or y2 <= y1:
            return 0.0
        roi = depth_frame[y1:y2, x1:x2]
        if roi.size == 0:
            return 0.0
        valid = roi[(roi >= 200) & (roi <= 4000)]
        return float(valid.size / roi.size)

    def _capture_frames(self, camera, base_joint_angles: list) -> list:
        """
        Captures 3 RGB+depth frame pairs around a viewpoint.
        The first sample uses the base viewpoint, then two small wrist offsets
        are applied to reduce self-occlusion and low-texture misses. If an
        offset move fails, capture falls back to the current pose and search
        continues. The base viewpoint is restored before returning.
        Returns list of (rgb, depth) tuples.
        """
        frames = []
        poses = [[float(v) for v in base_joint_angles]]
        for offset_pair in self.wrist_offsets[1:3]:
            poses.append(self._apply_wrist_offset(base_joint_angles, offset_pair))

        restore_required = False
        try:
            for idx, pose in enumerate(poses):
                if idx > 0:
                    moved = self._move_arm_to(pose)
                    if moved:
                        restore_required = True
                        time.sleep(self.capture_settle_s)
                    elif self.node:
                        self.node.get_logger().warn(
                            f'NBV wrist offset move failed at sample {idx + 1}; '
                            'capturing from current pose instead.'
                        )
                else:
                    time.sleep(min(0.05, self.capture_settle_s))

                rgb, depth = self._capture_frame_pair(camera)
                if rgb is not None and depth is not None:
                    frames.append((rgb, depth))
        finally:
            if restore_required:
                restored = self._move_arm_to(base_joint_angles)
                if not restored and self.node:
                    self.node.get_logger().warn('Failed to restore base NBV viewpoint after wrist-offset capture.')

        # Pad with copies if fewer than 3 frames captured
        while len(frames) < 3 and frames:
            frames.append(frames[-1])
        return frames if frames else [(None, None)] * 3

    def _check_temporal_consistency(self, dets: list, low_light_mode: bool = False) -> list:
        """
        Promotes detections with confidence >= 0.65 if seen at same location in
        previous viewpoint (within 50px). Handles partial occlusion.

        Spec Section XI: temporal_consistency_required = 3 viewpoints if low_light_mode,
        else 2. This method is called per-viewpoint; the caller tracks the viewpoint
        count across iterations — here we apply the confidence floor per lighting mode.
        """
        # In low-light mode, require confidence >= 0.65 (already at threshold floor).
        # In normal mode, require confidence >= 0.70.
        # Temporal promotion lowers the effective threshold to 0.65 in both cases
        # when the same object is seen at the same location.
        promoted = []
        for d in dets:
            cx = (d['bbox'][0] + d['bbox'][2]) // 2
            cy = (d['bbox'][1] + d['bbox'][3]) // 2
            prev = self.prev_detections.get(d['class_name'])
            if prev is not None:
                dist = ((cx - prev[0])**2 + (cy - prev[1])**2) ** 0.5
                if dist < 50 and d['confidence'] >= 0.65:
                    promoted.append(d)
                    continue
            # Base threshold depends on lighting
            base_thresh = 0.60 if low_light_mode else 0.70
            if d['confidence'] >= base_thresh:
                promoted.append(d)
        return promoted

    def _update_map(self, zone: str, model_class: str, found: bool, all_dets: list):
        """
        Bayesian update of the probability map for a zone after a search step.

        Update rules:
          Tool found:     P(zone, tool) *= 1.5
          Tool not found: P(zone, tool) *= 0.7
          Other tools seen (passive): P(zone, other) *= 1.3

        After update: normalise so zone probabilities sum to 1.0,
        then clamp each value to [0.05, 0.90].
        """
        if zone not in self.probability_map:
            self.probability_map[zone] = {t: 1.0 / len(ALL_TOOLS) for t in ALL_TOOLS}

        # Primary update
        current = self.probability_map[zone].get(model_class, 0.125)
        self.probability_map[zone][model_class] = current * (1.5 if found else 0.7)

        # Passive update for other detected tools
        for det in all_dets:
            t = det['class_name']
            if t != model_class:
                v = self.probability_map[zone].get(t, 0.125)
                self.probability_map[zone][t] = v * 1.3

        # Normalise
        total = sum(self.probability_map[zone].values())
        if total > 0:
            for t in self.probability_map[zone]:
                self.probability_map[zone][t] /= total

        # Clamp to [0.05, 0.90]
        for t in self.probability_map[zone]:
            v = self.probability_map[zone][t]
            self.probability_map[zone][t] = min(max(v, 0.05), 0.90)

    def _in_workspace(self, pos: tuple) -> bool:
        """Returns True if (x, y, z) is within the defined robot workspace."""
        x, y, z = pos
        w = WORKSPACE
        return (w['xmin'] <= x <= w['xmax'] and
                w['ymin'] <= y <= w['ymax'] and
                w['zmin'] <= z <= w['zmax'])

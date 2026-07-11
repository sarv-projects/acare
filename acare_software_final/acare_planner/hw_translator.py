# acare_planner/hw_translator.py
import logging
import yaml
from pathlib import Path
from acare_bringup.paths import SYSTEM_YAML

logger = logging.getLogger(__name__)

class HWTranslator:
    def __init__(self):
        self.config = self._load_config()
        self.base_grasp_force_n = float(self.config.get('planner', {}).get('base_grasp_force_n', 3.0))
        
        robot_cfg = self.config.get('robot', {})
        self.safe_drop_zone = self._to_float_list(robot_cfg.get('safe_drop_zone', [0.0, 0.35, 0.05]))
        self.face_verify_z = float(robot_cfg.get('face_verify_z', 0.70))
        self.presentation_z = float(robot_cfg.get('presentation_z', 0.45))
        
        hz = self._to_float_list(robot_cfg.get('handover_zone', [0.0, 0.4, 0.1]))
        self.handover_x = hz[0] if len(hz) > 0 else 0.0
        self.handover_y = hz[1] if len(hz) > 1 else 0.4
        
        planner_cfg = self.config.get('planner', {})
        self.grip_firmness_map = planner_cfg.get('grip_firmness', {'LIGHT': 0.0, 'NORMAL': 1.0, 'FIRM': 2.0})
        self.approach_variant_map = planner_cfg.get('approach_variant', {'TOP_DOWN': 0.0, 'SIDE_LEFT': -90.0, 'SIDE_RIGHT': 90.0})

    def _load_config(self) -> dict:
        if SYSTEM_YAML.exists():
            try:
                with open(SYSTEM_YAML) as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                logger.error(f"Failed to parse config file: {SYSTEM_YAML}. "
                             "Robot behaviour may be unsafe without valid configuration.")
        else:
            logger.error(f"Config file not found: {SYSTEM_YAML}. "
                         "Robot behaviour may be unsafe without valid configuration.")
        return {}

    def _to_float_list(self, val) -> list:
        if isinstance(val, str):
            raise ValueError(f"Expected list or dict for config value, got string: {val}")
        if isinstance(val, dict):
            return [float(val.get('x', 0.0)), float(val.get('y', 0.0)), float(val.get('z', 0.0))]
        return [float(v) for v in val] if isinstance(val, (list, tuple)) else val

    def translate_firmness(self, firmness: str) -> float:
        delta = self.grip_firmness_map.get(firmness.upper(), 1.0)
        return self.base_grasp_force_n + delta

    def translate_approach_variant(self, variant: str) -> float:
        return self.approach_variant_map.get(variant.upper(), 0.0)

    def translate_position(self, pos_name: str, grasp_point: tuple = None, user_z_offset: float = 0.0) -> list:
        pos = pos_name.upper()
        if pos == 'SAFE_DROP':
            return self.safe_drop_zone
        elif pos == 'FACE_HEIGHT':
            return [self.handover_x, self.handover_y, self.face_verify_z]
        elif pos == 'PRESENTATION':
            return [self.handover_x, self.handover_y, self.presentation_z + user_z_offset]
        elif pos == 'PREGRASP':
            if not grasp_point:
                return [0.0, 0.4, 0.1]
            return [grasp_point[0], grasp_point[1], grasp_point[2] + 0.05]
        elif pos == 'GRASP_POINT':
            if not grasp_point:
                return [0.0, 0.4, 0.05]
            return [grasp_point[0], grasp_point[1], grasp_point[2]]
        elif pos == 'REST':
            # Base rest position
            return [0.0, 0.2, 0.2]
        
        # Unknown position — raise error instead of silent fallback
        raise ValueError(f"Unknown position: {pos_name}")

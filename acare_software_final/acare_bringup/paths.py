from __future__ import annotations

from pathlib import Path


BRINGUP_ROOT = Path(__file__).resolve().parent
REPO_ROOT = BRINGUP_ROOT.parent
CONFIG_DIR = BRINGUP_ROOT / "config"
LAUNCH_DIR = BRINGUP_ROOT / "launch"
LOG_DIR = REPO_ROOT / "logs"
MODEL_DIR = REPO_ROOT / "models"
USERS_DB = CONFIG_DIR / "users.db"
SYSTEM_YAML = CONFIG_DIR / "system.yaml"
THRESHOLDS_YAML = CONFIG_DIR / "thresholds.yaml"
PROBABILITY_MAP_YAML = CONFIG_DIR / "probability_map.yaml"


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

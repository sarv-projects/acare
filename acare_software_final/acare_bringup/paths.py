from __future__ import annotations

from pathlib import Path


BRINGUP_ROOT = Path(__file__).resolve().parent
REPO_ROOT = BRINGUP_ROOT.parent
CONFIG_DIR = BRINGUP_ROOT / "config"
LAUNCH_DIR = BRINGUP_ROOT / "launch"
LOG_DIR = REPO_ROOT / "logs"
MODEL_DIR = REPO_ROOT / "models"
if not (MODEL_DIR / "acare_v26.onnx").exists():
    _src_models = Path("/home/acare/acare_ws/src/models")
    if (_src_models / "acare_v26.onnx").exists():
        MODEL_DIR = _src_models
USERS_DB = LOG_DIR / "users.db"
SYSTEM_YAML = CONFIG_DIR / "system.yaml"
THRESHOLDS_YAML = CONFIG_DIR / "thresholds.yaml"
PROBABILITY_MAP_YAML = CONFIG_DIR / "probability_map.yaml"
DOTENV_PATH = REPO_ROOT / ".env"
DB_PATH     = CONFIG_DIR / "task_memory.db"


def load_env():
    """Load environment variables from repo-root .env file (once only)."""
    from dotenv import load_dotenv as _load
    _load(dotenv_path=str(DOTENV_PATH), override=False)


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

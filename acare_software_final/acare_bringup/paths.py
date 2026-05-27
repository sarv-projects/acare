from __future__ import annotations

import os
from pathlib import Path


# ---------------------------------------------------------------------------
# Source-tree-relative paths (read-only at runtime)
# ---------------------------------------------------------------------------
# After `colcon build` these resolve into install/share/acare_bringup/... and
# must NEVER be written to. Use them only for reading config and launch files.

BRINGUP_ROOT = Path(__file__).resolve().parent
REPO_ROOT = BRINGUP_ROOT.parent
CONFIG_DIR = BRINGUP_ROOT / "config"
LAUNCH_DIR = BRINGUP_ROOT / "launch"
SYSTEM_YAML = CONFIG_DIR / "system.yaml"
THRESHOLDS_YAML = CONFIG_DIR / "thresholds.yaml"
PROBABILITY_MAP_YAML = CONFIG_DIR / "probability_map.yaml"


# ---------------------------------------------------------------------------
# Writable runtime data — kept OUTSIDE the install tree
# ---------------------------------------------------------------------------
# Earlier versions placed `users.db` and `logs/` next to this file. After
# colcon ament_python install, that resolved to
#   install/acare_bringup/lib/python3.x/site-packages/acare_bringup/...
# which (a) is recreated by every `colcon build` (operator loses logs and
# enrolled users) and (b) may be read-only or owned by root in production
# images.
#
# Resolution priority:
#   1. $ACARE_DATA_DIR  — explicit override (tests, containers, multi-tenant)
#   2. $XDG_STATE_HOME/acare  — Linux desktop convention
#   3. ~/.acare         — fallback for the deployment account
#
# /var/lib/acare is a sensible deployment override for system-installed
# instances; set $ACARE_DATA_DIR=/var/lib/acare in the systemd unit.

def _resolve_data_dir() -> Path:
    override = os.environ.get("ACARE_DATA_DIR")
    if override:
        base = Path(override).expanduser()
    else:
        xdg = os.environ.get("XDG_STATE_HOME")
        if xdg:
            base = Path(xdg).expanduser() / "acare"
        else:
            base = Path.home() / ".acare"
    base.mkdir(parents=True, exist_ok=True)
    return base


DATA_DIR = _resolve_data_dir()
LOG_DIR = DATA_DIR / "logs"
USERS_DB = DATA_DIR / "users.db"
STATE_DB = DATA_DIR / "state.db"          # used by acare_planner.state_manager
MODEL_DIR = REPO_ROOT / "models"          # models stay packaged with the source


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

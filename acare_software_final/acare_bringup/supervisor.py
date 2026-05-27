#!/usr/bin/env python3
# acare_bringup/supervisor.py
# Spec Reference: Section V (Node Crash Recovery), Section XVII (Power Recovery)
#
# Standalone Python script — NOT a ROS2 node.
# Launched separately from the ROS2 stack.
# Monitors all ACARE nodes and handles crashes.
#
# Auto-restart (non-critical nodes):
#   log_node, admin_node, dialogue_node, voice_node, auth_node
#
# No auto-restart (critical nodes) — trigger ESTOP instead:
#   safety_node, embedded_interface_node, state_manager, planner_node
#
# Detection method: ros2 node list (queries ROS2 graph directly)
# This is reliable — checks actual node presence, not launcher exit code.
#
# Check interval: 5 seconds.
#
# Power recovery (Section XVII):
# Power recovery is now performed by acare_planner.state_manager itself —
# it reads ~/.acare/state.db on startup and recovers the last persisted
# state. The supervisor only emits an audible TTS alert AFTER all nodes
# have come up so that voice_node is actually subscribed and can play it.

import os
import subprocess
import time
import sys

from pathlib import Path

# Resolve the writable data dir the same way acare_bringup.paths does.
# We avoid importing acare_bringup at module load because the supervisor
# is launched before the ROS environment is necessarily sourced.

def _data_dir() -> Path:
    override = os.environ.get("ACARE_DATA_DIR")
    if override:
        base = Path(override).expanduser()
    else:
        xdg = os.environ.get("XDG_STATE_HOME")
        base = Path(xdg).expanduser() / "acare" if xdg else Path.home() / ".acare"
    base.mkdir(parents=True, exist_ok=True)
    return base


DATA_DIR = _data_dir()
LOG_DB_PATH = DATA_DIR / "logs" / "acare_logs.db"
STATE_DB_PATH = DATA_DIR / "state.db"

AUTO_RESTART = {'log_node', 'admin_node', 'dialogue_node', 'voice_node', 'auth_node'}
CRITICAL = {'safety_node', 'embedded_interface_node', 'state_manager', 'planner_node'}

# ROS2 node names as they appear in `ros2 node list`
NODE_ROS_NAMES = {
    'log_node':                '/log_node',
    'admin_node':              '/admin_node',
    'dialogue_node':           '/dialogue_node',
    'voice_node':              '/voice_node',
    'auth_node':               '/auth_node',
    'safety_node':             '/safety_node',
    'embedded_interface_node': '/embedded_interface_node',
    'state_manager':           '/state_manager',
    'planner_node':            '/planner_node',
    'vision_node':             '/vision_node',
}

# Commands to start each node
NODE_CMDS = {
    'log_node':                ['ros2', 'run', 'acare_logging',           'log_node'],
    'admin_node':              ['ros2', 'run', 'acare_admin',             'admin_node'],
    'dialogue_node':           ['ros2', 'run', 'acare_dialogue',          'dialogue_node'],
    'voice_node':              ['ros2', 'run', 'acare_voice',             'voice_node'],
    'auth_node':               ['ros2', 'run', 'acare_auth',              'auth_node'],
    'safety_node':             ['ros2', 'run', 'acare_safety',            'safety_node'],
    'embedded_interface_node': ['ros2', 'run', 'acare_embedded_interface','interface_node'],
    'state_manager':           ['ros2', 'run', 'acare_planner',           'state_manager'],
    'planner_node':            ['ros2', 'run', 'acare_planner',           'planner_node'],
    'vision_node':             ['ros2', 'run', 'acare_vision',            'vision_node'],
}

# Bring-up order: state_manager and embedded_interface come up first so the
# rest of the graph can immediately publish to /robot_state and /motion_feedback.
STARTUP_ORDER = [
    'state_manager',
    'embedded_interface_node',
    'safety_node',
    'log_node',
    'vision_node',
    'auth_node',
    'planner_node',
    'dialogue_node',
    'voice_node',
    'admin_node',
]

# Order matters — only nodes published in NODE_CMDS get supervised.
processes = {}


def start_node(name: str):
    """Starts a node as a background subprocess.

    Cleans up any prior process for the same name first to avoid leaks
    when a CRITICAL node is restarted.
    """
    cmd = NODE_CMDS.get(name)
    if not cmd:
        print(f'[supervisor] Unknown node: {name}')
        return

    old = processes.get(name)
    if old is not None and old.poll() is None:
        try:
            old.terminate()
            old.wait(timeout=3.0)
        except Exception:
            try:
                old.kill()
            except Exception:
                pass

    proc = subprocess.Popen(cmd)
    processes[name] = proc
    print(f'[supervisor] Started {name} (PID {proc.pid})')


def is_node_alive(ros_name: str) -> bool:
    """
    Checks if a ROS2 node is alive by querying the ROS2 graph.
    Returns True if node is present, False if missing.
    Returns True on timeout (assume alive — avoid false ESTOP).
    """
    try:
        result = subprocess.run(
            ['ros2', 'node', 'list'],
            capture_output=True, text=True, timeout=5.0
        )
        return ros_name in result.stdout
    except subprocess.TimeoutExpired:
        print(f'[supervisor] WARNING: ros2 node list timed out — assuming {ros_name} alive')
        return True
    except Exception as e:
        print(f'[supervisor] WARNING: could not check {ros_name}: {e}')
        return True


def trigger_estop(reason: str):
    """Publishes an ESTOP signal to /emergency_stop and /safety_alert."""
    print(f'[supervisor] TRIGGERING ESTOP: {reason}')
    try:
        subprocess.run([
            'ros2', 'topic', 'pub', '--once', '/emergency_stop',
            'acare_msgs/msg/EmergencySignal',
            f'{{reason: "{reason}", source: "supervisor"}}'
        ], timeout=5.0)
    except Exception as exc:
        print(f'[supervisor] Failed to publish /emergency_stop: {exc}')
    try:
        subprocess.run([
            'ros2', 'topic', 'pub', '--once', '/safety_alert',
            'acare_msgs/msg/SafetyAlert',
            f'{{severity: "ESTOP", reason: "{reason}", source: "supervisor"}}'
        ], timeout=5.0)
    except Exception as exc:
        print(f'[supervisor] Failed to publish /safety_alert: {exc}')


def wait_for_subscribers(topic: str, type_name: str, timeout_s: float = 30.0) -> bool:
    """Block until at least one subscriber appears on `topic` or timeout."""
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            result = subprocess.run(
                ['ros2', 'topic', 'info', topic],
                capture_output=True, text=True, timeout=3.0,
            )
            stdout = result.stdout or ''
            for line in stdout.splitlines():
                line = line.strip().lower()
                if line.startswith('subscription count:'):
                    try:
                        count = int(line.split(':', 1)[1].strip())
                    except ValueError:
                        count = 0
                    if count > 0:
                        return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def announce_power_recovery():
    """
    Spec Section XVII: Power Recovery.
    Reads the last persisted state from the audit log AND the state DB and,
    if the previous shutdown was mid-task, publishes a TTS warning *after*
    the voice node is online so the operator actually hears it.
    """
    last_state = None

    # Prefer the dedicated state DB (written by state_manager on every
    # transition). Fall back to the audit log if it is missing.
    import sqlite3
    if STATE_DB_PATH.exists():
        try:
            conn = sqlite3.connect(str(STATE_DB_PATH))
            row = conn.execute(
                "SELECT state FROM state_snapshot WHERE id = 1"
            ).fetchone()
            conn.close()
            if row:
                last_state = str(row[0]).upper()
        except Exception as exc:
            print(f'[supervisor] state.db read failed: {exc}')

    if last_state is None and LOG_DB_PATH.exists():
        try:
            conn = sqlite3.connect(str(LOG_DB_PATH))
            row = conn.execute(
                "SELECT state FROM events ORDER BY timestamp DESC LIMIT 1"
            ).fetchone()
            conn.close()
            if row:
                last_state = str(row[0]).upper()
        except Exception as exc:
            print(f'[supervisor] acare_logs.db read failed: {exc}')

    if last_state is None:
        print('[supervisor] No prior state record — clean boot.')
        return

    print(f'[supervisor] Last known state: {last_state}')

    if last_state in {'EXECUTING', 'HOLDING', 'HANDOVER'}:
        print('[supervisor] POWER_RECOVERY: previous shutdown was mid-task.')
        # Wait for /tts_request subscribers (voice_node) before publishing.
        if not wait_for_subscribers('/tts_request', 'std_msgs/msg/String', timeout_s=20.0):
            print('[supervisor] WARNING: no /tts_request subscribers — recovery alert may be lost')

        try:
            subprocess.run([
                'ros2', 'topic', 'pub', '--once', '/tts_request',
                'std_msgs/msg/String',
                '{data: "System recovered from unexpected shutdown. Please verify the workspace before continuing."}'
            ], timeout=5.0)
        except Exception as exc:
            print(f'[supervisor] Failed to publish recovery TTS: {exc}')

        try:
            subprocess.run([
                'ros2', 'topic', 'pub', '--once', '/log_event',
                'acare_msgs/msg/LogEvent',
                ('{event_type: "POWER_RECOVERY", user_id: "", tool: "", '
                 'state: "STANDBY", description: "Recovered from unexpected shutdown", '
                 'timestamp: 0, voice_e2e_ms: 0, vision_search_ms: 0, '
                 'motion_ms: 0, total_task_ms: 0, safety_severity: ""}')
            ], timeout=5.0)
        except Exception as exc:
            print(f'[supervisor] Failed to publish POWER_RECOVERY log: {exc}')


def monitor():
    """Main monitoring loop. Checks all nodes every 5 seconds."""
    print('[supervisor] Monitoring started. Check interval: 5s')
    while True:
        time.sleep(5)
        for name, ros_name in NODE_ROS_NAMES.items():
            if name not in NODE_CMDS:
                continue
            if not is_node_alive(ros_name):
                print(f'[supervisor] {name} not found in ROS2 graph')
                if name in AUTO_RESTART:
                    print(f'[supervisor] Restarting {name}...')
                    time.sleep(1)
                    start_node(name)
                elif name in CRITICAL:
                    try:
                        trigger_estop(f'Critical node {name} crashed')
                    except Exception as e:
                        print(f'[supervisor] Failed to trigger ESTOP: {e}')


def main():
    if 'ROS_DISTRO' not in os.environ:
        print('[supervisor] WARNING: ROS2 not sourced. Run: source /opt/ros/jazzy/setup.bash')

    print('[supervisor] Starting ACARE nodes...')
    for name in STARTUP_ORDER:
        if name in NODE_CMDS:
            start_node(name)
            time.sleep(0.5)   # stagger starts to avoid race conditions

    # Spec Section XVII: announce recovery only AFTER voice/log nodes are up
    # so the alert is not lost into the void.
    print('[supervisor] Checking for power recovery condition...')
    announce_power_recovery()

    print('[supervisor] All nodes started. Beginning health monitoring.')
    try:
        monitor()
    except KeyboardInterrupt:
        print('\n[supervisor] Shutting down...')
        for name, proc in list(processes.items()):
            try:
                proc.terminate()
                print(f'[supervisor] Stopped {name}')
            except Exception:
                pass
        sys.exit(0)


if __name__ == '__main__':
    main()

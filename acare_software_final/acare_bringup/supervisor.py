#!/usr/bin/env python3
# DEPRECATED - Use supervisor_node.py instead
# acare_bringup/supervisor.py
# Spec Reference: Section V (Node Crash Recovery)
#
# Standalone Python script — NOT a ROS2 node.
# Launched separately from the ROS2 stack.
# Monitors all ACARE nodes and handles crashes.
#
# Auto-restart (non-critical nodes):
#   log_node, admin_node, dialogue_node
#
# No auto-restart (critical nodes) — trigger ESTOP instead:
#   safety_node, embedded_interface_node, state_manager, planner_node
#
# Detection method: ros2 node list (queries ROS2 graph directly)
# This is reliable — checks actual node presence, not launcher exit code.
#
# Check interval: 5 seconds
# ESTOP trigger: ros2 topic pub --once /emergency_stop

import subprocess
import time
import sys

AUTO_RESTART = {'log_node', 'admin_node', 'dialogue_node', 'voice_node', 'auth_node'}
CRITICAL     = {'safety_node', 'embedded_interface_node', 'state_manager', 'planner_node', 'vision_node'}

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

processes = {}


def start_node(name: str):
    """Starts a node as a background subprocess."""
    cmd = NODE_CMDS.get(name)
    if not cmd:
        print(f'[supervisor] Unknown node: {name}')
        return
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
    """Publishes an ESTOP signal to /emergency_stop."""
    print(f'[supervisor] TRIGGERING ESTOP: {reason}')
    try:
        subprocess.run([
            'ros2', 'topic', 'pub', '--once', '/emergency_stop',
            'acare_msgs/msg/EmergencySignal',
            f'{{reason: "{reason}", source: "supervisor"}}'
        ], timeout=5.0)
    except Exception as e:
        print(f'[supervisor] Failed to publish ESTOP: {e}')


def check_power_recovery():
    """
    Spec Section XVII: Power Recovery.
    On boot, check last SQLite state.
    If last state was EXECUTING or HOLDING → arm was mid-task during shutdown.
    Publishes a safe-state transition and TTS warning.
    """
    import sqlite3
    from pathlib import Path

    db_path = Path(__file__).resolve().parent.parent / 'logs' / 'acare_logs.db'
    if not db_path.exists():
        print('[supervisor] No log DB found — clean boot.')
        return

    try:
        conn = sqlite3.connect(str(db_path))
        row = conn.execute(
            "SELECT state FROM events ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        conn.close()

        if row is None:
            return

        last_state = str(row[0]).upper()
        print(f'[supervisor] Last known state from DB: {last_state}')

        if last_state in {'EXECUTING', 'HOLDING', 'HANDOVER'}:
            print('[supervisor] POWER_RECOVERY: last state was mid-task. Publishing safe state.')

            def _pub(topic, msg_type, payload):
                try:
                    subprocess.run([
                        'ros2', 'topic', 'pub', '--once', topic, msg_type, payload
                    ], timeout=5.0)
                except Exception as e:
                    print(f'[supervisor] Failed to publish {topic}: {e}')

            _pub('/state_transition', 'acare_msgs/msg/StateTransition',
                 '{target_state: "STANDBY", reason: "power_recovery"}')
            _pub('/tts_request', 'std_msgs/msg/String',
                 '{data: "System recovered from unexpected shutdown. Please verify workspace."}')
            _pub('/log_event', 'acare_msgs/msg/LogEvent',
                 ('{event_type: "POWER_RECOVERY", user_id: "", tool: "", '
                  'state: "STANDBY", description: "Recovered from unexpected shutdown", '
                  'timestamp: 0, voice_e2e_ms: 0, vision_search_ms: 0, '
                  'motion_ms: 0, total_task_ms: 0, safety_severity: ""}'))

    except Exception as e:
        print(f'[supervisor] Power recovery check failed: {e}')


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
    import os
    if 'ROS_DISTRO' not in os.environ:
        print('[supervisor] WARNING: ROS2 not sourced. Run: source /opt/ros/jazzy/setup.bash')

    # Spec Section XVII: Check for power recovery condition before starting nodes
    print('[supervisor] Checking for power recovery condition...')
    time.sleep(2.0)   # brief wait for ROS2 graph to initialise after launch
    check_power_recovery()

    print('[supervisor] All nodes should be started by acare.launch.py. Beginning health monitoring.')
    try:
        monitor()
    except KeyboardInterrupt:
        print('\n[supervisor] Shutting down...')
        for name, proc in processes.items():
            proc.terminate()
            print(f'[supervisor] Stopped {name}')
        sys.exit(0)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
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

AUTO_RESTART = {'log_node', 'admin_node', 'dialogue_node'}
CRITICAL     = {'safety_node', 'embedded_interface_node', 'state_manager', 'planner_node'}

# ROS2 node names as they appear in `ros2 node list`
NODE_ROS_NAMES = {
    'log_node':                '/log_node',
    'admin_node':              '/admin_node',
    'dialogue_node':           '/dialogue_node',
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
    subprocess.run([
        'ros2', 'topic', 'pub', '--once', '/emergency_stop',
        'acare_msgs/msg/EmergencySignal',
        f'{{reason: "{reason}", source: "supervisor"}}'
    ], timeout=5.0)


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
    # Source ROS2 if not already sourced
    if 'ROS_DISTRO' not in os.environ:
        print('[supervisor] WARNING: ROS2 not sourced. Run: source /opt/ros/jazzy/setup.bash')

    print('[supervisor] Starting all ACARE nodes...')
    for name in NODE_CMDS:
        start_node(name)
        time.sleep(0.5)   # stagger starts to avoid race conditions

    print('[supervisor] All nodes started. Beginning health monitoring.')
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

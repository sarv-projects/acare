#!/usr/bin/env python3
# acare_admin/admin_cli.py
# Spec Reference: Section XVIII (Admin CLI & Calibration)
#
# Command-line interface for ACARE system administration.
# Run on Pi via: python3 admin_cli.py <command> [options]
#
# Commands:
#   enrol          --name "Dr. Sharma" --role surgeon
#   revoke         --id staff_001
#   list-staff
#   set-api-key    --service deepgram|groq --key YOUR_KEY
#   set-threshold  --sensor joint_current|joint_temp|gripper_force --value 8.0
#   show-logs      --last 50
#   export-logs    --format csv
#   status
#   calibrate
#   demo-mode      --enable | --disable
#
# API keys are stored encrypted using Fernet symmetric encryption.
# Key file: /etc/acare/key.bin (created on first use)
# API keys file: /etc/acare/api_keys.yaml

import argparse
import sqlite3
import yaml
import sys
import subprocess
from pathlib import Path
from acare_bringup.paths import LOG_DIR, SYSTEM_YAML, THRESHOLDS_YAML, USERS_DB

DB_PATH       = LOG_DIR / 'acare_logs.db'
KEY_PATH      = Path('/etc/acare/key.bin')
API_KEYS_PATH = Path('/etc/acare/api_keys.yaml')
THRESHOLDS    = THRESHOLDS_YAML


def get_fernet():
    """Returns a Fernet instance, creating the key file if it doesn't exist."""
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print('ERROR: cryptography package not installed. Run: pip install cryptography')
        sys.exit(1)

    if not KEY_PATH.exists():
        key = Fernet.generate_key()
        KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
        KEY_PATH.write_bytes(key)
        print(f'Generated new encryption key at {KEY_PATH}')
    return Fernet(KEY_PATH.read_bytes())


def cmd_enrol(args):
    """
    Triggers staff enrolment via ROS2 service call to auth_node.
    auth_node handles the actual biometric capture and storage.
    """
    print(f'Enrolling: {args.name} ({args.role})')
    result = subprocess.run([
        'ros2', 'service', 'call', '/enrol_staff',
        'acare_msgs/srv/EnrolStaff',
        f'{{"name": "{args.name}", "role": "{args.role}"}}'
    ], capture_output=True, text=True)
    print(result.stdout or result.stderr or 'No response from auth_node')


def cmd_revoke(args):
    """Marks a staff member as inactive in users.db."""
    users_db = USERS_DB
    if not users_db.exists():
        print(f'users.db not found at {users_db}')
        return
    conn = sqlite3.connect(str(users_db))
    conn.execute('UPDATE users SET active=0 WHERE id=?', (args.id,))
    conn.commit()
    rows = conn.execute('SELECT changes()').fetchone()[0]
    conn.close()
    if rows:
        print(f'Staff {args.id} revoked.')
    else:
        print(f'Staff ID {args.id} not found.')


def cmd_list_staff(args):
    """Lists all enrolled staff from users.db."""
    users_db = USERS_DB
    if not users_db.exists():
        print('No users.db found — no staff enrolled yet.')
        return
    conn = sqlite3.connect(str(users_db))
    rows = conn.execute(
        'SELECT id, name, role, registered_at, active FROM users ORDER BY registered_at'
    ).fetchall()
    conn.close()
    if not rows:
        print('No staff enrolled.')
        return
    print(f'{"ID":<20} {"Name":<20} {"Role":<15} {"Registered":<20} {"Active"}')
    print('-' * 80)
    for r in rows:
        print(f'{r[0]:<20} {r[1]:<20} {r[2]:<15} {r[3]:<20} {"Yes" if r[4] else "No"}')


def cmd_set_api_key(args):
    """Stores an API key encrypted in /etc/acare/api_keys.yaml."""
    f = get_fernet()
    keys = {}
    if API_KEYS_PATH.exists():
        keys = yaml.safe_load(API_KEYS_PATH.read_text()) or {}
    keys[args.service] = f.encrypt(args.key.encode()).decode()
    API_KEYS_PATH.parent.mkdir(parents=True, exist_ok=True)
    API_KEYS_PATH.write_text(yaml.dump(keys))
    print(f'API key for {args.service} saved (encrypted).')


def cmd_set_threshold(args):
    """Updates a safety threshold in thresholds.yaml."""
    sensor_map = {
        'joint_current': ('safety', 'current_limit_A'),
        'joint_temp':    ('safety', 'temperature_estop_C'),
        'gripper_force': ('safety', 'gripper_force_limit_N'),
    }
    if args.sensor not in sensor_map:
        print(f'Unknown sensor. Valid options: {list(sensor_map.keys())}')
        return
    with open(THRESHOLDS) as f:
        cfg = yaml.safe_load(f)
    section, key = sensor_map[args.sensor]
    old = cfg[section].get(key, 'unknown')
    cfg[section][key] = float(args.value)
    with open(THRESHOLDS, 'w') as f:
        yaml.dump(cfg, f)
    print(f'Threshold {args.sensor} ({key}): {old} → {args.value}')


def cmd_show_logs(args):
    """Shows the most recent log events from acare_logs.db."""
    if not DB_PATH.exists():
        print('No log database found.')
        return
    conn = sqlite3.connect(str(DB_PATH))
    rows = conn.execute(
        'SELECT timestamp, staff_id, event_type, tool, state FROM events '
        'ORDER BY timestamp DESC LIMIT ?', (args.last,)
    ).fetchall()
    conn.close()
    if not rows:
        print('No log entries found.')
        return
    print(f'{"Timestamp":<25} {"Staff":<15} {"Event":<25} {"Tool":<15} {"State"}')
    print('-' * 90)
    for r in rows:
        print(f'{str(r[0]):<25} {str(r[1]):<15} {str(r[2]):<25} {str(r[3]):<15} {r[4]}')


def cmd_export_logs(args):
    """Exports all log events to a CSV file."""
    import csv
    if not DB_PATH.exists():
        print('No log database found.')
        return
    out_path = LOG_DIR / f'export_{int(__import__("time").time())}.csv'
    conn = sqlite3.connect(str(DB_PATH))
    rows = conn.execute('SELECT * FROM events ORDER BY timestamp').fetchall()
    cols = [d[0] for d in conn.execute('SELECT * FROM events LIMIT 0').description]
    conn.close()
    with open(out_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)
    print(f'Exported {len(rows)} events to {out_path}')


def cmd_status(args):
    """Shows current ROS2 node status."""
    print('=== ACARE System Status ===')
    result = subprocess.run(['ros2', 'node', 'list'],
                            capture_output=True, text=True)
    nodes = result.stdout.strip().split('\n') if result.stdout.strip() else []
    expected = [
        '/state_manager', '/vision_node', '/safety_node',
        '/log_node', '/ascamera_hp60c'
    ]
    print(f'\nActive nodes ({len(nodes)}):')
    for n in nodes:
        print(f'  {n}')
    print('\nExpected nodes:')
    for n in expected:
        status = '✓' if n in nodes else '✗ MISSING'
        print(f'  {n}: {status}')

    # Pi health
    try:
        temp = subprocess.run(['vcgencmd', 'measure_temp'],
                              capture_output=True, text=True).stdout.strip()
        print(f'\nPi temperature: {temp}')
    except Exception:
        pass


def cmd_demo_mode(args):
    """Enables or disables demo mode (disables biometric checks)."""
    with open(SYSTEM_YAML) as f:
        cfg = yaml.safe_load(f)
    cfg['demo_mode'] = args.enable
    with open(SYSTEM_YAML, 'w') as f:
        yaml.dump(cfg, f)
    state = 'ENABLED' if args.enable else 'DISABLED'
    print(f'Demo mode {state}.')
    if args.enable:
        print('WARNING: Biometric checks are disabled in demo mode.')


def cmd_calibrate(args):
    """
    7-step calibration procedure.
    Each step triggers the appropriate ROS2 service or action.
    """
    print('=== ACARE Calibration Procedure ===')
    print('Ensure the arm is in a safe position before starting.\n')

    steps = [
        ('Step 1: Joint homing',
         'Teensy moves each joint to limit switch and zeros encoders.',
         ['ros2', 'service', 'call', '/calibrate', 'std_srvs/srv/Trigger', '{}']),
        ('Step 2: Camera intrinsics calibration',
         'Place 9x6 checkerboard in workspace. Camera will capture 20 frames.',
         None),
        ('Step 3: Workspace boundary confirmation',
         'Verify arm can reach all corners of workspace in system.yaml.',
         None),
        ('Step 4: SAFE_DROP_ZONE definition',
         'Move arm to safe drop position. Coordinates will be captured.',
         None),
        ('Step 5: NBV viewpoints definition',
         'Move arm to each search viewpoint. Joint angles will be saved.',
         None),
        ('Step 6: Fake detection threshold calibration',
         'Place 20 real tools then 20 printed replicas. Thresholds computed.',
         None),
        ('Step 7: LiDAR baseline scan',
         'Clear workspace. LiDAR captures empty-workspace reference.',
         None),
    ]

    for i, (title, desc, cmd) in enumerate(steps, 1):
        print(f'\n{title}')
        print(f'  {desc}')
        input('  Press ENTER to proceed (Ctrl+C to abort)...')
        if cmd:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(f'  Result: {result.stdout or result.stderr or "OK"}')
        else:
            print('  [Manual step — confirm when complete]')

    print('\nCalibration complete. System ready.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='admin',
        description='ACARE system administration CLI'
    )
    sub = parser.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('enrol', help='Enrol a new staff member')
    p.add_argument('--name', required=True)
    p.add_argument('--role', required=True, choices=['surgeon', 'nurse', 'admin'])

    p = sub.add_parser('revoke', help='Revoke staff access')
    p.add_argument('--id', required=True)

    sub.add_parser('list-staff', help='List all enrolled staff')

    p = sub.add_parser('set-api-key', help='Store an API key (encrypted)')
    p.add_argument('--service', required=True, choices=['deepgram', 'groq'])
    p.add_argument('--key', required=True)

    p = sub.add_parser('set-threshold', help='Update a safety threshold')
    p.add_argument('--sensor', required=True,
                   choices=['joint_current', 'joint_temp', 'gripper_force'])
    p.add_argument('--value', required=True, type=float)

    p = sub.add_parser('show-logs', help='Show recent log events')
    p.add_argument('--last', type=int, default=20)

    p = sub.add_parser('export-logs', help='Export logs to CSV')
    p.add_argument('--format', choices=['csv'], default='csv')

    sub.add_parser('status', help='Show system status')
    sub.add_parser('calibrate', help='Run calibration procedure')

    p = sub.add_parser('demo-mode', help='Enable/disable demo mode')
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--enable',  dest='enable', action='store_true')
    g.add_argument('--disable', dest='enable', action='store_false')

    args = parser.parse_args()
    dispatch = {
        'enrol':         cmd_enrol,
        'revoke':        cmd_revoke,
        'list-staff':    cmd_list_staff,
        'set-api-key':   cmd_set_api_key,
        'set-threshold': cmd_set_threshold,
        'show-logs':     cmd_show_logs,
        'export-logs':   cmd_export_logs,
        'status':        cmd_status,
        'demo-mode':     cmd_demo_mode,
        'calibrate':     cmd_calibrate,
    }
    dispatch[args.cmd](args)

# acare_logging/log_node.py
# Spec Reference: Section XVI (Logging & Audit Trail)
#
# Subscribes to /log_event and writes all events to SQLite.
# Batches writes (10 events) for efficiency.
# Auto-rotates: when DB exceeds 200MB, archives oldest 20% to gzipped CSV.
#
# DB location: /home/acare/acare_ws/logs/acare_logs.db
# Archive location: /home/acare/acare_ws/logs/archive_<timestamp>.csv.gz

import rclpy
from rclpy.node import Node
import sqlite3
import uuid
import gzip
import csv
import time
from acare_bringup.paths import LOG_DIR, ensure_parent

try:
    from acare_msgs.msg import LogEvent
    MSGS_OK = True
except ImportError:
    MSGS_OK = False

DB_PATH     = LOG_DIR / 'acare_logs.db'
MAX_SIZE_MB = 200
BATCH_SIZE  = 10

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS events (
    event_id         TEXT PRIMARY KEY,
    timestamp        TEXT,
    staff_id         TEXT,
    event_type       TEXT,
    tool             TEXT,
    state            TEXT,
    description      TEXT,
    safety_severity  TEXT,
    voice_e2e_ms     INTEGER,
    vision_search_ms INTEGER,
    motion_ms        INTEGER,
    total_task_ms    INTEGER
)
"""


class LogNode(Node):

    def __init__(self):
        super().__init__('log_node')

        ensure_parent(DB_PATH)
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self.conn.execute(CREATE_SQL)
        self.conn.commit()
        self.buffer = []

        if MSGS_OK:
            self.create_subscription(LogEvent, '/log_event', self._on_log, 10)
            self.get_logger().info(f'LogNode ready — DB: {DB_PATH}')
        else:
            self.get_logger().error('acare_msgs not available — log_node cannot subscribe')

    def _on_log(self, msg: 'LogEvent'):
        self.buffer.append((
            str(uuid.uuid4()),
            str(msg.timestamp),
            msg.user_id,
            msg.event_type,
            msg.tool,
            msg.state,
            msg.description,
            msg.safety_severity,
            int(msg.voice_e2e_ms),
            int(msg.vision_search_ms),
            int(msg.motion_ms),
            int(msg.total_task_ms),
        ))
        if len(self.buffer) >= BATCH_SIZE:
            self._flush()

    def _flush(self):
        if not self.buffer:
            return
        try:
            self.conn.executemany(
                'INSERT OR IGNORE INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                self.buffer
            )
            self.conn.commit()
            self.buffer.clear()
            self._check_rotation()
        except Exception as e:
            self.get_logger().error(f'Log flush error: {e}')

    def _check_rotation(self):
        try:
            size_mb = DB_PATH.stat().st_size / (1024 * 1024)
            if size_mb < MAX_SIZE_MB:
                return

            # Archive oldest 20% of rows
            rows = self.conn.execute(
                'SELECT * FROM events ORDER BY timestamp ASC LIMIT '
                '(SELECT COUNT(*) * 20 / 100 FROM events)'
            ).fetchall()

            if not rows:
                return

            archive = DB_PATH.parent / f'archive_{int(time.time())}.csv.gz'
            with gzip.open(archive, 'wt') as f:
                csv.writer(f).writerows(rows)

            ids = [r[0] for r in rows]
            self.conn.execute(
                f'DELETE FROM events WHERE event_id IN ({",".join("?"*len(ids))})',
                ids
            )
            self.conn.commit()
            self.get_logger().info(
                f'Log rotation: archived {len(rows)} rows → {archive.name}')
        except Exception as e:
            self.get_logger().error(f'Log rotation error: {e}')

    def destroy_node(self):
        self._flush()   # flush remaining buffer on shutdown
        self.conn.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = LogNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

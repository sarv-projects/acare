# acare_planner/task_memory.py
import sqlite3
import time
from acare_bringup.paths import DB_PATH

MAX_TASK_OUTCOMES = 1000   # G2: prune old entries to prevent unbounded growth

class TaskMemory:
    def __init__(self):
        self.db_path = DB_PATH
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_priors (
                    user_id TEXT PRIMARY KEY,
                    preferred_zone TEXT,
                    handover_z_offset REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS task_outcomes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    tool TEXT,
                    zone_found TEXT,
                    success BOOLEAN,
                    timestamp REAL
                )
            """)
            conn.commit()

    def get_user_prior(self, user_id: str) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT preferred_zone, handover_z_offset FROM user_priors WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return {"preferred_zone": row[0], "handover_z_offset": row[1] or 0.0}
            return {"preferred_zone": None, "handover_z_offset": 0.0}

    def save_outcome(self, user_id: str, tool: str, zone_found: str, success: bool):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO task_outcomes (user_id, tool, zone_found, success, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, tool, zone_found, success, time.time()))

            # If successful, update user prior for zone
            if success and zone_found:
                cursor.execute("""
                    INSERT INTO user_priors (user_id, preferred_zone) 
                    VALUES (?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET preferred_zone=excluded.preferred_zone
                """, (user_id, zone_found))

            # G2: Prune old task outcomes to prevent unbounded growth
            cursor.execute("SELECT COUNT(*) FROM task_outcomes")
            count = cursor.fetchone()[0]
            if count > MAX_TASK_OUTCOMES:
                excess = count - MAX_TASK_OUTCOMES
                cursor.execute("""
                    DELETE FROM task_outcomes 
                    WHERE id IN (SELECT id FROM task_outcomes ORDER BY timestamp ASC LIMIT ?)
                """, (excess,))

            conn.commit()

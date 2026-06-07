from __future__ import annotations

import io
import sqlite3
import time
from dataclasses import dataclass
from typing import Optional

import numpy as np

from acare_bringup.paths import USERS_DB, ensure_parent


CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    voice_emb BLOB,
    face_emb BLOB,
    registered_at INTEGER NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    handover_z_offset REAL NOT NULL DEFAULT 0.0
)
"""


def emb_to_blob(arr: Optional[np.ndarray]) -> bytes | None:
    if arr is None:
        return None
    buf = io.BytesIO()
    np.save(buf, np.asarray(arr, dtype=np.float32))
    return buf.getvalue()


def blob_to_emb(blob: bytes | None) -> Optional[np.ndarray]:
    if blob is None:
        return None
    return np.load(io.BytesIO(blob))


@dataclass
class UserRecord:
    user_id: str
    name: str
    role: str
    voice_emb: Optional[np.ndarray]
    face_emb: Optional[np.ndarray]
    registered_at: int
    active: bool
    handover_z_offset: float


class UserStore:
    def __init__(self):
        ensure_parent(USERS_DB)
        self._conn = sqlite3.connect(str(USERS_DB), check_same_thread=False)
        self._conn.execute(CREATE_TABLE)
        self._conn.commit()

    def enrol(self, name: str, role: str, voice_emb: Optional[np.ndarray], face_emb: Optional[np.ndarray]) -> UserRecord:
        user_id = f"staff_{int(time.time())}"
        record = UserRecord(
            user_id=user_id,
            name=name,
            role=role,
            voice_emb=voice_emb,
            face_emb=face_emb,
            registered_at=int(time.time()),
            active=True,
            handover_z_offset=0.0,
        )
        self._conn.execute(
            """
            INSERT INTO users (id, name, role, voice_emb, face_emb, registered_at, active, handover_z_offset)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.user_id,
                record.name,
                record.role,
                emb_to_blob(record.voice_emb),
                emb_to_blob(record.face_emb),
                record.registered_at,
                1,
                record.handover_z_offset,
            ),
        )
        self._conn.commit()
        return record

    def latest_active(self) -> Optional[UserRecord]:
        row = self._conn.execute(
            """
            SELECT id, name, role, voice_emb, face_emb, registered_at, active, handover_z_offset
            FROM users WHERE active=1 ORDER BY registered_at DESC LIMIT 1
            """
        ).fetchone()
        return self._row_to_record(row)

    def get(self, user_id: str) -> Optional[UserRecord]:
        row = self._conn.execute(
            """
            SELECT id, name, role, voice_emb, face_emb, registered_at, active, handover_z_offset
            FROM users WHERE id=?
            """,
            (user_id,),
        ).fetchone()
        return self._row_to_record(row)

    def all_active(self) -> list[UserRecord]:
        rows = self._conn.execute(
            """
            SELECT id, name, role, voice_emb, face_emb, registered_at, active, handover_z_offset
            FROM users WHERE active=1 ORDER BY registered_at
            """
        ).fetchall()
        return [self._row_to_record(row) for row in rows if row]

    def update_handover_offset(self, user_id: str, offset_m: float):
        self._conn.execute(
            "UPDATE users SET handover_z_offset=? WHERE id=?",
            (float(max(min(offset_m, 0.15), -0.15)), user_id),
        )
        self._conn.commit()

    def update_voice_embedding(self, user_id: str, voice_emb: Optional[np.ndarray]):
        self._conn.execute(
            "UPDATE users SET voice_emb=? WHERE id=?",
            (emb_to_blob(voice_emb), user_id),
        )
        self._conn.commit()

    def update_face_embedding(self, user_id: str, face_emb: Optional[np.ndarray]):
        self._conn.execute(
            "UPDATE users SET face_emb=? WHERE id=?",
            (emb_to_blob(face_emb), user_id),
        )
        self._conn.commit()

    def _row_to_record(self, row) -> Optional[UserRecord]:
        if not row:
            return None
        return UserRecord(
            user_id=row[0],
            name=row[1],
            role=row[2],
            voice_emb=blob_to_emb(row[3]),
            face_emb=blob_to_emb(row[4]),
            registered_at=int(row[5]),
            active=bool(row[6]),
            handover_z_offset=float(row[7]),
        )

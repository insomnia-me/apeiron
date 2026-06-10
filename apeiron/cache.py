from __future__ import annotations

import hashlib
import sqlite3
import threading
from pathlib import Path
from typing import Optional

from apeiron.config import CACHE_DIR


class ResponseCache:
    """SQLite-backed response cache with TTL."""

    _local = threading.local()

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or (CACHE_DIR / "apeiron_cache.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @property
    def conn(self):
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(str(self.db_path))
            self._local.conn.execute("PRAGMA journal_mode=WAL")
        return self._local.conn

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT,
                created_at REAL
            )
        """)
        self.conn.commit()

    def _key(self, url: str) -> str:
        return hashlib.sha256(url.encode()).hexdigest()

    def get(self, url: str, ttl_seconds: int = 300) -> Optional[str]:
        import time
        key = self._key(url)
        row = self.conn.execute(
            "SELECT value, created_at FROM cache WHERE key = ?", (key,)
        ).fetchone()
        if row and (time.time() - row[1]) < ttl_seconds:
            return row[0]
        return None

    def set(self, url: str, value: str):
        import time
        key = self._key(url)
        self.conn.execute(
            "INSERT OR REPLACE INTO cache (key, value, created_at) VALUES (?, ?, ?)",
            (key, value, time.time()),
        )
        self.conn.commit()

    def clear(self):
        self.conn.execute("DELETE FROM cache")
        self.conn.commit()

from __future__ import annotations

import hashlib
import os
import sqlite3
import threading
from pathlib import Path
from typing import Optional

from apeiron.config import CACHE_DIR


class ResponseCache:
    """SQLite-backed response cache with TTL."""

    def __init__(self, db_path: Optional[Path] = None):
        self._local = threading.local()
        env_db_path = os.getenv("APEIRON_CACHE_DB")
        self.db_path = db_path or (Path(env_db_path) if env_db_path else CACHE_DIR / "apeiron_cache.db")
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
                url TEXT,
                value TEXT,
                created_at REAL
            )
        """)
        columns = {row[1] for row in self.conn.execute("PRAGMA table_info(cache)").fetchall()}
        if "url" not in columns:
            self.conn.execute("ALTER TABLE cache ADD COLUMN url TEXT")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_cache_created_at ON cache(created_at)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_cache_url ON cache(url)")
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
            "INSERT OR REPLACE INTO cache (key, url, value, created_at) VALUES (?, ?, ?, ?)",
            (key, url, value, time.time()),
        )
        self.conn.commit()

    def list_entries(self, limit: int = 50) -> list[dict]:
        rows = self.conn.execute(
            """
            SELECT url, value, created_at
            FROM cache
            WHERE url IS NOT NULL
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [_entry_from_row(row) for row in rows]

    def search(self, query: str, limit: int = 20) -> list[dict]:
        needle = f"%{query}%"
        rows = self.conn.execute(
            """
            SELECT url, value, created_at
            FROM cache
            WHERE url IS NOT NULL AND (url LIKE ? OR value LIKE ?)
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (needle, needle, limit),
        ).fetchall()
        return [_entry_from_row(row) for row in rows]

    def clear(self):
        self.conn.execute("DELETE FROM cache")
        self.conn.commit()


def _entry_from_row(row) -> dict:
    url, value, created_at = row
    return {
        "url": url,
        "created_at": created_at,
        "chars": len(value or ""),
        "preview": (value or "")[:240],
    }

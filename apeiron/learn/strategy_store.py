from __future__ import annotations

import json
from typing import Optional
from urllib.parse import urlparse

from apeiron.config import STRATEGIES_PATH
from apeiron.types import Tier


class StrategyStore:
    """Persists best tier per domain so future fetches skip straight to it."""

    def __init__(self):
        self._data: dict[str, str] = {}
        self._load()

    def _load(self):
        if STRATEGIES_PATH.exists():
            try:
                self._data = json.loads(STRATEGIES_PATH.read_text())
            except Exception:
                self._data = {}

    def _save(self):
        STRATEGIES_PATH.parent.mkdir(parents=True, exist_ok=True)
        STRATEGIES_PATH.write_text(json.dumps(self._data, indent=2))

    @staticmethod
    def _domain(url: str) -> str:
        return urlparse(url).netloc or url

    def get(self, url: str) -> Optional[Tier]:
        domain = self._domain(url)
        raw = self._data.get(domain)
        if raw:
            try:
                return Tier(raw)
            except ValueError:
                return None
        return None

    def set(self, url: str, tier: Tier):
        domain = self._domain(url)
        self._data[domain] = tier.value
        self._save()

    def all(self) -> dict[str, str]:
        return dict(self._data)

    def count(self) -> int:
        return len(self._data)

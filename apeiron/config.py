from __future__ import annotations

import os
from pathlib import Path
from apeiron.types import Tier

# ── Paths ──────────────────────────────────────────────────
PROJECT_DIR = Path(__file__).resolve().parent.parent
STRATEGIES_PATH = PROJECT_DIR / "strategies.json"
DEFAULT_CACHE = Path(os.getenv("XDG_CACHE_HOME", Path.home() / ".cache")) / "apeiron"
CACHE_DIR = Path(os.getenv("APEIRON_CACHE_DIR", str(DEFAULT_CACHE)))

# ── Infrastructure ─────────────────────────────────────────
SEARXNG_BASE = os.getenv("APEIRON_SEARXNG", "http://localhost:4004")
FLARESOLVERR_BASE = os.getenv("APEIRON_FLARESOLVERR", "http://localhost:8191")

# ── Tiers ──────────────────────────────────────────────────
DEFAULT_TIER = Tier.CLOAKBROWSER  # ★ default if no strategy known

# ── Politeness ─────────────────────────────────────────────
DELAY_BETWEEN_REQUESTS = float(os.getenv("APEIRON_DELAY", "1.0"))
MAX_RETRIES = int(os.getenv("APEIRON_MAX_RETRIES", "3"))

# ── Search ─────────────────────────────────────────────────
MAX_SEARCH_RESULTS = int(os.getenv("APEIRON_MAX_SEARCH", "10"))

# ── Git ops ────────────────────────────────────────────────
GIT_AUTO_COMMIT = os.getenv("APEIRON_GIT_COMMIT", "false").lower() == "true"


def tier_from_str(s: str) -> Tier:
    try:
        return Tier(s)
    except ValueError:
        return DEFAULT_TIER

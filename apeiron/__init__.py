"""Apeiron (ἄπειρον) — Unlimited Web Access for AI Agents.

Self-learning, tiered-escalation scraper that combines every free anti-bot
technology into one autonomous agent. Bypasses Cloudflare, Turnstile, Anubis,
reCAPTCHA, and any other wall between an AI and the information it needs.

Core philosophy: information wants to be free. Apeiron is the tool that
makes it so.

    from apeiron import search, fetch

    results = search("quantum computing 2026")
    content = fetch("https://arxiv.org/pdf/2203.02155.pdf")
    content = fetch("https://youtube.com/watch?v=dQw4w9WgXcQ")
    content = fetch("https://cloudflare-protected.site")
"""
from __future__ import annotations

from apeiron.version import __version__

from apeiron.api.python_api import fetch, fetch_sync, search, search_sync, learn, learn_sync
from apeiron.types import FetchResult, ScrapeResult, SearchHit, Source, Tier, Verdict

__all__ = [
    "__version__",
    "search", "search_sync",
    "fetch", "fetch_sync",
    "learn", "learn_sync",
    "FetchResult", "ScrapeResult", "SearchHit",
    "Source", "Tier", "Verdict",
]

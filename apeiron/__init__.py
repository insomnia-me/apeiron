"""Apeiron — local-first web search, fetch, and extraction tools for AI agents.

Apeiron provides a CLI, Python API, and MCP server for agent workflows that
need search results, fetched URL content, extraction, diagnostics, and local
per-domain strategy learning.

    from apeiron import search_sync, fetch_sync, learn_sync

    results = search_sync("agent web access")
    result = fetch_sync("https://example.com", cache_ttl=0)
    learned = learn_sync("https://example.com")
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

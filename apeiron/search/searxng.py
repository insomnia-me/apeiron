from __future__ import annotations

import httpx

from apeiron.config import SEARXNG_BASE
from apeiron.types import SearchHit, Source


async def search_searxng(query: str, max_results: int = 10) -> list[SearchHit]:
    try:
        params: dict[str, str | int] = {
            "q": query,
            "format": "json",
            "language": "en",
            "categories": "general,news,science",
            "pageno": 1,
        }
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(f"{SEARXNG_BASE}/search", params=params)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return []

    hits = []
    for r in data.get("results", [])[:max_results]:
        hits.append(SearchHit(
            title=r.get("title", ""),
            url=r.get("url", ""),
            snippet=r.get("content", ""),
            source=Source.WEB,
        ))
    return hits


def search_searxng_sync(query: str, max_results: int = 10) -> list[SearchHit]:
    import asyncio
    return asyncio.run(search_searxng(query, max_results))

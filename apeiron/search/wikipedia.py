from __future__ import annotations

import httpx
from apeiron.types import SearchHit, Source

API_BASE = "https://en.wikipedia.org/api/rest_v1"


async def search_wikipedia(query: str, max_results: int = 5) -> list[SearchHit]:
    try:
        params = {
            "q": query,
            "limit": max_results,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{API_BASE}/search/title", params=params)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return []

    hits = []
    for page in data.get("pages", [])[:max_results]:
        hits.append(SearchHit(
            title=page.get("title", ""),
            url=f"https://en.wikipedia.org/wiki/{page.get('title', '').replace(' ', '_')}",
            snippet=page.get("excerpt", ""),
            source=Source.WIKIPEDIA,
        ))
    return hits


async def fetch_wikipedia(title: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{API_BASE}/page/summary/{title}")
            resp.raise_for_status()
            data = resp.json()
            return data.get("extract", "")
    except Exception:
        return ""

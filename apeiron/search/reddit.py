from __future__ import annotations

import httpx
from apeiron.types import SearchHit, Source


async def search_reddit(query: str, max_results: int = 5) -> list[SearchHit]:
    try:
        url = f"https://www.reddit.com/search.json?q={query}&limit={max_results}&sort=relevance"
        headers = {"User-Agent": "apeiron/0.1 (by insomnia)"}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return []

    hits = []
    for child in data.get("data", {}).get("children", [])[:max_results]:
        d = child.get("data", {})
        hits.append(SearchHit(
            title=d.get("title", ""),
            url=f"https://reddit.com{d.get('permalink', '')}",
            snippet=d.get("selftext", "")[:200] or d.get("url", ""),
            source=Source.REDDIT,
        ))
    return hits

from __future__ import annotations

import httpx
from apeiron.types import SearchHit, Source


async def search_github(query: str, max_results: int = 5) -> list[SearchHit]:
    try:
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": max_results,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get("https://api.github.com/search/repositories", params=params)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return []

    hits = []
    for repo in data.get("items", [])[:max_results]:
        hits.append(SearchHit(
            title=repo.get("full_name", ""),
            url=repo.get("html_url", ""),
            snippet=repo.get("description", "") or "",
            source=Source.GITHUB,
        ))
    return hits

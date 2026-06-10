from __future__ import annotations

import httpx
from apeiron.types import SearchHit, Source

API_BASE = "https://api.semanticscholar.org/graph/v1/paper/search"


async def search_semantic_scholar(query: str, max_results: int = 5) -> list[SearchHit]:
    try:
        params = {
            "query": query,
            "limit": max_results,
            "fields": "title,url,abstract,citationCount",
        }
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(API_BASE, params=params)
            if resp.status_code == 429:
                return []
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return []

    hits = []
    for paper in data.get("data", [])[:max_results]:
        hits.append(SearchHit(
            title=paper.get("title", ""),
            url=paper.get("url", "") or f"https://semanticscholar.org/paper/{paper.get('paperId', '')}",
            snippet=f"Citations: {paper.get('citationCount', 0)}",
            source=Source.SEMANTIC_SCHOLAR,
        ))
    return hits

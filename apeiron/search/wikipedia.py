from __future__ import annotations

import httpx
from apeiron.types import SearchHit, Source

API_BASE = "https://en.wikipedia.org/w/api.php"


async def search_wikipedia(query: str, max_results: int = 5) -> list[SearchHit]:
    try:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": max_results,
            "format": "json",
            "origin": "*",
        }
        headers = {
            "User-Agent": "Apeiron/0.1 (unlimited web access for AI agents; https://github.com/insomnia-me/apeiron)"
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(API_BASE, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return []

    hits = []
    for page in data.get("query", {}).get("search", [])[:max_results]:
        title = page.get("title", "")
        hits.append(SearchHit(
            title=title,
            url=f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
            snippet=page.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", ""),
            source=Source.WIKIPEDIA,
        ))
    return hits


async def fetch_wikipedia(title: str) -> str:
    try:
        params = {
            "action": "query",
            "titles": title,
            "prop": "extracts",
            "explaintext": True,
            "exlimit": 1,
            "format": "json",
            "origin": "*",
        }
        headers = {
            "User-Agent": "Apeiron/0.1 (unlimited web access for AI agents; https://github.com/insomnia-me/apeiron)"
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(API_BASE, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            pages = data.get("query", {}).get("pages", {})
            for pid, info in pages.items():
                if pid != "-1":
                    return info.get("extract", "")
    except Exception:
        pass
    return ""

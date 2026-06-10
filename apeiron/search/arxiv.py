from __future__ import annotations

import httpx
from apeiron.types import SearchHit, Source

ARXIV_BASE = "http://export.arxiv.org/api/query"


async def search_arxiv(query: str, max_results: int = 5) -> list[SearchHit]:
    try:
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
        }
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(ARXIV_BASE, params=params)
            resp.raise_for_status()
            text = resp.text
    except Exception:
        return []

    import xml.etree.ElementTree as ET
    ns = {"a": "http://www.w3.org/2005/Atom"}
    hits = []
    root = ET.fromstring(text)
    for entry in root.findall("a:entry", ns)[:max_results]:
        title = entry.find("a:title", ns)
        summary = entry.find("a:summary", ns)
        link = entry.find("a:id", ns) or entry.find("a:link", ns)
        hits.append(SearchHit(
            title=(title.text or "").replace("\n", " ").strip() if title is not None else "",
            url=link.text.strip() if link is not None and link.text else "",
            snippet=(summary.text or "").replace("\n", " ").strip()[:300] if summary is not None else "",
            source=Source.ARXIV,
        ))
    return hits

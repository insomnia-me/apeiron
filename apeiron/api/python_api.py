from __future__ import annotations

from typing import Optional

from apeiron.learn.auto_detect import fetch as _fetch, learn as _learn
from apeiron.search.searxng import search_searxng
from apeiron.search.arxiv import search_arxiv
from apeiron.search.semantic_scholar import search_semantic_scholar
from apeiron.search.wikipedia import search_wikipedia
from apeiron.search.reddit import search_reddit
from apeiron.search.github import search_github
from apeiron.types import FetchResult, SearchHit, Source


async def search(query: str, sources: Optional[list[Source]] = None, max_results: int = 10) -> list[SearchHit]:
    """Search across multiple sources. Returns LLM-ready results."""
    if sources is None:
        sources = [Source.WEB, Source.ARXIV, Source.WIKIPEDIA, Source.GITHUB]

    all_hits: list[SearchHit] = []

    tasks = []
    source_map = {
        Source.WEB: (search_searxng, "web"),
        Source.ARXIV: (search_arxiv, "arxiv"),
        Source.SEMANTIC_SCHOLAR: (search_semantic_scholar, "semantic scholar"),
        Source.WIKIPEDIA: (search_wikipedia, "wikipedia"),
        Source.REDDIT: (search_reddit, "reddit"),
        Source.GITHUB: (search_github, "github"),
    }

    import asyncio

    for src in sources:
        if src in source_map:
            fn, _ = source_map[src]
            tasks.append(fn(query, max_results=max(3, max_results // len(sources))))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for r in results:
        if isinstance(r, list):
            all_hits.extend(r)

    all_hits.sort(key=lambda h: h.score, reverse=True)
    return all_hits[:max_results]


async def fetch(url: str, cache_ttl: int = 300, proxy: str | None = None) -> FetchResult:
    """Fetch a URL and extract clean LLM-ready text when a tier succeeds."""
    return await _fetch(url, cache_ttl)


async def learn(url: str) -> FetchResult:
    """Proactively learn the best strategy for a domain."""
    return await _learn(url)


def search_sync(query: str, sources: Optional[list[Source]] = None, max_results: int = 10) -> list[SearchHit]:
    import asyncio
    return asyncio.run(search(query, sources, max_results))


def fetch_sync(url: str, cache_ttl: int = 300) -> FetchResult:
    import asyncio
    return asyncio.run(fetch(url, cache_ttl))


def learn_sync(url: str) -> FetchResult:
    import asyncio
    return asyncio.run(learn(url))

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from apeiron.api.python_api import search, fetch, learn
from apeiron.types import Source


mcp = FastMCP("apeiron")


@mcp.tool()
async def apeiron_search(
    query: str,
    sources: list[str] | None = None,
    max_results: int = 10,
) -> str:
    """Search the web across multiple sources (SearXNG, arXiv, Wikipedia, Reddit, GitHub). Returns LLM-ready results.

    Args:
        query: Search query
        sources: Sources to search (default: all). Options: searxng, arxiv, wikipedia, reddit, github
        max_results: Max results (default: 10)
    """
    srcs = [Source(s) for s in sources] if sources else None
    results = await search(query=query, sources=srcs, max_results=max_results)
    return json.dumps([
        {
            "title": r.title,
            "url": r.url,
            "snippet": r.snippet,
            "source": r.source.value,
        }
        for r in results
    ], indent=2, ensure_ascii=False)


@mcp.tool()
async def apeiron_fetch(url: str, cache_ttl: int = 300) -> str:
    """Fetch a URL and return structured LLM-ready content plus diagnostics.

    Args:
        url: URL to fetch
        cache_ttl: Cache TTL in seconds (default: 300)
    """
    result = await fetch(url=url, cache_ttl=cache_ttl)
    return json.dumps({
        "url": result.url,
        "content": result.content,
        "tier": result.tier.value,
        "verdict": result.verdict.value,
        "content_type": result.content_type,
        "title": result.title,
        "elapsed_ms": result.elapsed_ms,
        "error": result.error,
        "confidence": result.confidence,
        "warnings": result.warnings,
    }, indent=2, ensure_ascii=False)


@mcp.tool()
async def apeiron_learn(url: str) -> str:
    """Proactively learn the best strategy for a domain. Tries all tiers and saves the best one.

    Args:
        url: URL on the domain to learn
    """
    result = await learn(url=url)
    return json.dumps({
        "url": result.url,
        "tier": result.tier.value,
        "verdict": result.verdict.value,
        "content_type": result.content_type,
        "title": result.title,
        "elapsed_ms": result.elapsed_ms,
        "error": result.error,
        "confidence": result.confidence,
        "warnings": result.warnings,
    }, indent=2, ensure_ascii=False)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

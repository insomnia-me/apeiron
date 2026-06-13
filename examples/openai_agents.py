from __future__ import annotations

import json

from agents import Agent, Runner, function_tool
from apeiron import fetch_sync, search_sync


@function_tool
def apeiron_fetch(url: str) -> str:
    """Fetch a public URL and return LLM-ready content with diagnostics."""
    result = fetch_sync(url, cache_ttl=300)
    return json.dumps(
        {
            "url": result.url,
            "content": result.content[:12000],
            "tier": result.tier.value,
            "verdict": result.verdict.value,
            "content_type": result.content_type,
            "title": result.title,
            "error": result.error,
        },
        ensure_ascii=False,
    )


@function_tool
def apeiron_search(query: str, max_results: int = 5) -> str:
    """Search public web-oriented sources and return ranked hits."""
    hits = search_sync(query, max_results=max_results)
    return json.dumps(
        [
            {
                "title": hit.title,
                "url": hit.url,
                "snippet": hit.snippet,
                "source": hit.source.value,
                "score": hit.score,
            }
            for hit in hits
        ],
        ensure_ascii=False,
    )


agent = Agent(
    name="Research agent",
    instructions="Use Apeiron tools when you need to search or read public web sources.",
    tools=[apeiron_search, apeiron_fetch],
)


if __name__ == "__main__":
    result = Runner.run_sync(agent, "Find and summarize the Python packaging guide.")
    print(result.final_output)

from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent

from apeiron.api.python_api import search, fetch, learn
from apeiron.types import Source


server = Server("apeiron")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="apeiron_search",
            description="Search the web across multiple sources (SearXNG, arXiv, Wikipedia, Reddit, GitHub). Returns LLM-ready results.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "sources": {
                        "type": "array",
                        "items": {"type": "string", "enum": [s.value for s in Source]},
                        "description": "Sources to search (default: all)",
                    },
                    "max_results": {"type": "integer", "description": "Max results (default: 10)"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="apeiron_fetch",
            description="Fetch any URL and extract clean LLM-ready text. Handles HTML, PDF, YouTube, and more. Automatically bypasses Cloudflare, Turnstile, CAPTCHA.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to fetch"},
                    "cache_ttl": {"type": "integer", "description": "Cache TTL in seconds (default: 300)"},
                },
                "required": ["url"],
            },
        ),
        Tool(
            name="apeiron_learn",
            description="Proactively learn the best strategy for a domain. Tries all tiers and saves the best one.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL on the domain to learn"},
                },
                "required": ["url"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    try:
        if name == "apeiron_search":
            sources = arguments.get("sources")
            if sources:
                sources = [Source(s) for s in sources]
            results = await search(
                query=arguments["query"],
                sources=sources,
                max_results=arguments.get("max_results", 10),
            )
            output = json.dumps([{
                "title": r.title,
                "url": r.url,
                "snippet": r.snippet,
                "source": r.source.value,
            } for r in results], indent=2, ensure_ascii=False)
            return [TextContent(type="text", text=output)]

        elif name == "apeiron_fetch":
            result = await fetch(url=arguments["url"], cache_ttl=arguments.get("cache_ttl", 300))
            return [TextContent(type="text", text=result.content)]

        elif name == "apeiron_learn":
            result = await learn(url=arguments["url"])
            status = f"Best tier: {result.tier.value}, verdict: {result.verdict.value}"
            return [TextContent(type="text", text=status)]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]


async def main():
    async with server.run() as running:
        await running


if __name__ == "__main__":
    asyncio.run(main())

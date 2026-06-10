#!/usr/bin/env python3
"""Apeiron CLI — apeiron search|fetch|learn|serve <args>"""

from __future__ import annotations

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="apeiron",
        description="Apeiron (ἄπειρον) — Unlimited Web Access for AI Agents",
    )
    sub = parser.add_subparsers(dest="cmd")

    # search
    p_search = sub.add_parser("search", help="Search across multiple sources")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--sources", nargs="*", default=None, help="Sources: web arxiv wikipedia reddit github")
    p_search.add_argument("--max", type=int, default=10, help="Max results")

    # fetch
    p_fetch = sub.add_parser("fetch", help="Fetch any URL and extract clean text")
    p_fetch.add_argument("url", help="URL to fetch")
    p_fetch.add_argument("--no-cache", action="store_true", help="Bypass cache")
    p_fetch.add_argument("--output", "-o", help="Save output to file")

    # learn
    p_learn = sub.add_parser("learn", help="Learn best strategy for a domain")
    p_learn.add_argument("url", help="URL to learn from")

    # serve
    p_serve = sub.add_parser("serve", help="Start MCP server")

    args = parser.parse_args()

    if args.cmd == "search":
        _cmd_search(args)
    elif args.cmd == "fetch":
        _cmd_fetch(args)
    elif args.cmd == "learn":
        _cmd_learn(args)
    elif args.cmd == "serve":
        _cmd_serve()
    else:
        parser.print_help()


def _cmd_search(args):
    import asyncio
    from apeiron.api.python_api import search as search_fn
    from apeiron.types import Source

    sources = None
    if args.sources:
        source_map = {
            "web": Source.WEB, "arxiv": Source.ARXIV,
            "semantic": Source.SEMANTIC_SCHOLAR, "scholar": Source.SEMANTIC_SCHOLAR,
            "wikipedia": Source.WIKIPEDIA, "wiki": Source.WIKIPEDIA,
            "reddit": Source.REDDIT, "github": Source.GITHUB,
        }
        sources = [source_map[s.lower()] for s in args.sources if s.lower() in source_map]

    results = asyncio.run(search_fn(args.query, sources, args.max))

    for r in results:
        print(f"\n── {r.source.value} ────────────────────────────────────────")
        print(f"  {r.title}")
        print(f"  {r.url}")
        print(f"  {r.snippet[:200]}")


def _cmd_fetch(args):
    import asyncio
    from apeiron.api.python_api import fetch as fetch_fn

    result = asyncio.run(fetch_fn(args.url, cache_ttl=0 if args.no_cache else 300))

    if args.output:
        with open(args.output, "w") as f:
            f.write(result.content)
        print(f"Saved to {args.output}")
    else:
        print(result.content)


def _cmd_learn(args):
    import asyncio
    from apeiron.api.python_api import learn as learn_fn

    result = asyncio.run(learn_fn(args.url))
    print(f"Domain: {args.url}")
    print(f"Best tier: {result.tier.value}")
    print(f"Verdict: {result.verdict.value}")


def _cmd_serve():
    from apeiron.api.mcp_server import main
    import asyncio
    asyncio.run(main())


if __name__ == "__main__":
    main()

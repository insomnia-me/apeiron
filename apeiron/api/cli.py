#!/usr/bin/env python3
"""Apeiron CLI — apeiron search|fetch|learn|serve <args>"""

from __future__ import annotations

import argparse
import json


def main(fetch_fn=None):
    parser = argparse.ArgumentParser(
        prog="apeiron",
        description="Apeiron — local-first web search, fetch, and extraction tools for AI agents",
    )
    sub = parser.add_subparsers(dest="cmd")

    # search
    p_search = sub.add_parser("search", help="Search across multiple sources")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--sources", nargs="*", default=None, help="Sources: web arxiv wikipedia reddit github")
    p_search.add_argument("--max", type=int, default=10, help="Max results")
    p_search.add_argument("--json", action="store_true", help="Print structured JSON")

    # fetch
    p_fetch = sub.add_parser("fetch", help="Fetch a URL and extract clean text")
    p_fetch.add_argument("url", help="URL to fetch")
    p_fetch.add_argument("--no-cache", action="store_true", help="Bypass cache")
    p_fetch.add_argument("--output", "-o", help="Save output to file")
    p_fetch.add_argument("--json", action="store_true", help="Print structured JSON")

    # research
    p_research = sub.add_parser("research", help="Search, fetch, and assemble a Markdown research report")
    p_research.add_argument("query", help="Research query")
    p_research.add_argument("--sources", nargs="*", default=None, help="Sources: web arxiv wikipedia github")
    p_research.add_argument("--max", type=int, default=5, help="Max unique sources to fetch")
    p_research.add_argument("--cache-ttl", type=int, default=300, help="Cache TTL for source fetches")
    p_research.add_argument("--max-chars", type=int, default=6000, help="Max characters per source in Markdown")
    p_research.add_argument("--markdown", "-m", help="Write Markdown report to file")
    p_research.add_argument("--json", action="store_true", help="Print structured JSON")

    # learn
    p_learn = sub.add_parser("learn", help="Learn best strategy for a domain")
    p_learn.add_argument("url", help="URL to learn from")
    p_learn.add_argument("--json", action="store_true", help="Print structured JSON")

    # serve
    sub.add_parser("serve", help="Start MCP server")

    # doctor
    p_doctor = sub.add_parser("doctor", help="Check optional dependencies and local services")
    p_doctor.add_argument("--json", action="store_true", help="Print structured JSON")

    # bench
    p_bench = sub.add_parser("bench", help="Run the bundled web access benchmark")
    p_bench.add_argument("--json", action="store_true", help="Print structured JSON")
    p_bench.add_argument("--cache-ttl", type=int, default=0, help="Cache TTL for benchmark fetches")

    # init
    p_init = sub.add_parser("init", help="Generate agent integration config or wrapper files")
    p_init.add_argument("--target", choices=["claude", "cursor", "opencode", "openai-agents"], required=True)
    p_init.add_argument("--output", default=".", help="Directory to write generated files")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing files")

    # demo
    p_demo = sub.add_parser("demo", help="Start a local visual fetch demo")
    p_demo.add_argument("--host", default="127.0.0.1", help="Host to bind")
    p_demo.add_argument("--port", type=int, default=8765, help="Port to bind")
    p_demo.add_argument("--no-open", action="store_true", help="Do not open a browser")

    # cache
    p_cache = sub.add_parser("cache", help="Inspect or clear the local response cache")
    cache_sub = p_cache.add_subparsers(dest="cache_cmd")
    p_cache_list = cache_sub.add_parser("list", help="List recent cached fetches")
    p_cache_list.add_argument("--limit", type=int, default=50)
    p_cache_list.add_argument("--json", action="store_true", help="Print structured JSON")
    p_cache_search = cache_sub.add_parser("search", help="Search cached URLs and content")
    p_cache_search.add_argument("query")
    p_cache_search.add_argument("--limit", type=int, default=20)
    p_cache_search.add_argument("--json", action="store_true", help="Print structured JSON")
    p_cache_clear = cache_sub.add_parser("clear", help="Clear cached fetches")
    p_cache_clear.add_argument("--json", action="store_true", help="Print structured JSON")

    args = parser.parse_args()

    if args.cmd == "search":
        _cmd_search(args)
    elif args.cmd == "fetch":
        _cmd_fetch(args)
    elif args.cmd == "research":
        _cmd_research(args)
    elif args.cmd == "learn":
        _cmd_learn(args)
    elif args.cmd == "serve":
        _cmd_serve()
    elif args.cmd == "doctor":
        _cmd_doctor(args)
    elif args.cmd == "bench":
        _cmd_bench(args, fetch_fn=fetch_fn)
    elif args.cmd == "init":
        _cmd_init(args)
    elif args.cmd == "demo":
        _cmd_demo(args)
    elif args.cmd == "cache":
        _cmd_cache(args)
    else:
        parser.print_help()


def _cmd_search(args):
    import asyncio
    from apeiron.api.python_api import search as search_fn

    sources = None
    if args.sources:
        sources = _parse_sources(args.sources)

    results = asyncio.run(search_fn(args.query, sources, args.max))

    if args.json:
        print(json.dumps([
            {
                "title": r.title,
                "url": r.url,
                "snippet": r.snippet,
                "source": r.source.value,
                "score": r.score,
            }
            for r in results
        ], indent=2, ensure_ascii=False))
        return

    for r in results:
        print(f"\n── {r.source.value} ────────────────────────────────────────")
        print(f"  {r.title}")
        print(f"  {r.url}")
        print(f"  {r.snippet[:200]}")


def _cmd_fetch(args):
    import asyncio
    from apeiron.api.python_api import fetch as fetch_fn

    result = asyncio.run(fetch_fn(args.url, cache_ttl=0 if args.no_cache else 300))

    if args.json:
        print(json.dumps(_fetch_result_payload(result), indent=2, ensure_ascii=False))
        return

    if args.output:
        with open(args.output, "w") as f:
            f.write(result.content)
        print(f"Saved to {args.output}")
    else:
        print(result.content)


def _cmd_research(args):
    import asyncio
    from apeiron.research import run_research

    selected_sources = _parse_sources(args.sources) if args.sources else None
    report = asyncio.run(
        run_research(
            args.query,
            sources=selected_sources,
            max_results=args.max,
            cache_ttl=args.cache_ttl,
            max_chars_per_source=args.max_chars,
        )
    )

    if args.markdown:
        with open(args.markdown, "w") as f:
            f.write(report.markdown)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
        return

    if args.markdown:
        print(f"Saved research report to {args.markdown}")
    else:
        print(report.markdown)


def _cmd_learn(args):
    import asyncio
    from apeiron.api.python_api import learn as learn_fn

    result = asyncio.run(learn_fn(args.url))
    if args.json:
        print(json.dumps(_fetch_result_payload(result), indent=2, ensure_ascii=False))
        return
    print(f"Domain: {args.url}")
    print(f"Best tier: {result.tier.value}")
    print(f"Verdict: {result.verdict.value}")


def _cmd_serve():
    from apeiron.api.mcp_server import main
    import asyncio
    asyncio.run(main())


def _cmd_doctor(args):
    from apeiron.doctor import collect_diagnostics, format_diagnostics

    report = collect_diagnostics()
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_diagnostics(report))


def _cmd_bench(args, fetch_fn=None):
    import asyncio
    from apeiron.benchmarks import format_benchmark_report, run_benchmark

    kwargs = {"cache_ttl": args.cache_ttl}
    if fetch_fn is not None:
        kwargs["fetch_fn"] = fetch_fn
    report = asyncio.run(run_benchmark(**kwargs))
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(format_benchmark_report(report))


def _cmd_init(args):
    from apeiron.init import generate_init_files

    written = generate_init_files(args.target, args.output, force=args.force)
    for path in written:
        print(f"Wrote {path}")


def _cmd_demo(args):
    from apeiron.demo import run_demo

    run_demo(host=args.host, port=args.port, open_browser=not args.no_open)


def _cmd_cache(args):
    from apeiron.cache import ResponseCache

    cache = ResponseCache()
    if args.cache_cmd == "list":
        entries = cache.list_entries(limit=args.limit)
        _print_cache_entries(entries, as_json=args.json)
        return
    if args.cache_cmd == "search":
        entries = cache.search(args.query, limit=args.limit)
        _print_cache_entries(entries, as_json=args.json)
        return
    if args.cache_cmd == "clear":
        cache.clear()
        payload = {"cleared": True}
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print("Cleared cache")
        return
    print("Usage: apeiron cache list|search|clear")


def _print_cache_entries(entries: list[dict], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(entries, indent=2, ensure_ascii=False))
        return
    for entry in entries:
        print(f"{entry['url']} ({entry['chars']} chars)")
        if entry["preview"]:
            print(f"  {entry['preview'][:120]}")


def _parse_sources(source_names: list[str]):
    from apeiron.types import Source

    source_map = {
        "web": Source.WEB,
        "arxiv": Source.ARXIV,
        "semantic": Source.SEMANTIC_SCHOLAR,
        "scholar": Source.SEMANTIC_SCHOLAR,
        "wikipedia": Source.WIKIPEDIA,
        "wiki": Source.WIKIPEDIA,
        "reddit": Source.REDDIT,
        "github": Source.GITHUB,
    }
    return [source_map[name.lower()] for name in source_names if name.lower() in source_map]


def _fetch_result_payload(result):
    return {
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
    }


if __name__ == "__main__":
    main()

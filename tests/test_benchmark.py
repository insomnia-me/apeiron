from __future__ import annotations

import json
import sys

import pytest

from apeiron.types import FetchResult, Tier, Verdict


def test_load_default_cases_includes_realistic_categories():
    from apeiron.benchmarks import load_default_cases

    cases = load_default_cases()

    assert len(cases) >= 8
    assert {case.category for case in cases} >= {"html", "docs", "research", "media"}
    assert all(case.url.startswith("http") for case in cases)
    assert all(case.min_chars > 0 for case in cases)


@pytest.mark.asyncio
async def test_run_benchmark_scores_successful_extractions():
    from apeiron.benchmarks import BenchmarkCase, run_benchmark

    cases = [
        BenchmarkCase(id="ok", url="https://example.com", category="html", min_chars=5),
        BenchmarkCase(id="short", url="https://short.example", category="html", min_chars=20),
        BenchmarkCase(id="blocked", url="https://blocked.example", category="html", min_chars=5),
    ]

    async def fake_fetch(url: str, cache_ttl: int = 0):
        if "blocked" in url:
            return FetchResult(url=url, content="", tier=Tier.FAST, verdict=Verdict.BLOCKED)
        if "short" in url:
            return FetchResult(url=url, content="tiny", tier=Tier.FAST, verdict=Verdict.SUCCESS)
        return FetchResult(url=url, content="clean markdown", tier=Tier.FAST, verdict=Verdict.SUCCESS)

    report = await run_benchmark(cases, fetch_fn=fake_fetch)

    assert report.total == 3
    assert report.successes == 1
    assert report.score == pytest.approx(33.33, abs=0.01)
    assert report.results[0].passed is True
    assert report.results[1].passed is False
    assert report.results[1].reason == "content_too_short"
    assert report.results[2].reason == "blocked"


def test_cli_bench_json(monkeypatch, capsys):
    from apeiron.api import cli
    from apeiron import benchmarks

    async def fake_fetch(url: str, cache_ttl: int = 0):
        return FetchResult(url=url, content="x" * 200, tier=Tier.FAST, verdict=Verdict.SUCCESS)

    monkeypatch.setattr(benchmarks, "load_default_cases", lambda: [
        benchmarks.BenchmarkCase(id="demo", url="https://example.com", category="html", min_chars=100)
    ])
    monkeypatch.setattr(sys, "argv", ["apeiron", "bench", "--json"])

    cli.main(fetch_fn=fake_fetch)

    payload = json.loads(capsys.readouterr().out)
    assert payload["total"] == 1
    assert payload["successes"] == 1
    assert payload["score"] == 100.0
    assert payload["results"][0]["id"] == "demo"

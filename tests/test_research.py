from __future__ import annotations

import json
import sys

import pytest

from apeiron.types import FetchResult, SearchHit, Source, Tier, Verdict


@pytest.mark.asyncio
async def test_research_builds_markdown_report_from_search_hits():
    from apeiron.research import run_research

    async def fake_search(query: str, sources=None, max_results: int = 5):
        return [
            SearchHit(title="First", url="https://example.com/first", snippet="one", source=Source.WEB, score=2.0),
            SearchHit(title="Duplicate", url="https://example.com/first", snippet="dupe", source=Source.GITHUB, score=1.5),
            SearchHit(title="Second", url="https://example.com/second", snippet="two", source=Source.ARXIV, score=1.0),
        ]

    async def fake_fetch(url: str, cache_ttl: int = 300):
        return FetchResult(
            url=url,
            content=f"content for {url}",
            tier=Tier.FAST,
            verdict=Verdict.SUCCESS,
            confidence=0.95,
        )

    report = await run_research("agent web access", search_fn=fake_search, fetch_fn=fake_fetch, max_results=5)

    assert report.query == "agent web access"
    assert len(report.sources) == 2
    assert report.sources[0].url == "https://example.com/first"
    assert "# Research: agent web access" in report.markdown
    assert "## Sources" in report.markdown
    assert "content for https://example.com/first" in report.markdown
    assert "content for https://example.com/second" in report.markdown


def test_cli_research_json_and_markdown_file(monkeypatch, tmp_path, capsys):
    from apeiron.api import cli
    from apeiron import research as research_module

    async def fake_search(query: str, sources=None, max_results: int = 5):
        return [SearchHit(title="First", url="https://example.com/first", snippet="one", source=Source.WEB)]

    async def fake_fetch(url: str, cache_ttl: int = 300):
        return FetchResult(url=url, content="hello research", tier=Tier.FAST, verdict=Verdict.SUCCESS)

    monkeypatch.setattr(research_module, "search", fake_search)
    monkeypatch.setattr(research_module, "fetch", fake_fetch)

    output = tmp_path / "report.md"
    monkeypatch.setattr(
        sys,
        "argv",
        ["apeiron", "research", "agent web access", "--max", "1", "--markdown", str(output), "--json"],
    )

    cli.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload["query"] == "agent web access"
    assert payload["sources"][0]["url"] == "https://example.com/first"
    assert output.exists()
    assert "hello research" in output.read_text()

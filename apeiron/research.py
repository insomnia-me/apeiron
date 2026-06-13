from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Awaitable, Callable

from apeiron.api.python_api import fetch, search
from apeiron.types import FetchResult, SearchHit, Source, Verdict


SearchCallable = Callable[[str, list[Source] | None, int], Awaitable[list[SearchHit]]]
FetchCallable = Callable[[str, int], Awaitable[FetchResult]]


@dataclass(frozen=True)
class ResearchSource:
    title: str
    url: str
    snippet: str
    source: str
    score: float
    verdict: str
    tier: str
    confidence: float
    warnings: list[str]
    content_chars: int


@dataclass(frozen=True)
class ResearchReport:
    query: str
    markdown: str
    sources: list[ResearchSource]

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "markdown": self.markdown,
            "sources": [asdict(source) for source in self.sources],
        }


async def run_research(
    query: str,
    *,
    sources: list[Source] | None = None,
    max_results: int = 5,
    cache_ttl: int = 300,
    max_chars_per_source: int = 6000,
    search_fn: SearchCallable | None = None,
    fetch_fn: FetchCallable | None = None,
) -> ResearchReport:
    search_runner = search_fn or search
    fetch_runner = fetch_fn or fetch

    hits = await search_runner(query, sources, max_results)
    unique_hits = _dedupe_hits(hits)
    sections: list[str] = []
    source_rows: list[ResearchSource] = []

    for index, hit in enumerate(unique_hits[:max_results], start=1):
        result = await fetch_runner(hit.url, cache_ttl)
        source_rows.append(_source_from_result(hit, result))
        if result.verdict != Verdict.SUCCESS:
            continue

        content = (result.content or "").strip()
        if len(content) > max_chars_per_source:
            content = content[:max_chars_per_source].rstrip() + "\n\n[truncated]"

        sections.append(
            "\n".join(
                [
                    f"## Source {index}: {hit.title or hit.url}",
                    "",
                    f"- URL: {hit.url}",
                    f"- Search source: {hit.source.value}",
                    f"- Fetch tier: {result.tier.value}",
                    f"- Confidence: {result.confidence}",
                    "",
                    content,
                ]
            )
        )

    markdown = _render_markdown(query, source_rows, sections)
    return ResearchReport(query=query, markdown=markdown, sources=source_rows)


def research_sync(
    query: str,
    *,
    sources: list[Source] | None = None,
    max_results: int = 5,
    cache_ttl: int = 300,
    max_chars_per_source: int = 6000,
) -> ResearchReport:
    import asyncio

    return asyncio.run(
        run_research(
            query,
            sources=sources,
            max_results=max_results,
            cache_ttl=cache_ttl,
            max_chars_per_source=max_chars_per_source,
        )
    )


def _dedupe_hits(hits: list[SearchHit]) -> list[SearchHit]:
    seen: set[str] = set()
    unique: list[SearchHit] = []
    for hit in hits:
        normalized = hit.url.rstrip("/")
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(hit)
    return unique


def _source_from_result(hit: SearchHit, result: FetchResult) -> ResearchSource:
    return ResearchSource(
        title=hit.title,
        url=hit.url,
        snippet=hit.snippet,
        source=hit.source.value,
        score=hit.score,
        verdict=result.verdict.value,
        tier=result.tier.value,
        confidence=result.confidence or 0.0,
        warnings=result.warnings or [],
        content_chars=len(result.content or ""),
    )


def _render_markdown(query: str, sources: list[ResearchSource], sections: list[str]) -> str:
    source_lines = [
        f"{index}. [{source.title or source.url}]({source.url}) - {source.verdict}, {source.content_chars} chars"
        for index, source in enumerate(sources, start=1)
    ]
    if not source_lines:
        source_lines = ["No sources found."]
    if not sections:
        sections = ["No successful fetches. Check source verdicts and warnings above."]

    return "\n".join(
        [
            f"# Research: {query}",
            "",
            "## Sources",
            "",
            *source_lines,
            "",
            "## Notes",
            "",
            "This report is assembled from search results and fetched public URLs. Review source verdicts, confidence, and warnings before relying on it.",
            "",
            *sections,
            "",
        ]
    )

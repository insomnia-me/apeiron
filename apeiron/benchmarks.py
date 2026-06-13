from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from importlib import resources
from typing import Awaitable, Callable, Iterable

from apeiron.api.python_api import fetch as default_fetch
from apeiron.types import FetchResult, Verdict


FetchCallable = Callable[[str, int], Awaitable[FetchResult]]


@dataclass(frozen=True)
class BenchmarkCase:
    id: str
    url: str
    category: str
    min_chars: int = 400
    required_contains: tuple[str, ...] = ()


@dataclass(frozen=True)
class BenchmarkResult:
    id: str
    url: str
    category: str
    passed: bool
    reason: str
    verdict: str
    tier: str
    content_chars: int
    elapsed_ms: float
    content_type: str
    title: str
    error: str
    confidence: float
    warnings: list[str]


@dataclass(frozen=True)
class BenchmarkReport:
    total: int
    successes: int
    score: float
    results: list[BenchmarkResult]

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "successes": self.successes,
            "score": self.score,
            "results": [asdict(result) for result in self.results],
        }


def load_default_cases() -> list[BenchmarkCase]:
    """Load the bundled smoke benchmark set used by `apeiron bench`."""
    data = resources.files("apeiron.data").joinpath("benchmark_cases.json").read_text(encoding="utf-8")
    raw_cases = json.loads(data)
    return [_case_from_dict(item) for item in raw_cases]


async def run_benchmark(
    cases: Iterable[BenchmarkCase] | None = None,
    *,
    fetch_fn: FetchCallable = default_fetch,
    cache_ttl: int = 0,
) -> BenchmarkReport:
    selected_cases = list(cases if cases is not None else load_default_cases())
    results: list[BenchmarkResult] = []

    for case in selected_cases:
        result = await fetch_fn(case.url, cache_ttl)
        passed, reason = _evaluate_case(case, result)
        results.append(
            BenchmarkResult(
                id=case.id,
                url=case.url,
                category=case.category,
                passed=passed,
                reason=reason,
                verdict=result.verdict.value,
                tier=result.tier.value,
                content_chars=len(result.content or ""),
                elapsed_ms=result.elapsed_ms,
                content_type=result.content_type,
                title=result.title,
                error=result.error,
                confidence=result.confidence or 0.0,
                warnings=result.warnings,
            )
        )

    successes = sum(1 for result in results if result.passed)
    score = round((successes / len(results)) * 100, 2) if results else 0.0
    return BenchmarkReport(total=len(results), successes=successes, score=score, results=results)


def format_benchmark_report(report: BenchmarkReport) -> str:
    lines = [
        f"Apeiron Web Access Score: {report.successes}/{report.total} ({report.score:.2f}%)",
        "",
    ]
    for result in report.results:
        marker = "PASS" if result.passed else "FAIL"
        detail = result.reason if result.passed else f"{result.reason} via {result.tier}"
        lines.append(f"{marker:4} {result.id:<24} {result.category:<9} {detail}")
    return "\n".join(lines)


def _evaluate_case(case: BenchmarkCase, result: FetchResult) -> tuple[bool, str]:
    if result.verdict != Verdict.SUCCESS:
        return False, result.verdict.value
    if len(result.content or "") < case.min_chars:
        return False, "content_too_short"
    content = (result.content or "").lower()
    for needle in case.required_contains:
        if needle.lower() not in content:
            return False, "required_text_missing"
    return True, "success"


def _case_from_dict(item: dict) -> BenchmarkCase:
    return BenchmarkCase(
        id=item["id"],
        url=item["url"],
        category=item["category"],
        min_chars=int(item.get("min_chars", 400)),
        required_contains=tuple(item.get("required_contains", ())),
    )

from __future__ import annotations

from apeiron.types import FetchResult, Tier, Verdict


def test_successful_fetch_result_derives_high_confidence():
    result = FetchResult(
        url="https://example.com",
        content="useful content " * 80,
        tier=Tier.FAST,
        verdict=Verdict.SUCCESS,
        content_type="text",
    )

    assert result.confidence >= 0.9
    assert result.warnings == []


def test_short_successful_fetch_result_adds_warning():
    result = FetchResult(
        url="https://example.com",
        content="tiny",
        tier=Tier.FAST,
        verdict=Verdict.SUCCESS,
        content_type="text",
    )

    assert 0 < result.confidence < 0.9
    assert "content is very short" in result.warnings


def test_error_fetch_result_has_zero_confidence_and_warning():
    result = FetchResult(
        url="https://example.com",
        content="",
        tier=Tier.FAST,
        verdict=Verdict.ERROR,
        error="empty extraction",
    )

    assert result.confidence == 0.0
    assert "empty extraction" in result.warnings

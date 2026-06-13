from __future__ import annotations

import json

import pytest

from apeiron.types import FetchResult, Tier, Verdict


@pytest.mark.asyncio
async def test_mcp_fetch_returns_structured_result(monkeypatch):
    from apeiron.api import mcp_server

    async def fake_fetch(url: str, cache_ttl: int = 300):
        return FetchResult(
            url=url,
            content="hello",
            tier=Tier.FAST,
            verdict=Verdict.SUCCESS,
            content_type="text",
            title="Greeting",
            elapsed_ms=12.5,
            confidence=0.91,
            warnings=[],
        )

    monkeypatch.setattr(mcp_server, "fetch", fake_fetch)

    payload = json.loads(await mcp_server.apeiron_fetch("https://example.com"))

    assert payload == {
        "url": "https://example.com",
        "content": "hello",
        "tier": "fast",
        "verdict": "success",
        "content_type": "text",
        "title": "Greeting",
        "elapsed_ms": 12.5,
        "error": "",
        "confidence": 0.91,
        "warnings": [],
    }

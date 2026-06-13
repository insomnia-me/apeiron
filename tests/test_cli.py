from __future__ import annotations

import json
import sys

from apeiron.types import FetchResult, Tier, Verdict


def test_cli_doctor_json(monkeypatch, capsys):
    from apeiron.api import cli

    monkeypatch.setattr(sys, "argv", ["apeiron", "doctor", "--json"])

    cli.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload["apeiron_version"]
    assert "packages" in payload


def test_cli_fetch_json(monkeypatch, capsys):
    from apeiron.api import cli
    from apeiron.api import python_api

    async def fake_fetch(url: str, cache_ttl: int = 300):
        return FetchResult(
            url=url,
            content="hello",
            tier=Tier.FAST,
            verdict=Verdict.SUCCESS,
            content_type="text",
            confidence=0.84,
            warnings=["short content"],
        )

    monkeypatch.setattr(python_api, "fetch", fake_fetch)
    monkeypatch.setattr(sys, "argv", ["apeiron", "fetch", "https://example.com", "--json"])

    cli.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload["url"] == "https://example.com"
    assert payload["verdict"] == "success"
    assert payload["tier"] == "fast"
    assert payload["content"] == "hello"
    assert payload["confidence"] == 0.84
    assert payload["warnings"] == ["short content"]

from __future__ import annotations

import json
import sys


def test_response_cache_lists_and_searches_entries(tmp_path):
    from apeiron.cache import ResponseCache

    cache = ResponseCache(tmp_path / "cache.db")
    cache.set("https://example.com/a", "alpha content")
    cache.set("https://example.com/b", "beta content")

    entries = cache.list_entries()
    assert [entry["url"] for entry in entries] == ["https://example.com/b", "https://example.com/a"]
    assert entries[0]["chars"] == len("beta content")

    results = cache.search("alpha")
    assert len(results) == 1
    assert results[0]["url"] == "https://example.com/a"

    cache.clear()
    assert cache.list_entries() == []


def test_cli_cache_list_json(monkeypatch, tmp_path, capsys):
    from apeiron.api import cli

    db_path = tmp_path / "cache.db"
    monkeypatch.setenv("APEIRON_CACHE_DB", str(db_path))

    from apeiron.cache import ResponseCache

    cache = ResponseCache(db_path)
    cache.set("https://example.com", "cached text")

    monkeypatch.setattr(sys, "argv", ["apeiron", "cache", "list", "--json"])

    cli.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload[0]["url"] == "https://example.com"
    assert payload[0]["chars"] == len("cached text")


def test_cli_cache_search_json(monkeypatch, tmp_path, capsys):
    from apeiron.api import cli
    from apeiron.cache import ResponseCache

    db_path = tmp_path / "cache.db"
    monkeypatch.setenv("APEIRON_CACHE_DB", str(db_path))
    cache = ResponseCache(db_path)
    cache.set("https://example.com", "needle text")
    cache.set("https://other.example", "plain text")

    monkeypatch.setattr(sys, "argv", ["apeiron", "cache", "search", "needle", "--json"])

    cli.main()

    payload = json.loads(capsys.readouterr().out)
    assert [entry["url"] for entry in payload] == ["https://example.com"]

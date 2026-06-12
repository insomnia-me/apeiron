from __future__ import annotations

import pytest

from apeiron.types import SearchHit, Source


@pytest.mark.asyncio
async def test_default_search_does_not_call_reddit_stub(monkeypatch):
    from apeiron.api import python_api

    called: list[Source] = []

    async def fake_source(source: Source):
        async def inner(query: str, max_results: int = 5):
            called.append(source)
            return [SearchHit(title=source.value, url="https://example.com", snippet="", source=source)]

        return inner

    async def fail_reddit(query: str, max_results: int = 5):
        raise AssertionError("reddit should not be in default sources until OAuth is implemented")

    monkeypatch.setattr(python_api, "search_searxng", await fake_source(Source.WEB))
    monkeypatch.setattr(python_api, "search_arxiv", await fake_source(Source.ARXIV))
    monkeypatch.setattr(python_api, "search_wikipedia", await fake_source(Source.WIKIPEDIA))
    monkeypatch.setattr(python_api, "search_github", await fake_source(Source.GITHUB))
    monkeypatch.setattr(python_api, "search_reddit", fail_reddit)

    results = await python_api.search("query")

    assert Source.REDDIT not in called
    assert {hit.source for hit in results} == {Source.WEB, Source.ARXIV, Source.WIKIPEDIA, Source.GITHUB}

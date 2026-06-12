from __future__ import annotations

import pytest

from apeiron.types import Verdict


@pytest.mark.asyncio
async def test_document_fetch_uses_binary_bytes_and_errors_on_empty_extraction(monkeypatch):
    from apeiron.learn import auto_detect

    async def fake_binary_fetch(url: str):
        return b"%PDF-1.4 fake pdf bytes", {"content-type": "application/pdf"}, ""

    monkeypatch.setattr(auto_detect, "fetch_curl_cffi_bytes", fake_binary_fetch)
    monkeypatch.setattr(auto_detect, "extract_markitdown_from_bytes", lambda content, suffix: "")

    result = await auto_detect.fetch("https://example.com/file.pdf", cache_ttl=0)

    assert result.verdict == Verdict.ERROR
    assert result.content == ""
    assert "empty" in result.error.lower()


def test_fast_fetch_module_exposes_binary_helper():
    from apeiron.fetch.http import curl_cffi

    assert hasattr(curl_cffi, "fetch_curl_cffi_bytes")

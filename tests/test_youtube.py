from __future__ import annotations

import sys
import types

import pytest

from apeiron.types import Verdict


class _FakeYoutubeDL:
    def __init__(self, opts):
        self.opts = opts

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def extract_info(self, url, download=False):
        return {
            "title": "Demo video",
            "description": "Demo description",
            "subtitles": {},
            "automatic_captions": {},
        }


@pytest.mark.asyncio
async def test_youtube_without_transcript_is_not_reported_as_success(monkeypatch):
    fake_module = types.SimpleNamespace(YoutubeDL=_FakeYoutubeDL)
    monkeypatch.setitem(sys.modules, "yt_dlp", fake_module)

    from apeiron.fetch.media.yt_dlp import fetch_youtube

    result = await fetch_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    assert result.verdict == Verdict.ERROR
    assert "transcript" in result.error.lower()
    assert "## Transcript\n\n" not in result.content

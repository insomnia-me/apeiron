from __future__ import annotations

import json
import re
from html import unescape

from apeiron.types import FetchResult, Tier, Verdict


def _clean_transcript_payload(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        return ""
    if raw.startswith("{"):
        try:
            data = json.loads(raw)
            events = data.get("events", [])
            chunks: list[str] = []
            for event in events:
                for segment in event.get("segs", []) or []:
                    text = segment.get("utf8", "")
                    if text.strip():
                        chunks.append(text.strip())
            return " ".join(chunks)
        except Exception:
            return raw
    raw = re.sub(r"WEBVTT.*?\n\n", "", raw, flags=re.DOTALL)
    raw = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}.*", "", raw)
    raw = re.sub(r"<[^>]+>", "", raw)
    lines = [unescape(line.strip()) for line in raw.splitlines() if line.strip()]
    return "\n".join(lines)


def _transcript_from_entries(entries: list[dict]) -> str:
    for entry in entries:
        data = entry.get("data")
        if data:
            text = _clean_transcript_payload(str(data))
            if text:
                return text
        url = entry.get("url")
        if url:
            try:
                import httpx

                resp = httpx.get(url, timeout=20, follow_redirects=True)
                resp.raise_for_status()
                text = _clean_transcript_payload(resp.text)
                if text:
                    return text
            except Exception:
                continue
    return ""


async def fetch_youtube(url: str) -> FetchResult:
    try:
        import yt_dlp

        opts = {
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["en", "ru"],
            "quiet": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get("title", "")
        description = info.get("description", "")

        subs = info.get("subtitles", {}) or {}
        auto_subs = info.get("automatic_captions", {}) or {}
        transcript = ""

        for lang in ["en", "ru", "en-US", "en-GB"]:
            if lang in subs:
                transcript = _transcript_from_entries(subs[lang])
                break
        if not transcript:
            for lang in ["en", "ru", "en-US", "en-GB"]:
                if lang in auto_subs and auto_subs[lang]:
                    transcript = _transcript_from_entries(auto_subs[lang])
                    break

        if not transcript.strip():
            content = f"# {title}\n\n{description}".strip()
            return FetchResult(
                url=url,
                content=content,
                tier=Tier.FAST,
                verdict=Verdict.ERROR,
                content_type="youtube",
                title=title,
                error="transcript unavailable",
            )

        content = f"# {title}\n\n{description}\n\n## Transcript\n\n{transcript}"
        return FetchResult(
            url=url,
            content=content,
            tier=Tier.FAST,
            verdict=Verdict.SUCCESS,
            content_type="youtube",
            title=title,
        )
    except Exception as e:
        return FetchResult(
            url=url,
            content="",
            tier=Tier.FAST,
            verdict=Verdict.ERROR,
            error=str(e),
        )

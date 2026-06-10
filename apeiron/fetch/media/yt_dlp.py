from __future__ import annotations

from apeiron.types import FetchResult, Tier, Verdict


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
                transcript = subs[lang][0].get("data", "") or ""
                break
        if not transcript:
            for lang in ["en", "ru"]:
                if lang in auto_subs and auto_subs[lang]:
                    transcript = auto_subs[lang][0].get("data", "") or ""
                    break

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

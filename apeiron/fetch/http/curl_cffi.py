from __future__ import annotations

from apeiron.types import FetchResult, Tier, Verdict


async def fetch_curl_cffi(url: str) -> FetchResult:
    try:
        from curl_cffi import requests as cr
        resp = cr.get(url, impersonate="chrome", timeout=30)
        html = resp.text
        return FetchResult(
            url=url,
            content=html,
            tier=Tier.FAST,
            verdict=Verdict.SUCCESS,
            content_type="html",
            elapsed_ms=resp.elapsed.total_seconds() * 1000 if hasattr(resp, "elapsed") else 0,
        )
    except Exception as e:
        return FetchResult(
            url=url,
            content="",
            tier=Tier.FAST,
            verdict=Verdict.ERROR,
            error=str(e),
        )

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


async def fetch_curl_cffi_bytes(url: str) -> tuple[bytes, dict[str, str], str]:
    """Fetch binary content with curl_cffi.

    Returns ``(content, headers, error)`` so callers can avoid corrupting binary
    formats by decoding them as text first.
    """
    try:
        from curl_cffi import requests as cr

        resp = cr.get(url, impersonate="chrome", timeout=30)
        headers = {str(k).lower(): str(v) for k, v in resp.headers.items()}
        return bytes(resp.content), headers, ""
    except Exception as e:
        return b"", {}, str(e)

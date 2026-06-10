from __future__ import annotations

import httpx

from apeiron.config import FLARESOLVERR_BASE
from apeiron.types import FetchResult, Tier, Verdict


async def fetch_flaresolverr(url: str) -> FetchResult:
    try:
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": 45000,
        }
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(f"{FLARESOLVERR_BASE}/v1", json=payload)
            resp.raise_for_status()
            data = resp.json()
            solution = data.get("solution", {})
            html = solution.get("response", "")
            return FetchResult(
                url=url,
                content=html,
                tier=Tier.FLARESOLVERR,
                verdict=Verdict.SUCCESS,
                content_type="html",
            )
    except Exception as e:
        return FetchResult(
            url=url,
            content="",
            tier=Tier.FLARESOLVERR,
            verdict=Verdict.ERROR,
            error=str(e),
        )

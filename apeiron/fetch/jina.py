from __future__ import annotations

import httpx

from apeiron.types import FetchResult, Tier, Verdict


async def fetch_jina(url: str) -> FetchResult:
    try:
        jina_url = f"https://r.jina.ai/{url}"
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
            resp = await client.get(jina_url, headers={"Accept": "text/plain"})
            resp.raise_for_status()
            content = resp.text

        return FetchResult(
            url=url,
            content=content,
            tier=Tier.JINA,
            verdict=Verdict.SUCCESS,
            content_type="text",
        )
    except Exception as e:
        return FetchResult(
            url=url,
            content="",
            tier=Tier.JINA,
            verdict=Verdict.ERROR,
            error=str(e),
        )

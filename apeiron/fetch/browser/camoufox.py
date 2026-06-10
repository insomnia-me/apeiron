from __future__ import annotations

from apeiron.types import FetchResult, Tier, Verdict


async def fetch_camoufox(url: str) -> FetchResult:
    try:
        from camoufox import AsyncCamoufox

        async with AsyncCamoufox(headless=True) as browser:
            page = await browser.new_page()
            await page.goto(url, timeout=45000)
            html = await page.content()
            title = await page.title()

        return FetchResult(
            url=url,
            content=html,
            tier=Tier.CAMOUFOX,
            verdict=Verdict.SUCCESS,
            content_type="html",
            title=title,
        )
    except Exception as e:
        return FetchResult(
            url=url,
            content="",
            tier=Tier.CAMOUFOX,
            verdict=Verdict.ERROR,
            error=str(e),
        )

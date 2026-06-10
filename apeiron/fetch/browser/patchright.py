from __future__ import annotations

from apeiron.types import FetchResult, Tier, Verdict


async def fetch_patchright(url: str) -> FetchResult:
    try:
        from patchright.async_api import async_playwright

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=30000)
            html = await page.content()
            await browser.close()

        return FetchResult(
            url=url,
            content=html,
            tier=Tier.PATCHRIGHT,
            verdict=Verdict.SUCCESS,
            content_type="html",
        )
    except Exception as e:
        return FetchResult(
            url=url,
            content="",
            tier=Tier.PATCHRIGHT,
            verdict=Verdict.ERROR,
            error=str(e),
        )

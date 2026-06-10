from __future__ import annotations

from apeiron.types import FetchResult, Tier, Verdict

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"}


async def fetch_cloakbrowser(url: str, proxy: str | None = None, headless: bool = True) -> FetchResult:
    try:
        from cloakbrowser import launch

        kwargs = dict(headless=headless)
        if proxy:
            kwargs["proxy"] = proxy
        browser = launch(**kwargs)
        page = browser.new_page()
        await page.goto(url, wait_until="networkidle", timeout=45000)
        html = await page.content()
        title = await page.title()
        await browser.close()

        return FetchResult(
            url=url,
            content=html,
            tier=Tier.CLOAKBROWSER,
            verdict=Verdict.SUCCESS,
            content_type="html",
            title=title,
        )
    except Exception as e:
        return FetchResult(
            url=url,
            content="",
            tier=Tier.CLOAKBROWSER,
            verdict=Verdict.ERROR,
            error=str(e),
        )

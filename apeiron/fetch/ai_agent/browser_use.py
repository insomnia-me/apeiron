from __future__ import annotations

from apeiron.types import FetchResult, Tier, Verdict


async def fetch_browser_use(url: str, task: str | None = None) -> FetchResult:
    try:
        from browser_use import Agent
        from playwright.async_api import async_playwright

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)

            if task:
                agent = Agent(
                    task=f"Go to {url} and {task}. Return the full page content.",
                    browser=browser,
                )
                await agent.run(max_steps=10)

            html = await page.content()
            title = await page.title()
            await browser.close()

        return FetchResult(
            url=url,
            content=html,
            tier=Tier.BROWSER_USE,
            verdict=Verdict.SUCCESS,
            content_type="html",
            title=title,
        )
    except Exception as e:
        return FetchResult(
            url=url,
            content="",
            tier=Tier.BROWSER_USE,
            verdict=Verdict.ERROR,
            error=str(e),
        )

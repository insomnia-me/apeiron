from __future__ import annotations

import time
from urllib.parse import urlparse

from apeiron.cache import ResponseCache
from apeiron.extract.trafilatura import extract_trafilatura
from apeiron.extract.markitdown import extract_markitdown_from_bytes
from apeiron.extract.utils import detect_content_type, is_blocked
from apeiron.fetch.http.curl_cffi import fetch_curl_cffi
from apeiron.fetch.browser.cloakbrowser import fetch_cloakbrowser
from apeiron.fetch.browser.camoufox import fetch_camoufox
from apeiron.fetch.browser.flaresolverr import fetch_flaresolverr
from apeiron.fetch.browser.patchright import fetch_patchright
from apeiron.fetch.ai_agent.browser_use import fetch_browser_use
from apeiron.fetch.media.yt_dlp import fetch_youtube
from apeiron.fetch.jina import fetch_jina
from apeiron.learn.heuristics import detect_challenge, add_marker
from apeiron.learn.strategy_store import StrategyStore
from apeiron.learn.git_ops import maybe_commit_new_pattern
from apeiron.types import FetchResult, Tier, Verdict

_cache = ResponseCache()
_store = StrategyStore()


TIER_FETCHERS = {
    Tier.FAST: fetch_curl_cffi,
    Tier.PATCHRIGHT: fetch_patchright,
    Tier.CLOAKBROWSER: fetch_cloakbrowser,
    Tier.CAMOUFOX: fetch_camoufox,
    Tier.FLARESOLVERR: fetch_flaresolverr,
    Tier.BROWSER_USE: fetch_browser_use,
    Tier.JINA: fetch_jina,
}

TIER_ORDER = [
    Tier.FAST,
    Tier.PATCHRIGHT,
    Tier.CLOAKBROWSER,
    Tier.CAMOUFOX,
    Tier.FLARESOLVERR,
    Tier.BROWSER_USE,
    Tier.JINA,
]


async def fetch(url: str, cache_ttl: int = 300) -> FetchResult:
    cached = _cache.get(url, ttl_seconds=cache_ttl)
    if cached:
        return FetchResult(url=url, content=cached, tier=Tier.FAST, verdict=Verdict.SUCCESS, content_type="text")

    start = time.time()

    # 1. Detect content type
    ctype = detect_content_type(url)

    # 2. Special handlers for non-HTML
    if ctype == "youtube":
        result = await fetch_youtube(url)
        if result.verdict == Verdict.SUCCESS:
            _cache.set(url, result.content)
        return result

    if ctype in ("pdf", "docx", "pptx", "xlsx"):
        result = await fetch_curl_cffi(url)
        if result.verdict == Verdict.SUCCESS and result.content:
            text = extract_markitdown_from_bytes(result.content.encode(), suffix=f".{ctype}")
            result.content = text
            result.content_type = "text"
            _cache.set(url, text)
        return result

    if ctype == "arxiv":
        result = await fetch_curl_cffi(url)
        if result.verdict == Verdict.SUCCESS:
            result.content = extract_trafilatura(result.content, url) or result.content
        return result

    # 3. HTML — use tier escalation
    domain = urlparse(url).netloc
    cached_tier = _store.get(url)

    if cached_tier and cached_tier in TIER_FETCHERS:
        result = await TIER_FETCHERS[cached_tier](url)
        if result.verdict == Verdict.SUCCESS and not detect_challenge(result):
            text = extract_trafilatura(result.content, url) or result.content
            result.content = text
            result.content_type = "text"
            _cache.set(url, text)
            result.elapsed_ms = (time.time() - start) * 1000
            return result

    # 4. Try each tier
    for tier in TIER_ORDER:
        fetcher = TIER_FETCHERS[tier]
        result = await fetcher(url)

        if result.verdict == Verdict.SUCCESS and not detect_challenge(result):
            _store.set(url, tier)

            for marker in CHALLENGE_MARKERS_SAMPLE:
                if marker in result.content.lower():
                    add_marker(marker)
                    maybe_commit_new_pattern(marker, url, tier)

            text = extract_trafilatura(result.content, url) or result.content
            result.content = text
            result.content_type = "text"
            _cache.set(url, text)
            result.elapsed_ms = (time.time() - start) * 1000
            return result

        if detect_challenge(result):
            for marker in CHALLENGE_MARKERS_SAMPLE:
                if marker in result.content.lower():
                    add_marker(marker)
                    maybe_commit_new_pattern(marker, url, tier)

    # 5. All tiers failed — return last result
    result.elapsed_ms = (time.time() - start) * 1000
    result.verdict = Verdict.BLOCKED
    return result


async def learn(url: str) -> FetchResult:
    """Proactively try all tiers on a domain to find the best one."""
    best: FetchResult | None = None

    for tier in TIER_ORDER:
        fetcher = TIER_FETCHERS[tier]
        result = await fetcher(url)
        if result.verdict == Verdict.SUCCESS and not detect_challenge(result):
            best = result
            _store.set(url, tier)
            break
        if best is None or result.verdict == Verdict.SUCCESS:
            best = result

    if best is None:
        best = FetchResult(url=url, content="", tier=Tier.FALLBACK, verdict=Verdict.ERROR, error="all tiers failed")

    return best


CHALLENGE_MARKERS_SAMPLE = [
    "just a moment", "enable javascript", "attention required",
    "checking your browser", "cloudflare", "turnstile",
    "captcha", "verify you are human", "blocked", "403 forbidden",
]

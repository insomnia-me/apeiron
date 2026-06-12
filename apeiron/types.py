from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Tier(str, Enum):
    FAST = "fast"                 # curl_cffi (TLS impersonation)
    PATCHRIGHT = "patchright"     # patchright (Playwright)
    CLOAKBROWSER = "cloakbrowser" # ★ CloakBrowser (58 C++ patches)
    CAMOUFOX = "camoufox"         # Camoufox (Firefox C++ patches)
    FLARESOLVERR = "flaresolverr" # FlareSolverr (Docker)
    BROWSER_USE = "browser_use"   # browser-use (AI agent browsing)
    JINA = "jina"                 # Jina Reader (URL → text API)
    FALLBACK = "fallback"         # Direct HTTP fallback


TIER_ORDER = [
    Tier.FAST,
    Tier.PATCHRIGHT,
    Tier.CLOAKBROWSER,
    Tier.CAMOUFOX,
    Tier.FLARESOLVERR,
    Tier.BROWSER_USE,
    Tier.JINA,
    Tier.FALLBACK,
]


class Source(str, Enum):
    WEB = "web"             # SearXNG (meta-search)
    ARXIV = "arxiv"         # arXiv API
    SEMANTIC_SCHOLAR = "semantic_scholar"
    WIKIPEDIA = "wikipedia"
    REDDIT = "reddit"
    GITHUB = "github"
    YOUTUBE = "youtube"


class Verdict(str, Enum):
    SUCCESS = "success"
    CHALLENGE = "challenge"
    BLOCKED = "blocked"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class FetchResult:
    url: str
    content: str
    tier: Tier
    verdict: Verdict
    content_type: str = "text"   # "html", "pdf", "youtube", "markdown", etc.
    title: str = ""
    elapsed_ms: float = 0.0
    error: str = ""


@dataclass
class ScrapeResult:
    url: str
    content: str
    tier: Tier
    verdict: Verdict
    metadata: dict = field(default_factory=dict)


@dataclass
class SearchHit:
    title: str
    url: str
    snippet: str
    source: Source
    score: float = 1.0

from __future__ import annotations

import re
from urllib.parse import urlparse


def detect_content_type(url: str, html: str = "", headers: dict | None = None) -> str:
    parsed = urlparse(url)
    path = parsed.path.lower()

    if re.search(r'youtube\.com|youtu\.be', parsed.netloc):
        return "youtube"
    if path.endswith(".pdf") or ("arxiv.org" in parsed.netloc and path.startswith("/pdf/")):
        return "pdf"
    if path.endswith(".docx"):
        return "docx"
    if path.endswith(".pptx"):
        return "pptx"
    if path.endswith(".xlsx"):
        return "xlsx"
    if "arxiv.org" in parsed.netloc and "abs" in path:
        return "arxiv"

    if html:
        if "arXiv:" in html[:5000] or "arxiv.org" in html[:5000]:
            return "arxiv"

    content_type = (headers or {}).get("content-type", "")
    if "pdf" in content_type:
        return "pdf"

    return "html"


def is_blocked(html: str) -> bool:
    signals = [
        "just a moment", "enable javascript", "attention required",
        "cloudflare", "ddos protection", "challenge", "cf-challenge",
        "403 forbidden", "access denied", "blocked",
        "turnstile", "captcha", "verify you are human",
        "automated access", "suspicious activity",
    ]
    low = html.lower()
    for s in signals:
        if s in low:
            return True
    return False

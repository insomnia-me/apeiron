"""Challenge detection heuristics — auto-updated when Apeiron learns new patterns."""

from __future__ import annotations

from apeiron.types import FetchResult, Verdict


CHALLENGE_MARKERS = [
    "just a moment...",
    "enable javascript",
    "attention required!",
    "checking your browser",
    "ddos protection",
    "cloudflare",
    "cf-challenge",
    "cf-browser-verification",
    "turnstile",
    "captcha",
    "verify you are human",
    "automated access",
    "suspicious activity",
    "403 forbidden",
    "access denied",
    "blocked",
    "sorry, you have been blocked",
    "we detected unusual traffic",
    "entering the hCaptcha",
    "hcaptcha",
    "challenge-platform",
    "fingerprint",
]


def detect_challenge(result: FetchResult) -> bool:
    """Check if the response contains known anti-bot challenge markers."""
    if result.verdict in (Verdict.BLOCKED, Verdict.TIMEOUT, Verdict.ERROR):
        return True

    low = result.content.lower()
    for marker in CHALLENGE_MARKERS:
        if marker in low:
            return True
    return False


def add_marker(marker: str):
    """Add a new challenge marker to heuristics (called by self-learning)."""
    marker_lower = marker.lower().strip()
    if marker_lower and marker_lower not in CHALLENGE_MARKERS:
        CHALLENGE_MARKERS.append(marker_lower)

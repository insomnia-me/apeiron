from __future__ import annotations

import httpx


def extract_jina(url: str) -> str:
    try:
        jina_url = f"https://r.jina.ai/{url}"
        resp = httpx.get(jina_url, timeout=60, follow_redirects=True)
        resp.raise_for_status()
        return resp.text
    except Exception:
        return ""

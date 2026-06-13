from __future__ import annotations

import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

from apeiron.types import FetchResult, Tier, Verdict


def test_demo_html_contains_fetch_controls():
    from apeiron.demo import render_demo_html

    html = render_demo_html()

    assert "Apeiron Demo" in html
    assert 'id="url-input"' in html
    assert 'id="confidence"' in html
    assert "/api/fetch" in html


def test_demo_fetch_api_returns_fetch_payload():
    from apeiron.demo import make_demo_handler

    async def fake_fetch(url: str, cache_ttl: int = 300):
        return FetchResult(
            url=url,
            content="# Hello from Apeiron",
            tier=Tier.FAST,
            verdict=Verdict.SUCCESS,
            content_type="markdown",
            title="Demo",
            elapsed_ms=12.5,
        )

    server = ThreadingHTTPServer(("127.0.0.1", 0), make_demo_handler(fake_fetch))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_port}/api/fetch"
        request = urllib.request.Request(
            url,
            data=json.dumps({"url": "https://example.com"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode())
    finally:
        server.shutdown()
        thread.join(timeout=5)

    assert payload["url"] == "https://example.com"
    assert payload["content"] == "# Hello from Apeiron"
    assert payload["tier"] == "fast"
    assert payload["verdict"] == "success"

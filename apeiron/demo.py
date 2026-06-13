from __future__ import annotations

import asyncio
import json
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Awaitable, Callable

from apeiron.api.python_api import fetch as default_fetch
from apeiron.types import FetchResult


FetchCallable = Callable[[str, int], Awaitable[FetchResult]]


def render_demo_html() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Apeiron Demo</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #07090d;
      --panel: #0d1418;
      --panel-2: #101b1f;
      --line: #1d343a;
      --text: #eef7f7;
      --muted: #8da3a7;
      --accent: #49d8e8;
      --ok: #79f2a6;
      --warn: #ffd166;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 78% 18%, rgba(73, 216, 232, 0.15), transparent 28rem),
        linear-gradient(135deg, var(--bg), #050608 58%, #071111);
      color: var(--text);
    }
    main {
      min-height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr;
    }
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      padding: 1.5rem clamp(1rem, 3vw, 3rem);
      border-bottom: 1px solid rgba(141, 163, 167, 0.16);
    }
    .brand {
      font-size: 1.05rem;
      font-weight: 750;
      letter-spacing: 0;
    }
    .tagline {
      color: var(--muted);
      font-size: 0.95rem;
    }
    .workspace {
      display: grid;
      grid-template-columns: minmax(18rem, 0.9fr) minmax(22rem, 1.4fr);
      gap: clamp(1rem, 2vw, 1.5rem);
      padding: clamp(1rem, 3vw, 3rem);
      align-items: stretch;
    }
    section {
      min-width: 0;
      border: 1px solid rgba(141, 163, 167, 0.18);
      background: linear-gradient(180deg, rgba(16, 27, 31, 0.88), rgba(7, 9, 13, 0.88));
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
    }
    .control {
      padding: clamp(1rem, 2.2vw, 1.5rem);
      display: grid;
      align-content: start;
      gap: 1rem;
    }
    h1 {
      margin: 0;
      font-size: clamp(2.2rem, 5vw, 5.8rem);
      line-height: 0.94;
      letter-spacing: 0;
      max-width: 9ch;
    }
    label {
      display: block;
      color: var(--muted);
      font-size: 0.86rem;
      margin-bottom: 0.45rem;
    }
    input {
      width: 100%;
      min-height: 3rem;
      border: 1px solid var(--line);
      background: rgba(5, 8, 10, 0.76);
      color: var(--text);
      padding: 0 0.9rem;
      font: inherit;
      outline: none;
    }
    input:focus { border-color: var(--accent); }
    button {
      width: 100%;
      min-height: 3rem;
      border: 1px solid rgba(73, 216, 232, 0.55);
      background: #0b2a30;
      color: var(--text);
      font-weight: 750;
      cursor: pointer;
    }
    button:disabled {
      cursor: wait;
      opacity: 0.7;
    }
    .metrics {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 0.75rem;
    }
    .metric {
      border: 1px solid rgba(141, 163, 167, 0.16);
      background: rgba(9, 15, 18, 0.7);
      padding: 0.8rem;
      min-height: 4.5rem;
    }
    .metric span {
      display: block;
      color: var(--muted);
      font-size: 0.78rem;
      margin-bottom: 0.4rem;
    }
    .metric strong {
      font-size: 1.05rem;
      overflow-wrap: anywhere;
    }
    .output {
      display: grid;
      grid-template-rows: auto 1fr;
      min-height: 34rem;
    }
    .toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      padding: 1rem 1.2rem;
      border-bottom: 1px solid rgba(141, 163, 167, 0.16);
    }
    .status {
      color: var(--muted);
      overflow-wrap: anywhere;
    }
    .status.ok { color: var(--ok); }
    .status.warn { color: var(--warn); }
    pre {
      margin: 0;
      padding: 1.2rem;
      white-space: pre-wrap;
      overflow: auto;
      color: #dce7e8;
      line-height: 1.55;
      font-size: 0.92rem;
    }
    @media (max-width: 840px) {
      header, .workspace { padding: 1rem; }
      .workspace { grid-template-columns: 1fr; }
      h1 { max-width: 100%; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <div class="brand">Apeiron Demo</div>
      <div class="tagline">local-first web tools for AI agents</div>
    </header>
    <div class="workspace">
      <section class="control">
        <h1>read the web</h1>
        <form id="fetch-form">
          <label for="url-input">Public URL</label>
          <input id="url-input" name="url" value="https://example.com" autocomplete="url">
          <button id="fetch-button" type="submit">Fetch</button>
        </form>
        <div class="metrics">
          <div class="metric"><span>verdict</span><strong id="verdict">idle</strong></div>
          <div class="metric"><span>tier</span><strong id="tier">-</strong></div>
          <div class="metric"><span>type</span><strong id="content-type">-</strong></div>
          <div class="metric"><span>chars</span><strong id="chars">0</strong></div>
        </div>
      </section>
      <section class="output">
        <div class="toolbar">
          <div>LLM-ready content</div>
          <div id="status" class="status">waiting</div>
        </div>
        <pre id="content">Enter a URL and fetch.</pre>
      </section>
    </div>
  </main>
  <script>
    const form = document.getElementById('fetch-form');
    const button = document.getElementById('fetch-button');
    const statusEl = document.getElementById('status');
    const contentEl = document.getElementById('content');
    const fields = {
      verdict: document.getElementById('verdict'),
      tier: document.getElementById('tier'),
      contentType: document.getElementById('content-type'),
      chars: document.getElementById('chars'),
    };

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const url = document.getElementById('url-input').value.trim();
      if (!url) return;
      button.disabled = true;
      statusEl.textContent = 'fetching';
      statusEl.className = 'status warn';
      contentEl.textContent = '';
      try {
        const response = await fetch('/api/fetch', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({url}),
        });
        const payload = await response.json();
        if (!response.ok) throw new Error(payload.error || 'request failed');
        fields.verdict.textContent = payload.verdict || '-';
        fields.tier.textContent = payload.tier || '-';
        fields.contentType.textContent = payload.content_type || '-';
        fields.chars.textContent = String((payload.content || '').length);
        statusEl.textContent = payload.url;
        statusEl.className = payload.verdict === 'success' ? 'status ok' : 'status warn';
        contentEl.textContent = payload.content || payload.error || '';
      } catch (error) {
        statusEl.textContent = 'error';
        statusEl.className = 'status warn';
        contentEl.textContent = String(error);
      } finally {
        button.disabled = false;
      }
    });
  </script>
</body>
</html>
"""


def make_demo_handler(fetch_fn: FetchCallable = default_fetch) -> type[BaseHTTPRequestHandler]:
    class DemoHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path not in ("/", "/index.html"):
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            self._send_text(render_demo_html(), "text/html; charset=utf-8")

        def do_POST(self) -> None:
            if self.path != "/api/fetch":
                self.send_error(HTTPStatus.NOT_FOUND)
                return

            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                url = str(payload.get("url", "")).strip()
                if not url:
                    self._send_json({"error": "url is required"}, status=HTTPStatus.BAD_REQUEST)
                    return
                result = asyncio.run(fetch_fn(url, 300))
                self._send_json(_fetch_result_payload(result))
            except Exception as exc:
                self._send_json({"error": str(exc)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        def log_message(self, format: str, *args: object) -> None:
            return

        def _send_text(self, body: str, content_type: str) -> None:
            encoded = body.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def _send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
            encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

    return DemoHandler


def run_demo(host: str = "127.0.0.1", port: int = 8765, *, open_browser: bool = True) -> None:
    server = ThreadingHTTPServer((host, port), make_demo_handler())
    url = f"http://{host}:{server.server_port}"
    print(f"Apeiron demo running at {url}")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Apeiron demo")
    finally:
        server.server_close()


def _fetch_result_payload(result: FetchResult) -> dict:
    return {
        "url": result.url,
        "content": result.content,
        "tier": result.tier.value,
        "verdict": result.verdict.value,
        "content_type": result.content_type,
        "title": result.title,
        "elapsed_ms": result.elapsed_ms,
        "error": result.error,
    }

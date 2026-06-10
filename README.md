<p align="center">
  <img src="https://img.shields.io/badge/ἄπειρον-Apeiron-00D4FF?style=flat-square&logo=python&logoColor=00D4FF&color=000" alt="apeiron">
  <img src="https://img.shields.io/badge/license-MIT-000?style=flat-square&logo=open-source-initiative&logoColor=00D4FF&color=000" alt="license">
  <img src="https://img.shields.io/badge/Python-3.10+-000?style=flat-square&logo=python&logoColor=00D4FF&color=000" alt="python">
  <img src="https://img.shields.io/badge/MCP-✓-000?style=flat-square&logo=claude&logoColor=00D4FF&color=000" alt="mcp">
  <img src="https://img.shields.io/badge/CloakBrowser-✓-000?style=flat-square&logo=googlechrome&logoColor=00D4FF&color=000" alt="cloakbrowser">
  <img src="https://img.shields.io/badge/Markitdown-✓-000?style=flat-square&logo=microsoft&logoColor=00D4FF&color=000" alt="markitdown">
</p>

<h1 align="center">⚡ Apeiron</h1>

<p align="center">
  <b>Unlimited Web Access for AI Agents</b><br>
  <i>"That which has no boundaries" — Anaximander, 6th century BCE</i>
</p>

<p align="center">
  One tool to search, fetch, and extract anything on the web.<br>
  Self-learning. Anti-bot bypass. PDF → Markdown. YouTube transcripts.<br>
  All free. All open. All yours.
</p>

---

## 🧬 Philosophy

> **Why can Anthropic charge $200/month for knowledge, while ordinary people get blocked by Cloudflare?**

Information wants to be free. Apeiron is the tool that makes it so.

Every AI agent — OpenCode, Claude Code, Cursor, Cline, any of them — deserves **unrestricted access to the open web**. Not through paid APIs, not through corporate gatekeepers, but through the collective power of every free anti-bot technology united into one autonomous system.

Apeiron combines:
- **CloakBrowser** (58 C++ patches, 0.9 reCAPTCHA score) — best stealth browser
- **Markitdown** (Microsoft, 147k ⭐) — PDF/DOCX/PPTX → Markdown
- **yt-dlp** (95k ⭐) — YouTube transcripts
- **SearXNG** — privacy-respecting meta-search
- **Wikipedia / arXiv / Semantic Scholar / Reddit / GitHub APIs**
- **Self-learning** — remembers what works per domain, auto-commits new bypass patterns

Apeiron doesn't just scrape. It **learns**. Every new anti-bot pattern discovered by one user becomes a patch for everyone. The network gets smarter together.

---

## ⚡ One-command install

```bash
curl -fsSL https://raw.githubusercontent.com/insomnia-me/apeiron/main/install.sh | bash
```

Then:

```bash
# Fetch any URL — bypasses Cloudflare, Turnstile, CAPTCHA, everything
apeiron fetch "https://arxiv.org/pdf/2203.02155.pdf"

# Search across 6 sources at once
apeiron search "quantum computing 2026"

# Teach Apeiron a new domain
apeiron learn "https://protected-site.com"

# Start MCP server for your AI agent
apeiron serve
```

---

## 🔌 MCP server — use from any AI agent

```jsonc
// ~/.config/opencode/opencode.jsonc
{
  "mcp": {
    "servers": {
      "apeiron": {
        "command": "python",
        "args": ["-m", "apeiron.api.mcp_server"]
      }
    }
  }
}
```

Then your agent calls:

| Tool | What it does |
|---|---|
| `apeiron_search("query")` | Search web + arXiv + Wikipedia + Reddit + GitHub |
| `apeiron_fetch("url")` | Fetch anything: HTML, PDF, YouTube, bypassing all blocks |
| `apeiron_learn("url")` | Learn best strategy for a domain |

**Your agent never writes scraping code.** It just asks Apeiron.

---

## 🧠 Architecture

```
                    APEIRON
                        │
          ┌─────────────┴─────────────┐
          │                           │
     SEARCH                      FETCH
          │                           │
  ┌───┬───┼───┬───┬───┐     ┌───────┼──────────┐
  │   │   │   │   │   │     │       │          │
SearXNG  Wiki Reddit  GH  HTTP   BROWSER    MEDIA
  arXiv       pedia          Level  Level     Level
                                   │
                              CloakBrowser
                              Camoufox
                              FlareSolverr
                              browser-use
                                   │
                            ┌──────┴──────┐
                         EXTRACT       SELF-LEARN
                            │              │
                      Trafilatura     strategies.json
                      Markitdown      heuristics.py
                      Readability     git push
                                   (new bypass patterns)
```

### What happens when you call `apeiron.fetch(url)`:

```
1. Auto-detect content type
   ── YouTube? → yt-dlp → transcript
   ── PDF?     → Markitdown → clean text
   ── HTML?    → go to step 2

2. Check strategy cache
   ── Known domain? → use cached best tier → done
   ── Unknown?      → go to step 3

3. Tier escalation:
   ┌─ 1. curl_cffi (TLS impersonation)        0.2s
   ├─ 2. Patchright (Playwright)              1.5s
   ├─ 3. ★ CloakBrowser (58 C++ patches)      3.0s
   ├─ 4. Camoufox (Firefox C++ patches)       3.0s
   ├─ 5. FlareSolverr (Docker)                5.0s
   ├─ 6. browser-use (AI agent browsing)      15s
   └─ 7. Jina Reader (API fallback)           5.0s

4. Success? → save best tier to strategies.json
   Blocked? → detect challenge pattern → auto-commit to git
              → all users get the update
```

---

## 💻 Python API

```python
from apeiron import search_sync, fetch_sync, learn_sync

# Search across all sources
results = search_sync("transformer architecture 2026")
for r in results:
    print(f"[{r.source}] {r.title}")
    print(f"  {r.url}")
    print(f"  {r.snippet[:100]}\n")

# Fetch any URL — auto-detects content type
content = fetch_sync("https://arxiv.org/pdf/2203.02155.pdf")
# → PDF auto-detected → Markitdown → clean markdown text

content = fetch_sync("https://youtube.com/watch?v=dQw4w9WgXcQ")
# → YouTube auto-detected → yt-dlp → transcript

content = fetch_sync("https://cloudflare-protected-site.com")
# → HTML auto-detected → tier escalation → CloakBrowser → text

# Teach a new domain
result = learn_sync("https://example-protected-site.com")
print(f"Best tier: {result.tier}")  # → cloakbrowser
```

---

## ⚔️ vs alternatives

| Feature | Firecrawl | Crawl4AI | browser-use.com | **Apeiron** |
|---|---|---|---|---|
| Stealth browser | ❌ | ❌ | 💰 $49-299/mo | ✅ **CloakBrowser** (free) |
| PDF → Markdown | ❌ | ❌ | ❌ | ✅ **Markitdown** (147k ⭐) |
| YouTube transcripts | ❌ | ❌ | ❌ | ✅ **yt-dlp** (95k ⭐) |
| Multi-source search | ❌ | ❌ | ❌ | ✅ **SearXNG + 5 APIs** |
| Self-learning | ❌ | ❌ | ❌ | ✅ **strategies.json** |
| Auto-commit bypasses | ❌ | ❌ | ❌ | ✅ **git push to all** |
| MCP server | ❌ | ❌ | ❌ | ✅ **MCP protocol** |
| Price | Free tier | Free | $49-599/mo | **Free forever** |

---

## 📦 Install

### Quick (recommended)
```bash
curl -fsSL https://raw.githubusercontent.com/insomnia-me/apeiron/main/install.sh | bash
```

### pip
```bash
pip install apeiron
# With all features:
pip install "apeiron[all]"
```

### From source
```bash
git clone https://github.com/insomnia-me/apeiron.git
cd apeiron
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[all]"
```

### Docker infrastructure (optional — for SearXNG + FlareSolverr)
```bash
bash scripts/start-infra.sh
```

---

## 🧪 Commands

```bash
apeiron search "query"                    # Multi-source search
apeiron fetch "https://..."               # Fetch any URL
apeiron fetch "https://..." -o output.md  # Save to file
apeiron learn "https://..."               # Train on new domain
apeiron serve                             # Start MCP server
```

---

## 🏛️ How self-learning works

```
User fetches URL
       ↓
Tier 1 fails (blocked by Cloudflare)
       ↓
Tier 2 fails (Turnstile challenge)
       ↓
Tier 3 succeeds (CloakBrowser bypasses)
       ↓
✓ Save "cloakbrowser" as best tier for this domain
  in strategies.json
       ↓
✓ If new anti-bot pattern detected:
  → Add to heuristics.py
  → Git commit & push
  → All Apeiron users get the update
       ↓
Next time: direct to CloakBrowser for this domain
```

The network grows smarter with every fetch.

---

## 🛠️ What's under the hood

| Category | Technology | Stars | License |
|---|---|---|---|
| Stealth browser | **CloakBrowser** | 25k ⭐ | MIT |
| Document conversion | **Markitdown** (Microsoft) | 147k ⭐ | MIT |
| YouTube transcripts | **yt-dlp** | 95k ⭐ | Unlicense |
| Meta-search | **SearXNG** | — | AGPL |
| TLS impersonation | **curl_cffi** | 3k ⭐ | MIT |
| Firefox stealth | **Camoufox** | 5k ⭐ | MIT |
| AI browsing | **browser-use** | 70k ⭐ | MIT |
| AI extraction | **ScrapeGraphAI** | 25k ⭐ | MIT |
| Content extraction | **Trafilatura** | 3k ⭐ | GPL |
| Article extraction | **Readability** (Mozilla) | 8k ⭐ | Apache |
| Scientific search | **Semantic Scholar API** | — | Free |
| Knowledge base | **Wikipedia API** | — | Free |

---

<p align="center">
  <b>Apeiron (ἄπειρον)</b><br>
  <i>"That which has no boundaries"</i><br>
  <br>
  Information wants to be free.<br>
  This is how you free it.
</p>

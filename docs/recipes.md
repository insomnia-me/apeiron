# Recipes

These recipes are intentionally short. Copy one, run it, then adapt it.

## Give Claude Desktop web search

Install Apeiron with MCP support:

```bash
pipx install "git+https://github.com/insomnia-me/apeiron.git"
```

Generate a starter config:

```bash
apeiron init --target claude --output .
```

Copy the generated `claude_desktop_config.json` content into Claude Desktop's MCP config. Claude will get three tools:

- `apeiron_search`
- `apeiron_fetch`
- `apeiron_learn`

Ask Claude:

```text
Use Apeiron to search for recent MCP server examples, fetch the best sources, and summarize the implementation patterns.
```

## Build a research agent

Use Apeiron as a search-and-read layer inside a Python agent:

```python
from apeiron import fetch_sync, search_sync


def research(query: str) -> str:
    hits = search_sync(query, max_results=5)
    sections = []
    for hit in hits:
        page = fetch_sync(hit.url, cache_ttl=300)
        if page.verdict.value != "success":
            continue
        sections.append(f"# {hit.title}\n\nSource: {hit.url}\n\n{page.content[:6000]}")
    return "\n\n---\n\n".join(sections)


print(research("agent web access MCP local-first"))
```

For OpenAI Agents SDK, generate a wrapper:

```bash
apeiron init --target openai-agents --output .
```

Or use the built-in one-command research workflow:

```bash
apeiron research "agent web access MCP local-first" --markdown report.md
```

The report includes fetched source content plus `verdict`, `tier`, `confidence`, and `warnings` for each source.

## Extract PDFs into Markdown

Install with document extraction:

```bash
pip install -e ".[fetch,documents]"
```

Fetch a PDF-like public URL:

```bash
apeiron fetch "https://arxiv.org/pdf/1706.03762" --json > attention.json
```

Inspect the result before trusting it:

```bash
python - <<'PY'
import json

payload = json.load(open("attention.json"))
print(payload["verdict"], payload["content_type"], payload["confidence"], payload["warnings"])
print(payload["content"][:2000])
PY
```

## Build a RAG corpus from URLs

Create `urls.txt`:

```text
https://docs.python.org/3/tutorial/
https://docs.github.com/en/rest
https://example.com/
```

Convert each URL into Markdown-ish text files:

```bash
mkdir -p corpus
while read -r url; do
  slug=$(python - <<'PY' "$url"
import hashlib, sys
print(hashlib.sha1(sys.argv[1].encode()).hexdigest()[:12])
PY
)
  apeiron fetch "$url" --json > "corpus/$slug.json"
done < urls.txt
```

Search cached corpus entries later:

```bash
apeiron cache search "documentation" --json
```

## Monitor docs changes

Use a project-specific cache so repeated checks do not mix with unrelated runs:

```bash
export APEIRON_CACHE_DB="$PWD/.apeiron-docs-cache.db"
apeiron fetch "https://docs.python.org/3/tutorial/" --json > latest.json
```

Compare content against your last snapshot:

```bash
python - <<'PY'
import json
from pathlib import Path

latest = json.load(open("latest.json"))["content"]
snapshot = Path("snapshot.md")

if not snapshot.exists():
    snapshot.write_text(latest)
    print("snapshot created")
elif snapshot.read_text() != latest:
    print("docs changed")
    snapshot.write_text(latest)
else:
    print("no change")
PY
```

## Debug a failing URL

Start with diagnostics:

```bash
apeiron doctor
apeiron fetch "https://example.com" --json
apeiron learn "https://example.com" --json
```

Then compare with the visual demo:

```bash
apeiron demo
```

Look at:

- `verdict`
- `tier`
- `confidence`
- `warnings`
- extracted character count

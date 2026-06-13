# Install Guide

The PyPI name `apeiron` is not this project. Use the GitHub URL or the `apeiron-agent` distribution name after it is published.

## Minimal CLI and API

```bash
pip install "apeiron-agent @ git+https://github.com/insomnia-me/apeiron.git"
```

## Source Install

```bash
git clone https://github.com/insomnia-me/apeiron.git
cd apeiron
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[fetch,mcp,documents,media]"
```

## Profiles

- `fetch`: fast HTTP fetch and text extraction.
- `mcp`: MCP server support.
- `documents`: Markitdown document conversion.
- `media`: yt-dlp media metadata and subtitles.
- `browser`: optional browser automation tiers.
- `all`: every optional integration.
- `dev`: test, lint, type, and build tools.

## Optional Docker Infrastructure

```bash
bash scripts/start-infra.sh
```

Docker starts local SearXNG and FlareSolverr. It is not required for basic CLI, Python API, or MCP usage.

## Connect An Agent

After install, use [Agent Integrations](integrations.md) for copy-paste configs and tool wrappers.

Use [Recipes](recipes.md) for complete workflows such as Claude Desktop web search, research agents, PDF extraction, and RAG corpus creation.

For the fastest path, generate starter files:

```bash
apeiron init --target cursor --output .
```

## Cache Location

By default Apeiron stores cached fetches under the local application cache directory. Override it per project or CI run with:

```bash
export APEIRON_CACHE_DB="$PWD/.apeiron-cache.db"
```

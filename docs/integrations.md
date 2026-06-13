# Agent Integrations

Apeiron can be used two ways:

- run the MCP server and let an agent client call `apeiron_search`, `apeiron_fetch`, and `apeiron_learn`
- wrap the Python API as native function tools in your own agent runtime

For full copy-run-adapt workflows, see [Recipes](recipes.md).

## Generate Starter Files

Use `apeiron init` when you want files written into a project instead of copying snippets by hand:

```bash
apeiron init --target claude --output .
apeiron init --target cursor --output .
apeiron init --target opencode --output .
apeiron init --target openai-agents --output .
```

Existing files are not overwritten unless you pass `--force`.

## Visual Smoke Test

Use the local demo when you want to see the fetch pipeline before wiring it into an agent:

```bash
apeiron demo
```

The page shows the extracted content and the diagnostics an agent receives: `verdict`, `tier`, `confidence`, `warnings`, `content_type`, and output size.

## Cache Workflow

Agents often ask for the same page more than once. Apeiron keeps successful fetch output in a local SQLite cache and exposes it through the CLI:

```bash
apeiron cache list
apeiron cache search "model context protocol"
apeiron cache clear
```

Use `APEIRON_CACHE_DB=/path/to/project-cache.db` when you want a project-specific cache.

## Claude Desktop

Install Apeiron with the MCP extra, then add this to your Claude Desktop MCP config:

```json
{
  "mcpServers": {
    "apeiron": {
      "command": "python",
      "args": ["-m", "apeiron.api.mcp_server"],
      "cwd": "/path/to/apeiron"
    }
  }
}
```

## Cursor

Use this shape in Cursor's MCP config:

```json
{
  "apeiron": {
    "command": "python",
    "args": ["-m", "apeiron.api.mcp_server"],
    "cwd": "/path/to/apeiron"
  }
}
```

## OpenCode

```jsonc
{
  "mcp": {
    "servers": {
      "apeiron": {
        "command": "python",
        "args": ["-m", "apeiron.api.mcp_server"],
        "cwd": "/path/to/apeiron"
      }
    }
  }
}
```

## OpenAI Agents SDK

The OpenAI Agents SDK can turn typed Python functions into tools with `@function_tool`. Apeiron's sync API is small enough to wrap directly:

```python
import json

from agents import Agent, Runner, function_tool
from apeiron import fetch_sync, search_sync


@function_tool
def apeiron_fetch(url: str) -> str:
    """Fetch a public URL and return LLM-ready content with diagnostics."""
    result = fetch_sync(url, cache_ttl=300)
    return json.dumps(
        {
            "url": result.url,
            "content": result.content[:12000],
            "tier": result.tier.value,
            "verdict": result.verdict.value,
            "content_type": result.content_type,
            "title": result.title,
            "error": result.error,
        },
        ensure_ascii=False,
    )


@function_tool
def apeiron_search(query: str, max_results: int = 5) -> str:
    """Search public web-oriented sources and return ranked hits."""
    hits = search_sync(query, max_results=max_results)
    return json.dumps(
        [
            {
                "title": hit.title,
                "url": hit.url,
                "snippet": hit.snippet,
                "source": hit.source.value,
                "score": hit.score,
            }
            for hit in hits
        ],
        ensure_ascii=False,
    )


agent = Agent(
    name="Research agent",
    instructions="Use Apeiron tools when you need to search or read public web sources.",
    tools=[apeiron_search, apeiron_fetch],
)

result = Runner.run_sync(agent, "Find and summarize the Python packaging guide.")
print(result.final_output)
```

See `examples/openai_agents.py` for the same snippet as a file.

## Plain Python Agent Loop

If your agent runtime can call normal Python functions, start here:

```python
from apeiron import fetch_sync, search_sync


def read_web(query: str) -> str:
    hits = search_sync(query, max_results=3)
    pages = [fetch_sync(hit.url, cache_ttl=300).content for hit in hits]
    return "\n\n---\n\n".join(pages)
```

## Tool Behavior

Keep the tool boundary narrow:

- `apeiron_search` should return titles, URLs, snippets, sources, and scores.
- `apeiron_fetch` should return content plus `tier`, `verdict`, `content_type`, `title`, `elapsed_ms`, and `error`.
- Agents should use `confidence` and `warnings` to decide whether to trust, retry, or ask for another source.
- Agents should inspect `verdict` and `error` before trusting a result.
- Long content should be trimmed or chunked by the host agent runtime.

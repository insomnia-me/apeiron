from __future__ import annotations

import json
from pathlib import Path


TARGETS = ("claude", "cursor", "opencode", "openai-agents")


def generate_init_files(target: str, output_dir: str | Path = ".", *, force: bool = False) -> list[Path]:
    if target not in TARGETS:
        raise ValueError(f"unknown target: {target}")

    base = Path(output_dir)
    files = _target_files(target, base)
    for path, _content in files:
        if path.exists() and not force:
            raise FileExistsError(f"{path} already exists; pass --force to overwrite")

    written: list[Path] = []
    for path, content in files:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


def _target_files(target: str, base: Path) -> list[tuple[Path, str]]:
    if target == "claude":
        return [(base / "claude_desktop_config.json", _json_config("mcpServers"))]
    if target == "cursor":
        return [(base / ".cursor" / "mcp.json", _json_config("mcpServers"))]
    if target == "opencode":
        return [(base / "opencode.jsonc", _opencode_config())]
    if target == "openai-agents":
        return [(base / "apeiron_openai_agents.py", _openai_agents_wrapper())]
    raise ValueError(f"unknown target: {target}")


def _json_config(root_key: str) -> str:
    return json.dumps(
        {
            root_key: {
                "apeiron": {
                    "command": "python",
                    "args": ["-m", "apeiron.api.mcp_server"],
                }
            }
        },
        indent=2,
    ) + "\n"


def _opencode_config() -> str:
    return (
        "{\n"
        '  "mcp": {\n'
        '    "servers": {\n'
        '      "apeiron": {\n'
        '        "command": "python",\n'
        '        "args": ["-m", "apeiron.api.mcp_server"]\n'
        "      }\n"
        "    }\n"
        "  }\n"
        "}\n"
    )


def _openai_agents_wrapper() -> str:
    return '''from __future__ import annotations

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


if __name__ == "__main__":
    result = Runner.run_sync(agent, "Find and summarize the Python packaging guide.")
    print(result.final_output)
'''

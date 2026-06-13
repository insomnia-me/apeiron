from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_links_to_recipes_doc():
    readme = (ROOT / "README.md").read_text()

    assert "[docs/recipes.md](docs/recipes.md)" in readme


def test_recipes_doc_covers_primary_agent_workflows():
    recipes = (ROOT / "docs" / "recipes.md").read_text()

    required = [
        "Give Claude Desktop web search",
        "Build a research agent",
        "Extract PDFs into Markdown",
        "Build a RAG corpus from URLs",
        "Monitor docs changes",
    ]
    for heading in required:
        assert heading in recipes

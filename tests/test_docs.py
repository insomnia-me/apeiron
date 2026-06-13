from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_links_to_recipes_doc():
    readme = (ROOT / "README.md").read_text()

    assert "[docs/recipes.md](docs/recipes.md)" in readme


def test_readme_links_to_comparison_doc():
    readme = (ROOT / "README.md").read_text()

    assert "[docs/comparison.md](docs/comparison.md)" in readme


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


def test_comparison_doc_uses_cautious_positioning():
    comparison = (ROOT / "docs" / "comparison.md").read_text()

    assert "Apeiron is not trying to replace every hosted web API" in comparison
    assert "Firecrawl" in comparison
    assert "Tavily" in comparison
    assert "Exa" in comparison
    assert "Verify current pricing and limits before making a buying decision" in comparison

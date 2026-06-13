from __future__ import annotations

import json
import sys

import pytest


def test_init_cursor_writes_mcp_config(tmp_path):
    from apeiron.init import generate_init_files

    written = generate_init_files("cursor", tmp_path)

    config_path = tmp_path / ".cursor" / "mcp.json"
    assert written == [config_path]
    payload = json.loads(config_path.read_text())
    assert payload["mcpServers"]["apeiron"]["command"] == "python"
    assert payload["mcpServers"]["apeiron"]["args"] == ["-m", "apeiron.api.mcp_server"]


def test_init_openai_agents_writes_tool_wrapper(tmp_path):
    from apeiron.init import generate_init_files

    written = generate_init_files("openai-agents", tmp_path)

    wrapper = tmp_path / "apeiron_openai_agents.py"
    assert written == [wrapper]
    text = wrapper.read_text()
    assert "from agents import Agent, Runner, function_tool" in text
    assert "def apeiron_fetch" in text
    assert "def apeiron_search" in text


def test_init_refuses_to_overwrite_without_force(tmp_path):
    from apeiron.init import generate_init_files

    config_path = tmp_path / ".cursor" / "mcp.json"
    config_path.parent.mkdir()
    config_path.write_text("keep me")

    with pytest.raises(FileExistsError):
        generate_init_files("cursor", tmp_path)

    assert config_path.read_text() == "keep me"


def test_cli_init_prints_written_files(monkeypatch, tmp_path, capsys):
    from apeiron.api import cli

    monkeypatch.setattr(sys, "argv", ["apeiron", "init", "--target", "claude", "--output", str(tmp_path)])

    cli.main()

    assert (tmp_path / "claude_desktop_config.json").exists()
    assert "claude_desktop_config.json" in capsys.readouterr().out

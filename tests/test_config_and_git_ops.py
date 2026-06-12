from __future__ import annotations

import importlib


def test_git_auto_commit_defaults_to_false(monkeypatch):
    monkeypatch.delenv("APEIRON_GIT_COMMIT", raising=False)

    import apeiron.config as config

    reloaded = importlib.reload(config)

    assert reloaded.GIT_AUTO_COMMIT is False


def test_maybe_commit_adds_only_apeiron_owned_files(monkeypatch):
    from apeiron.learn import git_ops
    from apeiron.types import Tier

    calls: list[tuple[str, ...]] = []

    def fake_run_git(*args: str) -> str:
        calls.append(args)
        if args == ("status", "--porcelain"):
            return " M strategies.json\n M README.md"
        return ""

    monkeypatch.setattr(git_ops, "GIT_AUTO_COMMIT", True)
    monkeypatch.setattr(git_ops, "is_git_repo", lambda: True)
    monkeypatch.setattr(git_ops, "_run_git", fake_run_git)

    git_ops.maybe_commit_new_pattern("cloudflare", "https://example.com", Tier.FAST)

    assert ("add", "strategies.json", "apeiron/learn/heuristics.py") in calls
    assert ("add", "-A") not in calls

from __future__ import annotations

import subprocess

from apeiron.config import GIT_AUTO_COMMIT, PROJECT_DIR

APEIRON_OWNED_GIT_PATHS = ("strategies.json", "apeiron/learn/heuristics.py")


def _run_git(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git"] + list(args),
            capture_output=True,
            text=True,
            timeout=10,
            cwd=PROJECT_DIR,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def is_git_repo() -> bool:
    return bool(_run_git("rev-parse", "--is-inside-work-tree"))


def maybe_commit_new_pattern(marker: str, url: str, tier: object):
    """If a new challenge pattern was discovered, commit and push the update."""
    if not GIT_AUTO_COMMIT or not is_git_repo():
        return
    try:
        status = _run_git("status", "--porcelain")
        if not status:
            return
        _run_git("add", *APEIRON_OWNED_GIT_PATHS)
        _run_git("commit", "-m", f"apeiron: new challenge pattern '{marker}' on {url} (tier: {tier})")
        _run_git("push")
    except Exception:
        pass

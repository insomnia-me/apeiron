# Apeiron Audit Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the audit issues that block trust, installation, first-run success, and agent usability.

**Architecture:** Keep Apeiron's current small Python package structure, but add focused diagnostics, deterministic tests, safer defaults, and clearer docs. Separate deterministic core behavior from live network/browser behavior so CI can be green without pretending optional integrations are always installed.

**Tech Stack:** Python 3.10+, setuptools, pytest, ruff, mypy, GitHub Actions, FastMCP optional extra.

---

## File Structure

- Modify `README.md`: replace overclaims and unsafe `pip install apeiron` guidance with local-first positioning, GitHub install commands, profiles, known-good quickstart, and links to docs/examples.
- Modify `pyproject.toml`: add test tooling, ruff/mypy config, and make extras match documented install profiles.
- Modify `.github/workflows/test.yml`: split core deterministic checks from optional/network smoke checks; remove `|| true`.
- Modify `install.sh`: make Docker optional and install the documented full profile.
- Modify `apeiron/config.py`: make git auto-commit opt-in by default.
- Modify `apeiron/learn/git_ops.py`: narrow git add targets.
- Modify `apeiron/fetch/http/curl_cffi.py`: add binary fetch support.
- Modify `apeiron/learn/auto_detect.py`: use binary bytes for document conversion and mark empty extraction as error.
- Modify `apeiron/fetch/media/yt_dlp.py`: return transcript only when actually available; mark unavailable transcript as error/degraded.
- Modify `apeiron/api/mcp_server.py`: return structured JSON for fetch/search/learn.
- Modify `apeiron/api/cli.py`: add `doctor`, `--json`, and clearer source choices.
- Create `apeiron/doctor.py`: dependency/service diagnostics.
- Create `tests/`: deterministic tests for config, git ops, content type, binary extraction, media transcript status, CLI doctor, MCP structured output.
- Create `examples/` and docs hygiene files.

## Tasks

### Task 1: Baseline and test harness

- [ ] Add pytest/ruff/mypy config to `pyproject.toml`.
- [ ] Create deterministic `tests/` structure.
- [ ] Run `python -m pytest` and confirm current missing tests/setup fail or collect correctly before implementation.
- [ ] Add first tests for config default, content type detection, and CLI help.

### Task 2: P0 docs/install trust repair

- [ ] Rewrite README hero and install sections.
- [ ] Remove `pip install apeiron` as canonical guidance.
- [ ] Document install profiles: minimal, fetch, mcp, full.
- [ ] Move unproven bypass/media claims to "Experimental".
- [ ] Update install script so Docker is optional.

### Task 3: P0 CI and quality gates

- [ ] Fix current ruff findings.
- [ ] Add deterministic tests for core behavior.
- [ ] Update CI to run install, pytest, ruff, mypy, build, twine check.
- [ ] Add optional/manual network smoke workflow section.

### Task 4: P0 safe learning/git defaults

- [ ] Write failing tests showing `GIT_AUTO_COMMIT` defaults false.
- [ ] Write failing tests showing git add only targets Apeiron-owned files.
- [ ] Implement config/git_ops changes.
- [ ] Document opt-in behavior in `SECURITY.md`.

### Task 5: P1 doctor and CLI ergonomics

- [ ] Write tests for `apeiron doctor` text and JSON output.
- [ ] Implement `apeiron/doctor.py`.
- [ ] Add CLI `doctor`, `--json` for search/fetch/learn where practical.
- [ ] Verify missing optional packages produce actionable recommendations.

### Task 6: P1 document/media extraction fixes

- [ ] Write tests for binary fetch helper and empty document extraction error.
- [ ] Write tests for YouTube transcript unavailable behavior.
- [ ] Implement binary fetch support.
- [ ] Implement safer YouTube transcript handling.
- [ ] Verify tests pass without live network by mocking external packages.

### Task 7: P1 structured MCP responses

- [ ] Write tests that call MCP tool functions directly.
- [ ] Make search/fetch/learn return JSON with metadata.
- [ ] Update README/examples for structured MCP output.

### Task 8: P2 repo hygiene and examples

- [ ] Add `SECURITY.md`, `CONTRIBUTING.md`, issue templates, PR template.
- [ ] Add `examples/python_api.py`, `examples/opencode.jsonc`, `examples/claude_desktop.md`, `examples/cursor.md`, `examples/cli.md`.
- [ ] Add `docs/install.md`, `docs/benchmarks.md`.
- [ ] Add release checklist and topics list to docs.

### Task 9: Verification and completion audit

- [ ] Run `python -m pytest`.
- [ ] Run `python -m ruff check apeiron tests`.
- [ ] Run `python -m mypy apeiron --ignore-missing-imports`.
- [ ] Run `python -m build`.
- [ ] Run `python -m twine check dist/*`.
- [ ] Run CLI smoke commands from a clean venv where feasible.
- [ ] Compare final repo state against audit backlog and list any external-only actions not possible locally, such as publishing a release or setting GitHub topics.


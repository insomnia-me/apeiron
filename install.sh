#!/usr/bin/env bash
set -euo pipefail

REPO="insomnia-me/apeiron"
TARGET="${APEIRON_HOME:-${HOME}/.apeiron}"
PROFILE="${APEIRON_INSTALL_PROFILE:-fetch,mcp,documents,media}"

log()  { printf "\033[1;34m>\033[0m %s\n" "$*"; }
ok()   { printf "\033[1;32m✓\033[0m %s\n" "$*"; }
fail() { printf "\033[1;31m✗\033[0m %s\n" "$*"; exit 1; }

cat << "ART"
Apeiron — local-first web tools for AI agents
ART

log "Checking required dependencies..."
for cmd in python3 git; do
  command -v "$cmd" >/dev/null 2>&1 || fail "Missing required command: $cmd"
done
ok "Required dependencies found"

log "Cloning or updating repository..."
if [ -d "$TARGET/.git" ]; then
  git -C "$TARGET" pull --ff-only
else
  git clone --depth=1 "https://github.com/${REPO}.git" "$TARGET"
fi
ok "Repository ready at ${TARGET}"

cd "$TARGET"

log "Creating virtual environment..."
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip >/dev/null
ok "Virtual environment ready"

log "Installing Apeiron profile: ${PROFILE}"
.venv/bin/pip install -e ".[${PROFILE}]"
ok "Apeiron installed"

if command -v docker >/dev/null 2>&1; then
  log "Docker found. Optional SearXNG/FlareSolverR infra can be started with: bash scripts/start-infra.sh"
else
  log "Docker not found. Skipping optional SearXNG/FlareSolverR infra."
fi

cat << EOF

Apeiron is ready.

Try:
  ${TARGET}/.venv/bin/apeiron doctor
  ${TARGET}/.venv/bin/apeiron fetch "https://example.com" --json
  ${TARGET}/.venv/bin/apeiron search "python web scraping" --sources wikipedia github arxiv --json

MCP server:
  ${TARGET}/.venv/bin/apeiron serve

EOF

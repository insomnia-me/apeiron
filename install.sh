#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# Apeiron (ἄπειρον) — Unlimited Web Access for AI Agents
#   curl -fsSL https://raw.githubusercontent.com/insomnia-me/apeiron/main/install.sh | bash
# ─────────────────────────────────────────────────────────────
set -euo pipefail
REPO="insomnia-me/apeiron"
TARGET="${HOME}/.apeiron"
REQUIRED=(python3 git docker)

log()  { printf "\r\033[2K  \033[1;34m▶\033[0m  %s\n" "$*"; }
ok()   { printf "\r\033[2K  \033[1;32m✔\033[0m  %s\n" "$*"; }
fail() { printf "\r\033[2K  \033[1;31m✘\033[0m  %s\n" "$*"; exit 1; }

cat << "ART"
  ⚡ Apeiron (ἄπειρον) — Unlimited Web Access
  "That which has no boundaries"
ART

log "Checking dependencies..."
for cmd in "${REQUIRED[@]}"; do
  command -v "$cmd" &>/dev/null || fail "Missing: $cmd"
done
ok "All dependencies found"

log "Cloning repository..."
if [ -d "$TARGET/.git" ]; then
  (cd "$TARGET" && git pull --ff-only) || true
else
  git clone --depth=1 "https://github.com/${REPO}.git" "$TARGET"
fi
ok "Repository ready at ${TARGET}"

cd "$TARGET"

log "Creating Python virtual environment..."
python3 -m venv .venv
ok "Virtual environment created"

log "Installing core dependencies..."
.venv/bin/pip install --quiet -e "." 2>&1 | tail -1
ok "Core packages installed"

log "Installing all extras..."
.venv/bin/pip install --quiet -e ".[all]" 2>&1 | tail -1
ok "All extras installed"

log "Installing browser engines..."
.venv/bin/pip install --quiet cloakbrowser 2>&1 | tail -1
if command -v .venv/bin/patchright &>/dev/null; then
  .venv/bin/patchright install chromium 2>&1 | tail -1
fi
if command -v .venv/bin/scrapling &>/dev/null; then
  .venv/bin/scrapling install 2>&1 | tail -1 || true
fi
.venv/bin/python -m camoufox fetch 2>&1 | tail -1 || true
ok "Browser engines ready"

log "Starting infrastructure (SearXNG + FlareSolverr)..."
bash scripts/start-infra.sh 2>&1 | tail -1 || log "Docker infra skipped (optional)"

cat << "EOF"

  ─────────────────────────────────────────────────────────────
  ✅  Apeiron installed!

  Quick test:
    cd ~/.apeiron
    .venv/bin/apeiron fetch "https://httpbin.org/html"
    .venv/bin/apeiron search "quantum computing 2026"
    .venv/bin/apeiron learn "https://httpbin.org/html"

  MCP server for your AI agent:
    .venv/bin/apeiron serve

  Then add to OpenCode config:
    "mcp": {
      "servers": {
        "apeiron": {
          "command": "python",
          "args": ["-m", "apeiron.api.mcp_server"],
          "cwd": "~/.apeiron"
        }
      }
    }

  ─────────────────────────────────────────────────────────────
EOF

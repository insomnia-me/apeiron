#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
echo "⚡ Generating Apeiron demo GIFs..."
echo "   Requires: vhs (brew install vhs) + ttyd + ffmpeg"
echo "   Requires: apeiron installed in PATH"
echo ""

# Ensure apeiron is findable (for install.sh users)
export PATH="$HOME/.apeiron/.venv/bin:$PATH"

cd "$REPO/demos"

for tape in *.tape; do
  name="${tape%.tape}"
  echo "  ▶ $tape → ${name}.gif"
  vhs "$tape" 2>&1 | tail -1
done

echo ""
echo "✅ All GIFs generated in demos/"
ls -lh *.gif 2>/dev/null

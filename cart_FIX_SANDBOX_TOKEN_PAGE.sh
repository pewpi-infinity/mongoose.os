#!/data/data/com.termux/files/usr/bin/bash
# FIX: add TOKEN.md to each sandbox for vectorizer

set -euo pipefail
BASE="$HOME/infinity-repos"

for d in "$BASE"/infinity-sandbox-*; do
  [ -d "$d" ] || continue
  if [ ! -f "$d/TOKEN.md" ]; then
    cat << TOK > "$d/TOKEN.md"
# $(basename "$d")

## Modes
- 🔵 Engineer (build / paid)
- 🟢 Fix (repair / stabilize)
- 🟠 Decide (route / approve)
- 🟣 Assimilate (learn / merge)

## Vector
- source: sandbox
- created: $(date -u)
TOK
  fi
done

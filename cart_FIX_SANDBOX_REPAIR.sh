#!/data/data/com.termux/files/usr/bin/bash
# FIX: repair broken carts (permissions + shebang)

set -euo pipefail
BASE="$HOME/infinity-repos"

for d in "$BASE"/infinity-sandbox-*; do
  [ -d "$d" ] || continue
  for f in "$d"/cart_*; do
    [ -f "$f" ] || continue
    sed -i '1s|^#!.*|#!/usr/bin/env bash|' "$f" || true
    chmod +x "$f" || true
  done
done

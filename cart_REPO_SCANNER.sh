#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

API="http://127.0.0.1:5051/signal"
ROOT="$HOME"
COUNT=0

echo "[∞] Repo scanner online"

for repo in $(find "$ROOT" -maxdepth 2 -type d -name ".git" 2>/dev/null | sed 's|/.git||'); do
  COUNT=$((COUNT+1))
  echo "[→] Scanning $repo"
  curl -s -X POST "$API" \
    -H "Content-Type: application/json" \
    -d "{\"type\":\"repo_scan\",\"repo\":\"$repo\"}" >/dev/null
done

echo "[✓] Scanned $COUNT repos"

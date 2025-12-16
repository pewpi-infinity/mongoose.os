#!/data/data/com.termux/files/usr/bin/bash
set -e

ORG="pewpi-infinity"
OUT="$HOME/infinity-treasury/GLOBAL_REPO_CENSUS.json"

echo "[∞] Running global repo census for $ORG"

gh repo list "$ORG" --limit 1000 --json name,description,updatedAt,url \
  > "$OUT"

echo "[✓] Census written to $OUT"

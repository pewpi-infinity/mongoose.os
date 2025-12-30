#!/data/data/com.termux/files/usr/bin/bash
set -e

ORG="pewpi-infinity"
OUT="$(pwd)/GLOBAL_REPO_CENSUS.json"

echo "[∞] Generating GLOBAL_REPO_CENSUS.json for $ORG"

gh repo list "$ORG" --limit 1000 \
  --json name,description,updatedAt,url \
  > "$OUT"

echo "[✓] Census written to $OUT"

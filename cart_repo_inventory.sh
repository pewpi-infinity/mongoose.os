#!/data/data/com.termux/files/usr/bin/bash
set -e

ORG="pewpi-infinity"
OUT="infinity_repo_inventory.txt"

echo "[∞] Fetching repo list for $ORG"
gh repo list "$ORG" --limit 500 --json name,description,updatedAt \
  --jq '.[] | "\(.name)\t\(.updatedAt)\t\(.description)"' \
  > "$OUT"

echo "[✓] Inventory written to $OUT"

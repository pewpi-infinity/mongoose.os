#!/data/data/com.termux/files/usr/bin/bash
# PAY: register paid engineering task tokens

set -euo pipefail
BASE="$HOME/infinity-repos"
OUT="$HOME/infinity_storage/payments"
mkdir -p "$OUT"

for d in "$BASE"/infinity-sandbox-*; do
  [ -d "$d" ] || continue
  ID=$(basename "$d")
  FILE="$OUT/${ID}_engineer.json"
  if [ ! -f "$FILE" ]; then
    cat << JSON > "$FILE"
{
  "repo": "$ID",
  "mode": "engineer",
  "rate": "INF",
  "status": "open",
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
JSON
  fi
done

#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASE="$(pwd)"
IDX="$BASE/infinity_storage/index"
GEN="$BASE/cart_generated"
mkdir -p "$IDX"

echo "[∞] INDEX VIEWS"

echo "{ \"overview\": {" > "$IDX/views.json"
echo "  \"total_carts\": $(ls cart_*.sh 2>/dev/null | wc -l)," >> "$IDX/views.json"
echo "  \"generated\": $(ls $GEN 2>/dev/null | wc -l)" >> "$IDX/views.json"
echo "}}" >> "$IDX/views.json"

echo "[✓] Views updated"

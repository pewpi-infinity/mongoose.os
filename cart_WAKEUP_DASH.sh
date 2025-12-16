#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "[∞] WAKEUP DASH"
echo
echo "Recent generated carts:"
ls -1 cart_generated 2>/dev/null | tail -n 10
echo
echo "Index overview:"
cat infinity_storage/index/views.json 2>/dev/null
echo
echo "[✓] Swimming in intelligence"

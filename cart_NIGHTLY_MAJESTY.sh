#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "[∞] Nightly Majesty Cycle"
python3 cart_INTEL_ENGINE.py
./cart_INDEX_VIEWS.sh
echo "[✓] Majesty complete"

#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "[∞] Restarting mongoose.os API"

pkill -f cart_MONGOOSE_API.py || true
sleep 1

nohup python3 cart_MONGOOSE_API.py > infinity_storage/logs/mongoose_api.out 2>&1 &
disown

echo "[✓] API restarted"

#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "[∞] Checking mongoose.os API"

ps aux | grep -v grep | grep cart_MONGOOSE_API.py || {
  echo "[!] API process not found"
  exit 1
}

echo
echo "[∞] Health:"
curl -s http://127.0.0.1:5051/health || echo "NO RESPONSE"

echo
echo "[∞] Live:"
curl -s http://127.0.0.1:5051/live || echo "NO RESPONSE"

echo
echo "[✓] API is alive"

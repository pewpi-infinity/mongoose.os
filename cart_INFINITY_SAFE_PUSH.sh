#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

LOGDIR="infinity_storage/logs"
mkdir -p "$LOGDIR"

echo "[∞] Infinity Safe Push"

# show status
git status --short || true
echo

# nothing changed?
if git diff --quiet && git diff --cached --quiet; then
  echo "[∞] No changes to commit"
  exit 0
fi

# auto mode
AUTO_MODE="${INFINITY_AUTO:-0}"
if [ "$AUTO_MODE" = "1" ]; then
  echo "[∞] AUTO mode detected — skipping confirmation"
else
  read -p "[∞] Continue with add/commit? (y/n): " CONFIRM
  [[ "$CONFIRM" =~ ^[yY]$ ]] || exit 0
fi

# sparse-safe add
git add --sparse .

# nothing staged?
if git diff --cached --quiet; then
  echo "[∞] Nothing staged after sparse add"
  exit 0
fi

MSG="Infinity auto commit $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$MSG"
git push

date '+%Y-%m-%d %H:%M:%S' > "$LOGDIR/last_push.time"
echo "[∞] $MSG" >> "$LOGDIR/push.log"

echo "[✓] Safe Push complete"

#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

LOGDIR="infinity_storage/logs"
mkdir -p "$LOGDIR"

echo "[∞] Infinity Safe Push"

# Detect auto mode
AUTO_MODE="${INFINITY_AUTO:-0}"

# Check for changes
if git diff --quiet && git diff --cached --quiet; then
  echo "[∞] No changes to commit"
  exit 0
fi

echo "[∞] Modified files:"
git status --short
echo

if [ "$AUTO_MODE" = "1" ]; then
  echo "[∞] AUTO mode detected — skipping confirmation"
  CONFIRM="y"
else
  read -p "[∞] Continue with add/commit? (y/n): " CONFIRM
fi

if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
  echo "[∞] Commit aborted by user"
  exit 0
fi

# Stage & commit
git add .

COMMIT_MSG="Infinity auto commit $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MSG" || {
  echo "[∞] Nothing new to commit"
  exit 0
}

# Push
git push

# Log success
date '+%Y-%m-%d %H:%M:%S' > "$LOGDIR/last_push.time"
echo "[∞] Push successful: $COMMIT_MSG" >> "$LOGDIR/push.log"

echo "[✓] Infinity Safe Push complete"

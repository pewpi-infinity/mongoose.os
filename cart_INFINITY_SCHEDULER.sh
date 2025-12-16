#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

INTERVAL="${INFINITY_INTERVAL:-300}"   # 5 minutes default
LOGDIR="infinity_storage/logs"
mkdir -p "$LOGDIR"

echo "[∞] Infinity Scheduler ONLINE"
echo "[∞] Interval: ${INTERVAL}s"

while true; do
  TS="$(date '+%Y-%m-%d %H:%M:%S')"
  echo "[∞] Tick @ $TS"
  echo "$TS tick" >> "$LOGDIR/scheduler.log"

  INFINITY_AUTO=1 ./cart_INFINITY_SAFE_PUSH.sh || true

  for ((i=INTERVAL; i>0; i-=30)); do
    printf "[∞] Sleeping… %02d:%02d\n" $((i/60)) $((i%60))
    sleep 30
  done
done

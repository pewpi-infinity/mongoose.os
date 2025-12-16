#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASE="$(pwd)"
GEN="$BASE/cart_generated"
LOG="$BASE/infinity_storage/logs/infinite_engine.log"
IDX="$BASE/infinity_storage/index"
STATE="$BASE/infinity_storage/state"

mkdir -p "$GEN" "$IDX" "$STATE" "$(dirname "$LOG")"

echo "[∞] INFINITE ENGINE ONLINE"
echo "[∞] BASE: $BASE"
echo "[∞] Press CTRL+C to stop"
echo

# ---------- CLASSIFICATION RULES ----------
bucket_for() {
  local name="$1"
  if [[ "$name" =~ js|spa|react|vue ]]; then echo "02-js"; return; fi
  if [[ "$name" =~ index|map|graph ]]; then echo "04-index"; return; fi
  if [[ "$name" =~ api|server|flask ]]; then echo "07-api"; return; fi
  if [[ "$name" =~ cart ]]; then echo "01-cart"; return; fi
  echo "99-misc"
}

# ---------- CART GENERATOR ----------
make_cart() {
  local topic="$1"
  local bucket="$2"
  local ts sig file

  ts="$(date +%s)"
  sig="$(echo "$topic-$ts" | sha1sum | cut -c1-8)"
  file="$GEN/cart_AUTO_${bucket}_${topic}_${sig}.sh"

  cat << CART > "$file"
#!/bin/bash
echo "[∞] CART: $topic"
echo "[∞] BUCKET: $bucket"
echo "[∞] TIME: $(date)"
sleep 0.3
echo "[✓] $topic operational"
CART

  chmod +x "$file"
  echo "[BUILD] $file"
  echo "{\"topic\":\"$topic\",\"bucket\":\"$bucket\",\"file\":\"$(basename "$file")\",\"ts\":$ts}" >> "$IDX/feed.json"
}

# ---------- MAIN LOOP ----------
i=0
while true; do
  i=$((i+1))
  echo "[∞] TICK $i $(date)" | tee -a "$LOG"

  # scan repo tree fast
  find "$BASE" -maxdepth 3 -type f \( -name "*.py" -o -name "*.sh" -o -name "*.js" \) \
    | shuf -n 5 | while read -r f; do
        name="$(basename "$f" | sed 's/\..*//')"
        bucket="$(bucket_for "$f")"
        make_cart "$name" "$bucket"
    done

  # write heartbeat
  echo "{\"tick\":$i,\"time\":\"$(date)\"}" > "$STATE/heartbeat.json"

  # visible motion speed
  sleep 1
done

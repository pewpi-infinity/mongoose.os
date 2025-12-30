#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASE="$HOME/infinity-seeds"
mkdir -p "$BASE"
cd "$BASE"

for i in $(seq -w 1 100); do
  DIR="infinity-seed-$i"
  mkdir -p "$DIR"
  cd "$DIR"

  git init >/dev/null

  cat > seed.manifest.json <<JSON
{
  "seed_id": $((10#$i)),
  "role": "seed-node",
  "parent_system": "infinity",
  "status": "idle",
  "created_utc": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
JSON

  cat > cart_seed_$i.py <<PY
# cart_seed_$i.py
# Infinity Seed Cart $i
# Purpose: Expansion anchor / bolt-farm ignition

def seed_status():
    return {
        "seed": $((10#$i)),
        "status": "online",
        "role": "reference-point"
    }

if __name__ == "__main__":
    print(seed_status())
PY

  cat > README.md <<MD
# Infinity Seed $i

This repository is a **seed node** in the Infinity system.

Seed ID: $i  
Role: Reference / Expansion / Bolt-Farm  

Lightweight by design.
MD

  git add .
  git commit -m "∞ Initialize Infinity Seed $i" >/dev/null

  cd ..
done

echo "[✓] 100 Infinity seed repos initialized at $BASE"

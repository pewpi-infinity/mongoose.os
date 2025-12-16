#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ORG="pewpi-infinity"

echo "[∞] Creating Infinity Brain repos on GitHub"
echo "[∞] Org: $ORG"
echo

for i in $(seq -w 1 100); do
  REPO="infinity-brain-$i"

  echo "[→] Creating $REPO"

  gh repo create "$ORG/$REPO" \
    --public \
    --confirm \
    --description "Infinity Distributed Brain Node $i"

done

echo
echo "[✓] GitHub repo creation complete"

#!/data/data/com.termux/files/usr/bin/bash
set -e

ORG="pewpi-infinity"
COUNT=$(gh repo list "$ORG" --limit 1000 | grep infinity-brain- | wc -l)

if [ "$COUNT" -gt 80 ]; then
  NEXT=$(printf "%03d" $((COUNT+1)))
  REPO="infinity-brain-$NEXT"
  echo "[∞] Auto-creating overflow brain: $REPO"
  gh repo create "$ORG/$REPO" --public --confirm \
    --description "Auto-scaled Infinity Brain Node $NEXT"
fi

echo "[✓] Green pasture ready for planting"

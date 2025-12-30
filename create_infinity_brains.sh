#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASE="$HOME/infinity-brains"
ORG="pewpi-infinity"

echo "[∞] Creating Infinity Brain Repos"
echo "[∞] Base dir: $BASE"
echo "[∞] GitHub org: $ORG"
echo

mkdir -p "$BASE"
cd "$BASE"

for i in $(seq -w 1 100); do
  REPO="infinity-brain-$i"
  DIR="$BASE/$REPO"

  echo "[→] $REPO"

  mkdir -p "$DIR"
  cd "$DIR"

  if [ ! -d ".git" ]; then
    git init
  fi

  # Identity file
  cat << ID > README.md
# $REPO

Infinity Distributed Brain Node

- Brain ID: $i
- Role: $( [ "$i" = "04" ] && echo "Dashboard / Index" || echo "Specialized Logic Node" )
- System: Infinity / Octave / Mongoose

This repo is part of the Infinity distributed intelligence architecture.
ID

  # Placeholder structure
  mkdir -p carts logs data

  if [ "$i" = "04" ]; then
    mkdir -p dashboard
    cat << DASH > dashboard/index.md
# Infinity Brain 04 — Dashboard

This node aggregates and displays status from all other brains.

Responsibilities:
- Index visualization
- Health checks
- Token summaries
- Cross-brain navigation
DASH
  fi

  git add -A
  git commit -m "Initialize $REPO" || true

  # Set remote if not present
  if ! git remote | grep -q origin; then
    git remote add origin "https://github.com/$ORG/$REPO.git"
  fi

  git branch -M main
  git push -u origin main || echo "[!] Push failed for $REPO (repo may not exist yet)"

  cd "$BASE"
  echo
done

echo "[✓] Infinity Brain creation complete"

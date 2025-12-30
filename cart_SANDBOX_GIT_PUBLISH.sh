#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ORG="pewpi-infinity"
BASE="$HOME/infinity-repos"

for d in "$BASE"/infinity-sandbox-*; do
  [ -d "$d" ] || continue
  cd "$d"
  if [ ! -d .git ]; then
    NAME=$(basename "$d")
    git init
    git branch -M main
    git add .
    git commit -m "Initialize $NAME"
    gh repo create "$ORG/$NAME" --private --source=. --remote=origin --push
    echo "[✓] pushed $NAME"
  fi
done

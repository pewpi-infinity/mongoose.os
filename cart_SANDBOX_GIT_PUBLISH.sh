#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ORG="pewpi-infinity"
BASE="$HOME/infinity-repos"

echo "[∞] Sandbox Git Publisher online"

for d in "$BASE"/infinity-sandbox-*; do
  [ -d "$d" ] || continue
  cd "$d"

  if [ ! -d .git ]; then
    NAME=$(basename "$d")
    echo "[→] Initializing $NAME"

    git init
    git branch -M main
    git add .
    git commit -m "Initialize $NAME"

    gh repo create "$ORG/$NAME" --private --source=. --remote=origin --push

    echo "[✓] Published $NAME"
  fi
done

echo "[✓] Sandbox publish pass complete"

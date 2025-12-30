#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASE="$(pwd)"
GEN="$BASE/cart_generated"
REPOS="$BASE/.repos"
LOG="$BASE/infinity_storage/logs/repo_autocreator.log"

ORG="pewpi-infinity"
VISIBILITY="public"
MAX_COMMITS=25   # rotate repo after this many commits

mkdir -p "$REPOS" "$(dirname "$LOG")"

# ---------- name pool ----------
NAMES=(oak pine ant bee rover patrol sentinel atlas nova)

# ---------- bucket mapping ----------
bucket_group() {
  case "$1" in
    01*) echo "carts" ;;
    02*) echo "js" ;;
    04*) echo "index" ;;
    07*) echo "api" ;;
    *)   echo "misc" ;;
  esac
}

# ---------- repo naming ----------
current_repo_name() {
  local group="$1"
  local idx_file="$REPOS/.${group}_index"
  [ -f "$idx_file" ] || echo 0 > "$idx_file"
  local i
  i=$(cat "$idx_file")
  echo "infinity-${group}-${i}"
}

rotate_repo() {
  local group="$1"
  local idx_file="$REPOS/.${group}_index"
  local i
  i=$(cat "$idx_file")
  echo $((i+1)) > "$idx_file"
}

ensure_repo() {
  local repo="$1"
  if ! gh repo view "$ORG/$repo" >/dev/null 2>&1; then
    echo "[+] Creating repo: $repo"
    gh repo create "$ORG/$repo" --$VISIBILITY --confirm
  fi
}

ensure_clone() {
  local repo="$1"
  if [ ! -d "$REPOS/$repo/.git" ]; then
    git clone "https://github.com/$ORG/$repo.git" "$REPOS/$repo"
  fi
}

commit_count() {
  cd "$1" && git rev-list --count HEAD 2>/dev/null || echo 0
}

commit_cart() {
  local repo="$1"
  local cart="$2"
  cp "$GEN/$cart" "$REPOS/$repo/$cart"
  chmod +x "$REPOS/$repo/$cart"
  cd "$REPOS/$repo"
  git add "$cart"
  git commit -m "auto: $cart"
  git push
}

# ---------- main loop ----------
declare -A SEEN
echo "[∞] Repo Auto-Creator (rotating) ONLINE"

while true; do
  for f in "$GEN"/cart_AUTO_*.sh; do
    [ -e "$f" ] || continue
    bn="$(basename "$f")"
    [ "${SEEN[$bn]+x}" ] && continue
    SEEN[$bn]=1

    bucket="$(echo "$bn" | cut -d_ -f3)"
    group="$(bucket_group "$bucket")"
    repo="$(current_repo_name "$group")"

    ensure_repo "$repo"
    ensure_clone "$repo"

    count="$(commit_count "$REPOS/$repo")"
    if [ "$count" -ge "$MAX_COMMITS" ]; then
      echo "[↻] Rotating repo for $group (commit cap reached)"
      rotate_repo "$group"
      repo="$(current_repo_name "$group")"
      ensure_repo "$repo"
      ensure_clone "$repo"
    fi

    echo "[→] $bn → $repo"
    commit_cart "$repo" "$bn"
    echo "[✓] committed to $repo" | tee -a "$LOG"
  done
  sleep 2
done

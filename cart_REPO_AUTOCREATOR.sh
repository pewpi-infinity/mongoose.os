#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

# REQUIREMENTS:
# 1) gh CLI installed
# 2) gh auth login already completed
# 3) git configured (user.name / user.email)

BASE="$(pwd)"
GEN="$BASE/cart_generated"
LOG="$BASE/infinity_storage/logs/repo_autocreator.log"
ORG="pewpi-infinity"   # change if needed
VISIBILITY="public"    # public | private

mkdir -p "$GEN" "$(dirname "$LOG")"

echo "[∞] REPO AUTO-CREATOR ONLINE"
echo "[∞] Org/User: $ORG"
echo "[∞] Watching: $GEN"
echo "[∞] Press CTRL+C to stop"
echo

# ---- bucket -> repo naming rules ----
repo_for_bucket() {
  case "$1" in
    01-cart*) echo "infinity-carts-core" ;;
    02-js*)   echo "infinity-js-spa" ;;
    04-index*)echo "infinity-index-engine" ;;
    07-api*)  echo "infinity-api-services" ;;
    *)        echo "infinity-misc-lab" ;;
  esac
}

ensure_repo() {
  local repo="$1"
  if gh repo view "$ORG/$repo" >/dev/null 2>&1; then
    echo "[=] Repo exists: $repo"
  else
    echo "[+] Creating repo: $repo"
    gh repo create "$ORG/$repo" --$VISIBILITY --confirm
  fi
}

clone_or_pull() {
  local repo="$1"
  if [ ! -d "$BASE/.repos/$repo/.git" ]; then
    mkdir -p "$BASE/.repos"
    git clone "https://github.com/$ORG/$repo.git" "$BASE/.repos/$repo"
  else
    (cd "$BASE/.repos/$repo" && git pull)
  fi
}

commit_cart() {
  local repo="$1"
  local cart="$2"
  local src="$GEN/$cart"
  local dst="$BASE/.repos/$repo/$cart"

  cp "$src" "$dst"
  chmod +x "$dst"

  (cd "$BASE/.repos/$repo" && \
    git add "$cart" && \
    git commit -m "auto: add $cart" && \
    git push)
}

# ---- main loop ----
declare -A SEEN
while true; do
  for f in "$GEN"/cart_AUTO_*.sh; do
    [ -e "$f" ] || continue
    bn="$(basename "$f")"
    [ "${SEEN[$bn]+x}" ] && continue
    SEEN[$bn]=1

    bucket="$(echo "$bn" | cut -d_ -f3)"
    repo="$(repo_for_bucket "$bucket")"

    echo "[→] Routing $bn → $repo"
    ensure_repo "$repo"
    clone_or_pull "$repo"
    commit_cart "$repo" "$bn"

    echo "[✓] Committed $bn to $repo" | tee -a "$LOG"
  done
  sleep 2
done

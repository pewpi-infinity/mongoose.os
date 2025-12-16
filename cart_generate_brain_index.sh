#!/data/data/com.termux/files/usr/bin/bash
set -e

ORG="pewpi-infinity"
WORKDIR="$HOME/infinity-brains"
OUTDIR="$HOME/infinity-treasury"
JSON_OUT="$OUTDIR/BRAIN_INDEX.json"
MD_OUT="$OUTDIR/BRAIN_INDEX.md"

mkdir -p "$WORKDIR" "$OUTDIR"

echo "[∞] Generating Infinity Brain Index"
echo "[∞] Org: $ORG"
echo

echo "[" > "$JSON_OUT"
FIRST=1

gh repo list "$ORG" --limit 500 --json name,updatedAt \
  --jq '.[] | select(.name | startswith("infinity-brain-")) | "\(.name)\t\(.updatedAt)"' |
while IFS=$'\t' read -r REPO UPDATED; do

  echo "[→] Indexing $REPO"
  cd "$WORKDIR"

  if [ ! -d "$REPO" ]; then
    git clone "https://github.com/$ORG/$REPO.git" >/dev/null 2>&1
  fi

  cd "$REPO"

  # Explicit pull, no tracking assumptions
  git fetch origin >/dev/null 2>&1 || true
  git checkout main >/dev/null 2>&1 || true
  git pull origin main >/dev/null 2>&1 || true

  if [ -f brain.yaml ]; then
    ID=$(grep '^  id:' brain.yaml | awk '{print $2}')
    ROLE=$(grep '^  role:' brain.yaml | awk '{print $2}')
    VERSION=$(grep '^  version:' brain.yaml | awk '{print $2}')
    STATUS=$(grep '^  status:' brain.yaml | awk '{print $2}')
  else
    ID="$REPO"
    ROLE="unknown"
    VERSION="unknown"
    STATUS="missing_contract"
  fi

  if [ $FIRST -eq 0 ]; then
    echo "," >> "$JSON_OUT"
  fi
  FIRST=0

  cat << JSON >> "$JSON_OUT"
  {
    "repo": "$REPO",
    "id": "$ID",
    "role": "$ROLE",
    "version": "$VERSION",
    "status": "$STATUS",
    "updated_at": "$UPDATED",
    "url": "https://github.com/$ORG/$REPO"
  }
JSON

done

echo "]" >> "$JSON_OUT"

echo "[✓] JSON index written to $JSON_OUT"

# Markdown index (requires jq)
echo "# Infinity Brain Index" > "$MD_OUT"
echo >> "$MD_OUT"
echo "| Repo | Role | Version | Status | Updated |" >> "$MD_OUT"
echo "|------|------|---------|--------|---------|" >> "$MD_OUT"

jq -r '.[] | "| \(.repo) | \(.role) | \(.version) | \(.status) | \(.updated_at) |"' "$JSON_OUT" \
  >> "$MD_OUT"

echo "[✓] Markdown index written to $MD_OUT"
echo "[✓] Brain index generation complete"

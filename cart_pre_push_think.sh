#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "[∞] Pre-Push Cognitive Scan"

# Detect sparse checkout
if git config --get core.sparseCheckout | grep -q true; then
  echo "[i] Sparse-checkout active"
fi

# Detect blocked paths
BLOCKED=$(git status --short | grep '^??' || true)
if [ -n "$BLOCKED" ]; then
  echo "[!] Untracked files detected:"
  echo "$BLOCKED"
fi

# Detect cart reference failures
BROKEN=$(grep -R "cart[0-9]\{3\}_" -n . --exclude-dir=.git \
  | grep -E "factory|module" \
  | while read -r line; do
      REF=$(echo "$line" | sed -E 's/.*(cart[0-9]{3}_[a-zA-Z0-9_]+).*/\1/')
      [ ! -f "$REF.py" ] && echo "$REF"
    done)

if [ -n "$BROKEN" ]; then
  echo "[✗] Broken cart references detected:"
  echo "$BROKEN"
  echo "[→] Recommendation: normalize or split into a new repo (bolt-farm)"
fi

echo "[✓] Cognitive scan complete"

#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "[∞] Cart Name Normalizer (dry-run)"

for f in cart[0-9][0-9][0-9]*.py; do
  if echo "$f" | grep -qv "_"; then
    echo "[!] Non-canonical name: $f"
  fi
done

echo "[i] No changes made (dry-run)"

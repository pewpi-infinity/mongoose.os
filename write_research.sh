#!/usr/bin/env bash
set -euo pipefail

CHAIN="${1:?Chain number (e.g., 0001)}"
PAGE="${2:?Page number (e.g., 0001)}"
TITLE="${3:?Short-title-lowercase-with-dashes}"
shift 3

OUT="research/CHAIN-${CHAIN}/PAGE-${PAGE}-${TITLE}.txt"
mkdir -p "research/CHAIN-${CHAIN}"

# The remaining args are your research paragraphs. Paste freely.
CONTENT="$*"

# Write as real words, no code.
printf "%s\n" "$CONTENT" > "$OUT"

echo "$(date -Iseconds) | WRITE | $OUT | bytes=$(wc -c < "$OUT")" | tee -a logs/provenance.log
printf "%s\n" "$OUT"

#!/usr/bin/env bash
set -euo pipefail

mkdir -p storage
OUT="storage/tweets.jsonl"

TYPE="${1:?type (token|link|note)}"
shift

case "$TYPE" in
  token)
    CHAIN="${1:?chain}"; TOKEN="${2:?token}"; REF="${3:?ref path}"; PRICE="${4:-ask}"
    TWT="token:$CHAIN-$TOKEN | ref:$REF | price:$PRICE"
    ;;
  link)
    CHAIN="${1:?chain}"; FROM="${2:?from}"; TO="${3:?to}"
    TWT="link:$CHAIN | $FROM -> $TO"
    ;;
  note)
    TWT="$*"
    ;;
  *)
    echo "Unknown type"; exit 1
    ;;
esac

# Trim to ~240 chars to be safe
TWT_TRIM=$(printf "%s" "$TWT" | cut -c1-240)

jq -n --arg t "$TWT_TRIM" --arg ts "$(date -Iseconds)" '{tweet:$t,ts:$ts}' >> "$OUT"

echo "$(date -Iseconds) | TWEET-QUEUE | ${TWT_TRIM}" | tee -a logs/provenance.log
printf "%s\n" "$OUT"

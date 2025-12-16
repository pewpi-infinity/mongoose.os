#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

MODE="${1:-auto}"

echo "[∞] CART INDEX"
echo "[∞] Repo: $(pwd)"
echo

CARTS_SH=$(ls cart_*.sh 2>/dev/null | grep -v cart_index.sh || true)
CARTS_PY=$(ls cart_*.py 2>/dev/null || true)

if [ -z "$CARTS_SH$CARTS_PY" ]; then
  echo "[!] No carts found"
  exit 0
fi

echo "[∞] Shell carts:"
for c in $CARTS_SH; do echo "  - $c"; done
echo

echo "[∞] Python carts:"
for c in $CARTS_PY; do echo "  - $c"; done
echo

run_all() {
  for c in $CARTS_SH; do
    echo "[→] Running $c"
    bash "$c"
  done

  for c in $CARTS_PY; do
    echo "[→] Running $c"
    python3 "$c"
  done
}

case "$MODE" in
  list)
    ;;
  run)
    run_all
    ;;
  auto)
    export INFINITY_AUTO=1
    run_all
    if [ -x ./cart_INFINITY_SAFE_PUSH.sh ]; then
      echo "[↑] Auto pushing changes"
      ./cart_INFINITY_SAFE_PUSH.sh
    fi
    ;;
  *)
    echo "[!] Unknown mode: $MODE"
    echo "Usage: ./cart_index.sh [list|run|auto]"
    exit 1
    ;;
esac

echo
echo "[✓] CART INDEX complete"

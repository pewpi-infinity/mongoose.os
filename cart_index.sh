#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

MODE="${1:-list}"

echo "[∞] CART INDEX"
echo "[∞] Repo: $(pwd)"
echo

CARTS_SH=$(ls cart_*.sh 2>/dev/null | grep -v cart_index.sh || true)
CARTS_PY=$(ls cart_*.py 2>/dev/null || true)

if [ -z "$CARTS_SH$CARTS_PY" ]; then
  echo "[!] No carts found"
  exit 0
fi

show_index() {
  echo "[∞] Shell carts:"
  for c in $CARTS_SH; do echo "  - $c"; done
  echo
  echo "[∞] Python carts:"
  for c in $CARTS_PY; do echo "  - $c"; done
  echo
}

run_carts() {
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
  help|-h|--help)
    echo "Usage:"
    echo "  ./cart_index.sh           # show index"
    echo "  ./cart_index.sh list      # show index"
    echo "  ./cart_index.sh run       # run all carts"
    echo "  ./cart_index.sh auto      # run + push"
    echo
    exit 0
    ;;
  list)
    show_index
    ;;
  run)
    show_index
    run_carts
    ;;
  auto)
    show_index
    run_carts
    if [ -x ./cart_push_all.sh ]; then
      echo "[↑] Pushing changes"
      ./cart_push_all.sh
    else
      echo "[!] cart_push_all.sh not found or not executable"
    fi
    ;;
  *)
    echo "[!] Unknown option: $MODE"
    echo "Run: ./cart_index.sh help"
    exit 1
    ;;
esac

echo "[✓] CART INDEX complete"

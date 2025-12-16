#!/data/data/com.termux/files/usr/bin/bash
echo "[∞] SYSTEM STATUS"
echo "Time: $(date)"
echo
echo "Carts:"
ls -1 cart_*.sh cart_*.py 2>/dev/null | wc -l
echo
echo "Generated carts:"
ls -1 cart_generated 2>/dev/null | wc -l
echo
echo "API:"
curl -s http://127.0.0.1:5051/health || echo "API down"
echo
echo "[✓] Status complete"

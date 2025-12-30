#!/data/data/com.termux/files/usr/bin/bash
# UNIFY: run all structural layers together

set -euo pipefail

python3 cart_STRUCTURAL_INDEXER.py
python3 cart_VECTOR_TOKENIZE.py
./cart_FIX_SANDBOX_REPAIR.sh
./cart_DECIDE_ROUTE.sh
./cart_PAY_ENGINEER.sh

#!/data/data/com.termux/files/usr/bin/bash
set -e

REPO_NAME="$(basename "$(pwd)")"

if [ -f brain.yaml ]; then
  echo "[✓] brain.yaml already exists in $REPO_NAME"
  exit 0
fi

echo "[∞] Injecting brain.yaml into $REPO_NAME"

cat << 'YAML' > brain.yaml
brain:
  id: REPO_NAME
  role: research-node
  version: 1.0
  status: active

links:
  core: https://github.com/pewpi-infinity/mongoose.os
  treasury: https://github.com/pewpi-infinity/infinity-treasury

io:
  input: input/
  output: output/

sync:
  pulls_from: core
  pushes_to: treasury

notes:
  description: >
    Distributed Infinity Brain node.
YAML

sed -i "s/REPO_NAME/$REPO_NAME/g" brain.yaml

git add brain.yaml
git commit -m "Add brain contract (brain.yaml)" || true

echo "[✓] brain.yaml injected"

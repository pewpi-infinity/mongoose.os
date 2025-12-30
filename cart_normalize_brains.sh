#!/data/data/com.termux/files/usr/bin/bash
set -e

ORG="pewpi-infinity"
WORKDIR="$HOME/infinity-brains"

mkdir -p "$WORKDIR"
cd "$WORKDIR"

echo "[∞] Normalizing Infinity Brain repos"

gh repo list "$ORG" --limit 500 --json name \
  --jq '.[].name' | grep '^infinity-brain-' | while read -r REPO; do

  echo
  echo "[→] Processing $REPO"

  if [ ! -d "$REPO" ]; then
    git clone "https://github.com/$ORG/$REPO.git"
  fi

  cd "$REPO"

  if [ -f brain.yaml ]; then
    echo "[✓] brain.yaml already present"
  else
    echo "[∞] Injecting brain.yaml"

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

    sed -i "s/REPO_NAME/$REPO/g" brain.yaml

    git add brain.yaml
    git commit -m "Add brain contract (brain.yaml)"
    git push origin main
  fi

  cd ..
done

echo
echo "[✓] Brain normalization complete"

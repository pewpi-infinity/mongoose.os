#!/usr/bin/env python3
import json, subprocess, os, sys, re

CENSUS = "GLOBAL_REPO_CENSUS.json"

if not os.path.exists(CENSUS):
    print("[∞] GLOBAL_REPO_CENSUS.json missing — generating now")
    subprocess.check_call(["bash", "./cart_generate_global_repo_census.sh"])

with open(CENSUS) as f:
    data = json.load(f)

classified = []

for r in data:
    name = r["name"].lower()
    cls = "unknown"

    if name.startswith("infinity-brain-"):
        cls = "brain-node"
    elif name in ("mongoose.os", "infinity-treasury"):
        cls = "core"
    elif any(k in name for k in ("vector", "osprey", "octave")):
        cls = "vector"
    elif any(k in name for k in ("archive", "old", "backup")):
        cls = "archive"
    else:
        cls = "nursery"

    r["class"] = cls
    classified.append(r)

out = "REPO_CLASSIFICATION.json"
with open(out, "w") as f:
    json.dump(classified, f, indent=2)

print(f"[✓] Repo classification written to {out}")

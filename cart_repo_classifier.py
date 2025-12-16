#!/usr/bin/env python3
import json, re, pathlib

data = json.load(open("GLOBAL_REPO_CENSUS.json"))
out = []

for r in data:
    name = r["name"]
    cls = "unknown"

    if name.startswith("infinity-brain-"):
        cls = "brain-node"
    elif name in ("mongoose.os", "infinity-treasury"):
        cls = "core"
    elif any(k in name.lower() for k in ["vector", "osprey", "octave"]):
        cls = "vector"
    elif any(k in name.lower() for k in ["archive", "old", "backup"]):
        cls = "archive"
    else:
        cls = "nursery"

    r["class"] = cls
    out.append(r)

json.dump(out, open("REPO_CLASSIFICATION.json", "w"), indent=2)
print("[✓] Repo classification complete")

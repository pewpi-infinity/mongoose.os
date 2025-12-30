#!/usr/bin/env python3
# VECTOR ASSIMILATOR
# Reads vector outputs, clusters related carts, and writes unified groups

import os, json, hashlib, time
from collections import defaultdict

BASE = os.path.expanduser("~/infinity_storage")
VECTORS = os.path.join(BASE, "vectors")
OUT = os.path.join(BASE, "assimilated")
os.makedirs(OUT, exist_ok=True)

def fingerprint(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

clusters = defaultdict(list)

for root, _, files in os.walk(VECTORS):
    for f in files:
        if not f.endswith(".json"):
            continue
        path = os.path.join(root, f)
        try:
            data = json.load(open(path))
        except Exception:
            continue

        tokens = " ".join(map(str, data.get("tokens", [])))
        key = fingerprint(tokens)
        clusters[key].append({
            "file": path,
            "meta": data.get("meta", {}),
            "timestamp": data.get("timestamp", time.time())
        })

index = {
    "generated": time.time(),
    "cluster_count": len(clusters),
    "clusters": {}
}

for cid, items in clusters.items():
    out_file = os.path.join(OUT, f"cluster_{cid}.json")
    with open(out_file, "w") as f:
        json.dump({
            "cluster_id": cid,
            "count": len(items),
            "items": items
        }, f, indent=2)
    index["clusters"][cid] = {
        "count": len(items),
        "file": out_file
    }

with open(os.path.join(OUT, "index.json"), "w") as f:
    json.dump(index, f, indent=2)

print(f"[∞] Vector Assimilation complete: {len(clusters)} clusters formed")

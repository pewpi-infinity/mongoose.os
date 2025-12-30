#!/usr/bin/env python3
# VECTOR: generate vector metadata for visualizer

import os, json, time

BASE = os.path.expanduser("~/infinity-repos")
OUT  = os.path.expanduser("~/infinity_storage/vectors")
os.makedirs(OUT, exist_ok=True)

for d in os.listdir(BASE):
    if not d.startswith("infinity-sandbox-"):
        continue
    path = os.path.join(BASE, d)
    vec = {
        "id": d,
        "type": "sandbox",
        "nodes": [],
        "edges": [],
        "time": time.time()
    }
    for f in os.listdir(path):
        if f.startswith("cart_"):
            vec["nodes"].append({"name": f, "kind": "cart"})
    with open(os.path.join(OUT, f"{d}.json"), "w") as o:
        json.dump(vec, o, indent=2)

#!/usr/bin/env python3
# STRUCTURE: unified structural view across all sandboxes

import os, json, time

BASE = os.path.expanduser("~/infinity-repos")
OUT  = os.path.expanduser("~/infinity_storage/structure")
os.makedirs(OUT, exist_ok=True)

index = {
    "generated": time.time(),
    "sandboxes": []
}

for d in sorted(os.listdir(BASE)):
    if not d.startswith("infinity-sandbox-"):
        continue
    path = os.path.join(BASE, d)
    carts = [f for f in os.listdir(path) if f.startswith("cart_")]
    index["sandboxes"].append({
        "id": d,
        "cart_count": len(carts),
        "carts": carts
    })

with open(os.path.join(OUT, "structure_index.json"), "w") as f:
    json.dump(index, f, indent=2)

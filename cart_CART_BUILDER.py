#!/usr/bin/env python3
import os, time, hashlib, json, requests

BASE = os.getcwd()
API  = "http://127.0.0.1:5051/state/write"

src_dirs = ["mongoose.os", "infinity-seeds", "infinity-treasury"]
out = "cart_generated"

os.makedirs(out, exist_ok=True)

def hash_dir(path):
    h = hashlib.sha256()
    for root, _, files in os.walk(path):
        for f in files:
            h.update(f.encode())
    return h.hexdigest()[:12]

for d in src_dirs:
    if not os.path.isdir(d): continue
    sig = hash_dir(d)
    name = f"cart_AUTO_{d}_{sig}.sh"
    path = os.path.join(out, name)

    with open(path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f'echo "[∞] Auto cart from {d} ({sig})"\n')
        f.write(f'echo "Logic detected, executing..." \n')

    os.chmod(path, 0o755)

    requests.post(API, json={
        "type": "cart_build",
        "source": d,
        "cart": name,
        "signature": sig,
        "time": time.time()
    })

    print(f"[✓] Built {name}", flush=True)

#!/usr/bin/env python3
import os
import subprocess
import json
from datetime import datetime

BASE = os.path.expanduser("~/infinity-brains")
OUT  = os.path.expanduser("~/infinity-brains/_brain_index.json")

def run(cmd, cwd=None):
    try:
        return subprocess.check_output(cmd, cwd=cwd, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return None

index = {
    "generated": datetime.utcnow().isoformat() + "Z",
    "base": BASE,
    "brains": []
}

for name in sorted(os.listdir(BASE)):
    path = os.path.join(BASE, name)
    if not os.path.isdir(path):
        continue

    brain = {
        "name": name,
        "path": path,
        "git": False,
        "branch": None,
        "remote": None,
        "dirty": False,
        "status": "unknown"
    }

    if os.path.isdir(os.path.join(path, ".git")):
        brain["git"] = True
        branch = run(["git", "branch", "--show-current"], cwd=path)
        if not branch:
            run(["git", "checkout", "-B", "main"], cwd=path)
            branch = "main"

        brain["branch"] = branch
        brain["remote"] = run(["git", "remote", "get-url", "origin"], cwd=path)

        status = run(["git", "status", "--porcelain"], cwd=path)
        brain["dirty"] = bool(status)

        if brain["dirty"]:
            run(["git", "add", "-A"], cwd=path)
            run(["git", "commit", "-m", "Repo Doctor auto-clean"], cwd=path)

        brain["status"] = "healthy"

    else:
        brain["status"] = "not-a-repo"

    index["brains"].append(brain)

with open(OUT, "w") as f:
    json.dump(index, f, indent=2)

print(f"[∞] Repo Doctor complete")
print(f"[∞] Index written to {OUT}")

#!/usr/bin/env python3
import os
import subprocess
import re
import time
from datetime import datetime

REPO = os.path.expanduser("~/mongoose.os")

print("\n" + "="*70)
print("        ∞ Infinity OS — Master Orchestrator Loaded")
print("="*70 + "\n")

os.chdir(REPO)

# Categorize carts based on filename
scrapers = []
writers = []
tokenizers = []
analysis = []
other = []

for f in os.listdir(REPO):
    if re.match(r"cart\d+.*\.py", f):
        name = f.lower()
        if "scrape" in name or "source" in name:
            scrapers.append(f)
        elif "writer" in name or "research" in name:
            writers.append(f)
        elif "token" in name:
            tokenizers.append(f)
        elif "analy" in name or "calc" in name:
            analysis.append(f)
        else:
            other.append(f)

def run_cart(cart):
    print(f"[💜] Running {cart}…")
    try:
        subprocess.run(["python3", cart], check=True)
    except Exception as e:
        print(f"[⚠️] Error in {cart}: {e}")

print("[💙] Running SCRAPERS…")
for c in scrapers:
    run_cart(c)

print("[💚] Running ANALYSIS modules…")
for c in analysis:
    run_cart(c)

print("[💛] Running WRITERS…")
for c in writers:
    run_cart(c)

print("[💗] Running TOKEN engines…")
for c in tokenizers:
    run_cart(c)

print("[🤍] Running OTHER modules…")
for c in other:
    run_cart(c)

print("\n[💜] Staging and pushing outputs…\n")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", f"∞ Orchestrator run – {datetime.now()}"])
subprocess.run(["git", "push", "origin", "main"])

print("\n" + "="*70)
print("            ∞ Infinity Orchestrator Complete")
print("="*70 + "\n")

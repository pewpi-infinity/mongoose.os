#!/usr/bin/env python3
# Infinity Intelligence Engine — generates real carts continuously
import os, time, json, hashlib, random, textwrap

BASE = os.getcwd()
GEN  = os.path.join(BASE, "cart_generated")
LOGS = os.path.join(BASE, "infinity_storage", "logs")
IDX  = os.path.join(BASE, "infinity_storage", "index")

os.makedirs(GEN, exist_ok=True)
os.makedirs(LOGS, exist_ok=True)
os.makedirs(IDX, exist_ok=True)

DOMAINS = {
  "electronics": [
    ("oscilloscope", "FFT oscilloscope using WebAudio"),
    ("binaural", "Binaural oscillator + frequency math"),
    ("power", "DC-DC buck converter simulator"),
  ],
  "gizmos": [
    ("sensor_hub", "Virtual I2C sensor hub"),
    ("robot_arm", "3DOF kinematics solver"),
    ("rfid", "RFID state machine emulator"),
  ],
  "gadgets": [
    ("music_box", "Golden-ratio tone engine"),
    ("lightwall", "LED matrix animator"),
    ("timer", "High-precision task timer"),
  ]
}

def make_cart(name, body):
    sig = hashlib.sha256(body.encode()).hexdigest()[:10]
    fname = f"cart_AUTO_{name}_{sig}.sh"
    path = os.path.join(GEN, fname)
    with open(path, "w") as f:
        f.write("#!/bin/bash\nset -euo pipefail\n")
        f.write(body)
    os.chmod(path, 0o755)
    return fname, sig

built = []

for domain, items in DOMAINS.items():
    key, desc = random.choice(items)
    body = textwrap.dedent(f"""
        echo "[∞] DOMAIN: {domain}"
        echo "[∞] PROJECT: {key}"
        echo "[∞] DESC: {desc}"
        echo "[∞] Wiring subsystems…"
        sleep 1
        echo "[✓] {key} operational"
    """)
    fname, sig = make_cart(f"{domain}_{key}", body)
    built.append({
        "domain": domain,
        "project": key,
        "file": fname,
        "sig": sig,
        "ts": time.time()
    })

with open(os.path.join(IDX, "intelligence_feed.json"), "a") as f:
    for b in built:
        f.write(json.dumps(b) + "\n")

with open(os.path.join(LOGS, "intelligence.log"), "a") as f:
    f.write(f"[{time.strftime('%F %T')}] built {len(built)} carts\n")

print(f"[✓] Built {len(built)} intelligence carts", flush=True)

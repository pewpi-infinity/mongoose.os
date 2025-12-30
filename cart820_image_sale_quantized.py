#!/usr/bin/env python3
import os, json, time, uuid
from PIL import Image

BASE = "site"
CAPSULES = f"{BASE}/capsules"
FEED = f"{BASE}/feed"
LEDGER = f"{BASE}/ledger"
ASSETS = f"{BASE}/assets"

os.makedirs(CAPSULES, exist_ok=True)
os.makedirs(FEED, exist_ok=True)
os.makedirs(LEDGER, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)

def quantize_image(src, colors=6):
    img = Image.open(src).convert("RGB")
    q = img.quantize(colors=colors, method=Image.MEDIANCUT)
    out = f"{ASSETS}/quant_{uuid.uuid4().hex[:8]}.png"
    q.convert("RGB").save(out, "PNG")
    return out

def create_sale(image_path):
    sale_id = f"SALE-{int(time.time())}-{uuid.uuid4().hex[:6]}"
    quant_img = quantize_image(image_path)

    capsule = {
        "id": sale_id,
        "type": "image_sale",
        "created": time.time(),
        "image_original": image_path,
        "image_quantized": quant_img,
        "price_usd": 9.99,
        "price_infinity": 0.0006,
        "status": "listed"
    }

    feed_tile = {
        "id": sale_id,
        "tile_type": "image-sale",
        "image": quant_img,
        "headline": "Quantized Image Drop",
        "cta": "Buy Capsule",
        "timestamp": time.time()
    }

    ledger_entry = {
        "tx": sale_id,
        "asset": quant_img,
        "category": "image_sale",
        "value_usd": 9.99,
        "value_inf": 0.0006,
        "state": "available"
    }

    with open(f"{CAPSULES}/{sale_id}.json", "w") as f:
        json.dump(capsule, f, indent=2)

    with open(f"{FEED}/{sale_id}.json", "w") as f:
        json.dump(feed_tile, f, indent=2)

    ledger_path = f"{LEDGER}/WORLD_TOKEN_LEDGER.json"
    ledger = []
    if os.path.exists(ledger_path):
        ledger = json.load(open(ledger_path))

    ledger.append(ledger_entry)
    json.dump(ledger, open(ledger_path, "w"), indent=2)

    print(f"[✓] Image sale created: {sale_id}")
    print(f"    Quantized image: {quant_img}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 cart820_image_sale_quantized.py <image.png>")
        sys.exit(1)
    create_sale(sys.argv[1])

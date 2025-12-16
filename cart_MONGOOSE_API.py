#!/usr/bin/env python3
import os, json, time
from flask import Flask, request, jsonify

BASE = os.getcwd()
STATE = os.path.join(BASE, "infinity_storage", "state")
LOGS  = os.path.join(BASE, "infinity_storage", "logs")
os.makedirs(STATE, exist_ok=True)
os.makedirs(LOGS, exist_ok=True)

app = Flask(__name__)

def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(os.path.join(LOGS, "mongoose_api.log"), "a") as f:
        f.write(line + "\n")

@app.route("/state/read", methods=["GET"])
def read_state():
    return jsonify({
        "repos": os.listdir(STATE),
        "time": time.time()
    })

@app.route("/state/write", methods=["POST"])
def write_state():
    data = request.json or {}
    name = data.get("name", f"state_{int(time.time())}.json")
    path = os.path.join(STATE, name)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    log(f"STATE WRITE → {name}")
    return jsonify({"ok": True, "file": name})

@app.route("/signal", methods=["POST"])
def signal():
    data = request.json or {}
    log(f"SIGNAL {data}")
    return jsonify({"ok": True})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "alive", "time": time.time()})

if __name__ == "__main__":
    log("mongoose.os API online @ http://127.0.0.1:5051")
    app.run(host="127.0.0.1", port=5051)

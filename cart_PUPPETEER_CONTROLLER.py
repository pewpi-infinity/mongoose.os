#!/usr/bin/env python3
# OCTOPUS PUPPETEER: central mode dispatcher

from flask import Flask, request, jsonify
import time, json, os

app = Flask(__name__)
STATE = os.path.expanduser("~/infinity_storage/state/mode.json")
os.makedirs(os.path.dirname(STATE), exist_ok=True)

@app.route("/mode", methods=["POST"])
def set_mode():
    mode = request.json.get("mode","engineer")
    with open(STATE,"w") as f:
        json.dump({"mode":mode,"time":time.time()},f)
    return jsonify(ok=True, mode=mode)

@app.route("/state")
def state():
    if os.path.exists(STATE):
        return open(STATE).read()
    return jsonify(mode="engineer")

if __name__ == "__main__":
    app.run(port=6060)

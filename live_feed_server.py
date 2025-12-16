#!/usr/bin/env python3
import os, time
from flask import Flask, Response, send_from_directory

BASE = os.getcwd()
LOG = os.path.join(BASE, "infinity_storage", "logs", "live_feed.log")
os.makedirs(os.path.dirname(LOG), exist_ok=True)

app = Flask(__name__)

def event_stream():
    last_size = 0
    while True:
        if os.path.exists(LOG):
            size = os.path.getsize(LOG)
            if size > last_size:
                with open(LOG, "r") as f:
                    f.seek(last_size)
                    for line in f:
                        yield f"data: {line.strip()}\n\n"
                last_size = size
        time.sleep(0.5)

@app.route("/")
def index():
    return send_from_directory(".", "live_feed.html")

@app.route("/events")
def events():
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    print("[LIVE] Web feed running at http://127.0.0.1:6060")
    app.run(host="127.0.0.1", port=6060, threaded=True)

#!/usr/bin/env python3
import os, time, json, threading, subprocess
from flask import Flask, jsonify, request, Response

BASE = os.getcwd()
LOGD = os.path.join(BASE, "infinity_storage", "logs")
STAT = os.path.join(BASE, "infinity_storage", "state")
REPO_ROOT = os.path.expanduser("~/infinity-repos")
SRC_ROOT  = os.path.expanduser("~/")  # where existing repos live

os.makedirs(LOGD, exist_ok=True)
os.makedirs(STAT, exist_ok=True)
os.makedirs(REPO_ROOT, exist_ok=True)

app = Flask(__name__)
events = []
running = False
current = {"repo": None, "sandbox": None, "count": 0}

def emit(msg):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    events.append(line)
    if len(events) > 500:
        events.pop(0)
    with open(os.path.join(LOGD, "walker.log"), "a") as f:
        f.write(line + "\n")

def list_repos():
    out = []
    for root, dirs, files in os.walk(SRC_ROOT):
        if ".git" in dirs:
            out.append(root)
            dirs[:] = []  # stop deep walk
    return sorted(out, key=lambda p: os.path.getmtime(p))

def sanitize_and_copy(src, dst):
    os.makedirs(dst, exist_ok=True)
    count = 0
    for r, d, files in os.walk(src):
        for f in files:
            if f.startswith("cart_") and f.endswith((".sh", ".py")):
                sp = os.path.join(r, f)
                dp = os.path.join(dst, f)
                with open(sp, "r", errors="ignore") as fi:
                    data = fi.read()
                data = data.replace("\r\n", "\n")
                with open(dp, "w") as fo:
                    fo.write(data)
                try:
                    os.chmod(dp, 0o755)
                except:
                    pass
                count += 1
    return count

def walker():
    global running
    repos = list_repos()
    emit(f"Found {len(repos)} repos")
    for src in repos:
        if not running:
            emit("Paused")
            break
        name = os.path.basename(src)
        sandbox = f"infinity-sandbox-{int(time.time())}"
        dst = os.path.join(REPO_ROOT, sandbox)
        current.update({"repo": name, "sandbox": sandbox, "count": 0})
        emit(f"Entering {name}")
        c = sanitize_and_copy(src, dst)
        current["count"] = c
        emit(f"Sanitized {c} carts → {sandbox}")
        time.sleep(1)
    emit("Walker idle")
    running = False

@app.route("/start", methods=["POST"])
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=walker, daemon=True).start()
        emit("Walker started")
    return jsonify(ok=True)

@app.route("/pause", methods=["POST"])
def pause():
    global running
    running = False
    emit("Pause requested")
    return jsonify(ok=True)

@app.route("/throw", methods=["POST"])
def throw():
    # quick visible action
    emit("Cart throw requested")
    return jsonify(ok=True)

@app.route("/state")
def state():
    return jsonify(running=running, current=current)

@app.route("/events")
def stream():
    def gen():
        last = 0
        while True:
            if last < len(events):
                yield f"data: {events[last]}\n\n"
                last += 1
            time.sleep(0.3)
    return Response(gen(), mimetype="text/event-stream")

@app.route("/")
def page():
    return open("walker_live.html").read()

if __name__ == "__main__":
    emit("Repo Walker ONLINE @ http://127.0.0.1:7070")
    app.run(host="127.0.0.1", port=7070, threaded=True)

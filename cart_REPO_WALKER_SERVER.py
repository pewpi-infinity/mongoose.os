#!/usr/bin/env python3
import os, time, threading
from flask import Flask, Response, jsonify

BASE = os.getcwd()
REPO_ROOT = os.path.expanduser("~/infinity-repos")
SRC_ROOT  = os.path.expanduser("~/")
LOG = os.path.join(BASE, "infinity_storage/logs/walker.log")

os.makedirs(os.path.dirname(LOG), exist_ok=True)
os.makedirs(REPO_ROOT, exist_ok=True)

app = Flask(__name__)
events = []
running = False

def emit(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    events.append(line)
    if len(events) > 500:
        events.pop(0)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def list_repos():
    out = []
    for r, d, f in os.walk(SRC_ROOT):
        if ".git" in d:
            out.append(r)
            d[:] = []
    return sorted(out, key=lambda p: os.path.getmtime(p))

def sanitize(src, dst):
    os.makedirs(dst, exist_ok=True)
    c = 0
    for r, d, f in os.walk(src):
        for x in f:
            if x.startswith("cart_") and x.endswith((".sh",".py")):
                with open(os.path.join(r,x), errors="ignore") as fi:
                    data = fi.read()
                with open(os.path.join(dst,x),"w") as fo:
                    fo.write(data)
                os.chmod(os.path.join(dst,x),0o755)
                c += 1
    return c

def walker():
    global running
    for src in list_repos():
        if not running: break
        name = os.path.basename(src)
        sandbox = f"infinity-sandbox-{int(time.time())}"
        dst = os.path.join(REPO_ROOT, sandbox)
        emit(f"Entering {name}")
        c = sanitize(src, dst)
        emit(f"Sanitized {c} carts → {sandbox}")
        time.sleep(0.5)
    running = False
    emit("Walker idle")

@app.route("/start", methods=["POST"])
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=walker, daemon=True).start()
        emit("Walker started")
    return jsonify(ok=True)

@app.route("/events")
def events_stream():
    def gen():
        i = 0
        while True:
            if i < len(events):
                yield f"data: {events[i]}\n\n"
                i += 1
            time.sleep(0.25)
    return Response(gen(), mimetype="text/event-stream")

@app.route("/")
def page():
    return """
<!doctype html><body style="background:#05080f;color:#8ff;font-family:monospace">
<button onclick="fetch('/start',{method:'POST'})">▶ START</button>
<pre id=p></pre>
<script>
const p=document.getElementById('p');
new EventSource('/events').onmessage=e=>{p.textContent+=e.data+"\\n";p.scrollTop=1e9}
</script>
<footer><hr><p>Powered by Infinity</p><p><a href="mailto:marvaseater@gmail.com">marvaseater@gmail.com</a></p><p>808-342-9975</p><p>The Lending Giant</p></footer>
</body>
"""

if __name__ == "__main__":
    emit("Repo Walker ONLINE @ 7070")
    app.run(port=7070)

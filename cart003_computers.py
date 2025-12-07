# cart003_computers.py
"""
Cart 003: Computers Module
Compute specs, logic gates, memory maps, simple FSMs, and instruction simulations.

Features:
- CPU spec generator (cores, GHz, IPC, throughput estimate)
- Logic gates (AND/OR/XOR/NAND/NOR), truth tables, boolean simplify (basic)
- Memory map allocator (blocks, free/used), hex view
- Finite State Machine (FSM) runner with transitions and logs
- Tiny instruction set simulator (LOAD/ADD/STORE/JMP)
- Artifact export and audit logs
"""

import sys, os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(ROOT, "logs")
OUT_DIR = os.path.join(ROOT, "artifacts")
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
AUDIT = os.path.join(LOGS_DIR, "computers_audit.jsonl")

def audit(entry):
    entry = dict(entry)
    entry["t"] = __import__("time").strftime("%Y-%m-%dT%H:%M:%S", __import__("time").gmtime())
    with open(AUDIT, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

# ---------- CPU ----------
def cpu_spec(cores: int, ghz: float, ipc: float = 1.5) -> dict:
    throughput = cores * ghz * ipc  # rough ops/sec in billions
    return {"cores": cores, "ghz": ghz, "ipc": ipc, "throughput_bops": throughput}

# ---------- Logic ----------
def gate(a: int, b: int, kind: str) -> int:
    if kind == "AND": return a & b
    if kind == "OR": return a | b
    if kind == "XOR": return a ^ b
    if kind == "NAND": return int(not (a & b))
    if kind == "NOR": return int(not (a | b))
    raise ValueError("unknown gate")

def truth_table(kind: str) -> dict:
    rows = []
    for a in (0,1):
        for b in (0,1):
            rows.append({"a": a, "b": b, "out": gate(a,b,kind)})
    return {"gate": kind, "rows": rows}

# very basic boolean simplify: (A AND A) -> A, (A OR A) -> A
def simplify(expr: str) -> str:
    return expr.replace("AND A AND A", "A").replace("OR A OR A", "A")

# ---------- Memory ----------
def memory_map(size_mb: int, block_kb: int = 64) -> dict:
    blocks = (size_mb * 1024) // block_kb
    return {"size_mb": size_mb, "block_kb": block_kb, "blocks": [{"index": i, "state": "free"} for i in range(blocks)]}

def allocate(mem: dict, count: int) -> dict:
    allocated = 0
    for b in mem["blocks"]:
        if b["state"] == "free":
            b["state"] = "used"
            allocated += 1
            if allocated >= count: break
    return {"allocated": allocated}

# ---------- FSM ----------
def run_fsm(states, transitions, start, steps=10) -> dict:
    cur = start
    path = [cur]
    for _ in range(steps):
        nexts = transitions.get(cur, [])
        if not nexts: break
        cur = nexts[0]
        path.append(cur)
    return {"path": path}

# ---------- ISA ----------
def simulate(program):
    """
    Tiny ISA:
    - LOAD R, value
    - ADD R, value
    - STORE R, addr
    - JMP addr
    """
    regs = {"R": 0}
    mem = {}
    ip = 0
    steps = []
    while 0 <= ip < len(program):
        op = program[ip]
        steps.append({"ip": ip, "op": op})
        t = op["op"]
        if t == "LOAD":
            regs[op["reg"]] = op["value"]
            ip += 1
        elif t == "ADD":
            regs[op["reg"]] += op["value"]
            ip += 1
        elif t == "STORE":
            mem[op["addr"]] = regs[op["reg"]]
            ip += 1
        elif t == "JMP":
            ip = op["addr"]
        else:
            break
    return {"regs": regs, "mem": mem, "steps": steps}

def save_artifact(name, obj):
    path = os.path.join(OUT_DIR, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    return path

def main():
    args = sys.argv[1:]
    if not args:
        spec = cpu_spec(8, 3.2, ipc=1.8)
        tt = truth_table("XOR")
        mem = memory_map(256)
        alloc = allocate(mem, 10)
        fsm = run_fsm(states=["A","B","C"], transitions={"A":["B"], "B":["C"], "C":[]}, start="A", steps=5)
        prog = [
            {"op":"LOAD","reg":"R","value":5},
            {"op":"ADD","reg":"R","value":7},
            {"op":"STORE","reg":"R","addr":100}
        ]
        sim = simulate(prog)
        bundle = {"cpu": spec, "truth": tt, "memory": {"map": mem, "alloc": alloc}, "fsm": fsm, "isa": sim}
        audit({"action": "bundle"})
        path = save_artifact("computers_bundle", bundle)
        print(json.dumps(bundle, indent=2)); print(f"Saved: {path}")
        return
    cmd = args[0]
    audit({"action": "cli", "cmd": cmd})
    if cmd == "cpu":
        cores = int(args[1]); ghz = float(args[2]); ipc = float(args[3]) if len(args)>3 else 1.5
        res = cpu_spec(cores, ghz, ipc); print(json.dumps(res, indent=2))
    elif cmd == "truth":
        kind = args[1]; print(json.dumps(truth_table(kind), indent=2))
    elif cmd == "mem":
        size = int(args[1]); mm = memory_map(size); print(json.dumps(mm, indent=2))
    elif cmd == "isa":
        program = [
            {"op":"LOAD","reg":"R","value":10},
            {"op":"ADD","reg":"R","value":22},
            {"op":"STORE","reg":"R","addr":64}
        ]
        print(json.dumps(simulate(program), indent=2))
    else:
        print("Unknown. Try: cpu | truth | mem | isa")

if __name__ == "__main__":
    main()
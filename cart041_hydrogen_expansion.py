# cart041_hydrogen_shell.py
"""
Cart 041: Hydrogen Shell
A safe, abstract shell that stores coded “binary bricks” and attaches power accounting:
- Shell registry
- Brick attachment (from cart040)
- Power ledger (computational hydrogen kWh accounting)
- Artifacts + audit logs
"""

import sys, os, json, time
from typing import Dict, List

ROOT=os.path.dirname(os.path.abspath(__file__))
LOGS=os.path.join(ROOT,"logs"); os.makedirs(LOGS,exist_ok=True)
ART=os.path.join(ROOT,"artifacts"); os.makedirs(ART,exist_ok=True)
DATA=os.path.join(ROOT,"data"); os.makedirs(DATA,exist_ok=True)

AUDIT=os.path.join(LOGS,"hydrogen_shell_audit.jsonl")
REG=os.path.join(DATA,"hydrogen_shell_store.json")

DEFAULT={"shells":[],"ledger":[]}

def now(): return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
def audit(e: Dict): e=dict(e); e["t"]=now(); 
with open(AUDIT,"a",encoding="utf-8") as f: f.write(json.dumps(e)+"\n")

def load()->Dict:
    if not os.path.exists(REG): return DEFAULT.copy()
    try:
        with open(REG,"r",encoding="utf-8") as f: return json.load(f)
    except: return DEFAULT.copy()

def save(obj: Dict):
    with open(REG,"w",encoding="utf-8") as f: json.dump(obj,f,indent=2)

def save_artifact(name:str, obj:Dict)->str:
    p=os.path.join(ART,f"{name}.json")
    with open(p,"w",encoding="utf-8") as f: json.dump(obj,f,indent=2)
    return p

# ---------- Shell creation ----------
def shell_new(name:str, capacity_kwh:float=1.0)->Dict:
    db=load()
    sh={"name":name,"capacity_kWh":capacity_kwh,"bricks":[],"created":now()}
    db["shells"].append(sh); save(db)
    path=save_artifact(f"hydrogen_shell_{name}", sh)
    audit({"action":"shell.new","name":name,"capacity_kWh":capacity_kwh})
    return {"ok":True,"path":path,"shell":sh}

# ---------- Attach brick ----------
def attach_brick(shell_name:str, brick_id:str, note:str="")->Dict:
    db=load()
    sh=next((s for s in db["shells"] if s["name"]==shell_name),None)
    if not sh: return {"ok":False,"error":"shell not found"}
    sh["bricks"].append({"brick_id":brick_id,"note":note,"t":now()})
    save(db)
    path=save_artifact(f"hydrogen_shell_attach_{shell_name}_{brick_id}", sh)
    audit({"action":"shell.attach","shell":shell_name,"brick_id":brick_id})
    return {"ok":True,"path":path}

# ---------- Power ledger ----------
def ledger_add(shell_name:str, kwh:float, reason:str)->Dict:
    db=load()
    entry={"shell":shell_name,"kWh":kwh,"reason":reason,"t":now()}
    db["ledger"].append(entry); save(db)
    path=save_artifact(f"hydrogen_ledger_{int(time.time())}", entry)
    audit({"action":"ledger.add","shell":shell_name,"kWh":kwh})
    return {"ok":True,"path":path}

# ---------- Health ----------
def health()->Dict:
    db=load()
    out={"shells":len(db["shells"]), "ledger_entries":len(db["ledger"])}
    path=save_artifact("hydrogen_shell_health", out)
    audit({"action":"health","summary":out})
    return {"ok":True,"path":path,"summary":out}

# ---------- CLI ----------
def main():
    a=sys.argv[1:]
    if not a:
        print("Usage: new --name N [--cap kWh] | attach --shell N --brick BID [--note '...'] | ledger --shell N --kWh v --reason '...' | health")
        return
    cmd=a[0]
    if cmd=="new":
        name="Shell-Alpha"; cap=1.0
        for i,x in enumerate(a):
            if x=="--name" and i+1<len(a): name=a[i+1]
            if x=="--cap" and i+1<len(a): cap=float(a[i+1])
        print(json.dumps(shell_new(name,cap), indent=2)); return
    if cmd=="attach":
        sh="Shell-Alpha"; bid=""; note=""
        for i,x in enumerate(a):
            if x=="--shell" and i+1<len(a): sh=a[i+1]
            if x=="--brick" and i+1<len(a): bid=a[i+1]
            if x=="--note" and i+1<len(a): note=a[i+1]
        print(json.dumps(attach_brick(sh,bid,note), indent=2)); return
    if cmd=="ledger":
        sh="Shell-Alpha"; kwh=0.1; reason="accounting"
        for i,x in enumerate(a):
            if x=="--shell" and i+1<len(a): sh=a[i+1]
            if x=="--kWh" and i+1<len(a): kwh=float(a[i+1])
            if x=="--reason" and i+1<len(a): reason=a[i+1]
        print(json.dumps(ledger_add(sh,kwh,reason), indent=2)); return
    if cmd=="health":
        print(json.dumps(health(), indent=2)); return
    print(json.dumps({"error":"unknown command"}, indent=2))

if __name__=="__main__": main()
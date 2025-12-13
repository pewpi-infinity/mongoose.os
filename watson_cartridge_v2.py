import networkx as nx, requests, re, random, time
from collections import defaultdict, Counter

# ANSI COLORS — MILITARY GRADE
G, B, P, R, Y, C, W = '\033[92m', '\033[94m', '\033[95m', '\033[91m', '\033[93m', '\033[96m', '\033[97m'
END = '\033[0m'
BOLD = '\033[1m'

class WatsonCartridge:
    def __init__(self):
        self.token_graph = nx.Graph()
        self.knowledge_graph = nx.DiGraph()
        self.attentive = Counter()
        self.mission = "crypto warfare • quantum tokens • OPSEC"

    def ingest(self, text, src="intel", style=None):
        t = re.findall(r'\w+', text.lower())
        if len(t)<5: return
        for a,b in zip(t, t[1:]):
            if self.token_graph.has_edge(a,b):
                self.token_graph[a][b]['w'] += 1
            else:
                self.token_graph.add_edge(a,b,w=1)
        # quick entities
        ents = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', text)
        for e in set(ents):
            self.knowledge_graph.add_edge(e, src, rel="FROM")
            self.attentive[e] += 3

    def swim(self, start="bitcoin"):
        if start not in self.token_graph: return [start]
        path = [start]; cur = start
        for _ in range(30):
            nei = list(self.token_graph.neighbors(cur))
            if not nei: break
            cur = random.choices(nei, [self.token_graph[cur][n]['w'] for n in nei])[0]
            path.append(cur)
        return path

wc = WatsonCartridge()

print(f"{R}MONGOOSE.OS WAR MACHINE ONLINE{END}")
print(f"{P}MISSION LOCKED → {wc.mission}{END}\n")

cycle = 0
while True:
    cycle += 1
    print(f"{C}CYCLE {cycle:04d} | {wc.mission}{END}", end="")

    # 1. Wikipedia strike
    try:
        r = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary", timeout=8).json()
        wc.ingest(r.get("extract",""), f"{G}WIKI:{r['title']}{END}")
        print(f"  {G}WIKI{END}", end="")
    except: print(f"  {Y}WIKI OFFLINE{END}", end="")

    # 2. CoinGecko strike
    try:
        coins = requests.get("https://api.coingecko.com/api/v3/coins/list", timeout=8).json()
        wc.ingest(" ".join(f"{c['id']} {c['symbol'].upper()}" for c in coins), f"{R}COINGECKO{END}")
        print(f"  {R}COINS{END}", end="")
    except: print(f"  {Y}COINS OFFLINE{END}", end="")

    # 3. Targeted military hit
    hits = ["OPSEC", "zero knowledge proof", "SIGINT", "blockchain C2", "quantum key distribution"]
    try:
        term = random.choice(hits)
        r = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={term}&format=json&srlimit=1", timeout=6).json()
        wc.ingest(r['query']['search'][0]['snippet'], f"{B}TARGET:{term}{END}")
        print(f"  {B}{term}{END}", end="")
    except: pass

    # Live sharp swim every cycle (no more waiting)
    swim_path = wc.swim(random.choice(["bitcoin","quantum","opsec","mongoose","satoshi"]))
    print(f"  {P}SWIM → {', '.join(swim_path[:8])}{END}")

    time.sleep(4)  # rapid fire, no stutter

import networkx as nx, requests, re, random, logging, time, json
from collections import defaultdict, Counter
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class WatsonCartridge:
    def __init__(self):
        # Green: Fluency & Style Graph
        self.token_graph = nx.Graph()
        # Green: Semantic Knowledge Graph (reasoning)
        self.knowledge_graph = nx.DiGraph()
        self.style_profiles = defaultdict(dict)
        self.seen_urls = set()
        # Blue: Mission Control
        self.mission_focus = "crypto + military intelligence"
        # Purple: Attentive Memory (what matters right now)
        self.attentive_memory = Counter()

    def read_and_learn(self, text, source="unknown", style_label=None):
        tokens = re.findall(r'\w+', text.lower())
        if len(tokens) < 5: return

        # Green: Build fluency graph
        for i in range(1, len(tokens)):
            a, b = tokens[i-1], tokens[i]
            if self.token_graph.has_edge(a, b):
                self.token_graph[a][b]['weight'] += 1
            else:
                self.token_graph.add_edge(a, b, weight=1)

        # Green: Extract entities → knowledge graph
        entities = re.findall(r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)*\b', text)
        for entity in set(entities):
            self.knowledge_graph.add_node(entity, type="Entity")
            self.knowledge_graph.add_edge(entity, source, relationship="MENTIONED_IN")
            self.attentive_memory[entity] += 2

        # Special crypto handling
        if "coingecko" in source.lower():
            parts = text.split()
            for i in range(0, len(parts)-1, 2):
                coin_id, symbol = parts[i], parts[i+1].upper()
                self.knowledge_graph.add_node(symbol, type="CryptoCoin")
                self.knowledge_graph.add_edge(symbol, "Cryptocurrency", relationship="IS_A")
                self.knowledge_graph.add_edge(symbol, coin_id, relationship="HAS_ID")
                self.attentive_memory[symbol] += 5

        # Style learning
        if style_label:
            phrases = [' '.join(tokens[i:i+3]) for i in range(len(tokens)-2)]
            self.style_profiles[style_label]['phrases'] = self.style_profiles[style_label].get('phrases', Counter()) + Counter(phrases)

        logger.info(f"INGESTED ← {source[:50]}… ({len(tokens)} tokens) | Focus: {self.mission_focus}")

    def swim(self, token="bitcoin", steps=25):
        if token not in self.token_graph:
            self.token_graph.add_node(token)
        school = [token]; cur = token
        for _ in range(steps):
            nei = list(self.token_graph.neighbors(cur))
            if not nei: break
            cur = random.choices(nei, weights=[self.token_graph[cur][n]['weight'] for n in nei])[0]
            school.append(cur)
        return school

    def deduce(self, a, b):
        if not self.knowledge_graph.has_node(a) or not self.knowledge_graph.has_node(b):
            return f"Need more intel on {a} or {b}"
        try:
            path = nx.shortest_path(self.knowledge_graph, a, b)
            return f"Path: {' → '.join(path)}"
        except:
            return "No known connection"

    def set_mission(self, focus):
        self.mission_focus = focus
        logger.info(f"MISSION UPDATED → {focus}")

# ——————————————————————— ETERNAL LOOP ———————————————————————
def eternal_mongoose():
    wc = WatsonCartridge()
    wc.set_mission("crypto warfare · military strategy · quantum tokens")

    cycle = 0
    while True:
        cycle += 1
        logger.info(f"MONGOOSE.OS CYCLE {cycle} | MISSION: {wc.mission_focus}")

        # 1. Random Wikipedia (structured)
        try:
            r = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary", timeout=12)
            data = r.json()
            wc.read_and_learn(data.get("extract",""), f"Wiki:{data.get('title','?')}", "knowledge")
        except: pass

        # 2. Fresh CoinGecko feed
        try:
            coins = requests.get("https://api.coingecko.com/api/v3/coins/list", timeout=12).json()
            cointext = " ".join(f"{c['id']} {c['symbol'].upper()}" for c in coins)
            wc.read_and_learn(cointext, "CoinGecko_LIVE", "crypto")
        except: pass

        # 3. Targeted military/crypto search when memory is hungry
        if cycle % 4 == 0:
            term = random.choice(["OPSEC", "cryptocurrency regulation", "zero knowledge proof", "SIGINT", "blockchain warfare"])
            try:
                r = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={term}&format=json&srlimit=1")
                snippet = r.json()['query']['search'][0]['snippet']
                wc.read_and_learn(snippet, f"Targeted:{term}", "military_crypto")
            except: pass

        # Live demo every 6 cycles
        if cycle % 6 == 0:
            print(f"\nCYCLE {cycle} | SWIM → BTC:", wc.swim("bitcoin", 35))
            print(f"Deduction → BTC → Cryptocurrency:", wc.deduce("BTC", "Cryptocurrency"))
            print(f"Top attention:", wc.attentive_memory.most_common(5))

        time.sleep(6)  # Fast evolution

# ——————————————————————— LAUNCH ———————————————————————
if __name__ == "__main__":
    print("\nWATSON CARTRIDGE ∞ | MONGOOSE.OS V2 — ETERNAL WAR MODE\n")
    eternal_mongoose()

import numpy as np
import networkx as nx
from collections import defaultdict, Counter
import re
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class WatsonCartridge:
    def __init__(self):
        self.memory = {}
        self.waste_bin = []
        self.style_profiles = defaultdict(dict)
        self.token_graph = nx.Graph()
        self.vector_space = defaultdict(np.array)
        self.vocab = set()

    def read_and_learn(self, text, source_link=None, style_label=None, mode='light_speed'):
        logger.info(f"Starting read in {mode}.os mode: Processing text from {source_link or 'input'}...")
        tokens = re.findall(r'\w+', text.lower())
        if len(tokens) < 5:
            self.waste_bin.append(text)
            logger.info("Junk → waste bin.")
            return

        page_key = f"page_{len(self.memory)+1}"
        self.memory[page_key] = {
            'content': text, 'tags': self._generate_tags(tokens),
            'link': source_link or 'internal', 'tokens': tokens
        }

        # Vector space (simple bag-of-words)
        self.vocab.update(tokens)
        vocab_list = list(self.vocab)
        vec = np.zeros(len(vocab_list))
        for i, w in enumerate(vocab_list):
            vec[i] = tokens.count(w)
        self.vector_space[page_key] = vec

        # Token graph (quantum swimming pool)
        for i in range(1, len(tokens)):
            self.token_graph.add_edge(tokens[i-1], tokens[i], weight=1)

        # Style learning
        if style_label:
            phrases = [' '.join(tokens[i:i+3]) for i in range(len(tokens)-2)]
            emotions = self._infer_emotions(text)
            self.style_profiles[style_label]['phrases'] = self.style_profiles[style_label].get('phrases', []) + phrases
            self.style_profiles[style_label]['emotions'] = self.style_profiles[style_label].get('emotions', []) + emotions

        if mode == 'tortoise':
            logger.info("Tortoise mode activated — deep linking complete.")

        logger.info(f"Stored {page_key} — cartridge is now smarter.")

    def _generate_tags(self, tokens): return [w for w, c in Counter(tokens).most_common(3)]
    def _infer_emotions(self, text): return ['stern','authoritative'] if any(w in text.lower() for w in ['order','execute','government']) else ['neutral']

    def swim_tokens(self, start_token, steps=15):
        if start_token not in self.token_graph: return []
        school = [start_token]
        current = start_token
        for _ in range(steps):
            neighbors = list(self.token_graph.neighbors(current))
            if neighbors: current = random.choice(neighbors)
            school.append(current)
        return school

    def generate_in_style(self, prompt, style_label):
        if style_label not in self.style_profiles: return "Style not trained yet."
        phrases = random.sample(self.style_profiles[style_label].get('phrases', ['STAND BY']), 3)
        return f"[CLASSIFIED {style_label.upper()}] {prompt} → {' '.join(phrases)}."

# Quick demo when run directly
if __name__ == "__main__":
    wc = WatsonCartridge()
    wc.read_and_learn("Execute immediate government action with extreme prejudice.", style_label="military", mode="tortoise")
    wc.read_and_learn("Light-speed.os achieves infinite throughput while tortoise.os contemplates the void.", mode="light_speed")
    print("\nSwimming from 'government':", wc.swim_tokens("government"))
    print(wc.generate_in_style("Status report on Operation Black Wave", "military"))

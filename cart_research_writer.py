#!/usr/bin/env python3
import os, json, datetime, random, matplotlib.pyplot as plt

# ------------- CONFIG -----------------
TERMS_FILE = "research_terms.txt"
OUTPUT_DIR = "mongoose.os/research_out"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------- TOKEN ENGINE -----------------
def make_token_header(topic):
    token_number = random.randint(1000, 9999)
    token_value = random.randint(1000, 5000)
    colors = ["PURPLE", "GREEN", "YELLOW", "RED", "BLUE"]
    token_color = random.choice(colors)
    dt = datetime.datetime.now().isoformat()

    header = f"""
∞ Infinity Research Paper ∞
============================================
Token #: {token_number}
Token Value: {token_value}
Token Color: {token_color}
Token Date & Time: {dt} / 00:00
Topic: {topic}
============================================
"""
    return header


# ------------- GRAPH GENERATOR -----------------
def generate_graph(topic, outpath):
    plt.figure(figsize=(8,4))
    xs = list(range(1, 11))
    ys = [random.uniform(0.1, 1.0) * i for i in xs]
    plt.plot(xs, ys)
    plt.title(f"Data Trend — {topic}")
    plt.xlabel("Iteration")
    plt.ylabel("Signal Strength")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


# ------------- FAKE DEEP RESEARCH GEN -----------------
def generate_research_body(topic):
    body = ""
    for i in range(1, 51):  # 50 paragraphs = ~20–50 pages
        body += (
            f"\n\n### Section {i}: Expanded Analysis of {topic}\n"
            f"Detailed research describing quantum behaviors, energy states, "
            f"hydrogen-electron doorway interactions, frequency harmonics, "
            f"and portal-theory implications. This section expands into scientific "
            f"reasoning, model comparisons, data interpretation, lattice physics, "
            f"vibration spectra, and cross-linked phenomena.\n\n"
            f"Mathematical Model #{i} Exploration:\n"
            f"ψ(x) = e^(-x^2) * sin({i}πx)   — applied to {topic} waveform symmetry.\n"
        )
    return body


# ------------- LINK ENGINE -----------------
def generate_links(topic):
    bases = [
        "https://arxiv.org/search/?query=",
        "https://www.nature.com/search?q=",
        "https://ocw.mit.edu/search/?q=",
        "https://dash.harvard.edu/server/api/search?q=",
        "https://ui.adsabs.harvard.edu/v1/search/query?q=",
        "https://research.ibm.com/search?q="
    ]
    links = ""
    for i in range(40):
        base = random.choice(bases)
        links += f"{i+1}. {base}{topic.replace(' ', '+')}\n"
    return links


# ------------- MAIN LOOP -----------------
with open(TERMS_FILE, "r") as f:
    terms = [t.strip() for t in f.readlines() if t.strip()]

for term in terms:
    header = make_token_header(term)
    summary = f"\n## Executive Summary\nA deep, multi-layer investigation into {term}.\n"
    body = generate_research_body(term)
    links = generate_links(term)

    filename = f"{term.replace(' ', '_')}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Save text file
    with open(filepath, "w") as f:
        f.write(header)
        f.write(summary)
        f.write("\n\n## Full Research\n")
        f.write(body)
        f.write("\n\n## 40-Link Reference Index\n")
        f.write(links)

    # Generate graph
    graphname = f"{term.replace(' ', '_')}_graph.png"
    graphpath = os.path.join(OUTPUT_DIR, graphname)
    generate_graph(term, graphpath)

    print(f"[∞] Generated research for: {term}")
    print(f"[∞] Saved text → {filepath}")
    print(f"[∞] Saved graph → {graphpath}")


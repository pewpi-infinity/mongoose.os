#!/usr/bin/env python3
import os
import json
import datetime
import random
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# ────────────────────────────────────────────────
# CONFIGURATION
# ────────────────────────────────────────────────
SEARCH_TERMS_FILE = "search_terms_master.txt"
OUTPUT_DIR = "infinity_research_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

COLORS = ["💜 PURPLE", "💚 GREEN", "💛 YELLOW", "❤️ RED", "🩵 BLUE"]

# Headers are critical to avoid immediate 403 Forbidden errors
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

MAX_RESULTS_PER_SOURCE = 10  # 10 research articles at a time per source

# ────────────────────────────────────────────────
# SOURCES (Unique List)
# ────────────────────────────────────────────────
SEARCH_SOURCES = [
    "https://scholar.google.com/scholar?q=",
    "https://www.nature.com/search?q=",
    "https://arxiv.org/search/?query=",
    "https://www.sciencedirect.com/search?q=",
    "https://pubmed.ncbi.nlm.nih.gov/?term=",
    "https://www.researchgate.net/search?q=",
    "https://www.semanticscholar.org/search?q=",
]

# ────────────────────────────────────────────────
# HELPERS
# ────────────────────────────────────────────────
def make_article_token(article_title):
    return {
        "article_number": random.randint(1000, 999999),  # Numbered
        "article_value": random.randint(100, 5000),  # Valued
        "article_color": random.choice(COLORS),  # Color coded
        "generated": datetime.datetime.now().isoformat(),
        "title": article_title
    }

def parse_scholar(soup):
    articles = []
    results = soup.select('#gs_res_ccl_mid .gs_r .gs_ri')[:MAX_RESULTS_PER_SOURCE]
    for res in results:
        title_elem = res.select_one('.gs_rt a')
        title = title_elem.text.strip() if title_elem else None
        url = title_elem['href'] if title_elem else None
        authors = ', '.join([a.text for a in res.select('.gs_a a')])
        abstract = res.select_one('.gs_rs').text.strip() if res.select_one('.gs_rs') else None
        pdf_elem = res.select_one('a[href*=".pdf"]')
        pdf_url = pdf_elem['href'] if pdf_elem else None
        if title:
            articles.append({
                "title": title,
                "url": url,
                "authors": authors,
                "abstract": abstract,
                "pdf_url": pdf_url
            })
    return articles

def parse_arxiv(soup):
    articles = []
    results = soup.select('li.arxiv-result')[:MAX_RESULTS_PER_SOURCE]
    for res in results:
        title = res.select_one('p.title').text.strip() if res.select_one('p.title') else None
        url = res.select_one('p.list-title a')['href'] if res.select_one('p.list-title a') else None
        authors = ', '.join([a.text.strip() for a in res.select('.authors a')])
        abstract = res.select_one('p.abstract').text.strip() if res.select_one('p.abstract') else None
        pdf_elem = res.select_one('a[accesskey="f"]')
        pdf_url = pdf_elem['href'] if pdf_elem else None
        if title:
            articles.append({
                "title": title,
                "url": url,
                "authors": authors,
                "abstract": abstract,
                "pdf_url": pdf_url
            })
    return articles

def parse_pubmed(soup):
    articles = []
    results = soup.select('article.full-docsum')[:MAX_RESULTS_PER_SOURCE]
    for res in results:
        title_elem = res.select_one('.docsum-content a')
        title = title_elem.text.strip() if title_elem else None
        url = 'https://pubmed.ncbi.nlm.nih.gov' + title_elem['href'] if title_elem else None
        authors = res.select_one('.docsum-authors').text.strip() if res.select_one('.docsum-authors') else None
        abstract = res.select_one('.docsum-summary').text.strip() if res.select_one('.docsum-summary') else None
        pdf_url = None  # PubMed typically links to publishers, no direct PDF
        if title:
            articles.append({
                "title": title,
                "url": url,
                "authors": authors,
                "abstract": abstract,
                "pdf_url": pdf_url
            })
    return articles

def parse_sciencedirect(soup):
    articles = []
    results = soup.select('li.ResultListItem')[:MAX_RESULTS_PER_SOURCE]
    for res in results:
        title_elem = res.select_one('.js-article-title-link')
        title = title_elem.text.strip() if title_elem else None
        url = 'https://www.sciencedirect.com' + title_elem['href'] if title_elem else None
        authors = ', '.join([a.text.strip() for a in res.select('ol.Authors li')])
        abstract = res.select_one('p.js-article-abstract').text.strip() if res.select_one('p.js-article-abstract') else None
        pdf_url = res.select_one('a.js-pdf-download')['href'] if res.select_one('a.js-pdf-download') else None
        if title:
            articles.append({
                "title": title,
                "url": url,
                "authors": authors,
                "abstract": abstract,
                "pdf_url": pdf_url
            })
    return articles

def parse_nature(soup):
    articles = []
    results = soup.select('li.app-search-result-item')[:MAX_RESULTS_PER_SOURCE]
    for res in results:
        title_elem = res.select_one('h1 a')
        title = title_elem.text.strip() if title_elem else None
        url = 'https://www.nature.com' + title_elem['href'] if title_elem else None
        authors = ', '.join([a.text.strip() for a in res.select('ul.app-search-result-authors li')])
        abstract = res.select_one('p.app-search-result-snippet').text.strip() if res.select_one('p.app-search-result-snippet') else None
        pdf_url = res.select_one('a[data-track-action="download pdf"]')['href'] if res.select_one('a[data-track-action="download pdf"]') else None
        if title:
            articles.append({
                "title": title,
                "url": url,
                "authors": authors,
                "abstract": abstract,
                "pdf_url": pdf_url
            })
    return articles

def parse_researchgate(soup):
    articles = []
    results = soup.select('div.nova-legacy-v-publication-item')[:MAX_RESULTS_PER_SOURCE]
    for res in results:
        title_elem = res.select_one('h3 a.nova-legacy-e-link')
        title = title_elem.text.strip() if title_elem else None
        url = 'https://www.researchgate.net' + title_elem['href'] if title_elem else None
        authors = ', '.join([a.text.strip() for a in res.select('div.nova-legacy-v-publication-item__person-list li')])
        abstract = res.select_one('div.nova-legacy-v-publication-item__body').text.strip() if res.select_one('div.nova-legacy-v-publication-item__body') else None
        pdf_url = res.select_one('a.nova-legacy-e-button--color-green')['href'] if res.select_one('a.nova-legacy-e-button--color-green') else None  # For full text
        if title:
            articles.append({
                "title": title,
                "url": url,
                "authors": authors,
                "abstract": abstract,
                "pdf_url": pdf_url
            })
    return articles

def parse_semanticscholar(soup):
    articles = []
    results = soup.select('div.search-result')[:MAX_RESULTS_PER_SOURCE]
    for res in results:
        title_elem = res.select_one('div.search-result-title a')
        title = title_elem.text.strip() if title_elem else None
        url = 'https://www.semanticscholar.org' + title_elem['href'] if title_elem else None
        authors = ', '.join([a.text.strip() for a in res.select('div.author-list a')])
        abstract = res.select_one('div.tldr-abstract-replacement').text.strip() if res.select_one('div.tldr-abstract-replacement') else None
        pdf_url = res.select_one('a[data-selenium-selector="pdf-link"]')['href'] if res.select_one('a[data-selenium-selector="pdf-link"]') else None
        if title:
            articles.append({
                "title": title,
                "url": url,
                "authors": authors,
                "abstract": abstract,
                "pdf_url": pdf_url
            })
    return articles

def fetch_research(query):
    all_articles = []
    
    # Randomize order to reduce pattern detection
    sources = SEARCH_SOURCES.copy()
    random.shuffle(sources)

    print(f"   Searching {len(sources)} repositories for '{query}'...")

    for idx, base in enumerate(sources):
        # Politeness Delay: Random sleep between 3 and 7 seconds to avoid bans
        time.sleep(random.uniform(3, 7))
        
        target_url = base + quote_plus(query)
        domain = base.split('/')[2]
        
        try:
            r = requests.get(target_url, headers=HEADERS, timeout=10)
            
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                
                # Check for CAPTCHA
                page_title = soup.title.text.strip() if soup.title else "No Title Found"
                if "captcha" in page_title.lower() or "robot" in page_title.lower():
                    status = "BLOCKED/CAPTCHA"
                    articles = []
                else:
                    status = "SUCCESS"
                    if "scholar.google.com" in domain:
                        articles = parse_scholar(soup)
                    elif "arxiv.org" in domain:
                        articles = parse_arxiv(soup)
                    elif "pubmed.ncbi.nlm.nih.gov" in domain:
                        articles = parse_pubmed(soup)
                    elif "www.sciencedirect.com" in domain:
                        articles = parse_sciencedirect(soup)
                    elif "www.nature.com" in domain:
                        articles = parse_nature(soup)
                    elif "www.researchgate.net" in domain:
                        articles = parse_researchgate(soup)
                    elif "www.semanticscholar.org" in domain:
                        articles = parse_semanticscholar(soup)
                    else:
                        articles = []
            else:
                status = "FAILED"
                articles = []

            # Add token to each article and collect
            for art_idx, article in enumerate(articles):
                article['source_id'] = idx + 1
                article['engine'] = domain
                article['status'] = status
                article['token'] = make_article_token(article.get('title', ''))
                all_articles.append(article)

        except Exception as e:
            all_articles.append({
                "source_id": idx + 1,
                "url": target_url,
                "error": str(e),
                "status": "ERROR"
            })
            
    return all_articles

# ────────────────────────────────────────────────
# MAIN PROCESSOR
# ────────────────────────────────────────────────
def run_cart():
    if not os.path.exists(SEARCH_TERMS_FILE):
        # Create a dummy file for testing if it doesn't exist (add your 5000 terms here or externally)
        with open(SEARCH_TERMS_FILE, "w") as f:
            f.write("quantum computing\nmachine learning\nCRISPR\nartificial intelligence\nclimate change")
        print(f"Created dummy {SEARCH_TERMS_FILE} with examples. Add your terms and rerun.")

    with open(SEARCH_TERMS_FILE, "r", encoding="utf8") as f:
        terms = [t.strip() for t in f.readlines() if t.strip()]

    print(f"Loaded {len(terms)} terms. Starting infinite research loop (stop with Ctrl+C)...")

    iteration = 0
    while True:
        iteration += 1
        print(f"\n[Iteration {iteration}] Generating query...")

        # Randomly decide: single term (50% chance) or combo (50% chance)
        if random.random() < 0.5:
            query = random.choice(terms)
            print(f"  Single term query: {query}")
        else:
            num_terms = random.randint(2, 4)  # Random combo size
            selected = random.sample(terms, num_terms)
            query = ' '.join(selected)  # Join with spaces (can change to ' AND ' if needed)
            print(f"  Combo query ({num_terms} terms): {query}")
            # Intelligent path: optional - you can add logic here to build based on previous, e.g., track themes

        header = {
            "token_number": random.randint(1000, 999999),
            "token_value": random.randint(100, 5000),
            "token_color": random.choice(COLORS),
            "generated": datetime.datetime.now().isoformat(),
            "topic": query
        }
        articles = fetch_research(query)

        out = {
            "header": header,
            "articles": articles  # Now full articles with tokens
        }

        # Filename safe handling
        safe_query = "".join([c for c in query if c.isalnum() or c in (' ', '_')]).rstrip().replace(' ', '_')
        fname = f"{header['token_number']}_{safe_query}.json"
        path = os.path.join(OUTPUT_DIR, fname)

        with open(path, "w", encoding="utf8") as f:
            json.dump(out, f, indent=2)

        print(f"[∞] Saved → {fname}")

        # Longer delay between full iterations to avoid rate limits during infinite run
        time.sleep(random.uniform(10, 30))

if __name__ == "__main__":
    run_cart()

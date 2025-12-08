#!/usr/bin/env bash
set -e

echo ""
echo "∞ INFINITY MASTER ENGINE – FULL SYSTEM RUN"
echo "-------------------------------------------"
echo "Started at: $(date)"
echo ""

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

MASTER_LOG="$LOG_DIR/infinity_master_$(date '+%Y%m%d_%H%M%S').log"

echo "∞ Logging to $MASTER_LOG"
echo "" | tee -a "$MASTER_LOG"

echo "∞ STEP 1: Running research carts…" | tee -a "$MASTER_LOG"

# Run every cart file that matches cart*.py
for cart in cart*.py; do
    if [[ -f "\$cart" ]]; then
        echo "--------------------------------------------" | tee -a "$MASTER_LOG"
        echo "∞ Running: \$cart" | tee -a "$MASTER_LOG"
        echo "--------------------------------------------" | tee -a "$MASTER_LOG"
        python3 "\$cart" >> "$MASTER_LOG" 2>&1 || echo "⚠ Error in \$cart (continuing)" | tee -a "$MASTER_LOG"
    fi
done


echo "" | tee -a "$MASTER_LOG"
echo "∞ STEP 2: Running Infinity Research Writers…" | tee -a "$MASTER_LOG"

for writer in infinity_research.py infinity_research_fulltext.py infinity_research_txt_only.py cart_write_infinity_research.py cart_research_writer.py; do
    if [[ -f "\$writer" ]]; then
        echo "∞ Writer: \$writer" | tee -a "$MASTER_LOG"
        python3 "\$writer" >> "$MASTER_LOG" 2>&1 || echo "⚠ Error in \$writer" | tee -a "$MASTER_LOG"
    fi
done


echo "" | tee -a "$MASTER_LOG"
echo "∞ STEP 3: Running token engines…" | tee -a "$MASTER_LOG"

for tok in cart019_token_generation.py cart021_token_tiers.py cart900_infinity_research_rig.py cart901_autopush_research_rig.py; do
    if [[ -f "\$tok" ]]; then
        echo "∞ Token Engine: \$tok" | tee -a "$MASTER_LOG"
        python3 "\$tok" >> "$MASTER_LOG" 2>&1 || echo "⚠ Error in \$tok" | tee -a "$MASTER_LOG"
    fi
done


echo "" | tee -a "$MASTER_LOG"
echo "∞ STEP 4: Running scrapers…" | tee -a "$MASTER_LOG"

for scrape in cart_scrape_hydrogen_sources.py cart101_physics_research.py cart102_ai_research.py cart103_energy_research.py cart104_academic_research.py; do
    if [[ -f "\$scrape" ]]; then
        echo "∞ Scraper: \$scrape" | tee -a "$MASTER_LOG"
        python3 "\$scrape" >> "$MASTER_LOG" 2>&1 || echo "⚠ Error in \$scrape" | tee -a "$MASTER_LOG"
    fi
done


echo "" | tee -a "$MASTER_LOG"
echo "∞ STEP 5: Running term generators (153 carts etc.)…" | tee -a "$MASTER_LOG"

for gen in infinity_generate_153_terms.py infinity_make_153_carts.py; do
    if [[ -f "\$gen" ]]; then
        echo "∞ Generator: \$gen" | tee -a "$MASTER_LOG"
        python3 "\$gen" >> "$MASTER_LOG" 2>&1 || echo "⚠ Error in \$gen" | tee -a "$MASTER_LOG"
    fi
done


echo "" | tee -a "$MASTER_LOG"
echo "∞ FINAL STEP: Pushing to GitHub…" | tee -a "$MASTER_LOG"

./commit_gatekeeper.sh | tee -a "$MASTER_LOG"

echo ""
echo "∞ DONE – Infinity Master Engine Complete."
echo "Finished: $(date)"

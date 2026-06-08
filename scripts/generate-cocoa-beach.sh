#!/bin/bash
# Daily Cocoa Beach STR Market Scout generator
# Runs 30 minutes after Mansfield scout
# Requires: claude CLI installed and authenticated

set -euo pipefail

SCOUT_DIR="$HOME/STR-Scouts"
OUTPUT="$SCOUT_DIR/cocoa-beach-fl-market-scout.html"
LOG="$SCOUT_DIR/logs/cocoa-beach-$(date +%Y%m%d).log"

mkdir -p "$SCOUT_DIR/logs"

echo "[$(date)] Starting Cocoa Beach STR scout generation..." | tee -a "$LOG"

PROMPT='You are an expert STR market analyst. Generate a complete, professional HTML market scout report for Cocoa Beach, FL.

Buy box: Budget $500K–$750K | Cash $250K+ | DSCR 20% down | Target CF $30K+ net/yr | Thesis: Total Return | Tax bracket: 24% | 3+ bed, 2+ bath

Use current market data for June 2026. Include:
- Market score (scored 1–10 across 9 categories)
- Sub-market analysis: beachside east of A1A vs canal/west vs Cape Canaveral vs Merritt Island
- Buy box property lanes (Budget / Mid / Premium / Off-Market)
- Full financial model: gross revenue, expenses, NOI, DSCR, net CF
- OBBBA 100% bonus depreciation analysis (24% bracket)
- Space Coast launch economy impact (109 launches 2025, 120+ 2026)
- Seasonal revenue bar chart
- 4 representative properties (on-market + off-market/FSBO/distressed)
- Regulatory: Brevard TDT 5% + FL 6%, Florida SB 4-D condo risk, HOA flags
- 30-day action plan
- Total return analysis (Year 1 cash-on-cash + appreciation + tax savings)
- Comparison vs Gulf Shores and Mansfield

Style: match the format of a professional real-estate investment briefing. Dark navy hero with market score ring, color-coded alerts, mobile-responsive CSS. Output ONLY the complete self-contained HTML document (no markdown, no explanation).'

claude --print "$PROMPT" > "$OUTPUT" 2>>"$LOG"

# Verify output is valid HTML
if grep -q "<!DOCTYPE html>" "$OUTPUT" 2>/dev/null; then
    echo "[$(date)] SUCCESS — cocoa-beach-fl-market-scout.html updated ($(wc -c < "$OUTPUT") bytes)" | tee -a "$LOG"
else
    echo "[$(date)] ERROR — output does not appear to be valid HTML. Check log." | tee -a "$LOG"
    exit 1
fi

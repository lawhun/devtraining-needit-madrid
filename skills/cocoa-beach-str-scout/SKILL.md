# Cocoa Beach STR Scout — Daily Property Scout

## Purpose
Find and rank the top active STR investment listings in Cocoa Beach, FL each morning. Output a self-contained HTML dashboard saved to `~/STR-Scouts/cocoa-beach-scout-dashboard.html`, served at http://10.0.0.51:8754/cocoa-beach-scout-dashboard.html.

Runs 30 minutes after the Mansfield STR Scout (6:00 AM) to avoid API rate conflicts.

## Schedule
**Cowork scheduler — 6:30 AM ET daily**
`mcp__scheduled-tasks__create_scheduled_task` with cron `30 6 * * *` ET, skill name `cocoa-beach-str-scout`.

> ⚠️ DO NOT use launchd or `claude --print`. This skill requires Cowork artifact updates, first-party WebSearch, and AirROI MCP tools — none of which are available headless. The launchd plist and generate-cocoa-beach.sh in the repo are deprecated stubs.

---

## Buy Box
| Parameter | Value |
|-----------|-------|
| Budget | $500,000–$750,000 |
| Loan | DSCR 20% down · ~6.25% rate (verify current) |
| CF Target | $30,000+ net/yr |
| Beds | 3+ (4BR preferred) |
| Baths | 2+ |
| Type | SFH only — **no condos** (FL SB 4-D structural risk) |
| Location | Zip 32931 · East of A1A tourist zone preferred |
| Pool | Preferred (commands $15K–$25K premium revenue) |
| Avoid | Condos, Cape Canaveral (supply +47.2% YoY), Merritt Island (90-day minimum ordinance) |
| Tax bracket | 24% (OBBBA 100% bonus depreciation applies) |
| Thesis | Total Return: CF + appreciation + tax savings |

---

## Step 1 — Fetch Active Listings

Search for current active listings matching the buy box.

**Primary: Apify Zillow/Redfin scraper** (same pattern as Mansfield skill)

Search parameters:
- Location: `Cocoa Beach FL 32931`
- Property type: Single Family
- Price: $500,000–$750,000
- Beds: 3+, Baths: 2+
- Status: Active

**Fallback: WebSearch**
```
Search: "Cocoa Beach FL 32931 single family home for sale 3 bedroom" site:zillow.com OR site:redfin.com
Search: "Cocoa Beach FL 32931 pool home $500k $750k" site:zillow.com
```

Target: 15–25 raw listings before filtering.

For each listing collect:
- Full address (street, city, state, zip)
- List price
- Beds, baths, square footage
- Year built
- Days on market
- Pool (yes/no from listing description or features)
- Condo/HOA flag (disqualifier)
- East of A1A vs Canal vs West (determine from address/cross street)
- Zillow/Redfin URL

---

## Step 2 — Get AirROI Market Metrics

Fetch market-level data for Cocoa Beach:

```
mcp__airroi__airroi_market_metrics_all
  lat: 28.32
  lng: -80.6076
  locality: "Cocoa Beach"
  region: "Florida"
```

> ⚠️ CRITICAL: Do NOT include `listing_type` filter in any AirROI call. This causes all listings to be excluded (confirmed bug). Pass only lat/lng/locality/region.

Also fetch pacing:
```
mcp__airroi__airroi_market_future_pacing
  lat: 28.32
  lng: -80.6076
```

Extract from response:
- Market ADR (4BR target: ~$449 blended)
- Occupancy rate (target: ~62%)
- Active listing count
- Compression event count (next 30 days)
- Pacing vs prior year

---

## Step 3 — Read Dismissed Properties

Read `~/.claude/scout-dismissed.json` to get the list of properties the user has dismissed.

```json
// Example structure:
{
  "4412 Ocean Beach Blvd": true,
  "215 N Atlantic Ave": true
}
```

Filter out any listing whose street address matches a key in this file.

Also read the `cocoa-beach.dismissed` key from the dashboard's localStorage-compatible format if present.

---

## Step 4 — Score and Rank by True CoC

For each non-dismissed listing, calculate True CoC:

### Revenue estimate
- Pull property-specific AirROI if available: `mcp__airroi__airroi_search_by_market` with property address
- Fallback by bedroom count:
  - 3BR east A1A pool: $82K–$92K gross (top-25%)
  - 3BR canal/no pool: $70K–$80K gross
  - 4BR east A1A pool: $100K–$120K gross (top-25%)
  - 4BR canal/no pool: $88K–$100K gross
  - Use midpoint for Base case

### Expense model
| Expense | Calculation |
|---------|-------------|
| Platform fees | 3.5% of gross |
| Cleaning/supplies | $7,200 (3BR) or $8,400 (4BR) |
| Maintenance | 3% of net revenue |
| Utilities | $3,600 (3BR) or $4,800 (4BR) |
| Insurance — beachside/east A1A | $14,000/yr (use $12K–$18K range; ALWAYS get actual quotes) |
| Insurance — canal/west of A1A | $9,000/yr (use $7K–$11K range) |
| Property tax | 1.1% × purchase price |
| PriceLabs | $960/yr |
| Management | $0 (self-managed, owner-operated) |

> ⚠️ Florida coastal insurance is the #1 underwriting risk. The standard "35% OpEx" model assumes ~$4K insurance and overstates CF by $8K–$14K. Always use $12K–$18K for beachside. Flag any property where insurance-adjusted DSCR falls below 1.20.

### Loan parameters (DSCR)
- Down: 20%
- Rate: 6.25% (verify current; was 6.12%–6.49% in June 2026)
- Term: 30 years
- Monthly P&I = `P × [r(1+r)^n] / [(1+r)^n - 1]` where P=loan, r=monthly rate, n=360

### True CoC
```
True CoC = Net Cash Flow / Cash Down
Net Cash Flow = NOI − Annual P&I
NOI = Net Revenue − Operating Expenses (excl. mortgage)
```

Rank all non-dismissed listings by True CoC descending. Select top 5 for the dashboard.

---

## Step 5 — Reno Analysis Flag

For each top-5 property, flag for potential reno if ANY of:
- Year built ≤ 1985
- Days on market > 30
- List price > 10% below comparable active listings
- Listing description contains: "as-is", "investor special", "needs work", "fixer"

If flagged, estimate reno budget:
- Cosmetic (paint, flooring, fixtures): $20K–$35K
- Moderate (kitchen/bath update): $35K–$55K
- Structural (roof, HVAC, electrical): $55K–$95K+
- Post-reno revenue uplift: +$8K–$18K gross/yr (pool add = +$20K–$30K)
- Post-reno DSCR improvement: calculate and show

---

## Step 6 — Generate HTML Dashboard

Write a complete, self-contained HTML file to `~/STR-Scouts/cocoa-beach-scout-dashboard.html`.

Match the format and structure of `~/STR-Scouts/cocoa-beach-scout-dashboard.html` (the seed template in the repo at `index.html` → `cocoa-beach-scout-dashboard.html`). Preserve all JavaScript functionality:
- Dismiss × button (POST to http://10.0.0.51:8754/dismiss with `{address: [...]}`)
- localStorage key: `cocoa-beach.dismissed`
- Deep Underwrite toggle
- Reno Analysis panel (conditional)
- Send to Agent SMS (recipients: Susan 4195640676, Jen 6144068291)

Required sections (same order as template):
1. Hero header with generated date/time, buy box strip
2. KPI stats bar (6 stats from AirROI response)
3. Property cards (top 5, ranked #1–#5 by True CoC)
4. Monthly revenue heatmap (CSS bars, no JS library)
5. Bear/Base/Bull scenario grid (for the #1-ranked property)
6. Market health diagnostics (pacing, compression events)
7. SCOUT_META comment block (JSON, parsed by scheduler to verify output)
8. Back to Hub link → `index.html`

### SCOUT_META block (required, at end of `<body>`)
```html
<!-- SCOUT_META
{
  "market": "Cocoa Beach, FL",
  "generated": "<ISO timestamp>",
  "listingsFound": <count>,
  "listingsFiltered": <dismissed count>,
  "listingsShown": 5,
  "topCoC": "<top property CoC>",
  "buyBoxSummary": "3–4BR · 2+BA · SFH · $500k–$750k · 32931 · East of A1A",
  "renoEvalThreshold": 50000,
  "dismissedKey": "cocoa-beach.dismissed",
  "serverUrl": "http://10.0.0.51:8754",
  "airRoiADR": <value from API>,
  "airRoiOccupancy": <value from API>,
  "nextRefresh": "<next day ISO timestamp at 06:30 ET>"
}
SCOUT_META -->
```

---

## Step 7 — Quality Checks

Before saving, verify:
- [ ] HTML contains `<!DOCTYPE html>` 
- [ ] All 5 property cards present
- [ ] Each card has dismiss button, underwrite toggle, send-to-agent button
- [ ] Financial model numbers are internally consistent (NOI − P&I = Net CF)
- [ ] DSCR = NOI / Annual P&I (flag if < 1.20 with amber warning)
- [ ] No condos included (SB 4-D disqualifier)
- [ ] No Cape Canaveral or Merritt Island properties included
- [ ] SCOUT_META block present and valid JSON
- [ ] Generated timestamp current (within 1 hour of now)

If any check fails, retry Step 6 with corrected data.

---

## Step 8 — Notify

After saving the HTML, send a summary to Cowork artifact `cocoa-beach-str-scout-latest`.

Summary format:
```
🏠 Cocoa Beach STR Scout — [Date]
Top pick: [Address] · $[Price] · CoC [X]% · CF $[Y]K/yr
New listings: [count] · Filtered: [count] · Market ADR: $[ADR]
[Pacing note if compression event in next 7 days]
Dashboard: http://10.0.0.51:8754/cocoa-beach-scout-dashboard.html
```

---

## Market Context (preserve in skill memory)

### Sub-market priority
1. ✅ **East of A1A beachside (32931)** — Highest revenue ($63K avg, $100K+ top-25% 4BR), launch views premium, established tourist zone
2. ✅ **Canal/west of A1A (32931)** — Acceptable; 10–15% lower revenue, significantly lower insurance (~$9K vs $14K), good canal access
3. ❌ **Cape Canaveral** — AVOID. Supply +47.2% YoY, avg revenue only $24.5K vs $63K, occupancy 41.5% vs 59%
4. ❌ **Merritt Island** — AVOID. 90-day minimum STR ordinance; not a short-term rental market

### Insurance flag
Beachside: $12K–$18K/yr (combined HO Wind/Hurricane + NFIP Flood + STR endorsement).  
The standard "35% OpEx" model **underestimates insurance by $8K–$14K**. Always model insurance explicitly; never rely on percentage-based shorthand for Florida coastal.

### FL SB 4-D condo risk
Florida SB 4-D (2022) mandates structural inspections + reserve funding for condos 3+ stories built before 1992. HOA special assessments of $50K–$200K+ per unit have been reported. **No condos in buy box.**

### OBBBA 100% bonus depreciation (24% bracket)
On a $665K purchase: land ~15% = $99,750, improvements ~85% = $565,250.
Year 1 bonus dep deduction: up to $565,250 × 100% = $141,312 tax savings at 24% bracket.
Net Year-1 cash tax benefit: $33,915. Include in Y1 Total Return calculation.

### Space Coast launch economy
2025: 109 SpaceX/ULA/Blue Origin launches from KSC/CCAFS.  
2026 projected: 120+ launches. Launch weekends = compression events with ADR premiums of 30–60%.  
Typical compression cycle: booking spike 6 weeks out, 90%+ occupancy during launch window.  
Include compression event count from AirROI pacing data.

### Comparison benchmarks
| Market | Net CF | CoC | Market Score |
|--------|--------|-----|--------------|
| Cocoa Beach | $14.6K–$23.9K | 11–17% | 7.32/10 |
| Mansfield OH | ~$18K–$30K | varies | 7.8/10 |
| Gulf Shores AL | varies | varies | varies |

---

## Output File Path
`~/STR-Scouts/cocoa-beach-scout-dashboard.html`

Served at: `http://10.0.0.51:8754/cocoa-beach-scout-dashboard.html`

Hub link: `http://10.0.0.51:8754/index.html` (Cocoa Beach → Scout Dashboard button)

---

## Related Skills
- `mansfield-str-scout` — 6:00 AM ET daily (runs 30 min before this skill)
- `cocoa-beach-str-monthly-market-refresh` — 1st of month 7:00 AM ET (market metrics refresh, AirROI deep dive)
- `bryce-job-scout` — 7:00 AM ET daily (runs 30 min after this skill)

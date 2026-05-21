# PriceLabs Integration Research
## STR Acquisition Market Research & Analysis

---

## EXECUTIVE SUMMARY

PriceLabs is the most data-rich STR-native platform available for connecting to Claude for acquisition market research. It offers **four distinct connectivity paths** ranging from a purpose-built MCP server (direct Claude integration, zero code) to a full REST API. The platform covers ADR, occupancy, RevPAR, active listings, comp set analysis, demand classification, neighborhood data, and forward-looking pacing — exactly the data layer needed for STR acquisition due diligence.

**Recommended path: MCP Server** (nicholasgriffintn/pricelabs) → direct plug-in to Claude Code. Takes ~15 minutes to configure, requires only your PriceLabs API key.

---

## WHAT PRICELABS IS

PriceLabs is a dynamic pricing and revenue management platform built specifically for short-term rentals. It aggregates Airbnb and VRBO listing-level data across 200+ markets globally and surfaces it through dashboards, APIs, and now MCP tools. For STR acquisition research it is uniquely valuable because it contains *forward-looking* demand and pacing data — not just historical — which is critical for underwriting.

**Core product modules relevant to market research:**

| Module | What It Gives You | Cost |
|---|---|---|
| STR Index | Country/state/region ADR, occupancy, RevPAR, active listings (historical + pacing) | Free |
| Market Dashboards | 1k–10k listing-level data within 0.1–50km radius, comp sets, supply trends | $9.99/dashboard/mo |
| Neighborhood Data | How a specific listing ranks vs. 75th/90th percentile peers | Included with Dynamic Pricing sub |
| Revenue Estimator Pro | Projected annual revenue by address + property type | Separate sub |
| Revenue Estimator API | Programmatic revenue projections for any location | Developer access (apply) |
| Customer API | Full account data: listings, reservations, calendars, pricing | Included with PriceLabs account |

---

## CONNECTIVITY OPTIONS — DETAILED BREAKDOWN

### Option 1: MCP Server (BEST for Claude Integration)

**What it is:** A pre-built Model Context Protocol server that connects PriceLabs data directly into Claude. Two community MCP servers exist:

#### A. nicholasgriffintn/pricelabs (Recommended)
- Released: March 28, 2026
- **10 tools** covering the PriceLabs pricing API
- Direct integration with the Customer API
- Cleanest, most maintained option for Claude Code
- Source: [PulseMCP listing](https://www.pulsemcp.com/servers/nicholasgriffintn-pricelabs)

#### B. akashnambiar/pl-rm-skills (Advanced Revenue Management)
- **23 MCP tools** organized as a 3-layer skill tree
- Layer 1 (Base Data): `market-insight`, `reservation-insight`, `comp-set-data`, `listing-portfolio`
- Layer 2 (Analytical): `demand-classification`, `comp-set-positioning`, `revenue-health`, `seasonal-context`
- Layer 3 (Strategy): `orphan-gap-optimizer`, `los-optimizer`, `seasonal-pricing`, `last-minute-discount`, `comp-set-repricing`, `event-based-pricing`
- Includes mock API server with 24 endpoints for testing without live credentials
- Source: [LobeHub listing](https://lobehub.com/ko/mcp/akashnambiar-dot-pl-rm-skills)

**Use case for acquisition research:** Ask Claude to pull `market-insight` + `demand-classification` for a target market, then run `comp-set-positioning` against candidate properties. Claude synthesizes the data into an acquisition recommendation — all in one conversation.

---

### Option 2: PriceLabs Customer API (Direct REST)

**What it is:** A versioned REST API available to all PriceLabs account holders. Authenticated via API key.

- **Base URL:** `https://api.pricelabs.co/`
- **Documentation:** Postman collection + Swagger interactive explorer
- **Authentication:** API key (Settings → API Details → Enable)
- **Key endpoints:**
  - Listings — portfolio metadata
  - Listing calendars — date-level availability and pricing
  - Reservations — booking history and forward reservations
  - Pricing recommendations — dynamic price output per listing
- **Limitation:** The Customer API exposes *your own* listings' data. It does not expose raw market-wide comp data directly — that lives in Market Dashboards.

**Use case:** Automate data pulls into a spreadsheet or database; feed that structured data to Claude for analysis. Works well with Make.com (see Option 4).

---

### Option 3: Revenue Estimator API

**What it is:** A separate API that returns projected revenue, ADR, and occupancy for *any address* — even unlisted properties. Purpose-built for acquisition underwriting.

- **Access:** Apply via form at `hello.pricelabs.co/revenue-estimator-api-widget/`
- **Target users:** Developers, property management companies, real estate platforms
- **Returns:** Annual revenue projection, seasonal breakdown, comparable listing data
- **Widget variant:** Embeddable JavaScript widget (no API calls needed for simple use)
- **Limitation:** Requires separate approval process; not instant access

**Use case for acquisition:** Feed a target property address → get projected revenue in JSON → Claude interprets and computes cap rate, cash-on-cash return, payback period.

---

### Option 4: Make.com Automation (No-Code Workflow)

**What it is:** PriceLabs has a community integration on Make.com (formerly Integromat) that allows visual no-code workflows connecting PriceLabs to Google Sheets, Airtable, Notion, Slack, or any other app.

- **Integration page:** `make.com/en/integrations/pricelabs-community`
- **Setup:** Connect PriceLabs API key inside Make.com, then drag-and-drop workflows
- **Best workflows for acquisition research:**
  - Pull Market Dashboard CSV → append to Google Sheets → trigger Claude analysis via webhook
  - Monitor specific markets for ADR/occupancy changes → alert via Slack
  - Schedule weekly STR Index data pulls for target markets → build trend database

**Use case:** Best for recurring market monitoring. Not real-time, but excellent for building a structured research database Claude can query.

---

### Option 5: Manual CSV/PDF Export + Claude File Upload

**What it is:** Every module in Market Dashboards has a CSV export button (pink icon, upper right). Full dashboards export as PDF.

- **Exports available:** ADR trends, occupancy trends, supply changes, pacing, amenity demand, comp set rankings
- **Limitation:** Underlying booking-level data cannot be exported
- **Claude use:** Upload CSV directly to Claude → "analyze this market data and flag acquisition opportunities where RevPAR growth is >15% YoY and supply growth is <5%"

This is the lowest-friction starting point with zero setup.

---

### Option 6: STR Index (Free Public Data)

**What it is:** PriceLabs' free public market intelligence tool. No account required.

- **URL:** `hello.pricelabs.co/market-data/`
- **Coverage:** Nearly every country, with state/region breakdowns
- **Data:** ADR, occupancy, RevPAR, active listings, historical trends, forward pacing
- **Programmatic access:** Can be scraped or exported for research (review ToS for automated use)

**Use case:** Quick top-of-funnel market screening before buying a paid dashboard.

---

## RECOMMENDATIONS FOR STR ACQUISITION RESEARCH

### Recommended Stack (Prioritized)

1. **MCP Server** (nicholasgriffintn/pricelabs) → Claude Code — for live, conversational market analysis during deal evaluation
2. **Market Dashboards** ($9.99/mo per market) → CSV export → Claude — for deep comp set analysis on shortlisted markets
3. **Revenue Estimator API** (apply for access) → custom Python tool in Claude — for automated underwriting on specific addresses
4. **Make.com** → Google Sheets/Airtable → Claude — for ongoing portfolio monitoring of target markets

### What Claude Can Do With This Data

With PriceLabs data flowing into Claude via MCP or API, you can ask:
- *"Compare RevPAR trends for Nashville vs. Asheville over the past 24 months and identify which has better forward pacing heading into Q3"*
- *"For this address in Scottsdale, run a revenue projection and model a 6.5% cap rate — what purchase price does that support?"*
- *"Flag all markets where 2BR occupancy >70%, ADR growing >10% YoY, and fewer than 500 active listings (under-supplied)"*
- *"Build a comp set of 15 properties within 5km of this address, filter for 3BR with pool, and show me the 75th percentile ADR by month"*

---

## STEP-BY-STEP GUIDE: CONNECT PRICELABS TO CLAUDE CODE VIA MCP

### Prerequisites
- Active PriceLabs account (any paid plan)
- Claude Code CLI installed and running
- Node.js 18+ installed

---

### Step 1: Get Your PriceLabs API Key

1. Log into PriceLabs at `app.pricelabs.co`
2. Click your **profile icon** (top right) → **Account Settings**
3. Navigate to the **API Details** tab
4. Click **Enable API Access**
5. Copy your API key — it looks like a long alphanumeric string

---

### Step 2: Install the PriceLabs MCP Server

Open a terminal and run:

```bash
npm install -g @nicholasgriffintn/pricelabs-mcp-server
```

> If that package name doesn't resolve (it may be under a slightly different npm slug), find it via:
> ```bash
> npm search pricelabs mcp
> ```
> Or clone directly from GitHub:
> ```bash
> git clone https://github.com/nicholasgriffintn/pricelabs-mcp-server.git
> cd pricelabs-mcp-server
> npm install && npm run build
> ```

---

### Step 3: Configure the MCP Server in Claude Code

Open or create your Claude Code MCP config file:

```bash
# For project-level config (recommended):
nano /home/user/devtraining-needit-madrid/.claude/mcp.json

# For global config (applies to all projects):
nano ~/.claude/mcp.json
```

Add the PriceLabs server entry:

```json
{
  "mcpServers": {
    "pricelabs": {
      "command": "npx",
      "args": ["@nicholasgriffintn/pricelabs-mcp-server"],
      "env": {
        "PRICELABS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

If you cloned manually, point to the built file instead:

```json
{
  "mcpServers": {
    "pricelabs": {
      "command": "node",
      "args": ["/path/to/pricelabs-mcp-server/dist/index.js"],
      "env": {
        "PRICELABS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

---

### Step 4: Verify the Connection

Start or restart Claude Code:

```bash
claude
```

Then type:

```
/mcp
```

You should see `pricelabs` listed as a connected server with its available tools. If it shows as disconnected, check:
- API key is correct (no extra spaces)
- Node.js is on PATH
- Package installed successfully (`which pricelabs-mcp-server` or check npm global list)

---

### Step 5: Add the Advanced Skill Tree (Optional — for Revenue Management)

For the full 23-tool revenue management skill tree (Option 1B above):

```json
{
  "mcpServers": {
    "pricelabs": {
      "command": "npx",
      "args": ["@nicholasgriffintn/pricelabs-mcp-server"],
      "env": {
        "PRICELABS_API_KEY": "your_api_key_here"
      }
    },
    "pricelabs-rm-skills": {
      "command": "npx",
      "args": ["@akashnambiar/pl-rm-skills"],
      "env": {
        "PRICELABS_API_KEY": "your_api_key_here",
        "PRICELABS_API_BASE": "https://api.pricelabs.co"
      }
    }
  }
}
```

---

### Step 6: Apply for Revenue Estimator API Access (Acquisition Underwriting)

1. Go to: `hello.pricelabs.co/revenue-estimator-api-widget/`
2. Click **"Request API Access"**
3. Fill in the form — describe your use case as "STR acquisition underwriting and market research"
4. Once approved, you'll receive a separate API key for the Revenue Estimator endpoint
5. Add this as a second environment variable: `PRICELABS_RE_API_KEY`

---

### Step 7: Test With a Real Market Research Query

Once connected, try this prompt in Claude Code:

```
Using the PriceLabs MCP tools, pull market insight data for Nashville, TN.
Show me ADR, occupancy, and RevPAR for the past 12 months, then classify
current demand level and tell me if this market supports a 3BR STR acquisition
at a $450,000 purchase price targeting 8% cash-on-cash return.
```

---

## ALTERNATIVE: MAKE.COM NO-CODE SETUP

If you prefer no-code automation for recurring data pulls:

1. Create a free Make.com account at `make.com`
2. Search for **PriceLabs** in the app library → select **PriceLabs Community**
3. Click **Create a new scenario**
4. Add a **PriceLabs** trigger (e.g., "Watch Listings" or "Get Market Data")
5. Connect your PriceLabs account via API key
6. Add a **Google Sheets** or **Airtable** action to store the data
7. Schedule the scenario to run daily or weekly
8. Upload the resulting sheet to Claude for analysis, or connect Claude via webhook

---

## KEY LIMITATIONS TO KNOW

| Limitation | Impact | Workaround |
|---|---|---|
| Customer API exposes only *your* listings | Can't pull comp market data directly | Use Market Dashboards + CSV export |
| Underlying booking data not exportable | No guest-level data | Use aggregated ADR/occupancy from dashboards |
| Revenue Estimator API requires approval | Not instant access | Apply early; use Pro web UI in the meantime |
| Market Dashboards cost $9.99/mo each | Budget consideration for 10+ markets | Use STR Index for top-of-funnel screening first |
| MCP servers are community-maintained | May have gaps vs. official API | Supplement with direct API calls via Python tools |

---

## SOURCES

- [PriceLabs Customer API Documentation](https://help.pricelabs.co/portal/en/kb/articles/pricelabs-api)
- [Building an API Integration with PriceLabs](https://help.pricelabs.co/portal/en/kb/articles/building-an-integration-with-pricelabs)
- [PriceLabs Dynamic Pricing API](https://hello.pricelabs.co/dynamic-pricing-api/)
- [PriceLabs Revenue Estimator API & Widget](https://hello.pricelabs.co/revenue-estimator-api-widget/)
- [PriceLabs Market Dashboards](https://hello.pricelabs.co/market-dashboards/)
- [PriceLabs Open API Launch Blog](https://hello.pricelabs.co/blog/pricelabs-launches-open-api/)
- [PriceLabs STR Index / Market Data](https://hello.pricelabs.co/market-data/)
- [PriceLabs Enterprise Market Insights](https://hello.pricelabs.co/enterprise/market-insights/)
- [nicholasgriffintn PriceLabs MCP Server — PulseMCP](https://www.pulsemcp.com/servers/nicholasgriffintn-pricelabs)
- [akashnambiar PriceLabs Revenue Management Skills MCP — LobeHub](https://lobehub.com/ko/mcp/akashnambiar-dot-pl-rm-skills)
- [PriceLabs on Make.com](https://www.make.com/en/integrations/pricelabs-community)
- [PriceLabs API Postman Documentation](https://www.postman.com/security-geoscientist-28133657/pricelabs/documentation/yu0l484/pricelabs-api)
- [PriceLabs 2026 STR Revenue Management Strategy](https://hello.pricelabs.co/blog/revenue-management-strategy/)
- [PriceLabs Market Dashboards — Hotel Tech Report 2026](https://hoteltechreport.com/revenue-management/market-intelligence-tools/pricelabs-market-dashboards)

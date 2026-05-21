from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import PageBreak

# Brand colors
NAVY    = HexColor("#0D1B2A")
TEAL    = HexColor("#1A7A6E")
LIGHT   = HexColor("#F4F7F9")
BORDER  = HexColor("#D0D9E0")
ACCENT  = HexColor("#E8F4F2")
MUTED   = HexColor("#6B7C8A")
WHITE   = white
RED     = HexColor("#C0392B")
GREEN   = HexColor("#1A7A6E")

OUTPUT = "/home/user/devtraining-needit-madrid/PriceLabs-Integration-Research.pdf"

def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.6*inch,
        bottomMargin=0.75*inch,
        title="PriceLabs Integration Research",
        author="STR Acquisition Research",
    )

    styles = getSampleStyleSheet()

    # ── Custom styles ──────────────────────────────────────────────────────────
    h_cover = ParagraphStyle("h_cover", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=28, textColor=WHITE,
        leading=34, spaceAfter=6)
    sub_cover = ParagraphStyle("sub_cover", parent=styles["Normal"],
        fontName="Helvetica", fontSize=13, textColor=HexColor("#B0C8D4"),
        leading=18, spaceAfter=4)
    meta_cover = ParagraphStyle("meta_cover", parent=styles["Normal"],
        fontName="Helvetica", fontSize=10, textColor=HexColor("#8BAAB8"),
        leading=14)

    h1 = ParagraphStyle("h1", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=16, textColor=NAVY,
        spaceBefore=18, spaceAfter=6, leading=20,
        borderPad=0, leftIndent=0)
    h2 = ParagraphStyle("h2", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=12, textColor=TEAL,
        spaceBefore=12, spaceAfter=4, leading=15)
    h3 = ParagraphStyle("h3", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
        spaceBefore=8, spaceAfter=3, leading=13)
    body = ParagraphStyle("body", parent=styles["Normal"],
        fontName="Helvetica", fontSize=9.5, textColor=HexColor("#2C3E50"),
        leading=14.5, spaceAfter=4)
    body_sm = ParagraphStyle("body_sm", parent=styles["Normal"],
        fontName="Helvetica", fontSize=8.5, textColor=HexColor("#2C3E50"),
        leading=13, spaceAfter=3)
    bullet = ParagraphStyle("bullet", parent=styles["Normal"],
        fontName="Helvetica", fontSize=9.5, textColor=HexColor("#2C3E50"),
        leading=14, leftIndent=14, firstLineIndent=-10, spaceAfter=3)
    bullet_b = ParagraphStyle("bullet_b", parent=bullet,
        fontName="Helvetica-Bold")
    code_style = ParagraphStyle("code", parent=styles["Normal"],
        fontName="Courier", fontSize=8.5, textColor=HexColor("#1E3A4A"),
        leading=13, leftIndent=6, spaceAfter=2)
    label = ParagraphStyle("label", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=8, textColor=TEAL,
        leading=11, spaceAfter=1, spaceBefore=2)
    muted = ParagraphStyle("muted", parent=styles["Normal"],
        fontName="Helvetica-Oblique", fontSize=8.5, textColor=MUTED,
        leading=12, spaceAfter=3)
    section_note = ParagraphStyle("section_note", parent=styles["Normal"],
        fontName="Helvetica", fontSize=8.5, textColor=HexColor("#2C3E50"),
        leading=13, leftIndent=8, spaceAfter=2,
        backColor=ACCENT, borderPad=4)

    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # COVER BLOCK  (navy banner implemented via a single-cell Table)
    # ══════════════════════════════════════════════════════════════════════════
    cover_inner = [
        Paragraph("PriceLabs", h_cover),
        Paragraph("Integration Research &amp; Connection Guide", sub_cover),
        Spacer(1, 10),
        Paragraph("STR Acquisition Market Research · May 2026", meta_cover),
        Paragraph("Prepared for: gene@lawhun.com", meta_cover),
    ]
    cover_table = Table([[cover_inner]], colWidths=[7.0*inch])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 28),
        ("BOTTOMPADDING", (0,0), (-1,-1), 28),
        ("LEFTPADDING",   (0,0), (-1,-1), 24),
        ("RIGHTPADDING",  (0,0), (-1,-1), 24),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 20))

    # ══════════════════════════════════════════════════════════════════════════
    # EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Executive Summary", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=8))
    story.append(Paragraph(
        "PriceLabs is the most data-rich STR-native platform available for connecting to Claude for "
        "acquisition market research. It offers <b>four distinct connectivity paths</b> ranging from a "
        "purpose-built MCP server (direct Claude integration, zero code) to a full REST API. The "
        "platform covers ADR, occupancy, RevPAR, active listings, comp set analysis, demand "
        "classification, and forward-looking pacing data — exactly the layer needed for STR acquisition "
        "due diligence.", body))
    story.append(Spacer(1, 4))

    # Recommended path callout box
    rec_data = [[
        Paragraph("RECOMMENDED PATH", label),
        Paragraph(
            "<b>MCP Server</b> (nicholasgriffintn/pricelabs) → direct plug-in to Claude Code. "
            "Takes ~15 minutes to configure, requires only your PriceLabs API key. "
            "No additional cost beyond your existing PriceLabs subscription.", body_sm),
    ]]
    rec_table = Table(rec_data, colWidths=[1.1*inch, 5.9*inch])
    rec_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), ACCENT),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LINEAFTER",     (0,0), (0,-1), 2, TEAL),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 16))

    # ══════════════════════════════════════════════════════════════════════════
    # WHAT PRICELABS OFFERS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("What PriceLabs Offers for STR Acquisition Research", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=8))

    tbl_headers = ["Tool", "Data Available", "Cost"]
    tbl_rows = [
        ["STR Index",             "ADR, occupancy, RevPAR, active listings by country/state/region; historical + forward pacing", "Free"],
        ["Market Dashboards",     "1k–10k listing-level data within 0.1–50 km; comp sets, supply trends, demand pacing, amenity demand", "$9.99/dashboard/mo"],
        ["Revenue Estimator Pro", "Projected annual revenue by address + property type; seasonal breakdown", "Separate sub"],
        ["Revenue Estimator API", "Programmatic revenue projections for any address — not just your listings", "Apply for access"],
        ["Customer API",          "Your own listings: calendars, reservations, pricing output, neighborhood rankings", "Included with account"],
        ["Neighborhood Data",     "How a specific listing ranks vs. 75th/90th percentile peers in its micro-market", "Included w/ Dynamic Pricing"],
    ]
    col_w = [1.5*inch, 4.0*inch, 1.5*inch]
    data = [[Paragraph(f"<b>{c}</b>", ParagraphStyle("th", parent=body_sm,
                fontName="Helvetica-Bold", textColor=WHITE)
             ) for c in tbl_headers]]
    for i, row in enumerate(tbl_rows):
        bg = LIGHT if i % 2 == 0 else WHITE
        data.append([Paragraph(row[0], ParagraphStyle("td_b", parent=body_sm,
                         fontName="Helvetica-Bold", textColor=NAVY)),
                     Paragraph(row[1], body_sm),
                     Paragraph(row[2], body_sm)])

    t = Table(data, colWidths=col_w)
    ts = TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("GRID",          (0,0), (-1,-1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [LIGHT, WHITE]),
    ])
    t.setStyle(ts)
    story.append(t)
    story.append(Spacer(1, 20))

    # ══════════════════════════════════════════════════════════════════════════
    # CONNECTIVITY OPTIONS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Connectivity Options — Detailed Breakdown", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=8))

    # ── Option 1: MCP ─────────────────────────────────────────────────────────
    story.append(Paragraph("Option 1: MCP Server  ★ Recommended", h2))
    story.append(Paragraph(
        "A pre-built Model Context Protocol server that connects PriceLabs data directly into "
        "Claude Code. Two community MCP servers exist:", body))

    # Server A card
    def option_card(badge, title, subtitle, bullets, bg=ACCENT):
        inner = [
            [Paragraph(badge, ParagraphStyle("badge", parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=7.5, textColor=WHITE)),
             Paragraph(f"<b>{title}</b>", h3),
             Paragraph(subtitle, muted)],
        ]
        # flatten bullets as nested table rows
        rows = [[Paragraph(f"• {b}", body_sm)] for b in bullets]
        bullet_t = Table(rows, colWidths=[6.4*inch])
        bullet_t.setStyle(TableStyle([
            ("LEFTPADDING",   (0,0), (-1,-1), 0),
            ("TOPPADDING",    (0,0), (-1,-1), 1),
            ("BOTTOMPADDING", (0,0), (-1,-1), 1),
        ]))
        card_data = [
            [Paragraph(badge, ParagraphStyle("badge", parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=7, textColor=WHITE,
                backColor=TEAL)),
             [Paragraph(f"<b>{title}</b>", h3),
              Paragraph(subtitle, muted),
              bullet_t]]
        ]
        card = Table(card_data, colWidths=[0.55*inch, 6.45*inch])
        card.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (0,-1), TEAL),
            ("BACKGROUND",    (1,0), (1,-1), bg),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (0,-1), 6),
            ("RIGHTPADDING",  (0,0), (0,-1), 6),
            ("LEFTPADDING",   (1,0), (1,-1), 10),
            ("RIGHTPADDING",  (1,0), (1,-1), 10),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
            ("ROUNDEDCORNERS", [6]),
        ]))
        return card

    story.append(Spacer(1, 4))
    card_a = option_card(
        "A",
        "nicholasgriffintn / pricelabs",
        "10 tools · Pricing API · Released March 2026 · pulsemcp.com/servers/nicholasgriffintn-pricelabs",
        [
            "Cleanest, most maintained option for Claude Code",
            "Covers core pricing, listing, and calendar data",
            "Requires only your standard PriceLabs API key",
        ]
    )
    story.append(card_a)
    story.append(Spacer(1, 8))

    card_b = option_card(
        "B",
        "akashnambiar / pl-rm-skills",
        "23 tools · Full Revenue Management Skill Tree · lobehub.com/ko/mcp/akashnambiar-dot-pl-rm-skills",
        [
            "Layer 1 — Base Data: market-insight, reservation-insight, comp-set-data, listing-portfolio",
            "Layer 2 — Analytical: demand-classification, comp-set-positioning, revenue-health, seasonal-context",
            "Layer 3 — Strategy: orphan-gap-optimizer, los-optimizer, seasonal-pricing, last-minute-discount, comp-set-repricing, event-based-pricing",
            "Includes mock API server with 24 endpoints for testing without live credentials",
            "Skills execute bottom-up (Layer 1 → 2 → 3); each skill is self-contained with declared dependencies",
        ],
        bg=HexColor("#EEF6F5")
    )
    story.append(card_b)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Acquisition research use case:</b> Ask Claude to pull market-insight + demand-classification "
        "for a target market, then run comp-set-positioning against candidate properties. Claude "
        "synthesizes the data into an acquisition recommendation — all in one conversation.", section_note))

    story.append(Spacer(1, 14))

    # ── Option 2: Customer API ────────────────────────────────────────────────
    story.append(Paragraph("Option 2: PriceLabs Customer API", h2))
    story.append(Paragraph(
        "A versioned REST API available to all PriceLabs account holders, authenticated via API key.", body))
    cols2 = [
        ["Base URL", "https://api.pricelabs.co/"],
        ["Authentication", "API key (Settings → API Details → Enable)"],
        ["Documentation", "Postman collection + Swagger interactive explorer"],
        ["Key data", "Your listings, listing calendars, reservations, pricing recommendations"],
        ["Limitation", "Only exposes YOUR listings — not raw market-wide comp data"],
    ]
    t2 = Table([[Paragraph(f"<b>{r[0]}</b>", body_sm), Paragraph(r[1], body_sm)] for r in cols2],
               colWidths=[1.4*inch, 5.6*inch])
    t2.setStyle(TableStyle([
        ("GRID",          (0,0), (-1,-1), 0.5, BORDER),
        ("BACKGROUND",    (0,0), (0,-1), LIGHT),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    story.append(t2)
    story.append(Spacer(1, 14))

    # ── Option 3: Revenue Estimator API ───────────────────────────────────────
    story.append(Paragraph("Option 3: Revenue Estimator API", h2))
    story.append(Paragraph(
        "Returns projected revenue, ADR, and occupancy for <b>any address</b> — even unlisted "
        "properties. Purpose-built for acquisition underwriting.", body))
    for b in [
        "<b>Access:</b> Apply via form at hello.pricelabs.co/revenue-estimator-api-widget/",
        "<b>Returns:</b> Annual revenue projection, seasonal breakdown, comparable listing data",
        "<b>Widget variant:</b> Embeddable JavaScript widget (no API calls needed for simple use)",
        "<b>Limitation:</b> Requires separate approval; not instant access",
        "<b>Use case:</b> Feed a target address → get projected revenue in JSON → Claude computes cap rate, CoC return, payback period",
    ]:
        story.append(Paragraph(b, bullet))
    story.append(Spacer(1, 14))

    # ── Option 4: Make.com ────────────────────────────────────────────────────
    story.append(Paragraph("Option 4: Make.com No-Code Automation", h2))
    story.append(Paragraph(
        "Visual no-code workflows connecting PriceLabs to Google Sheets, Airtable, Notion, Slack, "
        "or any other app. Best for recurring market monitoring.", body))
    for b in [
        "Connect PriceLabs API key inside Make.com, then drag-and-drop workflows",
        "Pull Market Dashboard CSV → append to Google Sheets → trigger Claude analysis via webhook",
        "Monitor specific markets for ADR/occupancy changes → alert via Slack",
        "Schedule weekly STR Index pulls for target markets → build trend database",
    ]:
        story.append(Paragraph(f"• {b}", bullet))
    story.append(Spacer(1, 14))

    # ── Option 5: CSV Export ──────────────────────────────────────────────────
    story.append(Paragraph("Option 5: CSV / PDF Export + Claude Upload", h2))
    story.append(Paragraph(
        "Every module in Market Dashboards has a CSV export button (pink icon, upper right). "
        "Full dashboards export as PDF. Zero setup — upload directly to Claude and ask "
        "questions like: <i>Analyze this market data and flag acquisition opportunities where "
        "RevPAR growth is &gt;15% YoY and supply growth is &lt;5%.</i>", body))
    story.append(Paragraph(
        "Note: Underlying booking-level data cannot be exported.", muted))

    story.append(Spacer(1, 20))

    # ══════════════════════════════════════════════════════════════════════════
    # STEP-BY-STEP CONNECTION GUIDE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Step-by-Step: Connect PriceLabs to Claude Code via MCP", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=8))
    story.append(Paragraph(
        "<b>Prerequisites:</b> Active PriceLabs account (any paid plan) · Claude Code CLI installed · Node.js 18+", muted))
    story.append(Spacer(1, 8))

    steps = [
        ("Step 1", "Get Your PriceLabs API Key",
         "Log into app.pricelabs.co → click your profile icon (top right) → Account Settings → "
         "API Details tab → Enable API Access → copy your API key.",
         None),
        ("Step 2", "Install the MCP Server",
         "Open a terminal and run:", "npm install -g @nicholasgriffintn/pricelabs-mcp-server"),
        ("Step 3", "Configure in Claude Code",
         "Open or create .claude/mcp.json in your project root (or ~/.claude/mcp.json for global):",
         '{\n  "mcpServers": {\n    "pricelabs": {\n      "command": "npx",\n      "args": ["@nicholasgriffintn/pricelabs-mcp-server"],\n      "env": {\n        "PRICELABS_API_KEY": "your_api_key_here"\n      }\n    }\n  }\n}'),
        ("Step 4", "Verify the Connection",
         "Start or restart Claude Code, then type /mcp — 'pricelabs' should appear as a connected server with its tools listed. "
         "If disconnected, check: API key has no extra spaces, Node.js is on PATH, package installed successfully.",
         None),
        ("Step 5", "Apply for Revenue Estimator API",
         "For address-level underwriting, visit hello.pricelabs.co/revenue-estimator-api-widget/ and request developer access. "
         "Describe your use case as 'STR acquisition underwriting'. Once approved, add PRICELABS_RE_API_KEY to your env block.",
         None),
        ("Step 6", "Test With a Real Acquisition Query",
         "Try this prompt in Claude Code:", None),
    ]
    test_query = (
        "Using PriceLabs, pull market insight for [target city]. Show ADR, occupancy,\n"
        "and RevPAR trends for 12 months, classify current demand level, and tell me\n"
        "if a 3BR acquisition at $450,000 supports an 8% cash-on-cash return."
    )

    for num, title, desc, code in steps:
        step_content = [
            Paragraph(f"<b>{num}: {title}</b>", h3),
            Paragraph(desc, body_sm),
        ]
        if code:
            step_content.append(Spacer(1, 3))
            code_block_data = [[Paragraph(line if line else " ", code_style)] for line in code.split("\n")]
            code_t = Table(code_block_data, colWidths=[5.9*inch])
            code_t.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (-1,-1), HexColor("#EBF0F2")),
                ("TOPPADDING",    (0,0), (-1,-1), 2),
                ("BOTTOMPADDING", (0,0), (-1,-1), 2),
                ("LEFTPADDING",   (0,0), (-1,-1), 10),
                ("RIGHTPADDING",  (0,0), (-1,-1), 10),
                ("ROUNDEDCORNERS", [4]),
            ]))
            step_content.append(code_t)

        step_row = Table(
            [[Paragraph(num.replace("Step ", ""), ParagraphStyle("stepnum", parent=styles["Normal"],
                fontName="Helvetica-Bold", fontSize=11, textColor=WHITE, alignment=TA_CENTER)),
              step_content]],
            colWidths=[0.45*inch, 6.55*inch]
        )
        step_row.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (0,-1), TEAL),
            ("BACKGROUND",    (1,0), (1,-1), WHITE),
            ("TOPPADDING",    (0,0), (-1,-1), 10),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
            ("LEFTPADDING",   (0,0), (0,-1), 4),
            ("RIGHTPADDING",  (0,0), (0,-1), 4),
            ("LEFTPADDING",   (1,0), (1,-1), 12),
            ("RIGHTPADDING",  (1,0), (1,-1), 8),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
            ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
            ("LINEBELOW",     (0,0), (-1,-1), 0.5, BORDER),
        ]))
        story.append(step_row)

    # test query block
    query_lines = test_query.split("\n")
    q_data = [[Paragraph(line, code_style)] for line in query_lines]
    q_t = Table(q_data, colWidths=[7.0*inch])
    q_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), HexColor("#EBF0F2")),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(Spacer(1, 6))
    story.append(q_t)
    story.append(Spacer(1, 20))

    # ══════════════════════════════════════════════════════════════════════════
    # KEY LIMITATIONS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Key Limitations", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=8))

    lim_headers = ["Limitation", "Impact", "Workaround"]
    lim_rows = [
        ["Customer API only exposes YOUR listings", "Can't pull comp market data directly via API", "Use Market Dashboards + CSV export"],
        ["Underlying booking data not exportable", "No guest-level detail", "Use aggregated ADR/occupancy from dashboards"],
        ["Revenue Estimator API requires approval", "Not instant access", "Apply early; use Pro web UI in the meantime"],
        ["Market Dashboards cost $9.99/mo each", "Budget consideration for 10+ markets", "Use free STR Index for top-of-funnel screening first"],
        ["MCP servers are community-maintained", "May have gaps vs. official API", "Supplement with direct API calls via Python tools"],
    ]
    lim_col_w = [2.1*inch, 2.3*inch, 2.6*inch]
    lim_data = [[Paragraph(f"<b>{c}</b>", ParagraphStyle("lth", parent=body_sm,
                    fontName="Helvetica-Bold", textColor=WHITE)) for c in lim_headers]]
    for row in lim_rows:
        lim_data.append([Paragraph(row[0], ParagraphStyle("ltd_b", parent=body_sm,
                              fontName="Helvetica-Bold", textColor=RED)),
                         Paragraph(row[1], body_sm),
                         Paragraph(row[2], ParagraphStyle("ltd_g", parent=body_sm,
                              textColor=HexColor("#1A6A40")))])
    lim_t = Table(lim_data, colWidths=lim_col_w)
    lim_t.setStyle(TableStyle([
        ("BACKGROUND",     (0,0), (-1,0), NAVY),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [LIGHT, WHITE]),
        ("GRID",           (0,0), (-1,-1), 0.5, BORDER),
        ("TOPPADDING",     (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 6),
        ("LEFTPADDING",    (0,0), (-1,-1), 8),
        ("RIGHTPADDING",   (0,0), (-1,-1), 8),
        ("VALIGN",         (0,0), (-1,-1), "TOP"),
    ]))
    story.append(lim_t)
    story.append(Spacer(1, 20))

    # ══════════════════════════════════════════════════════════════════════════
    # SOURCES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Sources", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=8))
    sources = [
        ("PriceLabs Customer API Documentation", "help.pricelabs.co/portal/en/kb/articles/pricelabs-api"),
        ("Building an API Integration with PriceLabs", "help.pricelabs.co/portal/en/kb/articles/building-an-integration-with-pricelabs"),
        ("PriceLabs Dynamic Pricing API", "hello.pricelabs.co/dynamic-pricing-api/"),
        ("PriceLabs Revenue Estimator API & Widget", "hello.pricelabs.co/revenue-estimator-api-widget/"),
        ("PriceLabs Market Dashboards", "hello.pricelabs.co/market-dashboards/"),
        ("PriceLabs Open API Launch", "hello.pricelabs.co/blog/pricelabs-launches-open-api/"),
        ("PriceLabs STR Index / Market Data", "hello.pricelabs.co/market-data/"),
        ("PriceLabs Enterprise Market Insights", "hello.pricelabs.co/enterprise/market-insights/"),
        ("nicholasgriffintn PriceLabs MCP Server", "pulsemcp.com/servers/nicholasgriffintn-pricelabs"),
        ("akashnambiar Revenue Management Skills MCP", "lobehub.com/ko/mcp/akashnambiar-dot-pl-rm-skills"),
        ("PriceLabs on Make.com", "make.com/en/integrations/pricelabs-community"),
        ("PriceLabs API Postman Documentation", "postman.com/security-geoscientist-28133657/pricelabs/documentation/yu0l484/pricelabs-api"),
        ("2026 STR Revenue Management Strategy", "hello.pricelabs.co/blog/revenue-management-strategy/"),
        ("PriceLabs Market Dashboards — Hotel Tech Report 2026", "hoteltechreport.com/revenue-management/market-intelligence-tools/pricelabs-market-dashboards"),
    ]
    for title, url in sources:
        story.append(Paragraph(
            f"• <b>{title}</b> — <font color='#1A7A6E'>{url}</font>",
            body_sm))

    # ══════════════════════════════════════════════════════════════════════════
    # FOOTER (via canvas callback not needed — use bottom spacer + note)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Research conducted May 2026 · STR Acquisition Analysis · gene@lawhun.com · "
        "Repo: lawhun/devtraining-needit-madrid",
        ParagraphStyle("footer", parent=styles["Normal"],
            fontName="Helvetica", fontSize=7.5, textColor=MUTED,
            leading=10, alignment=TA_CENTER)))

    doc.build(story)
    print(f"PDF written to {OUTPUT}")

build()

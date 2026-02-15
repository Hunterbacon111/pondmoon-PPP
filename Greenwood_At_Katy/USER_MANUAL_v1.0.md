# Pondmoon PPP - Property Planning Panel
# Beta 1.0 User Manual
**Greenwood at Katy Apartment Homes**
**Last Updated: February 2026**

---

## Table of Contents
1. [What is PPP](#1-what-is-ppp)
2. [Quick Start](#2-quick-start)
3. [Login](#3-login)
4. [Cover Page](#4-cover-page)
5. [Tab 1: Leasing Performance](#5-tab-1-leasing-performance)
6. [Tab 2: T-12 Financials](#6-tab-2-t-12-financials)
7. [Tab 3: 2026 Budget](#7-tab-3-2026-budget)
8. [Tab 4: HUD Loan](#8-tab-4-hud-loan)
9. [Tab 5: Market Comps](#9-tab-5-market-comps)
10. [Tab 6: Management Actions](#10-tab-6-management-actions)
11. [Tab 7: Contacts](#11-tab-7-contacts)
12. [How to Update Data](#12-how-to-update-data)
13. [Project File Structure](#13-project-file-structure)
14. [Troubleshooting](#14-troubleshooting)

---

## 1. What is PPP

**Pondmoon PPP (Property Planning Panel)** is a self-contained, single-file HTML dashboard for Greenwood at Katy. It is designed to help Pondmoon's team:

- **Quickly recall the project's current status** across leasing, financials, budget, loan, and market comps
- **Share and present** to colleagues, co-investors (AHC), and partners via a single file
- **Track key management actions** and follow up on strategic decisions

The dashboard is a **static HTML file** (~5MB) that runs entirely in the browser with no server required. All data, images, and charts are embedded. You can open it locally, send it via email, or upload to any file sharing platform.

---

## 2. Quick Start

### Open the Dashboard
```
File location: dashboard/index.html
```
Double-click the file or drag it into any browser (Chrome recommended).

### Rebuild the Dashboard (after updating data)
```bash
cd /Users/fangheli/Downloads/Property_Analysis_Tool_ClaudeCode/Greenwood_At_Katy
source .venv/bin/activate
python build.py
```
This runs two steps:
1. **Extract data** from all source files (Excel, DOCX, PDF) into JSON
2. **Generate** a new `dashboard/index.html` from the template + JSON data

---

## 3. Login

The dashboard is password-protected with a client-side login screen.

| Field    | Value       |
|----------|-------------|
| Username | `pondmoon`  |
| Password | `pondmoon`  |

**Notes:**
- Login is remembered for the current browser tab (via sessionStorage). Refreshing the page in the same tab will stay logged in.
- Opening a **new tab** requires re-login.
- This is client-side protection for basic privacy. It is not meant to be a security barrier.
- The login page displays "Pondmoon PPP / Property Planning Panel" without mentioning the property name for confidentiality.

---

## 4. Cover Page

After login, you see the **Cover Page** with:
- A hero image of the property
- "Pondmoon Real Estate Partners - Property Planning Panel (PPP)"
- **Investment Overview**: Location, acquisition date, total units, rentable SF, year built, HUD loan amount, PM company, and a build timestamp
- Four property photos in a gallery row
- **"Enter Dashboard"** button to enter the main analysis interface

---

## 5. Tab 1: Leasing Performance

**Purpose:** Track weekly occupancy, leasing activity, concessions, and lease expirations.

### KPI Cards (Top)
- Current Occupancy Rate
- Net Leasing Activity (new leases vs move-outs)
- Current Exposure Rate
- Renewal Rate

### Charts
| Chart | Description |
|-------|-------------|
| Occupancy Trend | Weekly occupancy % over time (line chart) |
| Leasing Activity | Weekly new leases, renewals, move-outs, and NTV (bar chart) |

### Tables
| Table | Description |
|-------|-------------|
| Weekly Leasing Metrics | Full weekly data: occupancy, pre-leased, exposure, new leases, renewals, move-outs, NTV counts, delinquency |
| Expiration Matrix | Lease expiration counts by month and unit type, for planning lease-up timing |

### Additional
- **Concession Banner**: Shows current concession strategy (e.g., "6 Weeks Free Off Base Rent")
- **Delinquency Notes**: If any delinquency commentary exists in the weekly reports

**Data Source:** `Data_Leasing/` folder (weekly XLSX + supplemental DOCX updates)

---

## 6. Tab 2: T-12 Financials

**Purpose:** Review trailing 12-month income, expenses, and NOI with year-over-year comparison.

### KPI Cards
- T-12 Total Revenue
- T-12 Total OpEx
- T-12 NOI
- YoY NOI Change (%)

### Charts
| Chart | Description |
|-------|-------------|
| Revenue Trend | Monthly revenue, prior year overlay (line chart) |
| Operating Expenses | Monthly OpEx by category (bar chart) |
| Net Operating Income | Monthly NOI trend (bar chart) |
| Vacancy & Bad Debt | Monthly vacancy + bad debt loss (line chart) |

### AI Financial Q&A Assistant
A built-in chat interface powered by **Claude (Anthropic API)** that can answer questions about the T-12 data in English or Chinese.

**Setup:** Click the gear icon, enter your Anthropic API key (`sk-ant-...`), and save. The key is stored in your browser's localStorage.

**Example questions:**
- "今年T-12 Revenue比去年增加多少？"
- "Which month had the highest NOI?"
- "Operating expenses哪个类别增长最快？"
- "Compare NOI/unit: Greenwood vs Trails"

The assistant has access to all financial data including the companion property (Trails at Katy) for cross-property comparisons.

### T-12 Detail Table
A full-width, scrollable table showing every income and expense line item by month, with totals and per-unit calculations.

**Features:**
- **Cell Comments:** Click any numeric cell to add a note/comment. Comments are saved in localStorage and show a gold triangle indicator. Hover to see the preview; click to edit/delete.
- **Export PDF:** Click the **"Export PDF"** button to print the T-12 table as a landscape PDF report. The export includes a professional header with property name, address, reporting period, and export date.

**Data Source:** `Data_T12P&L/` folder (T-12 Excel statements), `Data_Financials/` for any supplemental data

---

## 7. Tab 3: 2026 Budget

**Purpose:** View the approved 2026 operating budget with monthly breakdowns.

### KPI Cards
- Budgeted Annual Revenue
- Budgeted Annual OpEx
- Budgeted Annual NOI
- Budget DSCR (Debt Service Coverage Ratio)

### Charts
| Chart | Description |
|-------|-------------|
| Budgeted Monthly Income | Monthly budgeted revenue (bar chart) |
| Budgeted OpEx Breakdown | OpEx categories as budgeted (bar chart) |
| Budgeted NOI vs Debt Service | Monthly NOI compared to debt service obligations (combo chart) |
| Budgeted Occupancy Targets | Monthly occupancy targets (line chart) |

### Budget Detail Table
Full line-item budget by month, same format as the T-12 table. Also supports cell comments.

**Data Source:** `Data_Annual_Budget/` folder (XLSB budget file)

---

## 8. Tab 4: HUD Loan

**Purpose:** Understand the HUD loan structure, amortization, and debt service obligations.

### Headline Banner
Quick summary: $49.3M HUD Loan @ 3.18% Fixed, origination date, maturity date, current balance.

### KPI Cards
- Current Balance
- Remaining Term
- Annual Debt Service
- DSCR

### Charts
| Chart | Description |
|-------|-------------|
| Loan Balance Over Time | Remaining balance projection over the full loan term (area chart) |
| Principal vs Interest Split | How each payment splits between P&I over time (stacked area) |
| Annual Debt Service Breakdown | Donut chart of interest, principal, MIP, admin fees |
| Monthly Debt Service Components | Monthly breakdown bar chart |

### Amortization Schedule Table
Year-by-year amortization showing beginning balance, principal, interest, ending balance, and cumulative interest paid.

**Data Source:** `Data_HUDLoan/` and loan parameters in `src/config.py`

---

## 9. Tab 5: Market Comps

**Purpose:** Compare Greenwood at Katy against 9 competitor properties in the Katy/West Houston submarket.

### KPI Cards
- GWK Avg Rent/SF
- Comp Avg Rent/SF
- GWK vs Comp Premium/Discount
- Avg Competitor Exposure Rate

### Concession Banner
Shows Greenwood's current concession offering.

### Charts
| Chart | Description |
|-------|-------------|
| Rent/SF by Unit Type | GWK vs comp average for 1BR, 2BR, 3BR (grouped bar chart) |
| Competitor Exposure Rate | Exposure % for each competitor (horizontal bar chart) |

### Tables
| Table | Description |
|-------|-------------|
| GWK Floor Plan Pricing | All 10 floor plans with market rent, rent/SF, essential vs market designation |
| Competitor Rent/SF & Concessions | All 9 comps with exposure rate, rent/SF by type, and concession details |

### Property Locations Map
Interactive **Google Maps** showing all 10 properties (Greenwood + 9 comps) with:
- **Gold marker + label** for Greenwood at Katy (with star)
- **Navy markers + labels** for each competitor
- Labels are always visible (speech-bubble style, no need to click)
- Map supports zoom, pan, and fullscreen

**Competitor Properties:**
1. Lakecrest Apartments — 1944 Katy Fort Bend Rd
2. The Maddox — 1330 Park West Green Dr
3. Bellrock Market Station — 24002 Colonial Pkwy
4. Luxe at Katy — 22631 Colonial Pkwy
5. Premier at Katy — 24117 Bella Dolce Ln
6. The Oak at Katy Park — 24720 Morton Ranch Rd
7. Katy Ranch Apartments — 24929 Katy Ranch Rd
8. Marquis at Katy — 2150 Katy Fort Bend Rd
9. Lenox at Katy Crossing — 23414 W Fernhurst Dr

**Data Source:** Hardcoded in `src/extractors/comps.py` (from Marketing Presentation, Feb 2026)

---

## 10. Tab 6: Management Actions

**Purpose:** Track decisions, action items, and strategic priorities from weekly calls, emails, and plans.

### Top Goal Banner
Displays the current priority target (e.g., "60-Day Property Goal: Achieve 94.8% Occupancy").

### Strategy Summary Cards
Six strategic categories, each with a summary and item count:
| Category | What it covers |
|----------|---------------|
| Concession | Free weeks, renewal offers, pricing strategies |
| Marketing | Ad spend, ILS platforms, campaign effectiveness |
| Personnel | Leasing team staffing, hiring, incentive programs |
| Renovation | Landscaping, courtyard, exterior improvements, broadband |
| Refinance | Any refinancing discussions (HUD loan) |
| Sale | Disposition or exit planning |

### Actions Table
Filterable list of all action items with:
- Date, source, action description, responsible party, status
- Filter buttons by source: All / Weekly Call / Email / Action Plan
- Each action is color-coded by strategic category

### Add Action Item
Manual input to add new action items directly in the dashboard. Enter the action text and responsible person, then click "+ Add".

### AI Document Parser
Upload meeting minutes, emails, or action plans (`.docx`, `.pdf`, `.txt`, `.eml`) and the AI will automatically extract action items. Review extracted items before adding them to the table.

**Note:** Adding actions or uploading documents modifies only the in-browser version. These changes are stored in localStorage and will persist across page refreshes but are not saved back to the source files.

**Data Source:** `Data_Minutes/` (meeting minutes DOCX), `Data_Marketing_Others/` (email DOCX, action plan PDF)

---

## 11. Tab 7: Contacts

**Purpose:** Maintain a directory of key contacts grouped by company.

### Features
- **Contact Cards** grouped by company: Greystar, AHC, Pondmoon, and any custom companies
- Each card shows: Name, Email, Phone, Role
- **Add Contact:** Fill in name, email, phone, role and click "+ Add Contact"
- **AI Role Detection:** When entering an email, the system auto-detects the company domain and suggests a role
- **Batch Import:** Paste multiple contacts at once in "Name, Email, Phone, Role" format
- **Delete Contact:** Click the X on any contact card to remove

**Note:** Contact changes are saved in localStorage (browser-level persistence).

---

## 12. How to Update Data

### Updating Source Data Files

Place new/updated files in the corresponding `Data_*` folders:

| Data Type | Folder | Expected File Format |
|-----------|--------|---------------------|
| Leasing weekly reports | `Data_Leasing/` | `.xlsx` (primary) + `.docx` (supplemental) |
| T-12 financial statements | `Data_T12P&L/` | `.xlsx` (12-month P&L statements) |
| Annual budget | `Data_Annual_Budget/` | `.xlsb` (Greenwood budget workbook) |
| Meeting minutes | `Data_Minutes/` | `.docx` (one file per meeting) |
| Emails/Action plans | `Data_Marketing_Others/` | `.docx` (emails), `.pdf` (action plans) |
| Market comps | `src/extractors/comps.py` | Edit Python file directly (hardcoded data) |
| Property photos | `Data_Project Information/` | `.jpg`/`.png` images |

### Rebuild After Updating

```bash
cd /Users/fangheli/Downloads/Property_Analysis_Tool_ClaudeCode/Greenwood_At_Katy
source .venv/bin/activate
python build.py
```

The build process:
1. Runs 8 extractors that parse all source files into JSON (`data_output/*.json`)
2. Reads the HTML template (`templates/dashboard_template.html`)
3. Injects all JSON data + base64 images into the template
4. Outputs the final `dashboard/index.html`

### Updating Comps Data
Market comp data is hardcoded in `src/extractors/comps.py`. To update:
1. Edit the `COMPETITOR_COMPS` list (name, address, lat/lng, exposure, rent_by_type, concession)
2. Edit `GWK_FLOOR_PLANS` for Greenwood's pricing
3. Edit `GWK_CONCESSION` for the current concession strategy
4. Run `python build.py`

---

## 13. Project File Structure

```
Greenwood_At_Katy/
├── build.py                      # Main build script (run this!)
├── dashboard/
│   └── index.html                # The generated dashboard (output)
├── templates/
│   └── dashboard_template.html   # HTML template with Chart.js, CSS, JS
├── src/
│   ├── config.py                 # Property info, file paths, constants
│   ├── build_data.py             # Orchestrates all extractors
│   ├── build_html.py             # Injects JSON into HTML template
│   └── extractors/
│       ├── leasing.py            # Parses weekly leasing XLSX + DOCX
│       ├── financials.py         # Parses T-12 P&L Excel files
│       ├── budget.py             # Parses annual budget XLSB
│       ├── comps.py              # Market comp data (hardcoded)
│       ├── loan_info.py          # HUD loan parameters + amortization
│       ├── minutes.py            # Parses meeting minutes DOCX
│       ├── emails.py             # Parses email communications DOCX
│       ├── action_plan.py        # Parses action plan PDF
│       └── companions.py         # Parses companion property T-12s (Trails)
├── data_output/                  # Intermediate JSON files (auto-generated)
│   ├── property_info.json
│   ├── leasing_weekly.json
│   ├── financials_monthly.json
│   ├── budget_monthly.json
│   ├── loan_info.json
│   ├── comps.json
│   ├── actions_log.json
│   ├── companions.json
│   └── images_b64.json
├── Data_Leasing/                 # Source: weekly leasing reports
├── Data_T12P&L/                  # Source: T-12 financial statements
├── Data_Annual_Budget/           # Source: annual budget workbook
├── Data_Minutes/                 # Source: meeting minutes
├── Data_Marketing_Others/        # Source: emails, action plans
├── Data_Comps/                   # Source: comp survey data
├── Data_HUDLoan/                 # Source: HUD loan documents
├── Data_Project Information/     # Source: property photos, docs
└── .venv/                        # Python virtual environment
```

---

## 14. Troubleshooting

### Dashboard shows old data after updating files
Make sure to run the full build:
```bash
source .venv/bin/activate
python build.py          # Correct!
# NOT: python -m src.build_html  (this does NOT execute the build)
```

### Google Maps not loading
- The map requires an internet connection (loads Google Maps API from CDN)
- If the API key expires, update it in `templates/dashboard_template.html` (line 11)

### AI Q&A not working
- You need to provide a valid Anthropic API key (click the gear icon in the T-12 tab)
- The key is stored per-browser in localStorage

### Cell comments disappeared
- Comments are stored in browser localStorage. If you clear browser data or switch browsers, comments are lost.
- Same applies to manually added actions and contacts.

### PDF export is blank
- Make sure you're on the T-12 Financials tab when clicking "Export PDF"
- Use Chrome or Edge for best results (Safari may have print CSS differences)

### Login page not appearing
- If you've already logged in on the same tab, sessionStorage persists the login
- Open a new tab to get the login prompt again
- Or clear sessionStorage: DevTools (F12) → Application → Session Storage → Clear

---

*Built by Pondmoon Real Estate Partners with Claude Code*
*Beta 1.0 - February 2026*

# Pondmoon PPP - New Property Onboarding Checklist
# (Based on Greenwood at Katy v1.0 Architecture)

---

## How to Use This Checklist

When starting a new property's PPP, provide the items below to Claude. Items are organized by priority — **Tier 1 is essential** (dashboard won't work without it), **Tier 2 is important** (specific tabs won't populate), **Tier 3 is nice-to-have** (enables advanced features).

---

## Tier 1: Essential Property Information

### 1A. Property Profile (Tell Claude These Facts)

| Item | Example (Greenwood) | Notes |
|------|---------------------|-------|
| Property Name | Greenwood at Katy | Display name on dashboard |
| Full Address | 1700 Katy Fort Bend Rd, Katy, TX 77493 | |
| City / State | Katy, Texas | |
| Year Built | 2022 | |
| Total Units | 324 | Used in per-unit calculations everywhere |
| Total Rentable SF | 310,836 | |
| Average Unit SF | 959 | |
| Site Size (acres) | 14.54 | |
| Construction Type | Three-Story Garden-Style | |
| Unit Mix | 1BR, 2BR, 3BR (50% affordable) | |
| Parking Spaces | 483 | |
| Tax Status | 100% Exempt (HCHA) | Or normal tax status |
| PM Company | Greystar | Who manages it |
| Community Manager | Name | On-site manager |
| Investors / Owners | Pondmoon, AHC (Allen Harrison) | All parties involved |

### 1B. Property Photos (4 Images)

| Item | Format | Purpose |
|------|--------|---------|
| Hero photo (exterior) | JPG/PNG | Cover page hero image |
| Photo 2 | JPG/PNG | Cover page gallery |
| Photo 3 | JPG/PNG | Cover page gallery |
| Photo 4 | JPG/PNG | Cover page gallery |

Place in: `Data_Project Information/`

---

## Tier 2: Tab-Specific Data Files

### 2A. T-12 Financials (Required for Financials Tab)

| Item | Format | Notes |
|------|--------|-------|
| **Current T-12 Statement** | `.xlsx` | 12-month P&L, e.g. "Property 12 Month Statement - Sept 2025.xlsx" |
| **Prior Year T-12** (optional) | `.xlsx` | Enables YoY comparison charts |

Place in: `Data_T12P&L/`

**Critical:** These Excel files must follow this structure:
- Row 3: Period string (e.g., "Period = Oct 2024-Sep 2025")
- Row 5: Month labels (columns C through N)
- Row 6+: Data rows with Account Code (col A), Label (col B), Monthly values (cols C-N), Annual total (col O)

**I need to know:** What property management system generates these T-12s? (Yardi, RealPage, Entrata, AppFolio, etc.) The account code format varies by system, and I need to map the codes correctly.

---

### 2B. Annual Budget (Required for Budget Tab)

| Item | Format | Notes |
|------|--------|-------|
| **Annual Operating Budget** | `.xlsb` or `.xlsx` | Budget workbook with "Budget Summary" tab |

Place in: `Data_Annual_Budget/`

**I need to know:** What year is the budget for? And does the budget file have a "Budget Summary" tab with monthly columns?

---

### 2C. Weekly Leasing Reports (Required for Leasing Tab)

| Item | Format | Notes |
|------|--------|-------|
| **Weekly Leasing Tracker** | `.xlsx` | Main weekly tracking spreadsheet (Greystar/PM format) |
| **Weekly Update Memos** (optional) | `.docx` | Supplemental narrative reports |

Place in: `Data_Leasing/`

**I need to know:** What does the weekly leasing spreadsheet look like? Is it a Greystar tracker, or a different PM system's format? The row layout (occupancy, leased %, move-ins, move-outs, etc.) is critical.

---

### 2D. Loan Information (Required for HUD Loan Tab)

| Item | Example | Notes |
|------|---------|-------|
| Loan Amount | $49,316,000 | Original loan amount |
| Interest Rate | 3.18% | Fixed rate |
| Loan Type | HUD / FHA 221(d)(4) | Or conventional, bridge, etc. |
| Origination Date | 10/1/2020 | |
| Maturity Date | 9/1/2062 | |
| Current Balance | $46,078,893 | As of most recent date |
| Annual Debt Service | Interest, Principal, MIP, Admin fees | If available from budget |

**If HUD loan:** Does the budget file contain a "Budget Detail" tab with debt service line items (interest, principal, MIP, admin)?

**If NOT HUD:** What type of loan? (Conventional, bridge, Fannie, Freddie) — I'll adjust the loan tab accordingly.

---

### 2E. Market Comps (Required for Comps Tab)

| Item | Format | Notes |
|------|--------|-------|
| **Subject Property Floor Plans** | Any format | Plan name, unit type, SF, market rent, rent/SF |
| **Current Concession** | Text | e.g., "6 Weeks Free Off Base Rent" |
| **Competitor Properties** | Any format (Excel, PDF, or text) | For each comp: name, address, exposure %, rent/SF by type, concession |

Provide for each competitor (typically 5-10 properties):
1. Property Name
2. Address
3. Exposure Rate (%)
4. Rent per SF by unit type (1BR, 2BR, 3BR)
5. Current concession offering

**I will geocode all addresses for the Google Map.**

---

### 2F. Meeting Minutes / Action Items (Required for Actions Tab)

| Item | Format | Notes |
|------|--------|-------|
| **Meeting Minutes** | `.docx` | Weekly call notes, investor meeting notes |
| **Email Communications** | `.docx` | Key decision emails (copy-paste into Word) |
| **Action Plans** | `.pdf` | Strategic plans from PM or consultants |

Place in: `Data_Minutes/` and `Data_Marketing_Others/`

**I need to know:** Are your meeting minutes in Chinese, English, or mixed? What's the typical section structure?

---

## Tier 3: Advanced / Optional

### 3A. Companion Properties (for Cross-Property Comparison)

If you want AI to compare this property against your other holdings:

| Item | Format | Notes |
|------|--------|-------|
| Companion Property T-12s | `.xlsx` | Same format as primary T-12 |
| Companion Property Name & Units | Text | Property name, total units, total SF |

Place in: `Data_T12P&L/Other Comps/[PropertyName]/`

### 3B. AI Features

| Item | Notes |
|------|-------|
| Anthropic API Key | For the T-12 Q&A chatbot (optional, can add later) |
| Google Maps API Key | For the interactive comp map (reuse existing key if available) |

### 3C. Custom Login Credentials

| Item | Default |
|------|---------|
| Username | `pondmoon` |
| Password | `pondmoon` |

Tell me if you want different credentials for the new property.

---

## What Claude Will Handle Automatically

Once you provide the above materials, Claude will:

1. Create the project directory structure (clone from Greenwood template)
2. Update `config.py` with all property-specific information
3. Adapt all 8 extractors to match the new property's data format
4. Map account codes to the new PM system's chart of accounts
5. Hardcode comp data and floor plan pricing
6. Geocode all competitor addresses for the map
7. Generate base64-encoded property images
8. Build and deliver the final `dashboard/index.html`

---

## Known Architecture Assumptions to Watch For

These things WILL need code changes if the new property is different from Greenwood:

| Assumption | Greenwood Specifics | What Could Be Different |
|------------|--------------------|-----------------------|
| PM System | Greystar (AHC format) | Yardi, RealPage, Entrata = different account codes, different Excel layouts |
| Budget Format | XLSB with "Budget Summary" tab | Could be XLSX, different tab names, different column layout |
| T-12 Account Codes | 5-digit dash format (41000-000) | Varies by PM system |
| Loan Type | HUD 221(d)(4) | Conventional, bridge, Fannie Mae, Freddie Mac = different amortization logic |
| Meeting Minutes | Chinese + English, Pondmoon section structure | Different language, different structure |
| Leasing Report | Greystar weekly tracker format | Different PM = different row layout |
| Tax Status | 100% exempt | Most properties pay taxes = need tax line items |

---

## Quick Start Conversation Template

When you're ready to start a new property, just tell Claude:

> "I want to create a new PPP for [Property Name]. Here are the details: [provide Tier 1 info]. I'll drop the data files into the folders. The PM system is [Greystar/Yardi/etc]. The loan is [HUD/conventional/etc]."

Claude will then:
1. Ask for any missing Tier 1 items
2. Set up the project structure
3. Guide you through Tier 2 data preparation
4. Build the dashboard

---

*Template Version 1.0 — Based on Greenwood at Katy PPP Architecture*
*February 2026*

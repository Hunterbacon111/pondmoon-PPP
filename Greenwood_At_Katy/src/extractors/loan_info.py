"""
Extract HUD Loan information from config, budget detail tab, and OM.
Computes amortization schedule and key metrics.
Reads actual debt service breakdown from Budget Detail (rows 1595-1635).
"""
import os
import glob
import math
from datetime import datetime, date
from pyxlsb import open_workbook
from src.config import PROPERTY, DATA_BUDGET, BUDGET_MONTH_COLS


def _read_budget_debt_detail():
    """Read debt service line items from Budget Detail tab of XLSB file.

    Returns dict with monthly arrays for:
      interest, principal, mip, admin_fee
    """
    # Find the XLSB file (may be in subdirectory)
    pattern = os.path.join(DATA_BUDGET, "**", "*.xlsb")
    matches = [f for f in glob.glob(pattern, recursive=True) if not os.path.basename(f).startswith("~")]
    xlsb_file = matches[0] if matches else None

    if not xlsb_file:
        print("  [loan] No XLSB budget file found")
        return None

    # GL code -> field name mapping
    gl_map = {
        "82010-000": "interest",       # Interest Expense - 1st Mortgage
        "82090-000": "principal",       # Principal Reduction - 1st Mortgage
        "82130-000": "mip",            # Mortgage Insurance Premium
        "82221-000": "admin_fee",      # Administration Fees
    }

    result = {k: [None] * 12 for k in gl_map.values()}

    with open_workbook(xlsb_file) as wb:
        sheet_names = wb.sheets
        # Find Budget Detail tab
        detail_sheet = None
        for sn in sheet_names:
            if "detail" in sn.lower() and "budget" in sn.lower():
                detail_sheet = sn
                break
        if not detail_sheet:
            # Try other common names
            for sn in sheet_names:
                if "detail" in sn.lower():
                    detail_sheet = sn
                    break

        if not detail_sheet:
            print("  [loan] No Budget Detail sheet found")
            return None

        print(f"  [loan] Reading debt service from: {detail_sheet}")

        with wb.get_sheet(detail_sheet) as sheet:
            for row_idx, row in enumerate(sheet.rows()):
                if row_idx < 1594 or row_idx > 1640:
                    continue
                cells = [c.v for c in row]

                # Check GL code in col 9
                gl_code = str(cells[9]).strip() if len(cells) > 9 and cells[9] else ""
                if gl_code in gl_map:
                    field = gl_map[gl_code]
                    desc = cells[10] if len(cells) > 10 else ""
                    # Read monthly values from cols 11-22
                    for mi, col_idx in enumerate(BUDGET_MONTH_COLS):
                        if col_idx < len(cells) and cells[col_idx] is not None:
                            result[field][mi] = round(cells[col_idx], 2)
                    print(f"  [loan]   {gl_code}: {desc} -> annual ${sum(v or 0 for v in result[field]):,.0f}")

    return result


def extract():
    """Build comprehensive HUD loan data dict."""

    # --- Core loan terms from config ---
    original_amount = PROPERTY["loan_amount"]  # 49,316,000
    annual_rate = PROPERTY["loan_rate"]        # 0.0318
    monthly_rate = annual_rate / 12
    origination = datetime.strptime(PROPERTY["loan_origination"], "%Y-%m-%d").date()
    maturity = datetime.strptime(PROPERTY["loan_maturity"], "%Y-%m-%d").date()

    # Total months
    total_months = (maturity.year - origination.year) * 12 + (maturity.month - origination.month)

    # Monthly P&I payment (fixed-rate fully amortizing)
    monthly_pi = original_amount * (monthly_rate * (1 + monthly_rate) ** total_months) / \
                 ((1 + monthly_rate) ** total_months - 1)

    # --- Read actual 2026 budget breakdown ---
    budget_detail = _read_budget_debt_detail()

    # 2026 monthly breakdown from budget
    ds_2026_monthly = None
    if budget_detail:
        ds_2026_monthly = {
            "interest": budget_detail["interest"],
            "principal": budget_detail["principal"],
            "mip": budget_detail["mip"],
            "admin_fee": budget_detail["admin_fee"],
        }
        # Calculate totals
        annual_interest_2026 = sum(v or 0 for v in budget_detail["interest"])
        annual_principal_2026 = sum(v or 0 for v in budget_detail["principal"])
        annual_mip_2026 = sum(v or 0 for v in budget_detail["mip"])
        annual_admin_2026 = sum(v or 0 for v in budget_detail["admin_fee"])
        annual_total_ds_2026 = annual_interest_2026 + annual_principal_2026 + annual_mip_2026 + annual_admin_2026
    else:
        # Fallback to hardcoded totals
        annual_interest_2026 = 0
        annual_principal_2026 = 0
        annual_mip_2026 = 116_208
        annual_admin_2026 = 64_889
        annual_total_ds_2026 = 2_305_875

    # --- Build amortization snapshots ---
    balance = original_amount
    year_interest = 0.0
    year_principal = 0.0

    # User-provided: end of 2025 balance = $46,078,893
    user_eoy2025_balance = 46_078_893
    user_annual_interest_2025 = 1_580_506
    user_annual_principal_2025 = 636_597

    amort_by_year = {}

    for m in range(total_months):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_pi - interest_payment
        balance -= principal_payment
        year_interest += interest_payment
        year_principal += principal_payment

        # Figure out what year this payment belongs to
        pay_month = origination.month + m + 1
        pay_year = origination.year + (pay_month - 1) // 12
        pay_month_in_year = ((pay_month - 1) % 12) + 1

        if pay_month_in_year == 12 or m == total_months - 1:
            amort_by_year[pay_year] = {
                "year": pay_year,
                "ending_balance": round(max(balance, 0), 0),
                "interest_paid": round(year_interest, 0),
                "principal_paid": round(year_principal, 0),
                "total_paid": round(year_interest + year_principal, 0),
            }
            year_interest = 0.0
            year_principal = 0.0

    # Use user-provided values for end of 2025
    eoy2025_balance = user_eoy2025_balance

    # Override 2026 from budget detail if available
    if budget_detail:
        amort_by_year[2026] = {
            "year": 2026,
            "ending_balance": round(eoy2025_balance - annual_principal_2026, 0),
            "interest_paid": round(annual_interest_2026, 0),
            "principal_paid": round(annual_principal_2026, 0),
            "total_paid": round(annual_interest_2026 + annual_principal_2026, 0),
        }

    # Remaining term from Jan 2026
    months_elapsed_to_2026 = (2026 - origination.year) * 12 + (1 - origination.month)
    remaining_months = total_months - months_elapsed_to_2026
    remaining_years = remaining_months / 12

    # Build amort table for display (select years)
    display_years = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030,
                     2035, 2040, 2045, 2050, 2055, 2060, 2062]
    amort_table = []
    for y in display_years:
        if y in amort_by_year:
            entry = dict(amort_by_year[y])
            if y == 2025:
                entry = {
                    "year": 2025,
                    "ending_balance": eoy2025_balance,
                    "interest_paid": user_annual_interest_2025,
                    "principal_paid": user_annual_principal_2025,
                    "total_paid": user_annual_interest_2025 + user_annual_principal_2025,
                }
            amort_table.append(entry)

    # Balance trend for chart
    balance_trend = []
    for y in range(2020, 2063):
        if y in amort_by_year:
            bal = amort_by_year[y]["ending_balance"]
            if y == 2025:
                bal = eoy2025_balance
            balance_trend.append({"year": y, "balance": bal})

    # Interest vs principal split
    interest_principal_split = []
    for y in range(2021, 2063):
        if y in amort_by_year:
            entry = amort_by_year[y]
            if y == 2025:
                interest_principal_split.append({
                    "year": y, "interest": user_annual_interest_2025,
                    "principal": user_annual_principal_2025,
                })
            else:
                interest_principal_split.append({
                    "year": y, "interest": entry["interest_paid"],
                    "principal": entry["principal_paid"],
                })

    # --- Debt service component breakdown for 2026 ---
    ds_components_2026 = {
        "interest": round(annual_interest_2026, 0),
        "principal": round(annual_principal_2026, 0),
        "mip": round(annual_mip_2026, 0),
        "admin_fee": round(annual_admin_2026, 0),
        "total": round(annual_total_ds_2026, 0),
    }

    # Budget NOI for DSCR
    budget_noi_2026 = 4_121_512
    dscr_2026 = round(budget_noi_2026 / annual_total_ds_2026, 2) if annual_total_ds_2026 > 0 else 0

    loan_data = {
        # Core terms
        "loan_type": "HUD / FHA Section 221(d)(4)",
        "original_amount": original_amount,
        "interest_rate": annual_rate,
        "interest_rate_pct": f"{annual_rate * 100:.2f}%",
        "origination_date": PROPERTY["loan_origination"],
        "maturity_date": PROPERTY["loan_maturity"],
        "total_term_months": total_months,
        "total_term_years": round(total_months / 12, 1),
        "monthly_pi_payment": round(monthly_pi, 2),
        "annual_pi_payment": round(monthly_pi * 12, 2),

        # Current status (as of end 2025)
        "as_of_date": "2025-12-31",
        "current_balance": eoy2025_balance,
        "annual_interest_2025": user_annual_interest_2025,
        "annual_principal_2025": user_annual_principal_2025,
        "principal_paid_to_date": round(original_amount - eoy2025_balance, 0),
        "pct_paid_down": round((original_amount - eoy2025_balance) / original_amount * 100, 1),
        "remaining_months": remaining_months,
        "remaining_years": round(remaining_years, 1),

        # 2026 Debt Service breakdown (from Budget Detail)
        "ds_components_2026": ds_components_2026,
        "ds_2026_monthly": ds_2026_monthly,

        # HUD-specific features
        "hud_features": [
            {"label": "Loan Program", "value": "FHA Section 221(d)(4)"},
            {"label": "Rate Type", "value": "Fixed Rate (3.18%)"},
            {"label": "Amortization", "value": f"Fully amortizing, {round(total_months/12, 0):.0f}-year term"},
            {"label": "Guarantee", "value": "Guaranteed by AHC (Allen Harrison Company)"},
            {"label": "Assumable", "value": "Yes (subject to HUD/FHA approval)"},
            {"label": "Property Tax", "value": "100% Exempt (HCHA Redevelopment Authority)"},
            {"label": "Tax Exemption Expiry", "value": "At loan maturity (Sep 2062)"},
            {"label": "MIP (Mortgage Insurance)", "value": f"${annual_mip_2026:,.0f}/yr (${round(annual_mip_2026/12):,.0f}/mo)"},
            {"label": "Administration Fee", "value": f"${annual_admin_2026:,.0f}/yr (${round(annual_admin_2026/12):,.0f}/mo)"},
            {"label": "Replacement Reserves", "value": "HUD-required; funded via monthly escrow"},
            {"label": "Prepayment", "value": "Lockout period + declining penalty schedule (HUD standard)"},
        ],

        # Budget debt service totals
        "budget_annual_debt_service_2026": round(annual_total_ds_2026, 0),
        "budget_monthly_debt_service_2026": round(annual_total_ds_2026 / 12, 0),
        "debt_service_vs_pi_gap": round(annual_total_ds_2026 - monthly_pi * 12, 0),

        # DSCR
        "budget_noi_2026": budget_noi_2026,
        "dscr_2026": dscr_2026,

        # Amortization table
        "amort_table": amort_table,

        # Chart data
        "balance_trend": balance_trend,
        "interest_principal_split": interest_principal_split,
    }

    return loan_data

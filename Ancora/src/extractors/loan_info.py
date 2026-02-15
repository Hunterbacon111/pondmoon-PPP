"""Extract SBLIC Construction Loan information for Ancora.

Unlike Greenwood's HUD fixed-rate fully-amortizing loan, Ancora has a
floating-rate construction loan from Security Benefit Life Insurance Company.

Key differences:
- Floating rate: SOFR + 4.50% (floor 3.50%)
- 48-month term + 12-month extension
- Interest-only (no amortization during construction)
- 100% NOI cash sweep after stabilization
- Construction loan, not permanent financing
"""
from src.config import PROPERTY
from datetime import datetime


def extract():
    """Build comprehensive SBLIC construction loan data dict."""

    # Core loan terms
    loan_amount = PROPERTY["loan_amount"]  # $73,000,000
    spread = PROPERTY["loan_rate_spread"]  # 4.50%
    sofr_floor = PROPERTY["sofr_floor"]    # 3.50%

    # Current SOFR estimate (as of Feb 2026)
    # Using approximate SOFR rate
    current_sofr = 0.043  # ~4.30% (approximate)
    effective_sofr = max(current_sofr, sofr_floor)
    current_rate = effective_sofr + spread  # ~8.80%

    # Monthly interest (interest-only)
    monthly_interest = loan_amount * current_rate / 12
    annual_interest = loan_amount * current_rate

    # Loan timeline
    origination_date = PROPERTY["loan_origination"]  # 2023-09-21
    term_months = PROPERTY["loan_term_months"]  # 48
    extension_months = PROPERTY["loan_extension_months"]  # 12

    # Calculate maturity dates
    orig = datetime.strptime(origination_date, "%Y-%m-%d")
    initial_maturity_year = orig.year + (orig.month + term_months - 1) // 12
    initial_maturity_month = ((orig.month + term_months - 1) % 12) + 1
    initial_maturity = f"{initial_maturity_year}-{initial_maturity_month:02d}-{orig.day:02d}"

    extended_maturity_year = initial_maturity_year + (initial_maturity_month + extension_months - 1) // 12
    extended_maturity_month = ((initial_maturity_month + extension_months - 1) % 12) + 1
    extended_maturity = f"{extended_maturity_year}-{extended_maturity_month:02d}-{orig.day:02d}"

    # Months elapsed & remaining
    now = datetime(2026, 2, 1)
    months_elapsed = (now.year - orig.year) * 12 + (now.month - orig.month)
    months_remaining_initial = term_months - months_elapsed
    months_remaining_extended = term_months + extension_months - months_elapsed

    # Project cost & equity structure
    total_project_cost = PROPERTY["total_project_cost"]
    total_equity = PROPERTY["total_equity"]

    # Interest reserve analysis (from budget)
    interest_reserve_initial = 3050000
    # Budget shows IR depleted by June 2026
    ir_depletion_month = "June 2026"
    additional_funding_needed = 2374790  # from budget analysis

    # Fees
    origination_fee = loan_amount * 0.015  # 1.50%
    exit_fee = loan_amount * 0.0075  # 0.75%
    extension_fee = loan_amount * 0.0025  # 0.25%

    # Recourse
    recourse_amount = 11500000
    recourse_burnoff = "50% leased at 8% debt yield"

    # DSCR is not applicable during interest-only construction phase
    # But we can show projected stabilized DSCR
    stabilized_noi = PROPERTY["stabilized_noi"]  # $7,001,930
    projected_dscr = round(stabilized_noi / annual_interest, 2) if annual_interest > 0 else 0

    # Monthly interest schedule (12 months of 2026)
    # Rate may vary with SOFR changes, but we use current estimate
    monthly_interest_schedule = [round(monthly_interest, 2)] * 12

    # Build interest rate scenarios
    rate_scenarios = []
    for sofr_rate in [0.035, 0.040, 0.045, 0.050, 0.055]:
        eff_sofr = max(sofr_rate, sofr_floor)
        rate = eff_sofr + spread
        mo_interest = loan_amount * rate / 12
        ann_interest = loan_amount * rate
        rate_scenarios.append({
            "sofr": round(sofr_rate * 100, 2),
            "all_in_rate": round(rate * 100, 2),
            "monthly_interest": round(mo_interest, 0),
            "annual_interest": round(ann_interest, 0),
        })

    loan_data = {
        # Core terms
        "loan_type": "SBLIC Construction Loan",
        "lender": "Security Benefit Life Insurance Company",
        "original_amount": loan_amount,
        "interest_rate_structure": f"SOFR + {spread*100:.2f}%",
        "sofr_floor": f"{sofr_floor*100:.2f}%",
        "current_sofr_estimate": round(current_sofr * 100, 2),
        "current_all_in_rate": round(current_rate * 100, 2),
        "origination_date": origination_date,
        "initial_maturity_date": initial_maturity,
        "extended_maturity_date": extended_maturity,
        "term_months": term_months,
        "extension_months": extension_months,
        "amortization": "Interest-Only (construction phase)",

        # Current status
        "as_of_date": "2026-02-01",
        "current_balance": loan_amount,  # No principal paydown on IO loan
        "months_elapsed": months_elapsed,
        "months_remaining_initial": months_remaining_initial,
        "months_remaining_extended": months_remaining_extended,

        # Monthly/Annual interest
        "monthly_interest_estimate": round(monthly_interest, 0),
        "annual_interest_estimate": round(annual_interest, 0),
        "monthly_interest_schedule": monthly_interest_schedule,

        # Interest rate scenarios
        "rate_scenarios": rate_scenarios,

        # Interest reserve
        "interest_reserve_initial": interest_reserve_initial,
        "ir_depletion_month": ir_depletion_month,
        "additional_funding_needed": additional_funding_needed,

        # Fees
        "fees": {
            "origination": {"pct": "1.50%", "amount": round(origination_fee, 0)},
            "exit": {"pct": "0.75%", "amount": round(exit_fee, 0)},
            "extension": {"pct": "0.25%", "amount": round(extension_fee, 0)},
            "admin_agent": {"quarterly": 25000, "annual": 100000},
            "prepayment_multiple": "1.10x (if before month 36)",
        },

        # LTV / LTC constraints
        "max_ltv": f"{PROPERTY['loan_ltv_max']*100:.0f}%",
        "max_ltc": f"{PROPERTY['loan_ltc_max']*100:.0f}%",
        "actual_ltc": round(loan_amount / total_project_cost * 100, 1),

        # Recourse
        "recourse_amount": recourse_amount,
        "recourse_burnoff_condition": recourse_burnoff,
        "guarantor": "Greystar Real Estate Partners, LLC",

        # Capital structure
        "total_project_cost": total_project_cost,
        "total_equity": total_equity,
        "equity_breakdown": {
            "pondmoon": {"amount": PROPERTY["pondmoon_equity"], "pct": f"{PROPERTY['pondmoon_equity_pct']*100:.0f}%"},
            "greystar": {"amount": PROPERTY["greystar_equity"], "pct": f"{PROPERTY['greystar_equity_pct']*100:.0f}%"},
            "land_seller": {"amount": PROPERTY["land_equity"], "pct": f"{PROPERTY['land_equity_pct']*100:.0f}%"},
        },

        # Projected stabilized metrics
        "stabilized_noi": stabilized_noi,
        "projected_dscr_stabilized": projected_dscr,

        # Extension conditions
        "extension_conditions": [
            "No existing Events of Default",
            "LTV does not exceed 60% (as-stabilized appraisal)",
            "Debt yield of 8% based on 6 months collected rents",
            "Current in all interest/fee payments",
        ],

        # Key loan features
        "loan_features": [
            {"label": "Loan Program", "value": "SBLIC Construction Loan"},
            {"label": "Rate Type", "value": f"Floating: SOFR + 4.50% (Floor: 3.50%)"},
            {"label": "Current Est. Rate", "value": f"{current_rate*100:.2f}%"},
            {"label": "Amortization", "value": "Interest-Only; 100% NOI sweep post-stabilization"},
            {"label": "Guarantor", "value": "Greystar Real Estate Partners, LLC"},
            {"label": "Max LTV", "value": f"{PROPERTY['loan_ltv_max']*100:.0f}%"},
            {"label": "Max LTC", "value": f"{PROPERTY['loan_ltc_max']*100:.0f}%"},
            {"label": "Recourse", "value": f"${recourse_amount:,} (burns off at 50% leased + 8% DY)"},
            {"label": "Origination Fee", "value": f"1.50% (${origination_fee:,.0f})"},
            {"label": "Exit Fee", "value": f"0.75% (${exit_fee:,.0f})"},
            {"label": "Extension Fee", "value": f"0.25% (${extension_fee:,.0f})"},
            {"label": "Prepayment", "value": "1.10x multiple if before month 36"},
            {"label": "Interest Reserve", "value": f"${interest_reserve_initial:,} (depleted {ir_depletion_month})"},
            {"label": "Assumption", "value": "1x permitted post-completion; 1.00% fee"},
        ],

        # No amortization table for IO loan, but include balance/rate trend
        "amort_table": [],  # Not applicable for IO loan
        "balance_trend": [{"year": y, "balance": loan_amount} for y in range(2024, 2029)],
        "interest_principal_split": [],  # Not applicable for IO loan
    }

    return loan_data

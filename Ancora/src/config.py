"""Central configuration for Ancora (1st & Beech) property analysis."""
import os

# Project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Property metadata
PROPERTY = {
    "name": "Ancora",
    "full_name": "Ancora (1st & Beech Residential)",
    "address": "110 Beech St, San Diego, CA 92101",
    "city": "San Diego",
    "state": "California",
    "neighborhood": "Little Italy",
    "year_built": 2025,
    "total_units": 220,
    "total_sf": 122259,
    "avg_unit_sf": 556,
    "site_acres": 0.23,
    "density_per_acre": 958,
    "construction": "22-Story High-Rise",
    "unit_mix": "Studio, 1BR, 2BR (incl. 6 affordable units at 50% AMI)",
    "parking_spaces": 20,
    "tax_status": "Subject to Ad Valorem Property Taxes",
    # Loan info (SBLIC Construction Loan)
    "loan_amount": 73000000,
    "loan_rate_spread": 0.045,  # SOFR + 4.50%
    "sofr_floor": 0.035,
    "loan_origination": "2023-09-21",
    "loan_term_months": 48,
    "loan_extension_months": 12,
    "loan_type": "SBLIC Construction",
    "loan_ltv_max": 0.60,
    "loan_ltc_max": 0.65,
    # Project cost
    "total_project_cost": 111912289,
    "land_cost": 6500000,
    "hard_costs": 81716803,
    "soft_costs": 16195486,
    "financing_costs": 7500000,
    # Management & investors
    "pm_company": "Greystar",
    "developer": "Greystar Real Estate Partners, LLC",
    "investor_pondmoon": "Pondmoon Capital (Steven Li, Nicole, Patrick)",
    "investor_greystar": "Greystar (GP, 13% equity)",
    "investor_land": "Land Seller LP (7% equity)",
    "pondmoon_equity": 30954726,
    "pondmoon_equity_pct": 0.80,
    "greystar_equity": 3891229,
    "greystar_equity_pct": 0.13,
    "land_equity": 4066334,
    "land_equity_pct": 0.07,
    "total_equity": 38912289,
    # Stabilized projections
    "stabilized_noi": 7001930,
    "stabilized_cap_rate": 0.0425,
    "stabilized_valuation": 148525630,
    "target_exit_date": "2026-Q4",
    "target_irr": 0.2372,
    "target_equity_multiple": 1.80,
    # Key contacts
    "community_manager": "Victoria (Greystar, on-site)",
    "greystar_contacts": "Jerry Brand (EVP), Beau Brand (Sr Director), Jake, Adrian",
}

# Data source directories
DATA_LEASING = os.path.join(PROJECT_ROOT, "Data_Leasing")
DATA_BUDGET = os.path.join(PROJECT_ROOT, "Data_Annual_Budget")
DATA_FINANCIALS = os.path.join(PROJECT_ROOT, "Data_Financials")
DATA_MINUTES = os.path.join(PROJECT_ROOT, "Data_Minutes")
DATA_MARKETING = os.path.join(PROJECT_ROOT, "Data_Marketing_Others")
DATA_PROJECT_INFO = os.path.join(PROJECT_ROOT, "Data_Project Information")
DATA_COMPS = os.path.join(PROJECT_ROOT, "Data_Comps")
DATA_T12 = os.path.join(PROJECT_ROOT, "Data_T12P&L")
DATA_LOAN = os.path.join(PROJECT_ROOT, "Data_Loan")

# No companion properties for Ancora
COMPANION_PROPERTIES = {}

# Output directories
DATA_OUTPUT = os.path.join(PROJECT_ROOT, "data_output")
DASHBOARD_DIR = os.path.join(PROJECT_ROOT, "dashboard")
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "templates")

# Budget Cash Flow Projections - row mapping
# Based on Ancora_Cash Flow Projections_1.23.2026.xlsx, sheet Ext_Capital_Call
# Labels in column C, monthly values in columns F-Q (Jan-Dec 2026), total in R
BUDGET_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Row-to-metric mapping (1-indexed row numbers from the XLSX)
BUDGET_ROW_MAP = {
    # Lease-up metrics
    "move_ins": 15,
    "occupied_units": 16,
    "occupancy_pct": 18,
    "market_rent_per_unit": 19,
    "scheduled_rent_per_unit": 20,
    "concession_pct": 21,
    # Income
    "market_rent": 24,
    "gain_loss_to_lease": 25,
    "potential_rent": 27,
    "concessions": 30,
    "vacancy_loss": 31,
    "non_revenue_units": 32,
    "bad_debt": 33,
    "total_net_rental_income": 36,
    "total_other_income": 38,
    "total_income": 42,
    # Expenses
    "payroll_benefits": 44,
    "repairs_maintenance": 45,
    "make_ready": 47,
    "recreational_amenities": 48,
    "contract_services": 49,
    "marketing": 53,
    "office_expenses": 54,
    "other_admin": 55,
    "utilities": 56,
    "controllable_expenses": 57,
    "management_fees": 59,
    "ground_lease": 60,
    "taxes": 61,
    "insurance": 62,
    "non_controllable_expenses": 64,
    "total_opex": 66,
    # NOI & below the line
    "noi": 68,
    "routine_replacement": 70,
    "noi_after_replacements": 72,
    "other_capital": 74,
    "debt_service": 77,
    "net_income": 81,
    # Cash adjustments
    "re_tax_accrual": 84,
    "insurance_accrual": 85,
    "net_cashflow": 87,
    "property_tax_payment": 88,
    "other_tax_payment": 89,
    "insurance_payment": 90,
    "net_cashflow_adj": 91,
    "operating_deficit_funding": 93,
    "net_cashflow_adj_financing": 95,
    # Reserve / funding
    "cumulative_reserve_advances": 97,
    "interest_reserve_balance": 102,
    "ir_starting_balance": 108,
    "ir_ending_balance": 109,
    "potential_additional_funding": 111,
}

# Column mapping for budget XLSX
# Column F = Jan 2026, ... Column Q = Dec 2026, Column R = Total
BUDGET_DATA_COL_START = 6   # 1-indexed column F
BUDGET_TOTAL_COL = 18       # 1-indexed column R

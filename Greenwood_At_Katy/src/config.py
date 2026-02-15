"""Central configuration for Greenwood at Katy property analysis."""
import os

# Project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Property metadata
PROPERTY = {
    "name": "Greenwood at Katy",
    "address": "1700 Katy Fort Bend Rd, Katy, TX 77493",
    "city": "Katy",
    "state": "Texas",
    "year_built": 2022,
    "total_units": 324,
    "total_sf": 310836,
    "avg_unit_sf": 959,
    "site_acres": 14.54,
    "density_per_acre": 22.3,
    "construction": "Three-Story Garden-Style",
    "unit_mix": "1BR, 2BR, 3BR (50% affordable)",
    "parking_spaces": 483,
    "tax_status": "100% Property Tax Exempt (HCHA)",
    "loan_amount": 49316000,
    "loan_rate": 0.0318,
    "loan_origination": "2020-10-01",
    "loan_maturity": "2062-09-01",
    "loan_type": "HUD",
    "pm_company": "Greystar",
    "investor_pondmoon": "Pondmoon (Steven Li, Nicole)",
    "investor_ahc": "Allen Harrison Company (Meredith)",
    "community_manager": "Danteil Kirkland",
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
DATA_COMPANIONS = os.path.join(DATA_T12, "Other Comps")

# Companion property registry — properties we own/co-invest for cross-comparison
COMPANION_PROPERTIES = {
    "trails": {
        "name": "Trails at City Park",
        "short_name": "Trails",
        "address": "Houston, TX",
        "total_units": 288,
        "total_sf": 278784,
        "data_dir": os.path.join(DATA_T12, "Other Comps", "Trails"),
        "format": "trails",  # parser identifier
    },
}

# Output directories
DATA_OUTPUT = os.path.join(PROJECT_ROOT, "data_output")
DASHBOARD_DIR = os.path.join(PROJECT_ROOT, "dashboard")
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "templates")

# Budget Summary sheet column mapping
# Columns 11-22 = Jan 2026 through Dec 2026
BUDGET_MONTH_COLS = list(range(11, 23))  # indices 11..22
BUDGET_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Budget Summary row-to-label mapping (row index in sheet)
# Discovered from exploration of the XLSB file
BUDGET_ROW_MAP = {
    # Occupancy metrics (rows ~32-34 area)
    "targeted_occupancy": "Targeted End-of-Month Occupancy Pct",
    "financial_occupancy": "Financial Occupancy Pct",
    "economic_occupancy": "Economic Occupancy Pct",
    # Move ins / outs
    "move_ins": "Move Ins",
    "move_outs": "Move Outs",
    "projected_expirations": "Projected Expirations",
    "renewals": "Renewals",
    # Rent metrics
    "net_potential_rent_per_unit": "Net Potential Rent Per Unit",
    "avg_market_rent_per_unit": "Average Market Rent per Unit (All Units)",
    # Income
    "potential_rent": "Potential Rent",
    "net_potential_rent": "Net Potential Rent",
    "vacancy_loss": "Vacancy Loss",
    "non_revenue_units": "Non Revenue Units",
    "bad_debt": "Bad Debt",
    "total_rental_income": "TOTAL RENTAL INCOME-RESIDENTIAL",
    "other_income_residential": "Other Income-Residential",
    "total_income": "TOTAL INCOME",
    # Expenses
    "payroll_benefits": "Payroll & Benefits",
    "repairs_maintenance": "Repairs & Maintenance",
    "make_ready": "Make-Ready / Redecorating",
    "recreational_amenities": "Recreational Amenities",
    "contract_services": "Contract Services",
    "marketing": "Advertising / Marketing / Promotions",
    "office_expenses": "Office Expenses",
    "other_admin": "Other General & Administrative",
    "utilities": "Utilities",
    "controllable_expenses": "CONTROLLABLE EXPENSES",
    "management_fees": "Management Fees",
    "taxes": "Taxes",
    "insurance": "Insurance",
    "non_controllable_expenses": "NON-CONTROLLABLE EXPENSES",
    "total_opex": "TOTAL OPERATING EXPENSES",
    # Below the line
    "routine_replacement": "Routine Replacement Expense",
    "capital_renovation": "Capital / Renovation Expense",
    "noi": "NET OPERATING INCOME",
    "noi_after_replacements": "NOI AFTER REPLACEMENTS",
    "partnership_owner_expenses": "Partnership / Owner Expenses",
    "closing_costs": "Closing Costs",
    "debt_service": "Debt Service",
    "total_non_operating": "TOTAL NON-OPERATING EXPENSE",
    "net_income": "NET INCOME",
}

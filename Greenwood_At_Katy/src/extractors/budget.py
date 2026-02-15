"""Extract budget data from the XLSB Budget Summary tab."""
import os
import glob
from datetime import datetime, timedelta
from pyxlsb import open_workbook
from src.config import DATA_BUDGET, BUDGET_MONTH_COLS, BUDGET_MONTHS, BUDGET_ROW_MAP


def _find_budget_file():
    """Find the most recent budget XLSB file."""
    pattern = os.path.join(DATA_BUDGET, "**", "*.xlsb")
    files = glob.glob(pattern, recursive=True)
    if not files:
        return None
    # Return the most recently modified file
    return max(files, key=os.path.getmtime)


def _parse_value(raw):
    """Parse a cell value into a float, handling percentages and strings."""
    if raw is None:
        return None
    try:
        val = float(raw)
        return val
    except (ValueError, TypeError):
        return None


def _find_label_column(rows_data):
    """Determine which column contains the row labels.

    The Budget Summary sheet uses column 9 or 10 for labels.
    We detect it by looking for known label strings.
    """
    known_labels = {"TOTAL INCOME", "NET OPERATING INCOME", "Potential Rent",
                    "Payroll & Benefits", "TOTAL OPERATING EXPENSES"}
    for col_idx in [9, 10, 8, 7]:
        matches = 0
        for row in rows_data:
            if col_idx < len(row):
                val = row[col_idx]
                if val and str(val).strip() in known_labels:
                    matches += 1
        if matches >= 3:
            return col_idx
    return 10  # default


def extract():
    """Extract monthly budget data from the Budget Summary tab.

    Returns a dict with year, months list, and metrics dict.
    Each metric key maps to a list of 12 monthly values.
    """
    filepath = _find_budget_file()
    if not filepath:
        print("  [budget] No budget file found.")
        return {"year": None, "months": BUDGET_MONTHS, "metrics": {}, "source_file": None}

    print(f"  [budget] Reading: {os.path.basename(filepath)}")

    # Read all rows from Budget Summary
    rows_data = []
    with open_workbook(filepath) as wb:
        with wb.get_sheet("Budget Summary") as sheet:
            for row in sheet.rows():
                cells = [c.v for c in row]
                rows_data.append(cells)

    # Find the label column
    label_col = _find_label_column(rows_data)
    print(f"  [budget] Label column index: {label_col}")

    # Build a label-to-row-index map
    label_to_row = {}
    for row_idx, row in enumerate(rows_data):
        if label_col < len(row) and row[label_col]:
            label_str = str(row[label_col]).strip()
            if label_str:
                label_to_row[label_str] = row_idx

    # Reverse the BUDGET_ROW_MAP: label_string -> metric_key
    label_to_metric = {v: k for k, v in BUDGET_ROW_MAP.items()}

    # Extract monthly values for each metric
    metrics = {}
    for label_str, metric_key in label_to_metric.items():
        if label_str in label_to_row:
            row_idx = label_to_row[label_str]
            row = rows_data[row_idx]
            monthly_vals = []
            for col_idx in BUDGET_MONTH_COLS:
                if col_idx < len(row):
                    monthly_vals.append(_parse_value(row[col_idx]))
                else:
                    monthly_vals.append(None)
            metrics[metric_key] = monthly_vals
        else:
            print(f"  [budget] Warning: label not found: '{label_str}'")
            metrics[metric_key] = [None] * 12

    # Compute annual totals for key metrics
    annual_totals = {}
    for key in ["total_income", "total_opex", "noi", "net_income", "debt_service",
                "payroll_benefits", "marketing", "contract_services", "insurance"]:
        vals = metrics.get(key, [])
        non_null = [v for v in vals if v is not None]
        annual_totals[key] = sum(non_null) if non_null else None

    return {
        "year": 2026,
        "months": BUDGET_MONTHS,
        "metrics": metrics,
        "annual_totals": annual_totals,
        "source_file": os.path.basename(filepath),
    }

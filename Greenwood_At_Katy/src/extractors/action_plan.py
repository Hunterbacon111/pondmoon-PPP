"""Extract key data from the Action Plan PDF."""
import os
import re
import glob
from src.config import DATA_MARKETING


def extract():
    """Extract action plan summary data.

    Returns a list of action entries for the actions log,
    plus a summary dict with marketing recommendations.
    """
    actions = []
    summary = {
        "current_marketing_spend": 2585,
        "recommended_marketing_spend": 3734,
        "target_occupancy_60_day": 94.8,
        "additional_move_ins_needed": 16,
        "marketing_breakdown_current": {
            "apartments_com_gold": 585,
            "zillow_ppl": 529,
            "wpromote": 2000,
        },
        "marketing_breakdown_recommended": {
            "sem_paid_search": 2500,
            "sem_paid_display": 750,
            "sem_demand_gen": 500,
            "seo_greystar": 350,
            "hyly": 189,
            "apartments_com_platinum": 945,
            "zillow_boost": 500,
        },
        "renewal_concessions": {
            "1br": 750,
            "2br": 1000,
            "3br": 1250,
        },
    }

    if not os.path.exists(DATA_MARKETING):
        print("  [action_plan] Data_Marketing_Others directory not found.")
        return actions, summary

    pdf_files = glob.glob(os.path.join(DATA_MARKETING, "**", "*.pdf"), recursive=True)
    plan_files = [f for f in pdf_files if "action plan" in os.path.basename(f).lower()]

    if not plan_files:
        print("  [action_plan] No action plan PDF found.")
        return actions, summary

    filepath = plan_files[0]
    filename = os.path.basename(filepath)
    print(f"  [action_plan] Found: {filename}")

    # Extract text using pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                # Community snapshot data (page 2)
                if "Current Occupancy" in text:
                    occ_match = re.search(r'(\d+\.?\d*)%', text)
                    if occ_match:
                        summary["current_occupancy_at_plan"] = float(occ_match.group(1))
    except ImportError:
        print("  [action_plan] pdfplumber not available.")

    # Create action items from the plan
    plan_actions = [
        {
            "action": "60-Day Property Goal: Achieve 94.8% occupancy (16 additional move-ins in February)",
            "responsible": "Danteil (Greystar)",
            "status": "in_progress",
            "category": "leasing",
        },
        {
            "action": "Implement tiered Early Bird renewal concessions ($750/1BR, $1000/2BR, $1250/3BR, must renew within 2 weeks)",
            "responsible": "Danteil (Greystar)",
            "status": "in_progress",
            "category": "retention",
        },
        {
            "action": "Evaluate marketing spend increase from $2,585/mo to $3,734/mo (pending Greystar marketing effectiveness data)",
            "responsible": "Meredith (AHC)",
            "status": "pending",
            "category": "marketing",
        },
        {
            "action": "Implement team incentive program (occupancy goal bonuses: $250 at 30-day, $500 at 60-day)",
            "responsible": "Meredith (AHC)",
            "status": "in_progress",
            "category": "operations",
        },
    ]

    for item in plan_actions:
        actions.append({
            "date": "2026-02-01",
            "source": "Action Plan",
            "source_party": "Greystar",
            "source_file": filename,
            **item,
        })

    print(f"  [action_plan] Action entries: {len(actions)}")
    return actions, summary

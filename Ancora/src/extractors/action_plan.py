"""Extract action plan summary data for Ancora.

Ancora does not have a standalone Action Plan PDF like Greenwood.
Instead, we synthesize action items from meeting minutes context.
"""
import os
from src.config import DATA_MARKETING


def extract():
    """Extract action plan summary data.

    Returns a list of action entries for the actions log,
    plus a summary dict with key strategies.
    """
    actions = []
    summary = {
        "current_marketing_spend": None,
        "recommended_marketing_spend": None,
        "target_occupancy_stabilized": 95.0,
        "lease_up_velocity_target": 23,  # units/month from Debt Memo
        "marketing_strategies": {
            "el90_email_campaign": {"cost": 700, "reach": 40000, "cost_per_lead": 57},
            "search_engine_marketing": {"monthly_spend": 4976},
            "ils_listing_services": {"monthly_spend": 16090},
            "social_media": {"monthly_spend": 2000},
        },
        "pricing_strategy": "Sticker Shock — lower asking rent, reduce concessions, maintain net effective",
        "current_concession": "10 Weeks Free + $3,000 Look-and-Lease",
    }

    # Synthesized action items from meeting minutes analysis
    plan_actions = [
        {
            "action": "Lease-up Goal: Achieve 95% stabilized occupancy (~210 units) by May 2026",
            "responsible": "Victoria (Greystar)",
            "status": "in_progress",
            "category": "leasing",
        },
        {
            "action": "Implement 'Sticker Shock' pricing strategy: lower asking rent while reducing concessions to maintain net effective rent",
            "responsible": "Victoria (Greystar)",
            "status": "pending",
            "category": "pricing",
        },
        {
            "action": "Deploy EL90 email campaign targeting 40,000 tenants within 15-mile radius (leases expiring within 90 days)",
            "responsible": "Greystar Marketing",
            "status": "in_progress",
            "category": "marketing",
        },
        {
            "action": "Replace Community Manager; new CM to be assigned by Greystar",
            "responsible": "Greystar",
            "status": "in_progress",
            "category": "personnel",
        },
        {
            "action": "Add temporary leasing staff: Adrian (39.5% close rate) for 2 weeks + Jake (ex-Simone regional manager)",
            "responsible": "Greystar",
            "status": "in_progress",
            "category": "personnel",
        },
        {
            "action": "Submit 4P improvement plan (Pricing, Promotion, Product, People) by next Thursday",
            "responsible": "Greystar",
            "status": "pending",
            "category": "strategy",
        },
        {
            "action": "Conduct sensitivity analysis and reverse NOI modeling for exit loan requirements",
            "responsible": "Pondmoon Asset Management",
            "status": "pending",
            "category": "finance",
        },
        {
            "action": "Update HelloData with net effective Price per SF for accurate comp tracking",
            "responsible": "Victoria (Greystar)",
            "status": "pending",
            "category": "marketing",
        },
    ]

    for item in plan_actions:
        actions.append({
            "date": "2026-02-12",
            "source": "Action Plan (from Meeting Minutes)",
            "source_party": "Pondmoon / Greystar",
            "source_file": "Synthesized from meeting minutes",
            **item,
        })

    print(f"  [action_plan] Action entries: {len(actions)}")
    return actions, summary

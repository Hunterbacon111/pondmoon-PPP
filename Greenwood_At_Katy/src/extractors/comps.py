"""Extract comparable property data from marketing presentation + OM baseline."""
from src.config import DATA_COMPS
import os
import glob


# === GWK Floor Plan Pricing (from Marketing Presentation, Feb 2026) ===
GWK_FLOOR_PLANS = [
    {"plan": "Oak",            "type": "1BR", "sf": 722,  "market_rent": 1403.20, "rent_psf": 1.94, "is_essential": False},
    {"plan": "Essential Oak",  "type": "1BR", "sf": 722,  "market_rent": 1286.13, "rent_psf": 1.78, "is_essential": True},
    {"plan": "Elm",            "type": "2BR", "sf": 835,  "market_rent": 1542.08, "rent_psf": 1.84, "is_essential": False},
    {"plan": "Essential Elm",  "type": "2BR", "sf": 835,  "market_rent": 1414.39, "rent_psf": 1.69, "is_essential": True},
    {"plan": "Birch",          "type": "3BR", "sf": 1152, "market_rent": 1853.10, "rent_psf": 1.60, "is_essential": False},
    {"plan": "Essential Birch","type": "3BR", "sf": 1152, "market_rent": 1724.80, "rent_psf": 1.49, "is_essential": True},
    {"plan": "Hazel",          "type": "3BR", "sf": 1228, "market_rent": 1906.61, "rent_psf": 1.55, "is_essential": False},
    {"plan": "Essential Hazel","type": "3BR", "sf": 1228, "market_rent": 1704.58, "rent_psf": 1.38, "is_essential": True},
    {"plan": "Maple",          "type": "3BR", "sf": 1466, "market_rent": 2309.27, "rent_psf": 1.57, "is_essential": False},
    {"plan": "Essential Maple","type": "3BR", "sf": 1466, "market_rent": 1924.50, "rent_psf": 1.31, "is_essential": True},
]

GWK_CONCESSION = "6 Weeks Free Off Base Rent, No Prorate by 3/15"


# === Competitor Comps (from Marketing Presentation, Feb 2026) ===
COMPETITOR_COMPS = [
    {
        "name": "Lakecrest Apartments",
        "address": "1944 Katy Fort Bend Rd, Katy, TX 77493",
        "lat": 29.8004, "lng": -95.8013,
        "exposure": 13.8,
        "rent_by_type": {"1x1": 1.52, "2x2": 1.23},
        "concession": "One Month Free with $99 App and Admin",
    },
    {
        "name": "The Maddox",
        "address": "1330 Park West Green Dr, Katy, TX 77493",
        "lat": 29.7895, "lng": -95.7921,
        "exposure": 9.8,
        "rent_by_type": {"1x1": 1.70, "2x2": 1.59, "3x2": 1.51},
        "concession": "8 Weeks Free with $500 LNL",
    },
    {
        "name": "Bellrock Market Station",
        "address": "24002 Colonial Pkwy, Katy, TX 77493",
        "lat": 29.7917, "lng": -95.7912,
        "exposure": 17.3,
        "rent_by_type": {"1x1": 1.60, "2x2": 1.44, "3x2": 1.60},
        "concession": "6 Weeks Free with $500 GC on Select Units",
    },
    {
        "name": "Luxe at Katy",
        "address": "22631 Colonial Pkwy, Katy, TX 77449",
        "lat": 29.7929, "lng": -95.7636,
        "exposure": 6.5,
        "rent_by_type": {"1x1": 1.48, "2x2": 1.27},
        "concession": "Reduced Rental Rates",
    },
    {
        "name": "Premier at Katy",
        "address": "24117 Bella Dolce Ln, Katy, TX 77494",
        "lat": 29.7825, "lng": -95.7879,
        "exposure": 6.5,
        "rent_by_type": {"1x1": 1.64, "2x2": 1.49},
        "concession": "2 Weeks Free, Reduced Rates on Select Units, $99 App and Admin",
    },
    {
        "name": "The Oak at Katy Park",
        "address": "24720 Morton Ranch Rd, Katy, TX 77493",
        "lat": 29.8187, "lng": -95.8022,
        "exposure": 11.5,
        "rent_by_type": {"1x1": 2.10, "2x2": 1.81, "3x2": 1.74},
        "concession": "8 Weeks Free on Select Units",
    },
    {
        "name": "Katy Ranch Apartments",
        "address": "24929 Katy Ranch Rd, Katy, TX 77494",
        "lat": 29.7820, "lng": -95.7950,
        "exposure": 11.5,
        "rent_by_type": {"1x1": 1.67, "2x2": 1.45, "3x1": 1.32},
        "concession": "One Month Free if Move In within 30 Days",
    },
    {
        "name": "Marquis at Katy",
        "address": "2150 Katy Fort Bend Rd, Katy, TX 77493",
        "lat": 29.8036, "lng": -95.8020,
        "exposure": 10.9,
        "rent_by_type": {"1x1": 1.41, "2x2": 1.42, "3x2": 1.39},
        "concession": "6 Weeks Free on All Floorplans",
    },
    {
        "name": "Lenox at Katy Crossing",
        "address": "23414 W Fernhurst Dr, Katy, TX 77494",
        "lat": 29.7778, "lng": -95.7806,
        "exposure": 17.1,
        "rent_by_type": {"1x1": 2.01, "2x2": 1.83, "3x2": 1.63},
        "concession": "8 Weeks Free with $750 Gift Card if Move In by 2/15",
    },
]


def extract():
    """Extract comparable property data from marketing presentation."""

    print("  [comps] Using marketing presentation comps (Feb 2026)")

    # --- GWK averages by unit type ---
    gwk_by_type = {}
    for fp in GWK_FLOOR_PLANS:
        t = fp["type"]
        if t not in gwk_by_type:
            gwk_by_type[t] = {"plans": [], "total_rent": 0, "total_psf": 0, "count": 0}
        gwk_by_type[t]["plans"].append(fp)
        gwk_by_type[t]["total_rent"] += fp["market_rent"]
        gwk_by_type[t]["total_psf"] += fp["rent_psf"]
        gwk_by_type[t]["count"] += 1

    gwk_type_avg = {}
    for t, data in gwk_by_type.items():
        gwk_type_avg[t] = {
            "avg_rent": round(data["total_rent"] / data["count"], 2),
            "avg_psf": round(data["total_psf"] / data["count"], 2),
        }

    # --- Competitor averages ---
    all_1x1 = [c["rent_by_type"]["1x1"] for c in COMPETITOR_COMPS if "1x1" in c["rent_by_type"]]
    all_2x2 = [c["rent_by_type"].get("2x2", c["rent_by_type"].get("2x1")) for c in COMPETITOR_COMPS if "2x2" in c["rent_by_type"] or "2x1" in c["rent_by_type"]]
    all_3x = []
    for c in COMPETITOR_COMPS:
        for k, v in c["rent_by_type"].items():
            if k.startswith("3"):
                all_3x.append(v)

    comp_avg = {
        "1x1": round(sum(all_1x1) / len(all_1x1), 2) if all_1x1 else None,
        "2x2": round(sum(all_2x2) / len(all_2x2), 2) if all_2x2 else None,
        "3x": round(sum(all_3x) / len(all_3x), 2) if all_3x else None,
    }

    avg_exposure = round(sum(c["exposure"] for c in COMPETITOR_COMPS) / len(COMPETITOR_COMPS), 1)

    return {
        "source": "Marketing Presentation (Feb 2026)",
        "gwk_floor_plans": GWK_FLOOR_PLANS,
        "gwk_concession": GWK_CONCESSION,
        "gwk_type_avg": gwk_type_avg,
        "competitors": COMPETITOR_COMPS,
        "comp_averages": comp_avg,
        "avg_exposure": avg_exposure,
    }

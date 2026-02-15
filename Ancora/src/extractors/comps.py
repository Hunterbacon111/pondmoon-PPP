"""Extract comparable property data for Ancora (Little Italy, San Diego).

Data sourced from Ancora Comps 2.12.2026.pdf and Debt Memo.
"""
from src.config import DATA_COMPS
import os


# === Ancora Floor Plans (from Debt Memo, 220 units) ===
ANCORA_FLOOR_PLANS = [
    # Market Rate Studios (109 units, ~50%)
    {"plan": "A1/S", "type": "Studio", "sf": 483, "units": 57, "market_rent": 2715, "rent_psf": 5.62, "is_affordable": False},
    {"plan": "A2/S", "type": "Studio", "sf": 408, "units": 16, "market_rent": 2605, "rent_psf": 6.38, "is_affordable": False},
    {"plan": "A3/S", "type": "Studio", "sf": 491, "units": 20, "market_rent": 2780, "rent_psf": 5.66, "is_affordable": False},
    {"plan": "A4/S", "type": "Studio", "sf": 486, "units": 16, "market_rent": 2770, "rent_psf": 5.70, "is_affordable": False},
    # Market Rate 1BR (65 units, ~30%)
    {"plan": "B1/1BR", "type": "1BR", "sf": 576, "units": 20, "market_rent": 3592, "rent_psf": 6.24, "is_affordable": False},
    {"plan": "B2/1BR", "type": "1BR", "sf": 638, "units": 17, "market_rent": 3697, "rent_psf": 5.79, "is_affordable": False},
    {"plan": "B3/1BR", "type": "1BR", "sf": 586, "units": 14, "market_rent": 3607, "rent_psf": 6.16, "is_affordable": False},
    {"plan": "B4/1BR", "type": "1BR", "sf": 538, "units": 14, "market_rent": 3570, "rent_psf": 6.64, "is_affordable": False},
    # Market Rate 2BR (26 units, ~12%)
    {"plan": "C1/2BR", "type": "2BR", "sf": 816, "units": 20, "market_rent": 4650, "rent_psf": 5.70, "is_affordable": False},
    {"plan": "C2/2BR", "type": "2BR", "sf": 917, "units": 3, "market_rent": 4800, "rent_psf": 5.23, "is_affordable": False},
    {"plan": "C3/2BR", "type": "2BR", "sf": 863, "units": 3, "market_rent": 4700, "rent_psf": 5.45, "is_affordable": False},
    # Affordable Units (6 units, 2.7% at 50% AMI — reduced via negotiation)
    {"plan": "Affordable", "type": "Affordable", "sf": 500, "units": 6, "market_rent": 1296, "rent_psf": 2.59, "is_affordable": True},
]

ANCORA_CONCESSION = "10 Weeks Free + $3,000 Look-and-Lease (if move in by 1/31)"


# === Competitor Comps (from Ancora Comps 2.12.2026.pdf) ===
COMPETITOR_COMPS = [
    {
        "name": "Luma",
        "address": "1400 Columbia St, San Diego, CA 92101",
        "lat": 32.7218, "lng": -117.1648,
        "total_units": 220,
        "avg_sf": 920,
        "vintage": 2019,
        "occupancy": 96,
        "exposure": 4.0,
        "manager": "Lennar",
        "product_type": "High Rise",
        "avg_rent": 4784,
        "rent_psf": 5.20,
        "rent_by_type": {
            "Studio": {"rent": 3141, "psf": 5.65, "sf": 556},
            "1BR": {"rent": 4135, "psf": 5.26, "sf": 786},
            "2BR": {"rent": 6383, "psf": 5.15, "sf": 1228},
        },
        "concession": "N/A",
    },
    {
        "name": "Hanover Little Italy",
        "address": "310 A St, San Diego, CA 92101",
        "lat": 32.7195, "lng": -117.1687,
        "total_units": 270,
        "avg_sf": 838,
        "vintage": 2021,
        "occupancy": 91,
        "exposure": 9.0,
        "manager": "Hanover",
        "product_type": "Mid Rise",
        "avg_rent": 3853,
        "rent_psf": 4.60,
        "rent_by_type": {
            "Studio": {"rent": 2800, "psf": 5.00, "sf": 560},
            "1BR": {"rent": 3500, "psf": 4.50, "sf": 778},
            "2BR": {"rent": 5200, "psf": 4.30, "sf": 1209},
        },
        "concession": "1 Month Free",
    },
    {
        "name": "525 Olive",
        "address": "525 Olive St, San Diego, CA 92101",
        "lat": 32.7210, "lng": -117.1640,
        "total_units": 204,
        "avg_sf": 957,
        "vintage": 2022,
        "occupancy": 94,
        "exposure": 6.0,
        "manager": "Hanover",
        "product_type": "High Rise",
        "avg_rent": 5850,
        "rent_psf": 6.11,
        "rent_by_type": {
            "Studio": {"rent": 3500, "psf": 6.25, "sf": 560},
            "1BR": {"rent": 5000, "psf": 6.10, "sf": 820},
            "2BR": {"rent": 7800, "psf": 6.00, "sf": 1300},
        },
        "concession": "Reduced Rates on Select",
    },
    {
        "name": "Simone",
        "address": "1401 Union Street, San Diego, CA 92101",
        "lat": 32.7240, "lng": -117.1642,
        "total_units": 395,
        "avg_sf": 804,
        "vintage": 2023,
        "occupancy": None,  # Pre-Leasing
        "exposure": None,
        "manager": "Greystar",
        "product_type": "High Rise",
        "avg_rent": 4739,
        "rent_psf": 5.93,
        "rent_by_type": {
            "Studio": {"rent": 3123, "psf": 6.35, "sf": 492},
            "1BR": {"rent": 3900, "psf": 5.57, "sf": 700},
            "2BR": {"rent": 6550, "psf": 5.90, "sf": 1110},
        },
        "concession": "Extra 2 Weeks Free; Parking Discounts",
    },
]


def extract():
    """Extract comparable property data."""
    print("  [comps] Using comps from Ancora Comps 2.12.2026.pdf + Debt Memo")

    # Ancora averages by unit type (market rate only)
    ancora_by_type = {}
    for fp in ANCORA_FLOOR_PLANS:
        if fp["is_affordable"]:
            continue
        t = fp["type"]
        if t not in ancora_by_type:
            ancora_by_type[t] = {"plans": [], "total_rent": 0, "total_psf": 0,
                                 "total_units": 0, "total_sf": 0, "count": 0}
        ancora_by_type[t]["plans"].append(fp)
        ancora_by_type[t]["total_rent"] += fp["market_rent"] * fp["units"]
        ancora_by_type[t]["total_psf"] += fp["rent_psf"] * fp["units"]
        ancora_by_type[t]["total_units"] += fp["units"]
        ancora_by_type[t]["total_sf"] += fp["sf"] * fp["units"]
        ancora_by_type[t]["count"] += fp["units"]

    ancora_type_avg = {}
    for t, data in ancora_by_type.items():
        ancora_type_avg[t] = {
            "avg_rent": round(data["total_rent"] / data["count"], 2),
            "avg_psf": round(data["total_psf"] / data["count"], 2),
            "avg_sf": round(data["total_sf"] / data["count"], 0),
            "total_units": data["total_units"],
        }

    # Competitor averages
    comp_avg_by_type = {}
    for comp in COMPETITOR_COMPS:
        for unit_type, type_data in comp["rent_by_type"].items():
            if unit_type not in comp_avg_by_type:
                comp_avg_by_type[unit_type] = {"rents": [], "psfs": [], "sfs": []}
            comp_avg_by_type[unit_type]["rents"].append(type_data["rent"])
            comp_avg_by_type[unit_type]["psfs"].append(type_data["psf"])
            comp_avg_by_type[unit_type]["sfs"].append(type_data["sf"])

    comp_type_avg = {}
    for t, data in comp_avg_by_type.items():
        comp_type_avg[t] = {
            "avg_rent": round(sum(data["rents"]) / len(data["rents"]), 0),
            "avg_psf": round(sum(data["psfs"]) / len(data["psfs"]), 2),
            "avg_sf": round(sum(data["sfs"]) / len(data["sfs"]), 0),
        }

    # Rent comparison: Ancora vs comps
    rent_comparison = {}
    for t in ancora_type_avg:
        if t in comp_type_avg:
            rent_comparison[t] = {
                "ancora_rent": ancora_type_avg[t]["avg_rent"],
                "ancora_psf": ancora_type_avg[t]["avg_psf"],
                "comp_rent": comp_type_avg[t]["avg_rent"],
                "comp_psf": comp_type_avg[t]["avg_psf"],
                "rent_diff": round(ancora_type_avg[t]["avg_rent"] - comp_type_avg[t]["avg_rent"], 0),
                "psf_pct_of_comp": round(ancora_type_avg[t]["avg_psf"] / comp_type_avg[t]["avg_psf"] * 100, 0),
            }

    avg_comp_occupancy = []
    avg_comp_exposure = []
    for c in COMPETITOR_COMPS:
        if c["occupancy"] is not None:
            avg_comp_occupancy.append(c["occupancy"])
        if c.get("exposure") is not None:
            avg_comp_exposure.append(c["exposure"])
    avg_occ = round(sum(avg_comp_occupancy) / len(avg_comp_occupancy), 1) if avg_comp_occupancy else None
    avg_exp = round(sum(avg_comp_exposure) / len(avg_comp_exposure), 1) if avg_comp_exposure else 0

    # Flat comp_averages map (PSF only) for template compatibility
    # Template expects keys like 'Studio', '1x1', '2x2'
    comp_averages = {}
    for t, data in comp_avg_by_type.items():
        avg_psf = round(sum(data["psfs"]) / len(data["psfs"]), 2)
        comp_averages[t] = avg_psf
        # Also add Greenwood-style keys for compatibility
        if t == "1BR":
            comp_averages["1x1"] = avg_psf
        elif t == "2BR":
            comp_averages["2x2"] = avg_psf

    return {
        "source": "Ancora Comps 2.12.2026.pdf + Debt Memo",
        "anc_floor_plans": ANCORA_FLOOR_PLANS,
        "anc_concession": ANCORA_CONCESSION,
        "anc_type_avg": ancora_type_avg,
        "competitors": COMPETITOR_COMPS,
        "comp_type_avg": comp_type_avg,
        "comp_averages": comp_averages,
        "rent_comparison": rent_comparison,
        "avg_comp_occupancy": avg_occ,
        "avg_exposure": avg_exp,
    }

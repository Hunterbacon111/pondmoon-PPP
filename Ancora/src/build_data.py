"""Orchestrate all data extractors and write JSON output files."""
import json
import os
import re
from src.config import DATA_OUTPUT, PROPERTY


def write_json(filepath, data):
    """Write data to a JSON file with pretty formatting."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  -> Wrote: {os.path.basename(filepath)}")


def _build_strategy_summary(actions, ap_summary):
    """Categorize all actions into strategic summary buckets.

    Categories:
    - Concession: free weeks, loss leaders, renewal offers
    - Marketing: ad spend, ILS, campaigns, EL90
    - Personnel: staffing, leasing team, hiring, CM replacement
    - Renovation: make-ready, improvements (minimal for new build)
    - Refinance: loan, refinancing, exit debt
    - Sale: disposition, sale, exit
    """
    categories = {
        "Concession": {
            "icon": "C",
            "keywords": [r"concession", r"free", r"loss leader", r"renewal.*offer",
                         r"incentiv", r"price", r"pricing", r"sticker shock",
                         r"rent.*(?:reduc|adjust|lower)", r"net effective",
                         r"move[- ]?in", r"look.and.lease", r"激励"],
            "items": [],
        },
        "Marketing": {
            "icon": "M",
            "keywords": [r"market(?:ing)?", r"advertis", r"ILS", r"campaign",
                         r"EL90", r"email.*campaign", r"HelloData", r"SEM",
                         r"social media", r"lead", r"outreach",
                         r"营销", r"定价"],
            "items": [],
        },
        "Personnel": {
            "icon": "P",
            "keywords": [r"leasing.*(?:team|member|agent|staff)", r"staff",
                         r"hiring", r"headcount", r"employee", r"CM",
                         r"community manager", r"Adrian", r"Jake", r"Victoria",
                         r"人手", r"人员", r"replace.*manager",
                         r"4P.*plan"],
            "items": [],
        },
        "Renovation": {
            "icon": "R",
            "keywords": [r"renovati", r"improvement", r"make[- ]?ready",
                         r"construction", r"TCO", r"capital",
                         r"amenity", r"pool", r"lounge",
                         r"工程", r"改造"],
            "items": [],
        },
        "Refinance": {
            "icon": "F",
            "keywords": [r"refinanc", r"loan", r"debt.*(?:restructur|yield|service)",
                         r"sensitivity.*analysis", r"NOI.*model",
                         r"interest reserve", r"exit.*loan"],
            "items": [],
        },
        "Sale": {
            "icon": "S",
            "keywords": [r"dispositi", r"\bsale\b", r"sell", r"exit(?!.*loan)"],
            "items": [],
        },
    }

    for action in actions:
        text = action.get("action", "")
        if text.startswith("[Concern]"):
            action["sentiment"] = "concern"
        elif text.startswith("[Positive]"):
            action["sentiment"] = "positive"
        matched_cats = []
        for cat_name, cat in categories.items():
            for kw in cat["keywords"]:
                if re.search(kw, text, re.IGNORECASE):
                    matched_cats.append(cat_name)
                    break
        if matched_cats:
            action["strategy_category"] = matched_cats[0]
        for cat_name in matched_cats:
            categories[cat_name]["items"].append({
                "text": text[:200],
                "source": action.get("source", ""),
                "status": action.get("status", ""),
                "responsible": action.get("responsible", ""),
            })

    always_show = {"Concession", "Marketing", "Personnel", "Renovation", "Refinance", "Sale"}
    result = []
    for cat_name, cat in categories.items():
        if cat["items"] or cat_name in always_show:
            summary = _summarize_category(cat_name, cat["items"], ap_summary)
            result.append({
                "category": cat_name,
                "icon": cat["icon"],
                "summary": summary,
                "count": len(cat["items"]),
                "items": cat["items"],
            })

    return result


def _summarize_category(cat_name, items, ap_summary):
    """Generate a concise summary for each strategy category."""
    if cat_name == "Concession":
        if not items:
            return "No current concession action items."
        parts = []
        for it in items:
            t = it["text"].lower()
            if "10 week" in t or "free" in t:
                parts.append("10 weeks free + $3,000 look-and-lease")
            if "sticker shock" in t or "lower asking" in t:
                parts.append("'Sticker Shock' pricing strategy under review")
            if "net effective" in t:
                parts.append("Maintain net effective rent while adjusting asking price")
        if parts:
            return "; ".join(list(dict.fromkeys(parts))) + "."
        return f"{len(items)} action(s) related to concessions and pricing."

    elif cat_name == "Marketing":
        if not items:
            return "No current marketing action items."
        parts = []
        for it in items:
            t = it["text"].lower()
            if "el90" in t:
                parts.append("EL90 email campaign: $700 for 40,000 targeted tenants")
            if "ils" in t or "listing" in t:
                parts.append("ILS spend at $16K/mo")
            if "hellodata" in t:
                parts.append("Updating HelloData with net effective PSF")
        if parts:
            return "; ".join(list(dict.fromkeys(parts))) + "."
        return f"{len(items)} marketing-related action(s)."

    elif cat_name == "Personnel":
        if not items:
            return "No current personnel action items."
        parts = []
        for it in items:
            t = it["text"].lower()
            if "replace" in t or "cm" in t or "community manager" in t:
                parts.append("Replacing Community Manager")
            if "adrian" in t:
                parts.append("Adrian (39.5% close rate) deployed for 2 weeks")
            if "jake" in t:
                parts.append("Jake (ex-Simone regional manager) on site")
            if "4p" in t:
                parts.append("4P improvement plan (Pricing, Promotion, Product, People)")
        if parts:
            return "; ".join(list(dict.fromkeys(parts))) + "."
        return f"{len(items)} personnel-related action(s)."

    elif cat_name == "Renovation":
        if not items:
            return "New construction (2025). No renovation needed."
        return f"{len(items)} renovation-related action(s)."

    elif cat_name == "Refinance":
        if not items:
            return "SBLIC construction loan at SOFR+4.50%. Interest reserve depleted by June 2026."
        parts = []
        for it in items:
            t = it["text"].lower()
            if "sensitivity" in t or "noi" in t:
                parts.append("Sensitivity analysis & reverse NOI modeling for exit loan")
            if "interest reserve" in t:
                parts.append("Interest reserve tracking ($3.05M, depleted by June 2026)")
        if parts:
            return "; ".join(list(dict.fromkeys(parts))) + "."
        return f"{len(items)} refinancing-related action(s)."

    elif cat_name == "Sale":
        if not items:
            return "Target exit Q4 2026 at ~$148.5M (4.25% cap). Projected 1.80x equity multiple."
        return f"{len(items)} disposition-related action(s)."

    return f"{len(items)} action(s)."


def extract_all():
    """Run all extractors and write output JSON files."""
    from src.extractors import leasing, budget, financials, minutes, emails, action_plan, comps, loan_info, companions

    # 1. Property info (static)
    print("\n[1/8] Property Info...")
    write_json(os.path.join(DATA_OUTPUT, "property_info.json"), PROPERTY)

    # 2. Budget
    print("\n[2/8] Budget Data...")
    budget_data = budget.extract()
    write_json(os.path.join(DATA_OUTPUT, "budget_monthly.json"), budget_data)

    # 3. Leasing
    print("\n[3/8] Leasing Data...")
    leasing_data = leasing.extract()
    write_json(os.path.join(DATA_OUTPUT, "leasing_weekly.json"), leasing_data)

    # 4. Financial Actuals
    print("\n[4/8] Financial Actuals...")
    financials_data = financials.extract()
    write_json(os.path.join(DATA_OUTPUT, "financials_monthly.json"), financials_data)

    # 5. Actions Log (combined from minutes, emails, action plan)
    print("\n[5/8] Actions Log...")
    all_actions = []

    minutes_actions = minutes.extract()
    all_actions.extend(minutes_actions)

    email_actions = emails.extract()
    all_actions.extend(email_actions)

    ap_actions, ap_summary = action_plan.extract()
    all_actions.extend(ap_actions)

    # Sort by date
    all_actions.sort(key=lambda a: a.get("date", ""))

    # Build strategy summary
    strategy_summary = _build_strategy_summary(all_actions, ap_summary)

    # Top-level property goal
    top_goal = {
        "goal": "Lease-Up Goal: Achieve 95% Stabilized Occupancy (~210 units)",
        "target_value": 95.0,
        "metric": "occupancy_pct",
        "date_set": "2026-02-10",
        "deadline": "November 2026",
        "source": "Meeting Minutes (Feb 10, 2026)",
    }

    actions_data = {
        "actions": all_actions,
        "action_plan_summary": ap_summary,
        "strategy_summary": strategy_summary,
        "top_goal": top_goal,
    }
    write_json(os.path.join(DATA_OUTPUT, "actions_log.json"), actions_data)

    # 6. Comps
    print("\n[6/8] Comparable Properties...")
    comps_data = comps.extract()
    write_json(os.path.join(DATA_OUTPUT, "comps.json"), comps_data)

    # 7. Loan Info
    print("\n[7/8] Loan Info...")
    loan_data = loan_info.extract()
    write_json(os.path.join(DATA_OUTPUT, "loan_info.json"), loan_data)

    # 8. Companion Properties
    print("\n[8/8] Companion Properties...")
    companion_data = companions.extract()
    write_json(os.path.join(DATA_OUTPUT, "companions.json"), companion_data)

    # 9. Images (encode property photos as base64)
    print("\n[Bonus] Property Images...")
    _encode_images()

    print(f"\nAll data extracted to {DATA_OUTPUT}/")


def _encode_images():
    """Encode selected property photos as base64 for embedding in dashboard."""
    import base64
    import glob as glob_mod
    from src.config import DATA_PROJECT_INFO, DATA_OUTPUT

    images_dir = os.path.join(DATA_PROJECT_INFO, "web res")
    if not os.path.exists(images_dir):
        print("  [images] No web res directory found.")
        write_json(os.path.join(DATA_OUTPUT, "images_b64.json"), {})
        return

    jpg_files = sorted(glob_mod.glob(os.path.join(images_dir, "*.jpg")))
    if not jpg_files:
        jpg_files = sorted(glob_mod.glob(os.path.join(images_dir, "*.JPG")))

    if not jpg_files:
        print("  [images] No JPG files found.")
        write_json(os.path.join(DATA_OUTPUT, "images_b64.json"), {})
        return

    # Select up to 5 representative images (spread evenly)
    n = len(jpg_files)
    if n <= 5:
        selected = jpg_files
    else:
        # Pick evenly spaced images
        indices = [0, n // 4, n // 2, 3 * n // 4, n - 1]
        selected = [jpg_files[i] for i in indices]

    images_data = {}
    for i, filepath in enumerate(selected):
        with open(filepath, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        key = f"property_{i + 1}"
        images_data[key] = f"data:image/jpeg;base64,{b64}"
        print(f"  [images] Encoded: {os.path.basename(filepath)} -> {key}")

    # Use a specific atmospheric photo for login background
    login_bg_file = os.path.join(images_dir, "I64A1832-Edit-2.jpg")
    if os.path.exists(login_bg_file):
        with open(login_bg_file, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        images_data["login_bg"] = f"data:image/jpeg;base64,{b64}"
        print(f"  [images] Encoded: I64A1832-Edit-2.jpg -> login_bg (golden lounge)")
    elif "property_1" in images_data:
        images_data["login_bg"] = images_data["property_1"]

    write_json(os.path.join(DATA_OUTPUT, "images_b64.json"), images_data)
    print(f"  [images] Total images encoded: {len(images_data)}")

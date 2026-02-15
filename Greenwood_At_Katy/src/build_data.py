"""Orchestrate all data extractors and write JSON output files."""
import json
import os
from src.config import DATA_OUTPUT, PROPERTY


def write_json(filepath, data):
    """Write data to a JSON file with pretty formatting."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  -> Wrote: {os.path.basename(filepath)}")


import re


def _build_strategy_summary(actions, ap_summary):
    """Categorize all actions into strategic summary buckets.

    Categories:
    - Concession: free weeks, loss leaders, renewal offers
    - Marketing: ad spend, apartment.com, ILS, campaigns
    - Personnel: staffing, leasing team, hiring
    - Renovation: make-ready, landscaping, courtyard, improvements
    - Refinance: loan, refinancing (only if present)
    - Sale: disposition, sale (only if present)
    """
    categories = {
        "Concession": {
            "icon": "C",
            "keywords": [r"concession", r"free", r"loss leader", r"renewal.*offer",
                         r"renewal.*concession", r"renewal.*increase", r"incentiv",
                         r"price increase", r"NTV", r"occupancy.*goal",
                         r"move[- ]?in", r"激励", r"奖金"],
            "items": [],
        },
        "Marketing": {
            "icon": "M",
            "keywords": [r"market(?:ing)?", r"advertis", r"apartment\.com",
                         r"ILS", r"campaign", r"marketing spend",
                         r"营销", r"定价"],
            "items": [],
        },
        "Personnel": {
            "icon": "P",
            "keywords": [r"part[- ]?time", r"leasing.*(?:team|member|agent)",
                         r"staff", r"hiring", r"headcount", r"employee",
                         r"人手", r"人员", r"高层.*(?:会议|通话|机制)",
                         r"闭门会议"],
            "items": [],
        },
        "Renovation": {
            "icon": "R",
            "keywords": [r"renovati", r"landscap", r"courtyard", r"院落",
                         r"improvement", r"make[- ]?ready", r"工程", r"改造",
                         r"宽带", r"broadband", r"comcast", r"capital",
                         r"exterior", r"value engineer"],
            "items": [],
        },
        "Refinance": {
            "icon": "F",
            "keywords": [r"refinanc", r"loan", r"debt.*restructur"],
            "items": [],
        },
        "Sale": {
            "icon": "S",
            "keywords": [r"dispositi", r"\bsale\b", r"sell", r"exit"],
            "items": [],
        },
    }

    for action in actions:
        text = action.get("action", "")
        # Tag sentiment: [Concern] or [Positive]
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
        # Tag the action with its primary category (first match)
        if matched_cats:
            action["strategy_category"] = matched_cats[0]
        # Add to all matched category buckets
        for cat_name in matched_cats:
            categories[cat_name]["items"].append({
                "text": text[:200],
                "source": action.get("source", ""),
                "status": action.get("status", ""),
                "responsible": action.get("responsible", ""),
            })

    # Build output — always show all 6 strategic categories
    always_show = {"Concession", "Marketing", "Personnel", "Renovation", "Refinance", "Sale"}
    result = []
    for cat_name, cat in categories.items():
        if cat["items"] or cat_name in always_show:
            # Create a concise summary sentence for each category
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
        texts = " | ".join(set(it["text"][:100] for it in items[:4]))
        # Try to extract key numbers
        parts = []
        for it in items:
            t = it["text"].lower()
            if "6 week" in t or "free" in t:
                parts.append("6 weeks free on all units")
            if "loss leader" in t:
                parts.append("Loss leaders approved (new batch of 10)")
            if "renewal" in t and ("increase" in t or "offer" in t or "concession" in t):
                parts.append("Renewal offers with small increases")
        if parts:
            return "; ".join(list(dict.fromkeys(parts))) + "."
        return f"{len(items)} action(s) related to concessions and pricing."

    elif cat_name == "Marketing":
        if not items:
            return "No current marketing action items."
        parts = []
        for it in items:
            t = it["text"].lower()
            if "hold off" in t or "hold" in t:
                parts.append("Marketing spend increase on hold pending results")
            elif "increase" in t and "marketing" in t:
                parts.append("Evaluating spend increase ($2,585 → $3,734/mo)")
            elif "campaign" in t or "apartment.com" in t:
                parts.append("Reviewing ILS/platform effectiveness")
            elif "营销" in t or "marketing" in t:
                parts.append("Marketing plan under review")
        if parts:
            return "; ".join(list(dict.fromkeys(parts))) + "."
        return f"{len(items)} marketing-related action(s)."

    elif cat_name == "Personnel":
        if not items:
            return "No current personnel action items."
        parts = []
        for it in items:
            t = it["text"].lower()
            if "part-time" in t or "part time" in t or "add" in t:
                parts.append("Adding part-time leasing team member (3 → 4 staff)")
            if "incentiv" in t:
                parts.append("Team incentive program tied to occupancy goals")
        if parts:
            return "; ".join(list(dict.fromkeys(parts))) + "."
        return f"{len(items)} personnel-related action(s)."

    elif cat_name == "Renovation":
        if not items:
            return "No current renovation action items."
        parts = []
        for it in items:
            t = it["text"].lower()
            if ("exterior" in t or "landscape" in t or "landscap" in t) and ("excessive" in t or "value engineer" in t or "$" in it["text"]):
                parts.append("Exterior improvements ($86K) & landscape upgrades ($221K) costs excessive — exploring value engineering")
            elif "landscap" in t or "景观" in t:
                parts.append("Phase 1 landscaping complete ahead of schedule")
            if "courtyard" in t or "院落" in t:
                parts.append("Courtyard renovation under budget ($109K)")
            if "宽带" in t or "comcast" in t or "broadband" in t:
                parts.append("Broadband (Comcast) delayed to Q2")
            if ("improvement" in t or "改进" in t or "蓝图" in t) and "exterior" not in t:
                parts.append("Improvement blueprint to be shared")
        if parts:
            return "; ".join(list(dict.fromkeys(parts))) + "."
        return f"{len(items)} renovation-related action(s)."

    elif cat_name == "Refinance":
        if not items:
            return "No active refinancing discussions. HUD loan at 3.18% maturing 2062."
        return f"{len(items)} refinancing-related action(s)."

    elif cat_name == "Sale":
        if not items:
            return "No active disposition plans at this time."
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

    # Build strategy summary — categorize actions into strategic buckets
    strategy_summary = _build_strategy_summary(all_actions, ap_summary)

    # Top-level property goal
    top_goal = {
        "goal": "60-Day Property Goal: Achieve 94.8% Occupancy",
        "target_value": 94.8,
        "metric": "occupancy_pct",
        "date_set": "2026-02-06",
        "deadline": None,
        "source": "Weekly Call (Feb 6, 2026)",
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

    # 7. HUD Loan Info
    print("\n[7/8] HUD Loan Info...")
    loan_data = loan_info.extract()
    write_json(os.path.join(DATA_OUTPUT, "loan_info.json"), loan_data)

    # 8. Companion Properties (T-12 cross-property comparison)
    print("\n[8/8] Companion Properties...")
    companion_data = companions.extract()
    write_json(os.path.join(DATA_OUTPUT, "companions.json"), companion_data)

    print(f"\nAll data extracted to {DATA_OUTPUT}/")

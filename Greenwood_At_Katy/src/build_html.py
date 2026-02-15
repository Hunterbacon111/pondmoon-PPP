"""Generate the dashboard HTML from template + JSON data."""
import json
import os
from datetime import datetime
from src.config import DATA_OUTPUT, DASHBOARD_DIR, TEMPLATES_DIR, PROPERTY


def generate_dashboard():
    """Read JSON data files and inject into HTML template."""
    template_path = os.path.join(TEMPLATES_DIR, "dashboard_template.html")
    output_path = os.path.join(DASHBOARD_DIR, "index.html")

    # Read template
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Read all JSON data files
    def load_json(filename):
        filepath = os.path.join(DATA_OUTPUT, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    property_info = load_json("property_info.json")
    leasing_data = load_json("leasing_weekly.json")
    budget_data = load_json("budget_monthly.json")
    financial_data = load_json("financials_monthly.json")
    actions_data = load_json("actions_log.json")
    comps_data = load_json("comps.json")
    loan_data = load_json("loan_info.json")
    companion_data = load_json("companions.json")

    # Replace static property placeholders
    html = html.replace("/* __PROPERTY_NAME__ */", PROPERTY["name"])
    html = html.replace("/* __PROPERTY_ADDRESS__ */", PROPERTY["address"])
    html = html.replace("/* __PROPERTY_UNITS__ */", str(PROPERTY["total_units"]))
    html = html.replace("/* __PROPERTY_YEAR__ */", str(PROPERTY["year_built"]))
    html = html.replace("/* __PROPERTY_SF__ */", f"{PROPERTY['total_sf']:,}")
    html = html.replace("/* __PROPERTY_PM__ */", PROPERTY["pm_company"])
    html = html.replace("/* __BUILD_DATE__ */", datetime.now().strftime("%Y-%m-%d %H:%M"))

    # Inject property images as base64
    images_data = load_json("images_b64.json")
    if images_data:
        for i in range(1, 5):
            key = f"property_{i}"
            if key in images_data:
                html = html.replace(f"/* __IMG_{i}__ */", images_data[key])
        # Login background image
        if "login_bg" in images_data:
            html = html.replace("/* __LOGIN_BG__ */", images_data["login_bg"])
        print(f"  -> Embedded {len(images_data)} property images")

    # Inject JSON data
    html = html.replace("/* __PROPERTY_JSON__ */", json.dumps(property_info, ensure_ascii=False))
    html = html.replace("/* __LEASING_JSON__ */", json.dumps(leasing_data, ensure_ascii=False))
    html = html.replace("/* __BUDGET_JSON__ */", json.dumps(budget_data, ensure_ascii=False))
    html = html.replace("/* __FINANCIAL_JSON__ */", json.dumps(financial_data, ensure_ascii=False))
    html = html.replace("/* __ACTIONS_JSON__ */", json.dumps(actions_data, ensure_ascii=False))
    html = html.replace("/* __COMPS_JSON__ */", json.dumps(comps_data, ensure_ascii=False))
    html = html.replace("/* __LOAN_JSON__ */", json.dumps(loan_data, ensure_ascii=False))
    html = html.replace("/* __COMPANION_JSON__ */", json.dumps(companion_data, ensure_ascii=False))

    # Write output
    os.makedirs(DASHBOARD_DIR, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  -> Dashboard generated: {output_path}")
    print(f"  -> File size: {os.path.getsize(output_path) / 1024:.1f} KB")

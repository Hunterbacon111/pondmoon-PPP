"""Extract action items and decisions from email communications."""
import os
import re
import glob
from docx import Document
from src.config import DATA_MARKETING


def _parse_email_docx(filepath):
    """Parse an email communication DOCX file."""
    doc = Document(filepath)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    full_text = "\n".join(paragraphs)

    actions = []

    # Determine sender from filename or content
    filename = os.path.basename(filepath)
    sender = "Unknown"
    source_party = "Unknown"
    if "meredith" in filename.lower() or "meredith" in full_text.lower()[:200]:
        sender = "Meredith"
        source_party = "AHC"

    # Parse for actionable decisions
    decision_keywords = [
        (r"occupancy.*incentiv", "Occupancy incentive plan established"),
        (r"loss leaders?", "Loss leaders approved/updated"),
        (r"renewal.*(?:concession|offer|incentive)", "Renewal concession strategy updated"),
        (r"marketing.*(?:spend|increase|hold)", "Marketing spend decision"),
        (r"part[- ]?time.*(?:leasing|team|employee|member)", "Staffing change recommended"),
        (r"(?:close|closing).*(?:sunday|office)", "Office hours adjustment"),
    ]

    for pattern, label in decision_keywords:
        if re.search(pattern, full_text, re.IGNORECASE):
            # Find the relevant paragraph
            for para in paragraphs:
                if re.search(pattern, para, re.IGNORECASE):
                    actions.append({
                        "action": para[:200],
                        "label": label,
                        "responsible": sender,
                        "status": "recommended",
                        "category": "strategy",
                    })
                    break

    # If no specific patterns matched, treat each paragraph as a decision point
    if not actions:
        for para in paragraphs:
            if len(para) > 50 and not para.startswith("Steven") and not para.startswith("Dear"):
                actions.append({
                    "action": para[:200],
                    "label": "Strategic direction",
                    "responsible": sender,
                    "status": "communicated",
                    "category": "strategy",
                })

    return actions, sender, source_party


def extract():
    """Extract action items from all email communication files.

    Returns a list of action entries for the actions log.
    """
    all_actions = []

    if not os.path.exists(DATA_MARKETING):
        print("  [emails] Data_Marketing_Others directory not found.")
        return all_actions

    # Look for email-related DOCX files
    docx_files = glob.glob(os.path.join(DATA_MARKETING, "**", "*.docx"), recursive=True)
    email_files = [f for f in docx_files if "email" in os.path.basename(f).lower()
                   or "communication" in os.path.basename(f).lower()]

    for filepath in sorted(email_files):
        filename = os.path.basename(filepath)
        print(f"  [emails] Parsing: {filename}")

        actions, sender, source_party = _parse_email_docx(filepath)

        for item in actions:
            all_actions.append({
                "date": "2026-02-10",  # Approximate date from context
                "source": "Email",
                "source_detail": f"From {sender} ({source_party})",
                "source_party": source_party,
                "source_file": filename,
                "action": item["action"],
                "responsible": item["responsible"],
                "status": item["status"],
                "category": item["category"],
            })

    print(f"  [emails] Total action entries: {len(all_actions)}")
    return all_actions

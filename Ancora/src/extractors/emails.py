"""Extract action items from email communications.

Note: Ancora does not currently have email communication files.
This is a stub that returns empty results.
"""
import os
import glob
from src.config import DATA_MARKETING


def extract():
    """Extract action items from email communication files.

    Returns a list of action entries for the actions log.
    """
    all_actions = []

    if not os.path.exists(DATA_MARKETING):
        print("  [emails] Data_Marketing_Others directory not found.")
        return all_actions

    # Look for email-related DOCX files
    from docx import Document
    docx_files = glob.glob(os.path.join(DATA_MARKETING, "**", "*.docx"), recursive=True)
    email_files = [f for f in docx_files if "email" in os.path.basename(f).lower()
                   or "communication" in os.path.basename(f).lower()]

    if not email_files:
        print("  [emails] No email communication files found.")
        return all_actions

    # Parse any found files (future-proofing)
    for filepath in sorted(email_files):
        filename = os.path.basename(filepath)
        print(f"  [emails] Parsing: {filename}")
        doc = Document(filepath)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        for para in paragraphs:
            if len(para) > 50:
                all_actions.append({
                    "date": "2026-02-10",
                    "source": "Email",
                    "source_party": "Unknown",
                    "source_file": filename,
                    "action": para[:200],
                    "responsible": "Unknown",
                    "status": "communicated",
                    "category": "strategy",
                })

    print(f"  [emails] Total action entries: {len(all_actions)}")
    return all_actions

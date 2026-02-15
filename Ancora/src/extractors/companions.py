"""Extract T-12 financial data from companion properties.

Note: Ancora does not currently have companion property data.
This is a stub that returns empty results.
"""
from src.config import COMPANION_PROPERTIES


def extract():
    """Extract T-12 data for companion properties.

    Returns empty dict since Ancora has no companion properties configured.
    """
    if not COMPANION_PROPERTIES:
        print("  [companions] No companion properties configured.")
        return {}

    return {}

#!/usr/bin/env python3
"""Build the Ancora property analysis dashboard."""
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.build_data import extract_all
from src.build_html import generate_dashboard


def main():
    print("=" * 60)
    print("Ancora - Property Analysis Dashboard Builder")
    print("=" * 60)

    print("\nStep 1: Extracting data from source files...")
    extract_all()

    print("\nStep 2: Generating dashboard HTML...")
    generate_dashboard()

    print("\n" + "=" * 60)
    print("Done! Open dashboard/index.html in a browser.")
    print("=" * 60)


if __name__ == "__main__":
    main()

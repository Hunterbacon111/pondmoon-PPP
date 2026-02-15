#!/usr/bin/env python3
"""Run a single extractor and output JSON to stdout.
Used by the API server to process uploaded files without import conflicts.
All print() output from extractors is redirected to stderr so stdout is clean JSON.
"""
import sys
import json
import io

sys.path.insert(0, '.')

data_type = sys.argv[1] if len(sys.argv) > 1 else None

# Redirect stdout to stderr during extraction (extractors use print() for logging)
real_stdout = sys.stdout
sys.stdout = sys.stderr

if data_type == 'leasing':
    from src.extractors.leasing import extract
elif data_type == 'financials':
    from src.extractors.financials import extract
else:
    print(f"Unknown data_type: {data_type}", file=sys.stderr)
    sys.exit(1)

result = extract()

# Restore stdout and write clean JSON
sys.stdout = real_stdout
json.dump(result, sys.stdout, ensure_ascii=False)

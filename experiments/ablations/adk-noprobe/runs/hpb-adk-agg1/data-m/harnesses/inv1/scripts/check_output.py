#!/usr/bin/env python3
"""Stop hook: block finishing until output/answer.json is a valid deliverable."""
import json, sys

try:
    with open("output/answer.json") as f:
        d = json.load(f)
    assert isinstance(d, dict) and set(d) == {"net_usd", "transactions", "refunds"}, f"keys are {sorted(d) if isinstance(d, dict) else type(d).__name__}"
    assert all(isinstance(d[k], (int, float)) and not isinstance(d[k], bool) for k in d), "values must be numbers"
except Exception as e:
    print(f"output/answer.json is missing or invalid ({e}). Run: python3 scripts/net_revenue.py 2026-09 transactions.csv refunds.csv fx_daily.csv output/answer.json", file=sys.stderr)
    sys.exit(2)

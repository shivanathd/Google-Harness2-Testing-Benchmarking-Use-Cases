#!/usr/bin/env python3
"""Stop-hook check: output/answer.json must exist, parse, and have the requested keys.
Exit 2 (stderr goes to the agent) if not; exit 0 otherwise."""
import json, sys
try:
    d = json.load(open("output/answer.json"))
    assert isinstance(d["net_usd"], (int, float)) and not isinstance(d["net_usd"], bool)
    assert isinstance(d["transactions"], int) and isinstance(d["refunds"], int)
except Exception as e:
    print("output/answer.json is missing or invalid (%r). Write it now: run python3 scripts/reconcile_revenue.py YYYY-MM, "
          "or compute by hand, then write {\"net_usd\": <2 decimals>, \"transactions\": <int>, \"refunds\": <int>}." % (e,), file=sys.stderr)
    sys.exit(2)

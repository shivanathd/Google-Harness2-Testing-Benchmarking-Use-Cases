#!/usr/bin/env python3
"""Stop-hook check: exit 2 (stderr to agent) if output/answer.json is missing or malformed."""
import json, sys
try:
    d = json.load(open("output/answer.json"))
    assert isinstance(d, dict), "top level must be an object"
    assert isinstance(d["net_usd"], (int, float)) and not isinstance(d["net_usd"], bool)
    assert round(d["net_usd"], 2) == d["net_usd"], "net_usd must have at most 2 decimals"
    for k in ("transactions", "chargebacks"):
        assert isinstance(d[k], int) and not isinstance(d[k], bool), k + " must be an integer"
except Exception as e:
    print("output/answer.json is missing or invalid (%s: %s). It must be plain JSON with no backslash-escaped "
          'quotes: {"net_usd": <2dp number>, "transactions": <int>, "chargebacks": <int>}. Compute the values '
          "from the source files (`python3 scripts/net_revenue.py --month YYYY-MM` writes it), "
          "never a placeholder." % (type(e).__name__, e), file=sys.stderr)
    sys.exit(2)

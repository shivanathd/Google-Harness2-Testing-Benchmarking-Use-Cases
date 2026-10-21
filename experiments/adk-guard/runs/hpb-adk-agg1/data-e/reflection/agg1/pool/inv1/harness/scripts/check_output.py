#!/usr/bin/env python3
"""Stop-hook check: exit 2 (stderr to agent) if output/answer.json is missing or malformed."""
import json, sys
try:
    d = json.load(open("output/answer.json"))
    assert isinstance(d["net_usd"], (int, float)) and not isinstance(d["net_usd"], bool)
    assert isinstance(d["transactions"], int) and not isinstance(d["transactions"], bool)
except Exception as e:
    print("output/answer.json is missing or invalid (%s: %s). Write it as "
          '{"net_usd": <2dp number>, "transactions": <int>} before finishing; '
          "`python3 scripts/net_revenue.py` writes it." % (type(e).__name__, e), file=sys.stderr)
    sys.exit(2)

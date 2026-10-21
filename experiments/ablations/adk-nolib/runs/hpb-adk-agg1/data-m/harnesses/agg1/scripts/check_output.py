#!/usr/bin/env python3
"""Stop hook / manual check: output/answer.json must exist and parse with the required keys.
Exit 2 (stderr = instruction to the agent) when it does not; exit 0 otherwise."""
import json, sys
try:
    a = json.load(open("output/answer.json"))
    assert isinstance(a["net_usd"], (int, float)) and not isinstance(a["net_usd"], bool)
    assert isinstance(a["transactions"], int) and isinstance(a["refunds"], int)
except Exception as e:
    print("output/answer.json is missing or invalid (%s). Compute the figures now and write "
          'it as {"net_usd": <2dp number>, "transactions": <int>, "refunds": <int>} '
          "(see systemprompt.md), then re-open it to confirm." % e, file=sys.stderr)
    sys.exit(2)

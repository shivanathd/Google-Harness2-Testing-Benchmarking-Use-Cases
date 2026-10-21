#!/usr/bin/env python3
"""Stop-hook: block finishing until output/answer.json exists and parses as a non-empty JSON object.
Exit 2 (stderr goes to the agent) otherwise; exit 0 for any valid deliverable."""
import json, sys
p = 'output/answer.json'
try:
    d = json.load(open(p))
    if not isinstance(d, dict) or not d: raise ValueError('not a non-empty JSON object')
except Exception as e:
    print(f'Deliverable {p} is missing or unusable ({e}). Write it with exactly the keys/types the task names, then reopen it. '
          'If shell one-liners keep failing, put the code in a .py file and run that instead.', file=sys.stderr)
    sys.exit(2)

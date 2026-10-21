#!/usr/bin/env python3
"""Stop hook: refuse to finish until output/ holds a non-empty, parseable deliverable."""
import json, os, sys
d = 'output'
files = [f for f in os.listdir(d) if not f.startswith('.')] if os.path.isdir(d) else []
if not files:
    print('output/ has no deliverable yet. Write it now (e.g. python3 -I scripts/log_window_stats.py ... --write output/answer.json), then reopen it to check.', file=sys.stderr)
    sys.exit(2)
for f in files:
    p = os.path.join(d, f)
    if os.path.getsize(p) == 0:
        print(f'{p} is empty; rewrite it.', file=sys.stderr); sys.exit(2)
    if f.endswith('.json'):
        try:
            json.load(open(p))
        except Exception as e:
            print(f'{p} is not valid JSON ({e}); fix it.', file=sys.stderr); sys.exit(2)
sys.exit(0)

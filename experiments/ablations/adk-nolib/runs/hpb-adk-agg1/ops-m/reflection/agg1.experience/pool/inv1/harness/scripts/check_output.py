#!/usr/bin/env python3
"""Stop hook: block finishing until output/ has a non-empty, well-formed deliverable.
Exit 2 (stderr goes to the agent) if output/ is missing/empty or a .json file there does not parse.
Any other exit lets the agent finish."""
import json, os, sys

d = 'output'
files = [os.path.join(d, f) for f in os.listdir(d)] if os.path.isdir(d) else []
files = [f for f in files if os.path.isfile(f)]
problems = []
if not files:
    problems.append('output/ has no deliverable yet. Write the requested file under output/ before finishing.')
for f in files:
    if os.path.getsize(f) == 0:
        problems.append(f'{f} is empty.')
    elif f.endswith('.json'):
        try:
            json.load(open(f))
        except Exception as e:
            problems.append(f'{f} is not valid JSON: {e}')
if problems:
    print(' '.join(problems) + ' If a shell command keeps failing, stop retrying it: use a script file or the skill helper instead.', file=sys.stderr)
    sys.exit(2)

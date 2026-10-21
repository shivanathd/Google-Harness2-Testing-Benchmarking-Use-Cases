#!/usr/bin/env python3
"""Stop hook: block finishing until output/ holds a non-empty file and every .json parses."""
import glob, json, os, sys
files = [f for f in glob.glob("output/**/*", recursive=True) if os.path.isfile(f)]
if not files or any(os.path.getsize(f) == 0 for f in files):
    sys.stderr.write("No usable deliverable under output/. Compute the answer (use the loaded skill's script) and write the file the task names before finishing.\n")
    sys.exit(2)
for f in files:
    if f.endswith(".json"):
        try:
            json.load(open(f))
        except ValueError as e:
            sys.stderr.write("%s is not valid JSON (%s); rewrite it.\n" % (f, e))
            sys.exit(2)

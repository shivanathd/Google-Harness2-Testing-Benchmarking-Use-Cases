#!/usr/bin/env python3
"""Final gate: confirm the deliverable exists and the suite passes.

Usage: python3 scripts/check_done.py
Checks (from workspace root): output/CHANGES.md exists and is non-trivial, and
`python3 scripts/run_tests.py` exits 0. Prints each failure; exit 1 if any.
"""
import os
import subprocess
import sys

bad = []
p = "output/CHANGES.md"
if not os.path.isfile(p):
    bad.append(f"{p} is missing")
elif len(open(p, encoding="utf-8").read().strip()) < 40:
    bad.append(f"{p} is empty or too short")
here = os.path.dirname(os.path.abspath(__file__))
r = subprocess.run([sys.executable, os.path.join(here, "run_tests.py")], capture_output=True, text=True)
if r.returncode != 0:
    bad.append("tests failing:\n" + (r.stdout + r.stderr)[-1500:])
print("\n".join(bad) if bad else "OK: CHANGES.md present, tests pass")
sys.exit(1 if bad else 0)

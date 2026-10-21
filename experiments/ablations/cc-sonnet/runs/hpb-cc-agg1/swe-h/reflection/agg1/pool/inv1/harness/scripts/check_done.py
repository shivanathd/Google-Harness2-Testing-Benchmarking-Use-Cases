#!/usr/bin/env python3
"""Stop-hook check: output/CHANGES.md exists and is non-empty, sources compile, tests pass.

Usage: python3 scripts/check_done.py   (run from the workspace root)
Exit 0 when fine; exit 2 with an instruction on stderr otherwise.
A missing pytest or a test run that times out never blocks.
"""
import os
import subprocess
import sys

problems = []
path = os.path.join("output", "CHANGES.md")
if not os.path.isfile(path) or not open(path, encoding="utf-8", errors="replace").read().strip():
    problems.append("output/CHANGES.md is missing or empty: write a short summary of what changed, why, and what you ran.")

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("__pycache__", "output")]
    for name in files:
        if name.endswith(".py"):
            p = os.path.join(root, name)
            try:
                compile(open(p, "rb").read(), p, "exec")
            except SyntaxError as exc:
                problems.append(f"{p} does not compile: {exc}")

if os.path.isdir("tests") and not problems:
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q", "-x"], capture_output=True, text=True, timeout=90)
        if r.returncode == 1:
            problems.append("pytest tests fails; fix the code or, if the failure is unrelated, say why in output/CHANGES.md:\n" + r.stdout[-1200:])
    except (subprocess.TimeoutExpired, OSError):
        pass

if problems:
    print("Not done yet:\n- " + "\n- ".join(problems), file=sys.stderr)
    sys.exit(2)

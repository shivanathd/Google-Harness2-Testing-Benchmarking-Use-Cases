#!/usr/bin/env python3
"""Stop-hook / manual completion check. Exit 0 = ok; exit 2 = not done (reasons on stderr).

Requires: output/CHANGES.md exists, is non-empty and names at least one existing
workspace file; every non-test .py file compiles; tests in tests/ pass (and at least one ran).
"""
import pathlib
import re
import subprocess
import sys

problems = []
ws = pathlib.Path(".")
changes = ws / "output" / "CHANGES.md"
if not changes.is_file() or len(changes.read_text(errors="replace").strip()) < 20:
    problems.append("output/CHANGES.md is missing or empty. If the code is not fixed yet, fix it first "
                    "(edit the source, don't just plan); then write the summary: what was wrong, "
                    "files changed, how you verified.")
else:
    text = changes.read_text(errors="replace")
    named = [t for t in re.findall(r"[\w./-]+\.py", text) if (ws / t).is_file()]
    if not named:
        problems.append("output/CHANGES.md names no existing .py file; list the files you changed.")

for f in ws.rglob("*.py"):
    if any(p in {".git", "__pycache__", "output"} for p in f.parts):
        continue
    try:
        compile(f.read_bytes(), str(f), "exec")
    except SyntaxError as e:
        problems.append(f"{f} does not compile: {e}")

if (ws / "tests").is_dir():
    r = subprocess.run([sys.executable, str(pathlib.Path(__file__).parent / "run_tests.py")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        problems.append("tests fail or none ran:\n" + (r.stdout + r.stderr)[-1500:])

if problems:
    print("Not done yet:\n- " + "\n- ".join(problems), file=sys.stderr)
    sys.exit(2)

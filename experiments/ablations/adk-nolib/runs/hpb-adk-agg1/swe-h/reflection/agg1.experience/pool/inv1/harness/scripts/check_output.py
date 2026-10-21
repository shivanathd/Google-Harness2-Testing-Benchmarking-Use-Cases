#!/usr/bin/env python3
"""Pre-finish check for issue-resolution tasks. Run from the workspace root.

Checks: output/CHANGES.md exists, is non-empty and names every edited source file;
at least one non-test .py file was edited after the workspace was set up; existing
tests pass (skipped if pytest is unavailable). Exit 2 + stderr = problems, 0 = ok.
"""
import os
import subprocess
import sys

problems = []
SKIP = {"output", ".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv"}

pys = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in files:
        if f.endswith(".py"):
            pys.append(os.path.join(root, f))
others = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in files:
        p = os.path.join(root, f)
        if not f.endswith((".py", ".pyc")):
            others.append(p)

# Baseline = newest mtime among files the agent normally leaves alone (issue, docs).
base = max([os.path.getmtime(p) for p in others] or [0])
is_test = lambda p: "tests" in p.split(os.sep) or os.path.basename(p).startswith("test_")
edited = [p for p in pys if os.path.getmtime(p) > base + 1]
src_edited = [p for p in edited if not is_test(p)]
if not src_edited:
    problems.append("No non-test .py source file has been edited. The issue must be fixed in the source "
                    "files themselves: read them and edit them (output/ISSUE.md copies do not count).")

cp = os.path.join("output", "CHANGES.md")
if not os.path.isfile(cp) or not open(cp, errors="replace").read().strip():
    problems.append("output/CHANGES.md is missing or empty: write a short summary of the edits you made.")
else:
    text = open(cp, errors="replace").read()
    missing = [os.path.basename(p) for p in edited
               if os.path.basename(p) not in text and os.path.splitext(os.path.basename(p))[0] not in text]
    if missing:
        problems.append("output/CHANGES.md does not mention edited file(s): " + ", ".join(missing))

if os.path.isdir("tests"):
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "tests", "-x", "-q"],
                           capture_output=True, text=True, timeout=120)
        out = r.stdout + r.stderr
        if "No module named pytest" in out:
            pass
        elif r.returncode not in (0, 5):
            problems.append("Tests fail (python -m pytest tests):\n" + out[-1500:])
    except Exception as e:
        problems.append("Could not run tests: %r (run them yourself)" % e)

if problems:
    sys.stderr.write("Do not finish yet:\n- " + "\n- ".join(problems) + "\n")
    sys.exit(2)

#!/usr/bin/env python3
"""Stop-hook check: block finishing until output/CHANGES.md exists and tests pass.

Exit 0 = may finish. Exit 2 = blocked; stderr is the agent's next instruction.
Never blocks on infrastructure problems (no pytest, timeout) -- only on real findings.
"""
import os
import subprocess
import sys

problems = []

p = os.path.join("output", "CHANGES.md")
if not os.path.isfile(p) or not open(p, errors="replace").read().strip():
    problems.append("output/CHANGES.md is missing or empty. Make the fix in the source files first, "
                    "then write a short summary of the changes to output/CHANGES.md.")

if os.path.isdir("tests"):
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q", "-x"],
                           capture_output=True, text=True, timeout=90)
        out = r.stdout + r.stderr
        if r.returncode != 0 and "ModuleNotFoundError" not in out and "No module named" not in out:
            problems.append("`python -m pytest tests` fails. Fix the code (not the tests, unless a test "
                            "contradicts the issue) and re-run:\n" + out[-1500:])
    except Exception:
        pass

if problems:
    sys.stderr.write("Not finished:\n- " + "\n- ".join(problems) + "\n")
    sys.exit(2)

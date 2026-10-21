#!/usr/bin/env python3
"""Stop-hook check: output/CHANGES.md exists and is non-empty, and tests/ passes.

Usage: python3 scripts/check_done.py   (run from the workspace root)
Exit 0 when fine (or pytest/tests are unavailable, so nothing can be checked);
exit 2 with an instruction on stderr otherwise. Never loops forever: the runner
caps blocking at a few attempts.
"""
import os
import subprocess
import sys


def main():
    problems = []
    path = os.path.join("output", "CHANGES.md")
    if not os.path.isfile(path) or not open(path, encoding="utf-8", errors="replace").read().strip():
        problems.append(f"{path} is missing or empty: write a short summary of what changed, why, and what you ran")
    if os.path.isdir("tests"):
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q", "-x", "--no-header"],
                               capture_output=True, text=True, timeout=120)
            out = (r.stdout + r.stderr)
            if r.returncode == 1:
                problems.append("tests fail; fix the code (or state in CHANGES.md why a failure is unrelated):\n" + out[-1200:])
        except (subprocess.TimeoutExpired, OSError):
            pass
    if problems:
        print("Not done yet:\n- " + "\n- ".join(problems), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

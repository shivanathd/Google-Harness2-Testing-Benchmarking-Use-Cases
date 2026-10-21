#!/usr/bin/env python3
"""Stop-hook check: a deliverable must exist under output/ before the agent finishes.

Exit 0 when output/ holds at least one non-empty file and every .json file in it parses.
Exit 2 with an instruction on stderr otherwise. The shape is not checked here: each task names
its own shape, and this check serves every task. Run from the workspace root.
"""
import json
import os
import sys

OUT = "output"


def fail(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(2)


def main():
    names = [n for n in os.listdir(OUT) if not n.startswith(".")] if os.path.isdir(OUT) else []
    files = [os.path.join(OUT, n) for n in sorted(names) if os.path.isfile(os.path.join(OUT, n))]
    if not any(os.path.getsize(p) > 0 for p in files):
        fail("output/ has no deliverable yet. Write the file the task names under output/, then finish.")
    for path in files:
        if not path.endswith(".json"):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                json.load(f)
        except (OSError, ValueError) as e:
            fail(f"{path} is not valid JSON ({e}). Rewrite the whole file as valid JSON, then finish.")
    print(f"OK: output/ holds {len(files)} deliverable file(s).")


if __name__ == "__main__":
    main()

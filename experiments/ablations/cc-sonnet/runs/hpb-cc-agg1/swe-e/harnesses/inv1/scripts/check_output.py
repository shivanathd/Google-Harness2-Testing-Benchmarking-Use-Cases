#!/usr/bin/env python3
"""Check that each requested deliverable copy exists, compiles and matches its source.

Usage: python3 scripts/check_output.py SRC:DEST [SRC:DEST ...]
Exit 0 when every pair is fine (or the source does not exist, so nothing is owed);
exit 2 with an instruction on stderr otherwise (the Stop hook feeds this to the agent).
"""
import os
import sys


def main(pairs):
    problems = []
    for pair in pairs:
        src, _, dest = pair.partition(":")
        if not dest or not os.path.isfile(src):
            continue
        if not os.path.isfile(dest):
            problems.append(f"{dest} is missing: run `cp {src} {dest}` (mkdir -p {os.path.dirname(dest) or '.'} first)")
            continue
        with open(src, "rb") as a, open(dest, "rb") as b:
            sa, sb = a.read(), b.read()
        if sa != sb:
            problems.append(f"{dest} differs from {src}: re-copy the final file with `cp {src} {dest}`")
        if dest.endswith(".py"):
            try:
                compile(sb, dest, "exec")
            except SyntaxError as exc:
                problems.append(f"{dest} does not compile: {exc}")
    if problems:
        print("Deliverable check failed before finishing:\n- " + "\n- ".join(problems), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Check that each delivered copy exists, is non-empty, matches its source and compiles.

Usage: python3 skills/fix-python-bug/scripts/check_deliverable.py SOURCE DELIVERABLE [DELIVERABLE ...]

Prints one OK or FAIL line per deliverable. Exit 0 when all pass, 1 when any fail,
2 on bad arguments.
"""
import pathlib
import sys


def check(source, deliverable):
    if not source.is_file():
        return [f"missing source: {source}"]
    if not deliverable.is_file():
        return [f"missing deliverable: {deliverable}"]
    data = deliverable.read_bytes()
    problems = []
    if not data:
        problems.append(f"empty deliverable: {deliverable}")
    if data != source.read_bytes():
        problems.append(f"differs from source: {deliverable} vs {source}")
    try:
        compile(data, str(deliverable), "exec")
    except SyntaxError as exc:
        problems.append(f"syntax error in {deliverable} at line {exc.lineno}: {exc.msg}")
    return problems


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    source = pathlib.Path(argv[1])
    failed = False
    for name in argv[2:]:
        problems = check(source, pathlib.Path(name))
        if problems:
            failed = True
            for problem in problems:
                print(f"FAIL {problem}")
        else:
            print(f"OK {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

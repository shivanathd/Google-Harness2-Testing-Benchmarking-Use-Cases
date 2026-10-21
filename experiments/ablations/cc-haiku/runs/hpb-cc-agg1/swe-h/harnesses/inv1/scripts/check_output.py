"""Stop-hook gate: finishing is blocked until each named deliverable is a non-empty file.

Usage: python3 scripts/check_output.py <path> [<path> ...]
Exit 0 when every path is a file with text in it. Exit 2 with a message on stderr
otherwise, which the Stop hook returns to the agent as its next instruction.
Exit 1 on bad usage, which does not block finishing.
"""
import os
import sys


def has_text(path):
    if not os.path.isfile(path):
        return False
    with open(path, encoding="utf-8", errors="replace") as f:
        return bool(f.read().strip())


def main(argv):
    if not argv:
        print("usage: check_output.py <path> [<path> ...]", file=sys.stderr)
        return 1
    missing = [p for p in argv if not has_text(p)]
    if not missing:
        return 0
    names = ", ".join(missing)
    print(
        f"Not finished: {names} is missing or empty. Write it now: what changed "
        "per ISSUE.md item and the test result. Reopen it to confirm it reads "
        "back, then finish.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

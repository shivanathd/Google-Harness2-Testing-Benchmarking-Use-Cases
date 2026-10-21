#!/usr/bin/env python3
"""Check output/answer.json has the shape the task names: one object per service found in logs/.

Each service record must hold exactly requests (int), error_rate (number rounded to 4 decimals)
and p95_ms (int). Exit 0 when the file is usable; exit 2 with an instruction on stderr otherwise.
Run from the workspace root: python3 scripts/check_output.py
"""
import json
import os
import sys

OUT = "output/answer.json"
LOGS = "logs"
FIELDS = ("requests", "error_rate", "p95_ms")


def services():
    names = set()
    if os.path.isdir(LOGS):
        for fn in os.listdir(LOGS):
            for ext in (".jsonl.gz", ".jsonl"):
                if fn.endswith(ext):
                    names.add(fn[: -len(ext)])
                    break
    return sorted(names)


def fail(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(2)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    if not os.path.exists(OUT):
        fail(f"{OUT} does not exist. Write it now in the shape the task names, then re-run this check.")
    try:
        with open(OUT, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        fail(f"{OUT} is not valid JSON ({e}). Rewrite the whole file as valid JSON.")
    if not isinstance(data, dict) or not data:
        fail(f"{OUT} must be a non-empty JSON object keyed by service name.")

    expected = services()
    if expected:
        missing = [s for s in expected if s not in data]
        extra = [s for s in data if s not in expected]
        if missing:
            fail(f"{OUT} has no entry for service(s) {missing}. Add them.")
        if extra:
            fail(f"{OUT} has entries for {extra} that are not services in logs/. Remove them.")

    for svc, rec in data.items():
        if not isinstance(rec, dict):
            fail(f"{OUT}: entry '{svc}' must be an object with requests, error_rate and p95_ms.")
        if sorted(rec) != sorted(FIELDS):
            fail(f"{OUT}: entry '{svc}' must have exactly the keys {list(FIELDS)}; found {sorted(rec)}.")
        if not is_int(rec["requests"]) or rec["requests"] < 0:
            fail(f"{OUT}: '{svc}.requests' must be a non-negative integer.")
        er = rec["error_rate"]
        if not is_number(er) or round(er, 4) != er:
            fail(f"{OUT}: '{svc}.error_rate' must be a number rounded to 4 decimals.")
        if not is_int(rec["p95_ms"]):
            fail(f"{OUT}: '{svc}.p95_ms' must be an integer number of milliseconds.")

    print(f"OK: {OUT} has the required shape for {len(data)} service(s).")


if __name__ == "__main__":
    main()

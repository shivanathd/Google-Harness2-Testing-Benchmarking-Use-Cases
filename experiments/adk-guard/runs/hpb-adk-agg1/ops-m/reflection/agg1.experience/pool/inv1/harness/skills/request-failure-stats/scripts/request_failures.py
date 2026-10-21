#!/usr/bin/env python3
"""Failed-request statistics from rotated, mixed-offset service logs.
usage: request_failures.py LOG_DIR_OR_FILES... --start ISO --end ISO [--out output/answer.json]
START/END are ISO timestamps with offset, form YYYY-MM-DDTHH:MM:SS+00:00 (start inclusive, end exclusive).
Reads every file given (a directory means every file in it; *.gz is decompressed). Requests are
grouped by req= ACROSS all files; the last attempt is the highest attempt= number (ties: latest UTC time).
A request FAILED if that last attempt is an ERROR header line and its UTC time is inside the window.
Only lines starting at column 0 with a timestamp and a level carrying req= and attempt= are attempts;
indented traceback lines and req-less lines (e.g. 'cache warm after ERROR') are ignored.
Exit 1 with a message on bad input; exit 0 otherwise. Writes JSON only when --out is given."""
import argparse, collections, glob, gzip, json, os, re, sys
from datetime import datetime

ap = argparse.ArgumentParser()
ap.add_argument("paths", nargs="+")
ap.add_argument("--start", required=True)
ap.add_argument("--end", required=True)
ap.add_argument("--out")
a = ap.parse_args()

def ts(s):
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if d.tzinfo is None:
        sys.exit("timestamp without offset: " + s)
    return d
lo, hi = ts(a.start), ts(a.end)

files = []
for p in a.paths:
    files += sorted(glob.glob(os.path.join(p, "*"))) if os.path.isdir(p) else [p]
HEAD = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:?\d\d))\s+([A-Z]+)\s+(.*)$")
attempts = collections.defaultdict(list)
ignored = 0
for f in files:
    try:
        op = gzip.open if open(f, "rb").read(2) == b"\x1f\x8b" else open
        with op(f, "rt") as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        sys.exit("cannot read %s: %s" % (f, e))
    for line in lines:
        m = HEAD.match(line)
        if not m:
            ignored += 1
            continue
        t, lvl, rest = m.groups()
        req, att = re.search(r"\breq=(\S+)", rest), re.search(r"\battempt=(\d+)", rest)
        if not (req and att):
            ignored += 1
            continue
        user, code = re.search(r"\buser=(\S+)", rest), re.search(r"\bcode=(\S+)", rest)
        attempts[req[1]].append((int(att[1]), ts(t), lvl, user and user[1], code and code[1], f))

failed = []
for req, rows in attempts.items():
    last = max(rows, key=lambda r: (r[0], r[1]))
    if last[2] == "ERROR" and lo <= last[1] < hi:
        failed.append((req, last))
codes = collections.Counter(r[1][4] for r in failed)
users = {r[1][3] for r in failed}
top = codes.most_common()
print("files:", [os.path.basename(f) for f in files], "| requests seen:", len(attempts), "| non-attempt lines ignored:", ignored)
print("failed:", len(failed), "| users:", len(users), sorted(u for u in users if u))
print("code counts:", top)
if len(top) > 1 and top[0][1] == top[1][1]:
    print("WARNING: tie for top code; apply the task's tie rule")
dup = [r for r, rows in attempts.items() if len({x[0] for x in rows}) != len(rows)]
if dup:
    print("WARNING: duplicate attempt numbers for", dup)
if any(r[1][3] is None or r[1][4] is None for r in failed):
    print("WARNING: a failed last attempt lacks user= or code=")
for req, l in sorted(failed):
    print(" ", req, "attempt", l[0], l[1].astimezone(lo.tzinfo).isoformat(), l[3], l[4], os.path.basename(l[5]))
if a.out and top:
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump({"failed": len(failed), "users": len(users), "top_code": top[0][0]}, open(a.out, "w"))
    print("wrote", a.out, open(a.out).read())

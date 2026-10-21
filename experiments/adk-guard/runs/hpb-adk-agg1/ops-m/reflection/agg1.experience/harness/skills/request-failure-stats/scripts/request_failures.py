#!/usr/bin/env python3
"""Failed-request statistics from rotated, multi-timezone service logs.
usage: request_failures.py START_UTC END_UTC LOGFILE [LOGFILE ...]
START/END: ISO timestamps, naive = UTC (start inclusive, end exclusive).
Reads plain and .gz files (detected by magic bytes). A request (req=) FAILED if its
last attempt (latest UTC timestamp; ties by highest attempt=) is an ERROR line and that
attempt falls in the window. Prints failed / users / top_code plus audit detail."""
import collections, gzip, re, sys
from datetime import datetime, timezone

def utc(s):
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d.astimezone(timezone.utc)

def lines(path):
    raw = open(path, "rb").read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace").splitlines()

HEAD = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:?\d\d))\s+(\w+)\s+(.*)$")
lo, hi = utc(sys.argv[1]), utc(sys.argv[2])
reqs = collections.defaultdict(list)
seen, dups, noreq, odd = set(), 0, 0, []
for path in sys.argv[3:]:
    for n, line in enumerate(lines(path), 1):
        m = HEAD.match(line)          # events start at column 0; indented lines are continuations
        if not m:
            continue
        ts, lvl, rest = m.groups()
        r = re.search(r"\breq=(\S+)", rest)
        if not r:
            noreq += 1                # e.g. INFO lines that merely quote an error; not request attempts
            continue
        key = line.strip()
        if key in seen:
            dups += 1
            continue
        seen.add(key)
        a = re.search(r"\battempt=(\d+)", rest)
        u = re.search(r"\buser=(\S+)", rest)
        c = re.search(r"\bcode=(\S+)", rest)
        if lvl == "ERROR" and not (a and u and c):
            odd.append((path, n, line))
        reqs[r[1]].append((utc(ts), int(a[1]) if a else 0, lvl, u and u[1], c and c[1], path, n))

failed = []
for r, v in reqs.items():
    last = max(v, key=lambda x: (x[0], x[1]))
    if last[1] != max(x[1] for x in v):
        print("NOTE: latest-timestamp attempt != highest attempt number for", r)
    if last[2] == "ERROR" and lo <= last[0] < hi:
        failed.append((r, last))
codes = collections.Counter(b[4] for r, b in failed)
users = {b[3] for r, b in failed}
top = codes.most_common()
print("failed:", len(failed))
print("users:", len(users), sorted(users))
print("code counts (last attempts):", top)
if len(top) > 1 and top[0][1] == top[1][1]:
    print("WARNING: tie for top code")
print("top_code:", top[0][0] if top else None)
print("requests seen:", len(reqs), "| lines without req= ignored:", noreq, "| duplicate lines skipped:", dups)
print("ERROR lines missing user/code/attempt:", odd)
for r, b in sorted(failed, key=lambda x: x[1][0]):
    print(r, b[0].isoformat(), "user=%s code=%s attempt=%d" % (b[3], b[4], b[1]), "%s:%d" % (b[5], b[6]))

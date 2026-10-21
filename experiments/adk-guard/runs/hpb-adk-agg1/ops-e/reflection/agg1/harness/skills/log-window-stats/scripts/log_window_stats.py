#!/usr/bin/env python3
"""Count events of one level inside a UTC window from a multi-timezone log.
usage: log_window_stats.py LOG START_UTC END_UTC [LEVEL]
START/END like YYYY-MM-DDTHH:MM (UTC; start inclusive, end exclusive)."""
import collections, re, sys
from datetime import datetime, timezone

log, start, end = sys.argv[1:4]
level = sys.argv[4] if len(sys.argv) > 4 else "ERROR"
def utc(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=timezone.utc) if "+" not in s[10:] and "-" not in s[10:] else datetime.fromisoformat(s)
lo, hi = utc(start), utc(end)
HEAD = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:?\d\d))\s+(\w+)\s+(.*)$")
hits, skipped_cont, other = [], 0, 0
for n, line in enumerate(open(log), 1):
    m = HEAD.match(line.rstrip("\n"))   # events start at column 0; indented lines are continuations
    if not m:
        skipped_cont += 1
        continue
    ts, lvl, rest = m.groups()
    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if lvl != level or not (lo <= t < hi):
        continue
    user = re.search(r"\buser=(\S+)", rest)
    code = re.search(r"\bcode=(\S+)", rest)
    hits.append((n, ts, user and user[1], code and code[1]))
codes = collections.Counter(h[3] for h in hits if h[3])
print("events:", len(hits))
print("distinct users:", len({h[2] for h in hits if h[2]}), sorted({h[2] for h in hits if h[2]}))
print("code counts:", codes.most_common())
top = codes.most_common()
if len(top) > 1 and top[0][1] == top[1][1]:
    print("WARNING: tie for top code")
print("missing user:", sum(1 for h in hits if not h[2]), "missing code:", sum(1 for h in hits if not h[3]))
print("continuation/unparsed lines ignored:", skipped_cont)
for h in hits:
    print(*h)

#!/usr/bin/env python3
"""usage: window_stats.py LOGFILE START_ISO END_ISO [LEVEL]
START inclusive, END exclusive, ISO with offset (e.g. 2026-10-03T09:00:00+00:00). LEVEL default ERROR."""
import re, sys, collections
from datetime import datetime

path, start, end = sys.argv[1:4]
level = sys.argv[4] if len(sys.argv) > 4 else "ERROR"
start, end = datetime.fromisoformat(start), datetime.fromisoformat(end)
pat = re.compile(r"^(\d{4}-\d\d-\d\dT\S+)\s+(\w+)\s+\[([^\]]*)\]\s+user=(\S+)(?:\s+code=(\S+))?")
ev, skipped = [], 0
for line in open(path):
    m = pat.match(line)  # indented continuation lines never match
    if not m:
        skipped += 1
        continue
    ts = datetime.fromisoformat(m[1].replace("Z", "+00:00"))
    if m[2] == level and start <= ts < end:
        ev.append((ts, m[3], m[4], m[5]))
for ts, svc, u, c in sorted(ev):
    print(ts.astimezone(start.tzinfo).isoformat(), svc, u, c)
cnt = collections.Counter(c for *_, c in ev)
print("continuation/non-event lines skipped:", skipped)
print("errors", len(ev), "users", len({e[2] for e in ev}), "codes", cnt.most_common())
print({"errors": len(ev), "users": len({e[2] for e in ev}), "top_code": cnt.most_common(1)[0][0] if cnt else None})

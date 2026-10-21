#!/usr/bin/env python3
"""Count log records of one level inside a [start, end) window, timezone-aware.

usage: log_window_stats.py LOG START END [LEVEL]   (START/END ISO-8601 with offset or Z)
Record lines start with an ISO timestamp, then LEVEL, [service], key=value fields.
Continuation lines (no leading timestamp) are ignored.
"""
import re, sys, json
from collections import Counter
from datetime import datetime, timezone

def parse(s):
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)

path, start, end = sys.argv[1], parse(sys.argv[2]), parse(sys.argv[3])
level = sys.argv[4] if len(sys.argv) > 4 else "ERROR"
rec = re.compile(r'^(\d{4}-\d{2}-\d{2}[T ]\S+)\s+([A-Za-z]+)\s+(.*)$')
rows = []
for raw in open(path, encoding="utf-8"):
    m = rec.match(raw.rstrip("\n"))
    if not m or m.group(2).upper() != level.upper():
        continue
    ts = parse(m.group(1).replace(" ", "T", 1))
    if not (start <= ts < end):
        continue
    rest = m.group(3)
    u = re.search(r'\buser=(\S+)', rest)
    c = re.search(r'\bcode=(\S+)', rest)
    rows.append((ts, u and u.group(1), c and c.group(1)))
for r in sorted(rows, key=lambda r: r[0]):
    print(r[0].isoformat(), r[1], r[2])
codes = Counter(r[2] for r in rows if r[2])
print("events:", len(rows), "users:", len({r[1] for r in rows if r[1]}))
print("codes:", codes.most_common())
print(json.dumps({"errors": len(rows), "users": len({r[1] for r in rows if r[1]}),
                  "top_code": codes.most_common(1)[0][0] if codes else None}))

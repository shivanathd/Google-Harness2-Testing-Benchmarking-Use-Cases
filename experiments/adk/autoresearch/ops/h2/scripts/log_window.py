#!/usr/bin/env python3
"""Count ERROR events in a UTC time window of a multi-timezone log.

usage: python3 scripts/log_window.py LOGFILE START END [LEVEL] [--verbose]
  START/END: UTC, e.g. 2026-10-03T09:00 (START inclusive, END exclusive)
  LEVEL: default ERROR
Only lines that START with an ISO timestamp are events; the level must be the
token right after the timestamp. Indented/continuation lines (tracebacks) and
mentions of the level inside a message are NOT events. Prints errors, distinct
users, code counts (from the event's own header line), and a JSON answer.
"""
import re, sys, json, collections
from datetime import datetime, timezone

args = [a for a in sys.argv[1:] if not a.startswith("--")]
verbose = "--verbose" in sys.argv
path, start_s, end_s = args[:3]
level = args[3] if len(args) > 3 else "ERROR"

def parse_utc(s):
    s = s.strip().replace(" ", "T")
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    d = datetime.fromisoformat(s)
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)

start, end = parse_utc(start_s), parse_utc(end_s)
ev = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:?\d\d)?)\s+(\w+)\s+(.*)$")
n = 0
users = set()
codes = collections.Counter()
seen = set()
dups = 0
for line in open(path, encoding="utf-8", errors="replace"):
    line = line.rstrip("\n")
    m = ev.match(line)
    if not m:
        continue
    ts, lv, rest = m.groups()
    if lv != level:
        continue
    t = parse_utc(ts)
    if not (start <= t < end):
        continue
    if line in seen:
        dups += 1
    seen.add(line)
    n += 1
    u = re.search(r"\buser=(\S+)", rest)
    c = re.search(r"\bcode=(\S+)", rest)
    if u:
        users.add(u.group(1))
    if c:
        codes[c.group(1)] += 1
    if verbose:
        print(t.isoformat(), line)
print("events:", n, "| exact-duplicate lines:", dups)
print("distinct users:", len(users), sorted(users))
print("codes:", codes.most_common())
top = codes.most_common(1)[0][0] if codes else None
if len(codes) > 1 and codes.most_common(2)[0][1] == codes.most_common(2)[1][1]:
    print("WARNING: tie for top code - inspect")
print(json.dumps({"errors": n, "users": len(users), "top_code": top}))

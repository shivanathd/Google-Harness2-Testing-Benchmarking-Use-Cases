#!/usr/bin/env python3
"""Count log events of one level inside a UTC window, from a multi-timezone log.

usage: python3 scripts/log_window.py LOGFILE START END [--level ERROR]
  START/END are UTC, e.g. 2026-10-03T09:00 and 2026-10-03T12:00 (START inclusive, END exclusive).
An event = a line that STARTS with an ISO timestamp (with Z or +HH:MM/-HH:MM offset), then LEVEL.
Indented/continuation lines (tracebacks, wrapped text) are NOT events and are ignored, even if they
contain 'ERROR' or 'user=...'. Level must be the token right after the timestamp (INFO lines that
say 'retrying after ERROR' do not count). Users/codes are taken from the event's own header line.
Prints the counts, a per-code table, the user list, and a ready-to-use JSON line.
"""
import re, sys, json
from datetime import datetime, timezone
from collections import Counter

args = [a for a in sys.argv[1:]]
level = "ERROR"
if "--level" in args:
    i = args.index("--level"); level = args[i + 1]; del args[i:i + 2]
path, start_s, end_s = args[:3]

def parse_ts(s):
    s = s.strip().replace(" ", "T")
    if s.endswith("Z"): s = s[:-1] + "+00:00"
    d = datetime.fromisoformat(s)
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)

start, end = parse_ts(start_s), parse_ts(end_s)
hdr = re.compile(r"^(\d{4}-\d\d-\d\d[T ]\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:?\d\d))\s+\[?(\w+)\]?:?\s+(.*)$")
n = 0; users = set(); codes = Counter(); skipped = 0; nouser = 0; nocode = 0
with open(path, encoding="utf-8", errors="replace") as f:
    for line in f:
        line = line.rstrip("\n")
        m = hdr.match(line)
        if not m:
            if line.strip(): skipped += 1
            continue
        ts, lvl, rest = m.groups()
        ts = re.sub(r"([+-]\d\d)(\d\d)$", r"\1:\2", ts)
        if lvl.upper() != level.upper(): continue
        t = parse_ts(ts).astimezone(timezone.utc)
        if not (start <= t < end): continue
        n += 1
        u = re.search(r"\buser(?:_id|name)?=[\"\']?([^\s\"\',;]+)", rest); c = re.search(r"\b(?:error_)?code=[\"\']?([^\s\"\',;]+)", rest)
        if u: users.add(u.group(1))
        else: nouser += 1
        if c: codes[c.group(1)] += 1
        else: nocode += 1
top = codes.most_common()
print(f"events={n} distinct_users={len(users)} users={sorted(users)}")
print("codes:", top)
if len(top) > 1 and top[0][1] == top[1][1]: print("WARNING: tie for top code")
print(f"(ignored {skipped} continuation lines; events without user={nouser}, without code={nocode})")
print(json.dumps({"errors": n, "users": len(users), "top_code": top[0][0] if top else ""}))

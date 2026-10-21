#!/usr/bin/env python3
"""Count log events of a level inside a UTC window, with distinct users and top code.

usage: python3 scripts/log_window_stats.py LOGFILE START END [LEVEL]
  START/END are UTC, e.g. "2026-10-03 09:00" "2026-10-03 12:00" (START inclusive, END exclusive)
  LEVEL defaults to ERROR.
Only lines that START with a timestamp are events. Indented/continuation lines
(tracebacks, stack frames) are NOT events, even if they contain 'ERROR' or user=...
The level is the token right after the timestamp, never a word inside msg=.
Prints the counts, the full code/user tallies, and writes nothing.
"""
import re, sys, json
from collections import Counter
from datetime import datetime, timezone

TS = re.compile(r'^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})(\.\d+)?\s*(Z|[+-]\d{2}:?\d{2})?\s+(\S+)\s*(.*)$')

def parse_ts(date, time, frac, tz):
    s = f"{date}T{time}{frac or ''}"
    dt = datetime.fromisoformat(s)
    if tz in (None, '', 'Z'):
        return dt.replace(tzinfo=timezone.utc), tz is None
    sign = 1 if tz[0] == '+' else -1
    d = tz[1:].replace(':', '')
    from datetime import timedelta
    off = timezone(sign * timedelta(hours=int(d[:2]), minutes=int(d[2:])))
    return dt.replace(tzinfo=off), False

def pu(s):
    return datetime.fromisoformat(s.replace(' ', 'T')).replace(tzinfo=timezone.utc)

def main():
    path, start, end = sys.argv[1], pu(sys.argv[2]), pu(sys.argv[3])
    level = (sys.argv[4] if len(sys.argv) > 4 else 'ERROR').upper()
    events = []
    skipped, naive = [], 0
    for ln, line in enumerate(open(path, encoding='utf-8', errors='replace'), 1):
        line = line.rstrip('\n')
        if not line.strip():
            continue
        m = TS.match(line)
        if not m:  # continuation line
            continue
        ts, was_naive = parse_ts(m.group(1), m.group(2), m.group(3), m.group(4))
        naive += was_naive
        lvl = m.group(5).upper().strip('[]:')
        rest = m.group(6)
        kv = dict(re.findall(r'(\w+)=(\S+)', rest))
        events.append((ts, lvl, kv, ln, line))
    sel = [e for e in events if e[1] == level and start <= e[0].astimezone(timezone.utc) < end]
    codes = Counter(e[2].get('code') for e in sel)
    users = Counter(e[2].get('user') for e in sel)
    print(f"total events parsed: {len(events)}; naive-timestamp lines (assumed UTC): {naive}")
    print(f"levels seen: {dict(Counter(e[1] for e in events))}")
    print(f"{level} events in [{start}, {end}) UTC: {len(sel)}")
    print(f"distinct users: {len([u for u in users if u])}  {dict(users)}")
    print(f"codes: {codes.most_common()}")
    top = codes.most_common(2)
    if len(top) > 1 and top[0][1] == top[1][1]:
        print("WARNING: tie for top code")
    if codes:
        print("top_code:", codes.most_common(1)[0][0])
    dup = len(sel) - len({e[4] for e in sel})
    if dup:
        print(f"note: {dup} selected lines are exact duplicates of another selected line")
    print("matching lines:")
    for e in sorted(sel, key=lambda e: e[0]):
        print(f"  L{e[3]}: {e[4]}")
    print(json.dumps({"errors": len(sel), "users": len([u for u in users if u]),
                      "top_code": codes.most_common(1)[0][0] if codes else None}))

main()

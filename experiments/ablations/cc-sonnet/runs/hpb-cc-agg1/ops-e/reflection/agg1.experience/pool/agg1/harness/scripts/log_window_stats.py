#!/usr/bin/env python3
"""Count log events of one level inside a UTC window, from a multi-timezone log.

usage: python3 -I scripts/log_window_stats.py LOG START END [--level ERROR] [--write output/answer.json]
  START inclusive, END exclusive, ISO text, naive = UTC (e.g. 2026-10-03T09:00).
Only lines that BEGIN with an ISO timestamp are events; indented continuation
lines (tracebacks, wrapped text) are never counted, even if they contain
"ERROR user=..." text. The level is the token right after the timestamp, so
"msg=retrying after ERROR" on an INFO line is not an ERROR event.
Prints every matched event plus counts. --write emits
{"errors", "users", "top_code"}; exits 1 (and writes nothing) if no event
matched or the top code is tied, so the tie is resolved by a human decision.
"""
import argparse, json, re, sys
from collections import Counter
from datetime import datetime, timezone

HDR = re.compile(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2}))\s+(\w+)\s+(?:\[([^\]]*)\]\s+)?(.*)$')

def utc(s):
    d = datetime.fromisoformat(s.replace('Z', '+00:00'))
    return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d

ap = argparse.ArgumentParser()
ap.add_argument('log'); ap.add_argument('start'); ap.add_argument('end')
ap.add_argument('--level', default='ERROR'); ap.add_argument('--write')
a = ap.parse_args()
start, end = utc(a.start), utc(a.end)
ev, bad = [], []
for n, line in enumerate(open(a.log, encoding='utf-8', errors='replace'), 1):
    line = line.rstrip('\n')
    if not line.strip() or line[0] in ' \t':
        continue
    m = HDR.match(line)
    if not m:
        bad.append((n, line)); continue
    if m.group(2) != a.level:
        continue
    ts = utc(m.group(1))
    if not (start <= ts < end):
        continue
    u = re.search(r'\buser=(\S+)', m.group(4)); c = re.search(r'\bcode=(\S+)', m.group(4))
    ev.append((n, ts.isoformat(), u and u.group(1), c and c.group(1)))
for e in ev: print(e)
users = {e[2] for e in ev if e[2]}
codes = Counter(e[3] for e in ev if e[3])
print('unparsed non-indented lines:', bad)
print('events', len(ev), 'users', len(users), 'codes', codes.most_common())
top = codes.most_common(2)
if a.write:
    if not ev or (len(top) > 1 and top[0][1] == top[1][1]):
        print('NOT WRITTEN: no events or tied top code', file=sys.stderr); sys.exit(1)
    json.dump({'errors': len(ev), 'users': len(users), 'top_code': top[0][0]}, open(a.write, 'w'))
    print('wrote', a.write, open(a.write).read())

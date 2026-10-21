#!/usr/bin/env python3
"""Failed-request stats from a rotated, multi-timezone, retrying service log.

usage: python3 -I request_failures.py LOGDIR START END [--write output/answer.json]
  LOGDIR: directory holding app.log, app.log.N, app.log.N.gz (all are read).
  START inclusive, END exclusive, ISO text, naive = UTC (e.g. YYYY-MM-DDTHH:MM).
A request (req=) FAILED if its LAST attempt (latest UTC time; ties broken by
attempt number) is an ERROR header line AND that attempt's time is in the window.
Only lines beginning with a timestamp and carrying req= are attempts; indented
traceback lines and req-less INFO lines quoting "ERROR code=..." are ignored.
Attempts of one req are pooled across all files before choosing the last one.
Prints each failed request, then counts. --write emits {"failed","users","top_code"};
exits 1 and writes nothing if nothing failed or the top code is tied.
"""
import argparse, glob, gzip, json, os, re, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

HDR = re.compile(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2}))\s+(\w+)\s+(.*)$')

def utc(s):
    d = datetime.fromisoformat(s.replace('Z', '+00:00'))
    return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d.astimezone(timezone.utc)

ap = argparse.ArgumentParser()
ap.add_argument('logdir'); ap.add_argument('start'); ap.add_argument('end'); ap.add_argument('--write')
a = ap.parse_args()
start, end = utc(a.start), utc(a.end)
reqs, odd = defaultdict(list), []
for p in sorted(glob.glob(os.path.join(a.logdir, 'app.log*'))):
    op = gzip.open if p.endswith('.gz') else open
    with op(p, 'rt', encoding='utf-8', errors='replace') as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip('\n')
            if not line.strip() or line[0] in ' \t':
                continue
            m = HDR.match(line)
            r = m and re.search(r'\breq=(\S+)', m.group(3))
            if not r:
                if not (m and m.group(2) == 'INFO'):
                    odd.append((os.path.basename(p), n, line))
                continue
            kv = m.group(3)
            u = re.search(r'\buser=(\S+)', kv); at = re.search(r'\battempt=(\d+)', kv); c = re.search(r'\bcode=(\S+)', kv)
            reqs[r.group(1)].append((utc(m.group(1)), int(at.group(1)) if at else 0, m.group(2),
                                     u and u.group(1), c and c.group(1)))
failed, inwin = [], 0
for rid, at in reqs.items():
    last = max(at, key=lambda x: (x[0], x[1]))
    if start <= last[0] < end:
        inwin += 1
        if last[2] == 'ERROR':
            failed.append((rid, last[0].isoformat(), last[3], last[4]))
for x in sorted(failed): print(x)
users = {x[2] for x in failed if x[2]}
codes = Counter(x[3] for x in failed)
print('non-INFO lines without req= (review):', odd)
print('requests total', len(reqs), 'last-attempt in window', inwin, 'failed', len(failed),
      'users', len(users), 'codes', codes.most_common())
top = codes.most_common(2)
if a.write:
    if not failed or (len(top) > 1 and top[0][1] == top[1][1]):
        print('NOT WRITTEN: nothing failed or tied top code', file=sys.stderr); sys.exit(1)
    json.dump({'failed': len(failed), 'users': len(users), 'top_code': top[0][0]}, open(a.write, 'w'))
    print('wrote', a.write, open(a.write).read())

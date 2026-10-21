#!/usr/bin/env python3
"""Request-level failure stats from a rotated, multi-timezone service log directory.

usage: python3 -I scripts/request_failures.py LOGDIR START END [--write output/answer.json]
  START inclusive, END exclusive, ISO text, naive = UTC (e.g. 2026-10-06T08:00).
Reads every file in LOGDIR (app.log, app.log.N, *.gz) as one stream. Only lines
that BEGIN with an ISO timestamp and carry req= are attempts; indented
tracebacks and req-less lines (e.g. "cache warm after ERROR") are ignored.
Level = token right after the timestamp. Attempts are grouped by req across all
files; the LAST attempt is the highest attempt number (time order is checked
against it and any disagreement is printed). A request FAILED if its last
attempt is an ERROR line; it is in scope if that last attempt's UTC time is in
[START, END). users = distinct users of failed requests; top_code = most
frequent code= on the failed requests' last attempts only.
Prints every failed request, counts, anomalies. --write emits
{"failed", "users", "top_code"}; exits 1 and writes nothing on no failures or a
tied top code (resolve the tie by re-checking, then write by hand).
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
files = sorted(p for p in glob.glob(os.path.join(a.logdir, '*')) if os.path.isfile(p))
reqs, odd, nlines = defaultdict(list), [], 0
for p in files:
    op = gzip.open if p.endswith('.gz') else open
    with op(p, 'rt', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.rstrip('\n'); nlines += 1
            if not line.strip() or line[0] in ' \t':
                continue
            m = HDR.match(line)
            if not m:
                odd.append((os.path.basename(p), line)); continue
            body = m.group(3)
            r = re.search(r'\breq=(\S+)', body)
            if not r:
                continue
            at = re.search(r'\battempt=(\d+)', body)
            u = re.search(r'\buser=(\S+)', body); c = re.search(r'\bcode=(\S+)', body)
            reqs[r.group(1)].append((int(at.group(1)) if at else 0, utc(m.group(1)), m.group(2),
                                     u and u.group(1), c and c.group(1)))
print('files', [os.path.basename(p) for p in files], 'lines', nlines, 'requests', len(reqs))
print('non-indented lines with no timestamp:', odd[:10])
failed, disagree, dup = [], [], 0
for rid, al in reqs.items():
    by_att = max(al, key=lambda x: (x[0], x[1])); by_t = max(al, key=lambda x: (x[1], x[0]))
    if by_att != by_t:
        disagree.append(rid)
    if len({x[0] for x in al}) != len(al):
        dup += 1
    last = by_att
    if last[2] == 'ERROR' and start <= last[1] < end:
        failed.append((rid, last[1].isoformat(), last[3], last[4]))
for f in sorted(failed, key=lambda x: x[1]): print(f)
users = {f[2] for f in failed if f[2]}
codes = Counter(f[3] for f in failed if f[3])
print('attempt-order vs time-order disagreements:', disagree, '| requests with repeated attempt numbers:', dup)
print('failed', len(failed), 'users', len(users), 'codes', codes.most_common())
top = codes.most_common(2)
if a.write:
    if not failed or (len(top) > 1 and top[0][1] == top[1][1]):
        print('NOT WRITTEN: no failures or tied top code', file=sys.stderr); sys.exit(1)
    json.dump({'failed': len(failed), 'users': len(users), 'top_code': top[0][0]}, open(a.write, 'w'))
    print('wrote', a.write, open(a.write).read())

#!/usr/bin/env python3
"""Request-level failure stats from rotated, multi-timezone service logs.

usage: request_failures.py LOG [LOG ...] START END [--list] [--write OUT.json] [--names failed,users,top_code]
  Pass every log file (plain or gzip, detected by magic bytes). The LAST two positional args are
  START and END (ISO with offset or Z; START inclusive, END exclusive), e.g. 2026-10-06T08:00:00Z.
An event = a line that STARTS with a timestamp. Level = token after the timestamp. Fields come from
that header line only. Events without req= (e.g. 'cache warm after ERROR') and indented
continuation lines (tracebacks quoting 'ERROR code=.. user=..') are never request attempts.
Requests are grouped by req across ALL files. The last attempt = latest UTC timestamp; it is
cross-checked against the highest attempt= number. A request FAILED if its last attempt (over the whole
log, not just inside the window) is ERROR AND that last attempt's UTC time is inside the window.
"""
import sys, re, json, gzip, argparse, collections
from datetime import datetime, timezone

def ts(s):
    d = datetime.fromisoformat(s.strip().replace('Z', '+00:00'))
    return (d if d.tzinfo else d.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)

def lines(path):
    with open(path, 'rb') as fh:
        gz = fh.read(2) == b'\x1f\x8b'
    op = gzip.open if gz else open
    with op(path, 'rt', errors='replace') as fh:
        for ln in fh:
            yield ln.rstrip('\n')

ap = argparse.ArgumentParser()
ap.add_argument('args', nargs='+'); ap.add_argument('--list', action='store_true')
ap.add_argument('--write'); ap.add_argument('--names', default='failed,users,top_code')
a = ap.parse_args()
if len(a.args) < 3: sys.exit('need LOG... START END')
*logs, s0, s1 = a.args
lo, hi = ts(s0), ts(s1)
ev_re = re.compile(r'^(\d{4}-\d\d-\d\dT\S+)\s+([A-Za-z]+)\s+(.*)$')
reqs = collections.defaultdict(list); cont = bad = noreq = 0; perfile = {}
for p in logs:
    n = 0
    for line in lines(p):
        if not line.strip(): continue
        n += 1
        m = ev_re.match(line)
        if not m: cont += 1; continue
        try: t = ts(m[1])
        except ValueError: bad += 1; print('BAD TIMESTAMP:', line, file=sys.stderr); continue
        f = dict(x.split('=', 1) for x in m[3].split() if '=' in x)
        if 'req' not in f: noreq += 1; continue
        try: att = int(f.get('attempt', 0))
        except ValueError: att = 0
        reqs[f['req']].append((t, att, m[2], f.get('code'), f.get('user'), line))
    perfile[p] = n
disagree = []; fails = []
for r, v in reqs.items():
    last = max(v, key=lambda x: (x[0], x[1]))
    if max(v, key=lambda x: (x[1], x[0])) != last: disagree.append(r)
    if last[2] == 'ERROR' and lo <= last[0] < hi: fails.append((r, last))
fails.sort(key=lambda x: x[1][0])
users = {x[1][4] for x in fails}; codes = collections.Counter(x[1][3] for x in fails)
top = codes.most_common(); tie = len(top) > 1 and top[0][1] == top[1][1]
if a.list:
    for r, l in fails: print(l[0].strftime('%Y-%m-%dT%H:%M:%SZ'), r, 'attempt=%d' % l[1], l[4], l[3])
print('lines_per_file=', perfile)
print(f'requests_total={len(reqs)} failed={len(fails)} distinct_users={len(users)} users={sorted(users)}')
print('codes=', dict(top))
print(f'continuation_lines_skipped={cont} events_without_req_skipped={noreq} bad_timestamps={bad}')
if disagree: print('WARNING: last-by-time and last-by-attempt differ for', disagree)
if tie: print('WARNING: tie for top code:', [c for c, k in top if k == top[0][1]])
if a.write:
    if tie or bad or disagree or not top: sys.exit('not writing: tie/bad lines/ordering conflict/no failures - resolve manually')
    k = a.names.split(',')
    json.dump({k[0]: len(fails), k[1]: len(users), k[2]: top[0][0]}, open(a.write, 'w'))
    print('wrote', a.write, open(a.write).read())

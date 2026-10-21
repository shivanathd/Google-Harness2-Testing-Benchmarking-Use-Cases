#!/usr/bin/env python3
"""Request-level failure statistics over rotated service logs (plain or .gz).

usage: request_window_stats.py START END LOG [LOG ...] [--list] [--write OUT.json] [--keys failed,users,top_code]
  START inclusive, END exclusive; ISO with offset or Z, e.g. 2026-10-06T08:00:00Z (naive = UTC).
  LOG files may be gzip (detected by magic bytes, not by name). Pass ALL rotated files: a request's
  attempts can be split across files, and exact duplicate lines across files are collapsed.

Rules: an event is a line STARTING with a timestamp; level = token after it; fields (req, user, attempt,
code) come from the part before msg=. Indented lines (tracebacks) and lines without req= (e.g. INFO
"cache warm after ERROR") are never request attempts. Attempts are grouped by req across all files;
the LAST attempt = highest attempt number (a warning is printed if the latest UTC time disagrees).
A request FAILED if its last attempt is ERROR level AND that attempt's UTC time is in the window.
Prints failed count, distinct users of failed requests, code tally of last attempts (flags ties).
--write refuses on a tie, bad lines, a request seen under two users, or no failures.
"""
import sys, re, json, gzip, argparse, collections
from datetime import datetime, timezone

def ts(s):
    d = datetime.fromisoformat(s.strip().replace('Z', '+00:00'))
    return (d if d.tzinfo else d.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)

def lines(path):
    with open(path, 'rb') as fh:
        magic = fh.read(2)
    op = gzip.open if magic == b'\x1f\x8b' else open
    with op(path, 'rt', errors='replace') as fh:
        for l in fh:
            yield l.rstrip('\n')

ap = argparse.ArgumentParser()
ap.add_argument('start'); ap.add_argument('end'); ap.add_argument('logs', nargs='+')
ap.add_argument('--list', action='store_true'); ap.add_argument('--write')
ap.add_argument('--keys', default='failed,users,top_code')
a = ap.parse_args()
lo, hi = ts(a.start), ts(a.end)
ev_re = re.compile(r'^(\d{4}-\d\d-\d\dT\S+)\s+([A-Za-z]+)\s+(.*)$')

seen = set(); dup = cont = bad = noreq = noatt = 0
reqs = collections.defaultdict(list)  # req -> [(attempt, utc, level, user, code, line)]
for path in a.logs:
    for line in lines(path):
        if not line.strip(): continue
        m = ev_re.match(line)
        if not m: cont += 1; continue
        try: t = ts(m[1])
        except ValueError: bad += 1; print('BAD TIMESTAMP:', line, file=sys.stderr); continue
        if line in seen: dup += 1; continue
        seen.add(line)
        f = dict(x.split('=', 1) for x in m[3].split(' msg=')[0].split() if '=' in x)
        if 'req' not in f: noreq += 1; continue
        if 'attempt' not in f: noatt += 1
        reqs[f['req']].append((int(f.get('attempt', 1)), t, m[2], f.get('user'), f.get('code'), line))

users = set(); codes = collections.Counter(); failed = []; warn = []
for r, evs in sorted(reqs.items()):
    evs.sort(key=lambda e: (e[0], e[1]))
    last = evs[-1]
    if last[1] < max(e[1] for e in evs) or len({e[0] for e in evs}) != len(evs):
        warn.append(f'{r}: attempt order vs time disagree or repeated attempt numbers - inspect')
    if len({e[3] for e in evs}) > 1: warn.append(f'{r}: multiple users {sorted({str(e[3]) for e in evs})}')
    if last[2] == 'ERROR' and lo <= last[1] < hi:
        failed.append((r, last)); users.add(last[3]); codes[last[4]] += 1
        if a.list: print(last[1].strftime('%Y-%m-%dT%H:%M:%SZ'), r, last[3], last[4], f'attempt={last[0]}/{len(evs)}')
top = codes.most_common()
tie = len(top) > 1 and top[0][1] == top[1][1]
print(f'requests_total={len(reqs)} failed={len(failed)} distinct_users={len(users)} users={sorted(map(str, users))}')
print('codes_of_last_attempts=', dict(top))
print(f'skipped: continuation_lines={cont} no_req_lines={noreq} duplicate_lines={dup} bad_timestamps={bad} no_attempt_field={noatt}')
for w in warn: print('WARNING:', w)
if tie: print('WARNING: tie for top code:', [c for c, k in top if k == top[0][1]])
if a.write:
    if tie or bad or not top or any('multiple users' in w for w in warn):
        sys.exit('not writing: tie/bad lines/no failures/user conflict - resolve manually')
    k = a.keys.split(',')
    json.dump({k[0]: len(failed), k[1]: len(users), k[2]: top[0][0]}, open(a.write, 'w'))
    print('wrote', a.write, open(a.write).read())

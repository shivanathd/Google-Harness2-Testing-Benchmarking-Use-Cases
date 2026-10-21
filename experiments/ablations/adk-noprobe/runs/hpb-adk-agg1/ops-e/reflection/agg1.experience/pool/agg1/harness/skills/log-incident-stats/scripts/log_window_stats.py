#!/usr/bin/env python3
"""Count log events of one level inside a UTC window.

usage: log_window_stats.py LOG START END [--level ERROR] [--list] [--write OUT.json]
  START/END: ISO timestamps with offset or Z (END exclusive), e.g. 2026-10-03T09:00:00Z
An event = a line that STARTS with a timestamp; the level is the token right after it.
Indented/continuation lines (tracebacks) and levels quoted inside msg= are not events.
Fields (user=, code=) are read from the event's own header line only.
Prints counts, distinct users, per-code counts (flags ties) and skipped-line tallies.
--write emits {"errors","users","top_code"}; refuses to write on a code tie or bad lines.
"""
import sys, re, json, argparse, collections
from datetime import datetime, timezone

def ts(s):
    d = datetime.fromisoformat(s.strip().replace('Z', '+00:00'))
    return (d if d.tzinfo else d.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)

ap = argparse.ArgumentParser()
ap.add_argument('log'); ap.add_argument('start'); ap.add_argument('end')
ap.add_argument('--level', default='ERROR'); ap.add_argument('--list', action='store_true')
ap.add_argument('--write')
a = ap.parse_args()
lo, hi = ts(a.start), ts(a.end)
ev_re = re.compile(r'^(\d{4}-\d\d-\d\dT\S+)\s+([A-Za-z]+)\s+(.*)$')
n = 0; users = set(); codes = collections.Counter(); cont = bad = nolvl = 0; nouser = nocode = 0
for line in open(a.log, errors='replace'):
    line = line.rstrip('\n')
    if not line.strip(): continue
    m = ev_re.match(line)
    if not m:
        cont += 1; continue
    try: t = ts(m[1])
    except ValueError:
        bad += 1; print('BAD TIMESTAMP:', line, file=sys.stderr); continue
    if m[2] != a.level or not (lo <= t < hi): continue
    f = dict(x.split('=', 1) for x in m[3].split() if '=' in x)
    n += 1
    if 'user' in f: users.add(f['user'])
    else: nouser += 1
    if 'code' in f: codes[f['code']] += 1
    else: nocode += 1
    if a.list: print(t.strftime('%Y-%m-%dT%H:%M:%SZ'), f.get('user'), f.get('code'), '|', line)
top = codes.most_common()
tie = len(top) > 1 and top[0][1] == top[1][1]
print(f'events={n} distinct_users={len(users)} users={sorted(users)}')
print('codes=', dict(top))
print(f'continuation_lines_skipped={cont} bad_timestamps={bad} events_without_user={nouser} events_without_code={nocode}')
if tie: print('WARNING: tie for top code:', [c for c, k in top if k == top[0][1]])
if a.write:
    if tie or bad or not top: sys.exit('not writing: tie/bad lines/no codes - resolve manually')
    json.dump({'errors': n, 'users': len(users), 'top_code': top[0][0]}, open(a.write, 'w'))
    print('wrote', a.write, open(a.write).read())

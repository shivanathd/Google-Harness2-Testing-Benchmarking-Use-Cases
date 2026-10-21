#!/usr/bin/env python3
"""Count events of one level in a UTC window of a multi-timezone service log.

usage: log_window_stats.py LOG START END [--level ERROR] [--out output/answer.json]
  START/END: ISO timestamps with offset or Z, e.g. 2026-10-03T09:00:00Z (END exclusive).
Prints matched events (so they can be eyeballed), counts, code tally, ties.
--out writes {"errors","users","top_code"}; refused if the top code is tied or nothing matched.
Exit 2 on bad input / unparseable header lines; 3 on tie or empty match with --out.
"""
import argparse, collections, json, re, sys
from datetime import datetime, timezone

HEAD = re.compile(r'^(\d{4}-\d\d-\d\dT[\d:.]+(?:Z|[+-]\d\d:?\d\d))\s+(\w+)\s+\[([^\]]*)\]\s*(.*)$')

def ts(s):
    s = s.strip()
    if s.endswith('Z'):
        s = s[:-1] + '+00:00'
    t = datetime.fromisoformat(s)
    if t.tzinfo is None:
        sys.exit('timestamp needs an offset or Z: ' + s)
    return t.astimezone(timezone.utc)

def main():
    a = argparse.ArgumentParser()
    a.add_argument('log'); a.add_argument('start'); a.add_argument('end')
    a.add_argument('--level', default='ERROR'); a.add_argument('--out')
    a = a.parse_args()
    lo, hi = ts(a.start), ts(a.end)
    codes = collections.Counter(); users = set(); n = 0; bad = 0; cont = 0
    for raw in open(a.log, encoding='utf-8', errors='replace'):
        line = raw.rstrip('\n')
        if not line.strip():
            continue
        if line[0] in ' \t':      # traceback / continuation text: never an event
            cont += 1
            continue
        m = HEAD.match(line)
        if not m:
            bad += 1; print('UNPARSED:', line, file=sys.stderr); continue
        t, lvl, svc, rest = ts(m[1]), m[2], m[3], m[4]
        if lvl != a.level or not (lo <= t < hi):
            continue
        u = re.search(r'\buser=(\S+)', rest); c = re.search(r'\bcode=(\S+)', rest)
        n += 1
        if u: users.add(u[1])
        if c: codes[c[1]] += 1
        print(f'{t:%Y-%m-%dT%H:%M:%SZ} {svc} user={u[1] if u else None} code={c[1] if c else None}')
    top = codes.most_common()
    print(f'events={n} users={len(users)} {sorted(users)}', file=sys.stderr)
    print('codes:', top, f'(continuation lines skipped: {cont}, unparsed: {bad})', file=sys.stderr)
    tie = len(top) > 1 and top[0][1] == top[1][1]
    if tie: print('WARNING: top code is tied', file=sys.stderr)
    if bad: sys.exit(2)
    if a.out:
        if not n or tie: sys.exit(3)
        json.dump({'errors': n, 'users': len(users), 'top_code': top[0][0]}, open(a.out, 'w'))
        print('wrote', a.out, open(a.out).read(), file=sys.stderr)

main()

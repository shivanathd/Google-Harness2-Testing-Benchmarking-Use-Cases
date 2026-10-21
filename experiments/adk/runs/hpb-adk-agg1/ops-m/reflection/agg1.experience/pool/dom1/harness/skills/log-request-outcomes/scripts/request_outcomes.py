#!/usr/bin/env python3
"""Final outcome per request (req=) across rotated, mixed-timezone, partly gzipped logs.

usage: request_outcomes.py START END LOG [LOG ...] [--out output/answer.json]
  START/END: ISO with offset or Z (END exclusive), e.g. 2026-10-06T08:00:00Z.
  LOG: plain or gzip files (gzip detected by magic bytes, not by name).
A request's last attempt = highest attempt=, cross-checked against latest UTC time (disagreement is printed).
FAILED = last attempt is level ERROR AND its UTC time is in [START, END).
Prints every failed request, the code tally, tie warning. --out writes {"failed","users","top_code"}
(refused with exit 3 on tie/empty, exit 2 on unparseable lines).
"""
import argparse, collections, gzip, json, re, sys
from datetime import datetime, timezone

HEAD = re.compile(r'^(\d{4}-\d\d-\d\dT[\d:.]+(?:Z|[+-]\d\d:?\d\d))\s+(\w+)\s+(.*)$')

def ts(s):
    s = s.strip()
    if s.endswith('Z'):
        s = s[:-1] + '+00:00'
    t = datetime.fromisoformat(s)
    if t.tzinfo is None:
        sys.exit('timestamp needs an offset or Z: ' + s)
    return t.astimezone(timezone.utc)

def lines(path):
    raw = open(path, 'rb').read()
    if raw[:2] == b'\x1f\x8b':
        raw = gzip.decompress(raw)
    return raw.decode('utf-8', 'replace').splitlines()

def main():
    a = argparse.ArgumentParser()
    a.add_argument('start'); a.add_argument('end'); a.add_argument('logs', nargs='+')
    a.add_argument('--out')
    a = a.parse_args()
    lo, hi = ts(a.start), ts(a.end)
    reqs = collections.defaultdict(list); bad = cont = noreq = 0; dup = set()
    for p in a.logs:
        for line in lines(p):
            if not line.strip():
                continue
            if line[0] in ' \t':          # traceback text: never an event
                cont += 1; continue
            m = HEAD.match(line)
            if not m:
                bad += 1; print('UNPARSED:', p, line, file=sys.stderr); continue
            rest = m[3]
            r = re.search(r'\breq=(\S+)', rest)
            if not r:                      # e.g. "cache warm after ERROR": not a request attempt
                noreq += 1; continue
            at = re.search(r'\battempt=(\d+)', rest); u = re.search(r'\buser=(\S+)', rest)
            c = re.search(r'\bcode=(\S+)', rest)
            reqs[r[1]].append((int(at[1]) if at else 0, ts(m[1]), m[2], u[1] if u else None, c[1] if c else None))
    codes = collections.Counter(); users = set(); n = 0
    for rid, ev in sorted(reqs.items()):
        if len({(e[0]) for e in ev}) != len(ev): dup.add(rid)
        last = max(ev, key=lambda e: (e[0], e[1]))
        if last != max(ev, key=lambda e: (e[1], e[0])):
            print(f'NOTE {rid}: highest attempt differs from latest time; inspect', file=sys.stderr)
        if len({e[3] for e in ev}) > 1:
            print(f'NOTE {rid}: more than one user', file=sys.stderr)
        if last[2] == 'ERROR' and lo <= last[1] < hi:
            n += 1; users.add(last[3]); codes[last[4]] += 1
            print(f'{last[1]:%Y-%m-%dT%H:%M:%SZ} {rid} attempt={last[0]}/{len(ev)} user={last[3]} code={last[4]}')
    top = codes.most_common()
    print(f'requests={len(reqs)} failed={n} users={len(users)} {sorted(users)}', file=sys.stderr)
    print('codes:', top, f'(continuation lines {cont}, non-request lines {noreq}, unparsed {bad}, dup attempts {sorted(dup)})', file=sys.stderr)
    tie = len(top) > 1 and top[0][1] == top[1][1]
    if tie: print('WARNING: top code is tied', file=sys.stderr)
    if bad: sys.exit(2)
    if a.out:
        if not n or tie: sys.exit(3)
        json.dump({'failed': n, 'users': len(users), 'top_code': top[0][0]}, open(a.out, 'w'))
        print('wrote', a.out, open(a.out).read(), file=sys.stderr)

main()

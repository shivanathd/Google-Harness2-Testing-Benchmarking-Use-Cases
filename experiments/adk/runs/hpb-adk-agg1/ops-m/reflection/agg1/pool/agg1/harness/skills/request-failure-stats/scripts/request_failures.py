#!/usr/bin/env python3
"""Failed-request statistics from rotated, mixed-timezone service logs (some gzip).

usage: request_failures.py LOG_DIR_OR_FILES... --start 2026-10-06T08:00:00Z --end 2026-10-06T12:00:00Z [--out output/answer.json]
A request (req=) FAILED if its LAST attempt is an ERROR line. Only requests whose last
attempt falls in [start, end) UTC are considered. Gzip is detected by magic bytes.
Header lines only (start with a timestamp); indented traceback lines and lines without req=
(e.g. 'INFO user=x msg=cache warm after ERROR code=E500') are never attempts.
Prints every considered request's last attempt, then tallies. Writes {"failed","users","top_code"}.
Exit 2: no log read / unparseable non-indented line / last-attempt ambiguity (attempt number
vs UTC time disagree, or duplicate attempt) -- inspect, do not retry blindly.
Exit 3: --out refused (tied top code or no failed requests).
"""
import argparse, collections, glob, gzip, json, os, re, sys
from datetime import datetime, timezone

HEAD = re.compile(r'^(\d{4}-\d\d-\d\dT[\d:.]+(?:Z|[+-]\d\d:?\d\d))\s+([A-Z]+)\s+(.*)$')

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
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='+'); ap.add_argument('--start', required=True)
    ap.add_argument('--end', required=True); ap.add_argument('--out')
    a = ap.parse_args()
    files = []
    for p in a.paths:
        files += sorted(glob.glob(os.path.join(p, '*'))) if os.path.isdir(p) else [p]
    lo, hi = ts(a.start), ts(a.end)
    reqs = collections.defaultdict(list); bad = 0; cont = 0; noreq = 0; seen = set()
    for f in files:
        for line in lines(f):
            if not line.strip():
                continue
            if line[0] in ' \t':
                cont += 1; continue
            m = HEAD.match(line)
            if not m:
                bad += 1; print('UNPARSED:', f, line, file=sys.stderr); continue
            kv = dict(re.findall(r'\b(\w+)=(\S+)', m[3]))
            if 'req' not in kv:
                noreq += 1; continue
            if line in seen:       # same line repeated across rotated files
                print('DUPLICATE LINE ignored:', line, file=sys.stderr); continue
            seen.add(line)
            reqs[kv['req']].append((ts(m[1]), int(kv.get('attempt', 0)), m[2], kv.get('user'), kv.get('code')))
    amb = 0; failed = []
    for r, ev in sorted(reqs.items()):
        by_n = max(ev, key=lambda e: e[1]); by_t = max(ev, key=lambda e: e[0])
        if by_n is not by_t:
            amb += 1; print(f'AMBIGUOUS last attempt req={r}: {sorted(ev)}', file=sys.stderr)
        last = by_n
        if not (lo <= last[0] < hi):
            continue
        ok = last[2] != 'ERROR'
        print(f'{r} n={len(ev)} last={last[0]:%Y-%m-%dT%H:%M:%SZ} #{last[1]} {last[2]} user={last[3]} code={last[4]}' + ('' if ok else '  FAILED'))
        if not ok:
            failed.append(last)
    users = {e[3] for e in failed}; codes = collections.Counter(e[4] for e in failed).most_common()
    print(f'files={len(files)} requests={len(reqs)} failed={len(failed)} users={len(users)} {sorted(users)}', file=sys.stderr)
    print('codes:', codes, f'(continuation lines skipped: {cont}, non-req lines skipped: {noreq}, unparsed: {bad}, ambiguous: {amb})', file=sys.stderr)
    tie = len(codes) > 1 and codes[0][1] == codes[1][1]
    if tie: print('WARNING: top code is tied', file=sys.stderr)
    if bad or amb or not files:
        sys.exit(2)
    if a.out:
        if not failed or tie: sys.exit(3)
        os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
        json.dump({'failed': len(failed), 'users': len(users), 'top_code': codes[0][0]}, open(a.out, 'w'))
        print('wrote', a.out, open(a.out).read(), file=sys.stderr)

main()

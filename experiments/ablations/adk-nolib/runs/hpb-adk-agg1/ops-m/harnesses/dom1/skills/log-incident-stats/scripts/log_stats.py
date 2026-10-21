#!/usr/bin/env python3
"""Failed-request stats from rotated service logs.
usage: python3 log_stats.py LOG_DIR START END [--out answer.json]
START/END are ISO timestamps with offset (END exclusive), e.g. YYYY-MM-DDTHH:MM:SS+00:00.
Reads app.log, app.log.N and *.gz in LOG_DIR (all rotations, gzip handled)."""
import gzip, os, re, sys, collections
from datetime import datetime, timezone

RX = re.compile(r'^(\d{4}-\d\d-\d\dT\S+) (\w+) req=(\S+) user=(\S+) attempt=(\d+)(.*)$')

def utc(s):
    return datetime.fromisoformat(s).astimezone(timezone.utc)

def main():
    d, s, e = sys.argv[1:4]
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    S, E = utc(s), utc(e)
    reqs = collections.defaultdict(list)
    skipped = collections.Counter()
    seen = set()
    dups = 0
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d, fn)
        if not os.path.isfile(p):
            continue
        op = gzip.open if fn.endswith('.gz') else open
        with op(p, 'rt', errors='replace') as f:
            for line in f:
                line = line.rstrip('\n')
                m = RX.match(line)
                if not m:
                    skipped['no req= attempt= header (traceback/continuation/cache-warm/other)'] += 1
                    continue
                if line in seen:
                    dups += 1
                    continue
                seen.add(line)
                c = re.search(r'\bcode=(\S+)', m[6])
                reqs[m[3]].append((int(m[5]), utc(m[1]), m[2], m[4], c.group(1) if c else None))
    failed = []
    for r, v in reqs.items():
        la = max(v, key=lambda x: x[0])   # highest attempt number
        lt = max(v, key=lambda x: x[1])   # latest UTC time
        if la != lt:
            print(f'WARN {r}: last-by-attempt != last-by-time, using attempt number', file=sys.stderr)
        if len({x[3] for x in v}) > 1:
            print(f'WARN {r}: multiple users', file=sys.stderr)
        if S <= la[1] < E and la[2] == 'ERROR':
            failed.append((r, la))
    codes = collections.Counter(l[4] for _, l in failed)
    users = {l[3] for _, l in failed}
    top = codes.most_common()
    ans = {"failed": len(failed), "users": len(users), "top_code": top[0][0] if top else None}
    print('requests seen:', len(reqs), '| exact-duplicate lines dropped:', dups)
    print('skipped lines:', dict(skipped))
    print('codes:', top)
    if len(top) > 1 and top[0][1] == top[1][1]:
        print('WARN: tie for top code')
    print(ans)
    if out:
        import json
        json.dump(ans, open(out, 'w'))

main()

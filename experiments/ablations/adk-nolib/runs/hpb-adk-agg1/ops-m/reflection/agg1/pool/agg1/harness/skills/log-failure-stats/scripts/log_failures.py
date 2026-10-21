#!/usr/bin/env python3
"""Request-level failure stats from rotated service logs (plain and .gz).

usage: log_failures.py LOGDIR START END [--out PATH]
  START/END are UTC, e.g. YYYY-MM-DDTHH:MM YYYY-MM-DDTHH:MM (START inclusive, END exclusive).
Prints counts plus audit info as JSON. With --out, also writes
{"failed": int, "users": int, "top_code": str} to PATH.
Exit 1 on unreadable input, no matching requests, or a tied top code (decide by hand).
"""
import gzip, json, os, re, sys
from collections import Counter
from datetime import datetime, timezone

LINE = re.compile(r'^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:?\d\d))\s+(\w+)\s+(.*)$')

def parse_ts(s):
    s = s.replace('Z', '+00:00')
    s = re.sub(r'([+-]\d\d)(\d\d)$', r'\1:\2', s)
    return datetime.fromisoformat(s).astimezone(timezone.utc)

def main():
    a = sys.argv[1:]
    out = None
    if '--out' in a:
        i = a.index('--out'); out = a[i + 1]; del a[i:i + 2]
    if len(a) != 3:
        sys.exit(__doc__)
    d = a[0]
    lo = datetime.fromisoformat(a[1]).replace(tzinfo=timezone.utc)
    hi = datetime.fromisoformat(a[2]).replace(tzinfo=timezone.utc)
    attempts = {}  # req -> list of (utc, attempt_no, level, user, code)
    skipped = 0
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d, fn)
        if not os.path.isfile(p):
            continue
        with open(p, 'rb') as fh:
            gz = fh.read(2) == b'\x1f\x8b'
        with (gzip.open(p, 'rt', errors='replace') if gz else open(p, errors='replace')) as f:
            for raw in f:
                m = LINE.match(raw.rstrip('\n'))  # traceback lines start with spaces: no match
                if not m:
                    skipped += 1
                    continue
                kv = dict(re.findall(r'(\w+)=(\S+)', m.group(3)))
                if 'req' not in kv:  # lines without a request id (cache warm notes) are not attempts
                    skipped += 1
                    continue
                attempts.setdefault(kv['req'], []).append(
                    (parse_ts(m.group(1)), int(kv.get('attempt', 0)), m.group(2), kv.get('user'), kv.get('code')))
    failed, conflict = [], []
    for req, rows in attempts.items():
        last = max(rows, key=lambda r: r[0])
        if max(rows, key=lambda r: r[1]) is not last:
            conflict.append(req)
        if lo <= last[0] < hi and last[2] == 'ERROR':
            failed.append((req, last[3], last[4]))
    codes = Counter(c for _, _, c in failed)
    users = {u for _, u, _ in failed}
    top = codes.most_common()
    res = {"failed": len(failed), "users": len(users), "top_code": top[0][0] if top else None}
    audit = {"requests_seen": len(attempts), "non_attempt_lines_skipped": skipped,
             "code_counts": dict(top), "time_vs_attempt_no_disagree": sorted(conflict)}
    print(json.dumps({"answer": res, "audit": audit}, indent=1))
    if not top or (len(top) > 1 and top[0][1] == top[1][1]):
        print("ERROR: no failures or tied top code", file=sys.stderr); sys.exit(1)
    if out:
        os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
        with open(out, 'w') as f:
            json.dump(res, f)

if __name__ == "__main__":
    main()

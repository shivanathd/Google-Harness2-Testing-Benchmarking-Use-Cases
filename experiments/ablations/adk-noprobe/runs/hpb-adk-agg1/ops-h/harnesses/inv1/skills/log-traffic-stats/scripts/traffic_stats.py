#!/usr/bin/env python3
"""Per-service traffic statistics (requests, error_rate, p95_ms) from JSON-lines access logs (plain or .gz).

usage: traffic_stats.py START END LOG [LOG ...] [--exclude-route /healthz] [--list] [--write OUT.json]
  START inclusive, END exclusive; ISO with offset or Z (naive = UTC), e.g. 2026-10-04T06:00:00Z.
  Service name = file name up to the first '.' (logs/billing.jsonl.gz -> billing). Gzip detected by magic bytes.

Rules (override with flags only if the RUNBOOK says otherwise):
  - lines that are not valid JSON objects (truncated by the shipper) are skipped and counted;
  - the window test is on the UTC instant of `ts` (offsets are mixed inside one file, never filter on local hour text);
  - records on --exclude-route (default /healthz) are dropped before ANY statistic;
  - error = status >= 500 (4xx are not errors); error_rate = errors/requests rounded to 4 dp;
  - latency in ms: `latency_ms` if present, else `latency_s` * 1000 (schema change); p95 = nearest rank,
    sorted[ceil(0.95*n)-1], rounded to int.
Prints a per-service summary and skip tallies; --write dumps {service: {requests, error_rate, p95_ms}} and
refuses if a service has zero requests or a record lacks both latency fields / a usable status.
"""
import sys, json, gzip, argparse, collections
from datetime import datetime, timezone

def ts(s):
    d = datetime.fromisoformat(str(s).strip().replace('Z', '+00:00'))
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
ap.add_argument('--exclude-route', default='/healthz')
ap.add_argument('--list', action='store_true'); ap.add_argument('--write')
a = ap.parse_args()
lo, hi = ts(a.start), ts(a.end)

data = collections.OrderedDict(); tally = {}
problems = []
for path in a.logs:
    svc = path.replace('\\', '/').rsplit('/', 1)[-1].split('.')[0]
    data.setdefault(svc, []); t = tally.setdefault(svc, collections.Counter())
    for line in lines(path):
        if not line.strip(): continue
        try: r = json.loads(line)
        except ValueError: t['invalid_json'] += 1; continue
        if not isinstance(r, dict): t['invalid_json'] += 1; continue
        try: when = ts(r['ts'])
        except (KeyError, ValueError): t['bad_ts'] += 1; problems.append(f'{svc}: bad ts: {line}'); continue
        if not lo <= when < hi: t['outside_window'] += 1; continue
        if r.get('route') == a.exclude_route: t['excluded_route'] += 1; continue
        try: st = int(r['status'])
        except (KeyError, ValueError, TypeError): problems.append(f'{svc}: no usable status: {line}'); continue
        if 'latency_ms' in r: lat = float(r['latency_ms']); t['lat_ms'] += 1
        elif 'latency_s' in r: lat = round(float(r['latency_s']) * 1000, 6); t['lat_s'] += 1
        else: problems.append(f'{svc}: no latency field: {line}'); continue
        data[svc].append((when, st, lat, r.get('route')))
        if a.list: print(svc, when.strftime('%Y-%m-%dT%H:%M:%SZ'), r.get('route'), st, lat)

out = {}
for svc, recs in data.items():
    n = len(recs)
    if not n: problems.append(f'{svc}: zero requests in window'); continue
    errs = sum(1 for _, s, _, _ in recs if s >= 500)
    lats = sorted(l for _, _, l, _ in recs)
    k = -(-95 * n // 100)  # ceil(0.95*n) in integers
    p95 = lats[k - 1]
    out[svc] = {'requests': n, 'error_rate': round(errs / n, 4), 'p95_ms': int(round(p95))}
    print(f'{svc}: requests={n} errors={errs} raw_rate={errs/n:.6f} p95_rank={k} p95_raw={p95} -> {out[svc]}')
    print(f'  skipped: {dict(tally[svc])}')
for p in problems[:20]: print('WARNING:', p)
if a.write:
    if problems: sys.exit('not writing: resolve WARNINGs above')
    json.dump(out, open(a.write, 'w'))
    print('wrote', a.write, open(a.write).read())

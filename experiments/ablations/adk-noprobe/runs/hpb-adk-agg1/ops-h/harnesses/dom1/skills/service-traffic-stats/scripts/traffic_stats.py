#!/usr/bin/env python3
"""Per-service traffic statistics from JSON-lines access logs (plain or gzip).

usage: traffic_stats.py START END LOG [LOG ...] [--exclude-route /healthz] [--write OUT.json]
  START inclusive, END exclusive; ISO with offset or Z (naive = UTC), e.g. 2026-10-04T06:00:00Z.
  Service name = file name up to the first dot (logs/gateway.jsonl -> gateway, billing.jsonl.gz -> billing).
  Gzip is detected by magic bytes. Several files with the same service name are merged.

Rules: lines that are not valid JSON objects (shipper truncation) or lack ts/status are skipped and counted.
Every ts is converted to UTC before the window test. Probe route(s) are dropped before any statistic.
errors = status >= 500. Latency: latency_ms as is; latency_s * 1000 (rounded to whole ms to kill float noise),
chosen PER RECORD by which field the record carries. p95 = nearest rank: sorted ascending, element ceil(0.95*n).
error_rate = errors/requests rounded to 4 dp. Prints a table, skip tallies and field/unit census; --write
stores {service: {requests, error_rate, p95_ms}} (refuses if a service has no requests).
"""
import sys, json, gzip, math, argparse, collections
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
            yield l

ap = argparse.ArgumentParser()
ap.add_argument('start'); ap.add_argument('end'); ap.add_argument('logs', nargs='+')
ap.add_argument('--exclude-route', action='append', default=None)
ap.add_argument('--write')
a = ap.parse_args()
lo, hi = ts(a.start), ts(a.end)
excl = set(a.exclude_route or ['/healthz'])

svc = collections.OrderedDict()
for path in a.logs:
    name = path.replace('\\', '/').rsplit('/', 1)[-1].split('.')[0]
    s = svc.setdefault(name, dict(lat=[], err=0, n=0, bad=0, nofield=0, outwin=0, probe=0, units=collections.Counter()))
    for line in lines(path):
        if not line.strip(): continue
        try:
            d = json.loads(line)
            t = ts(d['ts']); status = int(d['status']); route = d.get('route')
            if not isinstance(d, dict): raise ValueError
        except Exception:
            s['bad'] += 1; continue
        if not (lo <= t < hi): s['outwin'] += 1; continue
        if route in excl: s['probe'] += 1; continue
        if 'latency_ms' in d: ms = float(d['latency_ms']); s['units']['latency_ms'] += 1
        elif 'latency_s' in d: ms = float(d['latency_s']) * 1000; s['units']['latency_s'] += 1
        else: s['nofield'] += 1; ms = None
        s['n'] += 1; s['err'] += status >= 500
        if ms is not None: s['lat'].append(round(ms))

out = {}
for name, s in svc.items():
    n = s['n']; lat = sorted(s['lat'])
    if not n or not lat:
        print(f'{name}: NO REQUESTS/LATENCIES in window'); continue
    p95 = lat[math.ceil(0.95 * len(lat)) - 1]
    out[name] = {'requests': n, 'error_rate': round(s['err'] / n, 4), 'p95_ms': int(p95)}
    print(f"{name}: requests={n} errors={s['err']} error_rate={s['err']/n:.6f} p95_ms={p95} (n_lat={len(lat)}, rank={math.ceil(0.95*len(lat))})")
    print(f"   skipped: invalid_json={s['bad']} outside_window={s['outwin']} probe_routes={s['probe']} no_latency_field={s['nofield']} units={dict(s['units'])}")
print(json.dumps(out))
if a.write:
    if len(out) != len(svc) or any(s['nofield'] for s in svc.values()):
        sys.exit('not writing: a service has no requests or records without a latency field')
    json.dump(out, open(a.write, 'w'))
    print('wrote', a.write)

#!/usr/bin/env python3
"""Per-service traffic stats from JSON-lines access logs (plain or .gz).

usage: python3 -I scripts/traffic_report.py LOGDIR START END [--write output/answer.json]
  START inclusive, END exclusive, ISO text, naive = UTC (e.g. 2026-10-04T06:00).
One service per file: logs/<service>.jsonl or <service>.jsonl.gz.
Per line: skip blank / invalid-JSON (truncated) / non-object lines; parse ts and
convert any UTC offset to UTC; apply the half-open window; drop route /healthz;
requests = remaining rows; errors = status >= 500; latency = latency_ms, or
latency_s * 1000 when only latency_s is present (decided per row, by key).
p95_ms = nearest rank: sorted[ceil(0.95*n)-1], as an integer.
Prints counts, skipped-line tallies and anomalies per service. --write emits
{service: {"requests","error_rate"(4dp),"p95_ms"}} and exits 1 without writing
if any service has zero rows or a row has no usable latency/status/ts.
"""
import argparse, glob, gzip, json, math, os, sys
from datetime import datetime, timezone

def utc(s):
    d = datetime.fromisoformat(str(s).replace('Z', '+00:00'))
    return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d.astimezone(timezone.utc)

ap = argparse.ArgumentParser()
ap.add_argument('logdir'); ap.add_argument('start'); ap.add_argument('end'); ap.add_argument('--write')
a = ap.parse_args()
start, end = utc(a.start), utc(a.end)
out, problems = {}, []
for p in sorted(glob.glob(os.path.join(a.logdir, '*.jsonl*'))):
    svc = os.path.basename(p).split('.jsonl')[0]
    op = gzip.open if p.endswith('.gz') else open
    n_bad = n_health = n_out = n_anom = n_s = 0
    lats, errs = [], 0
    with op(p, 'rt', encoding='utf-8', errors='replace') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except ValueError:
                n_bad += 1; continue
            try:
                if not isinstance(r, dict):
                    raise ValueError
                t = utc(r['ts']); status = int(r['status']); route = r['route']
                if 'latency_ms' in r:
                    lat = float(r['latency_ms'])
                else:
                    lat = round(float(r['latency_s']) * 1000, 6); n_s += 1
            except (KeyError, ValueError, TypeError):
                n_anom += 1; continue
            if not (start <= t < end):
                n_out += 1; continue
            if route == '/healthz':
                n_health += 1; continue
            lats.append(lat); errs += status >= 500
    n = len(lats)
    print(f'{svc}: file={os.path.basename(p)} in_window_requests={n} errors={errs} truncated_skipped={n_bad} '
          f'healthz_excluded={n_health} out_of_window={n_out} latency_s_rows_converted={n_s} unusable_rows={n_anom}')
    if not n or n_anom:
        problems.append(svc); continue
    s = sorted(lats); v = s[math.ceil(0.95 * n) - 1]
    out[svc] = {'requests': n, 'error_rate': round(errs / n, 4), 'p95_ms': int(round(v))}
print(json.dumps(out, indent=1))
if a.write:
    if problems:
        print('NOT WRITTEN: zero rows or unusable rows in', problems, file=sys.stderr); sys.exit(1)
    os.makedirs(os.path.dirname(a.write) or '.', exist_ok=True)
    json.dump(out, open(a.write, 'w'))
    print('wrote', a.write, open(a.write).read())

#!/usr/bin/env python3
"""Per-service traffic stats (requests, error_rate, p95_ms) from JSONL access logs.

usage: python3 -I traffic_stats.py LOGDIR START END [--write output/answer.json]
  START inclusive, END exclusive, ISO text, naive = UTC (e.g. 2026-10-04T06:00).
Reads LOGDIR/<service>.jsonl and LOGDIR/<service>.jsonl.gz. Skips lines that are not
valid JSON objects, excludes /healthz, converts every ts offset to UTC, counts
status >= 500 as errors, takes latency_ms as-is or latency_s * 1000, and uses
nearest-rank p95 (ceil(0.95*n)-th smallest) rounded to an integer.
Prints an audit table per service; --write emits {service: {requests, error_rate, p95_ms}}.
Exits 1 and writes nothing if any in-window record has no usable latency/status/ts.
"""
import argparse, glob, gzip, json, math, os, sys
from datetime import datetime, timezone

def utc(s):
    d = datetime.fromisoformat(s.replace('Z', '+00:00'))
    return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d.astimezone(timezone.utc)

ap = argparse.ArgumentParser()
ap.add_argument('logdir'); ap.add_argument('start'); ap.add_argument('end'); ap.add_argument('--write')
a = ap.parse_args()
start, end = utc(a.start), utc(a.end)
files = sorted(glob.glob(os.path.join(a.logdir, '*.jsonl')) + glob.glob(os.path.join(a.logdir, '*.jsonl.gz')))
out, problems = {}, 0
for f in files:
    svc = os.path.basename(f).split('.jsonl')[0]
    op = gzip.open if f.endswith('.gz') else open
    n_bad = n_out = n_hz = n_prob = 0
    keys, lat, errs = {}, [], 0
    with op(f, 'rt', encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                assert isinstance(r, dict)
            except Exception:
                n_bad += 1; continue
            try:
                ts = utc(r['ts'])
            except Exception:
                n_prob += 1; continue
            if not (start <= ts < end):
                n_out += 1; continue
            if r.get('route') == '/healthz':
                n_hz += 1; continue
            try:
                st = int(r['status'])
                if 'latency_ms' in r:
                    v = float(r['latency_ms']); k = 'latency_ms'
                else:
                    v = float(r['latency_s']) * 1000; k = 'latency_s'
            except Exception:
                n_prob += 1; continue
            keys[k] = keys.get(k, 0) + 1
            errs += st >= 500
            lat.append(v)
    problems += n_prob
    lat.sort(); n = len(lat)
    p95 = int(round(lat[math.ceil(0.95 * n) - 1])) if n else None
    rate = round(errs / n, 4) if n else None
    out[svc] = {'requests': n, 'error_rate': rate, 'p95_ms': p95}
    print(f'{svc}: requests={n} errors={errs} error_rate={rate} p95_ms={p95} | skipped invalid-JSON={n_bad} '
          f'out-of-window={n_out} healthz-in-window={n_hz} unusable={n_prob} latency-keys={keys}')
if problems:
    print('NOT WRITTEN: in-window records with missing/odd ts, status or latency', file=sys.stderr); sys.exit(1)
if a.write:
    json.dump(out, open(a.write, 'w'))
    print('wrote', a.write, open(a.write).read())

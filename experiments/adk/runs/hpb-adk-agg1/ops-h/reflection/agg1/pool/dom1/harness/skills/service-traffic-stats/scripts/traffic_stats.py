#!/usr/bin/env python3
"""Per-service requests / error_rate / p95_ms from JSON-lines access logs for a UTC window.

usage: traffic_stats.py LOG_DIR --start 2026-10-04T06:00:00Z --end 2026-10-04T12:00:00Z [--out output/answer.json]
Service name = file name up to the first '.' (gateway.jsonl -> gateway, billing.jsonl.gz -> billing).
Gzip detected by magic bytes. Lines that are not valid JSON objects (truncated) are skipped and counted.
Window [start, end) is applied to ts converted to UTC. route == /healthz is excluded.
Error = status >= 500. Latency = latency_ms, else latency_s * 1000 (rounded) per record.
p95 = nearest rank: sorted ascending, element ceil(0.95 * n) (1-based).
Exit 2: a record in the window lacks ts/status/latency or has an unparseable ts (inspect, do not guess).
Exit 3: a service has zero requests in the window.
"""
import argparse, glob, gzip, json, math, os, sys
from datetime import datetime, timezone

def utc(s):
    s = s.strip()
    if s.endswith('Z'):
        s = s[:-1] + '+00:00'
    t = datetime.fromisoformat(s)
    if t.tzinfo is None:
        sys.exit('timestamp needs an offset or Z: ' + s)
    return t.astimezone(timezone.utc)

def read_lines(path):
    raw = open(path, 'rb').read()
    if raw[:2] == b'\x1f\x8b':
        raw = gzip.decompress(raw)
    return raw.decode('utf-8', 'replace').splitlines()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('logdir'); ap.add_argument('--start', required=True)
    ap.add_argument('--end', required=True); ap.add_argument('--out')
    a = ap.parse_args()
    lo, hi = utc(a.start), utc(a.end)
    files = sorted(glob.glob(os.path.join(a.logdir, '*')))
    svc_files = {}
    for f in files:
        svc_files.setdefault(os.path.basename(f).split('.')[0], []).append(f)
    result = {}; problems = 0
    for svc, fs in svc_files.items():
        rows = []; bad = outside = hz = sec = 0
        for f in fs:
            for line in read_lines(f):
                if not line.strip():
                    continue
                try:
                    o = json.loads(line)
                    assert isinstance(o, dict)
                except Exception:
                    bad += 1; continue
                try:
                    t = utc(o['ts'])
                except Exception:
                    problems += 1; print('BAD TS:', svc, line, file=sys.stderr); continue
                if not (lo <= t < hi):
                    outside += 1; continue
                if o.get('route') == '/healthz':
                    hz += 1; continue
                try:
                    status = int(o['status'])
                    if 'latency_ms' in o:
                        lat = float(o['latency_ms'])
                    else:
                        lat = float(o['latency_s']) * 1000; sec += 1
                except Exception:
                    problems += 1; print('BAD RECORD:', svc, line, file=sys.stderr); continue
                rows.append((status, round(lat, 6)))
        n = len(rows)
        if n == 0:
            print(f'{svc}: no requests in window', file=sys.stderr); sys.exit(3)
        errs = sum(1 for s, _ in rows if s >= 500)
        lats = sorted(l for _, l in rows)
        k = math.ceil(0.95 * n)
        p95 = lats[k - 1]
        print(f'{svc}: files={len(fs)} requests={n} errors={errs} rank={k}/{n} p95_raw={p95} '
              f'skipped: invalid_json={bad} outside_window={outside} healthz={hz} latency_s_rows={sec}'
              f'  top5_latency={lats[-5:]}', file=sys.stderr)
        result[svc] = {'requests': n, 'error_rate': round(errs / n, 4), 'p95_ms': int(round(p95))}
    if problems:
        sys.exit(2)
    print(json.dumps(result))
    if a.out:
        os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
        json.dump(result, open(a.out, 'w'))

main()

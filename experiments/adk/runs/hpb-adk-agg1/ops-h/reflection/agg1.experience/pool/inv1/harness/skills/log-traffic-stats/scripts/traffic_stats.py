#!/usr/bin/env python3
"""Per-service requests / error_rate / p95_ms from JSON-lines access logs.

usage: traffic_stats.py LOGDIR --start ISO --end ISO [--out output/answer.json]
                        [--exclude-route /healthz] [--error-status 500]
Window is [start, end) in UTC; timestamps with any offset are converted to UTC.
Files: LOGDIR/<service>.jsonl or .jsonl.gz (gzip detected by magic bytes).
Latency: `latency_ms` if present, else `latency_s`*1000 (per line, by key).
Exit 0 ok; 2 = a kept line has a missing/odd field (printed, nothing written);
3 = a service has zero requests in the window (nothing written).
"""
import argparse, glob, gzip, json, math, os, sys
from datetime import datetime, timezone


def parse_ts(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    d = datetime.fromisoformat(s)
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)


def lines(path):
    raw = open(path, "rb").read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", "replace").splitlines()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logdir")
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--out", default="output/answer.json")
    ap.add_argument("--exclude-route", default="/healthz")
    ap.add_argument("--error-status", type=int, default=500)
    a = ap.parse_args()
    start, end = parse_ts(a.start), parse_ts(a.end)

    svcs = {}
    for p in sorted(glob.glob(os.path.join(a.logdir, "*.jsonl*"))):
        svcs.setdefault(os.path.basename(p).split(".jsonl")[0], []).append(p)

    result, problems = {}, []
    for svc, paths in svcs.items():
        total = skipped = health = outside = 0
        lat, errs = [], 0
        for p in paths:
            for i, line in enumerate(lines(p), 1):
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                    assert isinstance(d, dict)
                except Exception:
                    skipped += 1  # truncated/invalid line: runbook says skip
                    continue
                try:
                    t = parse_ts(d["ts"])
                except Exception:
                    problems.append(f"{p}:{i} bad ts: {line[:100]}")
                    continue
                if not (start <= t < end):
                    outside += 1
                    continue
                if d.get("route") == a.exclude_route:
                    health += 1
                    continue
                try:
                    status = int(d["status"])
                    if "latency_ms" in d:
                        ms = float(d["latency_ms"])
                    else:
                        ms = float(d["latency_s"]) * 1000.0
                except Exception:
                    problems.append(f"{p}:{i} missing status/latency: {line[:100]}")
                    continue
                total += 1
                errs += status >= a.error_status
                lat.append(round(ms, 6))
        lat.sort()
        n = len(lat)
        print(f"{svc}: kept={n} errors={errs} skipped_invalid={skipped} "
              f"healthz_excluded={health} outside_window={outside}", file=sys.stderr)
        if n == 0:
            problems.append(f"{svc}: zero requests in window")
            continue
        p95 = lat[math.ceil(0.95 * n) - 1]  # nearest rank: ceil(0.95*n)-th smallest
        if abs(p95 - round(p95)) > 1e-4:
            print(f"  note {svc}: p95 {p95} not whole ms, rounded", file=sys.stderr)
        result[svc] = {"requests": n, "error_rate": round(errs / n, 4), "p95_ms": int(round(p95))}

    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 3 if any("zero requests" in x for x in problems) else 2
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(result, f)
    print(json.dumps(result))
    return 0


sys.exit(main())

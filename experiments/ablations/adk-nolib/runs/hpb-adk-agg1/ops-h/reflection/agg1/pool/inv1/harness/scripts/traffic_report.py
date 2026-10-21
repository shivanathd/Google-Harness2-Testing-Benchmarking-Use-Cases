#!/usr/bin/env python3
"""Per-service traffic stats from JSONL access logs (plain or .gz).

usage: python3 scripts/traffic_report.py START END [--logs logs] [--out output/answer.json]
  START/END: ISO timestamps with offset, e.g. 2026-10-04T06:00:00+00:00 (END exclusive;
  a bare 'Z' or no offset is read as UTC).
Writes {service: {requests, error_rate, p95_ms}} and prints per-service diagnostics
(skipped lines, excluded health probes, latency units used) to stderr.
Exit 1 if no log files are found or a service ends up with zero requests.
"""
import argparse, glob, gzip, json, math, os, sys
from datetime import datetime, timezone

def parse_ts(s):
    d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d

def lat_ms(r):
    # per-record unit: latency_ms is ms, latency_s is seconds (billing after its schema change)
    if r.get("latency_ms") is not None:
        return float(r["latency_ms"]), "ms"
    if r.get("latency_s") is not None:
        return float(r["latency_s"]) * 1000.0, "s"
    return None, None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("start"); ap.add_argument("end")
    ap.add_argument("--logs", default="logs"); ap.add_argument("--out", default="output/answer.json")
    ap.add_argument("--exclude-route", default="/healthz")
    a = ap.parse_args()
    t0, t1 = parse_ts(a.start), parse_ts(a.end)
    files = sorted(glob.glob(os.path.join(a.logs, "*.jsonl")) + glob.glob(os.path.join(a.logs, "*.jsonl.gz")))
    if not files:
        sys.exit("no *.jsonl / *.jsonl.gz files in " + a.logs)
    out = {}
    for f in files:
        name = os.path.basename(f).split(".jsonl")[0]
        op = gzip.open if f.endswith(".gz") else open
        bad = health = outside = 0
        lats, errs, units = [], 0, {}
        with op(f, "rt", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    ts = parse_ts(r["ts"]); status = int(r["status"]); route = str(r["route"])
                    ms, u = lat_ms(r)
                    if not isinstance(r, dict) or ms is None:
                        raise ValueError
                except Exception:
                    bad += 1; continue
                if route.split("?")[0] == a.exclude_route:
                    health += 1; continue
                if not (t0 <= ts < t1):
                    outside += 1; continue
                lats.append(round(ms, 6)); units[u] = units.get(u, 0) + 1
                errs += status >= 500
        n = len(lats)
        print(f"{name}: kept={n} errors={errs} unparseable={bad} healthz={health} out_of_window={outside} units={units}", file=sys.stderr)
        if n == 0:
            sys.exit(f"{name}: zero requests in window - check window/offsets")
        lats.sort()
        p95 = lats[math.ceil(0.95 * n) - 1]  # nearest rank
        out[name] = {"requests": n, "error_rate": round(errs / n, 4), "p95_ms": int(round(p95))}
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out))

if __name__ == "__main__":
    main()

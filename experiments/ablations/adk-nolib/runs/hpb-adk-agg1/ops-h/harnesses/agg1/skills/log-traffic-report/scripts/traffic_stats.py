#!/usr/bin/env python3
"""Per-service requests / error_rate / p95_ms from JSONL access logs.

usage: python3 skills/log-traffic-report/scripts/traffic_stats.py LOGDIR START END [OUT_JSON]
  START/END are UTC ISO instants, e.g. 2026-10-04T06:00:00+00:00 (END exclusive).
Reads LOGDIR/*.jsonl and *.jsonl.gz. Prints a per-service audit line to stderr and the
answer dict to stdout (also written to OUT_JSON if given).
"""
import glob, gzip, json, math, os, sys
from datetime import datetime, timezone


def parse_utc(s):
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def latency_ms(rec):
    if "latency_ms" in rec:
        return float(rec["latency_ms"])
    if "latency_s" in rec:
        return round(float(rec["latency_s"]) * 1000, 3)
    return None


def main():
    logdir, start, end = sys.argv[1], parse_utc(sys.argv[2]), parse_utc(sys.argv[3])
    out = {}
    files = sorted(glob.glob(os.path.join(logdir, "*.jsonl")) + glob.glob(os.path.join(logdir, "*.jsonl.gz")))
    for path in files:
        svc = os.path.basename(path).split(".jsonl")[0]
        opener = gzip.open if path.endswith(".gz") else open
        bad = health = outside = 0
        rows = []
        with opener(path, "rt") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    r = json.loads(line)
                    t = parse_utc(r["ts"]).astimezone(timezone.utc)
                    st = int(r["status"])
                    lat = latency_ms(r)
                    route = r["route"]
                    if lat is None:
                        raise ValueError("no latency")
                except (ValueError, KeyError, TypeError):
                    bad += 1
                    continue
                if not (start <= t < end):
                    outside += 1
                    continue
                if route == "/healthz":
                    health += 1
                    continue
                rows.append((st, lat))
        n = len(rows)
        errs = sum(1 for s, _ in rows if s >= 500)
        lats = sorted(l for _, l in rows)
        k = -(-95 * n // 100)  # nearest rank: ceil(0.95*n), integer arithmetic
        p95 = lats[k - 1] if n else None
        out[svc] = {"requests": n,
                    "error_rate": round(errs / n, 4) if n else None,
                    "p95_ms": int(round(p95)) if n else None}
        print(f"{svc}: file={path} unparseable_skipped={bad} outside_window={outside} "
              f"healthz_excluded={health} requests={n} errors={errs} rank={k} p95_raw={p95}",
              file=sys.stderr)
    text = json.dumps(out)
    if len(sys.argv) > 4:
        os.makedirs(os.path.dirname(sys.argv[4]) or ".", exist_ok=True)
        with open(sys.argv[4], "w") as f:
            f.write(text)
    print(text)


main()

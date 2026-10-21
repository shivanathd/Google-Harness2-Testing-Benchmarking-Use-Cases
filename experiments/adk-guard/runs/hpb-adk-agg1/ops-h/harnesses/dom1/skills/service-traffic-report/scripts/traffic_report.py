#!/usr/bin/env python3
"""Per-service requests / error_rate / p95_ms from JSON-lines access logs.

usage: traffic_report.py START END FILE [FILE ...] [--out output/answer.json]
START/END: ISO with offset (e.g. 2026-10-04T06:00+00:00); window is [START, END).
Service name = file name up to the first '.'; .gz files are decompressed.
"""
import gzip, json, sys
from datetime import datetime, timezone

def parse(ts):
    d = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if d.tzinfo is None:
        raise ValueError("no offset")
    return d.astimezone(timezone.utc)

def main(argv):
    out = None
    if "--out" in argv:
        i = argv.index("--out"); out = argv[i + 1]; del argv[i:i + 2]
    start, end, files = parse(argv[0]), parse(argv[1]), argv[2:]
    result = {}
    for f in files:
        svc = f.replace("\\", "/").split("/")[-1].split(".")[0]
        op = gzip.open if f.endswith(".gz") else open
        lat, errs, skipped, health, outside, sec = [], 0, 0, 0, 0, 0
        for ln in op(f, "rt", encoding="utf-8", errors="replace"):
            ln = ln.strip()
            if not ln:
                continue
            try:
                d = json.loads(ln)
                t = parse(d["ts"]); status = int(d["status"])
                if "latency_ms" in d:
                    ms = float(d["latency_ms"])
                else:
                    ms = float(d["latency_s"]) * 1000; sec += 1
            except Exception:
                skipped += 1; continue
            if d.get("route") == "/healthz":
                health += 1; continue
            if not (start <= t < end):
                outside += 1; continue
            lat.append(round(ms))
            errs += status >= 500
        lat.sort(); n = len(lat)
        rank = (95 * n + 99) // 100  # ceil(0.95*n), exact integer arithmetic
        result[svc] = {"requests": n,
                       "error_rate": round(errs / n, 4) if n else 0.0,
                       "p95_ms": int(lat[rank - 1]) if n else 0}
        print(f"{svc}: file={f} requests={n} errors={errs} rank={rank} "
              f"skipped_bad_lines={skipped} healthz_excluded={health} "
              f"outside_window={outside} latency_s_rows_in_file={sec}", file=sys.stderr)
    print(json.dumps(result))
    if out:
        with open(out, "w") as fh:
            json.dump(result, fh)

main(sys.argv[1:])

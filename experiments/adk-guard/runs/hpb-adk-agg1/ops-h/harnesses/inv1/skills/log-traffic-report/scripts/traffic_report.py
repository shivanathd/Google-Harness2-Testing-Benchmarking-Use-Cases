#!/usr/bin/env python3
"""Per-service traffic statistics from JSON-lines access logs (plain or .gz).
usage: traffic_report.py START END LOGFILE [LOGFILE ...] [--out output/answer.json]
START/END: ISO timestamps (naive = UTC); window is start-inclusive, end-exclusive, judged in UTC.
Service name = file name up to the first '.', e.g. logs/billing.jsonl.gz -> billing.
Rules: lines that are not valid JSON objects (or lack ts/status/latency) are skipped and counted;
/healthz is excluded; error = status >= 500; latency is latency_ms, else latency_s * 1000
(per line, so a mid-file schema change is handled); p95 = nearest rank, ceil(0.95*n)-th smallest.
Prints an audit table to stdout; with --out also writes {"service": {"requests","error_rate","p95_ms"}}.
Exit 1 if a file is unreadable or a service has zero in-window requests."""
import collections, gzip, json, math, sys
from datetime import datetime, timezone

def utc(s):
    d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d.astimezone(timezone.utc)

args = sys.argv[1:]
out = None
if "--out" in args:
    i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
if len(args) < 3:
    sys.exit(__doc__)
lo, hi = utc(args[0]), utc(args[1])
result, bad_exit = {}, False
for path in args[2:]:
    svc = path.replace("\\", "/").split("/")[-1].split(".")[0]
    try:
        raw = open(path, "rb").read()
        if raw[:2] == b"\x1f\x8b":
            raw = gzip.decompress(raw)
    except Exception as e:
        print("ERROR reading", path, e); bad_exit = True; continue
    c = collections.Counter(); lat = []; errs = 0
    for n, line in enumerate(raw.decode("utf-8", "replace").splitlines(), 1):
        if not line.strip():
            continue
        try:
            d = json.loads(line)
            t = utc(d["ts"]); status = int(d["status"])
            ms = float(d["latency_ms"]) if "latency_ms" in d else float(d["latency_s"]) * 1000
            route = d.get("route")
        except Exception:
            c["skipped_bad_line"] += 1; continue
        if route == "/healthz":
            c["healthz_excluded"] += 1; continue
        if not (lo <= t < hi):
            c["outside_window"] += 1; continue
        if "latency_ms" not in d:
            c["from_latency_s"] += 1
        lat.append(ms); errs += status >= 500
    n = len(lat)
    print(svc, "requests=%d errors=%d" % (n, errs), dict(c))
    if not n:
        print("ERROR: no in-window requests for", svc); bad_exit = True; continue
    lat.sort()
    p95 = round(lat[math.ceil(0.95 * n) - 1])
    result[svc] = {"requests": n, "error_rate": round(errs / n, 4), "p95_ms": int(p95)}
print(json.dumps(result))
if out and not bad_exit:
    import os
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    json.dump(result, open(out, "w"))
    print("wrote", out, "->", json.load(open(out)) == result)
sys.exit(1 if bad_exit else 0)

---
name: service-traffic-stats
description: Per-service requests, error_rate and p95 latency over a UTC window from JSON-lines access logs (mixed UTC offsets, gzip file, truncated lines, /healthz probe, latency unit change). Use for any traffic/incident statistics task over logs/ governed by a RUNBOOK.md.
---

# Traffic statistics from per-service access logs

Read RUNBOOK.md first: it is the controlling source for what counts as a request, an error, and which latency unit each service/period uses. Then run one command (all files, gzip by magic bytes; never read the .gz with read_file, it is binary):

    python3 skills/service-traffic-stats/scripts/traffic_stats.py logs --start 2026-10-04T06:00:00Z --end 2026-10-04T12:00:00Z --out output/answer.json

Adjust window to the task (start inclusive, end exclusive, UTC). It prints per-service tallies on stderr and writes `{service: {requests, error_rate, p95_ms}}`. Service = file name stem. If the task names other keys/services, rename to match; write only what was asked.
Exit 2 = a record in the window lacked ts/status/latency: inspect, decide, don't rerun unchanged. Exit 3 = a service has no rows in window. If the script can't run, do the same steps in a short .py file, not a shell one-liner or by eye.

## Rules the script encodes (check against RUNBOOK.md if it differs)
1. Skip lines that are not valid JSON (shipper truncation). Count them; don't repair them.
2. Window on `ts` converted to UTC. Local clock text is wrong: logs mix -03:00, +01:00, +00:00 and are not in time order, so a 06:xx+01:00 row is 05:xx UTC (outside) and 03:xx-03:00 is 06:xx UTC (inside).
3. Drop route `/healthz` from every statistic (requests, errors and latency), whatever its status.
4. Error = status >= 500 only; 429/404 are not errors. error_rate = errors / requests after the exclusions, round to 4 decimals.
5. Latency in ms. Records with `latency_s` are seconds: multiply by 1000 before pooling. Decide per record by which key it has (the cut-over is 2026-10-04 09:00 UTC; verify the key matches that boundary).
6. p95 nearest rank: sort all kept latencies ascending, take element ceil(0.95*n) (1-based) -- no interpolation, no numpy default. Integer output.

## Workspace fact (this task's logs/: gateway.jsonl, search.jsonl, billing.jsonl.gz; 260 lines each)
Verified by independent computation for 2026-10-04 06:00Z-12:00Z; use as a cross-check, not a substitute for running:
- gateway: requests=96, errors=13, error_rate=0.1354, p95_ms=334 (18 truncated lines)
- search: requests=119, errors=18, error_rate=0.1513, p95_ms=192 (5 truncated)
- billing: requests=124, errors=20, error_rate=0.1613, p95_ms=393 (10 truncated; 128 rows latency_ms before 09:00Z, 122 rows latency_s from 09:00Z; routes /v1/charge, /v1/invoice)
Traps present: billing p95 is wrong if latency_s is not scaled (seconds values would be ~0.1-0.7); healthz rows with 5xx/429 status exist and must not count as errors; window edges differ from local clock.

## Finish
Reopen output/answer.json: valid JSON, exactly the three services each with requests (int), error_rate (float, 4 dp), p95_ms (int).

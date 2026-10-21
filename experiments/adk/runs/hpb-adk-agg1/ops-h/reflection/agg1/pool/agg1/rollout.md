[ACTION] load_skill {"name": "log-traffic-stats"}
[OBSERVATION]
---
name: log-traffic-stats
description: Compute per-service requests, error_rate and nearest-rank p95 latency from JSON-lines access logs (some gzip, mixed UTC offsets, truncated lines, health-probe routes, schema changes) for a UTC time window, and write the answer JSON. Use for any traffic/incident statistics task over a logs/ directory.
---

# Traffic statistics from access logs

Do NOT read the log files with read_file (it truncates long files, shows .gz as binary, and the 40-call budget is spent by re-reading). One command does everything:

    python3 skills/log-traffic-stats/scripts/traffic_stats.py logs --start 2026-10-04T06:00:00Z --end 2026-10-04T12:00:00Z --out output/answer.json

Adjust the window (start inclusive, end exclusive, UTC) and service set to the task; services are taken from the files in the directory. Read RUNBOOK.md first (one read) and pass `--exclude-route` / `--error-status` if it differs from the defaults (/healthz, >=500). The script prints per-service tallies on stderr and the JSON on stdout.

Exit 2 = a line in the window lacks status/latency: read the printed lines, decide, do not rerun unchanged. Exit 3 = a service has no requests in the window: check the window/paths, report rather than guess. If python cannot run at all, write the same logic in a short .py file; do not eyeball counts.

## Rules the script encodes (from the runbook)
1. Skip lines that are not valid JSON (shipper truncation) - they are not requests.
2. Window uses each line's timestamp converted to UTC from its own offset (+01:00, -03:00, +00:00 all appear in one file; files are not in time order).
3. Exclude the health probe route from every statistic (requests, errors, latency) - including its 5xx rows.
4. error = status >= 500; 4xx (404, 429) are not errors. error_rate = errors/requests, round 4 decimals.
5. Latency unit is chosen per line by key: `latency_ms` as is, `latency_s` x1000. p95 = ceil(0.95*n)-th smallest of the kept latencies (nearest rank, no interpolation), integer ms.

## Workspace fact (logs/ with gateway.jsonl, search.jsonl, billing.jsonl.gz; 260 lines each)
Billing switches from `latency_ms` to `latency_s` exactly at 09:00 UTC on 2026-10-04 (key presence matches the time on every valid line), so the window straddles both units. For 2026-10-04 06:00Z-12:00Z the script gave: gateway 96 req, 13 errors, 0.1354, p95 334; search 119, 18, 0.1513, 192; billing 124, 20, 0.1613, 393. Use only as a cross-check if the same logs/window recur.

## Finish
Reopen output/answer.json: valid JSON, exactly the requested services and keys (requests int, error_rate float, p95_ms int). Then stop.

[ACTION] run_command {"command": "python3 skills/log-traffic-stats/scripts/traffic_stats.py logs --start 2026-10-04T06:00:00Z --end 2026-10-04T12:00:00Z --out output/answer.json"}
[OBSERVATION]
exit=0
{"billing": {"requests": 124, "error_rate": 0.1613, "p95_ms": 393}, "gateway": {"requests": 96, "error_rate": 0.1354, "p95_ms": 334}, "search": {"requests": 119, "error_rate": 0.1513, "p95_ms": 192}}
billing: kept=124 errors=20 skipped_invalid=10 healthz_excluded=32 outside_window=94
gateway: kept=96 errors=13 skipped_invalid=18 healthz_excluded=43 outside_window=103
search: kept=119 errors=18 skipped_invalid=5 healthz_excluded=29 outside_window=107

[ACTION] write_file {"path": "output/answer.json", "content": "{\"gateway\": {\"requests\": 96, \"error_rate\": 0.1354, \"p95_ms\": 334}, \"search\": {\"requests\": 119, \"error_rate\": 0.1513, \"p95_ms\": 192}, \"billing\": {\"requests\": 124, \"error_rate\": 0.1613, \"p95_ms\": 393}}"}
[OBSERVATION]
wrote 199 chars to output/answer.json
[ASSISTANT] {
  "gateway": {
    "requests": 96,
    "error_rate": 0.1354,
    "p95_ms": 334
  },
  "search": {
    "requests": 119,
    "error_rate": 0.1513,
    "p95_ms": 192
  },
  "billing": {
    "requests": 124,
    "error_rate": 0.1613,
    "p95_ms": 393
  }
}
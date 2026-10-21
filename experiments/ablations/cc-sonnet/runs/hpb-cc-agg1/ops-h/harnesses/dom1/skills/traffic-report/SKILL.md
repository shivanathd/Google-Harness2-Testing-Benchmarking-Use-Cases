---
name: traffic-report
description: Per-service traffic report (requests, error_rate, p95 latency) from multi-timezone JSONL access logs for a UTC window, following a runbook. Use for any request-count / error-rate / percentile task over service logs.
---

# Traffic report from access logs

ANALYTIC MOVE: calculate per-service requests, error_rate and p95 over a UTC window from raw log lines. The RUNBOOK.md in the workspace controls the definitions; re-read it first, because exclusions, error threshold and schema changes are set there, not by convention.

## Counting rules (check each against RUNBOOK.md)
1. Parse: skip lines that are not valid JSON objects (shipper truncation). Do not repair them, and do not count them toward requests. Report the skipped count per service.
2. Window: convert every `ts` to UTC using its own offset (offsets can be mixed within one file) BEFORE comparing. START inclusive, END exclusive. File order is not time order; never slice by line position or by the local hour text.
3. Exclude the probe route (the route the runbook names, typically `/healthz`) from requests, errors AND latency, after window filtering.
4. Errors: status >= 500 only. 4xx (404, 429) are not errors but remain in the requests denominator.
5. Latency unit: take `latency_ms` as-is; where only `latency_s` exists multiply by 1000. Decide per record by which key it has, not by service or file position. Then confirm the cut-over: cross-tab in-window records by UTC hour and key, and check the switch falls where the runbook says (UTC time, not local hour text). Confirm gzip-compressed log files were read too.
6. p95 nearest-rank: sort ascending, take element number ceil(0.95*n) (1-based). No interpolation. Round to integer only at the end (round, not truncate, after the x1000 float conversion).
7. error_rate = errors / requests, rounded to 4 decimals, as a number.

## Helper
`python3 -I skills/traffic-report/scripts/traffic_stats.py LOGDIR START END` prints the audit line per service (START/END are ISO text, naive = UTC, copied from the runbook/task); add `--write output/answer.json` to emit {service: {requests, error_rate, p95_ms}}. The output keys and order must match the task's wording exactly; if the task names different keys or services, write the file yourself from the printed numbers.

## Before finishing
- output file exists, parses, has exactly the services and the three keys asked for, requests/p95_ms are ints, error_rate is a float with <= 4 decimals.
- requests + healthz + invalid-JSON + out-of-window lines account for each file's line count (no silent drops).
- Final reply states the skipped-line counts and the unit conversion applied.

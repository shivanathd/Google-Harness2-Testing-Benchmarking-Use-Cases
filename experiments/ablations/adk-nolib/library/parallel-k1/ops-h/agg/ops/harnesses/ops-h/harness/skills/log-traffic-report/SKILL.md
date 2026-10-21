---
name: log-traffic-report
description: Compute per-service request count, error rate and p95 latency for a UTC time window from JSONL access logs (mixed timezone offsets, gzip, truncated lines, healthz probe, latency unit change), following the fleet RUNBOOK.
---

# Service-log traffic statistics

Controlling source: `RUNBOOK.md` in the workspace (re-read it; its rules override this file if they differ).
The task's window is in UTC and is start-inclusive, end-exclusive.

## Rules to apply to every line (check each before finishing)
1. Parse each line as JSON; skip lines that fail (shipper truncation). Count them per file; do not guess the missing fields.
2. Timestamps carry mixed offsets within ONE file (in this workspace: -03:00, +00:00, +01:00 in all three services, and files are not time-sorted). Convert every `ts` to UTC before the window test. Never filter on the local clock text or on file position.
3. Drop route `/healthz` (any status) before computing requests, errors and percentiles.
4. requests = remaining in-window lines, all statuses (2xx, 3xx, 4xx, 5xx). errors = status >= 500 only; 429/404 are not errors. error_rate = errors / requests, round to 4 decimals.
5. Latency in ms. Records with `latency_s` are seconds: multiply by 1000. Decide per record by which field it has, not by file name (in this workspace billing has both fields; `latency_s` appears only from 09:00 UTC on, so the window mixes both units; other services only have `latency_ms`). Never feed raw seconds into the percentile.
6. p95 nearest-rank: sort ascending, rank = ceil(0.95 * n) (1-based), take that element, output as integer. No interpolation. Compute ceil with integer arithmetic to avoid float error.
7. Gzip logs (`billing.jsonl.gz` in this workspace) are read as text via gzip; `logs/billing.jsonl` does not exist.

## How
`read_file` output is capped (≈65 lines, cut mid-line) so the logs cannot be hand-tallied from it; re-reading the same range returns the same text. Run the helper instead:

    python3 skills/log-traffic-report/scripts/traffic_stats.py logs 2026-10-04T06:00:00+00:00 2026-10-04T12:00:00+00:00 output/answer.json

(adjust window to the task). It prints per-service audit counts to stderr (unparseable, outside window, healthz excluded). If no shell is available, page with `start_line`/small `max_lines` and tally with explicit UTC conversion; never submit estimates.

## Before finishing
- answer.json has exactly the keys the task names, `requests` int, `error_rate` float (4 dp), `p95_ms` int, for every service in logs/ (gateway, search, billing here).
- Sanity: requests + healthz + outside-window + unparseable = total lines per file; error_rate in [0,1]; p95_ms lies in a plausible ms range (hundreds, not 0.4 — that would be unconverted seconds).

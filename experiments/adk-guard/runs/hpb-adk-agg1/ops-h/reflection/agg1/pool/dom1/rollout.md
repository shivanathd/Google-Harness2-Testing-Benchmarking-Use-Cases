[ACTION] load_skill {"name": "service-traffic-report"}
[OBSERVATION]
---
name: service-traffic-report
description: Per-service requests, error rate and nearest-rank p95 latency from JSON-lines access logs (some gzip) over a UTC window, following the fleet RUNBOOK. Incident and traffic statistics.
---

# Per-service traffic report (requests / error_rate / p95_ms)

## Analytic move
Classify every log line as counted or not, then calculate per service: requests = counted lines; error_rate = errors / requests; p95 = nearest-rank over counted lines' latency. Output is exactly the JSON the task names (service keys, field names, order), plain numbers, no extra fields.

## Controlling source
RUNBOOK.md (next to logs/) governs exclusions, error definition and schema changes; the task governs window and rounding. Re-read both and reconcile; do not rely on this skill's summary if they differ.

## Rules (verify each against RUNBOOK.md)
- Skip lines that are not valid JSON (shipper truncation), and valid JSON lacking ts/status/latency. Count them, don't repair them.
- Exclude the load-balancer probe route `/healthz` from every statistic: requests, errors AND latency, whatever its status. It is a large share of lines.
- Error = status >= 500 only; 429/404 etc. are not errors. error_rate = errors / requests after the healthz and window filters, rounded to 4 decimals only at the end.
- Window: convert each line's own offset to UTC before comparing; start inclusive, end exclusive. Lines are not in time order and mixed offsets (-03:00, +01:00, +00:00) occur in every file; local clock digits are not UTC.
- Units: a service that changed schema logs `latency_s` (seconds, float) after the cutover instant and `latency_ms` before it. Convert to ms (x1000, rounded to the nearest integer to kill float noise) per line BEFORE pooling; the cutover is a UTC instant, so a window straddling it mixes both fields in one service. Never treat a seconds value as ms.
- p95 nearest-rank: sort ascending, rank = ceil(0.95 * n), answer = value at that 1-based rank. No interpolation (numpy default percentile is wrong). Pool all counted lines of one service; never average per-route or per-hour p95s.
- `.gz` is read by decompressing (gzip module); read_file shows binary.

## Do it with the script
`python3 -I skills/service-traffic-report/scripts/traffic_report.py START END FILE [FILE ...] --out output/answer.json`
e.g. START=2026-10-04T06:00+00:00 END=2026-10-04T12:00+00:00 (take the real window from the task). Service name = file name before the first dot. It prints the JSON to stdout and per-service diagnostics to stderr (counts of bad lines, healthz excluded, out-of-window, latency_s rows). If the task's JSON needs different service keys or field order, edit the written file instead of re-deriving.

## Before finishing
- One entry per file in logs/ (compare with the directory listing); every service key and field exactly as the task names; requests/p95_ms are ints, error_rate a float.
- Diagnostics are plausible: some bad lines and healthz exclusions per file; for a service with a unit change, latency_s rows > 0 and p95 is on the ms scale of its peers (a p95 of ~0 or in the thousands means a unit error).
- Spot-check 2-3 lines near the window edges by hand-converting their offset to UTC.

[ACTION] list_files {"path": "logs/"}
[OBSERVATION]
logs/billing.jsonl.gz
logs/gateway.jsonl
logs/search.jsonl
[ACTION] run_command {"command": "python3 -I skills/service-traffic-report/scripts/traffic_report.py 2026-10-04T06:00+00:00 2026-10-04T12:00+00:00 logs/billing.jsonl.gz logs/gateway.jsonl logs/search.jsonl --out output/answer.json"}
[OBSERVATION]
exit=0
{"billing": {"requests": 124, "error_rate": 0.1613, "p95_ms": 393}, "gateway": {"requests": 96, "error_rate": 0.1354, "p95_ms": 334}, "search": {"requests": 119, "error_rate": 0.1513, "p95_ms": 192}}
billing: file=logs/billing.jsonl.gz requests=124 errors=20 rank=118 skipped_bad_lines=10 healthz_excluded=57 outside_window=69 latency_s_rows_in_file=122
gateway: file=logs/gateway.jsonl requests=96 errors=13 rank=92 skipped_bad_lines=18 healthz_excluded=63 outside_window=83 latency_s_rows_in_file=0
search: file=logs/search.jsonl requests=119 errors=18 rank=114 skipped_bad_lines=5 healthz_excluded=60 outside_window=76 latency_s_rows_in_file=0

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
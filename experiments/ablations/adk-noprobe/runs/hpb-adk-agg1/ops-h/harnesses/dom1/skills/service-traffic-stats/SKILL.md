---
name: service-traffic-stats
description: Per-service request count, error rate and nearest-rank p95 latency from JSON-lines access logs (some gzipped, mixed UTC offsets, truncated lines, probe routes, latency unit change) inside a UTC window, following the task's RUNBOOK.
---
# Traffic report from access logs

Analytic move: CALCULATE per service, over records (one JSON line = one request) in a half-open UTC window: requests, error_rate, p95_ms. The RUNBOOK.md next to the logs is the controlling source for exclusions, the error definition and schema changes: read it first and apply it literally; where it and your habits differ, the RUNBOOK wins. Output keys/shape come from the task text only (no extra fields).

Run the helper (works on plain and gzip files; service = file name stem), using every file in logs/:
`python3 skills/service-traffic-stats/scripts/traffic_stats.py <START_UTC> <END_UTC> logs/<each file> --write output/answer.json`
(START/END are the task's window, ISO UTC; the helper's rules are listed in its docstring. Add `--exclude-route` if the RUNBOOK names a probe other than /healthz.) If no shell exists, you cannot read the .gz with read_file: say so in the reply, and do the same rules by hand on the plain files, listing every counted record.

Rules to confirm against the RUNBOOK before trusting the output:
- Truncated shipper lines are not valid JSON: skip them (the helper prints the tally; a count > 0 is expected, a count of 0 on a large file is suspicious).
- Probe route (/healthz) is excluded from requests, errors AND latency, for every service, before computing anything.
- Error = status >= 500 only. 4xx (404, 429) are not errors. Denominator = requests after exclusions.
- Window test on the UTC instant, never on local clock text: files mix offsets (e.g. -03:00, +00:00, +01:00) and are not in time order, so a +01:00 stamp is one hour earlier in UTC.
- Latency units: convert to milliseconds per record by which field it carries (latency_s x 1000, round to whole ms to avoid 0.074*1000=74.00000000000001). Do not decide units by file or by local hour; the helper's `units=` census shows which fields each service carries; a service that switched units must show both.
- p95 nearest rank: sort ascending, take element ceil(0.95 x n) (1-based) of the n retained latencies; integer, no interpolation. error_rate rounded to 4 decimals, as a number.

Cross-checks to re-derive from the actual files (do not assume): which services carry which latency field (the helper's `units=` census), whether any service mixes both units inside the window, and that the probe route's share of lines is removed before counting.

Before finishing: reopen output/answer.json and confirm it has exactly one key per service file with requests (int), error_rate (float, 4 dp), p95_ms (int); that each requests value equals the helper's printed count; and that no service printed "NO REQUESTS".

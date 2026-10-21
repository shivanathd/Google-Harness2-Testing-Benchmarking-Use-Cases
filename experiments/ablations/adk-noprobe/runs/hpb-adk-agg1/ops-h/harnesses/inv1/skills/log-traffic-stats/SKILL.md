---
name: log-traffic-stats
description: Compute per-service request count, error rate and nearest-rank p95 latency from JSON-lines access logs (some gzipped, mixed UTC offsets, truncated lines, probe routes, latency unit change) inside a UTC window, and write the answer JSON.
---
# Per-service traffic statistics from access logs

Unit of analysis: one JSON record = one request. The logs are far too long to count by eye, and `read_file` truncates long files and cannot read `.gz`. Never count or take percentiles from what you viewed. Work in this order, with at most one look at each source file:

1. Read `RUNBOOK.md` (it is in the workspace root next to `logs/`). It defines which routes to exclude, what counts as an error, and any schema/unit change. Its rules override the script defaults. If a rule differs from the defaults below, pass the matching flag or edit the script.
2. Peek at ~5 lines per log (use `head`, or `gzip -dc f | head` for gz) to confirm field names. Do not page through whole files.
3. Run the helper once over ALL log files with the window from the task (START inclusive, END exclusive, UTC):
   `python3 skills/log-traffic-stats/scripts/traffic_stats.py 2026-10-04T06:00:00Z 2026-10-04T12:00:00Z logs/gateway.jsonl logs/search.jsonl logs/billing.jsonl.gz`
   Add `--list` to print every kept record if you want to spot-check. Add `--write output/answer.json` once the summary is right; it writes `{service: {requests, error_rate, p95_ms}}` keyed by file stem (rename keys in the file if the task uses other service names).
4. Check the printed tallies against the hazards in this workspace's logs:
   - timestamps carry mixed offsets (-03:00, +00:00, +01:00) in the same file, lines out of time order: the window is tested on the UTC instant;
   - ~5-18 truncated, non-JSON lines per file (shipper truncation): skipped, `invalid_json` tally;
   - `/healthz` records (about 1 in 4, with every status incl. 500) are dropped BEFORE counting requests, errors and latency;
   - errors are status >= 500 only; 429/404 are not errors;
   - billing logs `latency_s` (float seconds) from 2026-10-04 09:00 UTC and `latency_ms` before it, in the same file: convert seconds to ms (x1000). Billing's `lat_ms` and `lat_s` tallies should both be non-zero when the window spans 09:00;
   - p95 is nearest rank: sorted ascending, element at ceil(0.95*n), 1-based; it is an existing observation, not interpolated.
5. Reopen `output/answer.json` and confirm: top-level keys exactly as the task lists, `requests` int, `error_rate` float with at most 4 decimals, `p95_ms` int, every service present.

If no shell is available: do the same by hand on a record list you write out, per service, exactly once (read each file once; do not re-read files), and write the answer anyway rather than reading again.

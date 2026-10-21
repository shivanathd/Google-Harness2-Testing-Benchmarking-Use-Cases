---
name: traffic-report
description: Compute per-service traffic statistics (request count, error rate, nearest-rank p95 latency) from service access logs over a UTC time window, and deliver them in the exact JSON shape the task names. Use when asked for a traffic, error-rate, latency or incident statistics report from logs.
---

# Traffic report from access logs

The operation: for each service, filter its access records to the window, classify each record, then aggregate. Inputs are the log files, the runbook (RUNBOOK.md in the workspace), and the window and output path the task names. The result is one JSON deliverable.

The runbook overrides this file if they differ. Read it first and apply its rules.

## Definitions

- Window: convert every timestamp to UTC, then start inclusive, end exclusive. Records in one file carry different UTC offsets, so comparing raw timestamp strings is wrong.
- Request population: in-window records whose route is the load balancer probe. Drop probes from the request count, the error count and the latency sample alike.
- Error: status 500 or higher. A 4xx response is a request, not an error.
- error_rate: errors divided by the request population, rounded to 4 decimal places, stored as a number.
- p95_ms: nearest rank over all request-population latencies for that service. Sort ascending and take the element at 1-based rank ceil(0.95 * n). No interpolation and no mean. Store as an integer in milliseconds.
- Units: if a service's latency field changes unit or name partway through the window, convert each value to milliseconds before pooling. Never pool raw seconds with milliseconds. Locate the switch in the data and compare it with the runbook's timestamp; if they disagree, say so.
- Malformed lines: a line that does not parse as JSON is a truncated record. Skip it and count the skips. Do not salvage partial fields.

## Artifact contract

The deliverable is the file at the path the task names. Its shape is part of the request:

- Top-level keys are exactly the services the task names, in the order given, each holding exactly the three fields the task names. Counts of errors, latency min and max, parse statistics and other intermediate values stay out of the file, even though they are useful in the terminal.
- requests is an integer, error_rate a number with four decimal places, p95_ms an integer.
- Terminal output is not delivery. The file must exist, parse as JSON, and be written before you finish.
- If a service has no requests in the window, its rate and percentile are undefined. Say so in the final message and do not write an invented zero.

## Checks before finishing

1. For each service, requests equals the count of in-window non-probe records, counted in a separate pass from the one that produced the aggregates.
2. errors is less than or equal to requests, and error_rate equals round(errors / requests, 4) from the same numbers written to the file.
3. p95_ms equals one of that service's converted latency values (nearest rank selects an observed value) and lies between that service's min and max.
4. The file parses as JSON and contains only the required keys and fields.

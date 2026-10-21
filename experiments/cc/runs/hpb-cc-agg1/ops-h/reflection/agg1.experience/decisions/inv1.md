KEEP_BASE: I made no changes to `context/harness/`.

- **Rollout:** `base1` is the only rollout. It read RUNBOOK.md and sampled all three logs, including the gzip billing file. It then wrote one script covering every runbook rule. The rules were: skip invalid-JSON lines, drop `/healthz`, count errors as status >= 500, filter the 06:00–12:00 UTC window after converting mixed offsets (-03:00, +01:00, +00:00), and multiply billing `latency_s` by 1000. Nearest-rank p95 used ceil(0.95n). It ran a second check on the billing unit conversion, wrote `output/answer.json`, and summarised its method.
- **My check:** I recomputed all three services independently from `source/logs`, with the same rules and the latencies rounded to 6 decimals to absorb float noise. The results match `deliverables/base1/output__answer.json.txt` exactly:
  - gateway: 96 requests, error_rate 0.1354, p95 334
  - search: 119 requests, error_rate 0.1513, p95 192
  - billing: 124 requests, error_rate 0.1613, p95 393
- **Why not edit:** I found no divergence, tool error, repeated failure or visible risk in the trajectory. The runbook already carries the workspace facts that matter, and the run applied them correctly.
- **Possible residual risk (not edited):** the run did not reopen the written file. It also did not round the `latency_s * 1000` values before the nearest-rank selection, so float noise (for example 392.99999) could in principle shift a p95 after an int cast. Here it did not matter. A single clean run does not justify adding always-on text or a skill for either point.
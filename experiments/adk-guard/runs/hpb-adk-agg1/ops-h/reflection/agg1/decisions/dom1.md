**Evidence:** There is one rollout, base1, and it produced no deliverable. It called `read_file` on gateway.jsonl, search.jsonl and a nonexistent `billing.jsonl` roughly 20 times, re-dumping 260-line logs each time. It never touched the gzip file and never computed anything. It ended with `LlmCallsLimitExceededError` after 40 calls. The base harness had no guidance at all, so the cause is a missing computation path. I confirmed on disk that billing is a real gzip file and that the logs contain the traps the RUNBOOK warns about.

**Workspace facts I checked:**
- Billing switches from `latency_ms` to `latency_s` strictly at the UTC instant 09:00. The last `latency_ms` row is at 08:53 UTC and the first `latency_s` row is at 09:03 UTC. Some rows carry a -03:00 offset, so a filter on local clock digits would misplace them.
- All three files use mixed -03:00, +01:00 and +00:00 offsets.
- All three files contain truncated, invalid-JSON lines (18 in gateway, 5 in search, 10 in billing) and many `/healthz` lines.
- `/healthz` rows carry 200, 201, 429, 500 and 404 statuses, so they also pollute error counts.

**Changes:**
1. **New skill `skills/service-traffic-report/SKILL.md` plus `scripts/traffic_report.py`.** The skill states the analytic move and the practitioner rules, each marked as to be checked against the RUNBOOK:
   - exclude `/healthz` from every statistic;
   - errors are status >= 500 only;
   - convert offsets to UTC, with the window start-inclusive and end-exclusive;
   - convert `latency_s` to ms per line before pooling, because the cutover is a UTC instant and the window straddles it;
   - nearest-rank p95 is ceil(0.95n) on the pooled lines of one service;
   - skip truncated lines.

   It also lists pre-finish checks: one entry per file, exact keys, ints as ints, a unit sanity check, and edge spot-checks. The script reads gzip, does exact integer ranking and rounds the unit conversion. It writes `output/answer.json` with only the three requested fields and prints diagnostics to stderr, not into the deliverable. I ran it on the workspace, and it completes and prints the per-service JSON. I did not record those numbers in the harness, since they are matter-specific.
2. **`systemprompt.md`:** one trigger line naming `service-traffic-report` and telling the agent not to read whole logs or count by eye. This is the base1 failure.
3. **`tool_descriptions/tool_guidance.md`:** one line saying whole-log `read_file` floods context and shows `.gz` as binary, and that a missing output file is the worst outcome.

**Not changed:** the deliverable shape comes from the task and is untouched. I added no always-on workspace results. The answer was not independently verified against any key, and no rollout has yet used the skill.
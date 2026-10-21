I ran the new script on the workspace logs and it wrote a complete `answer.json` with all three services. I did not run a full agent rollout against the edited harness.

**Evidence.** In `base1` (the only rollout), the agent only ever called `list_files` and `read_file`. It made 12 `list_files` and 28 `read_file` calls, repeatedly re-reading `gateway.jsonl` and `search.jsonl` (260 lines each). It hit "Max number of llm calls limit of 40 exceeded" with no deliverable. It never opened `RUNBOOK.md`, which holds the `/healthz` exclusion, the status >= 500 rule and the billing `latency_s` change at 09:00 UTC. It guessed `logs/billing.jsonl` and got a FileNotFoundError, since the real file is `billing.jsonl.gz`. The logs have mixed offsets (-03:00, +00:00, +01:00), truncated lines and `/healthz` records, so counting by eye was never going to work.

**Changes:**
1. **New skill `skills/log-traffic-stats/SKILL.md`.** It gives the order of work: read the runbook, peek at a few lines, run the script once over all files, check the tallies, then reopen the answer file. It also records facts verified in this workspace:
   - Offsets are mixed within each file.
   - Each file has 5–18 truncated lines.
   - `/healthz` records carry every status, including 500.
   - Billing switches to `latency_s` at 09:00 UTC.
   - Billing's `lat_ms` and `lat_s` tallies should both be non-zero for this window.

   The skill also has a no-shell fallback that reads each file once and writes the answer anyway. This is not tied to the evidence, since base1 never showed whether a shell existed.
2. **New script `skills/log-traffic-stats/scripts/traffic_stats.py`.** It reads gzip by magic bytes and skips invalid JSON. It tests the window on the UTC instant and drops `/healthz` before any statistic. Errors are status >= 500. Latency is `latency_ms`, or `latency_s` × 1000. p95 is nearest rank, `ceil(0.95n)`, computed with integers. It writes `{service: {requests, error_rate, p95_ms}}`, and refuses to write if there are warnings such as zero requests or a missing latency field. On the workspace logs it printed:
   - gateway: 96 requests, 0.1354, 334
   - search: 119 requests, 0.1513, 192
   - billing: 124 requests, 0.1613, 393
3. **`systemprompt.md`.**
   - The prompt now names the `log-traffic-stats` skill, as the validation trigger rule requires.
   - It says to read any instruction file the task names first, because base1 never opened `RUNBOOK.md`.
   - It says to read each source file at most once, because of the 40-call loop.
   - It keeps the "reopen the deliverable" completion rule.
4. **`tool_descriptions/tool_guidance.md`.** Added three rules:
   - `read_file` can't read `.gz` files and truncates long ones.
   - Move failing multi-step commands into a `.py` file, and don't resend an identical command.
   - Don't repeat an identical read or list call, given the roughly 40-call budget.

I made no plugin or Stop-hook change. The failure in base1 was running out of calls, which a Stop hook can't fix.
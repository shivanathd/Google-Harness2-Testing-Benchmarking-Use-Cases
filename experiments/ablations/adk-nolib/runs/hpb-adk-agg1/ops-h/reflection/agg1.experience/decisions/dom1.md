**Evidence.** There is one rollout, `base1`. It produced no `answer.json`. It issued about 40 `read_file` calls, mostly re-reading `logs/gateway.jsonl` and `logs/search.jsonl` from `start_line` 0. Each call returned only about 65 of the 260 lines, cut mid-line, so the agent never saw whole files. It tried the nonexistent `logs/billing.jsonl` several times. The real file is `billing.jsonl.gz`, and its first attempt returned FileNotFoundError. It never computed anything and ended with `LlmCallsLimitExceededError` at 40 calls.

**Changes.**
1. **New skill `skills/log-traffic-report/SKILL.md`**, with a trigger line added to `systemprompt.md`. It turns the RUNBOOK rules and the traps I checked in the logs into a checklist:
   - Skip lines that are not valid JSON.
   - Convert mixed UTC offsets (-03:00, +00:00, +01:00, seen in all three files, not time-sorted) to UTC before testing the window.
   - Exclude `/healthz` at any status.
   - Count errors as status >= 500 only.
   - Multiply `latency_s` by 1000 per record. Billing mixes both fields inside the window, and `latency_s` only appears from 09:00 UTC.
   - Use nearest-rank p95 with integer ceil.
   - Read gzip files as text; `billing.jsonl` does not exist.
   - Check the output shape and sanity before finishing.

   It also records that `read_file` output is capped, so re-reading the same range does not help (the `read_file` cap is what the trajectory showed).
2. **New helper `skills/log-traffic-report/scripts/traffic_stats.py`.** It does the deterministic calculation and writes `output/answer.json` in the task's shape. It prints per-file audit counts to stderr. The audit covers unparseable lines, outside-window lines and excluded healthz lines. I ran it against the source logs as a check:
   - gateway: 96 requests, 13 errors, error_rate 0.1354, p95 334.
   - search: 119 requests, 18 errors, error_rate 0.1513, p95 192.
   - billing: 124 requests, 20 errors, error_rate 0.1613, p95 393.

   I wrote the figures here only to show the script runs. They are not stored in the harness as facts.

I did not change the guardrails, memory or tool guidance. The workspace facts are labelled "in this workspace" inside the skill.

The rollout only ever used `list_files` and `read_file`, and I did not confirm that a shell exists. The skill therefore says to page with small ranges and tally by hand if no shell is available.
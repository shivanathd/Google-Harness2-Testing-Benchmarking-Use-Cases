This revision responds to the rejection. I edited only `skills/traffic-report/SKILL.md`, and I did not re-read the trajectories for it.

- **Removed the "Workspace facts" block.** It held this instance's line counts, truncated-line counts, per-service results (requests, errors, error rates, p95) and healthz counts. It also had the billing latency cut-over hours and the file names. The skill now keeps only the method. The agent derives these figures from the logs and RUNBOOK.md on each run.
- **Generalized instance-specific wording in the counting rules.**
  - "Offsets mixed: -03:00, +00:00, +01:00 seen" became "offsets can be mixed within one file".
  - "`/healthz` here" became "the route the runbook names, typically `/healthz`".
  - The helper command's concrete window and `logs` directory became `LOGDIR START END` placeholders. These are ISO text, naive = UTC, copied from the runbook or task.
- **Rule 5 now says to confirm gzip-compressed log files were read.** This is a general check. It replaces the billing-specific fact.
- **Kept the trigger line in `systemprompt.md`.** It already names `traffic-report`, and `scripts/traffic_stats.py` ships inside the skill directory.
- **Not changed.** The counting rules, the helper script and the "Before finishing" checks stay as they were. I made no edits outside `skills/traffic-report/SKILL.md`.
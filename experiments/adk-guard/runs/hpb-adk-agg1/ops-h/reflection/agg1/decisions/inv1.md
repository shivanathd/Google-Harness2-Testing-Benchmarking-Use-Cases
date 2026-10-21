This revises the previous rejected attempt. I did not re-read the trajectories this round.

- **Change:** In `skills/log-traffic-report/SKILL.md`, I removed the workspace-fact block. That block carried instance-specific facts: billing switches units at 2026-10-04 09:00 UTC, and 404 and 429 are not errors. I also removed the `billing.jsonl.gz` filename example from step 1. Step 1 now says to note each file's exact name, including `.gz` suffixes.
- **Replacement:** The rules section is now "Defaults the script applies (compare each against the runbook before trusting the output)". It lists the script's behaviour as procedure for the agent to check against the runbook:
  - skipping bad lines;
  - the `/healthz` exclusion;
  - error = status >= 500;
  - nearest-rank p95;
  - per-line latency unit handling;
  - service name taken from the file name.
  
  Each default says to edit a script copy if the runbook differs.
- **Failure handling:** A separate "If the script fails" section tells the agent to read the error first. It then allows one retry with a corrected copy under /tmp and says to write the best computed result. This keeps the bounded fallback and the stop condition.
- **Unchanged:** The script, `systemprompt.md` (which already names the skill in its trigger line), and the other components are untouched. I did not run the script this round.
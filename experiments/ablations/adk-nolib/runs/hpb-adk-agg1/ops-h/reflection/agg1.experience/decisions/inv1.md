This revision fixes what the rejection flagged in `systemprompt.md`. I made no other changes and did not re-read the trajectories this round.

- **Instance results removed.** I deleted the sentence recording the script's per-service output for one specific window (request counts, error rates and p95 values). That was the content the validator rejected.
- **Window example made generic.** The example call used this task's own time window. It now says to take the window from the task and shows a `YYYY-MM-DDTHH:MM:SS+00:00` placeholder.
- **Workspace-fact block replaced with checks.** The old block described this instance's files. It is now a short list of things the agent must confirm from the data:
  - mixed timestamp offsets and unordered files
  - truncated lines and `/healthz` probes to drop
  - any service that switches latency field or unit partway through, decided per record by which field is present
- **Procedure and script untouched.** The call-budget rule, the read-`RUNBOOK.md`-first rule, the gzip handling, the `scripts/traffic_report.py` call, and the final re-read of `output/answer.json` stay as they were. They came from the earlier divergence evidence: a run that died at the 40-call limit while re-reading logs and never opening `RUNBOOK.md`.
- **Check for leftovers.** A grep of `systemprompt.md` for the flagged ids and values (0.1354, 0.1513, 0.1613, 119, 124, 192, 334, 393, 96) found no matches.
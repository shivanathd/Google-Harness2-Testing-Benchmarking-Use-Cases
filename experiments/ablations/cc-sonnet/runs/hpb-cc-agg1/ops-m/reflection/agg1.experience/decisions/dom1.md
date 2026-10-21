I fixed the two rejection reasons in `skills/log-incident-stats/SKILL.md`. I did not re-read the trajectories this round, so this edit only removes the flagged material.

- **Removed the "Workspace facts" block.** It held this task's counts (failed=19, users=8, top_code=E401, per-code tallies, file and line counts). Its useful part is kept as a new generic "Cross-check before writing" section, which asks the agent to re-derive and confirm:
  - the parsed, in-window and failed request counts;
  - that no req line failed to parse;
  - that the per-code counts sum to the failed total.
- **Generalised instance-specific details.**
  - The example window `2026-10-06T08:00 2026-10-06T12:00` is now a `YYYY-MM-DDTHH:MM` format taken from the task wording.
  - The named offsets (+02:00, -04:00) became "check the offsets present".
  - The "08:00 in, 12:00 out" wording became "start in, end out".
  - The "E500 is the decoy code here" note is gone.
  - The `code=E500` noise example is now `code=...`.
- **Cleaned the helper script.** The example date in the `scripts/request_failures.py` docstring is now generic. A grep afterwards found no leftover task values in either file.
- **Left unchanged.** The trigger line in `systemprompt.md` and the method rules.
This revision fixes the two problems the validator reported. I didn't re-read the trajectories this round. I only removed instance data from the harness and re-checked the result.

- **Removed the "Workspace fact" block** from `skills/request-failure-stats/SKILL.md`. It held this task's own results: failed=19, users=8, top_code=E401, the per-code counts, and the 06 Oct window. The skill now teaches only the method, which the agent re-derives on each run.
- **Replaced the other instance-specific examples:**
  - The date in the timestamp example is now the generic form `YYYY-MM-DDTHH:MM:SS+00:00`. I changed it in both `SKILL.md` and the `request_failures.py` docstring.
  - The "cache warm after ERROR code=E500" example is now a generic description: an INFO line that merely mentions "ERROR code=...".
- **Checked what's left.**
  - A grep of the harness finds no error-code ids, no 2026 dates and no "Workspace fact" text.
  - `request_failures.py` still byte-compiles.
  - The skill's trigger line is still in `systemprompt.md`, and the script still ships at `skills/request-failure-stats/scripts/request_failures.py`.
  - There are no `{{` or `{%` sequences in the always-on text.
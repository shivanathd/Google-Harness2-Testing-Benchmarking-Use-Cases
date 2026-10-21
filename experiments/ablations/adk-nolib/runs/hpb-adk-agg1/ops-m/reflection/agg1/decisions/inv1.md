This revision fixes the two problems that got the last attempt rejected. Both edits are in `skills/log-failure-stats/SKILL.md` and `skills/log-failure-stats/scripts/log_failures.py`.

- **Instance data removed from `SKILL.md`.** I deleted the "Workspace facts" block, including the line that recorded the result counts and window for this task's logs. I also took the concrete dates and the `output/answer.json` path out of the run command, which now uses `<logdir> <START> <END> --out output/<name>.json`. A grep of the harness finds no `2026` or `E401` anywhere.
- **Method kept as checks the agent re-derives.** A short section now covers the three checks that came from the base run's trajectory. They are written as procedure, with no task values:
  - Convert every timestamp to UTC before windowing, because offsets vary and file order doesn't follow time.
  - Group attempts by request id across all files and count a request as failed only if its final attempt is an error inside the window.
  - Ignore lines that merely mention an error but are not request attempts.
- **Script docstring.** The example window in the usage line of `log_failures.py` now reads `YYYY-MM-DDTHH:MM`, so the script no longer carries this task's dates.
- **Unchanged.** `systemprompt.md` already has the trigger line naming `log-failure-stats`, and the helper script still ships at `skills/log-failure-stats/scripts/log_failures.py`.
- **Not re-checked.** I didn't re-read the trajectories or run the helper this round. The edits only remove task-specific content and keep the existing method.
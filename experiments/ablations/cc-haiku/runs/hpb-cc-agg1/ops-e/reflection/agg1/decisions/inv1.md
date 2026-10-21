Changed: `skills/log-window-stats/SKILL.md` (rejection fix)

- Removed the "Workspace facts" section entirely. It held this instance's counts (163 lines, 130 headers, 35 ERROR headers, 11 continuation hits, 27 msg-text hits), the sample `E500` / `ERROR user=` text, and the timezone mix. None of it is a method. A grep of the harness now finds no instance ids, counts, or file-specific values.
- Replaced it with checks the agent re-derives from the helper output and the file:
  - Step 3: `levels` must contain the task's level. This is a check on the run's own output, not a recorded fact.
  - Step 4: only the level field of a header counts as an event. A level word inside `msg=` text or a continuation line is not one. This is generic method, with no values.
  - Step 6: map the helper's keys to the task's keys explicitly.
- Step 3 check changed from `wc -l` to `grep -c .` (non-blank lines). Trace: in base1, `wc -l app.log` reported 163 while the Read tool showed a 164th empty line, so the reference count was ambiguous in that very run. `grep -c .` removes that ambiguity. The change is a latent-risk fix, not an observed failure. The helper ignores blank lines, so the two sides now match exactly.
- Step 1 now states the helper rejects offset-less times. This is in the helper's code, not the data.

Trigger check: `log-window-stats` is still named in `systemprompt.md` line 5. The frontmatter `name:` and `description:` are intact. The helper path `skills/log-window-stats/scripts/window_stats.py` ships in the skill directory. No `{{` or `{%` appears in always-on text.

Evidence for the other files, which are unchanged (KEEP_BASE for them):

- base1 (the only rollout) ended after its own `/tmp` script printed the figures. It never wrote `output/answer.json`, never ran the checker, and gave no final message. The deliverable is missing. Its procedure failures are the ones the always-on steps 1, 2, and 4 already cover: it skipped the CLAUDE.md read, did not load `log-window-stats`, and did not write the file. The prose was clear, so this is the "ignored invariant" case. A single run does not show repetition, so I did not add a Stop hook. If the next runs also end without the file, a Stop hook in the rig's `hooks.json` form is the justified next step.
- The run's figures were not used or recorded in the harness.
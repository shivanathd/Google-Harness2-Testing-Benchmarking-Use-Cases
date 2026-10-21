I removed the "Workspace facts" block from `skills/log-request-failure-stats/SKILL.md`, because the last attempt was rejected for putting facts about this instance's files in it. I did not re-open the trajectories this time. This revision only fixes the rejected block, and the earlier motivation for the skill still stands.

- **Layout checks:** The block is now a generic "Layout checks" section of things the agent re-derives from the files:
  - Check the `.gz` rotated files: they are binary, so grep and awk silently skip them. Decompress them and confirm every file contributes lines.
  - Identify the event header format.
  - Check for mixed UTC offsets, out-of-order lines, and attempts of one request split across files.
  - Exclude lookalike lines: traceback continuations and lines with no `req=`.
  - Check that timestamp order and `attempt=` order agree.
- **Instance-specific details dropped:** I removed the three file names, the specific offsets, the claim that ordering agreed for every request, and the example window and file list in the helper command. The command now uses placeholders. The "08:00 to 12:00" example became "a task window". The "all three files" wording became "every log file".
- **Unchanged:** The rules, the helper script and the trigger line in `systemprompt.md`. The motivating moment was the unaided run reading the gzip file as garbage and never counting it. That check is still in the skill, now framed as a procedure.
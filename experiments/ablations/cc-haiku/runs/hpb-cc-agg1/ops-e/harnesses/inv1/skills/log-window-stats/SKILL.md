---
name: log-window-stats
description: Count events of one level, distinct users and the top error code inside a UTC time window of service logs whose timestamps carry mixed UTC offsets. Use when analysing service or application logs into incident or traffic statistics.
---

# Log window statistics

Helper: `skills/log-window-stats/scripts/window_stats.py` (run it with `python3 -I`). It prints JSON and never writes into the workspace.

## Procedure

1. Convert the task's window to explicit offsets, e.g. `--start 2026-10-03T09:00:00+00:00 --end 2026-10-03T12:00:00+00:00`. Start is inclusive, end is exclusive. The helper rejects times without an offset.
2. Run `python3 -I skills/log-window-stats/scripts/window_stats.py <log> --start <start> --end <end> --level <LEVEL>`, using the level the task names.
3. Check the evidence before using the numbers:
   - `unparsed` must be empty.
   - `headers` + `continuation_lines` must equal the non-blank line count, `grep -c . <log>`. Use this rather than `wc -l`, which counts newlines and differs when the last line has no newline. If either check fails, read the reported lines yourself and account for them before trusting the counts.
   - `levels` lists the level values the file actually contains. The task's level must appear there; if it does not, re-read the task before going on.
4. Only the level field of a timestamped header line is an event. The same level word can also appear inside `msg=` text or in an indented continuation line; the helper never counts those, and a plain text search for the level word does.
5. If `top_codes` has more than one entry, apply the task's tie rule. If the task gives none, say so in the final message; do not pick silently.
6. Write the figures with exactly the keys the task names (see the always-on checker step). The helper's key names are its own: map each figure to the task's key explicitly rather than copying the helper's keys.

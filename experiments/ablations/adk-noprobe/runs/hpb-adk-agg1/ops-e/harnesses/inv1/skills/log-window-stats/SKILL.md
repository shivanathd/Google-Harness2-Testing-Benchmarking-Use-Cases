---
name: log-window-stats
description: Count events of a given level (e.g. ERROR) in a UTC time window from a multi-timezone service log; distinct users and most frequent code.
---
1. `head`/skim the log once to see the line format (timestamp, level, [service], user=, code=, msg=) and note the offsets present.
2. Run (needs a shell): `python3 skills/log-window-stats/scripts/log_window_stats.py source/app.log START END --level ERROR --list`
   START inclusive, END exclusive, both with offset/Z. Check the `--list` output: each row's UTC time must be inside the window.
3. Write the deliverable with `--write output/answer.json` only if the task's keys match errors/users/top_code; otherwise write the JSON by hand from the printed numbers.
4. Re-read the written file and confirm it is valid JSON with the exact requested keys and int/str types.

No shell available: do NOT tally from memory. Read the log, then list every ERROR event line-by-line with its UTC-converted time (local time minus offset), keep only those in [start, end), and count from that written list.
Before counting, re-derive from the log itself: which UTC offsets appear, whether lines are in time order (do not assume), and whether continuation lines (indented tracebacks) or INFO/other lines merely mention the level word. Only lines that begin with a timestamp and carry the level in the level position are events.

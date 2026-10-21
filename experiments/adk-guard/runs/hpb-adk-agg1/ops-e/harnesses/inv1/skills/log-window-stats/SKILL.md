---
name: log-window-stats
description: Count events, distinct users and top code for one log level inside a UTC time window from a multi-timezone service log. Use for any "analyse logs into incident/traffic statistics" task.
---

# Log window statistics

Never tally by eye: a mental estimate of a ~150-line mixed-timezone log overcounted badly in the
first run. Compute counts with the script or from a written-out list.

## Log format traps (check against the actual file with a quick look, then rely on them)
- An event line starts with a timestamp + UTC offset (`Z` and signed offsets such as `+01:00`,
  `+05:30`, `-07:00` can all occur in one file), then LEVEL, `[service]`, `user=`, `code=`, `msg=`.
  Many lines are not events (continuation lines); count only event header lines.
- Lines are NOT in time order and offsets are mixed: convert every timestamp to UTC before
  filtering. A local time near a window edge can land on either side after conversion.
- Look-alikes that are not events at the target level: indented traceback/continuation lines that
  mention `ERROR user=... code=...` inside text (they carry a different user/code than their parent
  event and must be ignored); INFO lines with `msg=retrying after ERROR code=...`; WARN lines with codes.
- Window is start-inclusive, end-exclusive; an event at exactly the end time is out.

## Procedure
1. Read the file in full (check that the lines you received equal the stated total; re-read a range if
   output was cut). Do not assume a field's meaning beyond what the lines show.
2. If you can run shell commands:
   `python3 skills/log-window-stats/scripts/log_window_stats.py app.log --start <UTC start> --end <UTC end> --level <LEVEL>`
   (times are UTC, format YYYY-MM-DDTHH:MM; take them from the task). It prints count, distinct users, per-code counts, `top_tie`, and each counted
   event with its UTC time. Exit 1 means `problems` lists lines it could not parse or that had no
   offset -- read them and decide, do not ignore. If `top_tie` is true, re-check the filter before answering.
   If the script path is missing, write the same ~20 lines of Python yourself rather than counting by hand.
3. If you cannot execute anything: list every candidate event line (header lines at the target level only)
   one per row with its UTC time, in-window yes/no, user, code; then count the yes rows from that list. Do not
   report a number you did not derive from a written-out list.
4. Write the deliverable in exactly the shape the task specifies (file name, keys and types exactly as the task
   states; integers as integers) and read the file back to confirm it parses.

---
name: log-window-stats
description: Count events, distinct users and top error code for a level inside a UTC time window from a multi-timezone service log (incident / traffic statistics).
---

# Log window statistics (practitioner rules)

Deliverable: the exact JSON shape the task names, values as plain numbers/strings computed by you (never estimated from reading the log by eye).

## Define the event first
- An EVENT is a record whose line starts at column 0 with a timestamp, then a level token (ERROR/WARN/INFO), then `[service]`. Level is the token right after the timestamp, nothing else.
- Not events, even though they contain the text "ERROR": indented traceback continuation lines (they may mention a different user or code than the parent event), and lower-level lines that merely quote an error (e.g. an INFO line saying it is retrying after an error). WARN lines may also carry `code=`; they are not ERROR.
- Attribute user and code from the event's own header line only, never from its continuation lines.

## Window
- Convert every timestamp to UTC using its own offset before comparing (`Z` and numeric offsets, including non-whole-hour ones, may be mixed; lines need not be in chronological order). Start inclusive, end exclusive: an event exactly at the window end is out, exactly at the start is in.
- Do not filter on the local clock digits or on the date prefix; an event with a local date before the window date can fall inside the UTC window, and vice versa.

## Calculations
- errors = number of qualifying events (not users, not lines).
- users = distinct `user=` values among those same events.
- top_code = most frequent `code=` among those same events; if the script warns of a tie, re-check the event filter; if the tie is real, pick by the task's stated rule, else say so in the final reply (the file still holds one code).

## Check before writing
- Run `python3 -I skills/log-window-stats/scripts/log_window_stats.py app.log START_UTC END_UTC ERROR` (START/END as ISO with offset, e.g. YYYY-MM-DDTHH:MM:00+00:00). It prints counts plus every qualifying event line number; spot-check 2-3 boundary-near events by hand-converting their offset.
- Confirm users <= errors, the code counts sum to errors, and the JSON keys are exactly those requested.

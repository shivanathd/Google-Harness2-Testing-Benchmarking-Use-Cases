[ACTION] load_skill {"name": "log-window-stats"}
[OBSERVATION]
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

[ACTION] run_command {"command": "python3 -I skills/log-window-stats/scripts/log_window_stats.py app.log 2026-10-03T09:00:00+00:00 2026-10-03T12:00:00+00:00 ERROR"}
[OBSERVATION]
exit=0
events: 15
distinct users: 6 ['alice', 'chen', 'diya', 'eve', 'gita', 'hiro']
code counts: [('E500', 5), ('E403', 4), ('E401', 4), ('E502', 1), ('E504', 1)]
missing user: 0 missing code: 0
continuation/unparsed lines ignored: 33
47 2026-10-03T14:38:44+05:30 diya E500
52 2026-10-03T14:43:45+05:30 alice E500
56 2026-10-03T10:15:48+01:00 gita E502
59 2026-10-03T09:17:42Z diya E403
64 2026-10-03T09:40:31Z diya E403
71 2026-10-03T10:56:27+01:00 eve E401
75 2026-10-03T10:05:38Z alice E500
76 2026-10-03T03:07:28-07:00 alice E401
78 2026-10-03T15:46:10+05:30 alice E403
85 2026-10-03T11:32:41+01:00 hiro E401
88 2026-10-03T10:59:20Z diya E403
90 2026-10-03T11:17:07Z chen E504
96 2026-10-03T17:06:50+05:30 chen E500
98 2026-10-03T11:38:49Z diya E401
105 2026-10-03T17:26:05+05:30 hiro E500

[ACTION] write_file {"path": "output/answer.json", "content": "{\"errors\": 15, \"users\": 6, \"top_code\": \"E500\"}"}
[OBSERVATION]
wrote 46 chars to output/answer.json
[ASSISTANT] {
  "errors": 15,
  "users": 6,
  "top_code": "E500"
}
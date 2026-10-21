[ACTION] load_skill {"name": "log-window-stats"}
[OBSERVATION]
---
name: log-window-stats
description: Count ERROR events, distinct users and top error code from a multi-timezone service log for a UTC time window. Use for any incident/traffic statistics task over raw log files.
---

# Log window statistics (errors / distinct users / top code)

ANALYTIC MOVE: classify each log line as event vs. non-event, convert event time to UTC, filter to the window, then count. Eyeballing a 100+ line log gives wrong numbers (a prior run counted by eye and answered errors=21 where the correct count was 15) — compute, don't estimate. If a shell is available, run `python3 skills/log-window-stats/scripts/window_stats.py app.log "2026-10-03T09:00:00+00:00" "2026-10-03T12:00:00+00:00"` (start inclusive, end exclusive; adjust the window to the task) and use its output. If there is no shell, apply the rules below line by line and list every counted event (UTC time, user, code) before totalling.

## What counts as an event
1. An EVENT is a line that STARTS with an ISO timestamp followed by LEVEL, `[service]`, `user=`. Lines indented under it (Traceback, `File ...`, `RuntimeError: upstream ERROR user=X code=Y`) are continuation text of the previous event: NEVER count them, and never take the user/code from them — the event's own `user=`/`code=` fields are the truth (the traceback often names a different user and code).
2. Level is the token right after the timestamp. Only `ERROR` counts. `INFO ... msg=retrying after ERROR code=...` is INFO; `WARN ... slow response` is WARN, even though both carry a `code=`. A substring match on "ERROR" overcounts.
3. Every timestamp has its own offset (`Z`, `+01:00`, `+05:30`, `-07:00` seen in this workspace). Convert to UTC (subtract the offset) BEFORE filtering; the file is not in time order, and the date part of the local stamp can differ from the UTC date (e.g. `2026-10-02T23:31-07:00` is 2026-10-03 06:31Z). Do not filter on the local clock text.
4. Window is start-inclusive, end-exclusive: 12:00:00Z is out, 09:00:00Z is in. Check events near the edges explicitly (e.g. +05:30 stamps around 14:30–17:30 local, +01:00 around 10:00–13:00 local, -07:00 around 02:00–05:00 local).

## Answer fields
- errors = number of qualifying events (not distinct).
- users = distinct `user=` values of those same events.
- top_code = most frequent `code=` among those same events; check for a tie and report the tie in your reply if one exists (don't silently pick).
Write exactly the requested JSON keys/types (ints, string code) — no extra keys.

## Cross-check before writing
- errors equals the sum of per-code counts; users <= errors.
- Recount boundary events and one event per offset by hand.
- Workspace fact (this app.log, 163 lines, 4 offsets): script gives errors=15, users=6, top_code=E500 (E500 x5, E403 x4, E401 x4) for the 09:00–12:00Z 2026-10-03 window. Treat as a check if the same file/window recurs; recompute for any other input.

[ACTION] run_command {"command": "python3 skills/log-window-stats/scripts/window_stats.py app.log \"2026-10-03T09:00:00+00:00\" \"2026-10-03T12:00:00+00:00\""}
[OBSERVATION]
exit=0
2026-10-03T09:08:44+00:00 search diya E500
2026-10-03T09:13:45+00:00 billing alice E500
2026-10-03T09:15:48+00:00 billing gita E502
2026-10-03T09:17:42+00:00 gateway diya E403
2026-10-03T09:40:31+00:00 billing diya E403
2026-10-03T09:56:27+00:00 billing eve E401
2026-10-03T10:05:38+00:00 gateway alice E500
2026-10-03T10:07:28+00:00 search alice E401
2026-10-03T10:16:10+00:00 billing alice E403
2026-10-03T10:32:41+00:00 auth hiro E401
2026-10-03T10:59:20+00:00 auth diya E403
2026-10-03T11:17:07+00:00 auth chen E504
2026-10-03T11:36:50+00:00 auth chen E500
2026-10-03T11:38:49+00:00 gateway diya E401
2026-10-03T11:56:05+00:00 search hiro E500
continuation/non-event lines skipped: 33
errors 15 users 6 codes [('E500', 5), ('E403', 4), ('E401', 4), ('E502', 1), ('E504', 1)]
{'errors': 15, 'users': 6, 'top_code': 'E500'}

[ACTION] write_file {"content": "{\"errors\": 15, \"users\": 6, \"top_code\": \"E500\"}", "path": "output/answer.json"}
[OBSERVATION]
wrote 46 chars to output/answer.json
[ASSISTANT] {
  "errors": 15,
  "users": 6,
  "top_code": "E500"
}
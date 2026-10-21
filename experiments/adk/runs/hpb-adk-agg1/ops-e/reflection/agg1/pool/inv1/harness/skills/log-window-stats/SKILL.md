---
name: log-window-stats
description: Count events of a given level, distinct users and top error code for a UTC time window in a mixed-timezone service log, and write the small JSON answer.
---
# Log window statistics

1. Read the first ~30 lines of the log to see the format. In this workspace (app.log) each event is a header line
   `<ISO ts with Z or +HH:MM/-HH:MM> LEVEL [service] user=<u> code=<c> msg=...`; some ERROR events are followed by
   indented traceback lines. Those indented lines (and `msg=retrying after ERROR code=...` on INFO lines, and the
   `RuntimeError: upstream ERROR user=<other> code=<other>` text inside tracebacks) are NOT events and carry other
   users/codes: never count them. An event's level, user and code come only from its own header line.
2. Convert every timestamp to UTC before comparing with the window (start inclusive, end exclusive). Lines are not in
   time order, and some local dates differ from the UTC date.
3. Run (needs a shell):
   `python3 skills/log-window-stats/scripts/log_window_stats.py app.log 2026-10-03T09:00:00Z 2026-10-03T12:00:00Z --level ERROR --out output/answer.json`
   (a copy also lives at scripts/log_window_stats.py). It prints each matched event and the tallies.
   It refuses to write on a tied top code or unparseable lines (exit 2/3): inspect and decide, don't retry blindly.
4. If no shell/execution tool exists, do not eyeball the whole file: list each header line with level ERROR, write its
   UTC time next to it, keep only those in the window, then count events, distinct users, and codes from that list.
   Re-count the list once before writing.
5. Reopen output/answer.json and confirm it is valid JSON with exactly the keys the task names, with int and string types.
   Reference check for this workspace's data: the window 2026-10-03 09:00-12:00Z gives 15 ERROR events, 6 users, top E500.

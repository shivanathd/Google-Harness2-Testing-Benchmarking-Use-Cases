---
name: log-window-stats
description: Count ERROR-level events, distinct users and the most frequent error code from a timestamped service log over a UTC time window, and deliver the result as a JSON file. Use for any log-window counting or top-value task.
---

# Log window statistics

## What the deliverable is
- The named file under output/ is the deliverable. Figures printed to the console or computed by a helper are not. The task is incomplete until the file exists, parses as JSON, and holds exactly the keys the task names, with the JSON types the task names (numbers as numbers, strings as strings).
- Add no extra keys. Whatever reads this file keys on the exact names.

## What counts as an event
- An event is a header line: an ISO-8601 timestamp, then the level, then the [component]. Match the level token exactly (ERROR) unless the task says otherwise.
- Indented lines (stack traces, continuation text) belong to the header above them. They are not events, and any "LEVEL user= code=" text inside them does not supply the event's user or code. Take attributes from the header.

## Time
- Every timestamp carries its own UTC offset. Convert each one to UTC before comparing it with the window. Comparing raw timestamp strings, or assuming one zone, gives a different count.
- Apply the window bounds as the task states them (start inclusive, end exclusive, if so stated). Check events sitting exactly on a bound.

## Statistics
- errors: number of in-window events at the requested level.
- users: distinct user values among those same events, each user counted once.
- top_code: most frequent code among those same events. If two codes tie, the task does not say which to report. Name the tie in the final message rather than picking silently.

## Consistency checks before finishing
- users is at most errors. If errors is 0, users is 0 and top_code has no defined value; say so.
- The per-code counts sum to errors.
- top_code's count is the maximum, and the code occurs among the in-window events, not just somewhere in the file.
- Re-check the two events nearest each window bound against the UTC conversion.

## Facts observed in this workspace (app.log of this task; re-verify on any new log)
- 163 lines: 130 header events and 33 indented traceback lines in 11 blocks.
- Four offset forms appear: Z, +01:00, +05:30, -07:00.
- In all 11 traceback blocks, the "upstream ERROR user= code=" text names a user and code that differ from the header the block belongs to. Counting users or codes from that text gives the wrong set.
- A raw-string comparison against the UTC window undercounts ERROR events compared with a UTC-converted comparison.

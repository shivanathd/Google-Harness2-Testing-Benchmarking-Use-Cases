---
name: log-incident-stats
description: Rules for turning a multi-service, multi-timezone application log into incident/traffic statistics (error counts, distinct users, top error code) for a UTC window.
---

# Log -> incident statistics: practitioner rules

ANALYTIC MOVE: classify each log *event* (level, service, user, code, instant), filter by instant in UTC, then count / de-duplicate / rank. Result must be exact integers and a code string, computed by a parser, not eyeballed.

## What counts as an event
- An event is a line that STARTS with an ISO timestamp (with offset) followed by a level token. Indented lines after it (Traceback, File, RuntimeError...) belong to the previous event; they are NOT events.
- The level is the token right after the timestamp. Text "ERROR" elsewhere in the line (e.g. a free-text `msg=` on an INFO line that quotes the word ERROR and a code) or inside an indented continuation line (an exception message that repeats `ERROR user=... code=...`) is NOT an ERROR-level event.
- user and code come from the event's own header line. Never take user/code from a continuation line: they name a different user/code than the event and would inflate users/codes.
- WARN lines also carry `code=`; they are not ERROR events and must not feed the code ranking.

## Time window
- Convert every timestamp to UTC using its own offset (Z, +01:00, +05:30, -07:00 ...) BEFORE comparing. File order is not time order, and the calendar date in a local timestamp may differ from the UTC date (a late-evening timestamp with a negative offset falls on the next UTC day).
- Window is half-open: start inclusive, end exclusive. List any event within a minute of either boundary and decide it explicitly.
- Half-hour offsets (+05:30) shift minutes, not just hours; do not round the offset.

## Counting rules
- errors = number of ERROR events in the window (each event once; do not dedupe events).
- users = distinct user values among exactly those events (not among all users in the log, not including WARN/INFO-only users).
- top_code = most frequent code among exactly those events. If two codes tie for first, say so explicitly in your final message rather than silently picking one; re-check the window and parsing first, since a tie often signals a parsing error.

## Consistency checks before finishing
1. Sum of per-code counts == errors; users <= errors; top_code's count is the max.
2. Print the in-window ERROR events (line number, UTC instant, user, code) and eyeball boundary and offset cases.
3. Count of header lines + continuation lines == total lines in file (nothing silently dropped by the regex).
4. Output file matches the requested JSON shape exactly: integer values for counts, string for code, no extra keys. Write it as soon as the checks pass.

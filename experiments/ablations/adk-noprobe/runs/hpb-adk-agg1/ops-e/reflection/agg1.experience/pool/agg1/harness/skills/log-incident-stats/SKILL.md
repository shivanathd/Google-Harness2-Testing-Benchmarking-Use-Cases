---
name: log-incident-stats
description: Count ERROR events, distinct users and top error code from a multi-timezone service log inside a UTC time window.
---
# Log incident / traffic statistics

ANALYTIC MOVE: classify each log *event* (not each line), normalise its timestamp to UTC, filter to the window, then count/aggregate over the surviving events.

## 1. What is an event
- An event starts at a line beginning with a timestamp (ISO-8601 with Z or ±hh:mm), followed by LEVEL, optional service, and `key=value` fields before `msg=`. Confirm this layout on the actual file first.
- Lines that start with whitespace are continuation lines (stack traces, exception text). They belong to the preceding event. They are NOT events, and any user/code text inside them is NOT the event's user/code, even if it looks like a full log record. Never count them or take their fields.
- The LEVEL is only the token right after the timestamp. The word ERROR inside msg text (e.g. an INFO event whose msg mentions an error) does not make an event ERROR-level. WARN is not ERROR.
- user and code come from the event's own first line, fields before `msg=`.

## 2. Window
- Take the window and its timezone from the task. Convert every event timestamp to UTC by subtracting its offset (`+05:30` -> minus 5h30; `-07:00` -> plus 7h; `Z` unchanged). Lines may be out of time order, and the local date prefix is not reliable: a late-evening local time with a negative offset can already be the next UTC day, and a positive offset can move earlier.
- Treat the window as half-open (start inclusive, end exclusive) unless the task says otherwise; state this assumption.
- For each distinct offset in the file, precompute the equivalent local window and use it only to cross-check your per-event conversion.

## 3. Aggregate
- errors = number of ERROR-level events in window.
- users = number of distinct `user=` values among exactly those events.
- top_code = most frequent `code=` among exactly those events. Tally every code, list the full tally, and check for ties before naming one; if tied, say so in your final reply (do not silently pick).

## 4. Before finishing, check
- Write out the list of qualifying events (UTC time, user, code) one per line; errors must equal the list length, users the distinct users in it, and the code tallies must sum to errors. If any disagree, recount.
- Confirm no continuation line, INFO event mentioning an error, or WARN line is in the list, and no event outside the UTC window is.
- Confirm the output has exactly the keys the task names, with ints as ints and strings as strings.
- If no code-execution tool is available, count by hand from the written list; do not estimate or answer from a skim of the file. If one is available, still reconcile its result against the written list.

## 5. Helper script (only if you have a shell)
`python3 skills/log-incident-stats/scripts/log_window_stats.py <path-to-log> START END --level ERROR --list` (START inclusive, END exclusive, ISO with Z or offset, e.g. 2026-10-03T09:00:00Z). It applies the rules above and prints the qualifying events, distinct users and per-code tally with a tie warning; `--write output/answer.json` writes errors/users/top_code. Use the printed list for the section 4 reconciliation, then reopen the written file and check keys and types. Without a shell, do section 4 by hand from the written list.

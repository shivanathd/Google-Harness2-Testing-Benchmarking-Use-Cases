---
name: log-window-stats
description: Count events at one log level, distinct users and the most frequent code inside a UTC time window of a service log whose timestamps carry mixed UTC offsets, and deliver the figures as the JSON file the task names. Use for incident or traffic statistics over a log window.
---

# Log window statistics

## The deliverable
- The file the task names under output/ is the deliverable. Figures printed to the console or left in the transcript do not count. The task is not finished until the file exists and parses.
- Write exactly the keys the task names, with the JSON types it names (numbers as numbers, strings as strings). Add no extra keys; whatever reads the file keys on exact names.
- End with a one-line final message that names the file, its values, and any tie or empty-window case below.

## What is an event
- An event is a header line: an ISO-8601 timestamp, then the level token, then the [component]. Match the level exactly as the task states it.
- Indented lines (stack traces and continuation text) belong to the header above them and are not events. Any "LEVEL user= code=" text inside them is not the event's user or code; take those from the header.
- A level word inside msg= text is not a level field.

## Time
- Every timestamp carries its own UTC offset. Convert each one to UTC before comparing it with the window. Comparing raw strings, or assuming one zone, gives wrong counts.
- Apply the bounds as the task states them (for example start inclusive, end exclusive). Re-check the events nearest each bound after conversion.

## Statistics
- errors: in-window events at the requested level.
- users: distinct user values among those same events.
- top_code: most frequent code among those same events. If codes tie and the task gives no tie rule, write the alphabetically first tied code and name every tied code in the final message.
- No events: errors 0, users 0, top_code an empty string, and the final message says so.

## Helper and checks
- Helper: `scripts/window_stats.py` in this skill's own directory (the folder holding this SKILL.md; the runtime may place it under `.claude/skills/`). Run it as `python3 -I <skill-dir>/scripts/window_stats.py <log> --start <ISO> --end <ISO> --level <LEVEL>`, with bounds that carry explicit offsets. It prints JSON with count, users, top_code (None on a tie), top_codes, codes, matches, headers, continuation_lines, levels and unparsed. Map each figure to the task's key names yourself.
- Before using the figures: `unparsed` is empty; `headers` plus `continuation_lines` equals the non-blank line count `grep -c . <log>`; `levels` contains the task's level.
- Consistency: users is at most errors; the per-code counts sum to errors; top_code's count is the maximum among codes of in-window events.
- Without the helper, do the same parse in one pass over every line of the file and check the same counts. A hand-read sample is not enough.

## Verify the file
- Parse it and confirm the key set and types, for example `python3 -I -c "import json,sys; d=json.load(open(sys.argv[1])); print(d, {k: type(v).__name__ for k, v in d.items()})" output/<file>.json`.

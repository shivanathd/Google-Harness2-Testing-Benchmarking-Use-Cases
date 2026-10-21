---
name: log-incident-stats
description: Turn rotated service logs (plain + gzip, mixed UTC offsets, retried requests) into failed-request, distinct-user and top-error-code statistics for a UTC window, and write the answer file.
---

# Log -> incident / traffic statistics

ANALYTIC MOVE: classify each request by its final attempt, filter by that attempt's UTC time, then count requests, distinct users and error codes. Inputs: every file in logs/ (app.log, app.log.N, app.log.N.gz). Result: the exact JSON the task names, written to output/.

## Run it
`python3 -I skills/log-incident-stats/scripts/request_failures.py logs START END` (START inclusive, END exclusive, UTC, format YYYY-MM-DDTHH:MM, taken from the task wording). It prints each failed request, then the counts. Add `--write output/answer.json` when the printout looks right; it writes keys failed / users / top_code. If the task names different keys, write the file yourself from the printed numbers. If the script path is not found, search the workspace for it; if it cannot be found, write an equivalent script.

## Rules to check (each one is a way the count goes wrong)
- Unit is the REQUEST (req=), not the log line. Pool all attempts of a req across ALL files before choosing the last one; a retry chain can straddle a rotation boundary.
- Last attempt = latest UTC time (attempt number breaks ties). FAILED = that line is level ERROR. An earlier ERROR followed by an INFO status=200 retry is a recovered request, not a failure.
- Window applies to the LAST attempt's time, converted from its own offset to UTC (several different offsets, including +00:00, can appear in one file set; check the offsets present). Never compare local clock text. Half-open: the start instant is in, the end instant is out. A request whose first attempt is in the window but last is outside does not count, and the reverse also holds.
- Noise that is NOT an attempt: indented `Traceback` / `UpstreamError: ERROR code=... user=...` lines, and req-less INFO lines such as `msg=cache warm after ERROR code=...`. They carry look-alike code/user text and must not feed users or codes.
- Code and user come from the failing last attempt's own line, not from earlier attempts of that request. Users = distinct user values among failed requests (a user with several failed requests counts once).
- Top code: if two codes tie, do not guess; report the tie in the final reply and pick per the task wording.

## Finish
Reopen output/answer.json: valid JSON, exactly the requested keys, ints as ints, top_code a string. Computing without writing the file is not finishing.

## Cross-check before writing
Count the parsed requests, the requests with last attempt in the window, and failed requests; confirm no req line failed to parse and the per-code counts sum to the failed total. If the task states or implies a different expected figure, find which rule above was broken.

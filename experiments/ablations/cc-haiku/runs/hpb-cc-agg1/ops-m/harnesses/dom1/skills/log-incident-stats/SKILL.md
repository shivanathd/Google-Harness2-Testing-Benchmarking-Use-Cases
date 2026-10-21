---
name: log-incident-stats
description: Turn rotated service log files into incident and traffic statistics (failed requests, affected users, error-code counts) over a stated time window. Load when a task asks for counts or rankings of failed or erroring requests from logs.
---

# Log incident statistics

The unit is the request, not the log line. Each request is identified by its `req=` ID, and its outcome is decided by its last attempt. The deliverable is a handful of counts over one window, and whoever reads it keys on the exact field names.

## Rules that decide the numbers

- **Request**: all lines sharing one `req=` ID, gathered across every rotated file. Read `.gz` files decompressed. A request's attempts can sit in more than one file, so group by ID across all files, not per file.
- **Attempt time**: the line timestamp converted to UTC before any comparison. Offsets can differ from line to line, even within one file, so an hour on the clock is not necessarily an hour in UTC. Order attempts by the UTC instant, not by file order or attempt number.
- **Outcome**: the last attempt by UTC time. The request failed if that attempt is level ERROR. An earlier ERROR followed by a successful retry is not a failure.
- **Window**: the task's window applies to the UTC instant of the request's last attempt, not its first. Treat the start as inclusive and the end as exclusive.
- **Only `req=` lines are attempts.** Other lines do not count toward failures, users or codes, even when they contain the words ERROR or `code=E...`. Examples of such lines: summary or informational lines that mention an earlier error without a request ID, and indented traceback or exception continuation lines. A plain grep for ERROR or `code=` over-counts.
- **Users**: distinct `user=` values among the failed requests in the window. Each request should carry one user; if a request shows two, report the conflict instead of picking one.
- **Top code**: the most frequent `code=` among the failed requests' last attempts only. Not all attempts, not all lines, not all-time. If two codes tie, state the tie in the final message and the rule used to break it.

## Checks before writing the output

- Recount the window from UTC instants; confirm the boundary requests on both edges fall on the correct side.
- If the windowed failed count equals the count with no window applied, the window was not applied. Go back and apply it.
- Failed count equals the number of requests whose last attempt is ERROR within the window. The per-code counts for those requests sum to the failed count.
- The output file holds exactly the keys the task names, with the types it names (integers for counts, a string for the code). Add no extra keys, comments or notes inside the file; put reasoning and tie notes in the final message.

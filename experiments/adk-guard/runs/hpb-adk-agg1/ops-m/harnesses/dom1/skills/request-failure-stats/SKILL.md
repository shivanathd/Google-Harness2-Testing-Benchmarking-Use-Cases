---
name: request-failure-stats
description: Failed-request count, distinct affected users and top error code from rotated multi-timezone service logs where requests are retried (req= / attempt=), restricted to a UTC window. Incident and traffic statistics.
---

# Failed-request statistics from retried-request logs

## Analytic move
Classify each REQUEST (not each log line) by its last attempt, then count requests, distinct users and codes among the requests that failed inside the window. Result: the exact JSON the task names, with plain integer/string values.

## Rules
- Unit = `req=` id. Group every attempt line of a request across ALL files (app.log, app.log.N, and the .gz ones) before judging it. Attempts of one request can be in different files and in mixed UTC offsets.
- Last attempt = latest instant after converting each line's own offset to UTC (check it agrees with the highest `attempt=`; if not, flag it). File order and local clock digits are not chronological order.
- FAILED = the last attempt is an ERROR line. A request that errored earlier but ended in INFO status=200 is a recovered request, not a failure. A request whose last attempt is an ERROR is failed even if its first attempt succeeded.
- Window: judge membership by the LAST attempt's UTC time only (start inclusive, end exclusive). Earlier attempts inside the window do not make a request count if its last attempt is outside it, and vice versa.
- user and code come from that last-attempt line's own `user=` and `code=`.
- Not request attempts, though they contain the text "ERROR": indented `Traceback` / `UpstreamError: ERROR code=... user=...` continuation lines (they name other users/codes than their parent) and INFO lines without `req=` such as "cache warm after ERROR code=E500". Never count or grep these.
- Compressed rotations: `read_file` on a .gz shows binary; decompress it (gzip module / zcat) before analysing, otherwise the oldest hours are silently missing.
- Tie for top code: re-check the filter; if the tie is real apply the task's rule, else state the tie in the reply.

## Do it with the script
`python3 -I skills/request-failure-stats/scripts/request_failures.py START_UTC END_UTC FILE [FILE ...]`
(START/END ISO with offset, e.g. YYYY-MM-DDTHH:MM+00:00; pass every log file in the directory, including .gz, by listing the directory first). It prints failed / users / code counts / top_code and each failed request with its last-attempt UTC time and source line. Spot-check 2-3 near the window edges by hand-converting the offset.

## Before writing
- users <= failed; code counts sum to failed; JSON keys exactly as the task names them, ints as ints.
- Every log file in the directory was passed to the script (count them against `ls`).

- Sanity-check the answer against a naive count of every ERROR line in the window: the two should differ, and you should be able to say why (retries, recovered requests, continuation lines).

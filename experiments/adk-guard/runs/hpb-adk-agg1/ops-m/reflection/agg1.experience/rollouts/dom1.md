[ACTION] load_skill {"name": "request-failure-stats"}
[OBSERVATION]
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

[ACTION] list_files {"path": "logs/"}
[OBSERVATION]
logs/app.log
logs/app.log.1
logs/app.log.2.gz
[ACTION] run_command {"command": "python3 -I skills/request-failure-stats/scripts/request_failures.py 2026-10-06T08:00+00:00 2026-10-06T12:00+00:00 logs/app.log logs/app.log.1 logs/app.log.2.gz"}
[OBSERVATION]
exit=0
failed: 19
users: 8 ['ana', 'cai', 'dev', 'eli', 'fay', 'gus', 'hal', 'ivy']
code counts (last attempts): [('E401', 7), ('E503', 5), ('E409', 4), ('E500', 3)]
top_code: E401
requests seen: 110 | lines without req= ignored: 26 | duplicate lines skipped: 0
ERROR lines missing user/code/attempt: []
r610093 2026-10-06T08:02:36+00:00 user=cai code=E409 attempt=2 logs/app.log.2.gz:78
r610038 2026-10-06T08:10:13+00:00 user=eli code=E401 attempt=1 logs/app.log.2.gz:87
r610071 2026-10-06T08:20:39+00:00 user=hal code=E503 attempt=3 logs/app.log.2.gz:96
r610024 2026-10-06T08:35:24+00:00 user=eli code=E503 attempt=2 logs/app.log.1:4
r610060 2026-10-06T08:43:54+00:00 user=eli code=E500 attempt=2 logs/app.log.1:7
r610026 2026-10-06T09:00:35+00:00 user=dev code=E409 attempt=1 logs/app.log.1:12
r610058 2026-10-06T09:12:52+00:00 user=ivy code=E409 attempt=1 logs/app.log.1:15
r610080 2026-10-06T09:12:55+00:00 user=dev code=E401 attempt=1 logs/app.log.1:16
r610051 2026-10-06T09:18:08+00:00 user=ana code=E409 attempt=3 logs/app.log.1:29
r610052 2026-10-06T09:32:09+00:00 user=ana code=E401 attempt=2 logs/app.log.1:36
r610082 2026-10-06T09:51:54+00:00 user=ivy code=E401 attempt=1 logs/app.log.1:42
r610095 2026-10-06T09:52:38+00:00 user=hal code=E503 attempt=3 logs/app.log.1:43
r610109 2026-10-06T10:21:01+00:00 user=gus code=E401 attempt=2 logs/app.log.1:50
r610050 2026-10-06T10:27:29+00:00 user=gus code=E503 attempt=3 logs/app.log.1:53
r610099 2026-10-06T10:38:21+00:00 user=dev code=E401 attempt=3 logs/app.log.1:61
r610075 2026-10-06T10:42:46+00:00 user=eli code=E401 attempt=3 logs/app.log.1:66
r610100 2026-10-06T11:06:03+00:00 user=fay code=E503 attempt=2 logs/app.log.1:80
r610085 2026-10-06T11:21:25+00:00 user=ana code=E500 attempt=1 logs/app.log.1:88
r610040 2026-10-06T11:47:35+00:00 user=hal code=E500 attempt=1 logs/app.log:1

[ACTION] write_file {"path": "output/answer.json", "content": "{\"failed\": 19, \"users\": 8, \"top_code\": \"E401\"}"}
[OBSERVATION]
wrote 46 chars to output/answer.json
[ASSISTANT] {
  "failed": 19,
  "users": 8,
  "top_code": "E401"
}
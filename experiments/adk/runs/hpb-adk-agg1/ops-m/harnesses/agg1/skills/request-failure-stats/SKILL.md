---
name: request-failure-stats
description: Count failed requests, distinct affected users and the top error code from rotated multi-timezone service logs (some gzip) where requests are retried and "failed" means the last attempt is an ERROR. Use for any incident/traffic statistics task over a log directory.
---

# Failed-request statistics from rotated logs

Run first (one command, all files, gzip handled by magic bytes, never read the .gz with read_file):

    python3 skills/request-failure-stats/scripts/request_failures.py logs --start 2026-10-06T08:00:00Z --end 2026-10-06T12:00:00Z --out output/answer.json

Adjust the window to the task (start inclusive, end exclusive, in UTC). It prints each considered request's last attempt, tallies on stderr, and writes `{"failed","users","top_code"}`. If the task names other keys, rename them after the run with the same values; write only the requested keys.
Exit 2 = unparseable line or last-attempt ambiguity (attempt number vs UTC time disagree): read the printed lines, decide, do not rerun unchanged. Exit 3 = tied top code or nothing failed: report the tie, do not guess. If the script cannot run, do the same steps with python in a short script file (not a long shell one-liner).

## Rules the script encodes
1. Only header lines starting with a timestamp are events; indented Traceback lines are continuation text whose `user=`/`code=` (often a different user/code) are ignored.
2. Only lines with `req=` are attempts. `INFO user=x msg=cache warm after ERROR code=E500` has no req= and is not a failure.
3. Group attempts by req across ALL files (a request's attempts span rotated files and offsets); last attempt = highest `attempt=` number. Failed = that line's level is ERROR; a request that failed earlier but ended INFO status=200 is not failed.
4. The window applies to the last attempt's time converted to UTC, not to the first attempt or local clock text. Offsets seen: Z/+00:00, +02:00, -04:00. Files are not in time order.
5. failed = distinct failed requests; users = distinct `user=` of those last attempts; top_code = most frequent `code=` of those last attempts only (not earlier attempts).

## Workspace fact (this task's logs/, 3 files, 110 requests)
For 2026-10-06 08:00Z-12:00Z the script gives failed=19, users=8, top_code=E401 (E401 x7, E503 x5, E409 x4, E500 x3), no ambiguity. Treat as a cross-check only if the same logs/window recur.

## Finish
Reopen output/answer.json and confirm valid JSON, requested keys only, ints as ints, code as string.

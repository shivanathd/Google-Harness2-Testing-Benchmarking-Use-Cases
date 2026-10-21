---
name: request-failure-stats
description: Count failed requests, distinct affected users and the top error code from rotated, mixed-offset, partly gzip-compressed service logs where requests are retried (req= / attempt=) and the window is in UTC.
---

# Failed-request statistics from rotated logs

Run the script; do not count by eye and do not try to read `.gz` with read_file (it returns binary garbage).

1. `python3 -I skills/request-failure-stats/scripts/request_failures.py logs --start <ISO+offset> --end <ISO+offset>`
   (a directory argument reads every file in it, gzip auto-detected; START inclusive, END exclusive; form `YYYY-MM-DDTHH:MM:SS+00:00`, converting the task's window to UTC). Add `--out output/answer.json` once the numbers look right; it writes exactly `{"failed", "users", "top_code"}`.
2. Definitions the script applies (check the task text still matches before trusting it):
   - A request is every line group sharing `req=`, pooled across ALL rotated files (attempts of one request are split across files and lines are not in time order; do not judge per file or per line).
   - Last attempt = highest `attempt=` number. FAILED = that last attempt is an ERROR line AND its own UTC time is in the window. Earlier ERRORs that were retried successfully are not failures; a request whose last attempt is INFO/200 is not failed even if earlier attempts failed.
   - `users` = distinct `user=` and `top_code` = most frequent `code=`, both taken from the failed requests' LAST attempts only (earlier attempts may carry different codes).
   - Ignored non-attempts: indented traceback lines (they name other users/codes), and req-less lines such as an INFO message that merely mentions "ERROR code=..." in its text.
3. Heed script warnings (tie for top code, duplicate attempt numbers, missing user/code). On a tie apply the task's tie rule; if none, say so in the final reply. If the script exits 1, fix the input (path, timestamp with offset) and rerun once; do not loop.
4. Read `output/answer.json` back and confirm the keys, int types, and users <= failed.

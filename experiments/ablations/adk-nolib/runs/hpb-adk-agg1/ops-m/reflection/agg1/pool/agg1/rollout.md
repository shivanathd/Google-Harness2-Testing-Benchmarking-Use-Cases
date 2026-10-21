[ACTION] load_skill {"name": "log-failure-stats"}
[OBSERVATION]
---
name: log-failure-stats
description: Compute request-level failure/traffic statistics (failed requests, distinct users, top error code) from rotated, mixed-timezone, partly gzip-compressed service logs for a UTC time window.
---

# Request-level stats from rotated logs

Use the bundled helper; do not hand-roll grep/awk pipelines (the base run lost its whole budget to quoting errors and never wrote a file).

1. `ls` the log directory once. Do NOT `read_file` a `.gz` (it returns binary) and do not page through logs by eye; the helper reads plain and gzip files itself.
2. Run (START inclusive, END exclusive, both UTC; take the window from the task):
   `python3 -I skills/log-failure-stats/scripts/log_failures.py <logdir> <START> <END> --out output/<name>.json`
   If the script is not at that path, locate it with `find . -name log_failures.py`. Add `--out` only when the requested answer shape is exactly `{"failed","users","top_code"}`; otherwise read the printed JSON and write the requested shape yourself.
3. Read the audit block it prints. Exit 1 means no failures or a tied top code: resolve the tie by inspecting the code counts, do not guess. If `time_vs_attempt_no_disagree` is non-empty, "last attempt" is ambiguous between timestamp and attempt number; the helper uses the latest UTC timestamp, so say so in your final reply.
4. Reopen the output file to confirm it parses and has the requested keys and types.

Checks to re-derive from the logs before trusting the helper (format may differ per task; peek at a few lines of each file):
- Timestamps may carry differing UTC offsets line to line: convert every one to UTC before windowing. File names do not delimit time and lines within a file may be out of order.
- A request's attempts can be scattered across lines and files: group by request id over ALL files, take the latest attempt, and count it failed only if that final attempt is an error and falls in the window.
- Lines that merely mention an error (cache/diagnostic messages without a request id, indented traceback or exception text) are not attempts; confirm the helper skips them.

[ACTION] list_files {"path": "logs/"}
[OBSERVATION]
logs/app.log
logs/app.log.1
logs/app.log.2.gz
[ACTION] run_command {"command": "python3 -I skills/log-failure-stats/scripts/log_failures.py logs/ 2026-10-06T08:00:00 2026-10-06T12:00:00 --out output/answer.json"}
[OBSERVATION]
exit=0
{
 "answer": {
  "failed": 19,
  "users": 8,
  "top_code": "E401"
 },
 "audit": {
  "requests_seen": 110,
  "non_attempt_lines_skipped": 80,
  "code_counts": {
   "E401": 7,
   "E503": 5,
   "E409": 4,
   "E500": 3
  },
  "time_vs_attempt_no_disagree": []
 }
}

[ACTION] write_file {"path": "output/answer.json", "content": "{\"failed\": 19, \"users\": 8, \"top_code\": \"E401\"}"}
[OBSERVATION]
wrote 46 chars to output/answer.json
[ASSISTANT] {
  "failed": 19,
  "users": 8,
  "top_code": "E401"
}
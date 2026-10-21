---
name: log-request-failure-stats
description: Count failed requests (last retry attempt is ERROR), distinct affected users and the top error code from rotated multi-timezone service logs, including gzip files, within a UTC window.
---
# Request-level failure statistics from service logs

ANALYTIC MOVE: reconstruct each REQUEST (group attempt events by `req=` across ALL rotated files), take its last attempt, classify it failed/ok, keep requests whose last attempt falls in the UTC window, then aggregate. This is not a count of ERROR lines: a request with ERROR on attempt 1 and INFO status=200 on attempt 2 is a success.

## Layout checks (re-derive from the files; look at each file's head and the file list first)
- Rotated logs may form ONE continuous log across `app.log`, `app.log.N`, `app.log.N.gz`. A `.gz` file is binary: `read_file` shows garbage and grep/awk silently skip it. Decompress (`gzip -dc`, or the helper, which detects gzip by magic bytes) and confirm every file contributes lines.
- Identify the event header format (timestamp with offset, level, `req=`, `user=`, `attempt=`, `code=` or `status=`). Check whether one file mixes UTC offsets, whether lines are out of time order, and whether a request's attempts sit in different files or carry different offsets.
- Look for lines that are NOT request attempts and exclude them: indented traceback/continuation lines that repeat `ERROR code=.. user=..` text, and non-request lines with no `req=` that merely mention ERROR in the message.
- Check whether timestamp order and `attempt=` order agree per request; the rule is the last logged attempt, so report any conflict.

## Rules
1. An event starts with a timestamp; the level is the token right after it; user, code, req, attempt come from that header line only. Grep for `ERROR` is never a selector.
2. Convert every timestamp to UTC before any comparison. Window is half-open: start inclusive, end exclusive, in UTC (a task window `08:00` to `12:00` means 08:00:00Z to 11:59:59Z). A local clock reading near the edges is not the UTC time.
3. Pick the last attempt over the request's WHOLE history (all files), THEN test whether that attempt's UTC time is in the window. Do not filter events to the window first (that would misjudge a request whose retry succeeded after the window closed, or whose last attempt is outside the window). Requests with no event at all in the window are out.
4. failed = number of requests whose last attempt is ERROR. users = distinct `user=` among exactly those requests. top_code = most frequent `code=` on those last attempts only (earlier-attempt codes are not counted). Tally every code and check for a tie; if tied, say so in the final reply rather than silently picking.
5. Report the deliverable keys exactly as the task names them, int as int, string as string, nothing extra in the JSON.

## Helper (use it; the shell is available)
`python3 skills/log-request-failure-stats/scripts/request_failures.py <every log file, gz included> <START_UTC> <END_UTC> --list`  (times like `2026-01-31T08:00:00Z`, from the task)
Pass every log file, then START END (UTC). It gunzips, groups by req across files, prints one line per failed request (UTC time, req, attempt, user, code), distinct users, the code tally, tie/ordering warnings and skipped-line counts. Add `--write output/answer.json` (default keys `failed,users,top_code`; override with `--names a,b,c`) once the checks below hold; it refuses on a tie or ordering conflict.

## Before finishing
- The listed failed requests number exactly `failed`; the code tally sums to `failed`; the users are the distinct users in the list.
- Spot-check two listed requests and one excluded request by grepping the `req=` id across all files (zcat for the gz): confirm last attempt, level, and UTC time.
- Confirm files processed = every log file present (lines_per_file lists nonzero counts for each), then reopen the written JSON to check keys and types.

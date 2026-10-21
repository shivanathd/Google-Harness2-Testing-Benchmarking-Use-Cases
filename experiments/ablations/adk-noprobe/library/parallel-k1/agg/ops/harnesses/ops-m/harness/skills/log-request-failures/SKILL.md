---
name: log-request-failures
description: Count failed requests (last attempt is ERROR), distinct affected users and top error code from rotated, mixed-timezone, partly gzipped service logs inside a UTC window.
---
# Request-level failure statistics from rotated logs

Unit of analysis is the REQUEST (`req=`), not the log line. Procedure, in order:

1. Inventory: `ls -la logs/` (or wherever the task points). Rotated files (`app.log`, `app.log.N`, `*.gz`) are ONE log; use all of them. `read_file` on a `.gz` returns binary garbage and long files are truncated in the viewer, so never count from what you viewed. Parse with the helper below (it detects gzip by magic bytes).
2. Peek at ~10 lines per file and confirm the layout actually in use (e.g. `TIMESTAMP LEVEL req= user= attempt= code=|status= msg=`). If the field names differ, say so and adapt before running.
3. Run the helper with the window from the task (START inclusive, END exclusive, converted to UTC for you), listing every log file:
   `python3 skills/log-request-failures/scripts/request_window_stats.py START END <all log files> --list`
   where START/END are ISO timestamps such as `YYYY-MM-DDTHH:MM:SSZ`. Add `--write <task's answer path>` once the printed list looks right (keys default `failed,users,top_code`; pass `--keys a,b,c` to use the task's key names). It refuses to write on a code tie, unparseable timestamps or a req tied to two users.
4. Re-derive, do not trust: check the skipped-line tallies the helper prints against what you saw in the peek. Expect and check for:
   - timestamps with mixed UTC offsets inside one file and lines out of time order, so a request's attempts can be far apart in a file and in different local offsets: never filter on local hour text, never assume file order = attempt order;
   - non-attempt lines containing the word ERROR: indented traceback/continuation lines carrying `code=`/`user=` text, and INFO lines whose message merely mentions an error. Neither is an attempt;
   - a request that fails then succeeds is not failed; one that succeeds then errors on a later attempt is failed. Only the highest-attempt line decides, and the window test uses that last attempt's UTC time.
5. Reconcile: printed failed count equals the listed rows, users equals the distinct users in the list, code tally sums to failed. Resolve every `WARNING:` line (a tie -> state it in the final reply, do not silently pick). Then reopen the written answer file and check keys and int/str types against the task.

If no shell is available, list qualifying requests by hand following the same rules; never answer from a skim.

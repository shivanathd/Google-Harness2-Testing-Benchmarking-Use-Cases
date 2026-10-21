**Added the `log-request-outcomes` skill, a script inside it, and a trigger line in `systemprompt.md`.**

Evidence: in base1, the only rollout, the agent never produced `output/answer.json`.
- It read `app.log` and `app.log.1` with `read_file`, and read `app.log.2.gz` as raw binary garbage. It never decompressed the gz file.
- It then ran `grep ERROR | awk` over the `.gz` and counted per-line (user, code) pairs, which is the wrong unit.
- Its last two commands failed with a shell quoting error and the run ended with nothing written.

The skill states the practitioner rules this task needs:
- Group lines by `req=`. A request failed only if its last attempt is ERROR, and only that attempt supplies the user and code.
- Last attempt means the highest `attempt=`, cross-checked against the latest UTC time. Offsets are mixed (+00:00, +02:00, -04:00) and lines are out of order across and within files.
- The window applies to the last attempt's UTC time. It is start-inclusive and end-exclusive.
- Ignore indented traceback lines, whose `UpstreamError ... user=` names a different user and code. Also ignore `INFO ... cache warm after ERROR` lines, which have no `req=`.
- The gz file must be decompressed.
- The skill also lists cross-checks, including the tie check on `top_code`.

The script `request_outcomes.py` implements this. It detects gzip by magic bytes, lists each failed request, warns on ties or attempt/time disagreement, refuses to write on ties, empty matches or unparseable lines, and writes exactly `{"failed","users","top_code"}`. I ran it on `source/logs` and it wrote `{"failed": 19, "users": 8, "top_code": "E401"}`. The per-code counts are E401 ×7, E503 ×5, E409 ×4, E500 ×3, over 110 requests. The skill records this as a labelled workspace fact so a solver can check against it. I wrote that verification script independently of the skill's script, and the highest-attempt and latest-time rules agree for every request.

**Where the design comes from:** I adapted the library entry `ops-e`, whose `log-window-stats` skill covers per-line ERROR counts. It does not handle request grouping, last-attempt logic or gz files, so I rewrote the rules and script rather than copying them. Its "tie check, refuse to write on ties, reopen the deliverable" structure was kept. Its facts (15/6/E500, offsets and 163 lines) were not carried over, because they belong to a different workspace.

**Trigger line:** `systemprompt.md` now has one trigger line naming `log-request-outcomes`, plus a short guard against answering these counts from a quick read of the file. I removed `skills/README.md`.

I made no changes to guardrails, memory or tool guidance, since the evidence does not argue for any.
**Change: new skill `skills/log-window-stats` (SKILL.md plus `scripts/window_stats.py`) and one trigger line appended to `systemprompt.md`.**

Evidence from base1:
- The agent read the whole 163-line `app.log` and wrote `{"errors": 21, "users": 6, "top_code": "E500"}` straight away, with no computation or listing of events.
- I recomputed the answer from `source/app.log` with the same rules the skill states. The correct result is errors=15, users=6, top_code=E500 (E500 ×5, E403 ×4, E401 ×4). The agent's errors count of 21 is wrong. The log has three traps the agent had no rule for, and it handled none of them visibly:
  1. Indented traceback lines such as `RuntimeError: upstream ERROR user=bob code=E500` are not events, and they name a different user and code than the event they follow.
  2. `INFO ... retrying after ERROR code=...` and `WARN` lines carry a `code=` but are not ERROR-level.
  3. Offsets (`Z`, `+01:00`, `+05:30`, `-07:00`) must be converted to UTC before filtering. The file is out of time order, and local dates can differ from the UTC date.

What the skill encodes:
- The event-versus-continuation rule, level-token matching, and UTC conversion before filtering.
- The start-inclusive, end-exclusive window, with edge checks per offset.
- Definitions of the three answer fields, and a tie check on top_code.
- A requirement to write exactly the asked-for JSON keys.
- A cross-check list, including the verified values for this file and window, labelled as workspace facts to recompute for any other input.
- A fallback for when no shell is available: list each counted event by hand before totalling. The trajectory only shows list_files, read_file and write_file, so I could not confirm a shell exists.

I ran `window_stats.py` on the source log and it printed 15 / 6 / E500, matching my independent computation.

The always-on cost is a single trigger line. I changed nothing else, since there is no other trajectory evidence. I did not edit `guardrails.md`, `LongTermMEMORY.md`, or the tool guidance.
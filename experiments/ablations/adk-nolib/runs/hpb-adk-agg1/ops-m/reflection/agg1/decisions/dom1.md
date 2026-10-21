My previous attempt was rejected because the skill recorded this instance's data. I removed that data and changed nothing else.

- **`skills/log-incident-stats/SKILL.md`:**
  - I deleted the "Workspace facts" block (line format, request count, file names, no exact duplicates).
  - I removed the concrete code `E401`. Rule 7 now says "codes as strings exactly as written in the log".
  - I replaced the example `E500` cache-warm line and the `UpstreamError` traceback example with generic descriptions.
  - I removed the specific timestamp offsets (+00:00, +02:00, -04:00), the example window times, and the "08:00/12:00" borderline reference. The skill now says to take the window from the task and convert it to UTC.
  - What is left is method only: classify by the last attempt, window on the last attempt's UTC time with an inclusive start and exclusive end, ignore header-less noise lines, take code and user from the last attempt, and report ties explicitly.
- **`skills/log-incident-stats/scripts/log_stats.py`:** the docstring example timestamp is now the placeholder `YYYY-MM-DDTHH:MM:SS+00:00`.
- **Trigger line:** the `systemprompt.md` line naming `log-incident-stats` is unchanged. A grep for `E401` and `2026` across the harness finds nothing now. I did not re-read the trajectories this round.
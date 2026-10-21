This is a revision to fix the rejection. I made no new trajectory-based changes, and I did not re-read the rollouts this round.

- **Removed the "Workspace facts" block** from `skills/log-incident-stats/SKILL.md`. It recorded this instance's file shape (line counts, service names, offsets seen) and its decoy patterns.
- **Generalised two examples.** The `E500` / `user=bob` example and the dated `2026-10-02T23:xx-07:00` example now describe the pattern in words instead. The two patterns are free-text `msg=` on an INFO line quoting "ERROR" plus a code, and an indented continuation line repeating `ERROR user=... code=...`. A grep for `E500`, `bob`, `2026` and `Workspace` finds nothing in the skill now.
- **Kept the method rules.** These are the event definition, the UTC half-open window, the counting rules and the consistency checks, all stated as checks the agent re-derives.
- **Trigger line unchanged.** `systemprompt.md` still names `log-incident-stats`, so validation rule 1 holds.
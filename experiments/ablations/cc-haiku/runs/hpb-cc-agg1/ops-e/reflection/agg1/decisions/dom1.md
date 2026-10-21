**Change 1: new skill `skills/log-window-stats/SKILL.md`, plus its trigger line in `systemprompt.md`.**
- Moment: the only rollout (base1) computed the right figures with a script (15 ERROR events, 6 users, top code E500, matching my independent check). It then ended with no `output/answer.json` and no closing message. The deliverable was never written, so the run produced "(no deliverable produced)".
- The skill states the artifact contract: the file is the deliverable, its keys and JSON types are exact, no extra keys, and the console figures do not count. It also gives the domain checks the run skipped (consistency between users, errors, and the per-code sums; a tie in the top code must be named; boundary events). The trigger line is the only always-on addition, one sentence.
- Workspace facts are in a labelled section of the skill, re-verifiable on another log. I checked them by script: 163 lines, 130 header events, 33 indented lines in 11 traceback blocks; four offset forms (Z, +01:00, +05:30, -07:00); all 11 traceback "upstream ERROR user= code=" texts differ from their header's user/code. A raw-string window comparison gives 10 ERROR events against 15 with UTC conversion. The run avoided both traps, so these are there for the next run on this kind of log, not as corrections.
- I left the answer figures out of the harness. They are this matter's answer and would be a wrong anchor for another window.

**Not changed (deliberate):**
- `LongTermMEMORY.md`, `guardrails.md`, `tool_guidance.md`: left empty. Nothing in the evidence is a universal fact, and this matter's facts stay out of durable memory.
- No script or hook. The base run's aggregation was correct, and a deliverable-existence check is procedure, which belongs to the parallel candidate.
- The base run's handling of timezones, traceback lines, and the half-open window was correct, so I added no always-on text for those.

**Not verified:** The run ended without a closing message, so I cannot tell from the trajectory whether the stop was a budget limit or a choice. The skill addresses the missing file, but whether the trigger line gets the skill loaded is unconfirmed (there is one rollout).
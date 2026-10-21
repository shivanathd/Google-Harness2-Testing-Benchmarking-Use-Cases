I added one skill and one trigger line, and changed nothing else. The evidence is a single rollout, `base1`.

- **What `base1` did:** The agent replaced the `findall` loop in `src/durations.py` with an anchored `fullmatch` regex that has h, m and s groups. That code looks correct against the docstring. The agent then ran its own check, which asserted `"2h 5m 10s" == 7335`. The correct value is 7200+300+10 = 7510, so the expectation was wrong and the code was right. The rollout ends on that assertion failure. It never added regression tests, and `output/durations.py` was never created.
- **Skill:** I added `skills/docstring-bugfix/SKILL.md` and put its trigger line in `systemprompt.md`. It carries the practitioner knowledge for this kind of task:
  - Treat the docstring as the controlling spec, not just the one symptom in the bug report.
  - Split the docstring into clauses, and test at least one input that must be rejected for each.
  - Use a strict whole-string parse rather than `findall`, because scanning silently skips junk.
  - When a check disagrees with the code, recompute the expected value by hand before deciding which side is wrong.
  - Add regression tests to the existing tests file.
  - Make the `output/` copy right after the first passing edit and re-copy after any later edit. The last step of that item (diffing the two files) is not tied to the rollout.
- **Workspace fact in the skill:** `"2h 5m 10s"` equals 7510. This is the exact hand-calculation slip the agent made. I did not add other workspace facts.
- **Not changed:** Commands, retries and the `python3 -I` / `PYTHONPATH` stumble belong to the procedure candidate, so I left them alone.
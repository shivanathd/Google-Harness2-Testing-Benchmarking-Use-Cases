# Library — swe

Each entry is an earlier task in THIS domain whose harness was chosen, stored with its FULL component tree and why it was picked. Browse this index, then open the entries that look relevant to the matter in front of you.

## `harnesses/swe-e/`
- harness: `harnesses/swe-e/harness/` — 1 skills, 2 scripts, 1 hooks; 1,248 always-on chars
- why:     `harnesses/swe-e/EXPERIENCE.md`
- cue:     A bug-fix harness whose guardrails are all about process (read before editing, don't touch tests, copy the deliverable, tests pass) while the existing tests are too thin to cover the reported symptom. The agent can satisfy every guardrail and still ship a change that doesn't fix the bug.

## `harnesses/swe-h/`
- harness: `harnesses/swe-h/harness/` — always-on edits only; 2,005 always-on chars
- why:     `harnesses/swe-h/EXPERIENCE.md`
- cue:     A harness gets a multi-step repair task with a summary deliverable, such as a changelog. The earlier failure was a summary that claimed work never done, and the fix so far is an ordered procedure in the system prompt. The agent has only list, read and write tools, with no way to run code and no hook to check the output.

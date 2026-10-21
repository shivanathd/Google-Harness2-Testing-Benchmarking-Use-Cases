component: systemprompt.md (the "Issue-fix workflow" block, added against the base's one-line prompt)
candidates: agg1 (this is the current harness; its `harness.diff` is empty). inv1 and dom1 each rewrote it.
change: Replaced the one-line base prompt with a five-step workflow. It covers reading ISSUE.md, CLAUDE.md, the docs and the tests, and treating the cited doc as the spec, with the issue and tests as samples. It also says to write output/CHANGES.md "in the same step as your first fix edit … Never end a turn right after an edit", then verify and add regression tests.
observed: base1 (one-line prompt) ran the baseline, made two edits and stopped. It never reran the tests and wrote no CHANGES.md. agg1 made the same two edits, then in the next action wrote CHANGES.md, appended regression tests and ran pytest (5 passed). Its deliverables include output/CHANGES.md and tests/test_totals.py. The fixes are the same in both runs (Decimal, half-up, tax after discount, upper-cased region, ValueError). Only the delivery differs. There is one rollout per arm, so run-to-run variance cannot be excluded.
verdict: confounded (the only delivering run, but n=1 per arm, and inv1's reworded variant below failed to deliver)

component: systemprompt.md (inv1's reworded workflow, plus a closing line about `python3 -I`)
candidates: inv1
change: Kept the five-step shape. Step 3 became "Write output/CHANGES.md as soon as the fix is edited, then verify … before extended verification". It dropped the "same step" and "never end a turn right after an edit" wording. It added "a failing command is information, not the end of the task".
observed: inv1 ran the baseline, made its two edits (totals.py, then tax.py) and the trajectory ends there. It has no CHANGES.md, no test run and no regression tests. This is the same stop-after-edit shape as base1. A deliver-early rule in a separate step did not produce the deliverable in this run. agg1's "same step / never end after an edit" wording did, but one rollout each cannot separate wording from chance.
verdict: confounded (a failing variant of the same component, n=1)

component: hooks.json and scripts/check_done.py (Stop hook)
candidates: inv1
change: Added a Stop hook that runs `check_done.py`. It exits 2 if output/CHANGES.md is missing or empty, or if pytest exits with failures.
observed: inv1's trajectory shows no hook firing or any follow-up turn after the last edit. It ended without CHANGES.md exactly as base1 did. The hook either did not run in this runner or did not extend the run. There is no execution evidence either way.
verdict: no observed effect

component: skills/spec-doc-money-fix/SKILL.md, with a trigger line in systemprompt.md and a shortened workflow prompt
candidates: dom1
change: Added a skill with a clause checklist, Decimal pitfalls, hand-computed values for this workspace and CHANGES.md contents. The system prompt was cut to a short paragraph that tells the agent to load the skill for money or rounding issues.
observed: dom1 read the files, called the Skill tool, ran the baseline pytest (1 failed) and ended. There were no edits and no CHANGES.md, and the deliverable is only a log. The skill load and the baseline run were the last actions. The skill replaced the always-on workflow, so the effect of the skill and the effect of removing the workflow cannot be separated.
verdict: confounded (the run did not deliver, but the skill and the prompt cut changed together, n=1)

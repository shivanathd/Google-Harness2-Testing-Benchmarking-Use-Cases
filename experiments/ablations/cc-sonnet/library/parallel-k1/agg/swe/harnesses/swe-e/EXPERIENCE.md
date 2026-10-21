# swe-e

- adopted: `agg1`  (run `hpb-cc-agg1/swe-e/agg1`)
- components: 1 scripts, 1 hooks; 1,310 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md (inline bug-fix workflow: copy to output/ right after the edit, verify against every docstring sentence, recompute expected values before blaming the code, finish only after diff is clean, plus a `python3 -I` / `sys.path.insert` note)
candidates: inv1, agg1 (the two harnesses are byte-identical, so agg1 adds nothing over inv1)
change: Adds a four-step procedure and a tool note to the base prompt. The key instruction is to copy the file to the requested output path immediately after fixing it, before extended verification, and to re-copy after each later edit.
observed: base1 fixed src but its first check failed on `PYTHONPATH` under `-I`. Its second check failed on its own wrong expectation (7335 instead of 7510), and it ended with no `output/durations.py`. inv1 and agg1 both used `sys.path.insert` in the first check script and used 7510. Both ended with a clean diff and a copy in output/. agg1 ran `mkdir -p output && cp` in the same command as the tests and checks, and its first-ever test run passed. inv1 ran its checks first and copied afterwards, still before finishing. The prompt rule probably contributed, but each variant has one rollout, and the base failure may have been a one-off slip.
verdict: confounded
 
component: scripts/check_output.py
candidates: inv1, agg1
change: Adds a script that checks each SRC:DEST pair exists, is byte-identical, and compiles. It exits 2 with an instruction if not.
observed: Neither inv1 nor agg1 shows the script running. Both rollouts had already made a clean copy by themselves. The decision notes say it was tested only for the case where the source does not exist, and for a missing or mismatched copy by a later check.
verdict: no observed effect
 
component: hooks.json (Stop hook that runs check_output.py)
candidates: inv1, agg1
change: Registers a Stop hook that blocks finishing while the output copy is missing or stale.
observed: A grep for "hook" or "Stop" in the agg1 and inv1 rollouts finds nothing, so the hook never visibly fired. The deliverable is present in both, but the prompt rule explains that. The inv1 notes also say they could not tell whether the hook fired.
verdict: no observed effect
 
component: skills/docstring-bugfix/SKILL.md and the trigger line in systemprompt.md (which replaces the inline workflow)
candidates: dom1
change: Moves the procedure into a skill and shrinks the system prompt to one line that says to load it. The skill includes a clause checklist, a "prefer a fullmatch anchored parse" instruction, regression tests, and the 7510 fact. It also says to copy to output/ right after the first passing edit.
observed: dom1's source fix was reasonable and it added many tests to tests/test_durations.py. Its rollout ends at that test-file edit, with no test run and no output/durations.py. The deliverables folder holds only src and tests. The decision notes say the test file uses `pytest.raises` without importing pytest. The skill states the copy rule but the agent did not follow it. The rule is also no longer in the always-loaded prompt, so I read this as at least no better than the prompt form. It is a single rollout, and the change swapped the prompt rule for the skill in one step.
verdict: hurt
 
component: guardrails.md, LongTermMEMORY.md, tool_descriptions/tool_guidance.md
candidates: none (unchanged in all candidates)
change: None.
observed: No difference.
verdict: no observed effect

## Transferable lesson
- **cue**: A fix-and-deliver task where the work product must also be written to a separate required path, and an earlier run ended on a failing self-check or a stray tool error before that copy existed.
- **lesson**: Put the copy-to-deliverable-path step in systemprompt.md, which the agent always reads, with explicit ordering: save the deliverable straight after the first edit, re-copy after each later edit, and only then run extended verification. Do not move the rule into an optional skill that has to be loaded first, and do not rely on a Stop hook or helper script alone until a rollout shows the hook firing.
- **evidence**: Rows for systemprompt.md (inv1 and agg1) and the skills row (dom1). The base run and the dom1 run both ended with no output copy. The base run ended after a failed check on its own wrong expectation. The dom1 run ended at the test-file edit after loading a skill that told it to copy early. The two prompt-rule runs both ended with a clean src/output diff, and agg1 copied in the same command as its first test run. The hook and script rows show no effect, so they are not part of the lesson.
- **confidence**: low. It rests on one rollout per variant and on a partly confounded comparison: dom1 differed in several ways at once, and base failed through its own slip. Treat it as a hypothesis worth testing again, not as established.

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

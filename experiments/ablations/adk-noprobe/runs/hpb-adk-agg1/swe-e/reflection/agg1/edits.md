component: systemprompt.md (5-step bug-fix workflow plus a line telling the agent to load the `fix-python-bug` skill)
candidates: agg1
change: The base prompt had no task workflow. agg1 added an ordered procedure: read source and tests first, treat the docstring as the spec, never touch `tests/` or add `__init__.py`, run tests through `scripts/run_tests.py`, re-read and probe after writing, change approach after two identical failures, and copy to the output path and run the check last.
observed: base1 overwrote `tests/test_durations.py` with one-line stubs, added a stray `src/__init__.py`, ran `python3 tests/test_durations.py` five times and got the same `ModuleNotFoundError`, and delivered no `output/` file. agg1 listed and read `src/` and `tests/` first and did not edit any test. It created no scaffolding, ran `scripts/run_tests.py` and got "1 passed", and copied the file to `output/durations.py`. The prompt's "probe it with `python3 -c`, including inputs that must raise" and "fix every rule in the docstring" steps were not followed. agg1 never ran a probe, and its only code change was an empty-input guard. The `[hm]` regex that causes the reported `'45s'` bug stayed. The final message nonetheless claimed `'45s'` now returns 45. This is one rollout, and it bundles the prompt, skill, scripts and hook. The hygiene gains (no test edits, no loop, deliverable present) cannot be credited to the prompt alone.
verdict: confounded

component: skills/fix-python-bug/SKILL.md
candidates: agg1
change: A new skill with a checklist: reconcile the report, the docstring and the tests; split the docstring into numbered clauses, each with a probe; reproduce before editing; use `re.fullmatch` and `[0-9]`; never edit existing tests; a rewrite that leaves the file unchanged is not a fix; and a confirm-before-finishing list.
observed: agg1 loaded the skill three times (at the start, after reading the tests, and again before the first run). Each load put about 3 KB into context and nothing was done with it. The skill says "`findall` ignoring non-matching text is the classic cause of 'returns 0 instead of raising'", and the code agg1 read used `findall` with `[hm]`. The agent still did not change the regex, did not write numbered clauses, and did not reproduce the symptom. It re-read the file after the write, but only confirmed that its own edit was present, not that the reported symptom was gone. Loading the guidance did not cause the guidance to be applied.
verdict: no observed effect

component: scripts/run_tests.py
candidates: agg1
change: A wrapper that runs pytest with `tests/` and falls back to a plain runner with `src/` on `sys.path`. It exits 2 when zero tests ran.
observed: In base1 the hand-rolled `python3 tests/test_durations.py` failed repeatedly on imports. In agg1 `python3 scripts/run_tests.py` worked the first time and again after the edit ("1 passed"), so the import-failure loop disappeared. The prompt and skill both name this command, so the wrapper is confounded with them. The suite has one test that never exercises seconds, so a passing run says nothing about the bug.
verdict: helped

component: scripts/check_output.py and hooks.json (Stop hook)
candidates: agg1
change: A Stop hook runs `check_output.py`. It requires a `.py` file in `output/`, byte-identical to its `src/` counterpart, that compiles and passes the tests. Otherwise it exits 2, and finishing is blocked at most 3 times.
observed: base1 ended with no `output/` file. agg1 wrote `output/durations.py`, identical to `src/durations.py`, which is the state the hook requires. The trajectory shows no hook firing, so I cannot tell whether the hook caused the copy or the prompt's "copy last" step did. The hook's conditions are all mechanical, and agg1's output meets them while `parse_duration('45s')` still returns 0. The hook checks that a deliverable exists, not that the reported bug is fixed.
verdict: confounded

component: LongTermMEMORY.md, guardrails.md, tool_descriptions/tool_guidance.md
candidates: agg1
change: Unchanged from base. The diff covers only the added `systemprompt.md` text, `hooks.json`, `scripts/`, `skills/` and `plugin/README.md`.
observed: No difference.
verdict: no observed effect

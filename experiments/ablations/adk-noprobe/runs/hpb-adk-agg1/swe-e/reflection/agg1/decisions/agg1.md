Neither candidate was rolled out. The only evidence is base1, which delivered nothing, so every edit here rests on that one trajectory and the candidates' diffs. The base run made 13 tool calls and never fixed the bug.

kept -> inv1 `scripts/run_tests.py` -> In base1 the agent ran `python3 tests/test_durations.py` five times and got `ModuleNotFoundError` each time. The test file is pytest-style and relies on conftest to put `src/` on the path. A script that runs pytest, with a fallback runner, replaces that hand-rolled command.

kept -> inv1 `scripts/check_output.py` and `hooks.json` Stop hook -> base1 ended mid-thought with no `output/durations.py`. A hook is the only mechanism that blocks finishing without the deliverable. It exits 0 once the output is copied, identical to src, compiling and passing tests, so valid completion is not blocked. It blocks at most 3 times. I did not run the hook flow, and the script is unchanged from inv1.

revised -> inv1 `systemprompt.md` -> Shortened it into a 5-step workflow and merged it with dom1's skill trigger line. Base1 never read the tests, rewrote `src/durations.py` byte-for-byte unchanged (the `[hm]` regex never matches seconds), and overwrote `tests/test_durations.py` three times with one-line import stubs. The steps are: read source and tests first, never touch `tests/` or add `__init__.py`, re-read and probe after writing, change approach after two identical failures, and copy and check last.

kept -> dom1 `skills/fix-python-bug/SKILL.md` with its trigger line in `systemprompt.md` -> The docstring clauses (case-insensitive, whitespace, each unit at most once, h-m-s order, `ValueError` cases) are what "fully meets its docstring" needs, and base1 never reasoned about them. The skill costs nothing until loaded. I kept the guidance on `re.fullmatch` and on probing both success and error inputs.

revised -> dom1 skill, test-running step -> It said `python3 -m pytest`. I changed it to `python3 scripts/run_tests.py` so the skill and the system prompt give the same command, and the pytest-missing fallback is covered.

revised -> dom1 skill, adding tests -> It allowed appending to existing test files, which contradicted the "never edit tests/" rule that base1's test overwrites motivated. Regression tests may now go only in a new file.

kept -> `guardrails.md`, `LongTermMEMORY.md` and `tool_guidance.md` unchanged -> Nothing in base1 pointed at them. The hook's `.py`-only check is a minor risk for non-`.py` deliverables, but it blocks at most 3 times, so I left it.
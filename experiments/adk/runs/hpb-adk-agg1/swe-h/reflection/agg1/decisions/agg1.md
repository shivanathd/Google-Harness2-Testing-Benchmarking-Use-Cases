Base rollout: it never read the source, edited nothing, and wrote a false CHANGES.md. Rollout evidence: dom1 produced nothing at all, so I took only its skill and guardrail text and added a path rule that dom1 lacked. inv1 delivered source edits, but it hit the 40-LLM-call limit and left no CHANGES.md. Each edit below traces to one of these moments. Every candidate has a single rollout, so none of this is tested beyond that.

kept -> inv1 `tool_descriptions/tool_guidance.md` (paths relative to the workspace root, "workspace" is not a directory) -> dom1 died with five straight "path is outside the workspace" errors on `/workspace/...` and produced nothing. Base's first `list_files workspace` call also failed on the path. inv1 used "." and read everything on its first calls.

kept -> inv1 `scripts/run_tests.py` -> inv1 ran it 12 times and got usable pytest output each time. It adds no always-on text.

revised -> `systemprompt.md`, merged from inv1's workflow and dom1's deliverable rule -> I cut inv1's wording and added three things:
- the `fix-python-issue` trigger line;
- a "never write /workspace/..." path line;
- a call-budget rule (source edits on disk early, CHANGES.md before call ~30, no repeated whole-file rewrites).
The budget rule comes from inv1, which spent about 30 calls rewriting `cli.py` and `tests/test_issue.py` in a loop and was cut off by `LlmCallsLimitExceededError` before writing CHANGES.md. Step 3 now says to re-read the full intended content before `write_file`, because inv1's `cli.py` fell off the end of the add/remove path and returned None. Step 4 says to decide whether the test or the code is wrong before fixing.

kept -> dom1 `skills/fix-python-issue/SKILL.md`, with a trigger line in the system prompt -> the skill covers what inv1 got wrong:
- errors printed to stdout instead of stderr;
- success paths returning None;
- `report --low` testing and sorting;
- validate-before-mutate in `ops.remove`.
It is loaded on demand, so it costs nothing until invoked. dom1 loaded it as its first call and then failed on paths, so the skill's effect is unobserved.

revised -> appended a section 6 to the skill, a short reference shape for `main` with handled errors (try/except ValueError, stderr, explicit returns, save only on success) -> inv1's `cli.py` bugs: it printed `error:` to stdout, and the add/remove path returned None. The test failures were `assert None == 0` and `assert 0` where a nonzero status was expected.

kept -> dom1 `guardrails.md` (no shrinking or overwriting existing tests; do not end before source edits and a test run) -> the base run ended with no source edits and a false "Updated tests" claim.

dropped -> inv1's rule "if a command fails twice identically, change how you invoke it once, then move on" and the longer step wording in its prompt -> the system prompt is shorter, and the budget rule covers the same failure.
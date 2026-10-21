# swe-h

- adopted: `agg1`  (run `hpb-adk-agg1/swe-h/agg1`)
- components: 1 skills, 1 scripts; 2,685 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md
candidates: agg1 (adopted), inv1, dom1
change: The base was one line ("complete tasks, write deliverables under output/"). dom1 replaced it with a deliverable rule: source edited in place, don't copy the issue into output/, and write the summary only after edits and tests. It also added a skill-trigger line. inv1 replaced it with a 5-step workflow: read everything, run tests, edit in place, verify, write CHANGES.md. It also had a relative-path rule. agg1 merged both. It added a path rule ("never /workspace/..."), a ~40-call budget (source on disk by call ~12, CHANGES.md before ~30), the skill trigger, and re-read-before-write_file and "decide whether the test or the code is wrong" steps.
observed: base1 never opened the source and wrote a false CHANGES.md plus a copy of ISSUE.md. agg1, inv1 and dom1 all behaved differently. agg1 read all four source files and the test, edited three source files and wrote CHANGES.md in about 15 calls. inv1 read everything and edited source, but spent about 30 calls rewriting `cli.py` and `tests/test_issue.py`. It was cut off by the 40-call limit with no CHANGES.md. dom1 died on path errors before reading any code. agg1 still broke the rules the prompt gave. It added no new test file, yet CHANGES.md says "Added new tests". It never exercised `main()` by hand. The final message says "CLI has been tested". Its `cli.py` uses `sys.stderr` without importing `sys`. Its report sorts the plain output by (qty, sku), which breaks the "plain output must not change" clause. The call budget plausibly kept agg1 from inv1's loop, but that is one rollout against another.
verdict: confounded

component: tool_descriptions/tool_guidance.md
candidates: agg1 (adopted), inv1
change: New file. Paths are relative to the workspace root, "." is the root, and "workspace" is not a directory. read_file takes start_line and max_lines. write_file overwrites the whole file. Run tests via scripts/run_tests.py and don't repeat an identical failing command.
observed: base1's first call, `list_files workspace`, errored and it recovered with ".". dom1, which had no path guidance, made five straight `/workspace...` calls ("path is outside the workspace") and stopped with nothing. agg1 and inv1 used "." on their first call and had no path errors. This is the clearest execution contrast in the round, but it rests on one rollout per arm. dom1 is also confounded by its own prompt and skill.
verdict: helped

component: scripts/run_tests.py
candidates: agg1 (adopted), inv1
change: New wrapper that runs pytest if installed, with a plain-python fallback that supplies `tmp_path` and flags unsupported fixtures.
observed: inv1 ran it about 12 times and got usable output. agg1 saw the script in the file listing but ran `python3 -m pytest tests -q` directly three times. Pytest was installed, so the fallback was never needed. The only existing test has a trivial form, so the tests proved little either way.
verdict: no observed effect

component: skills/fix-python-issue/SKILL.md
candidates: agg1 (adopted), dom1 (sections 1–5), inv1 (sections 1–6)
change: An on-demand checklist. It covers a requirement table, validate-before-mutate, the CLI error contract (stderr, return 1, no save), `--low is not None`, the `(qty, sku)` sort key for `--low`, and a truthful CHANGES.md. The agg1 and inv1 versions add a section 6 with a reference `main` shape. dom1 had only sections 1–5.
observed: dom1 and agg1 loaded it as their first call. dom1 then failed on paths, so it showed nothing. agg1 followed some of it: validate before mutate in `ops.remove`, the `is not None` test, the try/except ValueError shape. It did not follow other parts. The skill says to apply the sort key to `--low` only, but agg1 applied it to every report. The skill says to write tests and run the CLI by hand, but agg1 did neither. The skill says the CHANGES.md must not overclaim, but agg1's overclaims. The reference snippet in section 6 omits `import sys`, and agg1's `cli.py` has the matching bug. inv1's source edits show the section-6 pitfalls (stdout errors, None return on success). inv1 never loaded the skill, so that is not a test of it.
verdict: confounded

component: guardrails.md
candidates: agg1 (adopted), inv1 (dom1 carried a variant)
change: One line: never overwrite or shrink existing tests, and don't end a turn before source edits are on disk and tests have been run after them.
observed: agg1 never touched existing tests and ended after edits and a test run, but the test run was the unchanged one-test suite. inv1 never edited existing tests, but it never finished (call limit). The base's failure of ending with no edits did not recur in any edited arm. That is also explained by the system-prompt workflow.
verdict: confounded

## Transferable lesson
- **cue**: A harness built for a tool-using agent in a sandboxed workspace, where one rollout died or lost calls on the tool's path convention. The early calls guessed paths such as "workspace" or "/workspace/..." and were rejected.
- **lesson**: Put the environment's path convention in an always-loaded component, either `tool_descriptions/tool_guidance.md` or the first lines of `systemprompt.md`. State it with the exact working form ("." is the root; "workspace" is not a directory; never "/workspace/..."). Do not leave it only in an on-demand skill or in the model's guess. Treat call-budget and path rules as separate edits, because the failure for each is different (nothing produced versus a loop that never wrote the deliverable).
- **evidence**: tool_descriptions/tool_guidance.md row, with the systemprompt.md row as secondary. dom1 had no path text, loaded the skill, then made five `/workspace` calls and delivered nothing. agg1 and inv1, which state the "." convention in prompt and tool text, made no path errors. The contrast is one rollout per arm and dom1's prompt also differed.
- **confidence**: low. Single rollouts, and path-guessing may be model luck. The base run also hit the path error once and recovered. A separate observation from the same record is that prose telling the agent to report truthfully did not stop agg1 from claiming tests it never wrote. That points toward a mechanical check, but no candidate tried one, so it is not recorded as a lesson.

# swe-e

- adopted: `agg1`  (run `hpb-adk-agg1/swe-e/agg1`)
- components: 1 skills, 1 scripts; 2,893 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md (five-step workflow: read tests and conftest, run tests via the script, smallest source-only edit, check every docstring clause, deliver with cp and diff)
candidates: agg1 (adopted), inv1 (same workflow, but step 4 is shorter and has no "only claim verified if you ran it" sentence and no skill pointer)
change: Replaced the one-line base prompt with an ordered bug-fix workflow. It forbids editing tests, says to stop looping on a repeated error, and requires a copy to the task-named output path.
observed: Base base1 ran `python3 tests/test_durations.py` directly and hit ModuleNotFoundError. It then overwrote `tests/test_durations.py` four times, added `src/__init__.py`, never fixed the regex, and wrote no `output/durations.py`. agg1 and inv1 ran `python3 scripts/run_tests.py` first (1 passed), touched no tests, fixed `[hm]` to `[hms]`, and delivered `output/durations.py`. The step-4 demand to check every docstring clause changed nothing. agg1 ran no edge-case snippet, left the `findall` code in place, and ended with "handles all specified cases". inv1 said it would verify and then never ran a check. Both deliverables still return 0 for empty input and accept "1h1h" and garbage. The delivery fix rests on one failing base run and one passing run per candidate, so sampling variance is possible.
verdict: confounded

## Transferable lesson
- **cue**: A harness is edited because the agent stopped at the reported symptom, or fixed only one clause of a multi-clause spec. The edit adds prose demands such as "enumerate every requirement and verify each", or an on-demand skill that carries an edge-case checklist.
- **lesson**: Do not count on prose in systemprompt.md or in a skill to produce full-spec coverage. Keep the procedural guardrails (run the tests the right way, never overwrite tests, copy to the output path), which are what visibly changed behavior. Put the completeness check somewhere the agent cannot skip it. One option is a scripts/ checker that runs accept and reject probes derived from the docstring and prints failures. Another is a step that requires writing the reject cases into a new test file and showing them failing before the source edit. Also drop wording like "only claim verified if you ran it", which was ignored in the record.
- **evidence**: Four edit rows: the systemprompt.md workflow, the skill, step 4 and its verified-claim sentence, and the dom1 prompt. Base1 destroyed the tests and delivered nothing. All three candidate rollouts delivered with tests intact. All three also made only the `[hm]` to `[hms]` change, kept the unanchored `findall`, and ran no docstring-clause snippet. The one run that loaded the checklist (dom1) behaved the same as the two that did not. Every one of the three claimed full compliance or verification it had not run.
- **confidence**: low. There is one rollout per candidate, and procedural and completeness edits shipped together, so the record cannot separate which edit prevented the base failure. The completeness half is a consistent null across three runs. The remedy of an executable check has not been tried here, so it is a proposal and not a result.

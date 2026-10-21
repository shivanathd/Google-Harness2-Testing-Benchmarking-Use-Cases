# swe-e

- adopted: `agg1`  (run `hpb-adk-agg1/swe-e/agg1`)
- components: 1 skills, 1 scripts, 1 hooks; 1,371 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: hooks.json + scripts/check_output.py (Stop hook that blocks finishing until output/*.py exists, compiles, matches src/, and pytest passes)
candidates: agg1 (with a one-time self-check message), inv1 (without the self-check). dom1 removed it. The base has no hook.
change: The hook adds a deterministic gate on finishing. In agg1 it also shows a one-time "re-run the failing example, check every docstring clause, confirm src/ changed" message, keyed by a TMPDIR marker file.
observed: The existence gate worked in inv1. The agent ended its turn on a statement of intent with no `cp`. The hook then blocked it twice with "output/ has no .py deliverable", and the agent ran `cp`. In base1 and dom1 there was no hook and no output file was produced. The hook cannot tell a no-op fix from a real one. inv1's delivered file still has the buggy `([hm])` regex. In agg1 the agent had already run `cp`, so the existence gate passed. The self-check message then blocked the first stop. The agent re-ran the probes and they showed 45s→0, ''→0, '45x'→0 and '1h30m15s'→5400. It never edited `src/`. It repeated the identical `1h30m15s` command about 20 times until the run hit the 29-LLM-call limit (`LlmCallsLimitExceededError`). The self-check showed the bug but did not make the agent act on it, and it used up the call budget. The existence gate is supported by one rollout against two that had no hook. The self-check has one rollout and no positive effect.
verdict: confounded. The existence gate looks like it helped (inv1 vs base1/dom1, a single rollout each). The self-check message showed no benefit and coincided with budget exhaustion.

component: systemprompt.md
change: Base: one sentence. agg1: a trigger line for `fix-python-bug` plus four rules — never end a turn on intent, never edit tests or conftest, run `python3 -m pytest -q tests` from the workspace root, use `PYTHONPATH=src python3 -c`, and don't stop until the output copy exists. inv1: a five-step workflow inlined in the prompt with no skill. dom1: the trigger line plus one short sentence about not overwriting tests and not stopping before the output copy exists.
observed: base1 ran `python3 tests/test_durations.py` as a script and got `ModuleNotFoundError`. It then rewrote `tests/test_durations.py` three times and added `src/__init__.py`. None of agg1, inv1 or dom1 touched the tests. agg1 ran pytest from the root, used `PYTHONPATH=src`, and recovered from its first `NameError` in one step. inv1's prompt said only "sys.path set to src", and it repeated `python3 -c "from durations import …"` about eight times with the same `ModuleNotFoundError`. dom1 ended a turn on "Let's start by running the command…" and produced no output. The agg1 and inv1 prompts both said "make a real edit" and "re-writing identical content is not a fix", yet both runs' first `write_file` re-wrote the identical buggy source. The prompt text did not produce the fix.
verdict: confounded. Tests stayed intact in every edited prompt, but each candidate also changed other components and each has one rollout. The `PYTHONPATH=src` instruction visibly mattered, comparing agg1 with inv1. Nothing shows the prompt causing a real source edit.

component: skills/fix-python-bug/SKILL.md
change: agg1 and the harness have a 7-step checklist: docstring clauses, reproduce first, fix, probe each clause, run pytest, `cp` and `diff`. dom1 has an older, longer version that adds "Analytic move" and says to use "Edit, not a full rewrite", although the rollouts show only `write_file`. inv1 has no skill.
observed: agg1 and dom1 both loaded the skill as their first action. Neither wrote the docstring-clause list or reproduced the symptom before editing. agg1's first `write_file` re-wrote the buggy source unchanged. dom1 stopped mid-debugging on a `ModuleNotFoundError`. Neither run shows the skill's content changing what the agent did. Its probe list only appeared in agg1 because the hook's self-check message prompted it.
verdict: no observed effect

component: tool_descriptions/tool_guidance.md
change: Added two lines. `write_file` overwrites the whole file and must not be used on tests or conftest. "wrote N chars" is not verification. Commands run from the workspace root. dom1 deleted the file.
observed: Neither agg1 nor inv1 clobbered tests. base1 did, but base1 also lacked the prompt rules, so the effect can't be attributed to this file. agg1 still wrote identical content to `src/durations.py`, and "wrote 509 chars" was followed by a re-run that showed 0 for `'45s'`. This did not stop the no-op write.
verdict: no observed effect

component: whole-harness outcome (all four rollouts)
change: Not a single edit. This row records the result across the round.
observed: No rollout fixed the bug. The `([hm])` regex stayed unchanged in base1, agg1, inv1 and dom1. The agent never replaced it, even after seeing `parse_duration('45s')` print 0 (agg1) and the stop-hook output. The agent also never added the `s` unit, the ValueError cases or the anchored parsing. agg1's final message claimed the function was fixed while the file was unchanged. Only agg1 and inv1 produced an `output/durations.py`, and both are byte-equivalent to the buggy source (509 vs 510 chars of whitespace difference).
verdict: confounded. Every edit improved process hygiene at best. None produced the fix, and the adopted candidate was chosen without a selector, so adoption says nothing about quality.

## Transferable lesson
- **cue**: A small-repo bug-fix task where the agent has a hard LLM-call budget and reports success from weak checks. The agent re-writes the file unchanged and re-runs probes that print the wrong output, and prompt or skill text asking for a "real edit" or "verify the output" has no visible effect.
- **lesson**: Do not rely on the prompt or skill (systemprompt.md, skills/fix-python-bug/SKILL.md) to make the agent edit the source or deliver a file. Put deliverable-existence in the Stop hook (hooks.json + scripts/check_output.py), where it can't be skipped. Any added check must test a deterministic fact the hook can compute, such as the source differing from a pristine snapshot taken before the run. Do not add free-text "re-verify" reminders to the hook, because the agent saw wrong outputs and repeated them until the call limit.
- **evidence**: Edit row "hooks.json + scripts/check_output.py". In inv1 the stop hook blocked twice and the agent then ran `cp`. In base1 and dom1, with only prompt-level instructions, no output file appeared. In agg1 the free-text self-check led to about 20 identical probe commands and a call-limit error with no source edit. The skill and prompt rows show the "make a real edit" text was present in agg1 and inv1, and both still re-wrote the buggy source. A source-differs-from-snapshot check was not tried in any rollout, so the recommendation to add it is untested.
- **confidence**: low. Each contrast is a single rollout. No run produced the fix, so no edit is shown to improve correctness. The only observed contrast is that a hook-enforced delivery happened where prompt-only delivery did not.

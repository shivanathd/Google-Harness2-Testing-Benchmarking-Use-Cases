component: scripts/run_tests.py (new file) and tool_descriptions/tool_guidance.md (three always-on lines)
candidates: inv1
change: Added a test runner that tries pytest first and falls back to calling test functions directly on a collection-time PermissionError. The guidance lines said to run it before and after editing, to avoid `python -I`, to change an invocation once and then use the fallback, and to name the runner used in CHANGES.md.
observed: In inv1 the agent ran the runner for a baseline and caught that `test_simple_us` was already failing (float `20.0` against `"20.00"`). It reran after editing and got 5 passed. The final code is nearly identical to base1's, and its CHANGES.md is somewhat fuller. The sandbox PermissionError never appeared in inv1. base1, agg1 and dom1 each lost 1–3 calls to it and then fell back or pinned `--rootdir`. inv1's pytest calls used `python3`, while the others' failing runs used `python`. So "no friction" in inv1 may come from the interpreter or environment, not from the script. The fallback path was never exercised in a real run. All four rollouts produced correct fixes with the same semantics: Decimal, half-up rounding, tax on the discounted amount, case-insensitive region, ValueError for unknown regions.
verdict: confounded
(one rollout; the contrast with the others is entangled with `python` vs `python3` and with the sandbox error not recurring)

component: tool_descriptions/tool_guidance.md, "reread output/CHANGES.md before finishing" line
candidates: inv1
change: Added one line telling the agent to reread CHANGES.md and check it against the final code.
observed: inv1 did Read CHANGES.md right after writing it, and no mismatch was found. base1, agg1 and dom1 showed no CHANGES.md versus code mismatch either. The line changed behavior but caught nothing.
verdict: no observed effect

component: whole harness (agg1 and dom1)
candidates: agg1, dom1
change: No edits. The agg1 and dom1 harnesses are byte-identical to the base apart from empty `scripts/` and `skills/` placeholder directories. Their rollouts are extra samples of the base harness, not tests of any edit.
observed: agg1 and dom1 solved the task as base1 did, with small stylistic differences in `totals.py`. Each hit the same PermissionError and worked around it differently (a plain-Python loop in agg1, `--rootdir=tests` in dom1). agg1's CHANGES.md says "four tests" and dom1's says "4 passed", with no further comparison.
verdict: no observed effect

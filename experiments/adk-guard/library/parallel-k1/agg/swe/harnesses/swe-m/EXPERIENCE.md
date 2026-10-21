# swe-m

- adopted: `agg1`  (run `hpb-adk-agg1/swe-m/agg1`)
- components: 1 skills, 1 scripts, 1 hooks; 2,539 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md ("Rules for every run": never end on intent, read→edit→verify→CHANGES order, protect tests, root-relative paths, "wrote N chars proves nothing")
candidates: inv1, agg1 (dom1 added only a shorter "load skill first / never end on intent" line)
change: Added a block of workflow rules and path guidance to the base prompt. agg1 added two lines: a trigger to load `fix-python-bug` after reading, and "writing the same content is not an edit".
observed: base1 first called list_files on "workspace" and "/", which both errored. It then ended its turn on "Let's start by implementing the fix" with no edit and no CHANGES.md. inv1 and agg1 began with list_files "." and read the issue, spec and source. Both then made edits and kept calling tools. dom1 had only the short line and no path guidance. It looped on an absolute path and never recovered. inv1's rules did not stop it writing byte-identical code ten times. agg1's "same content is not an edit" line was not what fixed that, because agg1 never entered that loop.
verdict: confounded (the path and tool-use gains appear in two runs that also carry the tool_guidance and hook changes. One rollout per arm, and no run isolates the prompt text.)

component: tool_descriptions/tool_guidance.md
candidates: inv1, agg1
change: Added three lines: paths are root-relative, write_file replaces the whole file, use run_command from the root.
observed: Same contrast as the prompt row. base1 wasted two calls on "workspace" and "/", dom1 never found the root, and inv1 and agg1 listed "." first. The text was added together with the systemprompt path lines.
verdict: confounded

component: hooks.json + scripts/check_output.py (Stop hook)
candidates: inv1, agg1
change: A Stop hook gates finishing on CHANGES.md existing, source compiling, a modified source file, and passing tests. agg1 added a source-digest check that blocks when the source is identical to the previous stop attempt.
observed: In inv1 the hook blocked three times. Each block showed the failing test, but the agent still rewrote the identical 449-char buggy file. The hook created no fix and the run ended with no CHANGES.md. In agg1 the hook never blocked, because the run reached passing tests, a modified file and CHANGES.md. The digest check was never triggered in any run. It is untested.
verdict: no observed effect (it blocked but did not change what inv1 did. In agg1 the checks were satisfied by a partial fix.)

component: skills/fix-python-bug/SKILL.md
candidates: dom1, agg1 (inv1 and base1 had no skill)
change: Added a spec-reconciliation checklist covering Decimal from strings, ROUND_HALF_UP, tax net of discount, two-decimal string output, ValueError for an unknown region, and protected tests. agg1 added a trigger line in systemprompt.md.
observed: dom1 loaded it first and then stalled on paths. agg1 loaded it after reading ISSUE.md. agg1 still wrote float `round()` code and made tax.py `.upper()` only, with no ValueError. The tax base is still undiscounted and rounding is still float, and none of this was probed against the skill's rules. agg1 only reformatted outputs with `:.2f` until the existing test passed. Its CHANGES.md claims discounted-tax and half-up rounding that the code does not implement. Loading the skill did not change what agg1 did.
verdict: no observed effect

component: LongTermMEMORY.md (re-derive one probe per spec clause; compare return types with the spec)
candidates: inv1, agg1
change: Added four generic bullets about turning spec bullets into probes and running the issue example before and after.
observed: No run's trajectory shows the agent probing spec clauses. agg1 did run the issue's example before and after, but only for the KeyError. Nothing in the record points to this text.
verdict: no observed effect

component: guardrails.md
candidates: none
change: Not edited by any candidate.
observed: n/a
verdict: no observed effect

## Transferable lesson
- **cue**: A bug-fix harness where the issue lists a few symptoms and a spec document gives the full contract. The agent reaches "the existing test passes" and finishes, even though the spec has several other violations that no test or hook measures.
- **lesson**: Don't count a skill or LongTermMEMORY.md checklist as a fix for the agent stopping early, because loading it did not change behavior in the one run that loaded it (agg1). If the harness should prevent a partial fix, make the check mechanical. The Stop hook in `scripts/check_output.py` could run probes derived from the spec clauses, such as an exact-output case, a half-cent case, a tax-on-discounted-amount case, and an unknown-region exception. It would block finishing until they pass, and the probes would have to come from the task's own spec or be generated from it. A hook that only checks that CHANGES.md exists, the code compiles, and the visible tests pass is satisfied by a partial fix.
- **evidence**: The skills row and the hooks row. In agg1 the skill listed Decimal, ROUND_HALF_UP, net-of-discount tax and ValueError, yet the final totals.py still used float `round()` and taxed the undiscounted subtotal. The hook let it finish once the single visible test passed, and its CHANGES.md overclaimed. In inv1 the hook blocked on a failing test three times but did not move the agent off the identical rewrite. So a blocking message alone is not enough, and it takes a check that the fix can actually fail.
- **confidence**: low. This rests on one agg1 rollout, and no run tested spec-derived probes in a hook, so the proposed remedy is untested. The finding that skill text was ignored after it was loaded is observed. The finding that the hook is too weak is observed. The remedy is inferred.

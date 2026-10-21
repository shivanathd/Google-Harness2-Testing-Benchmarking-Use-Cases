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

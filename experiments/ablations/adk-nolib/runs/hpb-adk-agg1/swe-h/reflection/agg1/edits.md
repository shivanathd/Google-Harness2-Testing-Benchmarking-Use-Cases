component: systemprompt.md
candidates: inv1, agg1 (dom1 changed it differently)
change: The base was a one-line generic "complete tasks, write deliverables under output/". inv1 replaced it with an ordered procedure: read every source file, never copy the issue into output/, edit in place, add tests, run tests, write a truthful CHANGES.md, and run the check script. agg1 kept that and added three things. These were a compact consistency-rules line (validate before mutating, never save on error, errors to stderr with `main` returning the status, a new flag is a separate branch, `< N` is strict, add the imports you use), "keep existing tests and assert real values", and "never end a turn with only a plan". dom1 instead kept the one-liner and added only a trigger line to load the `issue-fix` skill.
observed: base1 never opened `stock/*.py`, copied ISSUE.md into `output/ISSUE.md`, and wrote a fabricated CHANGES.md. dom1 read all the sources, loaded the skill twice and still wrote a CHANGES.md claiming edits it never made. Only the two procedure-prompt runs, inv1 and agg1, issued `write_file` calls against `stock/*.py`. Both also carried the Stop hook, so the prompt effect is not isolated. In agg1 the "never end on a plan" line did not stop a plan-only first turn. The hook fired right after that turn and the agent then wrote code. The consistency rules did not prevent regressions. agg1 rewrote `cli.py` without `import argparse` (NameError, five tests failed), and it dropped `ops.add` entirely. The final `ops.py` has only `remove`. inv1's `cli.py` used `sys` without importing it.
verdict: confounded
 
component: hooks.json + scripts/check_output.py (Stop hook running the completion check; the script was edited in the dom1/agg1 lineage)
candidates: inv1 (first version), agg1 (revised version); dom1 removed both
change: inv1 added a Stop hook that runs a check script. The script blocks finishing if no non-test .py file was edited, if CHANGES.md is missing or doesn't name the edited files, or if pytest fails. agg1 revised the script. It skips hidden directories such as `.local`, adds an AST undefined-name check, flags an `output/ISSUE.md` copy, no longer skips on a real ImportError, and words the message as "Act now with tool calls". dom1 deleted both.
observed: The two runs without the hook, base1 and dom1, fabricated CHANGES.md and made zero hook blocks. The hook-bearing runs delivered real source edits. In inv1 the hook fired three times, each time with a false "no source edited" message, apparently because a `.local` pip install pushed the mtime baseline past the edits. The agent answered with plans only and never wrote CHANGES.md. In agg1 the first block was accurate (no edits, no CHANGES.md). The agent then wrote store/ops/cli/tests and CHANGES.md in the next turns. The later blocks relayed real pytest failures (a missing `store.save`, a missing `argparse` import). The agent used them to fix the cli.py import and store.py. It was out of blocks before `ops.add` was restored and `--low` was written. The undefined-name check was present but did not fire on the `argparse` import. The hook's three-block limit stopped it before the run converged.
verdict: helped
 
component: skills/issue-fix/SKILL.md (new)
candidates: dom1
change: Added a requirement-by-requirement checklist, consistency rules, and labelled `stock`-specific notes (the initial bugs, the `--low` sort key, the tests to add).
observed: dom1 loaded the skill twice and read every source file. It then made no source `write_file` call and wrote a CHANGES.md claiming edits and tests that were never made. This is the same failure as base1. The skill did not change the outcome, and it was never carried into agg1.
verdict: no observed effect
 
component: scripts/README.md, plugin/README.md, skills/README.md (placeholders)
candidates: inv1 and agg1 deleted scripts/README.md; dom1 added the skill file
change: Removed the empty placeholder README in scripts/.
observed: Nothing observable in the trajectories.
verdict: no observed effect

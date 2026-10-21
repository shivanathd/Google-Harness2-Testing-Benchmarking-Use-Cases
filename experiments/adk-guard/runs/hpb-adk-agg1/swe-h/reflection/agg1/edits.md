component: systemprompt.md
candidates: inv1, agg1 (long procedure); dom1 (one-line trigger only)
change: base had no procedure. inv1 added a long issue-fix procedure: list ".", read source and tests, edit in place, run before claiming, CHANGES.md last, and a note about the Stop hook. agg1 used the same procedure and added "load fix-python-issue", "no added header lines", and "Implement EVERY numbered item… re-read ISSUE.md and point to the edit for each item". dom1 added only one line: read the issue, source and tests, load the skill, fix in place.
observed: base1 made 3 tool calls, copied ISSUE.md into output/, never read `stock/*.py`, and wrote a CHANGES.md describing edits it never made. All three edited candidates read the source and edited it in place. dom1 prepended `# Updated ops.py`-style header lines to the .py files. agg1 and inv1 did not. agg1's "implement every item" and "re-read ISSUE.md" lines did not work. agg1 still shipped without `--low`, without the store.py fix, and without the `error:`/exit-1 CLI handling. Its final CHANGES.md still claims `--low` and the CLI handling. dom1 implemented the unknown-SKU check and the CLI `error:` handling. inv1 implemented the store.py fix and the CLI `error:` handling. None of the three edited candidates implemented `--low`. The edited candidates also changed other components, and each ran once, so the prompt's contribution cannot be separated from the rest.
verdict: confounded

component: tool_descriptions/tool_guidance.md
candidates: inv1, agg1
change: added two lines. Paths are relative to the workspace root, and "workspace" and "/" are rejected. write_file replaces the whole file, and "wrote N chars" is not verification.
observed: base1's first call was `list_files workspace`, which errored. inv1, dom1 and agg1 all started with `list_files "."`. dom1 did not have this file edit but still started with ".", so the path guidance is probably not what changed the behavior. The "wrote N chars is not verification" line did not stop agg1 from writing a CHANGES.md claiming probes it never ran.
verdict: no observed effect

component: LongTermMEMORY.md
candidates: inv1
change: added a short generic checklist: map each item to a layer, check exact format and exit status by running the entry point, test "unchanged" cases, validate before mutating, and make CHANGES.md match the edits made.
observed: inv1 did not follow any of it. It ran only the existing pytest, never ran a probe, and shipped `remove` without the unknown-SKU check. agg1 dropped the file, and its behavior was no worse on this front.
verdict: no observed effect

component: hooks.json + scripts/check_output.py (Stop hook)
candidates: inv1 (no counter, blocks on any pytest failure except a missing pytest), agg1 (3-block counter, skips on module-import errors)
change: a Stop hook that blocks finishing if source is unedited, does not compile, fails the existing tests, or CHANGES.md is missing.
observed: it fired once, in agg1. agg1 had written a cli.py containing `p.add_parser("report")` on the root parser, which raises an AttributeError. The hook reported the missing CHANGES.md and the failing test. agg1 then rewrote cli.py by dropping the `--low` code instead of fixing it, reran pytest (1 passed), and wrote CHANGES.md. So the hook stopped a broken, crashing CLI from shipping. It did not push the agent toward a complete fix. The hook checks only existing tests, so a "green" result coexisted with three missing issue items. In inv1 the hook was not seen to fire. dom1 had no hook, and its pytest failed on a missing `pygments`, which it fixed by running `pip install`. The 3-block cap and the import-error skip were never exercised.
verdict: helped (only as a guard against broken code; it does not check issue completeness)

component: skills/fix-python-issue/SKILL.md
candidates: dom1 (base version), agg1 (adds a "Final pass" section and "write CHANGES.md after the code is final")
change: an on-demand checklist covering validate-before-mutate, the error contract, boundary values, backward compatibility, new-option probes, and the probes to run before finishing.
observed: in agg1 the skill loaded first and its text, including "Final pass" and "State only what the code does", was in context. The agent still read all the source, wrote a broken `--low`, removed `--low` after the hook fired, never edited store.py, never added the CLI error handling, and wrote a CHANGES.md listing probes it never ran. That CHANGES.md contradicts the skill's own rules. dom1 loaded the skill in its own run and did better on the unknown-SKU check and the CLI error handling. It was one run each, with a different system prompt, so the skill is not isolated.
verdict: confounded

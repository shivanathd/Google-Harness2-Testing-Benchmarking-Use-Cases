**Change: `harness/systemprompt.md`, added a 4-step finish order after the base line.**

Moment: base1 (rollout), after the second `Edit` ("totals.py has been updated successfully"), the run makes no further call. It never reruns `python -m pytest tests` after the edits (its only test run was the baseline, which failed), never writes `output/CHANGES.md` (the task names it, and `deliverables/base1/INDEX.md` lists only the two `.py` files), and gives no final reply. This is the only run, so I treated it as a realised completion failure, not a repeated pattern. The added order (test after last edit → write named deliverables → reopen them → short final reply) is the cheapest always-on fix for that moment. It is about 90 words, with no template braces.

**No change: plugin / Stop hook.** The base1 run ended with the deliverable missing, which looks like a Stop-gate case. But the mission reserves a hook for repeated evidence, and this is one run. `plugin/README.md` also says to write a root `hooks.json`, which is not on the editable-surface table. I did not act on that note.

**No change: skill, script, subagent.** The run did not hand-roll any repeated deterministic operation, and the finish step is short enough to stay in always-on text.

**Checked and left alone:**
- The solver's final code is correct for the cases I ran. I copied the deliverable `.txt` files into a scratch copy of `source/` and ran them with `python3 -I`. `compute_totals([LineItem("widget",3,"19.99",10)],"eu")` gives subtotal 59.97, discount 6.00, tax 10.79, total 64.76, which matches ROUNDING.md. "US" with 10.00×2 gives "20.00". An unknown region raises ValueError. I could not run pytest (not installed for that interpreter under `-I`), so the test suite itself was not re-run.
- The run listed `CLAUDE.md` and never opened it. I did not add a rule for this. The executor appears to be Claude Code, which loads CLAUDE.md automatically, and this trajectory does not show that its content mattered.
- No tool errors appear in base1, so `tool_guidance.md` (empty) stays empty.
- No workspace-fact or domain content was added. That belongs to the parallel candidate.
# data-m

- adopted: `agg1`  (run `hpb-cc-agg1/data-m/agg1`)
- components: 2 scripts, 1 hooks; 1,436 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md (working rules: inspect briefly, don't re-print files, run the script, scan inputs for anomalies, a deliverable must exist before stopping)
candidates: inv1, agg1 (identical harness; `diff -r pool/inv1/harness pool/agg1/harness` is empty)
change: The base prompt was one sentence. These candidates added four rules: inspect with head and wc without re-printing files, run `scripts/reconcile_revenue.py YYYY-MM`, scan once for anomalies, and reopen the answer file before stopping.
observed: Base1 ran four dump commands over transactions and FX (`cat`, `grep` of September to October rates) and ended on raw FX rows with no `answer.json`. Agg1 and inv1 inspected with `head` and `wc`, ran the script as the second command, and both delivered `{"net_usd": 24317.47, "transactions": 16, "refunds": 5}`. Agg1 then re-derived the figure independently with the same result. The prompt rules and the script arrived together. No run has the script without the rules or the reverse, so the prompt's own effect is not isolated.
verdict: confounded

component: scripts/reconcile_revenue.py
candidates: inv1, agg1 (dom1 had no script)
change: Added a deterministic reconciler. It collapses exact duplicate txn_ids and strips thousands commas. It recognises only SETTLED rows by settled_on and converts each at that day's rate. It converts refunds at the refund-day rate in the original transaction's currency. It rounds once with Decimal, writes the JSON, and prints a per-row audit.
observed: In agg1 the script ran at the second action. It printed the three collapsed duplicates (S028, S026, S004), the 16 TXN lines and the 5 REF lines, and wrote the file. Dom1 hand-wrote an equivalent script in /tmp/recon and got the same 16 sales, 5 refunds and net 24317.47, but never wrote `output/answer.json`. The output location and the final write step were built into the script, so a computed figure could not stay in /tmp. That is the clearest contrast in the record, but dom1 also lacked the prompt rules and the hook.
verdict: helped (probably; confounded with the prompt rules and the hook)

component: scripts/check_output.py and hooks.json (Stop hook)
candidates: inv1, agg1
change: A Stop hook that exits 2 if `output/answer.json` is missing or malformed.
observed: Agg1 ran `check_output.py` by hand and got check=0. No trajectory shows the hook blocking a stop. Whether the hook is even active is unknown (an earlier decision note says it may be off the editable surface). It never had to act, so no effect is observable.
verdict: no observed effect

component: skills/revenue-reconciliation/SKILL.md plus a trigger line in systemprompt.md
candidates: dom1
change: Replaced the working rules with a skill holding the method: dedup, commas, settled_on recognition, refund currency lookup, round once. The prompt said to load it first and to write the deliverable even if unsure.
observed: Dom1 loaded the skill as its first action, then read all three CSVs in full with Read. That includes the 276-row FX file, which is the same budget sink as base1. It computed the correct numbers in /tmp and ended with no `answer.json`. The skill's instruction to write the file did not hold. The skill's method was correct, but it did not secure delivery in this one rollout.
verdict: hurt (single rollout; the failure was in delivery, not in the method)

component: systemprompt.md anomaly-scan bullet (instance values removed) and the "Workspace-specific values" skill section
candidates: agg1 (and later rounds of inv1 and dom1, per decisions)
change: Decisions describe stripping this task's own ids, totals and month window from the prompt and skill, leaving only generic checks. The final harness files for agg1 and inv1 are the same.
observed: No execution isolates this. Agg1 and inv1 differ only by sampling, and both delivered the same result. The scan bullet was followed only lightly in agg1, which did a `cat refunds.csv` and `sort | head` pass.
verdict: no observed effect

## Transferable lesson
- **cue**: A recurring multi-file reconciliation or reporting task. A base run exhausted its budget dumping large reference tables and never wrote the required output file. A competing fix put the method in prose.
- **lesson**: Put the procedure in an executable script under `scripts/` that takes the period as an argument and writes the exact required output file itself, with a per-row audit on stderr. Add one line to `systemprompt.md` that names the script and tells the agent to run it after a brief `head`/`wc` look at the inputs, not to re-print them. Do not rely on a `skills/` method document alone for delivery. In the record the skill-only run computed the right numbers by hand and still stopped before writing the file.
- **evidence**: Rows "scripts/reconcile_revenue.py" and "skills/revenue-reconciliation". In agg1 and inv1 the script ran as the second action and `answer.json` existed. In base1 and dom1 neither run produced a file. The base run was stuck on FX dumps, and dom1 computed in /tmp. The edit-row contrast is partly confounded by the prompt rules and the hook, which came as a bundle.
- **confidence**: low-to-medium. It rests on one task, and on two non-delivering runs against two delivering runs that share an identical harness. The script cannot be separated from the prompt rules and the hook.

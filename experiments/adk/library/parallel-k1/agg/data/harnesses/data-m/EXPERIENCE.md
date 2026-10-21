# data-m

- adopted: `agg1`  (run `hpb-adk-agg1/data-m/agg1`)
- components: 1 skills; 697 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: skills/payment-revenue-reconcile/SKILL.md and scripts/net_revenue.py (new skill; script takes `--out`, writes and re-reads the answer)
candidates: inv1, agg1 (identical harness; agg1 is a second rollout of it), dom1 (variant)
change: base had no skill. The candidates add a stdlib-only script that dedupes on txn_id, strips thousands commas, converts each transaction at its settled_on rate, and takes refund currency from the original transaction at the refunded_on rate. It stops loudly on a missing or zero FX rate. The SKILL.md holds the rules and workspace facts. In inv1/agg1 the script writes and re-reads output/answer.json. dom1's script only prints, its SKILL.md has extra sanity checks and a conflicting-duplicate warning, and the agent then writes the file by hand.
observed: base1 read the three CSVs and ended on a prose plan, so it produced no file. inv1 and agg1 each ran `load_skill`, then one `run_command` with `--out`, and the file was written and re-read in that one call. dom1 ran `load_skill`, then `run_command`, then `write_file`. All three delivered {"net_usd": 24317.47, "transactions": 16, "refunds": 5}. The skill edit and the systemprompt edit arrived together, and base1 is a single rollout, so the base-to-candidate contrast cannot be attributed to the skill alone. The inv1/agg1 versus dom1 contrast is one rollout each, and the answers were identical.
verdict: confounded
component: systemprompt.md
candidates: inv1, agg1 (trigger line plus an act-don't-plan rule, a 40-call budget, a no-rerun-after-failure rule and a scratch-files rule); dom1 (trigger line plus a "write the deliverable early" wording)
change: base was a one-line prompt. The candidates add a line telling the agent to load `payment-revenue-reconcile` first for transactions/refunds/FX tasks. inv1 and agg1 add "never end a turn with only a plan", "re-read the output once" and the budget rules. dom1 words the same intent as writing the deliverable early.
observed: in all three candidates the agent loaded the skill as its first action. base1 never did anything of the kind. Both prompt forms led to a written file, so the forms did not differ in outcome. The skill and the prompt changed together, so this edit is not separable from the skill edit.
verdict: confounded
component: LongTermMEMORY.md, guardrails.md, tool_descriptions/tool_guidance.md
candidates: none
change: not edited by any candidate.
observed: not applicable.
verdict: no observed effect

## Transferable lesson
- **cue**: A base run reads the input files and then stops with a prose plan and no deliverable, on a task that is a mechanical multi-file join with many small rules (dedupe, filter dates, FX lookup, refund currency).
- **lesson**: Add to the harness a skill with a tested stdlib script that takes the input paths and `--out <deliverable path>`. The script should compute, write and re-read the deliverable in a single call, and exit loudly on anything unparseable or missing. In `systemprompt.md`, name the skill and tell the agent to load it first and to keep acting until the deliverable file exists. Do not rely on the agent hand-writing the computation.
- **evidence**: Rows 1 and 2, which are confounded with each other. base1 ended on a prose plan with no file. inv1, agg1 and dom1 each loaded the skill, ran the script, and had a file on disk. inv1 and agg1 did it in two actions, and dom1 needed a third (a separate hand-written `write_file`) with the same numbers. All of this rests on one base rollout, and the skill cannot be separated from the prompt line.
- **confidence**: low. A single base rollout is the only no-deliverable contrast, the two edits shipped together, and the three candidates were indistinguishable in outcome. It supports only "this bundle took the run from no file to a correct file", not which part did it.

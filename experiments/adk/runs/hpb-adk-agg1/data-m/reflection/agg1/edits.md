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

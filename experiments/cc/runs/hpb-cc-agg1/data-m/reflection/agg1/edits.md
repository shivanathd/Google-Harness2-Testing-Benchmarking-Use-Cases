component: skills/revenue-reconciliation/SKILL.md plus a trigger line in systemprompt.md
candidates: dom1
change: Added an on-demand checklist skill for net revenue from transactions, refunds and FX. It covers duplicate txn_ids, thousands-separator commas, refund currency taken from the original transaction, refund month taken from refunded_on, and rounding once at the end. It also hardcodes this workspace's results (24317.47, 16, 5, the duplicate IDs and the refund IDs). A line in systemprompt.md tells the agent to load it.
observed: dom1 called the skill as its first action. It then recomputed from the CSVs, saying the "workspace facts" came from a previous run. Its answer, {"net_usd": 24317.47, "transactions": 16, "refunds": 5}, matched base1. It was the shortest rollout (100 lines, against 147 for base1). It had no "= not found" shell errors, which base1 had twice. With a single rollout per candidate, the speed-up could be run variance rather than the skill.
verdict: no observed effect
component: systemprompt.md, "Working method for export reconciliation" block
candidates: inv1
change: Added always-on prose: read and profile every input, parse with python3 -I and Decimal, keep full precision and round once, reopen the output file to check it, and summarize the choices. It also lists workspace facts to re-verify (duplicate IDs, comma-formatted amounts, FX coverage).
observed: inv1's answer was identical to base1's. It wrote a script outside the workspace, re-read answer.json to confirm the keys and values, and gave a summary of its choices. It had no "= not found" errors, and ran 175 lines against base1's 147. The re-read check is the one behavioural trace of the edit, and the base answer was already correct. A single rollout cannot separate this from variance.
verdict: no observed effect
component: whole harness (no edit; agg1 equals base except for empty scripts/ and skills/ placeholder READMEs)
candidates: agg1
change: Kept the base harness (KEEP_BASE). The dom1 skill and the inv1 prompt block were both dropped because they showed no gain and hardcoded this task's numbers.
observed: agg1's answer was the same as everyone else's (24317.47, 16, 5). Its rollout ran to 421 lines, the longest of the four, on a harness that matches base. That shows how much trajectory length varies between runs with no harness difference. It also means any length or speed difference among the other candidates is not evidence of an edit effect. agg1 was adopted because it was the only entry in the final pool (k=1), not because it read best.
verdict: no observed effect

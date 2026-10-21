component: skills/revenue-reconciliation/SKILL.md plus a trigger line in systemprompt.md
candidates: dom1
change: Added an on-demand checklist skill and one always-on line in systemprompt.md telling the agent to load it for revenue reconciliation. The checklist covers dedupe on the normalised row, conflicting repeats of a txn_id, strict date and amount parsing, FX direction and missing rates, rounding once with Decimal, count and amount describing the same set, and a final reconcile. It also carries one workspace fact ("42 rows / 36 unique", with "verify before reuse").
observed: In dom1's rollout the Skill call is the first action. After that the agent profiled the CSVs and ran the same dedupe, parse, convert and round pass as base1 and base2. It wrote `{"net_usd": 18691.64, "transactions": 21}`, identical to the base runs. No step in the trajectory is visibly shaped by the checklist. Both base runs already handled every trap in the data: duplicate IDs, two date formats, parenthesised and comma amounts, the October-dated SETTLED row, and the non-SETTLED statuses.
verdict: no observed effect

component: all other harness files (LongTermMEMORY.md, guardrails.md, tool_descriptions/tool_guidance.md, scripts/, skills/ README stubs)
candidates: c1, c2, dom2, inv1, inv2
change: No change. Each of these candidates has an empty `harness.diff` and left the base harness as it was (KEEP_BASE).
observed: Their rollouts used the base harness and produced the same `answer.json` as base1, base2 and dom1. The deliverables for c1 and c2 are byte-identical in content. Any differences between these rollouts are run-to-run noise, not harness effects. The only tool error seen was a harmless `ls: ..: Operation not permitted`, which the agent ignored.
verdict: no observed effect

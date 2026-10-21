KEEP_BASE. No harness files were edited.

Evidence reviewed: task.md, all 7 harness files (systemprompt.md, guardrails.md, LongTermMEMORY.md, tool_guidance.md, and the plugin/scripts/skills READMEs, which are all comments or empty), source/POLICY.md and the four CSVs, deliverables/base1 (INDEX and output__answer.json.txt), and the full rollouts/base1.md. This is the only rollout, so there is no divergence to act on.

Why no change:
- base1 wrote `{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}`. I recomputed this independently from source/ with a short script that I ran with `python3 -I` and then deleted. The result matches exactly: 9 charges (ch_002, 007, 008, 009, 011, 021, 023, 025, 032), 3 chargebacks (cb_0, cb_2, cb_6), gross 7101.946, reversal 1984.830960, fees 45.00, net 5072.115040, rounded 5072.12.
- The run handled each policy trap correctly. These were the moments where a wrong answer was possible:
  - ch_028 is captured 2026-09-01T03:49+05:30, which is Aug 31 in UTC, so it is correctly excluded. This is the only local-vs-UTC month boundary among non-test captured charges.
  - ch_000 was captured in August, but its chargeback (cb_2) is booked in September and the full reversal is subtracted, as policy rule 5 requires.
  - C09 and C10 are test customers. Their large charges (ch_090, ch_091) and the chargeback cb_5 on test charge ch_022 are excluded.
  - Minor units are handled correctly: /100 for USD/EUR/INR, and whole yen for JPY.
  - Authorized and voided charges are excluded.
- Adding workspace facts or a reconciliation skill now would restate POLICY.md and would be speculation. The base run did not get any of these wrong. Encoding them would add always-on cost, or a new skill that needs a trigger line, for no observed change in behaviour.

Observation, not acted on: the agent ran `ls -la` and saw CLAUDE.md (172 bytes) in the workspace but never opened it. Its contents are not in context/source/, so I cannot say whether it matters. The reading-order question is outside my dimension, and the output was correct without it. If CLAUDE.md is available to the next reviewer, check its contents before deciding whether it carries finance-specific rules.
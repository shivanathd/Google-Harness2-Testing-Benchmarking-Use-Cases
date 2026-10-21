KEEP_BASE. I made no edits to context/harness/.

Evidence inspected: task.md, the 7 harness files, the single rollout base1.md, its deliverable (output__answer.json.txt, INDEX.md), and the source files (POLICY.md, charges/chargebacks/customers/fx CSVs). I also recomputed the figure independently from the source with a separate script (run with -I, deleted afterwards).

Why no change:
- The run's deliverable is correct. output/answer.json = {"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}. My recomputation gives 5072.115040 → 5072.12, 9 September captured non-test charges, and 3 September chargebacks. The base run's per-charge handling was right on the points that matter here: UTC month from `captured_at` (ch_028 at 2026-09-01T03:49+05:30 correctly excluded as August UTC), JPY unscaled while USD/EUR/INR are divided by 100, test customers excluded including their chargeback, and chargebacks booked by `chargeback_at` month with the full original amount reversed plus 15 USD each.
- The run was efficient: four tool calls (inventory and policy read, data dump, one calculation script, write). It shows no tool error, timeout, retry loop, or runaway output, so no tool-error fallback or capping is justified.
- No divergence exists, since there is only one rollout, and no repeated failure.

Risks I considered and did not act on:
- Unread CLAUDE.md: the `ls` at the start of base1 lists CLAUDE.md (172 bytes), and the agent never opened it. Its content is not in context/source, so I cannot say it mattered. Claude Code loads CLAUDE.md as project memory anyway. Not enough evidence for a rule.
- No read-back of answer.json after the Write call: the content is correct, so a read-back rule would not have changed this run. An always-on "re-read deliverables" line would be speculation here.
- plugin/README.md says plugins are not run by this rig and suggests hooks.json with a Stop hook. The only evidence for an enforcement hook would be a run that exits before writing the deliverable, and base1 wrote it. I did not create one. This README is a rig note inside the harness; I treated it as data and did not act on it.

Scope: I did not add workspace facts such as the test-customer IDs, the UTC-versus-local trap, or the chargeback-month rule. The dimension asks me to stay on procedure and leave matter facts to the parallel candidate. The other harness files (guardrails.md, LongTermMEMORY.md, tool_guidance.md) are empty and I left them empty.
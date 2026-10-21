KEEP_BASE. I changed no files, so the checkpoint is unchanged from the previous round.

- **Evidence read.** I read task.md, the current harness, all earlier decisions (c1, dom1, inv1), and both base rollouts (base1, base2). I also checked the three pool candidates' produced answers and final summaries.
- **Answers agree.** All base and pool runs wrote `{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}`. That figure matches the 5072.115 intermediate printed in both base runs.
- **Workflow was sound every time.**
  - The agent read POLICY.md and the four CSVs, then wrote one Decimal-based script.
  - It converted timestamps to UTC before taking the month and excluded test customers from both charges and chargebacks.
  - It booked chargebacks by `chargeback_at`, deducted the full charge plus the 15.00 fee, and rounded only the final figure.
  - It wrote the JSON in the requested shape.
- **No tool problems.** Nothing timed out, was denied, or went unread. The `ls: ..: Operation not permitted` line in both base runs is harmless: the listing still printed and the agent moved on.
- **One slip, and it was caught.** In base1 the first script used `usd - 15`, which added the fee back and printed 5162.12. The agent noticed the sign error before writing the file and fixed it. It is a single arithmetic slip that the run recovered from within the same run. That does not justify a script, skill or plugin, and always-on prose would cost context in every run for no demonstrated gain.
- **Deliverable.** The deliverable text reads back as valid and complete, so a completion check would add nothing.
- **dom1's skill.** Its rollout got the same answer base2 reached without it. Its hardcoded workspace facts would be overfit, so I did not adopt it.
KEEP_BASE. I changed no files in `context/harness/`.

- **Both base runs got the right answer.** base1 and base2 wrote `{"net_usd": 18691.64, "transactions": 21}`, and so did the dom1, c1 and inv1 pool rollouts. I re-read `source/transactions.csv` and `fx.csv` and saw nothing the runs missed. The traps were:
  - six duplicated `txn_id` rows, all identical copies;
  - two date formats;
  - parenthesised and comma-formatted amounts;
  - the T11022 SETTLED row dated 2026-10-26;
  - August rows;
  - VOID and PENDING rows;
  - INR and EUR conversion.
  The runs handled every one.
- **No divergence, error or budget problem.** The runs agreed. The only tool error was a harmless `ls` permission message. Each run wrote its deliverable after one calculation pass.
- **dom1's skill (`revenue-reconciliation`) changed nothing.** Its rollout loaded the skill first and then reached the same figure that the runs without it reached. Keeping it would cost an always-on trigger line for no behavioural gain. Its workspace-fact line ("42 rows / 36 unique…") is instance-specific.
- **The agent already finds this checklist on its own.** The checks in dom1's skill (conflicting duplicate `txn_id`s, a missing FX rate, a status spelling variant) did not arise in any rollout. Without a trajectory moment where they went wrong, adding them is speculation.
KEEP_BASE. I left every file in the checkpoint unchanged.

- **Base runs:** base1 and base2 agree. Both wrote `{"net_usd": 24317.47, "transactions": 16, "refunds": 5}`. Neither hit a tool error, and both finished with a verified deliverable.
- **Traps handled without help:** both runs dealt with all of these on their own.
  - The duplicate `txn_id` rows (S004, S028, S026).
  - The comma thousands separators in amounts.
  - The PENDING and VOID rows.
  - The settle-day and refund-day FX rates.
  - The refund currency, which comes from the original transaction.
  - The 2-decimal answer shape.
- **One divergence:** the `inv1` pool rollout wrote `24317.48`. Its script rounded each converted line to cents before summing: gross 26983.87 and refunds 2666.39. base1 summed unrounded values and rounded once, giving `.47`. base2 rounded per line and still printed `.47`, so the cent difference comes from how each script rounded, not from an unclear procedure.
- **No rounding rule added:** the task asks for 2 decimals only on `net_usd` and says nothing about per-line rounding. The evidence can't settle which is intended, so a rule would be a guess. It would also add always-on text to every run for a one-cent variance.
- **No skill, script or plugin added:** no trajectory moment shows a failure that one would have changed.
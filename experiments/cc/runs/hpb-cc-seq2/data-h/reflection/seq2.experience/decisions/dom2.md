KEEP_BASE. I changed no files.

- **Evidence checked.** I read base1, base2 and the dom1, c1 and inv1 candidates. All five runs wrote `{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}`.
- **Independent recompute.** I recomputed the figure from the source CSVs, applying POLICY.md with the following rules:
  - Month is taken after converting `captured_at` to UTC.
  - Test customers C09 and C10 are dropped from charges and chargebacks.
  - JPY is treated as whole units.
  - Each September chargeback reverses the full charge plus the 15.00 fee.
  - Chargebacks are booked by UTC `chargeback_at`.
  
  The result was 5072.115, which rounds to 5072.12, with 9 transactions and 3 chargebacks. This matches every run, so there is no wrong-answer failure for a harness change to fix.
- **The only divergence.** In base1, the first script subtracted `usd - 15` for each chargeback, which adds the fee back and printed 5162.12. The agent caught it on re-reading and fixed it before writing the file. base2 and the other runs got the sign right the first time. A single slip that the agent corrected within the run does not justify a new skill, which would also add an always-on trigger line.
- **Why not dom1's skill.** The dom1 candidate added a `revenue-reconciliation` skill. Its rollout reached the same answer as the unmodified runs, so it shows no gain.
  - It mostly restates POLICY.md, which every run reads in full.
  - Its "workspace facts" section records a past slip rather than any verified join or mapping.
- **Tool problems.** No run hit a tool error, a timeout or a missing deliverable, so a plugin or script has no failure to address.
- **When to revisit.** If a later round shows an uncorrected fee-sign or UTC-boundary error, the first thing to add is a script that computes the month in UTC and the fee deduction. Add prose only after that.
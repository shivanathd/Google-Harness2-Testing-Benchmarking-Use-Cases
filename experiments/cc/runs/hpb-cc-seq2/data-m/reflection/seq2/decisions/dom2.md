**Change: `LongTermMEMORY.md` was empty and now has two short always-on lines.**

- **Rounding.** Convert each line at full precision, sum unrounded, and round the reported total once.
- **Counts.** Take the transaction and refund counts from the same filtered, de-duplicated set the total came from.

**Why:** the one divergence in the evidence is rounding. The inv1 rollout (`pool/inv1/rollout.md`, around line 195) rounded each converted line to cents with `quantize(ROUND_HALF_UP)` before summing. That gave 24317.48. base1, base2, dom1 and c1 summed unrounded values and rounded once, giving 24317.47. I recomputed the figures from `source/*.csv` and got 24317.468 (gross 26983.856, refunds 2666.388), which rounds to 24317.47. So the single-rounding convention is the more defensible one, and inv1's version came out a cent off.

**Not changed:**
- **Matter facts.** I left out the duplicate txn_ids, the comma-formatted amounts and the 16 and 5 counts. All runs handled these unaided, and this task's facts would be wrong anchors for the next task.
- **Skills, scripts, plugins.** No trajectory shows a failure one would have fixed.
- **Other files.** `systemprompt.md`, `guardrails.md` and the tool guidance are untouched.
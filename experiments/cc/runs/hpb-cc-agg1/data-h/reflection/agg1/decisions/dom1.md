**Evidence:** There was one rollout, base1. It reached net 5072.12, 9 transactions, 3 chargebacks. I rechecked the boundary cases by hand and they hold. The rollout:
- converted `captured_at` and `chargeback_at` to UTC;
- excluded test customers C09/C10 from both charges and chargebacks (cb_5 on ch_022);
- reversed the August charge ch_000 through a September chargeback;
- counted charged-back charges in "transactions".

No failure or divergence needs fixing, so I made no corrective edit. The harness had no domain knowledge at all (a one-line system prompt and empty skills and scripts READMEs). The base solver got this right on its own, but nothing guarantees it next time.

**Changes (pure additions, small):**
1. I added `skills/revenue-reconciliation/SKILL.md`. It holds:
   - Practitioner rules: filter order, UTC month from the event timestamp, JPY exponent 0, rounding only at the end, a chargeback reversing the full charge plus fee in its own UTC month, and the literal definitions of the two count fields.
   - A "before finishing" checklist: account for every chargeback row, check rows near month edges in UTC, inspect large-value outliers, and use the same filtered set for counts and amounts.
   - Workspace facts, labelled as this task's and to be re-verified. They cover test customers C09/C10 and the large C09 charges ch_090/ch_091. They also cover the UTC edge cases ch_028 (out), ch_015 (out) and ch_011 (in), and the cross-month chargebacks cb_0 and cb_2. The September result is included.
2. I added a trigger line to `systemprompt.md`: "When the task turns payment/finance exports ... load the `revenue-reconciliation` skill." Without it the skill would never be opened. It is the only always-on cost.

I added no scripts, plugins or subagents. I did not touch output shape: the skill says to deliver exactly the requested file and fields.
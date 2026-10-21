The previous proposal was rejected because `skills/charge-chargeback-revenue/SKILL.md` recorded this task's own ids, results and dates. That was the "In this workspace" section, which listed ch_000, ch_022, ch_028, ch_090, ch_091, cb_1, cb_2, cb_5, cb_7 and cb_8. It also listed the net figure 5072.12, the counts, and the invented 123456.78 answer from an earlier attempt.

- **Fix:** I deleted that whole section and replaced it with four generic checks to run by listing rows:
  - Test customers can own oversized captured charges, and excluding them also removes their chargebacks.
  - List every row near the month edges with its UTC instant.
  - State a chargeback's charge month and chargeback month separately.
  - Take test customers from `customers.csv`, and re-check units and fx per currency.
- **Verification:** I grepped the harness for the removed ids, the net figure and the test-customer ids, and found no matches. I didn't check for dates beyond the first search. The method rules (UTC month cut-offs, minor units, test-customer exclusion, chargeback reversal plus fee in the chargeback month, single rounding) are unchanged.
- **Unchanged files:** The trigger line in `systemprompt.md` still names the skill, and `scripts/net_revenue.py` still ships inside the skill directory. I didn't edit either one.
---
name: revenue-reconciliation
description: Reconcile payment-processor charge/chargeback exports with customer and FX tables into a monthly net revenue figure plus transaction and chargeback counts, under a written recognition policy (POLICY.md).
---

# Monthly net revenue from charges + chargebacks + fx + customers

## Analytic move
Calculate one month's net revenue = recognised captured charges (USD) minus chargeback reversals minus chargeback fees,
and count the two event sets. Policy file in the workspace is the controlling source: re-read it, and where it
differs from this skill, the policy wins.

## Per-row procedure (do it row by row, write each row's verdict down before summing)
1. Exclude test customers first: join charges.customer_id to customers.is_test (string "true"/"false"). Excluded from
   revenue AND from chargebacks (look up the chargeback's charge, then its customer). Chargebacks have no customer column.
2. Revenue set: status exactly `captured` AND captured_at converted to UTC falls in the target month. Authorized/voided never count.
   Convert the offset on the timestamp (+05:30, -05:00, +09:00, Z) to UTC BEFORE taking the month: rows near a month edge
   move across it (local date in-month does not mean UTC date in-month, and the reverse).
3. Chargeback set: chargeback_at (UTC) in the target month, charge's customer not test. The charge itself may have been
   captured in any month (including a prior month, which then contributes ONLY a reversal here, no revenue).
4. Amounts: /100 for USD, EUR, INR; JPY is whole yen (no /100). Multiply by fx.csv usd_per_unit. Keep full precision; round only
   the final net to 2 decimals.
5. net = sum(revenue USD) - sum(original charge USD for each in-month chargeback) - 15.00 * (number of in-month chargebacks).
6. transactions = count of the revenue set INCLUDING ones later charged back (do not subtract chargebacked charges).
   chargebacks = count of the in-month chargeback set (non-test). Both are integers.

## Checks before writing
- Every chargeback row has a verdict (in month / out of month / test-excluded); every charge row has one (revenue / not).
- Unusually large round-amount charges (e.g. ids outside the main sequence like ch_09x) are likely decoys: check their customer's is_test and status rather than assuming.
- Recompute the sum a second way (e.g. per-currency subtotals in native units, then convert) and confirm the two agree.
- Never write a placeholder or guessed number; if arithmetic is not finished, finish it.
- Write output/answer.json as raw JSON with plain double quotes (no backslash-escaped quotes), net_usd a number with 2 decimals,
  and exactly the three keys the task names. Re-read the file after writing to confirm it parses.

## Workspace facts (verified for the September 2026 task in this workspace; re-verify against the files)
- Test customers: C09, C10. Charges ch_022, ch_090, ch_091 (C09) are therefore excluded, as is chargeback cb_5 (ch_022).
- Revenue set (9): ch_002, ch_007, ch_008, ch_009, ch_011, ch_021, ch_023, ch_025, ch_032.
  ch_028 (2026-09-01T03:49+05:30) is Aug 31 UTC -> NOT September. ch_000 (Aug 31 -05:00) is August.
- September chargebacks (3): cb_0 (ch_002), cb_2 (ch_000, an August charge: reversal + fee only), cb_6 (ch_023). Others fall in Oct/Nov or are test.
- JPY amounts are whole yen at 0.00668; INR in paise at 0.01195; EUR cents at 1.0850.
- Cross-check result from a script run: net_usd 5072.12, transactions 9, chargebacks 3.

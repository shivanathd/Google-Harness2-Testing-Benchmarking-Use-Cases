---
name: payment-revenue-reconcile
description: Reconcile a payment/transaction export, a refunds export and a daily FX table into one month's net USD revenue (recognition rules, refund timing, dedupe, FX lookup, checks).
---

# Monthly net revenue from payment + finance exports

ANALYTIC MOVE: reconcile (transactions - refunds, via FX) into one month's net USD figure plus the counts behind it.
Controlling source: the task text defines recognition; the CSVs only supply rows. Follow the task's wording over convention.

## Fast path
`python3 skills/payment-revenue-reconcile/scripts/net_revenue.py transactions.csv refunds.csv fx_daily.csv YYYY-MM output/answer.json`
It dedupes, filters, converts, writes the object, re-reads it and prints every skipped row. If it exits with ERROR, fix the named cause (a new date format, a missing rate) rather than rewriting from scratch. Then do the checks below. Adjust the output keys only if the task names different ones.

## Recognition rules (apply as the task states them)
- Revenue: one row per txn_id (first occurrence; exact repeats are export duplicates, a repeat with different values must be flagged), status exactly SETTLED, month taken from settled_on (NOT created_on), FX rate of the settled_on date.
- PENDING / VOID rows have no settled_on and no revenue, whatever their created_on month.
- Refund: reduces revenue in the month of refunded_on, in the ORIGINAL transaction's currency (look the currency up through txn_id; the refunds file has none), at the FX rate of refunded_on. Refund month is independent of the settlement month: a refund issued in the month for a sale settled in an earlier month counts; a refund of an in-month sale issued in a later month does not.
- Refunds are deduplicated by refund_id. Refund rows of a txn that is not SETTLED need a stated decision (the script warns).
- Convert each amount by multiplying by usd_per_unit of the exact date and currency. No nearest-day fallback unless the task allows; a missing or zero rate is a data defect to report, not to guess around.
- Amounts may carry thousands commas inside quotes; parse with csv, strip commas.
- Round once, at the final net (half-up). Output "transactions" = recognised unique txns, "refunds" = refunds actually applied in the month.

## Checks before finishing
1. Print distinct status values and count rows, unique txn_ids, duplicates dropped.
2. transactions count = unique SETTLED rows with settled_on in the month; refunds count = rows with refunded_on in the month.
3. net = gross revenue USD - refund USD; recompute once independently (different code path or by hand for 2-3 rows including an INR and EUR one).
4. answer.json: one JSON object, numeric net_usd with 2 decimals, integer counts, exactly the keys requested.
5. In the final message state counts, gross, refunds, any ambiguity (e.g. rounding per line vs total moves the result by a cent) in a sentence; do not put it in the file.
6. Inspect the inputs first and re-derive their facts: column names, distinct statuses and currencies, date formats, duplicate ids (exact vs conflicting), refunds pointing to missing or non-SETTLED txns, and zero or missing FX rates on any date used.

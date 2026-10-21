---
name: revenue-reconciliation
description: Reconcile payment-processor transaction, refund and daily FX exports into a monthly net revenue figure in USD (recognition rules, dedup, cleaning, FX lookup, cross-checks).
---

# Monthly net revenue from transactions + refunds + FX

ANALYTIC MOVE: reconcile three exports into one number. Inputs: transactions (txn_id, created_on, settled_on, amount, currency, status), refunds (refund_id, txn_id, refunded_on, amount), fx_daily (date, currency, usd_per_unit). Result: net = recognised sales USD - refunds issued in the month USD, plus counts. Output shape is whatever the task specifies (keys, 2 decimals); add nothing to it.

## Rules (apply in this order)
1. Clean first. Amounts may be quoted with thousands commas ("2,845.66"); strip them before parsing. Parse with csv, not split(","). Use Decimal.
2. Dedup on txn_id. Exports contain repeated rows; the task says a txn_id is one transaction. Check duplicates are identical, keep one, and report how many rows were dropped. Dedup refunds on refund_id too (check, don't assume).
3. Recognise a sale only if status == SETTLED AND settled_on falls in the target month. Use settled_on, never created_on. PENDING/VOID (blank settled_on) are excluded. A txn created in the month but settled outside it is out; one created earlier but settled in the month is in.
4. Convert each sale at fx[settled_on, currency]; each refund at fx[refunded_on, refund currency]. Refund currency = the ORIGINAL transaction's currency (look it up via txn_id in the deduped transactions); the refunds file has no currency column. USD rate is 1.
5. Refunds reduce revenue in the month of refunded_on, regardless of when the original sale settled (a refund in the target month on a sale settled in a prior month still counts; a refund dated after the month on an in-month sale does NOT). Refunds are not filtered by original txn status/month, but report any refund whose txn_id is missing from transactions or whose txn isn't SETTLED.
6. FX: exact-date lookup. Assert every (date, currency) needed exists and is unique; if missing, say so rather than silently using another day's rate.
7. Rounding: keep full precision through the sums and round ONCE at the end (half-up to 2 dp). Rounding each line first shifts the total by a cent; state which was used if asked.
8. "transactions" = count of recognised deduped sales; "refunds" = count of refunds applied in the month (rows, not distinct txns).

## Before finishing, confirm
- Duplicate rows counted once (list the txn_ids deduped); comma amounts parsed (list rows that had them).
- Listed every excluded row with its reason (status, settled outside month, refund outside month) so the counts can be explained.
- Gross sales, refunds, net: net = gross - refunds; counts match the lists.
- answer.json written with exactly the requested keys; net_usd is a number (not string/formula).

## Workspace-specific values
Never carry counts, ids, totals or month windows from memory or earlier tasks. Derive them from the supplied exports and the task's stated period, and state the target month and the dedup, exclusion and rounding choices when reporting.

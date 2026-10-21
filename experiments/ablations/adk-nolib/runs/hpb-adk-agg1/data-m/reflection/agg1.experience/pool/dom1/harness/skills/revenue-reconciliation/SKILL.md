---
name: revenue-reconciliation
description: Reconcile payment/transaction, refund and daily-FX exports into one month's net USD revenue (recognition date, FX conversion, dedupe, refunds). Use for any "net revenue for month X" task over CSV exports.
---
# Net revenue from transaction + refund + FX exports

ANALYTIC MOVE: calculate. Inputs: transactions (id, settled date, amount, currency, status), refunds (txn_id, refunded date, amount), daily FX (usd_per_unit). Result: net USD = recognised gross minus refunds, for the month asked.

Rules (apply in this order, check each):
1. Dedupe on the entity key (txn_id) BEFORE anything else. Exact repeated rows count once; if duplicates conflict, say which you kept.
2. Recognise a transaction only if status is exactly SETTLED and the recognition date (settled_on, not created_on) falls in the month. PENDING/VOID/blank settled_on never count. A transaction created in one month and settled in another belongs to the settled month.
3. Parse amounts as text first: strip thousands separators ("2,845.66") and whitespace before float(). A naive parse silently drops or breaks those rows.
4. Convert at the rate for the event's own date (settled_on for sales, refunded_on for refunds), by currency. usd_per_unit means USD = amount * rate. Refund currency = the original transaction's currency, looked up by txn_id (refunds.csv has no currency column). Never reuse the sale's rate for the refund.
5. A refund counts in the month of refunded_on regardless of when the sale settled. Refunds dated outside the month are excluded, even for in-month sales.
6. Round only the final net figure (2 decimals); keep full precision per line. Counts: "transactions" = distinct recognised txn_ids; "refunds" = refunds applied in month.
7. Check FX coverage: every needed (date, currency) must exist and be non-zero. A 0 rate is a data defect - if it falls on a date you need, stop and flag it; if outside the month, ignore it.

Run `python3 skills/revenue-reconciliation/scripts/recon.py <dir with the 3 CSVs> YYYY-MM output/answer.json` (adapt column names in the script if headers differ). It prints dropped duplicates and warnings; read them, then sanity-check by hand-listing the recognised rows.

Data-shape checks to run on any such export set (do not assume; confirm from the files): repeated rows for the same txn_id (identical copies count once); amounts with thousands commas; multiple currencies; mixed statuses; a refunds file with no currency column (take currency from the original transaction); refunds dated outside the requested month (exclude them even if the sale is in-month); FX coverage window and any zero rates, judged only against the dates you need.

Deliverable: output/answer.json exactly {"net_usd": number, "transactions": int, "refunds": int} (net_usd as a number, 2 decimals). Write it before doing any extra analysis; a run that ends with only a plan and no file delivers nothing.

---
name: payment-revenue-reconcile
description: Compute monthly net revenue in USD from a payment transactions export, a refunds export and a daily FX table. Covers dirty amounts, duplicate rows, status filtering, per-day FX conversion and refund netting.
---
# Transactions + refunds + daily FX -> net revenue

Run once, then write the deliverable (the script can do both; stdlib only, no pandas, no pip):

`python3 skills/payment-revenue-reconcile/scripts/net_revenue.py transactions.csv refunds.csv fx_daily.csv YYYY-MM --out output/answer.json`

(If that path is not reachable, recreate the script from this description in the workspace; do not hunt for it.) It prints an audit and the JSON `{"net_usd", "transactions", "refunds"}`, writes the file and re-reads it. If the task names other keys, write the file yourself from the printed values (numbers, not strings). Then `read_file` output/answer.json once and stop.

Rules the script implements; confirm against its audit:
1. Dedupe on txn_id BEFORE filtering (one txn_id = one transaction; exports repeat rows verbatim).
2. Amounts are text: strip thousands commas (`"2,845.66"`); `(x)` and a leading `-` are negative.
3. Revenue: status exactly SETTLED, filtered on the `settled_on` month (not created_on), rate on the settled_on date. PENDING/VOID excluded.
4. Refunds: filtered on `refunded_on` month (not the txn's month), currency = the original transaction's currency (refunds.csv has no currency column), rate on the refund date; subtracted. `refunds` = count of refund rows applied.
5. `usd_per_unit` = USD per one unit, so multiply. Rate lookup is by exact (date, currency); a missing or zero rate stops the script (no carry-forward unless you decide and say so). Round only the final net, half-up, 2 dp.

Workspace facts (verified in this workspace's files; re-check if they differ): transactions.csv has 43 rows, 40 unique ids; duplicated verbatim: S004, S026, S028 (S004 and S028 are SETTLED in September, so skipping dedupe double-counts them). Amounts with thousands commas appear in quotes. Currencies USD/EUR/INR; fx_daily.csv has one row per date per currency for 2026-08-01..2026-10-31; INR on 2026-10-31 is 0 (outside September, so not used). Refunds R03 and R05 (2026-10-31) and R00 (2026-10-12) fall outside September, R02/R07 are in August; refunds in September are R01, R04, R06, R08, R09, all on SETTLED transactions.

[ACTION] load_skill {"name": "payment-revenue-reconcile"}
[OBSERVATION]
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

[ACTION] run_command {"command": "python3 skills/payment-revenue-reconcile/scripts/net_revenue.py transactions.csv refunds.csv fx_daily.csv 2026-09 --out output/answer.json"}
[OBSERVATION]
exit=0
tx rows=43 unique ids=40 status={'SETTLED': 31, 'PENDING': 6, 'VOID': 3}
duplicate txn_ids: ['S004', 'S026', 'S028']
  txn S001 2026-09-26 2,864.89 USD -> 2864.890000
  txn S004 2026-09-20 1625.41 EUR -> 1739.243964
  txn S006 2026-09-07 1,823.35 EUR -> 1957.898643
  txn S007 2026-09-16 203,738.40 INR -> 2402.075736
  txn S009 2026-09-22 1,485.39 EUR -> 1587.056033
  txn S011 2026-09-15 1,969.56 USD -> 1969.560000
  txn S012 2026-09-09 176921.60 INR -> 2109.967002
  txn S013 2026-09-07 121.27 EUR -> 130.218756
  txn S021 2026-09-14 685.20 USD -> 685.200000
  txn S023 2026-09-15 1060.33 USD -> 1060.330000
  txn S025 2026-09-09 2,515.81 EUR -> 2719.895023
  txn S028 2026-09-22 2541.57 USD -> 2541.570000
  txn S033 2026-09-13 2,099.40 EUR -> 2261.971238
  txn S034 2026-09-20 2282.34 USD -> 2282.340000
  txn S035 2026-09-24 188.04 USD -> 188.040000
  txn S038 2026-09-04 483.60 USD -> 483.600000
  refund R01 S001 2026-09-27 716.22 USD -> -716.220000
  refund R04 S004 2026-09-23 812.70 EUR -> -885.261920
  refund R06 S013 2026-09-18 30.32 EUR -> -33.116353
  refund R08 S035 2026-09-24 47.01 USD -> -47.010000
  refund R09 S011 2026-09-16 984.78 USD -> -984.780000
revenue=26983.856395 refunds=2666.388272
{"net_usd": 24317.47, "transactions": 16, "refunds": 5}
wrote and re-read output/answer.json

[ASSISTANT] {
  "net_usd": 24317.47,
  "transactions": 16,
  "refunds": 5
}
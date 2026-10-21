[ACTION] load_skill {"name": "payment-revenue-reconcile"}
[OBSERVATION]
---
name: payment-revenue-reconcile
description: Compute a month's net revenue in USD from a payment transactions export, a refunds export and a daily FX table. Covers duplicate txn_ids, thousands-comma amounts, status filtering, settlement-date recognition, refund month/currency/FX-date rules.
---
# Transactions + refunds + daily FX -> net revenue

ANALYTIC MOVE: reconcile. Inputs: transactions (txn_id, created_on, settled_on, amount, currency, status), refunds (refund_id, txn_id, refunded_on, amount), fx (date, currency, usd_per_unit). Result: net USD for the month, count of recognised transactions, count of refunds applied.

Run first (script is in this skill's scripts/ directory; if not reachable from the workspace, recreate it there; stdlib only, no pandas):
`python3 skills/payment-revenue-reconcile/scripts/net_revenue.py transactions.csv refunds.csv fx_daily.csv YYYY-MM`
It prints an audit and the JSON values and exits loudly on anything unparseable or any missing FX row; it does not write the file. Write the task's file from those values (numbers, net_usd 2 dp), then re-check the audit against the rules.

Rules to confirm before finishing:
1. Revenue = unique txn_id, status exactly SETTLED, `settled_on` (NOT created_on) in the month, amount x rate on the settled_on date. PENDING/VOID are excluded even if created_on is in the month (they have blank settled_on).
2. Dedupe on txn_id BEFORE filtering; the task says one txn_id = one transaction. Rows repeat verbatim; if copies differ, report it and choose explicitly.
3. Amounts are text with thousands commas ("2,845.66"); strip them (also `(x)` / leading `-` = negative if they appear). Parse dates to real dates, filter on year AND month.
4. Refunds: counted in the month of `refunded_on`, regardless of when the original transaction settled (a refund of an October- or August-settled txn is judged only by its own refunded_on). Currency = the ORIGINAL transaction's currency (refunds.csv has none); rate = fx on refunded_on, not the settled_on rate. Subtract. "refunds" count = refunds applied in the month.
5. FX: `usd_per_unit` = USD per 1 unit, so USD = amount x rate (multiply). Look up the exact (date, currency) row; never fall back silently to another day, and a rate of 0 is a data error, not a rate. Convert per row, round only the final net (half-up, 2 dp).
6. Sanity before writing: included + excluded-by-reason = unique ids; every refund's txn_id exists in transactions; counts in answer.json equal the audit lists.

Workspace facts (verified on the files here; re-run to confirm if files differ): transactions.csv has 43 rows / 40 unique ids; verbatim duplicates S004, S026, S028 (S004 and S028 are SETTLED in Sep, so no dedupe overcounts them; S026 is VOID). Currencies USD/EUR/INR. refunds.csv has 10 refunds, no duplicate ids, all txn_ids exist; 5 are issued in Sep and 5 (Aug/Oct) must be excluded, including R03/R05 dated 2026-10-31. fx_daily.csv has every date 2026-08-01..10-31 x USD/EUR/INR; its only anomaly is INR = 0 on 2026-10-31 (outside Sep, so irrelevant but never use it). Several Sep-created txns settle in October and several Aug-created settle in Aug: they are not September revenue.

[ACTION] run_command {"command": "python3 skills/payment-revenue-reconcile/scripts/net_revenue.py transactions.csv refunds.csv fx_daily.csv 2026-09"}
[OBSERVATION]
exit=0
txn rows=43 status={'SETTLED': 33, 'PENDING': 6, 'VOID': 4}
unique txn_ids=40; duplicated ids collapsed: ['S004', 'S026', 'S028']
  incl S028 2026-09-22 2541.57 USD -> 2541.5700
  incl S007 2026-09-16 203,738.40 INR -> 2402.0757
  incl S025 2026-09-09 2,515.81 EUR -> 2719.8950
  incl S023 2026-09-15 1060.33 USD -> 1060.3300
  incl S009 2026-09-22 1,485.39 EUR -> 1587.0560
  incl S006 2026-09-07 1,823.35 EUR -> 1957.8986
  incl S035 2026-09-24 188.04 USD -> 188.0400
  incl S011 2026-09-15 1,969.56 USD -> 1969.5600
  incl S021 2026-09-14 685.20 USD -> 685.2000
  incl S038 2026-09-04 483.60 USD -> 483.6000
  incl S004 2026-09-20 1625.41 EUR -> 1739.2440
  incl S034 2026-09-20 2282.34 USD -> 2282.3400
  incl S001 2026-09-26 2,864.89 USD -> 2864.8900
  incl S012 2026-09-09 176921.60 INR -> 2109.9670
  incl S033 2026-09-13 2,099.40 EUR -> 2261.9712
  incl S013 2026-09-07 121.27 EUR -> 130.2188
excluded txns: {'settled outside month': 15, 'status PENDING': 6, 'status VOID': 3}
refund rows=10 duplicated refund_ids=[]
  refund R01 S001 2026-09-27 716.22 USD -> 716.2200 (orig status SETTLED, settled_on 2026-09-26)
  refund R04 S004 2026-09-23 812.70 EUR -> 885.2619 (orig status SETTLED, settled_on 2026-09-20)
  refund R06 S013 2026-09-18 30.32 EUR -> 33.1164 (orig status SETTLED, settled_on 2026-09-07)
  refund R08 S035 2026-09-24 47.01 USD -> 47.0100 (orig status SETTLED, settled_on 2026-09-24)
  refund R09 S011 2026-09-16 984.78 USD -> 984.7800 (orig status SETTLED, settled_on 2026-09-15)
excluded refunds: {'issued outside month': 5}
gross_usd=26983.8564 refunds_usd=2666.3883
{"net_usd": 24317.47, "transactions": 16, "refunds": 5}

[ACTION] write_file {"path": "output/answer.json", "content": "{\"net_usd\": 24317.47, \"transactions\": 16, \"refunds\": 5}"}
[OBSERVATION]
wrote 55 chars to output/answer.json
[ASSISTANT] {
  "net_usd": 24317.47,
  "transactions": 16,
  "refunds": 5
}
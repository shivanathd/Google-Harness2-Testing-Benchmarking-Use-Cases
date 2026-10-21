[ACTION] load_skill {"name": "payment-revenue-reconcile"}
[OBSERVATION]
---
name: payment-revenue-reconcile
description: Compute monthly net revenue in USD from charges, chargebacks (or refunds), a customers flag file and an FX table, following the workspace POLICY.md. Covers timezone-converted month cut-offs, minor units, test-customer exclusion and chargeback netting.
---
# Charges + chargebacks + customers + FX -> net revenue

1. Read POLICY.md (it wins over anything here) and the task's exact output keys.
2. Run once (stdlib only; it computes, writes and re-reads the file):

`python3 skills/payment-revenue-reconcile/scripts/net_revenue.py charges.csv chargebacks.csv customers.csv fx.csv YYYY-MM --out output/answer.json`

(If that path is not reachable, recreate the script from this description in the workspace; do not hunt for it. Source files may sit at the workspace root or under source/.) It prints an audit and `{"net_usd", "transactions", "chargebacks"}`. If the task names other keys, write the file yourself from the printed values (numbers, not strings; real JSON, no escaped quotes). Then `read_file` output/answer.json once and stop.

Rules the script implements; skim the audit against them:
1. Status exactly `captured` is revenue; month decided on `captured_at` converted to UTC (offsets such as -05:00 / +05:30 / +09:00 move rows across month edges).
2. `amount_minor` / 100 for USD, EUR, INR; JPY is whole yen (divide by 1). Multiply by `usd_per_unit`.
3. Customers with `is_test` true are excluded from charges AND chargebacks.
4. Chargeback: subtract the full original charge (USD at the same rate) plus 15.00 fee, booked by the UTC month of `chargeback_at`, regardless of the charge's month or whether the charge was in the same month. `transactions` counts September captured non-test charges even if later charged back; `chargebacks` counts September non-test chargebacks.
5. Round only the final net, half-up, 2 dp.

Workspace facts (verified here from the files; re-check if they differ): test customers are C09 and C10 (includes the huge ch_090/ch_091 charges; ch_022 chargeback cb_5 is also excluded). Edge rows: ch_028 (2026-09-01T03:49+05:30) is August in UTC; ch_000 was captured 2026-08-31 but its chargeback cb_2 is in September, so it counts as a chargeback (not as a transaction). Charges ch_015, ch_013, ch_020, ch_026, ch_006 have chargebacks in Oct/Nov, so they are not September chargebacks. Script result on these files for 2026-09: net_usd 5072.12, transactions 9, chargebacks 3.

[ACTION] run_command {"command": "python3 skills/payment-revenue-reconcile/scripts/net_revenue.py charges.csv chargebacks.csv customers.csv fx.csv 2026-09 --out output/answer.json"}
[OBSERVATION]
exit=0
  charge ch_002 2026-09-01 04:08Z 153712 JPY -> 1026.796160
  charge ch_007 2026-09-01 06:45Z 27459 JPY -> 183.426120
  charge ch_008 2026-09-26 19:00Z 236616 JPY -> 1580.594880
  charge ch_009 2026-09-30 18:08Z 91527 JPY -> 611.400360
  charge ch_011 2026-09-20 19:00Z 142860 JPY -> 954.304800
  skip test customer C10 charge ch_016
  charge ch_021 2026-09-16 13:00Z 9583120 INR -> 1145.182840
  skip test customer C09 charge ch_022
  charge ch_023 2026-09-07 18:00Z 46488 EUR -> 504.394800
  charge ch_025 2026-09-26 06:00Z 529120 INR -> 63.229840
  charge ch_032 2026-09-01 05:33Z 95172 EUR -> 1032.616200
  skip test customer C09 charge ch_038
  skip test customer C09 charge ch_090
  skip test customer C09 charge ch_091
  chargeback cb_0 ch_002 2026-09-14Z -1026.796160 fee -15.00
  chargeback cb_2 ch_000 2026-09-16Z -453.640000 fee -15.00
  skip chargeback cb_5 (test customer)
  chargeback cb_6 ch_023 2026-09-26Z -504.394800 fee -15.00
revenue=7101.946000 chargebacks+fees=2029.830960
{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}
wrote and re-read output/answer.json

[ASSISTANT] {
  "net_usd": 5072.12,
  "transactions": 9,
  "chargebacks": 3
}
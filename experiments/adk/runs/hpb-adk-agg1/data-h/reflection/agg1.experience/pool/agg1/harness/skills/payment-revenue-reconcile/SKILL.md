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

Workspace facts (verified here from the files; re-check if they differ): test customers are C09 and C10 (includes the huge ch_090/ch_091 charges; ch_022 chargeback cb_5 is also excluded). Edge rows: ch_028 (2026-09-01T03:49+05:30) is August in UTC; ch_000 was captured 2026-08-31 but its chargeback cb_2 is in September, so it counts as a chargeback (not as a transaction). Charges ch_015, ch_013, ch_020, ch_026, ch_006 have chargebacks in Oct/Nov, so they are not September chargebacks.

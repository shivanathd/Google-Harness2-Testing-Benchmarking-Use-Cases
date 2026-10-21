---
name: charge-chargeback-revenue
description: Compute one month's net revenue from a payment-processor charges export, chargebacks export, customers (test flag) and an fx table, under a written POLICY.md. Covers UTC month cut-offs from offset timestamps, minor units, test-customer exclusion, chargeback reversal plus fee booked in the chargeback month.
---

# Analytic move
Reconcile three exports into a period figure: RECOGNISE (charges) minus REVERSE (chargebacks), each placed in its month independently, converted to USD, rounded once. POLICY.md in the workspace is the controlling source; the task text fixes the output keys. Read POLICY.md first and let it override anything below.

# Run it
`python3 skills/charge-chargeback-revenue/scripts/net_revenue.py <dir holding the csvs> <YYYY-MM from the task> output/answer.json` (it prints every recognised charge and every chargeback decision, then writes and re-reads the JSON). If you have no shell, apply the rules below by hand over the printed rows and write the file with write_file as plain JSON (raw `{"net_usd": ...}`, no backslash-escaped quotes). Never write a placeholder or estimated number: an unverified figure is worse than a slow one.

# Rules to check before finishing
1. Month is decided on the UTC instant of the timestamp, not the written local date. Offsets like +05:30, -05:00, +09:00 move rows across month edges. Boundary rows (first/last day of the month) need explicit conversion.
2. Recognise only status exactly `captured`; `authorized` and `voided` are never revenue.
3. Minor units: USD/EUR/INR /100, JPY /1 (whole yen). Rate is usd_per_unit: multiply.
4. Test customers (`is_test = true`) are dropped from charges AND from chargebacks (their chargeback gets no reversal and no fee). Look the customer up through the ORIGINAL charge of each chargeback.
5. A chargeback reverses the FULL original charge (converted at the same fx rate) and adds the fixed fee, in the month of `chargeback_at` (UTC) regardless of when the charge was captured. So a chargeback booked in the month may relate to a charge from a prior month (reversal with no matching recognition this month), and a charge recognised this month may be charged back in a later month (still counted in `transactions`, no reversal this month).
6. `transactions` = charges recognised in the month, including ones charged back later or earlier-booked; `chargebacks` = non-test chargebacks whose chargeback_at falls in the month. These counts are independent of each other.
7. Round only the final net to 2 decimals; do not round per row.
8. Confirm every chargeback charge_id exists in charges.csv, every currency has a fx rate, and output is numeric with exactly the three requested keys.

# Traps to check by listing rows, not by memory
- Test customers can own unusually large captured charges; confirm each is excluded and that the exclusion also removes their chargebacks.
- List every row within a day of the month edges and show its UTC instant; a written local date in the month is not evidence.
- For each chargeback, state the charge's own month and the chargeback's month separately; only the chargeback month matters for reversal and fee.
- Identify test customers from customers.csv, not from the task text, and re-check units and fx per currency against the files.

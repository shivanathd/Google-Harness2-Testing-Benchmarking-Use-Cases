Workspace layout (charges.csv, chargebacks.csv, customers.csv, fx.csv, POLICY.md at workspace root; deliverable output/answer.json with keys net_usd, transactions, chargebacks):
- captured_at carries mixed UTC offsets while chargeback timestamps end in Z: bucket every timestamp by its UTC month, since a row near a month boundary can change month after conversion.
- Test customers are flagged by is_test in customers.csv; exclusion applies to charges and to chargebacks on their charges.
- Minor-unit divisors: two-decimal currencies /100, JPY /1 (whole yen). fx.csv is usd_per_unit, so multiply.
- A chargeback reverses the original charge even when that charge falls in an earlier month; it is booked by chargeback_at month. "transactions" counts a recognised charge even if it was later charged back.
- Before writing, cross-check the script printout against POLICY.md wording and your own row-by-row listing; if they differ, find the differing row.

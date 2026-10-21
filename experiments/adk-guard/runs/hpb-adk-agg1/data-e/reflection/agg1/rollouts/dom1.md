[ACTION] load_skill {"name": "payment-revenue-reconcile"}
[OBSERVATION]
---
name: payment-revenue-reconcile
description: Reconcile a payment-processor transaction export with an FX rate table into net revenue for a period (status filter, month filter, dedupe by txn_id, multi-currency to USD). Use for any "net settled revenue" style task on CSV exports.
---

# Net settled revenue from a payment export + FX table

ANALYTIC MOVE: reconcile (classify each row -> dedupe -> filter -> convert -> sum). Inputs: transaction export (txn_id, date, amount, currency, status) and FX table (usd_per_unit per currency). Result: net USD for the period and the count of distinct transactions included, in exactly the shape the task specifies.

Fast path: `python3 skills/payment-revenue-reconcile/scripts/settled_revenue.py transactions.csv fx.csv YYYY-MM output/answer.json` (stdlib only, no pandas needed; handles the quirks below). Read its printed reconciliation, then confirm the checks.

Export quirks to expect (in this workspace they were all present; verify in any other):
- Exact duplicate rows of one txn_id (6 repeated rows, same content). "A txn_id identifies one transaction" -> keep one row per txn_id; count and sum it once. If duplicates of an id DIFFER, do not silently pick one: state the rule used.
- Mixed date formats in one column (`2026-09-15` and `Sep 15, 2026`). Parse every row to a date, then compare year AND month; a text match on "Sep" alone is not a month filter.
- Amounts as text: thousands separators (`"1,944.41"`), accounting negatives (`(954.34)` or `"(2,426.12)"` = -954.34 / -2426.12), plain `-` negatives. Refunds are negative and must stay in the sum (reduce revenue); never take abs().
- Status values: SETTLED / PENDING / VOID. Only SETTLED counts, including its negative (refund) rows; PENDING/VOID rows with negative amounts are excluded. Check the distinct status set and whitespace/case before filtering.
- Out-of-month neighbours (Aug and Oct dates, month-boundary days Sep 1 and Sep 30) must be excluded/included by parsed date.
- Files use CRLF line endings; use a CSV reader, not manual splitting.
- FX: `usd_per_unit` multiplies the native amount (USD = amount x rate). Every currency in the export must have a rate (in this workspace: USD, EUR, INR). Convert per row at full precision, sum, and round once at the end to 2 decimals (half-up); do not round per row.

Checks before finishing:
1. Rows read, duplicates dropped, unique ids reconcile (rows - dropped = unique).
2. `transactions` = number of distinct SETTLED September txn_ids, refunds included.
3. Per-currency native subtotals x rate add up to net_usd; at least one refund row and one accounting-negative row are in the included set.
4. output/answer.json parses as JSON with exactly the requested keys (`net_usd` number rounded to 2 decimals, `transactions` integer) -- a plain object, not a records-list or other pandas orient.

[ACTION] run_command {"command": "python3 skills/payment-revenue-reconcile/scripts/settled_revenue.py transactions.csv fx.csv 2026-09 output/answer.json"}
[OBSERVATION]
exit=0
rows read=42 unique txn_id=36 duplicate rows dropped=6
duplicates with CONFLICTING content: none
unparseable / unmapped: none
  EUR: n=2 native=1293.41 usd=1403.3498
  INR: n=5 native=521132.80 usd=6227.5370
  USD: n=14 native=11060.75 usd=11060.7500
RESULT net_usd=18691.64 transactions=21

[ASSISTANT] {
  "net_usd": 18691.64,
  "transactions": 21
}
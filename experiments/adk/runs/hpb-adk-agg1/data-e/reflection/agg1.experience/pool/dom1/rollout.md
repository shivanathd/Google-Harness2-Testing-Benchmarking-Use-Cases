[ACTION] load_skill {"name": "payment-revenue-reconcile"}
[OBSERVATION]
---
name: payment-revenue-reconcile
description: Compute net/settled revenue in a base currency for a period from a payment-processor transaction export plus an FX table. Covers dirty amounts, mixed date formats, duplicate rows, status filtering, refunds, FX direction.
---
# Payment export -> net revenue

ANALYTIC MOVE: reconcile (clean, dedupe, filter, convert, sum) a transaction export against an FX table; result = one net figure and one count.

Run first (the script is in this skill's scripts/ directory; if that path is not reachable from the workspace, recreate it there; stdlib only, no pandas needed; do not try to pip install):
`python3 skills/payment-revenue-reconcile/scripts/net_revenue.py transactions.csv fx.csv YYYY-MM [--status SETTLED]`
It prints an audit and the `{"net_usd", "transactions"}` JSON; write the task's requested file from those values (as numbers, rounded to 2 dp). Re-check the audit against the rules below.

Rules to confirm before finishing:
1. Dedupe on the identifier BEFORE filtering: the task says one txn_id = one transaction, and exports repeat rows verbatim. Count and sum each id once. If two rows with one id differ, report it and choose explicitly.
2. Amounts are text: strip thousands commas; `(x)` accounting parentheses and leading `-` both mean negative (refund) and must be netted, not dropped or made positive. Refunds count toward the transaction count.
3. Dates arrive in mixed formats (ISO `2026-09-15` and `Sep 15, 2026` in this workspace). Parse every row to a real date and filter on year AND month; never substring-match month names (misses ISO rows, would admit other years).
4. Status filter is exact (SETTLED only); PENDING and VOID are excluded even when negative or in-period. Filter on status and period together.
5. FX: `usd_per_unit` is USD per one unit of currency, so USD = amount * rate (multiply, never divide). Every currency in scope needs a rate; USD = 1. Convert per row, round only the final total (half-up, 2 dp).
6. Sanity: count included + excluded by reason = unique ids; every excluded row has a stated reason.

Workspace facts (verified on transactions.csv/fx.csv here; re-run to confirm if files differ): 42 data rows, 36 unique ids; duplicated ids T11007, T11010, T11012, T11014, T11019, T11022 (identical copies; only T11007, a SETTLED Sep EUR refund, affects the result, so skipping dedupe overcounts to 22 txns). Currencies USD/EUR/INR, rates 1 / 1.0850 / 0.01195. Script result: net_usd 18691.64, 21 transactions.

[ACTION] run_command {"command": "python3 skills/payment-revenue-reconcile/scripts/net_revenue.py transactions.csv fx.csv 2026-09 --status SETTLED"}
[OBSERVATION]
exit=0
rows=42 status={'SETTLED': 27, 'PENDING': 8, 'VOID': 7} currencies={'USD': 26, 'EUR': 7, 'INR': 9}
non-ISO dates=18 paren/comma amounts=15
duplicate txn_ids collapsed to one row: ['T11007', 'T11010', 'T11012', 'T11014', 'T11019', 'T11022']
  incl T11024 2026-09-15 1364.73 USD
  incl T11015 2026-09-09 1,944.41 USD
  incl T11025 2026-09-16 54051.20 INR
  incl T11034 2026-09-23 1036.57 USD
  incl T11030 2026-09-20 1,783.00 USD
  incl T11029 2026-09-14 131,625.60 INR
  incl T11021 2026-09-24 2084.50 USD
  incl T11001 2026-09-06 1175.71 USD
  incl T11002 2026-09-24 -1638.49 USD
  incl T11000 2026-09-18 95156.00 INR
  incl T11018 2026-09-05 (954.34) USD
  incl T11007 2026-09-22 (888.14) EUR
  incl T11009 2026-09-05 135396.80 INR
  incl T11020 2026-09-16 1919.95 USD
  incl T11008 2026-09-04 162.00 USD
  incl T11005 2026-09-10 189.08 USD
  incl T11011 2026-09-01 2181.55 EUR
  incl T11016 2026-09-03 603.72 USD
  incl T11023 2026-09-03 679.24 USD
  incl T11017 2026-09-01 710.67 USD
  incl T11026 2026-09-11 104,903.20 INR
excluded: {'status': 11, 'other month': 4}
{"net_usd": 18691.64, "transactions": 21}

[ACTION] write_file {"content": "{\n  \"net_usd\": 18691.64,\n  \"transactions\": 21\n}", "path": "output/answer.json"}
[OBSERVATION]
wrote 47 chars to output/answer.json
[ASSISTANT] {
  "net_usd": 18691.64,
  "transactions": 21
}
[ACTION] load_skill {"name": "payment-revenue-reconcile"}
[OBSERVATION]
---
name: payment-revenue-reconcile
description: Compute net settled revenue (or similar period totals) from a payment-processor transaction export plus an FX table. Covers dirty exports - duplicate rows, mixed date formats, accounting-style negatives, thousands separators, multi-currency conversion.
---

# Analytic move
Reconcile a raw processor export into one period revenue figure: clean -> de-duplicate on the transaction key -> filter (status AND period) -> convert to reporting currency -> sum. Result is the amount AND the count of transactions that made it in; both must come from the same filtered set.

# Rules a practitioner applies (check each before writing the answer)
1. Row identity: the task states the key (e.g. txn_id). Exports repeat rows (retries/re-exports). Drop duplicates by key BEFORE filtering and count each key once. If the same key appears with different field values, do not guess silently: list it, and pick by the task's wording.
2. Amount parsing: handle all of `1,234.56` (thousands comma), `(123.45)` (accounting negative = -123.45), `-123.45`, plain decimals. Strip commas, convert parentheses to a minus sign. Never use a bare float() on the raw string. After parsing, assert zero NaN/unparseable amounts.
3. Date parsing: columns mix ISO (`2026-09-15`) and text (`Sep 15, 2026`). Parse every value to a real date and test year AND month. Never filter with a substring match like contains "Sep" (ignores year, misses ISO rows). After parsing assert zero unparsed dates; compare against the period boundaries (first day <= d < first day of next month).
4. Status: filter by exact match to the status the task names, after trimming/upper-casing. Print the distinct status values so look-alikes are visible. Statuses other than the named one (PENDING, VOID, ...) are excluded even if the amount is negative.
5. Refunds: negative amounts with included status stay in the sum (they reduce revenue); they count as transactions. Do not take abs() and do not drop them.
6. FX: fx table gives USD per one unit of currency, so usd = amount * rate (multiply, do not divide). Check every currency in the included rows has a rate; fail loudly otherwise. Convert each row, sum, and round only once at the end (2 decimals).
7. Do not rely on a dependency being installed (pandas may be missing and installs may hang): the csv + datetime stdlib is sufficient for this size of file.
8. Finish: output must be exactly the shape the task specifies (keys, types: numeric not string, count an integer). Write it with json.dump, then re-read the file and confirm it parses and has only the requested keys. A run that ends without the deliverable file scores nothing - once a parse error appears, fix the parsing and rerun a changed script, never rerun the identical command.

# Sanity cross-checks
- count included + excluded-by-status + excluded-by-period + duplicates removed = raw row count.
- Print the included rows (key, date, native amount, rate, usd) and eyeball: refunds negative, no repeated key, all dates inside the month.

# Checks specific to this kind of export (re-derive counts from the files, never from memory)
- Verify the FX table's direction and every currency code present in the export against the table before converting.
- Print the distinct statuses, currencies and date formats found; each rule above must be exercised against what actually appears.
- Out-of-period rows with the included status (adjacent months, other years) are expected in these exports; list how many were excluded by period.
- Exact-duplicate rows are expected; report how many keys repeat and whether any repeated key has conflicting field values.
- The reconciliation identity above must hold exactly; if the final figure changes after fixing a rule, explain which rule moved it rather than adjusting the number.

[ACTION] run_command {"command": "python3 scripts/net_revenue.py transactions.csv fx.csv 2026-09 output/answer.json"}
[OBSERVATION]
exit=0
skip T11022: exact duplicate: ('T11022', '2026-10-26', '2,268.54', 'USD', 'SETTLED')
skip T11010: exact duplicate: ('T11010', '2026-10-01', '496.01', 'USD', 'VOID')
skip T11014: exact duplicate: ('T11014', '2026-09-18', '1805.86', 'USD', 'PENDING')
skip T11019: exact duplicate: ('T11019', 'Sep 05, 2026', '(2,426.12)', 'USD', 'PENDING')
skip T11012: exact duplicate: ('T11012', 'Sep 12, 2026', '1,635.92', 'EUR', 'PENDING')
skip T11007: exact duplicate: ('T11007', 'Sep 22, 2026', '(888.14)', 'EUR', 'SETTLED')
unique txn_ids: 36; wrote output/answer.json: {'net_usd': 18691.64, 'transactions': 21}

[ASSISTANT] {
  "net_usd": 18691.64,
  "transactions": 21
}
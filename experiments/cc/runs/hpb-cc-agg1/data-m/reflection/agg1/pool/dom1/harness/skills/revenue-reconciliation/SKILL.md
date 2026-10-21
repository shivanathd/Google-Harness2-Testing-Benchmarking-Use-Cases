---
name: revenue-reconciliation
description: Compute net revenue for a period from payment/transaction exports, refund exports and a daily FX table (multi-currency, recognise-on-settlement). Checklist of data traps and consistency checks.
---

# Net revenue from transactions + refunds + FX

Analytic move: RECONCILE and CALCULATE. Inputs: transaction export, refund export, daily FX table. Result: net USD for one period plus the counts of transactions and refunds that went into it. Net = sum(recognised transactions in USD) - sum(period refunds in USD).

## Before computing, profile each file
1. Transactions: duplicate txn_id rows (compare whole rows: identical = export duplicate, keep one; differing = a conflict to resolve and state). Status values present (only SETTLED is revenue; PENDING/VOID/other are not, whatever their dates). Blank settled_on on non-SETTLED rows. Amounts with thousands separators in quotes ("2,845.66") - strip commas before parsing, and check no amount parsed to 0 or text.
2. Refunds: every txn_id exists in transactions (look up the ORIGINAL transaction's currency; refund rows carry no currency). Refund month is the refunded_on month, NOT the original settle month - a refund of an out-of-period sale still counts, and a refund of an in-period sale issued outside the period does not. Check the refunded txn's status; a refund against a non-SETTLED txn is a conflict to flag, not silently apply.
3. FX: usd_per_unit means USD per 1 unit of currency (multiply, do not divide). Check one row per (date, currency), USD = 1, and that every date/currency you need exists (weekends/gaps: if a needed rate is missing, say so and state the fallback you used).

## Rules
- Recognition date = settled_on (not created_on); rate date = settled_on for sales, refunded_on for refunds. Period boundaries are inclusive on the first and last calendar day.
- Convert each row at its own day's rate, sum at full precision, round once at the end (half-up, 2 decimals). Do not round per row.
- "transactions" count = distinct recognised txn_ids; "refunds" count = refund rows applied in the period. Deliver exactly the keys/shape the task specifies.

## Before finishing
- Re-derive net from the listed rows and confirm gross - refunds = net.
- Confirm the counts equal the lengths of the lists you summed (post-dedup).
- Report in the reply what was excluded and why (duplicates, non-SETTLED, out-of-period, out-of-period refunds) and any assumption.

## Workspace facts (Sept 2026 task; re-verify if files differ)
- transactions.csv had 43 data rows; S004, S026, S028 each appear twice as identical rows (S026 is VOID anyway). Amounts are quoted with commas in many rows. Currencies USD/EUR/INR; fx_daily covers 2026-08-01..2026-10-31 daily with no gaps or duplicate keys.
- All 5 September refunds (R01, R04, R06, R08, R09) reference September-settled SETTLED sales; R00, R03, R05 are October and R02, R07 August (excluded).
- Result obtained: 16 transactions, 5 refunds, net_usd 24317.47 (gross 26983.86, refunds 2666.39), counting duplicates once.

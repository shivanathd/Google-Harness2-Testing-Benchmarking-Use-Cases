---
name: revenue-reconciliation
description: Reconcile payment, settlement, refund and FX exports into a period revenue figure in a reporting currency. Use for recognised or net revenue, refund netting, and multi-currency conversion from a daily rate table.
---

# Revenue reconciliation

Analytic move: calculate period recognised gross, subtract refunds issued in the period, and express both in the reporting currency. Convert each line once, at the rate for its own dated event.

## Decide each rule before summing

- Recognition: a transaction counts only if status is SETTLED and settled_on falls in the period. Use settled_on, never created_on. Non-SETTLED rows (PENDING, VOID, or any other status) are excluded whatever their amount.
- Identity: txn_id identifies one transaction. Collapse repeated txn_id rows to one before filtering, and count distinct transactions, not raw rows.
- Amounts: a quoted field may carry thousands separators ("2,845.66"). Strip the commas before reading the number.
- Currency: a transaction's currency is on its own row. If the refunds file has no currency column, take the currency from the original transaction matched on txn_id.
- Refunds: a refund counts in the period of refunded_on, whatever the period of the original transaction. The refund amount is in the original transaction's currency.
- FX: the rate table gives usd_per_unit for one unit of a currency, so USD = amount x rate. Look up (event date, currency): settled_on for a transaction, refunded_on for a refund. Never convert a refund at its original settlement rate.
- Rounding: keep full precision through the sums and round once to 2 dp, half-up, at the end. Rounding each line first can move the total by a cent.
- Missing rate: if the date and currency have no FX row, stop and report it. Do not carry a neighbouring rate.

## Profile the exports before summing

Run these checks on the files in front of you; do not assume their shape from another export set.

- Count raw rows and distinct txn_id values in the transactions file. For each repeated txn_id, confirm whether the copies are identical before collapsing them.
- Tabulate the status values. Confirm that non-SETTLED rows have no settled_on, or note where they do.
- List the currencies present in transactions, and the date range and currencies covered by the rate table. Check for duplicate (date, currency) keys in the rate table.
- Confirm every refund's txn_id joins to a transactions row, and tabulate refunds by refunded_on month so you know which refunds fall in the period.
- For each (date, currency) event you convert, confirm an FX row exists.

## Artifact contract

The deliverable is one JSON object at the path the task names, with exactly the keys the task lists. For this task type that means:
- net_usd: number, 2 dp.
- transactions: integer count of distinct recognised transactions.
- refunds: integer count of refunds applied.

Read the task's slots as counts. If the task asks for a list instead, follow the task. After writing, reopen the file and confirm it parses and the keys are exact.

## Checks before finishing

- net_usd equals round2(recognised gross USD minus refund USD), and both sums come from the lookups above.
- Every refund's txn_id matches a transactions row, and every refund in the period is counted once.
- transactions equals the number of distinct txn_id values that pass the recognition rule.
- The counts in the JSON equal the rows actually summed.
- Any refund whose original transaction is not itself recognised in the period is named in your final message, with the rule you applied to it.

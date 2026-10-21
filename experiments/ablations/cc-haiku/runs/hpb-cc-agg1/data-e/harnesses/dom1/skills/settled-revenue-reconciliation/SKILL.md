---
name: settled-revenue-reconciliation
description: Reconcile a payment-processor transaction export and an FX rate table into net settled revenue in a reporting currency for a stated period. Use for settled, net, or period revenue computed from processor exports.
---

# Settled revenue reconciliation

## Deliverable and decision rule
- The result is the net amount in the reporting currency for the stated period, plus the count of transactions that contributed to it.
- Settled revenue is net of refunds. Count only rows whose status is exactly the settled status the brief names. Refunds are negative and reduce the total. Pending and voided rows never count, whatever their amount.
- Assign each row to a period by its transaction date after parsing it. Rows outside the period do not count, whichever side of the period they fall on.

## Checks before the total
1. Identity: a transaction identifier names one transaction. If an identifier appears more than once, confirm every field matches and count it once. If the copies differ, do not pick one silently. Report the conflict and the rule you applied.
2. Parse completeness: every date and every amount must parse under a notation you have named. A row that fails to parse is a finding to report, not a row to drop quietly.
3. Amount notation: strip thousands separators inside quoted values. Treat a value wrapped in parentheses as negative (accounting notation) and a leading minus as negative. Where the export documents a different meaning, follow the documentation. Where it does not, state the convention you used in the final message, because it changes the total.
4. Currency: convert each amount with the per-unit USD rate for its own currency (USD per one unit of that currency). Every currency that appears in the included rows needs a rate. A missing rate means the total is not yet computable.
5. Rounding: carry full precision through the sum and round the net once, at the end, to 2 decimals.
6. Consistency: the transaction count equals the number of distinct identifiers in the included set, no identifier is included twice, and the rounded total equals the sum of the included converted amounts rounded once.

## Report
- In the final message, state the conventions you applied to ambiguous notation, every duplicate identifier you found, and any excluded row that looked like it might belong in the period.
- The output file carries only the fields the brief specifies, with the names it specifies.

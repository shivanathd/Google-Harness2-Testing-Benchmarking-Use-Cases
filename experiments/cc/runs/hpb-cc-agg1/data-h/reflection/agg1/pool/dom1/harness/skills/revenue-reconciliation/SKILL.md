---
name: revenue-reconciliation
description: Checks and conventions for turning payment-processor exports (charges, chargebacks, fx, customers) into a monthly net revenue figure under a written recognition policy.
---

# Monthly net revenue from payment exports

ANALYTIC MOVE: reconcile charges + chargebacks + fx + customer flags into one month's net revenue (USD), plus counts. The policy file in the workspace (POLICY.md) is the controlling source; the task text fixes the output fields and their definitions. Where they differ from these notes, they win.

## Order of operations (each step is a filter or a conversion; apply all before summing)
1. Exclude test customers first, from charges AND chargebacks (join chargebacks to charges by charge_id, then charge to customer). Policy says "excluded everywhere".
2. Recognise only status = captured. Authorized / voided are never revenue, whatever their timestamp.
3. Decide the month from the event timestamp converted to UTC: `captured_at` for revenue, `chargeback_at` for chargebacks. Timestamps carry mixed offsets (-05:00, +05:30, +09:00, Z); a local-date read is wrong near month edges.
4. Convert minor units by currency exponent (JPY exponent 0; others 2 unless policy says otherwise), then multiply by the policy's fx rate. Keep full precision; round only the final net.
5. Chargebacks: reverse the FULL original charge plus the flat fee, in the chargeback's UTC month, even if the charge was recognised in another month. A chargeback whose charge is not in the target month still reduces this month's net.
6. net = recognised revenue - reversals of charges charged back in the month - fees.

## Counts: read the task's definition literally
- "transactions" = charges recognised in the month, INCLUDING those later charged back (do not subtract chargebacks).
- "chargebacks" = non-test chargebacks whose chargeback_at falls in the month (not chargebacks of the month's charges).

## Before finishing, confirm
- Every chargeback row is accounted for: list each as in-month / out-of-month / test-excluded; none dropped for a missing charge join.
- Boundary rows were checked in UTC: list charges within ~1 day of the month start/end and state which side each falls on.
- Large-value rows were inspected: an outlier charge is usually a test-customer row or a wrong-unit trap, not real revenue.
- Count and amount use the same filtered set (same exclusions for both).
- Output is exactly the requested file/fields; net has 2 decimals as a number.

## Workspace facts (this task's data; re-verify against the files, they will differ for other months/exports)
- Workspace files are at the workspace root (POLICY.md, charges.csv, chargebacks.csv, customers.csv, fx.csv); test customers were C09 and C10 (C09 holds two very large USD charges ch_090/ch_091, and ch_022 whose chargeback cb_5 falls in September but is excluded as test).
- UTC edge cases: ch_028 (+05:30, 2026-09-01 local) is Aug 31 UTC -> out; ch_015 (Oct 1 03:10Z) -> out; ch_011 (+05:30 2026-09-21 00:30) is Sep 20 UTC -> in.
- Cross-month chargebacks: ch_000 (captured Aug 31 UTC) and ch_002 (Sep) are both reversed in September via cb_2 / cb_0.
- Result reached and checked by script for September 2026: net 5072.12, 9 transactions, 3 chargebacks (cb_0, cb_2, cb_6).

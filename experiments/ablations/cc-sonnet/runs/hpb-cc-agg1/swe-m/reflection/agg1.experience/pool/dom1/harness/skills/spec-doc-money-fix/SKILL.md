---
name: spec-doc-money-fix
description: Fix a money/rounding/tax/discount bug in a small Python codebase when a docs/ file (e.g. docs/ROUNDING.md) defines the rules. Gives the clause-by-clause checklist, Decimal pitfalls, hand-checked expected values and the CHANGES.md contents.
---

# Spec-document money fix

Operation: RECONCILE issue symptoms against the controlling doc, then implement every clause (not only the reported symptoms) and prove it with hand-computed numbers.

## Controlling sources (in order)
1. The doc the issue names (docs/ROUNDING.md) -- binding for every clause.
2. ISSUE.md -- symptoms only; they are a sample of the violations.
3. Existing tests -- a sample; one may already fail because it encodes the doc (read the failure before editing).
4. Also read `CLAUDE.md` in the workspace root if present.

## Clause checklist (tick each against the code before finishing)
- Each doc bullet -> one line in your notes -> the code line that implements it -> one test that fails without it.
- Return TYPE/FORMAT: if the doc says amounts are strings with exactly two decimals, every value of every returned key is `"12.30"`-style, including zero (`"0.00"`) and empty input.
- Order of operations: the doc's formula order is binding (discount BEFORE tax; tax base = subtotal - discount; total = subtotal - discount + tax). Do not re-derive a "more natural" order.
- Rounding at each step the doc names (per-line gross, per-line discount, tax), not only at the end. Sum the ROUNDED per-line values.
- Input normalisation (case-insensitive codes): normalise in the single lookup function every path goes through; unknown value raises the exact exception type the doc names (ValueError), raised before any arithmetic. Don't let a KeyError leak (`raise ... from None`).
- Keep public names/signatures. If a helper's return type changes (e.g. float -> Decimal), grep for its other callers and tests.

## Decimal pitfalls
- Never `float()` anywhere on the money path; build Decimals from the decimal STRINGS (`Decimal(item.unit_price)`), never from a float. Int qty / int pct multiply into Decimal fine.
- "Half-up" = `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`. Builtin `round()` and the default context (HALF_EVEN) are wrong: 0.125 -> 0.12 instead of 0.13.
- Divide by 100 only after multiplying (`gross * pct / 100`), then quantize; format with `f"{d:.2f}"` / `quantize` result `str()`.
- `sum()` of Decimals needs a Decimal start value for empty input.

## Hand-checked values for THIS workspace (recompute; they are facts for invoicing/, not for other repos)
- `compute_totals([LineItem("widget", 3, "19.99", 10)], "eu")`: gross 59.97, discount 5.997 -> 6.00, net 53.97, tax 53.97 x 0.20 = 10.794 -> 10.79, total 64.76. Strings: subtotal "59.97", discount "6.00", tax "10.79", total "64.76". Same result for "EU", "Eu".
- `LineItem("x", 1, "0.125")` US: line gross "0.13" (float gives 0.12). `LineItem("x", 3, "0.125")`: 0.375 -> "0.38".
- `LineItem("a", 2, "10.00")` US total "20.00" (the one existing test, which fails on the float code).
- Rates live in invoicing/tax.py RATES (US 0.00, EU 0.20, UK 0.20, IN 0.18); unknown region (e.g. "XX") -> ValueError.

## Tests
Add tests to tests/test_totals.py for: lower-case region, unknown region -> ValueError, discount-before-tax, half-cent rounding, zero-discount/US all-"0.00" formatting, empty list. Run `python -m pytest tests` and confirm the original test passes too.

## output/CHANGES.md contents (short)
Files changed; one line per issue symptom AND per extra doc clause fixed (float->Decimal, string format, discount-before-tax, case-insensitive, ValueError); tests added; test command and result. Write it right after the first passing edit and update it if the code changes; state plainly anything not run.

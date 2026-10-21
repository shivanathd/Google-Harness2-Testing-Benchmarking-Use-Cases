---
name: fix-python-bug
description: Practitioner checklist for resolving an issue in a small Python codebase against a written spec (ISSUE.md, docs/, docstrings) - clause enumeration, money/Decimal rules, regression floor, CHANGES.md contents.
---

# Resolve an issue in a small Python codebase

ANALYTIC MOVE: reconcile three sources. ISSUE.md gives symptoms (each bullet is ONE instance of a defect). The spec it points to (docs/*.md, docstring) is the controlling source for "correct". Existing tests are only a regression floor. Change code until all three agree.

## Before editing
1. Read ISSUE.md, every spec doc it names, ALL source modules in the package (not just the one named: the cause is often in a helper such as a lookup table or rate function), and tests/ (plus conftest.py).
2. Write a numbered list: one line per spec clause AND per issue bullet. Map each to the line of code that violates it. Several clauses are usually broken at once, and some clauses are not mentioned in the issue at all (e.g. rounding mode, output format, error type, case-insensitivity).
3. Keep every public name and signature (functions, dataclass fields, module-level tables). Fix at the lowest layer that owns the behaviour (e.g. normalise region case inside the lookup function so every caller benefits), and do not edit existing tests; add new tests in a new file (tests/test_<topic>.py).

## Money / rounding rules (when the spec says Decimal, half-up, cents)
- Build Decimals from strings: `Decimal(str(x))`. Never `Decimal(float)`; never `float()` anywhere in the money path. Python `round()` is banker's rounding on floats, so it is wrong here - use `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`.
- Round at exactly the points the spec names, in the spec's order; intermediate rounded values feed later steps (e.g. discount computed from the already-rounded line gross, tax from rounded subtotal - rounded discount). Do not round earlier or later than the spec says, and do not recompute a total from unrounded parts.
- Sum already-rounded line values; the result of sums of 2-dp Decimals is already 2 dp but still format it.
- Return exactly what the spec says: strings with exactly two decimals (`format(d, "f")` after quantize, or `str(d)` of a quantized value) - never floats, never Decimal objects, never "5" or "5.0". Empty input must still give "0.00" for every amount.
- Order of operations matters: tax base is the DISCOUNTED amount when the spec says so; total = subtotal - discount + tax (check each term's sign against the spec).
- Lookup tables / codes: normalise case (and strip) before lookup if spec says case-insensitive; an unknown key must raise the exact exception type the spec names (e.g. ValueError), not leak KeyError. `raise ValueError(...) from None`.
- If a helper is public and its return type is not fixed by the spec (e.g. a per-line helper), keep its name and make it return a quantized Decimal; make sure every caller is consistent.

## In this workspace (invoicing package, issue #142 - verified from the files; re-check if files differ)
- Files: invoicing/totals.py (line_total, compute_totals), invoicing/tax.py (RATES dict with upper-case keys "US","EU","UK","IN" and rate_for), invoicing/models.py (LineItem: description, qty:int, unit_price:str, discount_pct:int=0), docs/ROUNDING.md (the spec).
- Root causes: (a) rate_for does `RATES[region]` with no case folding and leaks KeyError, so "eu" fails and unknown regions are not ValueError; (b) tax is computed on subtotal instead of subtotal - discount; (c) float() and round() are used everywhere, and results are floats not 2-dp strings; (d) discount is computed from unrounded value and rounded only once on the sum, spec says per-line half-up; (e) total must be built from the rounded parts: subtotal - discount + tax.
- Hand-check worth running: compute_totals([LineItem("widget", 3, "19.99", 10)], "eu") must give subtotal "59.97", discount "6.00" (5.997 rounds half-up per line), tax "10.79" (53.97 x 0.20 = 10.794), total "64.76". Also check a 0.125 unit price case (qty 1 -> line gross "0.13" half-up, not "0.12"), mixed-case region "Eu", unknown region "XX" -> ValueError, empty item list -> all "0.00", and the existing test (US, 2 x "10.00" -> total "20.00").

## Finish
- Run the existing tests plus your new test file (`python -m pytest tests`, or plain python if pytest is missing); report failures honestly.
- Write output/CHANGES.md (the task requires it; create output/ if absent): list each root cause fixed, the files changed, the tests added, and any judgement calls. Do not end the turn with only a plan: the edits and CHANGES.md must exist.

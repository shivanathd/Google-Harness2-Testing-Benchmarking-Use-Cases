---
name: money-calc-bugfix
description: Fix monetary calculations (totals, tax, discounts, rounding, region/rate lookups) in a small Python codebase so they follow a written rounding/money spec without breaking existing callers.
---

# Analytic move
RECONCILE the code against the controlling spec (the docs file the ISSUE names, e.g. docs/ROUNDING.md), then
REWRITE the calculation so every spec line maps to one line of code. The ISSUE's bullets are symptoms; the spec is the
authority. If they conflict, follow the spec and say so in CHANGES.md.

# Spec-to-code checklist (confirm each before finishing)
1. Decimal only: build values with `Decimal(str_value)`; never `Decimal(float)` and never `float()` anywhere in the money path.
   Rates stored as strings (e.g. "0.20") go through `Decimal(rate)`.
2. Round with `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` at EXACTLY the steps the spec names (e.g. per-line gross,
   per-line discount, tax) - not once at the end, and not at steps the spec does not name. Python's `round()` is banker's/float: forbidden.
3. Order of operations is part of the spec: subtotal = sum of rounded line gross; discount = sum of rounded line discounts;
   tax base = subtotal - discount (NOT subtotal); total = subtotal - discount + tax. Check the sign of the discount and the tax base explicitly; float-era code often taxes the undiscounted amount or adds the discount.
4. Output format: every returned amount is a str with exactly two decimals (`format(x, "f")` after quantize, so "0.00" not "0" or "0E-2").
   Keep the dict keys and the function name/signature unchanged. Empty item list -> all "0.00".
5. Lookup keys: normalise region with `.upper()` (spec: case-insensitive) and raise ValueError (not KeyError) for unknown region,
   including non-string/empty input. Do this where the lookup lives (rate_for) so every caller benefits, and have compute_totals
   validate region even when items is empty. Keep `rate_for` name/signature.
6. Discount percent may be int; use `Decimal(item.discount_pct) / 100` or multiply then divide in Decimal - no float.

# Tests and deliverable
- Run the existing tests before and after. Add regression tests to tests/test_totals.py for each bullet of the ISSUE
  (lowercase/mixed-case region, tax on discounted base, half-up .125 case, unknown region -> ValueError, string-with-two-decimals format),
  asserting values you hand-compute from the spec (including a half-cent tie that float rounding gets wrong), not values copied from your own output.
- output/CHANGES.md: short; one line per fixed symptom naming the file/function changed, plus tests added. Do not change public names.

---
name: invoice-totals
description: Checks for invoice totals, line discounts, tax and money rounding in invoicing code. Use when computing, fixing or reviewing amounts, tax, discounts or their string formatting.
---

# Invoice totals

The controlling source is the workspace's money-rules or rounding doc. Locate it by listing the
tree (it is usually under docs/) and read it in full. The issue text is the symptom report; where
it and the doc disagree, the doc wins. Rates and region rules come from the code's rate table and
the doc, not from memory.

## Traps the doc does not spell out

- Build amounts with Decimal from strings. Decimal(float) keeps binary noise.
- Python's Decimal default rounding is ROUND_HALF_EVEN. Always pass `rounding=ROUND_HALF_UP`
  to quantize. Without it, a half-cent value such as 0.125 becomes 0.12.
- float round() is also half-even on the binary value, so round(0.125, 2) gives 0.12.
- A KeyError from a dict lookup of a region is not the error the doc names. Map unknown regions to
  the exception type the doc specifies.
- Keep the existing public function names, signatures and the return keys. Check the return types
  that the doc specifies and any test assertion on those types before choosing them.

## Checks before finishing

- Recompute the total from the returned amounts with Decimal: it must equal subtotal minus
  discount plus tax.
- Every returned amount has exactly two decimals, in the form the doc specifies.
- Recompute the example quoted in the issue by hand from the doc's rules, and confirm the code's
  output matches that hand result.
- Upper- and lower-case region codes return identical results, if the doc says region codes are
  case-insensitive.
- Each rule the doc states (rounding point, rounding mode, discount base, unknown-region behaviour)
  has a code path that visibly implements it.
- The task's test command passes after your last edit.

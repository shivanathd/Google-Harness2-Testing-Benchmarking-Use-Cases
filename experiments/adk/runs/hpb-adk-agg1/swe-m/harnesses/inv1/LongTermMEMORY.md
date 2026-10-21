Workspace facts (verified for the invoicing task; re-check if the codebase differs):
- Tools take paths relative to the workspace root. Layout: ISSUE.md, docs/ROUNDING.md (the spec), invoicing/{models,tax,totals}.py, tests/test_totals.py (one test, US only).
- The bug is spread across two modules: invoicing/tax.py `rate_for` does a case-sensitive dict lookup (raises KeyError, not ValueError, for unknown or lower-case codes), and invoicing/totals.py uses float and computes tax before discount. The fix may need both files.
- LineItem.unit_price is a decimal string and discount_pct an int; compute_totals must return all four amounts (subtotal, discount, tax, total) as two-decimal strings.
- Baseline: the one existing test already fails (returns float 20.0, expects "20.00"); it is a valid spec check, not a test to edit.

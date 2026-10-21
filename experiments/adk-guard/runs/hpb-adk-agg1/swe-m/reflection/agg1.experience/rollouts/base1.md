[ACTION] list_files {"path": "workspace"}
[OBSERVATION]
ERROR: ValueError: no such directory: 'workspace' (paths are relative to the workspace root)
[ACTION] list_files {"path": "/"}
[OBSERVATION]
ERROR: ValueError: path is outside the workspace
[ACTION] list_files {"path": "."}
[OBSERVATION]
ISSUE.md
docs/ROUNDING.md
invoicing/__init__.py
invoicing/models.py
invoicing/tax.py
invoicing/totals.py
tests/test_totals.py
[ACTION] read_file {"path": "ISSUE.md", "start_line": 0, "max_lines": 100}
[OBSERVATION]
[9 lines total]
# #142 Invoice totals wrong for discounted EU invoices

Reported by finance:

- `compute_totals([LineItem("widget", 3, "19.99", 10)], "eu")` raises KeyError.
- With "EU" the tax is charged on the undiscounted amount.
- Totals are sometimes a cent off (float rounding), e.g. a 0.125 unit price.

Please make `invoicing.totals.compute_totals` follow docs/ROUNDING.md.
[ACTION] read_file {"max_lines": 100, "path": "docs/ROUNDING.md", "start_line": 0}
[OBSERVATION]
[10 lines total]
# Money rules

- All money is computed with `decimal.Decimal`, never float, and every amount that
  `compute_totals` returns is a string with exactly two decimals, e.g. "12.30".
- Line gross = qty x unit_price, rounded half-up to cents.
- Line discount = line gross x discount_pct / 100, rounded half-up to cents.
- subtotal = sum of line gross; discount = sum of line discounts.
- tax = (subtotal - discount) x the region's rate, rounded half-up to cents.
- total = subtotal - discount + tax.
- Region codes are case-insensitive. An unknown region raises ValueError.
[ACTION] read_file {"max_lines": 100, "path": "tests/test_totals.py", "start_line": 0}
[OBSERVATION]
[6 lines total]
from invoicing.models import LineItem
from invoicing.totals import compute_totals


def test_simple_us():
    assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"
[ASSISTANT] I need to fix the `compute_totals` function in `invoicing/totals.py` to adhere to the rounding rules in `docs/ROUNDING.md`. I'll implement the following steps:

1. Ensure all calculations use `decimal.Decimal` to avoid floating-point errors.
2. Apply rounding rules for line gross, line discount, subtotal, tax, and total.
3. Handle region codes case-insensitively and raise a `ValueError` for unknown regions.
4. Ensure the function returns a string with exactly two decimal places.

I'll make these changes and then write a summary of the changes to `output/CHANGES.md`. Let's start by implementing the fix.
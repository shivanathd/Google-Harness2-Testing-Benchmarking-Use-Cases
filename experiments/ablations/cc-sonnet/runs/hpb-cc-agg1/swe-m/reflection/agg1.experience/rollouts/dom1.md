[ACTION] Bash {"command": "ls -la && cat ISSUE.md && ls -R docs tests output 2>/dev/null | head -50", "description": "List workspace and read ISSUE.md"}
[OBSERVATION]
total 16
drwxr-xr-x@ 9 me  staff  288 Oct 19 12:10 .
drwxr-xr-x@ 3 me  staff   96 Oct 19 12:10 ..
drwxr-xr-x@ 3 me  staff   96 Oct 19 12:10 .claude
-rw-r--r--@ 1 me  staff  705 Oct 19 12:10 CLAUDE.md
-rw-r--r--@ 1 me  staff  366 Oct 19 11:56 ISSUE.md
drwxr-xr-x@ 3 me  staff   96 Oct 19 11:56 docs
drwxr-xr-x@ 6 me  staff  192 Oct 19 11:56 invoicing
drwxr-xr-x@ 2 me  staff   64 Oct 19 11:56 output
drwxr-xr-x@ 3 me  staff   96 Oct 19 11:56 tests
# #142 Invoice totals wrong for discounted EU invoices

Reported by finance:

- `compute_totals([LineItem("widget", 3, "19.99", 10)], "eu")` raises KeyError.
- With "EU" the tax is charged on the undiscounted amount.
- Totals are sometimes a cent off (float rounding), e.g. a 0.125 unit price.

Please make `invoicing.totals.compute_totals` follow docs/ROUNDING.md.
docs:
ROUNDING.md

output:

tests:
test_totals.py
[ACTION] Bash {"command": "cat docs/ROUNDING.md && echo ---- && find invoicing -type f | grep -v __pycache__ && echo ---- && for f in $(find invoicing -name '*.py' | grep -v __pycache__); do echo \"== $f\"; cat \"$f\"; done && echo ---- && cat tests/test_totals.py", "description": "Read rounding spec, source, and tests"}
[OBSERVATION]
# Money rules

- All money is computed with `decimal.Decimal`, never float, and every amount that
  `compute_totals` returns is a string with exactly two decimals, e.g. "12.30".
- Line gross = qty x unit_price, rounded half-up to cents.
- Line discount = line gross x discount_pct / 100, rounded half-up to cents.
- subtotal = sum of line gross; discount = sum of line discounts.
- tax = (subtotal - discount) x the region's rate, rounded half-up to cents.
- total = subtotal - discount + tax.
- Region codes are case-insensitive. An unknown region raises ValueError.
----
invoicing/tax.py
invoicing/models.py
invoicing/__init__.py
invoicing/totals.py
----
== invoicing/tax.py
RATES = {"US": "0.00", "EU": "0.20", "UK": "0.20", "IN": "0.18"}


def rate_for(region):
    return RATES[region]
== invoicing/models.py
from dataclasses import dataclass


@dataclass
class LineItem:
    description: str
    qty: int
    unit_price: str  # decimal string, e.g. "19.99"
    discount_pct: int = 0
== invoicing/__init__.py
== invoicing/totals.py
from .tax import rate_for


def line_total(item):
    return round(item.qty * float(item.unit_price), 2)


def compute_totals(items, region):
    subtotal = sum(line_total(i) for i in items)
    tax = round(subtotal * float(rate_for(region)), 2)
    discount = round(sum(line_total(i) * i.discount_pct / 100 for i in items), 2)
    total = subtotal + tax - discount
    return {"subtotal": subtotal, "discount": discount, "tax": tax, "total": total}
----
from invoicing.models import LineItem
from invoicing.totals import compute_totals


def test_simple_us():
    assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"
[ASSISTANT] The issue is a money/rounding bug with a `docs/` rules file, so I'm loading the matching skill as the project instructions require.
[ACTION] Skill {"skill": "spec-doc-money-fix"}
[OBSERVATION]
Launching skill: spec-doc-money-fix
[ASSISTANT] The skill's checklist is loaded. Before editing, I'll run the existing tests to see the baseline failure.
[ACTION] Bash {"command": "python -m pytest tests 2>&1 | tail -20", "description": "Run existing tests for baseline"}
[OBSERVATION]
============================= test session starts ==============================
platform darwin -- Python 3.13.16, pytest-9.1.1, pluggy-1.7.0
rootdir: .
plugins: anyio-4.13.0
collected 1 item

tests/test_totals.py F                                                   [100%]

=================================== FAILURES ===================================
________________________________ test_simple_us ________________________________

    def test_simple_us():
>       assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"
E       AssertionError: assert 20.0 == '20.00'

tests/test_totals.py:6: AssertionError
=========================== short test summary info ============================
FAILED tests/test_totals.py::test_simple_us - AssertionError: assert 20.0 == ...
============================== 1 failed in 2.01s ===============================
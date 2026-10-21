[ACTION] Bash {"command": "ls -la && cat ISSUE.md && find . -path ./.git -prune -o -type f -print | head -100", "description": "List work directory and read ISSUE.md"}
[OBSERVATION]
total 16
drwxr-xr-x@ 9 me  staff  288 Oct 19 12:53 .
drwxr-xr-x@ 3 me  staff   96 Oct 19 12:53 ..
drwxr-xr-x@ 3 me  staff   96 Oct 19 12:53 .claude
-rw-r--r--@ 1 me  staff  431 Oct 19 12:53 CLAUDE.md
-rw-r--r--@ 1 me  staff  366 Oct 19 12:02 ISSUE.md
drwxr-xr-x@ 3 me  staff   96 Oct 19 12:02 docs
drwxr-xr-x@ 6 me  staff  192 Oct 19 12:02 invoicing
drwxr-xr-x@ 2 me  staff   64 Oct 19 12:02 output
drwxr-xr-x@ 3 me  staff   96 Oct 19 12:02 tests
# #142 Invoice totals wrong for discounted EU invoices

Reported by finance:

- `compute_totals([LineItem("widget", 3, "19.99", 10)], "eu")` raises KeyError.
- With "EU" the tax is charged on the undiscounted amount.
- Totals are sometimes a cent off (float rounding), e.g. a 0.125 unit price.

Please make `invoicing.totals.compute_totals` follow docs/ROUNDING.md.
./tests/test_totals.py
./.claude/skills/invoice-totals/SKILL.md
./docs/ROUNDING.md
./ISSUE.md
./invoicing/tax.py
./invoicing/models.py
./invoicing/__init__.py
./invoicing/totals.py
./CLAUDE.md
[ACTION] Bash {"command": "for f in docs/ROUNDING.md invoicing/*.py tests/test_totals.py .claude/skills/invoice-totals/SKILL.md; do echo \"=== $f\"; cat \"$f\"; done; ls -la output", "description": "Read docs, source, tests and skill file"}
[OBSERVATION]
=== docs/ROUNDING.md
# Money rules

- All money is computed with `decimal.Decimal`, never float, and every amount that
  `compute_totals` returns is a string with exactly two decimals, e.g. "12.30".
- Line gross = qty x unit_price, rounded half-up to cents.
- Line discount = line gross x discount_pct / 100, rounded half-up to cents.
- subtotal = sum of line gross; discount = sum of line discounts.
- tax = (subtotal - discount) x the region's rate, rounded half-up to cents.
- total = subtotal - discount + tax.
- Region codes are case-insensitive. An unknown region raises ValueError.
=== invoicing/__init__.py
=== invoicing/models.py
from dataclasses import dataclass


@dataclass
class LineItem:
    description: str
    qty: int
    unit_price: str  # decimal string, e.g. "19.99"
    discount_pct: int = 0
=== invoicing/tax.py
RATES = {"US": "0.00", "EU": "0.20", "UK": "0.20", "IN": "0.18"}


def rate_for(region):
    return RATES[region]
=== invoicing/totals.py
from .tax import rate_for


def line_total(item):
    return round(item.qty * float(item.unit_price), 2)


def compute_totals(items, region):
    subtotal = sum(line_total(i) for i in items)
    tax = round(subtotal * float(rate_for(region)), 2)
    discount = round(sum(line_total(i) * i.discount_pct / 100 for i in items), 2)
    total = subtotal + tax - discount
    return {"subtotal": subtotal, "discount": discount, "tax": tax, "total": total}
=== tests/test_totals.py
from invoicing.models import LineItem
from invoicing.totals import compute_totals


def test_simple_us():
    assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"
=== .claude/skills/invoice-totals/SKILL.md
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
total 0
drwxr-xr-x@ 2 me  staff   64 Oct 19 12:02 .
drwxr-xr-x@ 9 me  staff  288 Oct 19 12:53 ..
[ACTION] Bash {"command": "(python -m pytest tests 2>&1 | tail -15); git status --short . | head", "description": "Run existing tests for baseline"}
[OBSERVATION]
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
============================== 1 failed in 0.29s ===============================
[ASSISTANT] The existing test already fails (float `20.0` vs the string `"20.00"` the doc requires). I'll rewrite the money math in `totals.py` and the region lookup in `tax.py`.
[ACTION] Read {"file_path": "./invoicing/totals.py"}
[OBSERVATION]
1	from .tax import rate_for
2	
3	
4	def line_total(item):
5	    return round(item.qty * float(item.unit_price), 2)
6	
7	
8	def compute_totals(items, region):
9	    subtotal = sum(line_total(i) for i in items)
10	    tax = round(subtotal * float(rate_for(region)), 2)
11	    discount = round(sum(line_total(i) * i.discount_pct / 100 for i in items), 2)
12	    total = subtotal + tax - discount
13	    return {"subtotal": subtotal, "discount": discount, "tax": tax, "total": total}
14	
[ACTION] Read {"file_path": "./invoicing/tax.py"}
[OBSERVATION]
1	RATES = {"US": "0.00", "EU": "0.20", "UK": "0.20", "IN": "0.18"}
2	
3	
4	def rate_for(region):
5	    return RATES[region]
6	
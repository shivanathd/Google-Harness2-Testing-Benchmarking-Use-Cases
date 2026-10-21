[ACTION] Bash {"command": "ls -la && cat ISSUE.md && find . -path ./output -prune -o -type f -print | head -100", "description": "Show workspace files and issue description"}
[OBSERVATION]
total 16
drwxr-xr-x@ 8 me  staff  256 Oct 19 11:59 .
drwxr-xr-x@ 3 me  staff   96 Oct 19 11:59 ..
-rw-r--r--@ 1 me  staff  172 Oct 19 11:59 CLAUDE.md
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
./tests/test_totals.py
./docs/ROUNDING.md
./ISSUE.md
./invoicing/tax.py
./invoicing/models.py
./invoicing/__init__.py
./invoicing/totals.py
./CLAUDE.md
[ACTION] Bash {"command": "for f in docs/ROUNDING.md invoicing/tax.py invoicing/models.py invoicing/__init__.py invoicing/totals.py tests/test_totals.py; do echo \"=== $f\"; cat -n \"$f\"; done", "description": "Print docs, source, and tests"}
[OBSERVATION]
=== docs/ROUNDING.md
     1	# Money rules
     2	
     3	- All money is computed with `decimal.Decimal`, never float, and every amount that
     4	  `compute_totals` returns is a string with exactly two decimals, e.g. "12.30".
     5	- Line gross = qty x unit_price, rounded half-up to cents.
     6	- Line discount = line gross x discount_pct / 100, rounded half-up to cents.
     7	- subtotal = sum of line gross; discount = sum of line discounts.
     8	- tax = (subtotal - discount) x the region's rate, rounded half-up to cents.
     9	- total = subtotal - discount + tax.
    10	- Region codes are case-insensitive. An unknown region raises ValueError.
=== invoicing/tax.py
     1	RATES = {"US": "0.00", "EU": "0.20", "UK": "0.20", "IN": "0.18"}
     2	
     3	
     4	def rate_for(region):
     5	    return RATES[region]
=== invoicing/models.py
     1	from dataclasses import dataclass
     2	
     3	
     4	@dataclass
     5	class LineItem:
     6	    description: str
     7	    qty: int
     8	    unit_price: str  # decimal string, e.g. "19.99"
     9	    discount_pct: int = 0
=== invoicing/__init__.py
=== invoicing/totals.py
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
=== tests/test_totals.py
     1	from invoicing.models import LineItem
     2	from invoicing.totals import compute_totals
     3	
     4	
     5	def test_simple_us():
     6	    assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"
[ASSISTANT] The docs define the rules, and the code breaks several of them: float math, tax on the undiscounted amount, and a case-sensitive region lookup that raises KeyError. I'll check the baseline test run before editing.
[ACTION] Bash {"command": "(python -m pytest tests -q 2>&1 || python -m pytest --version 2>&1) | tail -5; ls output", "description": "Run baseline tests and list output dir"}
[OBSERVATION]
tests/test_totals.py:6: AssertionError
=========================== short test summary info ============================
FAILED tests/test_totals.py::test_simple_us - AssertionError: assert 20.0 == ...
1 failed in 1.22s
pytest 9.1.1
[ASSISTANT] The existing test already fails: it expects `"20.00"` and gets the float `20.0`. The docs require strings, so that is part of the same fix. Next I'll update the region lookup and rewrite the totals math.
[ACTION] Edit {"replace_all": false, "file_path": "./invoicing/tax.py", "old_string": "def rate_for(region):\n    return RATES[region]", "new_string": "def rate_for(region):\n    try:\n        return RATES[region.upper()]\n    except KeyError:\n        raise ValueError(f\"unknown region: {region}\") from None"}
[ACTION] Edit {"replace_all": false, "file_path": "./invoicing/totals.py", "old_string": "from .tax import rate_for\n\n\ndef line_total(item):\n    return round(item.qty * float(item.unit_price), 2)\n\n\ndef compute_totals(items, region):\n    subtotal = sum(line_total(i) for i in items)\n    tax = round(subtotal * float(rate_for(region)), 2)\n    discount = round(sum(line_total(i) * i.discount_pct / 100 for i in items), 2)\n    total = subtotal + tax - discount\n    return {\"subtotal\": subtotal, \"discount\": discount, \"tax\": tax, \"total\": total}", "new_string": "from decimal import ROUND_HALF_UP, Decimal\n\nfrom .tax import rate_for\n\nCENT = Decimal(\"0.01\")\n\n\ndef _cents(value):\n    return value.quantize(CENT, rounding=ROUND_HALF_UP)\n\n\ndef line_total(item):\n    return _cents(item.qty * Decimal(item.unit_price))\n\n\ndef compute_totals(items, region):\n    rate = Decimal(rate_for(region))\n    subtotal = sum((line_total(i) for i in items), Decimal(\"0.00\"))\n    discount = sum(\n        (_cents(line_total(i) * i.discount_pct / 100) for i in items), Decimal(\"0.00\")\n    )\n    tax = _cents((subtotal - discount) * rate)\n    total = subtotal - discount + tax\n    return {\n        \"subtotal\": f\"{subtotal:.2f}\",\n        \"discount\": f\"{discount:.2f}\",\n        \"tax\": f\"{tax:.2f}\",\n        \"total\": f\"{total:.2f}\",\n    }"}
[OBSERVATION]
The file ./invoicing/tax.py has been updated successfully.
[OBSERVATION]
The file ./invoicing/totals.py has been updated successfully.
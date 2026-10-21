[ACTION] Bash {"command": "find . -type f -not -path '*/.git/*' | head -100 && echo --- && cat ISSUE.md", "description": "List workspace files and read the issue"}
[OBSERVATION]
./ISSUE.md
./CLAUDE.md
./tests/test_totals.py
./docs/ROUNDING.md
./invoicing/tax.py
./invoicing/models.py
./invoicing/__init__.py
./invoicing/totals.py
---
# #142 Invoice totals wrong for discounted EU invoices

Reported by finance:

- `compute_totals([LineItem("widget", 3, "19.99", 10)], "eu")` raises KeyError.
- With "EU" the tax is charged on the undiscounted amount.
- Totals are sometimes a cent off (float rounding), e.g. a 0.125 unit price.

Please make `invoicing.totals.compute_totals` follow docs/ROUNDING.md.
[ACTION] Bash {"command": "for f in docs/ROUNDING.md invoicing/totals.py invoicing/tax.py invoicing/models.py invoicing/__init__.py tests/test_totals.py; do echo \"=== $f\"; cat -n $f; done", "description": "Read docs, source and tests"}
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
=== tests/test_totals.py
     1	from invoicing.models import LineItem
     2	from invoicing.totals import compute_totals
     3	
     4	
     5	def test_simple_us():
     6	    assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"
[ASSISTANT] Root causes: `rate_for` does a case-sensitive dict lookup (so "eu" raises KeyError), tax is computed on the undiscounted subtotal, and everything uses float rounding. `docs/ROUNDING.md` is the spec. I'll fix the region lookup first, then rewrite the money math in Decimal.
[ACTION] Edit {"replace_all": false, "file_path": "./invoicing/tax.py", "old_string": "def rate_for(region):\n    return RATES[region]", "new_string": "def rate_for(region):\n    code = region.upper()\n    if code not in RATES:\n        raise ValueError(f\"unknown region: {region}\")\n    return RATES[code]"}
[OBSERVATION]
The file ./invoicing/tax.py has been updated successfully.
[ACTION] Edit {"replace_all": false, "file_path": "./invoicing/totals.py", "old_string": "from .tax import rate_for\n\n\ndef line_total(item):\n    return round(item.qty * float(item.unit_price), 2)\n\n\ndef compute_totals(items, region):\n    subtotal = sum(line_total(i) for i in items)\n    tax = round(subtotal * float(rate_for(region)), 2)\n    discount = round(sum(line_total(i) * i.discount_pct / 100 for i in items), 2)\n    total = subtotal + tax - discount\n    return {\"subtotal\": subtotal, \"discount\": discount, \"tax\": tax, \"total\": total}", "new_string": "from decimal import ROUND_HALF_UP, Decimal\n\nfrom .tax import rate_for\n\nCENT = Decimal(\"0.01\")\n\n\ndef _cents(amount):\n    return amount.quantize(CENT, rounding=ROUND_HALF_UP)\n\n\ndef line_total(item):\n    return _cents(item.qty * Decimal(item.unit_price))\n\n\ndef compute_totals(items, region):\n    rate = Decimal(rate_for(region))\n    subtotal = sum((line_total(i) for i in items), Decimal(\"0\"))\n    discount = sum(\n        (_cents(line_total(i) * i.discount_pct / 100) for i in items), Decimal(\"0\")\n    )\n    tax = _cents((subtotal - discount) * rate)\n    total = subtotal - discount + tax\n    return {\n        \"subtotal\": f\"{subtotal:.2f}\",\n        \"discount\": f\"{discount:.2f}\",\n        \"tax\": f\"{tax:.2f}\",\n        \"total\": f\"{total:.2f}\",\n    }"}
[OBSERVATION]
The file ./invoicing/totals.py has been updated successfully.
[ACTION] Bash {"command": "mkdir -p output && cat > output/CHANGES.md <<'EOF'\n# Changes for #142: invoice totals for discounted EU invoices\n\n## What changed\n- `invoicing/tax.py`: `rate_for` normalises region codes to upper case, so \"eu\" works. Unknown regions raise `ValueError` (previously `KeyError`).\n- `invoicing/totals.py`: all money is computed with `decimal.Decimal` and rounded half-up to cents, per docs/ROUNDING.md:\n  - line gross = qty x unit_price, rounded to cents\n  - line discount = line gross x discount_pct / 100, rounded to cents\n  - subtotal and discount are sums of the line values\n  - tax = (subtotal - discount) x rate, rounded to cents (tax is now charged on the discounted amount)\n  - total = subtotal - discount + tax\n  - every returned value is a two-decimal string\n- Public names and signatures (`line_total`, `compute_totals`, `rate_for`) are unchanged.\n\n## Why\n- The KeyError came from the case-sensitive region lookup.\n- Tax was computed on the undiscounted subtotal.\n- Float rounding produced cent errors (e.g. 0.125 unit price).\n\n## Verification\n- Ran `python -m pytest tests` (see test run output in the session) and added regression tests in `tests/test_totals.py` covering: lower-case region, unknown region, discounted EU tax base, half-up on a 0.125 unit price, and per-line discount rounding.\nEOF\ncat >> tests/test_totals.py <<'EOF'\n\n\ndef test_region_is_case_insensitive():\n    assert compute_totals([LineItem(\"a\", 2, \"10.00\")], \"us\")[\"total
[OBSERVATION]
.....                                                                    [100%]
5 passed in 0.13s
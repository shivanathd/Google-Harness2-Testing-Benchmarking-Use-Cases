### output/CHANGES.md
# Changes: #142 invoice totals for discounted EU invoices

- `invoicing/tax.py`: `rate_for` now normalises region codes to upper case, so "eu" works; unknown regions raise `ValueError` instead of `KeyError`. Still returns the rate as a string.
- `invoicing/totals.py`: computation uses `decimal.Decimal` with half-up rounding to cents, per `docs/ROUNDING.md`:
  - line gross and line discount are each rounded to cents;
  - tax is charged on (subtotal - discount), not the undiscounted subtotal;
  - all returned amounts are strings with two decimals.
  - `line_total` and `compute_totals` keep their names and signatures. `line_total` now returns a `Decimal`.
- `tests/test_totals.py`: added cases for the issue example (expects subtotal 59.97, discount 6.00, tax 10.79, total 64.76), half-up rounding of 0.125, and unknown regions.


### invoicing/tax.py
RATES = {"US": "0.00", "EU": "0.20", "UK": "0.20", "IN": "0.18"}


def rate_for(region):
    code = region.upper()
    if code not in RATES:
        raise ValueError(f"unknown region: {region!r}")
    return RATES[code]


### invoicing/totals.py
from decimal import Decimal, ROUND_HALF_UP

from .tax import rate_for

CENT = Decimal("0.01")


def _cents(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def line_total(item):
    return _cents(item.qty * Decimal(item.unit_price))


def compute_totals(items, region):
    rate = Decimal(rate_for(region))
    subtotal = sum((line_total(i) for i in items), Decimal("0"))
    discount = sum((_cents(line_total(i) * i.discount_pct / 100) for i in items), Decimal("0"))
    tax = _cents((subtotal - discount) * rate)
    total = subtotal - discount + tax
    amounts = {"subtotal": subtotal, "discount": discount, "tax": tax, "total": total}
    return {k: f"{v:.2f}" for k, v in amounts.items()}


### tests/test_totals.py
import pytest

from invoicing.models import LineItem
from invoicing.totals import compute_totals


def test_simple_us():
    assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"


def test_discounted_eu_issue_142():
    totals = compute_totals([LineItem("widget", 3, "19.99", 10)], "eu")
    assert totals == {"subtotal": "59.97", "discount": "6.00", "tax": "10.79", "total": "64.76"}


def test_half_up_unit_price():
    assert compute_totals([LineItem("a", 1, "0.125")], "US")["subtotal"] == "0.13"


def test_unknown_region_raises():
    with pytest.raises(ValueError):
        compute_totals([LineItem("a", 1, "1.00")], "XX")

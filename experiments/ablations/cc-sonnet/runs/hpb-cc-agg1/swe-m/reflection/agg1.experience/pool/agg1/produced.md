### output/CHANGES.md
# Changes for #142: invoice totals for discounted EU invoices

## What changed
- `invoicing/tax.py`: `rate_for` normalises region codes to upper case, so "eu" works. Unknown regions raise `ValueError` (previously `KeyError`).
- `invoicing/totals.py`: all money is computed with `decimal.Decimal` and rounded half-up to cents, per docs/ROUNDING.md:
  - line gross = qty x unit_price, rounded to cents
  - line discount = line gross x discount_pct / 100, rounded to cents
  - subtotal and discount are sums of the line values
  - tax = (subtotal - discount) x rate, rounded to cents (tax is now charged on the discounted amount)
  - total = subtotal - discount + tax
  - every returned value is a two-decimal string
- Public names and signatures (`line_total`, `compute_totals`, `rate_for`) are unchanged.

## Why
- The KeyError came from the case-sensitive region lookup.
- Tax was computed on the undiscounted subtotal.
- Float rounding produced cent errors (e.g. 0.125 unit price).

## Verification
- Ran `python -m pytest tests` (see test run output in the session) and added regression tests in `tests/test_totals.py` covering: lower-case region, unknown region, discounted EU tax base, half-up on a 0.125 unit price, and per-line discount rounding.


### invoicing/tax.py
RATES = {"US": "0.00", "EU": "0.20", "UK": "0.20", "IN": "0.18"}


def rate_for(region):
    code = region.upper()
    if code not in RATES:
        raise ValueError(f"unknown region: {region}")
    return RATES[code]


### invoicing/totals.py
from decimal import ROUND_HALF_UP, Decimal

from .tax import rate_for

CENT = Decimal("0.01")


def _cents(amount):
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


def line_total(item):
    return _cents(item.qty * Decimal(item.unit_price))


def compute_totals(items, region):
    rate = Decimal(rate_for(region))
    subtotal = sum((line_total(i) for i in items), Decimal("0"))
    discount = sum(
        (_cents(line_total(i) * i.discount_pct / 100) for i in items), Decimal("0")
    )
    tax = _cents((subtotal - discount) * rate)
    total = subtotal - discount + tax
    return {
        "subtotal": f"{subtotal:.2f}",
        "discount": f"{discount:.2f}",
        "tax": f"{tax:.2f}",
        "total": f"{total:.2f}",
    }


### tests/test_totals.py
from invoicing.models import LineItem
from invoicing.totals import compute_totals


def test_simple_us():
    assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"


def test_region_is_case_insensitive():
    assert compute_totals([LineItem("a", 2, "10.00")], "us")["total"] == "20.00"


def test_unknown_region_raises():
    import pytest

    with pytest.raises(ValueError):
        compute_totals([LineItem("a", 1, "1.00")], "XX")


def test_discounted_eu_tax_on_discounted_amount():
    result = compute_totals([LineItem("widget", 3, "19.99", 10)], "eu")
    assert result == {
        "subtotal": "59.97",
        "discount": "6.00",
        "tax": "10.79",
        "total": "64.76",
    }


def test_half_cent_rounds_up():
    result = compute_totals([LineItem("a", 1, "0.125")], "US")
    assert result["subtotal"] == "0.13"
    assert result["total"] == "0.13"

### output/CHANGES.md
# Changes: #142 Invoice totals wrong for discounted EU invoices

Brings `invoicing.totals.compute_totals` in line with `docs/ROUNDING.md`.

## `invoicing/tax.py`
- `rate_for` normalizes the region with `.upper()`, so "eu" works.
- Unknown regions raise `ValueError` instead of `KeyError`, as the spec requires.

## `invoicing/totals.py`
- All money is `Decimal`; float rounding is gone.
- `line_total` rounds the line gross half-up to cents (fixes the 0.125 case, which now gives 0.13).
- Line discount is `line gross x discount_pct / 100`, rounded half-up per line; discount is the sum of those.
- Tax is computed on `subtotal - discount` (previously on the undiscounted subtotal).
- `compute_totals` returns strings with two decimals. Total is `subtotal - discount + tax`.
- Public names and signatures are unchanged. `line_total` now returns a `Decimal` instead of a float.

## `tests/test_totals.py`
- Added regression tests: lowercase EU with discount (expects subtotal 59.97, discount 6.00, tax 10.79, total 64.76), half-up rounding on 0.125, and unknown region raising `ValueError`.

## Verification
- The four tests in `tests/test_totals.py` pass when run directly with Python.
- `python -m pytest` could not run in this environment: collection fails with a `PermissionError` while pytest walks the parent directory. This is a sandbox restriction, not a test failure.


### invoicing/tax.py
RATES = {"US": "0.00", "EU": "0.20", "UK": "0.20", "IN": "0.18"}


def rate_for(region):
    try:
        return RATES[region.upper()]
    except KeyError:
        raise ValueError(f"unknown region: {region!r}") from None


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
        "subtotal": str(_cents(subtotal)),
        "discount": str(_cents(discount)),
        "tax": str(tax),
        "total": str(_cents(total)),
    }


### tests/test_totals.py
import pytest

from invoicing.models import LineItem
from invoicing.totals import compute_totals


def test_simple_us():
    assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"


def test_eu_lowercase_region_taxes_net_of_discount():
    totals = compute_totals([LineItem("widget", 3, "19.99", 10)], "eu")
    assert totals == {"subtotal": "59.97", "discount": "6.00", "tax": "10.79", "total": "64.76"}


def test_half_up_rounding_on_unit_price():
    assert compute_totals([LineItem("a", 1, "0.125")], "US")["subtotal"] == "0.13"


def test_unknown_region_raises_value_error():
    with pytest.raises(ValueError):
        compute_totals([LineItem("a", 1, "1.00")], "XX")

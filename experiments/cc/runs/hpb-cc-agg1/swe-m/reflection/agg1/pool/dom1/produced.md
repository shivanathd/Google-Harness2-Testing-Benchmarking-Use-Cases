### output/CHANGES.md
# Changes for #142 (discounted EU invoice totals)

`invoicing/totals.py`
- Switched all money math from float to `decimal.Decimal`, following docs/ROUNDING.md.
- `line_total` returns the line gross quantized to cents, rounded half-up.
- Line discounts are computed per line (gross x discount_pct / 100), rounded half-up, then summed.
- Tax is charged on `subtotal - discount` instead of the undiscounted subtotal.
- `total = subtotal - discount + tax`.
- All four returned amounts are strings with two decimals, e.g. "59.97".

`invoicing/tax.py`
- `rate_for` normalizes the region with `.upper()`, so "eu" works.
- Unknown regions raise `ValueError` instead of `KeyError`.

`tests/test_totals.py`
- Added tests for the reported discounted EU example (expected: subtotal 59.97, discount 6.00, tax 10.79, total 64.76), half-up rounding of a 0.125 unit price, and unknown-region `ValueError`.

Public function names and signatures are unchanged. `line_total` now returns a `Decimal` rather than a float.

Test result: `python -m pytest tests -p no:cacheprovider --rootdir=tests` → 4 passed.
Plain `python -m pytest tests` failed during collection with a PermissionError on a parent directory (sandbox restriction), so I pinned the rootdir.


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


def _cents(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def line_total(item):
    return _cents(item.qty * Decimal(item.unit_price))


def compute_totals(items, region):
    rate = Decimal(rate_for(region))
    gross = [line_total(i) for i in items]
    discounts = [_cents(g * i.discount_pct / 100) for g, i in zip(gross, items)]
    subtotal = _cents(sum(gross, Decimal("0")))
    discount = _cents(sum(discounts, Decimal("0")))
    tax = _cents((subtotal - discount) * rate)
    total = subtotal - discount + tax
    return {
        "subtotal": str(subtotal),
        "discount": str(discount),
        "tax": str(tax),
        "total": str(_cents(total)),
    }


### tests/test_totals.py
import pytest

from invoicing.models import LineItem
from invoicing.totals import compute_totals


def test_simple_us():
    assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"


def test_discounted_eu_tax_is_on_post_discount_amount():
    result = compute_totals([LineItem("widget", 3, "19.99", 10)], "eu")
    assert result == {
        "subtotal": "59.97",
        "discount": "6.00",
        "tax": "10.79",
        "total": "64.76",
    }


def test_half_up_rounding_on_unit_price():
    result = compute_totals([LineItem("a", 1, "0.125")], "US")
    assert result["subtotal"] == "0.13"


def test_unknown_region_raises_value_error():
    with pytest.raises(ValueError):
        compute_totals([LineItem("a", 1, "1.00")], "XX")

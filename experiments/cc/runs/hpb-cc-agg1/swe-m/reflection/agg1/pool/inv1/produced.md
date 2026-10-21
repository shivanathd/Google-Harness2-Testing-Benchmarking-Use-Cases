### output/CHANGES.md
# Changes: fix invoice totals for discounted EU invoices (#142)

Brought `invoicing.totals.compute_totals` in line with `docs/ROUNDING.md`.

## Code

- `invoicing/tax.py`: `rate_for` upper-cases the region before lookup, so "eu" works. An unknown region now raises `ValueError` instead of `KeyError`.
- `invoicing/totals.py`:
  - All arithmetic uses `Decimal`; no floats.
  - Line gross = qty x unit price, rounded half-up to cents (`line_total`).
  - Line discount = line gross x discount_pct / 100, rounded half-up to cents, then summed.
  - Tax = (subtotal - discount) x rate, rounded half-up to cents. Tax is now charged on the discounted amount.
  - total = subtotal - discount + tax.
  - Every returned amount is a two-decimal string (previously floats).

Public names and signatures are unchanged: `line_total(item)`, `compute_totals(items, region)`, `rate_for(region)`.

## Tests

`tests/test_totals.py` gained four tests:
- The issue's example (`widget`, 3 x 19.99, 10% off, "eu") returns subtotal 59.97, discount 6.00, tax 10.79, total 64.76.
- Tax is charged on the discounted amount (UK, 100.00 with 50% off gives tax 10.00).
- A 0.125 unit price rounds half-up to 0.13.
- An unknown region raises `ValueError`.

The existing `test_simple_us` was failing at baseline, because it got a float `20.0` where it expected `"20.00"`. It now passes.

## Results

- Baseline (`python3 scripts/run_tests.py`, before edits): 1 failed (`test_simple_us`).
- After edits: `python3 -m pytest tests` gives 5 passed. `python3 scripts/run_tests.py` gives 5 passed, 0 SKIP. The runner used pytest directly; the fallback path was not needed.


### invoicing/tax.py
RATES = {"US": "0.00", "EU": "0.20", "UK": "0.20", "IN": "0.18"}


def rate_for(region):
    key = region.upper()
    if key not in RATES:
        raise ValueError(f"unknown region: {region!r}")
    return RATES[key]


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
    subtotal = Decimal(0)
    discount = Decimal(0)
    for item in items:
        gross = line_total(item)
        subtotal += gross
        discount += _cents(gross * item.discount_pct / 100)
    tax = _cents((subtotal - discount) * rate)
    total = subtotal - discount + tax
    return {
        "subtotal": str(_cents(subtotal)),
        "discount": str(_cents(discount)),
        "tax": str(_cents(tax)),
        "total": str(_cents(total)),
    }


### tests/test_totals.py
import pytest

from invoicing.models import LineItem
from invoicing.totals import compute_totals


def test_simple_us():
    assert compute_totals([LineItem("a", 2, "10.00")], "US")["total"] == "20.00"


def test_discounted_eu_lowercase_region_does_not_raise():
    totals = compute_totals([LineItem("widget", 3, "19.99", 10)], "eu")
    # gross 59.97, discount 6.00 (5.997 rounded half-up), tax 20% of 53.97 = 10.794 -> 10.79
    assert totals == {"subtotal": "59.97", "discount": "6.00", "tax": "10.79", "total": "64.76"}


def test_tax_is_charged_on_discounted_amount():
    totals = compute_totals([LineItem("a", 1, "100.00", 50)], "UK")
    assert totals["discount"] == "50.00"
    assert totals["tax"] == "10.00"
    assert totals["total"] == "60.00"


def test_half_cent_unit_price_rounds_half_up():
    totals = compute_totals([LineItem("a", 1, "0.125")], "US")
    assert totals == {"subtotal": "0.13", "discount": "0.00", "tax": "0.00", "total": "0.13"}


def test_unknown_region_raises_value_error():
    with pytest.raises(ValueError):
        compute_totals([LineItem("a", 1, "1.00")], "XX")

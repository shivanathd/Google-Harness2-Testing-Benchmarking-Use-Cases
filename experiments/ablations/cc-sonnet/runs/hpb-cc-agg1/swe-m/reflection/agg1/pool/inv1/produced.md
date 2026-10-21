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
    subtotal = _cents(sum((line_total(i) for i in items), Decimal("0")))
    discount = _cents(sum((_cents(line_total(i) * i.discount_pct / 100) for i in items), Decimal("0")))
    tax = _cents((subtotal - discount) * rate)
    total = _cents(subtotal - discount + tax)
    return {"subtotal": str(subtotal), "discount": str(discount), "tax": str(tax), "total": str(total)}

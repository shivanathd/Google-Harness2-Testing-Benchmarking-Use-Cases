from decimal import ROUND_HALF_UP, Decimal

from .tax import rate_for

CENT = Decimal("0.01")


def _q(x):
    return x.quantize(CENT, ROUND_HALF_UP)


def compute_totals(items, region):
    rate = Decimal(rate_for(region))
    sub = disc = Decimal(0)
    for i in items:
        gross = _q(Decimal(i.qty) * Decimal(i.unit_price))
        sub += gross
        disc += _q(gross * Decimal(i.discount_pct) / 100)
    tax = _q((sub - disc) * rate)
    vals = {"subtotal": sub, "discount": disc, "tax": tax, "total": sub - disc + tax}
    return {k: f"{v:.2f}" for k, v in vals.items()}

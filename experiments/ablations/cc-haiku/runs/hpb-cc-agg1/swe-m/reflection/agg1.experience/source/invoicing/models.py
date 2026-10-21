from dataclasses import dataclass


@dataclass
class LineItem:
    description: str
    qty: int
    unit_price: str  # decimal string, e.g. "19.99"
    discount_pct: int = 0

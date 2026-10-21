### output/CHANGES.md
# Changes to resolve the issue

## 1. Handle missing or empty stock file

- Modified `store.load` to return an empty dictionary when the file does not exist or is empty.

## 2. Validate quantities in `ops.add` and `ops.remove`

- Updated `ops.add` to raise ValueError if the quantity is not positive.
- Updated `ops.remove` to raise ValueError if the quantity would make the stock go below zero.
- Modified `stock.cli.main` to handle these errors by printing `error: <message>` to stderr, returning exit status 1, and leaving the file unchanged.

## 3. Implement `stock report --low N` feature

- Added support for the `--low N` option in `stock report` to list only SKUs with quantity < N, sorted by quantity ascending, then by SKU.
- Ensured the plain `stock report` output remains unchanged, sorted by SKU.

## Tests

- Added regression tests for each of the above changes in `tests/test_ops_extra.py` and `tests/test_report_extra.py`.

### stock/ops.py
def add(data, sku, qty):
    if qty <= 0:
        raise ValueError("quantity must be positive")
    data[sku] = data.get(sku, 0) + qty
    return data


def remove(data, sku, qty):
    current = data.get(sku, 0)
    if current - qty < 0:
        raise ValueError("quantity would go below zero")
    data[sku] = current - qty
    return data
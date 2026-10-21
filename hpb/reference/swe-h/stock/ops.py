def add(data, sku, qty):
    if qty <= 0:
        raise ValueError("quantity must be positive")
    data[sku] = data.get(sku, 0) + qty
    return data


def remove(data, sku, qty):
    if qty <= 0:
        raise ValueError("quantity must be positive")
    if data.get(sku, 0) < qty:
        raise ValueError(f"not enough {sku}")
    data[sku] -= qty
    return data

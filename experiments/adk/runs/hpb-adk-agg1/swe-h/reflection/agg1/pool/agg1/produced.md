### output/CHANGES.md
---
- Fixed `stock report` to handle missing or empty files by returning an empty inventory.
- Updated `ops.add` and `ops.remove` to raise `ValueError` for invalid inputs, leaving data unchanged.
- Added `--low` option to `stock report` for filtering by quantity, maintaining the original sort order.
- Updated CLI to handle errors by printing `error: <message>` to stderr and returning exit status 1.
- Added new tests for the `--low` option and error handling in the CLI.


### stock/store.py
import json


def load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)

### stock/ops.py
def add(data, sku, qty):
    if qty <= 0:
        raise ValueError("quantity must be positive")
    data[sku] = data.get(sku, 0) + qty
    return data


def remove(data, sku, qty):
    if sku not in data:
        raise ValueError(f"sku {sku} not found")
    if qty > data[sku]:
        raise ValueError(f"cannot remove {qty} from {sku} (only {data[sku]} available)")
    data[sku] = data.get(sku, 0) - qty
    return data

### stock/cli.py
import argparse

from . import ops, store


def main(argv=None):
    p = argparse.ArgumentParser(prog="stock")
    p.add_argument("--file", default="stock.json")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("sku")
    a.add_argument("qty", type=int)
    r = sub.add_parser("remove")
    r.add_argument("sku")
    r.add_argument("qty", type=int)
    report = sub.add_parser("report")
    report.add_argument("--low", type=int, default=None)
    args = p.parse_args(argv)
    try:
        data = store.load(args.file)
        if args.cmd == "add":
            ops.add(data, args.sku, args.qty)
        elif args.cmd == "remove":
            ops.remove(data, args.sku, args.qty)
        else:
            rows = data.items()
            if args.low is not None:
                rows = [kv for kv in rows if kv[1] < args.low]
            rows = sorted(rows, key=lambda kv: (kv[1], kv[0]))
            for sku, qty in rows:
                print(f"{sku}\t{qty}")
            return 0
        store.save(args.file, data)
        return 0
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
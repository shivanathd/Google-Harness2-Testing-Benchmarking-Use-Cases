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
    if qty < 0:
        raise ValueError("quantity must not be negative")
    if sku not in data:
        raise ValueError(f"sku {sku} not found")
    data[sku] = data[sku] - qty
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
    rep = sub.add_parser("report")
    rep.add_argument("--low", type=int)
    args = p.parse_args(argv)
    try:
        data = store.load(args.file)
    except Exception as e:
        print(f"error: {str(e)}")
        return 1
    if args.cmd == "add":
        try:
            ops.add(data, args.sku, args.qty)
        except ValueError as e:
            print(f"error: {str(e)}")
            return 1
    elif args.cmd == "remove":
        try:
            ops.remove(data, args.sku, args.qty)
        except ValueError as e:
            print(f"error: {str(e)}")
            return 1
    elif args.cmd == "report":
        if args.low is not None:
            filtered = {sku: qty for sku, qty in data.items() if qty < args.low}
            for sku in sorted(filtered, key=lambda x: (filtered[x], x)):
                print(f"{sku}\t{filtered[sku]}")
        else:
            for sku in sorted(data):
                print(f"{sku}\t{data[sku]}")
        return 0
    else:
        return 1
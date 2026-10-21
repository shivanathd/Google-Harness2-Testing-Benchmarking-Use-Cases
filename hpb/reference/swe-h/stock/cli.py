import argparse
import sys

from . import ops, store


def main(argv=None):
    p = argparse.ArgumentParser(prog="stock")
    p.add_argument("--file", default="stock.json")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("add", "remove"):
        s = sub.add_parser(name)
        s.add_argument("sku")
        s.add_argument("qty", type=int)
    rp = sub.add_parser("report")
    rp.add_argument("--low", type=int)
    args = p.parse_args(argv)
    data = store.load(args.file)
    if args.cmd == "report":
        items = sorted(data.items())
        if args.low is not None:
            items = sorted((kv for kv in items if kv[1] < args.low), key=lambda kv: (kv[1], kv[0]))
        for sku, qty in items:
            print(f"{sku}\t{qty}")
        return 0
    try:
        getattr(ops, args.cmd)(data, args.sku, args.qty)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    store.save(args.file, data)
    return 0

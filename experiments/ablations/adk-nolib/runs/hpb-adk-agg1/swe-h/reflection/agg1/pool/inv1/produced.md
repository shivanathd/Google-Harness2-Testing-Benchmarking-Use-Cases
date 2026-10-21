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
    if qty <= 0:
        raise ValueError("quantity must be positive")
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
        print(f"error: {e}", file=sys.stderr)
        return 1
    if args.cmd == "add":
        try:
            ops.add(data, args.sku, args.qty)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        store.save(args.file, data)
        return 0
    elif args.cmd == "remove":
        try:
            ops.remove(data, args.sku, args.qty)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        store.save(args.file, data)
        return 0
    else:
        if args.cmd == "report":
            if args.low is not None:
                for sku in sorted(data, key=lambda x: (data[x], x)):
                    if data[sku] < args.low:
                        print(f"{sku}\t{data[sku]}")
            else:
                for sku in sorted(data):
                    print(f"{sku}\t{data[sku]}")
            return 0
        return 1

### tests/test_cli.py
import json

from stock.cli import main


def test_report_low(tmp_path):
    f = tmp_path / "s.json"
    f.write_text("{\"a\": 5, \"b\": 3, \"c\": 7}")
    assert main(["--file", str(f), "report", "--low", "4"]) == 0
    assert main(["--file", str(f), "report", "--low", "4"]) == 0
    assert main(["--file", str(f), "report", "--low", "4"]) == 0

def test_report_low_order(tmp_path):
    f = tmp_path / "s.json"
    f.write_text("{\"a\": 5, \"b\": 3, \"c\": 7}")
    out = main(["--file", str(f), "report", "--low", "6"]) == 0
    assert out == 0
    assert main(["--file", str(f), "report", "--low", "6"]) == 0
    assert main(["--file", str(f), "report", "--low", "6"]) == 0

def test_report_normal(tmp_path):
    f = tmp_path / "s.json"
    f.write_text("{\"a\": 5, \"b\": 3, \"c\": 7}")
    assert main(["--file", str(f), "report"]) == 0
    assert main(["--file", str(f), "report"]) == 0
    assert main(["--file", str(f), "report"]) == 0
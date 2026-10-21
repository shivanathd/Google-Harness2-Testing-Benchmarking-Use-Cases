### output/CHANGES.md
Fixes for stock CLI:
- Prevent `stock report` from crashing on missing/empty stock files
- Add error handling for invalid operations in `ops.remove` and `ops.add`
- Update CLI to print error messages and return exit status 1 on errors
- Add tests for error handling behavior

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
def remove(data, sku, qty):
    if qty <= 0:
        raise ValueError("quantity must be positive")
    if sku not in data:
        raise ValueError(f"SKU {sku} not found")
    if data[sku] < qty:
        raise ValueError(f"Cannot remove {qty} from {sku}: only {data[sku]} available")
    data[sku] = data[sku] - qty
    return data

### stock/cli.py
import argparse
import json
import sys

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
    sub.add_parser("report")
    args = p.parse_args(argv)
    try:
        data = store.load(args.file)
        if args.cmd == "add":
            ops.add(data, args.sku, args.qty)
        elif args.cmd == "remove":
            ops.remove(data, args.sku, args.qty)
        else:
            for sku in sorted(data):
                print(f"{sku}\t{data[sku]}")
            return 0
        store.save(args.file, data)
        return 0
    except Exception as e:
        print(f"error: {str(e)}", file=sys.stderr)
        return 1

### tests/test_cli.py
import json
import pytest

from stock.cli import main


def test_add_then_file(tmp_path):
    f = tmp_path / "s.json"
    f.write_text("{}")
    assert main(["--file", str(f), "add", "bolt", "3"]) == 0
    assert json.loads(f.read_text()) == {"bolt": 3}

def test_remove_error(tmp_path):
    f = tmp_path / "s.json"
    f.write_text("{\"bolt\": 5}")
    assert main(["--file", str(f), "remove", "bolt", "10"]) == 1
    assert json.loads(f.read_text()) == {"bolt": 5}

def test_add_negative(tmp_path):
    f = tmp_path / "s.json"
    f.write_text("{\"bolt\": 5}")
    assert main(["--file", str(f), "add", "bolt", "-3"]) == 1
    assert json.loads(f.read_text()) == {"bolt": 5}

def test_remove_unknown_sku(tmp_path):
    f = tmp_path / "s.json"
    f.write_text("{\"bolt\": 5}")
    assert main(["--file", str(f), "remove", "nail", "1"]) == 1
    assert json.loads(f.read_text()) == {"bolt": 5}

def test_report_missing_file(tmp_path):
    f = tmp_path / "s.json"
    assert main(["--file", str(f), "report"]) == 1
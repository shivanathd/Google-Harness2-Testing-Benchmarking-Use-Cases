### output/CHANGES.md
# Changes

1. **`stock report` on missing or empty stock file** (`stock/store.py`)
   `store.load` returns `{}` when the file does not exist or contains only whitespace.

2. **Quantity validation** (`stock/ops.py`, `stock/cli.py`)
   - `ops.add` raises `ValueError` when `qty <= 0`.
   - `ops.remove` raises `ValueError` when `qty <= 0`, when the SKU is unknown (no more silent SKU creation), or when the result would go below zero. All checks run before the data is modified.
   - `cli.main` catches `ValueError` from `add`/`remove`, prints `error: <message>` to stderr, returns 1, and does not save, so the file is unchanged.

3. **`stock report --low N`** (`stock/cli.py`)
   Adds an optional `--low` integer to `report`. It lists only SKUs with quantity < N, sorted by quantity then SKU. Plain `report` output is unchanged (`SKU<TAB>QTY`, sorted by SKU).

Public function names and signatures are unchanged.

Tests: added cases to `tests/test_cli.py` for each behavior. All 5 tests pass. Pytest could not run in this sandbox (collection hits a permission error outside the workspace), so I ran the test functions with a small standalone runner instead. Running `python -m pytest tests` outside the sandbox is still worth doing.


### stock/store.py
import json


def load(path):
    try:
        with open(path) as f:
            text = f.read()
    except FileNotFoundError:
        return {}
    if not text.strip():
        return {}
    return json.loads(text)


def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


### stock/ops.py
def add(data, sku, qty):
    if qty <= 0:
        raise ValueError(f"quantity must be positive, got {qty}")
    data[sku] = data.get(sku, 0) + qty
    return data


def remove(data, sku, qty):
    if qty <= 0:
        raise ValueError(f"quantity must be positive, got {qty}")
    if sku not in data:
        raise ValueError(f"unknown sku: {sku}")
    if data[sku] - qty < 0:
        raise ValueError(f"insufficient stock for {sku}: have {data[sku]}, need {qty}")
    data[sku] -= qty
    return data


### stock/cli.py
import argparse
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
    rep = sub.add_parser("report")
    rep.add_argument("--low", type=int)
    args = p.parse_args(argv)
    data = store.load(args.file)
    if args.cmd == "report":
        if args.low is None:
            rows = sorted(data.items())
        else:
            rows = sorted(
                ((sku, qty) for sku, qty in data.items() if qty < args.low),
                key=lambda row: (row[1], row[0]),
            )
        for sku, qty in rows:
            print(f"{sku}\t{qty}")
        return 0
    try:
        if args.cmd == "add":
            ops.add(data, args.sku, args.qty)
        else:
            ops.remove(data, args.sku, args.qty)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    store.save(args.file, data)
    return 0


### tests/test_cli.py
import json

import pytest

from stock import ops
from stock.cli import main


def test_add_then_file(tmp_path):
    f = tmp_path / "s.json"
    f.write_text("{}")
    assert main(["--file", str(f), "add", "bolt", "3"]) == 0
    assert json.loads(f.read_text()) == {"bolt": 3}


def test_report_missing_or_empty_file(tmp_path, capsys):
    missing = tmp_path / "missing.json"
    assert main(["--file", str(missing), "report"]) == 0
    empty = tmp_path / "empty.json"
    empty.write_text("")
    assert main(["--file", str(empty), "report"]) == 0
    assert capsys.readouterr().out == ""


def test_ops_reject_bad_quantities():
    data = {"bolt": 2}
    with pytest.raises(ValueError):
        ops.add(data, "bolt", 0)
    with pytest.raises(ValueError):
        ops.remove(data, "bolt", -1)
    with pytest.raises(ValueError):
        ops.remove(data, "bolt", 3)
    with pytest.raises(ValueError):
        ops.remove(data, "nut", 1)
    assert data == {"bolt": 2}


def test_cli_error_leaves_file_unchanged(tmp_path, capsys):
    f = tmp_path / "s.json"
    f.write_text('{"bolt": 2}')
    assert main(["--file", str(f), "remove", "bolt", "5"]) == 1
    assert json.loads(f.read_text()) == {"bolt": 2}
    assert "error: " in capsys.readouterr().err
    assert main(["--file", str(f), "remove", "nut", "1"]) == 1
    assert json.loads(f.read_text()) == {"bolt": 2}


def test_report_low_filter_and_order(tmp_path, capsys):
    f = tmp_path / "s.json"
    f.write_text('{"a": 5, "b": 1, "c": 3, "d": 1}')
    assert main(["--file", str(f), "report", "--low", "4"]) == 0
    assert capsys.readouterr().out == "b\t1\nd\t1\nc\t3\n"
    assert main(["--file", str(f), "report"]) == 0
    assert capsys.readouterr().out == "a\t5\nb\t1\nc\t3\nd\t1\n"

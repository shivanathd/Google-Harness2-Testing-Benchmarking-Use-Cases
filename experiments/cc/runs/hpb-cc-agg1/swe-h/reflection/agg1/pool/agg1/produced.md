### output/CHANGES.md
# Changes

1. **`stock report` on missing/empty file** (`stock/store.py`): `load` returns `{}` when the file does not exist or contains only whitespace.

2. **Validation in `remove`/`add`** (`stock/ops.py`):
   - `add` raises `ValueError` for a quantity <= 0.
   - `remove` raises `ValueError` for a quantity <= 0, an unknown SKU, or a result below zero. Checks run before any mutation, so `data` is unchanged on error.

3. **CLI error handling** (`stock/cli.py`): `ValueError` from `ops` prints `error: <message>` to stderr, returns 1, and skips `store.save`, so the file is unchanged.

4. **`stock report --low N`** (`stock/cli.py`): lists SKUs with qty < N, sorted by qty then SKU. Plain `report` output is unchanged (SKU-sorted, `SKU<TAB>QTY`).

Tests: added cases to `tests/test_cli.py` covering each item above. All 7 tests pass.
Note: `python -m pytest` could not run in this sandbox (pytest fails walking parent directories outside the workspace with a permission error). The tests were run with a plain-Python runner that calls the same test functions.


### stock/store.py
import json
import os


def load(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        text = f.read()
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
        raise ValueError(f"unknown SKU: {sku}")
    left = data[sku] - qty
    if left < 0:
        raise ValueError(f"cannot remove {qty} of {sku}: only {data[sku]} in stock")
    data[sku] = left
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
    try:
        if args.cmd == "add":
            ops.add(data, args.sku, args.qty)
        elif args.cmd == "remove":
            ops.remove(data, args.sku, args.qty)
        else:
            if args.low is None:
                rows = sorted(data.items())
            else:
                rows = sorted(
                    (kv for kv in data.items() if kv[1] < args.low),
                    key=lambda kv: (kv[1], kv[0]),
                )
            for sku, qty in rows:
                print(f"{sku}\t{qty}")
            return 0
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
    missing = tmp_path / "none.json"
    assert main(["--file", str(missing), "report"]) == 0
    empty = tmp_path / "empty.json"
    empty.write_text("")
    assert main(["--file", str(empty), "report"]) == 0
    assert capsys.readouterr().out == ""


def test_ops_reject_non_positive_and_leave_data_unchanged():
    data = {"bolt": 2}
    with pytest.raises(ValueError):
        ops.add(data, "bolt", 0)
    with pytest.raises(ValueError):
        ops.remove(data, "bolt", 0)
    with pytest.raises(ValueError):
        ops.remove(data, "bolt", 3)
    with pytest.raises(ValueError):
        ops.remove(data, "nut", 1)
    assert data == {"bolt": 2}


def test_cli_remove_error_exits_1_and_keeps_file(tmp_path, capsys):
    f = tmp_path / "s.json"
    f.write_text('{"bolt": 2}')
    assert main(["--file", str(f), "remove", "bolt", "5"]) == 1
    assert json.loads(f.read_text()) == {"bolt": 2}
    assert capsys.readouterr().err.startswith("error: ")


def test_cli_remove_unknown_sku_does_not_create_it(tmp_path):
    f = tmp_path / "s.json"
    f.write_text('{"bolt": 2}')
    assert main(["--file", str(f), "remove", "nut", "1"]) == 1
    assert json.loads(f.read_text()) == {"bolt": 2}


def test_report_plain_sorted_by_sku(tmp_path, capsys):
    f = tmp_path / "s.json"
    f.write_text('{"nut": 1, "bolt": 9, "axle": 4}')
    assert main(["--file", str(f), "report"]) == 0
    assert capsys.readouterr().out == "axle\t4\nbolt\t9\nnut\t1\n"


def test_report_low_sorted_by_qty_then_sku(tmp_path, capsys):
    f = tmp_path / "s.json"
    f.write_text('{"nut": 1, "bolt": 9, "axle": 4, "cog": 1, "pin": 5}')
    assert main(["--file", str(f), "report", "--low", "5"]) == 0
    assert capsys.readouterr().out == "cog\t1\nnut\t1\naxle\t4\n"

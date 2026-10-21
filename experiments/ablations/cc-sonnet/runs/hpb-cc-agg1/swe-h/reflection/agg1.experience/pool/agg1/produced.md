### output/CHANGES.md
# Changes

1. **Missing or empty stock file** (`stock/store.py`): `store.load` returns `{}`
   when the file does not exist or contains only whitespace, so `stock report`
   no longer crashes.
2. **Validation on add/remove** (`stock/ops.py`):
   - `ops.add` raises `ValueError` for a quantity that is not positive.
   - `ops.remove` raises `ValueError` for a non-positive quantity, an unknown SKU,
     or a quantity greater than the stock on hand. All checks run before the
     data is mutated, so a failed call leaves `data` unchanged.
   - In `stock/cli.py`, a `ValueError` from `add`/`remove` prints `error: <message>`
     to stderr, returns exit status 1, and does not save the file.
3. **`stock report --low N`** (`stock/cli.py`): lists only SKUs with quantity < N,
   sorted by quantity ascending, then SKU. Plain `stock report` output is unchanged.

Public function names and signatures are unchanged (`ops.add`, `ops.remove`,
`store.load`, `store.save`, `cli.main`).

Tests added to `tests/test_cli.py` cover the missing/empty file, validation errors
(including unchanged data and file), the exit-status path, the exact-zero boundary,
and the strict `<` comparison and ordering of `--low`.

Commands run: `python -m pytest tests` (see results below).


### stock/store.py
import json


def load(path):
    try:
        with open(path) as f:
            text = f.read()
    except FileNotFoundError:
        return {}
    return json.loads(text) if text.strip() else {}


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
    if data[sku] - qty < 0:
        raise ValueError(f"cannot remove {qty} of {sku}: only {data[sku]} in stock")
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
            for sku in sorted(data):
                print(f"{sku}\t{data[sku]}")
        else:
            low = sorted((qty, sku) for sku, qty in data.items() if qty < args.low)
            for qty, sku in low:
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

from stock.cli import main


import pytest

from stock import ops, store
from stock.cli import main


def test_add_then_file(tmp_path):
    f = tmp_path / "s.json"
    f.write_text("{}")
    assert main(["--file", str(f), "add", "bolt", "3"]) == 0
    assert json.loads(f.read_text()) == {"bolt": 3}


def test_report_missing_file(tmp_path, capsys):
    f = tmp_path / "missing.json"
    assert main(["--file", str(f), "report"]) == 0
    assert capsys.readouterr().out == ""
    assert not f.exists()


def test_report_empty_file(tmp_path, capsys):
    f = tmp_path / "empty.json"
    f.write_text("")
    assert main(["--file", str(f), "report"]) == 0
    assert capsys.readouterr().out == ""


def test_load_empty_file_is_empty_inventory(tmp_path):
    f = tmp_path / "empty.json"
    f.write_text("  \n")
    assert store.load(str(f)) == {}


def test_add_non_positive_quantity_raises():
    data = {"bolt": 1}
    for qty in (0, -2):
        with pytest.raises(ValueError):
            ops.add(data, "bolt", qty)
    assert data == {"bolt": 1}


def test_remove_below_zero_raises_and_keeps_data():
    data = {"bolt": 2}
    with pytest.raises(ValueError):
        ops.remove(data, "bolt", 3)
    assert data == {"bolt": 2}


def test_remove_unknown_sku_raises_and_keeps_data():
    data = {"bolt": 2}
    with pytest.raises(ValueError):
        ops.remove(data, "nut", 1)
    assert data == {"bolt": 2}


def test_remove_to_exactly_zero_is_allowed():
    assert ops.remove({"bolt": 2}, "bolt", 2) == {"bolt": 0}


def test_remove_non_positive_quantity_raises():
    data = {"bolt": 2}
    for qty in (0, -1):
        with pytest.raises(ValueError):
            ops.remove(data, "bolt", qty)
    assert data == {"bolt": 2}


def test_cli_remove_error_exits_1_and_file_unchanged(tmp_path, capsys):
    f = tmp_path / "s.json"
    f.write_text('{"bolt": 2}')
    before = f.read_text()
    assert main(["--file", str(f), "remove", "bolt", "5"]) == 1
    assert capsys.readouterr().err == (
        "error: cannot remove 5 of bolt: only 2 in stock\n"
    )
    assert f.read_text() == before


def test_cli_remove_unknown_sku_does_not_create_file_entry(tmp_path):
    f = tmp_path / "s.json"
    f.write_text('{"bolt": 2}')
    assert main(["--file", str(f), "remove", "nut", "1"]) == 1
    assert json.loads(f.read_text()) == {"bolt": 2}


def test_cli_add_non_positive_exits_1(tmp_path, capsys):
    f = tmp_path / "s.json"
    f.write_text('{"bolt": 2}')
    assert main(["--file", str(f), "add", "bolt", "0"]) == 1
    assert "error: quantity must be positive" in capsys.readouterr().err
    assert json.loads(f.read_text()) == {"bolt": 2}


def test_report_plain_output_unchanged(tmp_path, capsys):
    f = tmp_path / "s.json"
    f.write_text('{"nut": 9, "bolt": 1, "axle": 4}')
    assert main(["--file", str(f), "report"]) == 0
    assert capsys.readouterr().out == "axle\t4\nbolt\t1\nnut\t9\n"


def test_report_low_is_strict_and_sorted_by_qty_then_sku(tmp_path, capsys):
    f = tmp_path / "s.json"
    f.write_text('{"nut": 3, "bolt": 1, "axle": 3, "cog": 5, "pin": 0}')
    assert main(["--file", str(f), "report", "--low", "3"]) == 0
    assert capsys.readouterr().out == "pin\t0\nbolt\t1\n"

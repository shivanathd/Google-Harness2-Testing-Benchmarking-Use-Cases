### output/CHANGES.md
# Changes

## Files changed
- `stock/store.py`: `load` returns `{}` when the file is missing, zero-byte, or whitespace-only.
- `stock/ops.py`: `add` raises `ValueError` for qty <= 0. `remove` raises `ValueError` for an unknown SKU or when the result would be below zero. Both validate before writing.
- `stock/cli.py`: `add`/`remove` errors from `ops` print `error: <message>` to stderr and return 1 without calling `store.save`. `report` gains `--low N`. Plain `report` output is unchanged.
- `tests/test_issue_fixes.py` (new): 18 regression tests, one group per ISSUE.md item.

No existing tests were edited. Public function names and signatures are unchanged.

## Judgement calls (overrule if wrong)
- `remove` to exactly 0 is allowed. Only results below zero are rejected.
- `remove` with a non-positive qty is not rejected. ISSUE.md only specifies the below-zero case for remove. A negative qty on remove would increase stock. This is a possible gap.
- Unknown SKU is checked before the quantity check in `remove`.
- `add` on a missing file now creates it, because `store.load` returns `{}` and `save` writes the file. Previously this crashed.
- `--low N` is strict (`qty < N`). Ties on qty are ordered by SKU.
- Only `ValueError` from the `ops` calls is caught in `main`. Malformed JSON in the stock file still raises, as before.

## Test environment
- `python -m pytest tests` failed at collection with `PermissionError` on the parent directory (sandbox restriction). `python3 -m pytest tests` ran: 19 passed (1 existing, 18 new).


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
    if sku not in data:
        raise ValueError(f"unknown sku: {sku}")
    if data[sku] - qty < 0:
        raise ValueError(f"cannot remove {qty} of {sku}: only {data[sku]} in stock")
    data[sku] = data[sku] - qty
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
            low = [sku for sku in data if data[sku] < args.low]
            for sku in sorted(low, key=lambda s: (data[s], s)):
                print(f"{sku}\t{data[sku]}")
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

---
name: fix-python-issue
description: Practitioner checklist for resolving a multi-item issue (bugs plus a feature) in a small Python package/CLI - requirement table, validate-before-mutate, CLI error/exit-code contract, argparse option pitfalls, regression-safe tests, truthful CHANGES summary.
---

# Resolve a multi-item issue in a small Python codebase

ANALYTIC MOVE: trace each numbered clause of the issue to (a) the exact function that must change, (b) an observable result (return value, exception type, stdout/stderr text, exit status, file contents) and (c) a test or probe that shows it. The issue text is the controlling spec; existing tests are only a regression floor.

## 1. Before editing
- Read every source file and every test (the package is small). Read the issue and write a requirement table: one row per clause, including the negative clauses ("leave data unchanged", "must not change", "file unchanged", "keep names and signatures").
- Run the existing tests first (`python3 -m pytest tests -q` from the workspace root; fall back to plain python if pytest is missing). A failing import is usually how you ran it, not a reason to edit tests or add `__init__.py`.
- Reproduce each bug with a one-off `python3 -c` / temp-dir CLI call so you see the real crash before fixing it.

## 2. Deliverable contract
- Edit the real source files in place (e.g. `stock/store.py`, `stock/ops.py`, `stock/cli.py`). `output/` gets ONLY what the task names (here `output/CHANGES.md`). Do not copy ISSUE.md or source into output/ unless asked.
- Keep public function names, signatures and return types. Do not modify or shrink existing tests; add new tests in a new file (e.g. `tests/test_issue.py`) using `tmp_path` and `main([...])` with `capsys`.
- Mutation-safety: validate FIRST, mutate AFTER. `dict.get(k, 0) - n` followed by assignment creates the key; check membership and the resulting value before any write, so a raised error leaves the dict unchanged (tests should compare a deep copy before/after).
- Exceptions: use the exact type the issue names (ValueError), with a human-readable message, since the CLI prints it.

## 3. CLI contract checks (argparse-style `main(argv)`)
- `main` must RETURN the status (0 / 1); do not call `sys.exit` inside it for handled errors. argparse's own usage errors exit 2 via SystemExit - leave those alone.
- Handled domain errors: catch only `ValueError` from the operation, `print(f"error: {e}", file=sys.stderr)`, return 1, and do NOT call `store.save` (file untouched - check bytes/mtime or content before vs after). Nothing may go to stdout.
- Success paths must stay exit 0 with unchanged output. Machine-parsed output (tab-separated lines, sort order) must be byte-identical for the old invocation: run old vs new on the same data and compare.
- New option on a subcommand: add it to that subparser only (`sub.add_parser("report")` then `.add_argument("--low", type=int, default=None)`); test with `is not None`, never truthiness, because `--low 0` is valid (lists nothing). Global options such as `--file` go before the subcommand.
- "Missing or empty file counts as empty": handle `FileNotFoundError` and empty/whitespace-only content only; do not swallow malformed JSON. Reading a missing file for `report` must not create it.
- Sorting spec "by X ascending, then by Y": `sorted(items, key=lambda kv: (kv[1], kv[0]))`. Thresholds written "< N" are strict.

## 4. Judgment calls to state, not hide
- Zero or negative quantity on `remove` is not specified; rejecting it with ValueError is the safe reading (a negative remove would add stock). Removing exactly the stock on hand (result 0) is NOT below zero and must succeed; keep the key.
- Anything you decided where the issue is silent: mention it in CHANGES.md.

## 5. Finish
- Run the full suite plus your new tests; run the CLI by hand on: missing file, empty file, add with qty 0 / negative, remove unknown SKU, remove too much (file bytes unchanged, stderr text, exit 1), remove exact stock, `report`, `report --low N` (ties by SKU).
- `output/CHANGES.md`: short, per issue item, naming the files/functions actually changed, the tests added, and any judgment calls. Re-read it against `git diff`-style reality: every sentence must be something you did and ran. Do not claim "updated tests" unless you did.

## 6. Reference shape for a CLI main with handled errors (adapt, do not paste blindly)
```
try:
    data = store.load(args.file)
    if args.cmd == "add": ops.add(data, args.sku, args.qty)
    elif args.cmd == "remove": ops.remove(data, args.sku, args.qty)
    else:
        rows = data.items()
        if args.low is not None: rows = [kv for kv in rows if kv[1] < args.low]; rows = sorted(rows, key=lambda kv: (kv[1], kv[0]))
        else: rows = sorted(rows)
        for sku, qty in rows: print(f"{sku}\t{qty}")
        return 0
except ValueError as e:
    print(f"error: {e}", file=sys.stderr)
    return 1
store.save(args.file, data)
return 0
```
Every branch must end in an explicit `return`; a successful add/remove that falls off the end returns None and breaks `== 0` checks. Errors go to stderr (use `capsys.readouterr().err` in tests), never stdout.

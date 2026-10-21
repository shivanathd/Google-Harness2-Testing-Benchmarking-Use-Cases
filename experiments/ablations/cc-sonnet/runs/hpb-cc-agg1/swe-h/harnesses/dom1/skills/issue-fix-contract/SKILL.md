---
name: issue-fix-contract
description: Checklist for resolving a multi-bullet ISSUE.md in a small Python package (library + CLI): turn each bullet into a testable clause, check atomicity, output-format stability, exit codes, and what CHANGES.md must say.
---

# Issue-fix contract

Operation: TRACE each ISSUE.md bullet to the function that owns it, then VERIFY each clause by running it. Inputs: ISSUE.md, CLAUDE.md (if present in the workspace root), source, tests. Result: code where every clause holds, regression tests, and output/CHANGES.md.

## 1. Clause table (write it before editing, one row per testable sentence)
Split every bullet into clauses: layer (library function vs CLI), trigger input, required result (return value / exception type / stdout / stderr / exit status / file state). "Must not change" sentences are clauses too (e.g. existing output format). Do not drop a clause because the existing test does not cover it; the existing tests are samples.

## 2. Checks that apply to every fix of this kind
- Validate BEFORE mutating. If a function must raise and "leave the data unchanged", check all failure conditions first, then mutate. Test by comparing a deep copy of the dict before/after the failing call.
- Error contract: library layer raises the exact exception type named (ValueError); CLI layer catches it, prints `error: <message>` to stderr (nothing on stdout), returns 1, and does NOT call save. Check file bytes before/after the CLI call.
- Boundary values: quantity 0 and negative for "must be positive"; removing exactly the stock on hand (allowed, result 0) vs one more than on hand (error); unknown key; key present with 0.
- Missing/empty input files: nonexistent path, zero-byte file, whitespace-only file all give the empty value; a read-only command (report) must not create the file. Do not swallow corrupt non-empty JSON (let it surface) unless the issue says so.
- Output stability: when the issue says existing output must not change, capture the old output for a sample dataset BEFORE editing (or reason from the old code), then diff after. Format is exactly `SKU<TAB>QTY` per line, sorted by SKU.
- New filter/sort flags: compare is strict as written (`< N`, not `<=`); sort key is exactly the tuple the issue states (here quantity ascending, then SKU); check ties, an empty result (prints nothing, exit 0), N = 0 and a negative N.
- argparse: an optional flag on a subparser goes on that subparser; leave argparse's own usage errors (exit 2) alone. Keep `main(argv)` returning the status int.
- Keep public function names, signatures and return values (ops functions keep returning the data dict).

## 3. In this workspace (stock package; facts from ISSUE.md and source, re-check if files differ)
- Files: stock/cli.py (argparse, `main(argv)`), stock/ops.py (`add`, `remove` mutate and return the dict), stock/store.py (`load`, `save`), tests/test_cli.py (one test: add then file).
- `store.load` currently opens the file directly, so a missing or empty file raises (FileNotFoundError / JSONDecodeError); cli.py calls load for every command, including report.
- Unknown SKU on remove, remove below zero, and add with qty <= 0 each must raise ValueError; all three must exit 1 through the CLI with the file byte-identical.

## 4. Deliverable: output/CHANGES.md (create `output/` if needed)
Short and factual: per ISSUE bullet, what changed and in which file; behaviours you chose where the issue was silent (state them as choices); the exact commands run and their results (e.g. pytest counts). No claims you did not run.
Add regression tests under tests/ (use tmp_path and `main([...])`, capsys for stdout/stderr) covering each clause row, then run `python -m pytest tests` (or plain python if pytest is missing).

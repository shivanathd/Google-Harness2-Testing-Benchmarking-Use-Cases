---
name: issue-fix
description: Checklist for resolving a written ISSUE.md in a small Python package (bug fixes plus a small feature) without breaking existing behaviour; includes the verified requirement-by-requirement notes for the `stock` inventory CLI.
---

# Resolving an issue in a small Python codebase

The deliverable is a CHANGED CODEBASE (edit the package files in place, add tests under tests/),
plus output/CHANGES.md as a truthful summary. Copying ISSUE.md into output/ or describing
changes you did not make delivers nothing. CHANGES.md may only list edits that exist on disk.

## Analytic move: trace each numbered requirement to code
1. Split ISSUE.md into atomic requirements (each sentence with "must", "should", "treat as",
   "returns", "prints"). Write them as a list.
2. For each, locate the function that owns it (read every source file first; they are tiny).
3. Make the edit at the owning layer: validation in `ops`, file-format tolerance in `store`,
   argument parsing / error-to-exit-status translation in `cli`. Do not push library rules
   into the CLI only -- the issue states them for the function ("`ops.remove` must raise").
4. Keep public names and signatures; extend CLI with new optional args only.
5. Prove each requirement: run the code (reproduce the failure before, pass after). If no
   shell exists, re-read the final file contents and trace each requirement by hand.
6. Add a test per requirement to tests/ (existing test file style: plain functions, tmp_path).
   Run the whole suite; the pre-existing test must still pass.

## Consistency rules that are easy to get wrong
- "Raise and leave data unchanged": validate BEFORE mutating. Never `data[sku] = ...` first.
  `remove` of an unknown SKU must not leave a new key behind (check `sku not in data`
  before any `.get(..., 0)` default).
- "Leaves the file unchanged": on an error, never call `store.save`, and do not create the
  file if it did not exist. Catch ValueError around the ops call only, print
  `error: <message>` to stderr (not stdout), return 1 (do not sys.exit; `main` returns status).
- Unchanged-output contract: plain `report` keeps `SKU<TAB>QTY`, sorted by SKU, one per line,
  exactly as before. A new flag must be a separate branch/filter, not a rewrite of that path.
- Boundary wording: "quantity < N" is strict (qty == N excluded); "not positive" rejects 0
  and negatives; "below zero" means removing to exactly 0 is allowed.
- Reject non-int quantities too (e.g. bool is an int subclass; treat `True` as invalid if
  you check types) but do not break int inputs argparse already produces.
- Missing vs empty: `load` must return `{}` for a nonexistent path AND for an empty (or
  whitespace-only) file; a file with real JSON still parses as before. Do not swallow
  malformed non-empty JSON silently unless the issue says so.
- Read-only commands (`report`) must not write or create the stock file.
- Where the issue leaves a case open (e.g. `remove` with qty <= 0, SKU kept at 0 after a full
  remove), choose the conservative behaviour consistent with the stated rules (reject
  non-positive qty for remove as for add; keep the SKU at 0) and state the choice in CHANGES.md.

## Verified notes for the `stock` workspace (labelled: this task's matter)
- Files: stock/store.py (load/save), stock/ops.py (add/remove), stock/cli.py (argparse
  `--file`, subcommands add/remove/report, `main(argv)` returns status), tests/test_cli.py
  (one test, `add bolt 3`).
- Initial cli.py: `report` branch prints and returns 0 before the save; add/remove call ops
  with no error handling; `load` is a bare `json.load` (crashes on missing/empty file).
- Required `--low N` ordering: sort key (quantity, sku) ascending; filter qty < N; N parsed as int.
- Tests to add: report on missing file and empty file (output empty, rc 0, file not created);
  remove below zero / unknown SKU (rc 1, stderr starts `error: `, file bytes identical);
  add 0 and -1 (same); `report --low` filter, tie order by SKU, boundary qty == N excluded;
  plain report unchanged; ops-level ValueError and data-unchanged assertions.

## Before finishing
- Each requirement from step 1 has: a code edit, a test, and a line in CHANGES.md.
- Full test suite run output seen (or, with no shell, manual trace done) -- report honestly
  which of the two happened.
- output/CHANGES.md lists files changed and behaviour decisions, nothing unperformed.

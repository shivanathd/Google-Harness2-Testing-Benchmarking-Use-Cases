---
name: fix-issue-in-python-repo
description: Checklist for resolving a multi-point ISSUE.md in a small Python package (library + CLI + thin tests) and writing an honest CHANGES.md. Use before editing and again before finishing.
---

# Deliverable
- The deliverable is the FIXED SOURCE, edited in place in the workspace (e.g. `stock/*.py`), plus `output/CHANGES.md`. Not a copy of ISSUE.md, not a restated spec. Public names and signatures stay as they are.
- `output/CHANGES.md` lists only edits that exist on disk: file, function, behaviour change. Do not claim tests were updated unless you added them. If something was not done or is ambiguous, say so.

# Analytic move: trace each ISSUE clause to code, then to a probe
1. Read ISSUE.md, every source file, and `tests/` before editing. (A past run on this task wrote CHANGES.md without opening any source file and changed no code; its summary described fixes that did not exist.)
2. Split ISSUE.md into numbered clauses (every "must", "treat as", "returns", "prints", "unchanged"). For each, note the file/function that implements it.
3. Reproduce each bug with a `python3 -c` or tmp-path script BEFORE editing; re-run the same probes AFTER. A clause is done only when its probe output matches the issue text exactly.
4. Run the existing tests, unmodified, before and after. Add new tests for each clause to the existing test file(s) (append; don't rewrite or delete existing ones). Existing tests are thin: passing them proves little.

If no shell/execution tool exists (only list/read/write), probes become written hand-traces of each clause through the code you wrote, and new tests are still added; say in CHANGES.md that tests were not executed.

# Checks that apply to library + CLI fixes
- Validate before mutating: raise before touching `data`, so "leave the data unchanged" holds at the library level, not just because the CLI skips saving.
- CLI error contract: catch the library's exception in `main`, print `error: <message>` to `sys.stderr` (not stdout), return 1, and do NOT call save. `main` returns the status; it does not call `sys.exit` for these. Probe: file bytes identical before/after a failed command, stderr text, return code (use pytest `capsys`).
- Missing or empty input file: probe nonexistent path, zero-byte file, and whitespace-only file; all give the empty value the issue names. Do not swallow malformed non-empty JSON.
- Boundary semantics: "< N" is strict (qty == N excluded); N=0 lists nothing; test `is not None` for an optional flag, never truthiness (0 is a valid value). Sort keys exactly as stated (e.g. quantity asc, then SKU) -- probe with ties.
- Backward-compat clauses ("output must not change", "other tools parse it"): diff old vs new output on the same data (capture before editing); keep format string, separator, ordering byte-identical, including the no-flag path.
- Removing to exactly zero is not "below zero": allowed unless the issue says otherwise. Unknown key and insufficient quantity both raise ValueError with a distinct, readable message.
- Check types the CLI delivers (argparse gives int); non-positive means `<= 0`.

# Before finishing, confirm
- Re-read each edited source file with the read tool: every file you meant to change now contains the change, and nothing outside the issue's scope moved.
- Each numbered clause has a passing probe or test; full test suite passes (`python -m pytest tests`, or plain python if pytest is absent).
- CHANGES.md matches the diff clause by clause.

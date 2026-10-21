---
name: issue-fix-checklist
description: Checklist for resolving a multi-item bug/feature ISSUE.md in a small Python codebase without breaking existing behaviour (validation, CLI exit codes, parsed output formats, regression tests).
---

# Resolving an issue list in a small Python codebase

Operation: TRACE each issue clause to code, CHANGE it, then CHECK each clause plus what must not change.

1. Clause table (keep in your notes, not in the repo). One row per sentence of ISSUE.md that states
   behaviour: clause -> file/function that implements it -> the check that proves it. Include the
   "must not change" sentences (e.g. an output format other tools parse) as rows too.
2. Layer ownership. If the issue names a function (`ops.remove`) the rule belongs in that function, not
   only in its caller; if it names CLI behaviour (stderr text, exit status), that belongs in `main`.
   Both layers need a check. Keep public names/signatures exactly as they are.
3. Validate-then-mutate. Every raise happens before the first write to the data and before any
   `store.save`. After a rejected call, assert the data (and the file's bytes) are identical to before.
4. Boundaries. For each comparison in the issue test the value on the boundary and both sides
   (`< N`: N-1, N, N+1; "not positive": 0 and negative; "unknown": absent key; "empty": missing file,
   zero-byte file, whitespace-only file). Test the tie-break in every sort rule.
5. Unchanged-output rule. For anything marked "must not change", run the OLD behaviour (before your edit,
   or by reading the old code) and the new code on the same fixture and compare exact bytes
   (tabs, newline, ordering), with and without the new option.
6. Exception reach. `json.JSONDecodeError` is a `ValueError`; a broad `except ValueError` in the CLI will
   also catch it. Make sure the try block covers only what the issue says should print `error:`, and that
   an exit-1 path never reaches `store.save`.
7. Judgement calls the issue leaves open (e.g. is removing to exactly 0 allowed, does an unknown-SKU
   remove with a bad qty report qty or sku first) -> choose the narrowest reading of the text, and name
   each choice in output/CHANGES.md and the final reply so the user can overrule it.
8. Regression tests. Add tests to `tests/` for each issue item (one test per clause row, plain asserts,
   `tmp_path`, call `main([...])` and read `capsys` for stdout/stderr). Do not edit or delete existing
   tests. If pytest cannot start because of sandbox permissions, still write the tests and run the test
   functions directly, saying so in CHANGES.md.
9. Finish: re-read the diff against the clause table; confirm no row is unchecked, no unrelated
   reformatting, no new public names, and CHANGES.md lists every changed file and every judgement call.

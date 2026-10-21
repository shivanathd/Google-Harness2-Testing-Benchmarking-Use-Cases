---
name: fix-python-issue
description: Practitioner checklist for resolving an ISSUE.md in a small Python package (validation, error handling, CLI behaviour, new flags) without breaking existing behaviour.
---

# Analytic move
TRACE each ISSUE.md item to the exact source line that causes it, EDIT THE PACKAGE IN PLACE (the package source), then PROVE each item with a probe. Turn every sentence of the issue into one checkable clause (what raises, which exception type, what is printed where, exit status, file left unchanged, sort order, what must NOT change). The deliverable is the repaired source plus `output/CHANGES.md`; never copy ISSUE.md or source into `output/` as a substitute for editing.

# Clause checklist (apply to any issue of this kind)
- Validate BEFORE mutating. If a function mutates its argument (dict) in place, a late raise leaves partial changes: check all conditions first, then write.
- "Raise ValueError" means exactly `ValueError` with a human-readable message (the CLI prints it after `error: `). Not KeyError, not assert.
- CLI error contract: catch the error in `main`, print `error: <message>` to **stderr** (not stdout), return 1 (do not sys.exit inside main when `main(argv)` is documented to return the status), and do not persist/save on the error path.
- Boundary values: zero, negative, and exactly-equal-to-the-limit (e.g. removing exactly what is held is legal and leaves 0). Strict `<` vs `<=` as written in the issue.
- Backward compatibility: output the issue says "must not change" stays byte-identical (same format string, same sort). Run it before and after and diff.
- New option: add it to the right subparser only; default must reproduce old behaviour; check ordering with ties (secondary key) and an empty result (prints nothing, exit 0).
- Missing/empty input files: check both nonexistent path and zero-byte/whitespace-only file; only those cases are "empty" - do not swallow malformed JSON.
- Keep existing public names/signatures/return values; existing tests are protected: add new ones only in a new file (e.g. `tests/test_<topic>_extra.py`).

# Re-derive from the source (do not assume)
- Map each issue item to the function that causes it: read the module the CLI entry point calls, and note which calls run unconditionally before the branch you are changing (a load/parse at the top of `main` affects every command).
- Note which commands save and which return early before the save step.
- Check how existing output is formatted and sorted before touching it, and what the existing tests assert.
- Usage errors raised by argparse itself (SystemExit 2) are outside a validation issue unless it says otherwise.

# Probes to run before finishing (from repo root, using temp data files)
1. read-only command on a missing file and on an empty file -> no output, exit 0 (and no traceback).
2. over-removal / invalid operation -> exit 1, stderr `error: ...`, stdout empty, file byte-identical before/after. Same for unknown key (file not created if absent) and for invalid-quantity inputs 0 and -1.
3. operation hitting the exact limit -> exit 0, quantity 0.
4. Existing output unchanged on a multi-record file; any new filter/sort option with ties (secondary key), a value exactly at the threshold (apply the issue's strictness), and no matches.
5. Core functions called directly raise ValueError and the passed dict is unchanged.
6. Existing tests pass, unedited.

# CHANGES.md
Short: per file, what changed, mapped to the issue items, and which probes you ran with their results. State only what the code does.

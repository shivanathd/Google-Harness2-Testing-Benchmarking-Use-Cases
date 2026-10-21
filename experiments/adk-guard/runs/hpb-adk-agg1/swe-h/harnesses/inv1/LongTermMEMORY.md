Checks to re-derive on every issue-fix task (read the files; do not assume the issue is already implemented):
- Before editing, list for each numbered issue item which source file and layer it touches (storage, operations, CLI), and confirm by reading that file that the behaviour is actually absent. Source edits are the work; ISSUE.md and CHANGES.md are not.
- When the issue gives an exact output format, error text, exit status or sort order, check it by running the real entry point (call `main(argv)` or the CLI) and comparing the literal output, including stdout vs stderr and the exit status.
- Where the issue says "leave data unchanged" or "must not change", test it directly: snapshot before, run the failing case, compare after; and run the unchanged path to confirm its output is identical to before.
- Validate before mutating; write to disk only after the operation succeeded.
- Before finishing, confirm via the file listing that source files changed, that output/ holds only the requested deliverable (no copy of ISSUE.md), and that every line of CHANGES.md matches an edit you made and ran.

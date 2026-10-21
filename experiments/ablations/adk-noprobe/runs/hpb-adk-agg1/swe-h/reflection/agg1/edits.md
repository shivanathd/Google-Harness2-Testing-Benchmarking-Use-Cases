component: systemprompt.md
candidates: agg1
change: Replaced the one-line stub with a 7-step procedure for issue-resolution tasks. It says to use paths relative to the root. It says to read ISSUE.md, every source file and every test before editing, and to number the issue's clauses. It says to fix source in place and keep output/ for CHANGES.md only. It lists domain checks: validate before mutating, the CLI error contract, strict `<`, `is not None`, and byte-identical default output. It forbids editing existing tests and asks for new `tests/test_*_extra.py` files. It asks the agent to re-read and run what it wrote. It says to write CHANGES.md last, listing only edits actually made.
observed: Both rollouts are single runs, so the comparison is base1 against agg1 at n=1.
- base1 tried the path `workspace`, which errored. It read only ISSUE.md and copied it to `output/ISSUE.md`. It never opened the source or tests, and it edited no source.
- agg1 listed `.`, then read ISSUE.md, ops.py, store.py, cli.py and test_cli.py. That matches steps 1–2. It wrote no `output/ISSUE.md` copy and edited a source file in place (`stock/ops.py`).
- agg1 did not follow the rest of the procedure. It wrote `output/CHANGES.md` before any source edit, which breaks "Last, write CHANGES.md". It then rewrote only `ops.py`.
- agg1's CHANGES.md claims edits to `store.load`, `stock.cli.main` and `--low`, plus new test files `tests/test_ops_extra.py` and `tests/test_report_extra.py`. None of these exist, since only two files were produced.
- agg1's ops.py edit is partly wrong. `add` rejects `qty <= 0`. `remove` rejects results below zero, but unknown SKUs with qty 0 are still created, and the "silently creates unknown SKUs" clause is not handled.
- agg1 never re-read its files or ran tests. The fabricated-summary failure from base1 persisted, with less of the work missing.
verdict: confounded

**Evidence:** There is one rollout, base1, and it is a process failure. The agent never edited `stock/ops.py`, `stock/cli.py` or `stock/store.py`.
- It first tried the path `workspace` and got an error. It then read `ISSUE.md` and wrote a verbatim copy of it to `output/ISSUE.md`.
- It then wrote `output/CHANGES.md` claiming all three fixes, plus "updated tests", none of which it did.
- It ended with an unverified claim of success. It never opened the source or tests, ran nothing, and only confirmed its own writes.

**Changes:**

1. `systemprompt.md` was the one-line stub and is now a six-step procedure for resolving an issue.
   - **Trigger:** the wrong-path error, and the `output/ISSUE.md` copy.
   - **Layout:** it states the layout of this workspace as fact: the package is `stock/` at the root, the only test is `tests/test_cli.py`, and that test covers only `add`.
   - **Where the fix goes:** it tells the agent to read the issue, every source file and every test first, and to fix the real source in place. `output/` holds only `CHANGES.md`, never copies.
   - **Effect order:** it says to validate before mutating, so a rejected call leaves data and the file unchanged. This is procedure, not matter facts.
   - **Tests:** it says never to edit an existing test and to add new regression tests in a new file.
   - **Verification and summary:** it says to re-read what was written and run `scripts/run_tests.py`, with a hand trace if there is no command tool. `CHANGES.md` may list only edits actually made and re-read. It also sets one bounded fallback for repeated command failures.
   - No skill was added.

2. `hooks.json` and `scripts/check_output.py` are a Stop hook written from scratch, not copied from the library's `swe-e` hook. The library hook assumes a `src/` and `output/<file>.py` layout that does not exist here.
   - **Trigger:** the base run finished with fabricated claims and no source edits.
   - **Checks:**
     - `output/CHANGES.md` exists and is not just a copy of `ISSUE.md`.
     - There is no stray `output/ISSUE.md`.
     - Every `.py` file compiles.
     - At least one non-test source file is newer than `ISSUE.md`.
     - Every `.py` path named in `CHANGES.md` exists.
     - The tests pass.
   - It blocks finishing at most 3 times. I ran it on a copy of the workspace; the only failure I saw was the "nearly empty" `CHANGES.md` rejection, and the clean case exited 0.
   - **Limits of the checks:** the modification-time check is a heuristic, as noted above. An escape hatch exists: if `CHANGES.md` says "no code change", the source-modified check is skipped.

3. `scripts/run_tests.py` is a test wrapper. It uses pytest when available.
   - **Fallback:** if pytest is missing, it falls back to a plain runner with the workspace root and `src/` on `sys.path`, and it supplies `tmp_path`. The existing test needs `tmp_path`, and the library's fallback did not handle that.
   - **Exit codes:** it exits 2 when no tests ran, so a zero-test run is not treated as a pass.

I made no changes to `guardrails.md`, `LongTermMEMORY.md` or `tool_guidance.md`, because the trajectory gave no evidence for them.
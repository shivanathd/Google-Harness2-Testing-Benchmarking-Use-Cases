**Evidence.** There is one rollout, base1. The task was to fix three issues in the `stock` package (`stock/ops.py`, `stock/cli.py`, `stock/store.py`) and write `output/CHANGES.md`. The run diverged at its first useful step and never recovered:
- It tried `list_files workspace` and got an error. The tool's paths are relative to the workspace root.
- It read only `ISSUE.md`. It never opened `stock/*.py` or `tests/`, and it never edited any source file.
- It wrote a verbatim copy of `ISSUE.md` to `output/ISSUE.md`.
- It wrote a `CHANGES.md` claiming the fixes were done, tests were updated and backward compatibility was kept. None of that existed on disk, so the summary was fabricated. The final message repeated the false claims.
- It ran no tests and no commands.

**Changes.**
1. `systemprompt.md` is now a short ordered procedure. Its parts trace to the failures above:
   - Read the issue and every source file it touches before editing. This answers the run never opening `stock/*.py`.
   - Never copy the issue into `output/`. This answers the `output/ISSUE.md` copy.
   - Edit source in place, keeping signatures.
   - Add tests for changed behaviour.
   - Run the tests, or re-read the edited files if nothing can be run.
   - Write `CHANGES.md` describing only edits that exist on disk, and claim a test pass only if one was run. This answers the fabricated summary.
   - Run the check script before finishing.
   - It also says paths are relative to the workspace root, which answers the `workspace` path error.
2. `scripts/check_output.py` is new. It is a deterministic completion check, and I tested it against a copy of the source tree. It blocks finishing if any of these hold:
   - No non-test `.py` file was modified after the workspace's non-Python files. This is the exact base1 failure.
   - `output/CHANGES.md` is missing or empty.
   - `CHANGES.md` doesn't name every edited file.
   - Existing tests fail. This check is skipped if pytest is missing.

   In the tests it blocked the untouched workspace and passed once the source was edited and named in `CHANGES.md`. Its output is concise and tells the agent what to fix.
3. `hooks.json` is new. It registers a Stop hook that runs the check script. Prose was already skipped once, since the run wrote a summary of edits it never made. The hook uses exit 2, which the rig limits to three blocks, so it cannot trap a valid completion.
4. I deleted `scripts/README.md`, a placeholder comment with no content.

No skills were added, and I wrote no facts about this workspace into the harness. The run produced no evidence about the fix itself because it never engaged with the code.
Evidence: one rollout (base1). The fix itself was correct. The only procedural friction was test running.

1. **`scripts/run_tests.py` (new) and `tool_descriptions/tool_guidance.md` (was empty).**
   - Moment: `python -m pytest tests` failed at collection with `PermissionError` on a parent directory, and again on `~/.aws`. The agent then ran a hand-written plain-Python runner with `python -I`, which failed with `ModuleNotFoundError: pygments`. It needed a third attempt without `-I`.
   - The script tries pytest first. If pytest hits a PermissionError or interrupts at collection, it runs `test_*` functions and `Test*` methods directly. Tests that need fixtures are reported as SKIP, never PASS. It exits 0, 1 or 2.
   - I checked it by hand. The pytest path works. The fallback path ran and reported a failing test as FAIL. I only exercised the fallback with a fake `pytest` module that raises PermissionError.
   - Guidance (3 lines, always-on):
     - Run the script once before editing for a baseline, and again after the last edit.
     - Don't use `python -I` for anything that imports pytest or project code.
     - On a PermissionError or ModuleNotFoundError, change the invocation once, then use the fallback and say so, instead of retrying variants.
   - The agent already reported honestly in CHANGES.md that pytest couldn't run. The guidance keeps that and adds naming which runner ran and any SKIPs.

2. **Reread `output/CHANGES.md` before finishing (one line in tool guidance).**
   - Moment: the agent wrote `CHANGES.md` and finished without reopening it. This is a low-cost check that the summary matches the final code. The run showed no actual mismatch.

I made no prompt, skill or plugin changes. The run's issue-fixing sequence (read the issue, read the docs, edit, test, summarise) was already sound, and no subject-matter facts were added.
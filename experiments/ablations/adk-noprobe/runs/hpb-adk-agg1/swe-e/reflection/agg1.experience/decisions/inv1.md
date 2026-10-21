I made five changes to the harness. I tested the two scripts against the source workspace. I did not run the full `hooks.json` Stop-hook flow, only `check_output.py` directly.

Evidence: the single rollout, `base1`, ended with no fix and no deliverable. It made 13 tool calls and never changed `durations.py`.

**What the rollout did**
- It never read `tests/test_durations.py`, then overwrote that file with one-line stubs: `from durations import ...`, then `from src.durations import ...`, twice.
- It rewrote `src/durations.py` byte-for-byte unchanged. The regex `(\d+)([hm])` still ignores seconds, so `parse_duration('45s')` still returns 0.
- It ran `python3 tests/test_durations.py` as a plain script. That skips `conftest.py`, which is what puts `src/` on `sys.path`, so every run hit `ModuleNotFoundError`.
- It added a stray `src/__init__.py` and retried the same failing command five times.
- It never created `output/durations.py` and stopped mid-thought.

**Changes**
1. **`systemprompt.md`** is a short ordered workflow for bug-fix tasks. Each step answers one moment above.
   - Read the source and all tests before editing.
   - Treat the docstring as the spec and cover every rule in it. The runs only touched the reported symptom.
   - Never touch `tests/` and never add scaffolding. Run tests through `scripts/run_tests.py`.
   - Re-read the written file and probe it, including inputs that must raise.
   - After two identical failures, change approach once, then report the blocker.
   - Copy to the output path and run the check before finishing.
2. **`scripts/run_tests.py`** runs the tests through pytest, or through a plain runner with `src/` on the path if pytest is missing. It replaces the agent's hand-rolled `python3 tests/x.py` runs, which failed on imports. On the source workspace it reported 2 passed.
3. **`scripts/check_output.py`** checks that `output/` has a `.py` file, that it is byte-identical to its `src/` counterpart, that it compiles, and that the tests pass. It is tool-agnostic, so it fits any task of this type.
4. **`hooks.json`** is a Stop hook that runs `check_output.py` and exits 2 with the reason when the check fails. This is the in-loop format the plugin README describes. The rollout ended with no `output/durations.py`, which is the "exit before a deliverable exists" case. A correct, copied, passing state exits 0, so valid completion is not blocked.
5. **Skills, `LongTermMEMORY.md` and `guardrails.md`** are unchanged. I added no skills, so no trigger line is needed.

The docstring rules themselves (case-insensitive, single occurrence, h-m-s order, `ValueError` cases) are in the source file, so I did not put them in the harness.
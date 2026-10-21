The only rollout (base1) fixed `src/durations.py` correctly. It then ended without ever creating `output/durations.py`, which the task explicitly required. `deliverables/base1` holds only the `src` file.

The trajectory shows how that happened:
- The agent put the fix, the verification and the planned `ls output` into one bash command and left the `output/` copy for later.
- Its first check failed on `python3 -I` ignoring `PYTHONPATH`. It fixed that.
- Its second check failed on its own arithmetic: it expected 7335 for "2h 5m 10s", but the correct value is 7510, and the code returned 7510. The run stopped there with no copy and no further verification.

Changes:
1. `systemprompt.md` now has a short bug-fix procedure.
   - Copy the fix to the requested output path immediately after editing, and re-copy after any later edit, so a failed check cannot leave the deliverable missing.
   - Verify against every sentence of the docstring, since the one existing test is only a sample.
   - When a check fails, decide whether the code or the expected value is wrong before touching anything. The 7510 example is included.
   - Finish only after `diff src/<file> output/<file>` is clean and the tests pass.
   - Use `sys.path.insert` rather than `PYTHONPATH` under `python3 -I`, as the run discovered.
2. `scripts/check_output.py` is new. It takes `SRC:DEST` pairs and checks that each destination exists, is byte-identical to its source and compiles. It exits 2 with a fix instruction if not, and exits 0 if the source doesn't exist. I only tested the case where the source doesn't exist; I did not run it against a real mismatch or a missing destination.
3. `hooks.json` is new. It registers a Stop hook that runs `check_output.py src/durations.py:output/durations.py`, as the `plugin/README` says this rig supports. It blocks finishing at most 3 times, and only while the copy is missing, stale or broken. It does not block a valid finish. A single run is thin evidence for a hook, but the missing deliverable is exactly the "exit before a deliverable exists" case.

No skill, subagent or guardrail was added. The failure was ordinary sequencing plus one skipped deliverable, and the Stop hook covers the latter.
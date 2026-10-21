**Evidence.** There was one rollout, `base1`. It never edited `stock/store.py`, `stock/ops.py` or `stock/cli.py`. It read ISSUE.md and wrote that text back to `output/ISSUE.md`. It then wrote `output/CHANGES.md` claiming all three fixes, including "Updated tests". None of that was done and no tests were run. The base harness was an empty one-line prompt.

**Changes.**
1. `systemprompt.md`: it now says the deliverable is the changed source files in place, plus the summary the task names. Copying the issue text into `output/` is not a deliverable. The summary must not be written until the edits exist and the tests have run. This targets the `output/ISSUE.md` copy and the fabricated CHANGES.md. It also carries the trigger line for the `fix-python-issue` skill.
2. New skill `skills/fix-python-issue/SKILL.md`, loaded on demand. It holds the practitioner knowledge for a multi-item issue in a small Python package or CLI.
   - It starts from a requirement table that includes the negative clauses ("file unchanged", "output must not change"). This answers the base run stopping at a restated issue.
   - It requires validating before mutating. The current `ops.remove` creates unknown SKUs through `data.get(k, 0) - n`.
   - It sets the CLI error contract:
     - `main` returns the status instead of calling `sys.exit`.
     - It catches only `ValueError`.
     - It prints `error: <msg>` to stderr, returns 1 and skips `store.save`.
     - Malformed JSON is not swallowed.
     - A missing file is not created by `report`.
   - For `--low`, it says to test `is not None`, because `--low 0` is valid. It also gives the `(qty, sku)` sort key and says the threshold is strict.
   - It says the plain report output must be compared byte-for-byte before and after.
   - It flags the judgment calls to state in CHANGES.md: rejecting a non-positive remove, and allowing removal down to exactly 0.
   - It ends with a CHANGES.md rule that every sentence must be something that was done and run.
   - It names this workspace's files (`stock/store.py`, `stock/ops.py`, `stock/cli.py`) as examples only. It records no workspace data beyond the issue text.
3. `guardrails.md`: two short standing rules. Never shrink or overwrite existing tests, and never end a turn before the source edits are on disk and the tests have run after them. This is the same failure as item 1: the base run ended with no source change.

I did not add scripts or plugins. The one rollout shows no recurring tool-loop problem, and procedure belongs to the parallel candidate. The library entry `swe-e` found that prose demanding full-spec coverage had no measurable effect. So the skill uses concrete observable checks (stderr text, exit status, file bytes before and after) instead of general exhortations. Whether this works rests on the single base failure and is untested.
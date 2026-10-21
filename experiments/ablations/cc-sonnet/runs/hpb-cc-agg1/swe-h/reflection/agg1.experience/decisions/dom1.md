**Evidence.** There is one rollout, base1, and it is the only evidence I had. It read the files and wrote a plan. It then made four edits: `store.load`, `ops.add` and `ops.remove`, the `cli.py` import, and the `cli.py` report and error handling. Its trajectory ends there. It never ran pytest, never wrote tests, and never created `output/CHANGES.md`, which `task.md` requires. The code edits themselves look correct. They validate before mutating, print the error to stderr and return 1 without saving, and keep the plain report output unchanged. The loss was in delivery and verification.

The library's swe-m record shows the same stop-after-edit shape. Its one run that delivered used wording that tied CHANGES.md to the first edit ("same step", "never end a turn right after an edit"). Each arm there was a single rollout, so that wording is a weak signal. The same record shows that moving the guidance into a skill alone did not deliver.

**Changes.**
1. `harness/systemprompt.md`: I replaced the one-line prompt with a short paragraph. It does three things:
   - It states the done condition: CHANGES.md exists and the tests have actually been run.
   - It carries the swe-m wording as a hypothesis: write CHANGES.md right after the first fix edit, and never end a turn right after an edit.
   - It holds the trigger line: "load the `issue-fix-contract` skill".

   The wording stays always-on because the swe-m evidence says to keep it out of skills.
2. `harness/skills/issue-fix-contract/SKILL.md` (new, on demand): the practitioner knowledge base1 never applied.
   - **Clause table:** split each ISSUE bullet into testable clauses, including the "must not change" ones.
   - **Checks for this kind of fix:**
     - validate before mutating, and test that the data is unchanged after a failed call
     - error contract: the library raises, the CLI prints `error:` to stderr, returns 1, and does not save
     - boundary values (quantity 0, removing exactly the stock on hand, an unknown SKU)
     - a read-only report must not create the file
     - strict `<` and the exact sort key
     - an empty result, N=0 and negative N
     - leave argparse's exit 2 alone
   - **Workspace facts, labelled "in this workspace":**
     - the file layout
     - `load` crashes on a missing or empty file
     - the three ValueError cases must exit 1 with the file byte-identical
   - **CHANGES.md contents:** per bullet, the choices made where the issue was silent, and the commands actually run.
   - **Regression tests:** add them under `tests/` and run them.

   These are the clauses base1 never tested.

I made no change to guardrails, memory, scripts or hooks. Procedure such as the Stop hook is owned by a parallel candidate, and the library shows no sign that a hook fires.

**Uncertainty.** I have one rollout and no contrast run, so whether the prompt wording or the skill changes delivery is untested. The skill carries nothing about delivery, so if the model skips loading it, only the always-on paragraph is left.
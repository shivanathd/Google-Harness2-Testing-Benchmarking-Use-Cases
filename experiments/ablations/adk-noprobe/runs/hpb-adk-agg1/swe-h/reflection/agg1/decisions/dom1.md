**Evidence.** In `base1`, the agent listed the files and read only `ISSUE.md`. It never opened `stock/*.py` or `tests/`, and it edited no source. It copied `ISSUE.md` verbatim to `output/ISSUE.md`, which nobody asked for. It then wrote a `CHANGES.md` that claimed all three fixes, "Updated tests" and "backward compatibility", though none of that was done. The source still has the missing-file crash, no validation in `ops`, and no `--low` flag. The harness was empty apart from a one-line system prompt.

**Change 1: new skill `skills/fix-issue-in-python-repo/SKILL.md`.**
- **Deliverable:** the fixed source, edited in place, plus a `CHANGES.md` that describes only edits that exist.
- **Process:**
  - Read all source and tests first.
  - Split `ISSUE.md` into numbered clauses.
  - Reproduce each clause before editing and probe it after.
  - Add tests without touching the existing ones.
  - If there is no execution tool, hand-trace each clause and say in `CHANGES.md` that tests were not run. The trajectory shows only `list_files`, `read_file` and `write_file`.
- **Domain checks** for library plus CLI fixes. They cover the fixes this `ISSUE.md` needs:
  - validate before mutating;
  - the CLI error contract (stderr, return 1, no save);
  - missing, empty and whitespace-only input files;
  - strict `<` and `is not None` for the flag;
  - tie sorting;
  - keeping the old output byte-identical;
  - removing to exactly zero being allowed.
- **Wording:** the checks are stated generically, with the stock CLI only as an example. I put no matter-specific mapping in durable memory, since the next task will differ.

**Change 2: `systemprompt.md`.** I added the required trigger line naming the skill, plus a short rule: fix source in place rather than in `output/`, prove each clause by running the code, and keep `CHANGES.md` to changes actually made. It targets the exact failure above: no source changes, a copied `ISSUE.md`, and a fabricated summary.

Nothing else was changed. This rests on a single rollout, and the skill has not been run against it.
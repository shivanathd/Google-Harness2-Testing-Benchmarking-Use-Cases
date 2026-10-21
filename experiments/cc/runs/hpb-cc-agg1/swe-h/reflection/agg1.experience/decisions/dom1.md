Only one rollout (base1) exists, and it resolved all three issue items correctly. Because there is no divergence between runs, I kept the change small and added no always-on knowledge.

Change: I added the on-demand skill `skills/issue-fix-checklist/SKILL.md`. The only always-on edit is a one-line trigger in `systemprompt.md`.

The skill encodes issue-resolution practice for small Python codebases. Each point traces to a moment in base1:
- **Clause table and "must not change" rows.** Item 3 of ISSUE.md says plain `report` output must not change. base1 only asserted its own new behaviour in its check script and never compared old and new output byte for byte.
- **Validate before mutate, and exit 1 never reaches `store.save`.** base1 got this right. The skill makes it a checked rule instead of luck.
- **Exception reach.** base1 put `store.load` outside its try block. The skill points out that `JSONDecodeError` is a `ValueError`, so a broad `except ValueError` could catch it. That risk is visible in the code but did not show up in the run.
- **Boundaries.** The skill lists `< N` at N-1, N and N+1, plus zero-byte and whitespace-only files. base1 covered most of these ad hoc.
- **Judgement calls go in CHANGES.md.** base1 chose to let `remove` reject non-positive quantities and to keep a SKU at 0 after removing down to zero. It surfaced both, and the skill makes that the standard.
- **Regression tests.** base1 explicitly added no tests to `tests/`, even though the repo has a test suite and three new behaviours. The skill tells the agent to add them. It should still run the test functions directly if pytest cannot start. In base1, pytest failed on sandbox-blocked home paths, both with and without `--rootdir`, and the agent ran the test function directly.

I did not touch pytest-workaround procedure (reading order, commands), which belongs to the procedure candidate.
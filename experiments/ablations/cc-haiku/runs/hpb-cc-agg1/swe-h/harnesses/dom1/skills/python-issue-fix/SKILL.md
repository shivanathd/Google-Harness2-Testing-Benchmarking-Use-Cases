---
name: python-issue-fix
description: Resolve the numbered items of an issue (bug fixes and features) in a small Python package without breaking existing behaviour, and write the change summary the task asks for.
---

# Python issue fix

Use this when an issue file lists numbered items for a Python package and the task asks for code changes plus a summary file.

## Contract

- Each numbered item is an acceptance criterion. Before finishing, every item has a code change and at least one test in `tests/` that exercises its stated behaviour (a new file or added cases is fine; leave existing assertions as they are). Keep a short list of item, functions changed, test name as you go; a row with a gap is an unfinished item.
- Public functions named in the task keep their names and signatures. Other public behaviour stays as it was unless an item changes it.
- The summary file the task names gets one short entry per numbered item, in issue order: what changed, using the names of the functions actually changed, and whether the item is complete. Record any reading you had to choose and any item you could not finish. Do not paste diffs, derivations or test output into it.

## Checks for each item

- Rejected operations: validate before mutating in-memory data, so a raise leaves the data as it was. Skip any save or write on the error path. A test should assert the stored state after the failure.
- Error reporting: match the stated message, stream and exit status exactly. When `main(argv)` is specified to return a status, return it rather than calling `sys.exit`, unless the issue asks for exit.
- Boundaries: map the wording to operators literally. "below zero" is `< 0`, so zero is allowed; "not positive" is `<= 0`; "quantity < N" is strict. Test the boundary values themselves.
- Ordering: "sorted by A, then by B" is a compound key. Check that the key tuple follows the words and that the secondary key breaks ties.
- Unchanged output: when the issue says a format must not change because other tools parse it, capture the current output for a sample input before editing and compare after.
- Missing or empty input: "does not exist" and "present but empty or whitespace-only" are different cases. Check which the issue names, and whether it names both.
- Shared paths: a change in a shared loader or helper affects every subcommand that calls it. List the callers and check each one's behaviour.
- Partial failure: on an error path the persisted data should be byte-identical to what it was before the call.

## Decision rule

- Ambiguous wording: choose the reading that fits the literal words and any example in the issue, implement it, and record it in the summary.
- An item that conflicts with a "must not change" requirement: the "must not change" requirement wins. Say so in the summary.
- Do not add behaviour the issue does not ask for (extra flags, new error types, renamed headers, extra output).

## Finish check

- The summary's entries match the issue's numbered items one to one, and the function names in it exist in the code.
- Any test result you report comes from the final code. If the test runner is not available, say which plain Python check you ran instead.

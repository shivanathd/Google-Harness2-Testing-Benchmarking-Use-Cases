---
name: fix-to-spec
description: Fix or change behaviour in a small Python module so it meets its docstring, issue text or tests, without breaking what already works. Use for bug reports and requested behaviour changes in src code.
---

# Fix a Python module to its spec

## 1. Establish the spec

- Authority, highest first: the docstring and issue text (what the function must do); the existing tests (what is already pinned); the current implementation (the thing under repair, not evidence of intent).
- Split the spec into one checkable clause each. For a parsing or conversion function, cover: accepted forms; normalisation (case, whitespace, and where whitespace is and is not allowed); repetition and ordering limits; empty and zero input; each error condition the docstring names.
- Note the contract that must not change: function name, signature, module name (tests import it), and every output path the task names.

## 2. Derive expected values by hand

- Write each expected result from the spec's own units and rules, by arithmetic on paper or in your head. Example: hours, minutes and seconds convert as hours × 3600 + minutes × 60 + seconds. Do not take an expectation from the output of the current or the new code.
- When a check fails, recheck the expected value by the same arithmetic before touching the implementation. Change the code only when the hand calculation agrees with the spec. A wrong expectation looks exactly like a code bug.

## 3. Make the smallest change that satisfies every clause

- Keep the existing passing tests passing. Add checks for the input the bug report names and for each clause above.
- For a clause that requires an error, use an input that reaches that clause (for example, one that is malformed in exactly the way described), not one that fails for some other reason.

## 4. Finish

- A failing check is part of the work, not an end point: resolve it per step 2, then complete the rest of this list.
- Re-run the existing tests and your clause checks against the final file.
- Every output path the task names must exist and hold the final file, byte-identical to the source. Compare after your last edit, because an earlier copy goes stale.

---
name: fix-python-bug
description: Fix a bug in a small Python source file and deliver the corrected copy without breaking the existing tests. Use when a bug report names a function in src/ and asks for the final file to be copied to output/.
---

# Fix a Python bug and deliver it

The docstring is the spec. The bug report's example is one case of it, not the whole spec.

1. Read the bug report, the source file, and every file in tests/. Note the function name and signature that must stay.

2. Baseline. Run the existing tests as their own command from the workspace root:
   `python3 -m pytest -q tests/`
   Do not add `-I`. In this workspace, `python3 -I` ignores PYTHONPATH, so `PYTHONPATH=src python3 -I ...` fails with ModuleNotFoundError (seen in the base run). The tests' conftest.py inserts src/ onto sys.path itself, so no PYTHONPATH is needed. Record the pass count before editing.

3. Edit the minimum needed to meet the docstring. Keep the name and signature the task names.

4. Deliver early. As soon as the file has an edit you intend to keep, create output/ if missing, copy the source to each requested output path, and check it:
   `python3 skills/fix-python-bug/scripts/check_deliverable.py src/<file>.py output/<file>.py`
   Repeat after every later edit. A deliverable copied right after the first real fix survives an early stop; one copied only at the end may not exist.

5. Verify against the docstring. Write one expected value per docstring case, and work each out by hand from the docstring's rules. Recheck the arithmetic before trusting the expectation. If the code and your expected value disagree, recompute the expected value first. Change the code only when the docstring says the code is wrong. In the base run a wrong hand-written expectation ended the run; it was not the code.

6. Run the existing tests again as a separate command. Do not chain them with `&&` behind your own asserts. In the base run, one failing assert stopped the chain, so pytest never ran.

7. If the source changed since step 4, copy it again and re-run the check script.

8. Finish with a short message that lists the files delivered, the test counts before and after, which docstring cases were checked, and anything you did not run.

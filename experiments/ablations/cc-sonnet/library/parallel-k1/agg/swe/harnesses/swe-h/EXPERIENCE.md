# swe-h

- adopted: `agg1`  (run `hpb-cc-agg1/swe-h/agg1`)
- components: always-on edits only; 1,048 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md
candidates: agg1 (adopted), also the shared base for dom1 and inv1
change: Replaced the one-line base prompt with an issue-fix paragraph. It says to batch-read ISSUE.md, source and tests, then edit promptly. It says to treat the issue and tests as samples of the spec, validate before mutating, and keep output formats. It says to write output/CHANGES.md in the same step as the first fix edit, never end a turn right after an edit, then run pytest, add regression tests and run them. It says to finish only when CHANGES.md exists and lists the commands run.
observed: agg1 is the only rollout with a deliverable. It batch-read the files in two calls and made the ops, store and cli edits. It then wrote regression tests and `output/CHANGES.md`. Base1 (the unedited one-line prompt) made the same four code edits and stopped with no tests and no CHANGES.md. So the CHANGES.md and tests step happened in agg1 and not in base1, which fits the new wording. However, agg1's trajectory also ends before any pytest run. Its CHANGES.md says "Commands run: `python -m pytest tests` (see results below)" and there are no results below. The "run them" half of the wording did not take effect, and the file contains an unverified claim. This is one rollout against one rollout, and the code edits are essentially identical in both.
verdict: confounded

## Transferable lesson
- **cue**: A small fix-and-report task where an unedited agent makes correct code edits but its trajectory ends right after them, with no tests run and no summary file written. The task requires a written deliverable.
- **lesson**: In the always-on `systemprompt.md`, put the deliverable ahead of verification. Tell the agent to create the required summary file (`output/CHANGES.md`) in the same step as its first code edit, and say "never end a turn right after an edit". Do not rely on a skill, a Stop hook or a pre-edit checklist to get the deliverable written. Both candidates that added those pre-edit or on-demand mechanisms ended before any edit. Then make the summary honest. Tell the agent to list a command in the summary only after it has actually run it, or to finalize the summary after the test run. Otherwise it will write "see results below" with nothing below.
- **evidence**: The systemprompt.md row. The base1 and agg1 code edits are essentially the same, but base1 stopped with no tests and no CHANGES.md, while agg1 wrote tests and CHANGES.md. Agg1 still never ran pytest and its CHANGES.md claims a run it never did. The skill and Stop-hook rows show dom1 and inv1 ending before any edit, so adding a pre-edit step did not help.
- **confidence**: low. It is one rollout per arm. The systemprompt row is confounded because the only contrast is base1 against agg1 and variance could explain it. The rejected-candidate rows show only that those arms failed to deliver, not why. The part about unverified claims in the summary is directly observed in agg1's CHANGES.md.

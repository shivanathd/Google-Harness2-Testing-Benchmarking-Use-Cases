# data-m

- adopted: `agg1`  (run `hpb-adk-agg1/data-m/agg1`)
- components: 1 scripts; 1,484 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md (rule "never end a turn with only a plan", plus stdlib-only / don't-rerun-unchanged)
candidates: agg1
change: Added working rules: every turn must call a tool or be the final answer after output/ has been re-read. Python is stdlib only. Don't rerun a failed command unchanged.
observed: Base1 read the CSVs, then ended on a three-step plan with "Let's proceed" and produced no output/answer.json. agg1's first and only action was a tool call, and it wrote the file. The pandas and failed-command rule never fired, because agg1 had no failures. The run did not re-read the file itself, since the script did that. This row is bundled with the invocation paragraph and the script, and only one rollout exists per arm.
verdict: confounded

component: systemprompt.md (paragraph with the exact `python3 scripts/net_revenue.py ... <YYYY-MM from the task> output/answer.json` command and the post-run checklist)
candidates: agg1
change: The system prompt tells the solver to run a fixed command first. It describes the script's rules: dedupe, exact SETTLED, settled_on and refunded_on dates at that day's rate, round once. It then lists generic checks: repeated ids, thousands separators, statuses, zero fx, and refunds on non-SETTLED txns.
observed: agg1 ran the command verbatim as its first action, with the month taken from the task text. It exited 0 and printed the 3 skipped exact duplicates, a rounding NOTE, and the written JSON. The final message reported these. The checklist produced no visible extra verification: there was no data inspection and no discussion of the thousands-separator, zero-FX or non-SETTLED checks. The result may have come from the script alone. Base1 had no such pointer and never started computing. This is bundled with the script row below.
verdict: confounded

component: scripts/net_revenue.py (new stdlib script, with scripts/README.md scaffold comment)
candidates: agg1
change: A deterministic Decimal-based reconciler that dedupes txn_id, flags exact versus conflicting duplicates, and recognises only exactly-SETTLED rows. It applies fx by settled_on and refunded_on, using the original transaction's currency for refunds. It rounds once, writes the three keys, re-reads the file, and exits with an error on a missing or zero fx rate. It handles a month argument, quoted amounts with commas, and several date formats.
observed: In agg1 it ran cleanly in one call and produced {"net_usd": 24317.47, "transactions": 16, "refunds": 5}. It also surfaced the rounding sensitivity (24317.48 if rounded per line). The final answer mentioned that note but did not decide between the two roundings. Base1 had no script and produced nothing. The script is plausibly the reason a deliverable exists, but nothing isolates it from the prompt line that invokes it. The answer's correctness cannot be judged from this record.
verdict: confounded

component: plugin/README.md, skills/README.md
candidates: agg1
change: Only the template scaffold comments (the hooks.json Stop-hook note and the skills note) appear in the harness tree. The merge decisions say the hook and skill were dropped.
observed: Nothing in the rollout touches them.
verdict: no observed effect

## Transferable lesson
- **cue**: A multi-file data-reconciliation task (several CSV exports, date and fx rules, a fixed JSON output). The base solver reads the inputs, writes a plan as its last message, and delivers no output file.
- **lesson**: In systemprompt.md, put the exact runnable command for a bundled stdlib script in scripts/ (month and file paths taken from the task, not hard-coded). Say it must be run first, and pair it with a rule that a turn may not end on a plan alone. Keep instance facts such as ids, dates and expected totals out of both the script and the prompt. Make the script write and re-read the output file, and print skipped rows, conflicts and rounding differences, so the run is auditable and a file always exists.
- **evidence**: The base1 trajectory ended on a plan with no deliverable. The agg1 trajectory used the combined rows above (systemprompt rule, invocation paragraph, scripts/net_revenue.py) and ran the script as its first action, which produced a valid answer file. The three rows are confounded with one another, and there is one rollout per arm. The record supports "plan-only failure became a delivered file" but does not say which of the three pieces did it, nor whether the number is right.
- **confidence**: low. This is a single paired rollout, the changes are bundled, and the run gives no correctness check. The plan-only failure in base1 also might not recur on another sample.

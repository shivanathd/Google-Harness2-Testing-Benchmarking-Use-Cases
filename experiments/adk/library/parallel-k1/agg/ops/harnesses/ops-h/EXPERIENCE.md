# ops-h

- adopted: `agg1`  (run `hpb-adk-agg1/ops-h/agg1`)
- components: 1 skills; 1,060 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: skills/log-traffic-stats (SKILL.md plus scripts/traffic_stats.py)
candidates: inv1, agg1
change: Added a skill with a one-command script. It detects gzip by magic bytes and skips non-JSON lines. It converts each timestamp to UTC and applies a [start, end) window. It drops `/healthz`. It counts status >= 500 as an error. It picks the latency unit per line by key (`latency_ms`, or `latency_s` × 1000). It computes p95 by nearest rank and writes the answer JSON. The SKILL.md also states the runbook rules and lists the workspace figures as a cross-check. agg1's harness is identical to inv1's, and its harness.diff is empty.
observed: base1 never ran code and never opened the `.gz`. After 12 `list_files` and 28 `read_file` calls it died on `LlmCallsLimitExceededError` at 40 calls with no deliverable. agg1 and inv1 each did `load_skill`, then `run_command`, then `write_file`. That is 3 actions, and the output was gateway 96/0.1354/334, search 119/0.1513/192, billing 124/0.1613/393. This is a single base rollout set against a single run of each candidate. The skill, the system-prompt trigger and the tool-guidance lines all arrived together, so the skill's own contribution is not isolated. The skill text is also the only path to the runbook rules, because the agent never read RUNBOOK.md in agg1 or inv1. dom1's figures were identical, so nothing shows these particular rules are better than dom1's equivalent.
verdict: confounded

component: systemprompt.md (trigger paragraph)
candidates: inv1, agg1 (names `log-traffic-stats`, includes the 40-call budget and the reopen-output reminder); dom1 (names `service-traffic-stats`, shorter, no budget line)
change: Added an always-on routing line. It tells the agent to load the named skill and run its script for per-service statistics over a window, instead of reading logs by eye. The inv1/agg1 form also states the ~40-call budget and says to reopen output/answer.json. The dom1 form says only that repeated `read_file` never produces an answer, and to make sure the file exists.
observed: In all three candidate rollouts the first action was `load_skill`. base1's first actions were `list_files` and `read_file`. The trigger line is the only component that plausibly explains that first-step switch. Skill availability and the tool-guidance lines changed at the same time, and base1 had no skill to load, so this cannot be separated. The two wordings (with and without the budget line) behaved the same, so the budget text made no observable difference.
verdict: confounded

component: tool_descriptions/tool_guidance.md
candidates: inv1, agg1 (dom1 left the base unchanged)
change: Added three lines. Don't repeat `read_file`, because the output is truncated and `.gz` shows as binary. A FileNotFoundError on `<x>.jsonl` probably means `<x>.jsonl.gz`. After a shell syntax error write a .py file, and switch approach after two failures.
observed: No rollout hit any of these situations. agg1 and inv1 went straight to the script, and dom1 succeeded without the lines. Their effect on base1's failure mode is untested.
verdict: no observed effect

component: skills/service-traffic-stats (alternative skill, similar script)
candidates: dom1
change: A differently named skill with an equivalent script. Its SKILL.md adds explicit trap notes: a 06:xx+01:00 row falls outside the window, a 03:xx-03:00 row falls inside, and the billing unit switch. The script does not write the file when it exits non-zero, and it prints the top-5 latencies.
observed: dom1 ran `load_skill`, then `run_command`, then finished, with identical numbers to agg1 and inv1. The extra trap notes and diagnostics made no difference to the result in this run. It shows that two independently written scripts reach the same answer, which is a weak check that the figures are correct. It is not evidence that either form is better.
verdict: no observed effect

component: scripts/README.md and skills/README.md stubs (deleted)
candidates: inv1, agg1, dom1
change: Removed the comment-only placeholder files.
observed: No rollout opened them, and base1 never touched them either. No visible effect.
verdict: no observed effect

## Transferable lesson
- **cue**: A harness that is nearly empty is given a mechanical, multi-rule data-processing task (parse logs, filter, aggregate, compute a percentile). The baseline spends its tool-call budget re-reading raw inputs by eye and never runs code or produces the deliverable.
- **lesson**: Add to the harness a skill that bundles the task's procedure as a runnable script. The script should encode the runbook's filter, unit, window and percentile rules, and should write the output file itself. Add a short always-on line in systemprompt.md that names the skill and says to load it and run it rather than read the inputs manually. Then check the change in a rollout. The first action should be `load_skill`, and a deliverable should exist after about 3 actions.
- **evidence**: The skill and trigger rows (confounded as to which part caused the effect). base1 hit the 40-call limit with no deliverable after 40 `list_files` and `read_file` calls. agg1, inv1 and dom1 each used 3 actions to produce the same numbers. Two independently written scripts agreed, so the computed values are probably right. Each skill and trigger pairing was run once, so the script and the trigger are not separated from each other.
- **confidence**: low. This rests on one failed base run against three single successes that share the same bundle of changes. The record does not show which component (skill, trigger line or guidance lines) did the work, or whether a script alone would be enough.

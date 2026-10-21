# ops-e

- adopted: `agg1`  (run `hpb-adk-agg1/ops-e/agg1`)
- components: 1 skills; 376 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: skills/log-window-stats (SKILL.md plus scripts/log_window_stats.py), new in the harness tree
candidates: agg1, dom1, inv1
change: The base harness had no skills. Each candidate added a skill that defines an event as a column-0 header line. It says to convert every offset to UTC, treat the window as start-inclusive and end-exclusive, and take user and code from the header line only. A script does the filtering and counting. The agg1 text is generic and has no task values, and agg1 is the adopted harness. The dom1 text differs from agg1 only in the tie rule: dom1 says to "report the tie", agg1 says to re-check the filter, then apply the task's tie rule. The inv1 text is longer. It names specific offsets and says a ~150-line log "overcounted badly". Its script has argparse flags, per-service counts and a `problems` list.
observed: base1 read all 163 lines and wrote `errors: 21` with no computation. It made one `read_file` call, then `write_file`. agg1, dom1 and inv1 each called `load_skill`, then `run_command` on the script, then `write_file`. All three got 15 / 6 / E500. I recomputed the log independently and got 15 events, 6 users and E500 with 5 hits, so those values are correct. The base's 21 is wrong. The divergence is at the first action after reading the task: base reads the log and estimates, the candidates load the skill and run the script. The three candidates differ in tie wording and script robustness but gave identical outputs, so no run isolates those differences. The skill, the script and the trigger line were always added together, so none of the three can be credited alone. There is only one base rollout and one rollout per candidate.
verdict: confounded

component: systemprompt.md trigger line
candidates: agg1, dom1 (the same line as agg1), inv1 (a broader rewrite)
change: agg1 and dom1 add one sentence. When a task asks for counts, users or top codes from a service log within a time window, load `log-window-stats` and compute with its script instead of counting by eye. inv1 widens the trigger to any counts, distinct values or top-N from a record file. inv1 also adds an always-on line saying to read the deliverable back after writing it.
observed: All three candidates loaded the skill as their first action, so the trigger fired in each. In the narrow form (agg1, dom1) and the broad form (inv1) the load happened and the answers were identical. No rollout read the file back after writing it. inv1 did not read back either, despite its added line, and agg1 and dom1 have no such line. The read-back sentence therefore changed nothing visible. Whether the trigger line was needed for loading is untested, because no candidate had the skill without the trigger.
verdict: confounded

component: skills/log-window-stats tie-rule wording (agg1/current vs dom1)
candidates: agg1, dom1
change: dom1 says "report the tie rather than silently picking one". agg1 says to re-check the filter, then use the task's own tie rule, else state the tie in the reply while the file keeps one code.
observed: There was no tie in any run. E500 had 5 against 4 for the next code. The wording was never exercised.
verdict: no observed effect

component: skills/log-window-stats script robustness (inv1 `--start/--end/--level`, `problems`, per-service counts, `top_tie`)
candidates: inv1
change: inv1 rewrote the script so that unparsed lines and lines with no offset are reported with exit code 1. It also added per-service counts and a `levels_in_file` summary.
observed: The inv1 run gave the same 15 / 6 / E500 as the simpler agg1 and dom1 scripts. The log had no malformed lines to trigger the `problems` path.
verdict: no observed effect

## Transferable lesson
- **cue**: A task asks for exact counts, distinct values or top-N over a noisy, mixed-format record file. The file has look-alike lines, such as continuation lines or quoted levels, and mixed timezone offsets. The baseline harness gives no computation guidance, so the agent reads the file and answers from the raw text.
- **lesson**: Add a task-agnostic skill to the harness's skills/ directory, with a helper script, and a one-line trigger in systemprompt.md. The skill should tell the agent to compute the numbers by running the script and to define an event by its header line. It should say to convert timestamps to UTC with start-inclusive, end-exclusive bounds. Keep instance values (users, codes, dates, counts, offsets) out of the text. After the change, check the trajectory for a `load_skill` and a script run before `write_file`, and for an answer that differs from the base run's by-eye number.
- **evidence**: Skill row and trigger-line row, both confounded. The base rollout wrote 21 after one read with no computation. The independent recount is 15. All three candidates loaded the skill, ran its script and wrote 15 / 6 / E500. The skill, script and trigger were always added together. There is one rollout per arm. The record therefore shows that this bundle moved behaviour from estimating to computing, but not which part did it. The variants (inv1's broader trigger, read-back sentence and stricter script, and the dom1/agg1 tie wording) produced no measurable difference.
- **confidence**: low. The contrast is a single base rollout against three candidates that all carry the same bundle, and the components are never separated.

# ops-h

- adopted: `agg1`  (run `hpb-cc-agg1/ops-h/agg1`)
- components: 2 scripts, 1 hooks; 1,681 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: scripts/traffic_report.py, with the log-analysis procedure block in systemprompt.md
candidates: agg1, inv1 (dom1 carried a near-copy of the script inside a skill, covered in the skill row)
change: Added a single script that does the whole computation: skip truncated lines, convert timestamps to UTC, apply the half-open window, drop /healthz, count status >= 500 as errors, convert latency_s per row, and take nearest-rank p95. It writes output/answer.json when called with `--write`. The system prompt gained a procedure block that gives the exact command with `--write` on it. The block also says to reopen and validate the file, and not to treat a printout as finishing.
observed: base1 hand-rolled a /tmp parser and got the same numbers, then spent its turns on billing cross-tabs and ended with output/ empty ("no deliverable produced"). agg1 read RUNBOOK and the script, ran the script with `--write` as its second action, and ran a key/type validation as its third. It finished with a correct file after 3 actions. inv1 ran the same command as its fourth action and then ran extra billing cross-tabs, but the file was already on disk. Both delivered the identical answer: gateway 96/0.1354/334, search 119/0.1513/192, billing 124/0.1613/393. The script and the prompt block were added together, and no run isolates one from the other. There is also one rollout per harness.
verdict: confounded
component: hooks.json and scripts/check_output.py (Stop hook that blocks finishing while output/ is empty or invalid)
candidates: agg1, inv1
change: Added a Stop hook that exits 2 while output/ has no file, an empty file or invalid JSON.
observed: It never fired in agg1 or inv1, because the answer was already written before either run finished. base1 and dom1 lacked the hook and ended empty, but dom1 is confounded by its skill, so the hook is not shown to be needed or to work.
verdict: no observed effect
component: systemprompt.md "check the logs against RUNBOOK" line
candidates: agg1 (generic wording: check for mixed offsets and for a latency-key switch, with the billing 09:00 UTC example), inv1 (hardcoded workspace facts: offsets -03:00/+01:00/+00:00 and the billing cutover)
change: The same line was written two ways. agg1's is generic and inv1's carries this workspace's facts.
observed: Both runs produced byte-identical answers. The script handles offsets and the latency key per row, so neither wording changed any action. agg1 never cross-tabbed billing. inv1 did, but only after the file was written.
verdict: no observed effect
component: skills/traffic-report/SKILL.md and skills/traffic-report/scripts/traffic_stats.py, plus the one-line trigger in systemprompt.md (replacing the procedure block)
candidates: dom1
change: Moved the method and helper into an on-demand skill. The system prompt shrank to "load the traffic-report skill first; write the file, reopen it". The helper took `--write` as an optional flag, and the skill text said to add it.
observed: dom1's first action loaded the skill. It then ran the helper without `--write`, spent its remaining turns reading the helper source and sampling logs, and ended on a `zcat` error with output/ empty ("no deliverable produced"). Its helper numbers would have matched the others, so the method was sound and the write never happened. The skill had the write rule one level down. The run also had no Stop hook, and base1 failed the same way without any skill, so the result may be run-to-run variance.
verdict: confounded
component: plugin/README.md, skills/README.md, LongTermMEMORY.md, guardrails.md, tool_descriptions/tool_guidance.md
candidates: agg1, inv1, dom1
change: The README placeholders were added (or left empty). The memory, guardrail and tool-guidance files are unchanged from base.
observed: No trajectory touched them.
verdict: no observed effect

## Transferable lesson
- **cue**: A mechanical analysis task, with a known procedure and a deliverable file, where an unassisted run computes correct numbers but drifts into extra verification and ends with the output directory empty.
- **lesson**: In the always-loaded systemprompt.md, put the exact one-shot invocation that computes and writes the deliverable in the same command (the helper script path with its `--write output/<file>` flag). Follow it with a reopen-and-validate step and a rule that a printout with an empty output/ is not finishing. Do not leave the write as a separate later step, or behind an on-demand skill whose helper makes writing an optional flag. Check the result by confirming the deliverable exists after the helper's first run.
- **evidence**: Edit rows 1 and 4. base1 (no helper, no write instruction) and dom1 (helper behind a skill, run without `--write`) both ended with output/ empty after cross-checking. agg1 and inv1 (the write-inclusive command quoted in the system prompt) had the file on disk by their second and fourth actions, with identical correct numbers. The script and the prompt block were bundled, and the skill form differed in several ways, so the contrast supports "write-inclusive command in the always-on prompt" only as a bundle.
- **confidence**: low. There is one rollout per harness, the script and the prompt block were never tested apart, and dom1 differs from agg1/inv1 in more than one way. base1 and dom1 failing the same way could still be luck.

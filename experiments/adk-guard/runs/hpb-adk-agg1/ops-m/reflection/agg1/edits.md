component: skills/request-failure-stats (SKILL.md and scripts/request_failures.py) plus the trigger line in systemprompt.md
candidates: agg1 (the adopted bundle, shown in context/harness), dom1 (same skill with an in-script filter), inv1 (a different CLI and rule)
change: Added a skill and script for grouping retried requests by `req=`, judging the last attempt in UTC, treating the window as start-inclusive and end-exclusive, skipping traceback and req-less lines, and reading `.gz` files. The system prompt gained a line telling the agent to load the skill for this kind of task. The three candidates differ in detail. dom1 and agg1 use a positional `START END FILE...` CLI that judges the last attempt by UTC instant and flags a disagreement with the highest `attempt=`. inv1 uses a `logs --start --end --out` CLI, takes the highest `attempt=` as the last attempt, and writes the answer file itself.
observed: base1 never loaded a skill. It read `.gz` through `read_file` and got binary, hit a shell quoting error, resent the same broken awk command twice, and produced no deliverable. agg1, dom1 and inv1 all loaded the skill as their first action, ran the script once on all 3 files, and wrote `{"failed":19,"users":8,"top_code":"E401"}`. The dom1 and agg1 rollouts are identical. No run checks 19/8/E401 independently, so correctness is unverified. The skill and its trigger line were always added together, and the only baseline is one rollout.
verdict: confounded

component: systemprompt.md (sentence "Write the deliverable as soon as the computed numbers are in hand… Never answer from partial reading")
candidates: agg1 and inv1 (inv1 also adds "read the file back after writing"); dom1 omits it
change: Added a rule to write the output file as soon as the numbers are computed, and not to answer from partial reading. inv1 extended it with a read-back step.
observed: dom1 had no such sentence and behaved the same as agg1, which did have it. The inv1 rollout did not read the file back either. The sentence was not tested against a failure path.
verdict: no observed effect

component: tool_descriptions/tool_guidance.md (3 lines: `.gz` returns binary from read_file, don't resend a failed quoted command, large reads truncate)
candidates: agg1 (kept from inv1's edit); dom1 removes it
change: Added guidance aimed at the three failures seen in base1. The dom1 variant deletes these lines.
observed: In none of the three candidate runs did the agent call `read_file` on a `.gz` file or hit a shell error. The skill path ran straight to the script, so the guidance was never exercised. dom1 without it behaved the same as agg1 with it.
verdict: no observed effect

component: hooks.json and scripts/check_output.py (Stop hook that blocks finishing when output/ is empty or has bad JSON)
candidates: inv1 only
change: Registered a stop hook that exits 2 when no usable file is under output/ or a `.json` file does not parse.
observed: The hook never fired in the inv1 rollout, because the file was written correctly on the first try. The decision log dropped it as an unlisted component and a possible misfire risk. Its effect is untested.
verdict: no observed effect

component: skills/request-failure-stats/SKILL.md "Before writing" checks, including the naive ERROR-line sanity check
candidates: agg1 (the dom1 skill text with this check added)
change: Added checklist items: users ≤ failed, code counts sum to failed, every file passed to the script, and a comparison against a naive ERROR count. The "Workspace facts" block holding this task's own results was removed.
observed: The agg1 rollout did not run the naive-count comparison. It ran the script once and wrote the file. The agg1 trajectory is identical to dom1's, which lacks the naive-count line.
verdict: no observed effect

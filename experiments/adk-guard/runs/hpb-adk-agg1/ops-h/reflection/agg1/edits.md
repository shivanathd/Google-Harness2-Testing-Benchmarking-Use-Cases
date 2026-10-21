component: skills/service-traffic-report (SKILL.md and scripts/traffic_report.py)
candidates: agg1, dom1 (inv1 carried a near-duplicate under another name, see the next row)
change: Added a skill that classifies lines, excludes /healthz, counts errors as status >= 500, converts offsets to UTC, converts latency_s to ms per line, takes nearest-rank p95 and skips invalid JSON. A script reads the plain and gzip logs, computes the three fields and writes output/answer.json. The skill tells the agent not to read_file the logs. agg1 also added a "read RUNBOOK.md once and confirm the rules match" step and an os.makedirs call before writing. dom1 removed both.
observed: base1 (no skill) made 40 calls, mostly repeated whole-file read_file calls on gateway and search. It never opened the gzip file and ended with LlmCallsLimitExceededError and no deliverable. agg1 and dom1 loaded the skill as their first action and ran the script once on all three files. agg1 finished in 3 actions and dom1 in 4. Both produced identical numbers (billing 124/0.1613/393, gateway 96/0.1354/334, search 119/0.1513/192). Every skill-using run delivered and the only run without the skill failed. The skill, the system-prompt trigger and the tool-guidance line were all added together, so no run isolates the skill. Neither agg1 nor dom1 opened RUNBOOK.md, so the added runbook-check step was never exercised. The makedirs fix never mattered, because output/ already existed.
verdict: confounded
 
component: skills/log-traffic-report (SKILL.md and scripts/traffic_report.py)
candidates: inv1
change: A competing skill with a different name and the same job. It gave a 4-6 call step list, listed script defaults to compare against the runbook, and added a failure-recovery path. Its script includes an exit-1 guard when a service has zero requests and a unit audit count.
observed: inv1 made the same 4 actions (load skill, list_files, run script, write_file). It produced numbers identical to agg1 and dom1 and did not read RUNBOOK.md. The run shows nothing that separates this skill from the other.
verdict: no observed effect
 
component: systemprompt.md (trigger line naming the skill, and a 40-call budget sentence)
candidates: agg1 (trigger and budget), dom1 (trigger only), inv1 (reworded trigger and a longer budget sentence ending "A missing output file is the worst outcome")
change: Added a line that sends log-statistics tasks to the skill and says not to read whole logs. Added a sentence on the small call budget and not re-reading files.
observed: All three rollouts called load_skill first. base1, with no trigger line, never discovered the skill. The trigger line can't be separated from the skill itself, because no run has one without the other. The budget sentence is also unisolated. dom1 dropped it and inv1 reworded it, and both runs finished in the same 4 calls as agg1, which kept it. The run with the sentence omitted looks the same as the runs with it.
verdict: confounded
 
component: tool_descriptions/tool_guidance.md
candidates: agg1 and dom1 (one line: whole-log read_file floods context, gzip shows as binary, a missing output is the worst outcome); inv1 (three lines, including the billing.jsonl.gz filename, a FileNotFoundError note and a shell-quoting note)
change: Added guidance against whole-file read_file on logs.
observed: In every skill run the agent went straight to the script and never reached a point where this guidance would apply. No rollout shows it being read or acted on. inv1's filename-specific lines were never triggered either.
verdict: no observed effect

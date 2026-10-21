component: skills/log-traffic-report (SKILL.md plus scripts/traffic_stats.py), with a one-line trigger in systemprompt.md
candidates: agg1, dom1 (the two harnesses are byte-identical)
change: Added an on-demand skill that turns the RUNBOOK rules into a checklist: skip unparseable lines, convert mixed offsets to UTC, drop /healthz at any status, count status>=500 as errors, multiply latency_s by 1000 per record, nearest-rank p95, read gzip as text. It also adds a helper script that writes output/answer.json. The systemprompt line says to load the skill first for log-statistics tasks and to write the answer early.
observed: The base run (base1) made 40 read_file calls. Each call returned a truncated slice of the logs, it retried the nonexistent billing.jsonl, and it ended with LlmCallsLimitExceededError and no answer.json. In agg1 and dom1 the agent loaded the skill (call 1), ran the helper (call 2), and produced gateway 96/0.1354/334, search 119/0.1513/192, billing 124/0.1613/393. Neither run shows an unconverted-seconds error. Each run had one rollout, and the base run had a single failure, so the contrast is real but each side rests on one sample. agg1 and dom1 share the same harness, so they are not independent evidence.
verdict: helped (changed the outcome from no deliverable to a complete one; the skill and the trigger line were never tested separately, so neither is credited alone)

component: systemprompt.md, always-on "Working procedure" block (a call-budget rule, "read RUNBOOK.md first", .gz handling, run scripts/traffic_report.py, final re-read of answer.json, data checks)
candidates: inv1
change: Put about 12 lines of always-on procedure in the system prompt and added a scripts/traffic_report.py helper. It also added a no-shell fallback ("write by call 15") and a .gz FileNotFoundError note.
observed: inv1 finished in 3 calls: list_files, run the script, write_file. The nine values match agg1 and dom1 exactly. It never opened RUNBOOK.md, so the runbook-first rule it states was not followed. The script's stderr audit counts (unparseable, healthz, out_of_window, units) were printed. The rule set is the same as in the skill, so nothing distinguishes the two forms in outcome. They differ only in cost: the inv1 text is always loaded, while the skill loads on demand.
verdict: no observed effect (relative to agg1/dom1; it also fixed the base failure, but it is a single rollout confounded with the helper script)

component: LongTermMEMORY.md, guardrails.md, tool_descriptions/tool_guidance.md, README stubs
candidates: none
change: Left unchanged in all candidates.
observed: base1 failed through repeated truncated re-reads. The evidence does not point to these files as the cause.
verdict: no observed effect

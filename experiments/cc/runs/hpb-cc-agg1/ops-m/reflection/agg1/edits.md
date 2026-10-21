component: skills/service-log-incident-stats/SKILL.md (new file)
candidates: dom1
change: Added a skill covering the definitions (request as the unit, last attempt in UTC, half-open window) and the decoy line types (traceback lines, `cache warm after ERROR` lines with no `req=`). It also added a pre-write checklist and a "Workspace facts" section that hard-codes this instance's result (19 / 8 / E401, with code counts).
observed: dom1's first action was to load the skill. It then finished in 5 actions and wrote the same `{"failed": 19, "users": 8, "top_code": "E401"}` as base1. It reported line reconciliation, duplicate checks, and ±1-minute edge shifts, so the checklist was followed. The base1 run reached the same answer unprompted, so there is no accuracy difference. base1's trace uses a different format, so I couldn't count its calls. The decision notes say about six, against dom1's 5 and agg1's 7. The skill embeds the expected answer, which risks leakage on a different window or log set. One rollout per arm, so efficiency is not separable from noise.
verdict: no observed effect

component: systemprompt.md
candidates: dom1
change: Added one line telling the agent to load the `service-log-incident-stats` skill when a task asks for failure, user or error-code counts from service logs.
observed: dom1's first action was the skill invocation, so the trigger fired. It only delivered the skill, which is the other row. Its effect cannot be separated from the skill's.
verdict: confounded

component: scripts/README.md and skills/README.md (placeholder scaffolding)
candidates: agg1, inv1, dom1 (the harness has these two files, which base_harness lacks)
change: The `context/harness` tree has `scripts/` and `skills/` READMEs, each a one-line HTML comment. `base_harness` has neither. The agg1 and inv1 decisions say no edits were made. The `harness.diff` files for agg1 and inv1 are empty.
observed: No execution difference. agg1 and inv1 produced the same answer as base1 (19 / 8 / E401). inv1 re-derived it independently by both last-attempt definitions. agg1 took 7 actions and no extra behavior is attributable to the READMEs.
verdict: no observed effect

component: systemprompt.md, guardrails.md, LongTermMEMORY.md, tool_descriptions/tool_guidance.md (unchanged in all candidates)
candidates: agg1, inv1 (KEEP_BASE)
change: None. The adopted agg1 is equivalent to base.
observed: All four rollouts produced an identical deliverable. The base harness already handled the decoy lines, the gz file, mixed offsets and the half-open window. Adoption of agg1 reflects only that it was the sole final candidate, not that any edit helped.
verdict: no observed effect

component: skills/revenue-reconciliation/SKILL.md (new file)
candidates: dom1
change: Added a skill with a filter and conversion order, literal definitions of the two count fields, and a before-finishing checklist. It also had a "Workspace facts" section hard-coding this dataset's IDs (C09/C10, ch_028, cb_5) and the final result (5072.12 / 9 / 3).
observed: The dom1 rollout loaded the skill as its first action. It then produced 5072.12 / 9 / 3, which is identical to base1, inv1 and agg1. The rollout says it checked the skill's precomputed result against the data and it matched. It also says it worked the figure out by hand rather than by script. The base rollout got the same answer unaided, so nothing shows the skill changed the outcome. Part of the content is an answer leak, and that part cannot be separated from the procedural part.
verdict: no observed effect
component: systemprompt.md
candidates: dom1
change: Added one trigger line telling the agent to load `revenue-reconciliation` when a task turns payment exports into a period revenue figure.
observed: The dom1 rollout invoked the skill at its first step, so the trigger fired. The deliverable matched base1 exactly, so it made no difference to the result.
verdict: no observed effect
component: whole harness (inv1 and agg1)
candidates: inv1, agg1
change: KEEP_BASE. No files changed. The diffs against base are empty; the only difference is the empty scripts/ and skills/ README directories, which also exist in the adopted harness.
observed: Both runs gave `{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}`, identical to base1 and dom1. Base1 and agg1 were also identical, so unchanged harnesses can still vary in how they run. Four runs gave one identical answer. That shows the task was already within the base solver's ability. It cannot show that any edit helped or hurt.
verdict: no observed effect

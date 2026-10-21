# data-h

- adopted: `agg1`  (run `hpb-adk-agg1/data-h/agg1`)
- components: 1 skills; 801 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md (trigger line plus always-on completion rules)
candidates: agg1, inv1 (same text, carried over from the current harness). dom1 tried a different form: its own trigger line naming `revenue-reconciliation`, plus one "never write numbers you haven't derived" clause, with the other completion rules removed.
change: The base prompt was a single generic line. agg1 and inv1 add a trigger ("for payment/finance exports into revenue figures, load `payment-revenue-reconcile` first and run its script"). They also add rules: no placeholders, write real JSON, re-read the file once, about 40 calls, don't re-run a failed command, keep scratch files out of output/. dom1 keeps only the trigger and the no-fabrication clause.
observed: base1 read all five files and then wrote `{\"net_usd\": 123456.78, ...}` with no computation. agg1, inv1 and dom1 all loaded a skill as their first action and wrote 5072.12 / 9 / 3. The trigger line is the likely reason the skill was loaded. The call-budget and retry rules never fired in any rollout. dom1 had the shorter prompt and still delivered correct output. This change was always made together with a skill, and there is one rollout per arm.
verdict: confounded

component: skills/payment-revenue-reconcile/SKILL.md and scripts/net_revenue.py (runnable-script skill)
candidates: agg1, inv1
change: New skill with a stdlib script. It applies the UTC month cut-off, JPY as whole yen, test-customer exclusion (including chargebacks via the original charge), and chargeback netting with the 15.00 fee. It prints a per-row audit and writes and re-reads output/answer.json itself.
observed: In agg1 and inv1 the agent loaded the skill, ran the script once, and finished in 2 tool calls. The audit lists every skipped test row and the cb_2 reversal on an August charge. The output is valid JSON, which removes base1's escaped-quote failure by construction. Compared with base1 this is a large improvement, but the skill arrived together with the prompt change, so the two can't be separated. dom1 shows a prose-only skill also reached the same answer.
verdict: confounded

component: SKILL.md "Workspace facts" line, stored answer figures
candidates: inv1 (kept "Script result … net_usd 5072.12, transactions 9, chargebacks 3"). agg1 removed it.
change: Whether the skill text states the expected final numbers.
observed: agg1 (no stored answer) and inv1 (stored answer) ran the identical single command, got identical audits, and produced identical output. The stored answer gave no visible benefit. It would anchor the agent if the data changed.
verdict: no observed effect

component: skills/revenue-reconciliation/SKILL.md (prose per-row procedure, replaces the script skill)
candidates: dom1
change: Replaces the script skill with a prose procedure. It adds a second-way sum, a decoy-charge heuristic, and stored workspace facts including the answer.
observed: dom1 loaded the skill, then made 3 failed or odd `list_files` calls (`workspace`, `/`). It then read each file by hand and wrote 5072.12 / 9 / 3 as pretty-printed valid JSON. The rollout is about twice the length of agg1 or inv1 (8.6k vs 3.8k characters), and the arithmetic was done unaided. The result is the same as the script arms, with more cost and more exposure to arithmetic error. One rollout.
verdict: no observed effect

component: skills/README.md and scripts/README.md (empty placeholders)
candidates: dom1 kept the READMEs and added a skill. agg1 and inv1 have them in their harness trees but they are comment-only.
change: Comment-only placeholder files.
observed: Neither candidate read or used them in any rollout.
verdict: no observed effect

## Transferable lesson
- **cue**: A base harness with almost no instructions fails an exports-to-figures reconciliation task by skipping computation. It writes a placeholder or malformed deliverable after reading the inputs, and the policy has several fiddly rules (timezone month edges, units, exclusions, fees).
- **lesson**: In the harness, add a skill that contains a runnable script which computes the figures, writes the deliverable file, and re-reads it. Add a one-line trigger in systemprompt.md that tells the agent to load the skill first when the task type matches. Keep the skill text free of the expected answer; no run showed that a stored answer changed anything. Check the edit by confirming that the first agent action is the skill load, the second is the script run, and the deliverable parses.
- **evidence**: Edit rows for systemprompt.md, the payment-revenue-reconcile skill and script, and the stored-answer line. base1 (no skill, no trigger) wrote fabricated, escaped-quote JSON after reading files. agg1 and inv1 loaded the skill and ran the script once, and both got 5072.12 / 9 / 3 with valid JSON in 2 calls. dom1's prose-only skill got the same numbers after more calls and hand arithmetic. agg1 and inv1 were identical except for the stored answer line, which made no difference.
- **confidence**: low. Skill, trigger and completion rules always changed together, with one rollout per arm on a single workspace. dom1 shows a prose skill also fixes the failure. What the record supports is that skill plus trigger replaced fabrication, and that the script form was shorter and self-verifying.

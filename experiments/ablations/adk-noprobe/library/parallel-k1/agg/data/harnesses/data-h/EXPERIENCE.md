# data-h

- adopted: `agg1`  (run `hpb-adk-agg1/data-h/agg1`)
- components: 1 scripts; 2,620 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md (working rules: no placeholder figures, never end on a plan, read every input once, re-read the output, raw JSON with no escaped quotes)
candidates: agg1
change: Added generic working rules. The deliverable must be computed from the files, the output must be re-read and parsed, and write_file must get raw JSON.
observed: base1 read all five files and then wrote `{\"net_usd\": 123456.78, ...}` with escaped quotes. That is an invented placeholder and it does not parse. agg1 computed its figures and its file parsed as `{"net_usd": 5116.22, "transactions": 9, "chargebacks": 3}`. Two edits changed together here (these rules and the script), and each side has one rollout. I can't separate this rule set from the script's effect.
verdict: confounded

component: scripts/net_revenue.py, plus the exact run command in systemprompt.md (`--fee <flat fee stated in POLICY.md>`)
candidates: agg1
change: Added a stdlib script that applies the policy rules. It takes the UTC month of captured_at, converts minor units, excludes test customers from charges and chargebacks, and books the reversal plus fee in the chargeback_at month. It prints every recognised row and writes the JSON. The fee is a required `--fee` argument with no default.
observed: In agg1 the agent listed the directory, saw `scripts/net_revenue.py`, and ran it at once. It never opened POLICY.md and passed `--fee 0.30`. POLICY.md says the fee is 15.00 USD. The script's printout shows `fee 0.30` on each of the 3 chargebacks, so the net is understated in fees by about 3 × 14.70 = 44.10. That is 5116.22 where the correct figure is about 5072.12 (the decisions file also records 5072.12 as this data's figure). The counts (9 transactions, 3 chargebacks) match the policy logic. The script removed the placeholder and escaped-quote failure and produced correct counts. Making the fee a required argument that the prompt says to read from POLICY.md did not make the agent read the policy. It guessed the value.
verdict: helped (for structure and counts); the net_usd figure is wrong because of the fee argument

component: LongTermMEMORY.md
candidates: agg1
change: Added generic workspace layout and method notes. These cover UTC bucketing of mixed offsets, is_test exclusion, minor-unit divisors, fx as usd_per_unit, chargeback booking by chargeback_at, and a cross-check against POLICY.md. It states no fee value.
observed: The agg1 trajectory shows no sign that the agent used it. It did not cross-check the printout against POLICY.md, which would have caught the fee. Any behavior differences come from the script and the prompt.
verdict: no observed effect

component: guardrails.md, tool_descriptions/tool_guidance.md, plugin/README.md, skills/README.md
candidates: agg1
change: No content change. The plugin, scripts and skills directories are new scaffolding.
observed: None.
verdict: no observed effect

## Transferable lesson
- **cue**: A harness ships a calculator script that takes a policy-defined constant (fee, rate, threshold) as a required CLI argument. The rule text lives in a source file the agent can skip, because the script's printout looks complete.
- **lesson**: In systemprompt.md, make reading the policy file a required step before the script runs, and state that the argument value must be quoted from it. For example: "open POLICY.md, copy the fee line, then pass that number to --fee". Alternatively, have scripts/net_revenue.py parse the constant from POLICY.md itself, or refuse to run without a policy-derived value. Add a final check that compares each printed constant (such as the per-chargeback fee) with the policy text before the file is written.
- **evidence**: Edit rows "scripts/net_revenue.py + run command" and "systemprompt.md working rules". In agg1 the script removed the placeholder and escaped-quote failure seen in base1. The agent never read POLICY.md, though, and invented `--fee 0.30` where the policy says 15.00. That left net_usd wrong (5116.22 against about 5072.12) while the JSON was valid and the counts were right. The prompt's wording "fee stated in POLICY.md" and the memory note about cross-checking were both ignored.
- **confidence**: medium. The fee contrast is clear in one trajectory, and the correct figure is derivable from the policy text and the printout. The record has only one rollout per arm, and I did not independently recompute the full net.

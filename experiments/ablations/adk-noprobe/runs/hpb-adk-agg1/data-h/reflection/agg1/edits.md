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

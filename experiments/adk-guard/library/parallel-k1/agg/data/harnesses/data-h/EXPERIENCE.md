# data-h

- adopted: `agg1`  (run `hpb-adk-agg1/data-h/agg1`)
- components: 2 scripts, 1 hooks; 1,780 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md
candidates: agg1, inv1 (dom1 rewrote it differently)
change: The base prompt was one generic sentence. agg1 and inv1 expanded it in four ways. They forbid placeholder values. They say to start with `list_files "."` and not to probe "/". They point to `python3 scripts/net_revenue.py --month YYYY-MM`, with a by-hand fallback. They give method rules: convert to UTC, drop test customers, JPY is whole units, a chargeback can reverse a charge from any month, and count transactions before removing charged-back ones. inv1 also hard-coded this task's literal timestamps as examples. agg1 replaced them with the general instruction. dom1 instead cut the prompt back to the base sentence plus one line telling the agent to load the `revenue-reconcile` skill and not to write placeholders.
observed: base1 hit two path errors (`workspace`, then `/`) before finding ".". It read all five files, then wrote the placeholder `{\"net_usd\": 123456.78, \"transactions\": 12, \"chargebacks\": 3}` with escaped quotes and computed nothing. agg1 and inv1 ran `list_files "."` first, ran the script once, wrote the file, and finished in 3 calls. Their rollouts are essentially identical, so the literal-timestamp difference between them had no visible effect. dom1 had no orientation line. After loading the skill it called `list_files` on "/" and "/workspace" about 38 times and hit the 40-call limit with no output. This prompt change cannot be separated from the script it points to.
verdict: confounded

component: scripts/net_revenue.py
candidates: agg1, inv1 (dom1 removed it from its tree)
change: New stdlib-only Decimal script. It converts timestamps to UTC, keeps only captured charges, drops test-customer charges and chargebacks, reverses the full charge plus the 15.00 fee in the UTC month of `chargeback_at`, rounds once, and writes the three-key JSON. It prints diagnostics to stderr.
observed: In agg1 and inv1, one `run_command` produced `{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}`. The diagnostics flagged ch_028 as shifted into August UTC, the dropped test charges ch_090 and ch_091, and test chargeback cb_5. The agent then wrote that same content to output/answer.json. The decision notes say the author recomputed the figures independently from `source/` and matched. This is the only path that produced a correct deliverable. Neither agg1 nor inv1 read the CSVs or POLICY.md, so the script's fee default and rules were never checked against the policy in the run. The script ships with the prompt pointer, so the two effects are not separable.
verdict: confounded

component: hooks.json + scripts/check_output.py (Stop hook)
candidates: agg1, inv1
change: A Stop hook that blocks finishing if output/answer.json is missing, is not valid JSON, has the wrong types, or has a net figure with more than 2 decimals.
observed: The hook never fired in agg1 or inv1, because both wrote a valid file. base1's invalid placeholder is the case it was written for, but no run with the hook exercised it.
verdict: no observed effect

component: skills/revenue-reconcile (SKILL.md + scripts/recognise.py) plus the skill-trigger line in systemprompt.md
candidates: dom1
change: The method rules and a second helper script were packaged as a loadable skill instead of a root-level script. The agent had to load it first. The prompt dropped the "start with list_files '.'" guidance. In the version shown the skill text had already been stripped of instance-specific facts.
observed: The skill loaded fine, but the next 38 calls were all invalid `list_files` on "/" or "/workspace". The run hit the 40-call limit and wrote no answer. The skill's script path was never tried. The cause may be the missing orientation line, the skill indirection, or just a one-off rollout. base1 lacked the same line and recovered after two errors, so a single run does not isolate it.
verdict: confounded

component: plugin/README.md, skills/README.md, scripts/README.md (stubs)
candidates: agg1, inv1
change: Placeholder README files in the new directories.
observed: Nothing observable. No run read them.
verdict: no observed effect

## Transferable lesson
- **cue**: A task asks for exact figures computed from several exported data files under a written policy. The base harness has no executable tooling and a one-line prompt, and the agent can run commands.
- **lesson**: In `systemprompt.md`, name the deterministic helper script by its exact command, and keep the "start with `list_files '.'`, never probe '/'" line. Put the helper at a root-level path such as `scripts/` that the first directory listing shows. Do not hide the method behind a skill the agent must load first. Keep the prompt's method rules general (conversions, exclusions, count definitions) and leave out instance-specific timestamps or ids. After the helper runs, still check its stderr diagnostics against POLICY.md and the raw files, because its default fee and rules are fixed.
- **evidence**: Rests on the systemprompt.md and scripts/net_revenue.py rows, which carry the contrast only as a bundle. base1 had neither and wrote an invented, invalid-JSON placeholder after reading every file. agg1 and inv1 listed ".", ran the script, and wrote the correct file in 3 calls. dom1 put the method in a skill and cut the orientation line, then spent 38 calls on invalid path probes and delivered nothing. The dom1 failure is a single rollout with several simultaneous changes. The "root-level script, not a skill" part is therefore a hypothesis. The "pointer plus script beats bare prompt" part is better supported.
- **confidence**: low-medium. One task, one rollout per candidate, and agg1 and inv1 are near-duplicates, so they do not count as independent confirmation. The prompt and script were always changed together.

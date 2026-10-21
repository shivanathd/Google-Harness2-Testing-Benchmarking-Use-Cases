component: systemprompt.md (the "working method" section)
candidates: inv1, agg1 (the harnesses are identical, so this was one edit carried twice). dom1 deleted the section.
change: Added five bullets: derive every number from the rows, tally by hand with UTC conversion, apply exclusions to both lists, write raw JSON and read it back, and reconcile against the check script on a mismatch.
observed: The base rollout wrote the placeholder `{\"net_usd\": 123456.78,...}` straight after reading the files. The two rollouts with this text also wrote underived figures first. inv1 wrote 0.00, then 255891.87. agg1 wrote 0.00, then 119864.65, after re-reading the files three times. Neither rollout produced a per-row UTC tally. Both did write raw valid JSON, which base did not. This text is bundled with the hook in the same candidate, so no run isolates it. The record shows the "never write an underived number" bullet did not stop guessing.
verdict: confounded

component: scripts/check_output.py and hooks.json (Stop hook that recomputes the figure and blocks on a mismatch)
candidates: inv1, agg1 (identical). dom1 removed both.
change: Added a script that recomputes net, transactions and chargebacks from the CSVs under the hard-coded POLICY.md rules. It exits 2 with a per-row breakdown if answer.json is missing, is invalid JSON, or disagrees with the recomputation.
observed: In inv1 the agent wrote 255891.87 / 11 / 3. The hook returned exit 2 with the breakdown, the agent rewrote 5072.12 / 9 / 3, and the next run exited 0. In agg1 it wrote 119864.65 / 17 / 3, was blocked, then wrote 5072.12 / 10 / 3, and was blocked again on the count alone. It then wrote 5072.12 / 9 / 3 and passed. The delivered answer is correct in both. In dom1, which had no hook, nothing was delivered, though the failure was a workspace-path loop. Both agents used the breakdown to correct the figure rather than doing their own tally, so the correction came from the script. The script also hard-codes the month and the policy.
verdict: helped

component: skills/revenue-reconciliation/SKILL.md, plus the trigger line in systemprompt.md
candidates: dom1
change: Replaced the inline method and the hook with a loadable skill covering the method steps and the checks to re-derive from the files. A one-line trigger in the system prompt tells the agent to load it first.
observed: The agent loaded the skill, then called `list_files` on `/workspace` about 25 times. Each call failed with "outside the workspace", and it ended with "I cannot access the workspace directory". It never read the CSVs and delivered nothing. The loop did not come from the skill's text. The agent never tried `list_files` on `.`, which worked in the other rollouts. This is one rollout, and I cannot tie the failure to the skill.
verdict: confounded

component: guardrails.md, LongTermMEMORY.md, tool_descriptions/tool_guidance.md, plugin/skills README stubs
candidates: none changed them
change: Unchanged from base.
observed: No execution pointed to a defect in these files.
verdict: no observed effect

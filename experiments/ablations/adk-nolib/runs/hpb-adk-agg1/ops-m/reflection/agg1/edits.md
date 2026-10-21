component: skills/log-failure-stats (SKILL.md and scripts/log_failures.py)
candidates: inv1, agg1. agg1 is the adopted harness, and dom1's diff shows this skill removed from it. The skill is a log-stats helper script plus method notes.
change: Added a skill with a helper script. The script reads plain and gzip files (detected by magic bytes) and groups attempts by request id across all files. It converts timestamps to UTC, takes the latest attempt, and applies a start-inclusive, end-exclusive window. It skips lines that have no request id or are traceback text. It prints an audit block and exits 1 on a tied top code. The SKILL.md tells the agent to run the helper rather than hand-roll grep/awk, and it lists three re-derivation checks.
observed: In base1 there was no skill. The agent read the `.gz` file through `read_file` and ran a grep/awk pipeline. It then sent the same quote-broken command twice (exit=2 both times) and wrote no `output/answer.json`. In inv1 and agg1 the agent's first action was `load_skill log-failure-stats`. It then ran the helper once (exit=0) and wrote `{"failed":19,"users":8,"top_code":"E401"}`. agg1 passed the window as naive `2026-10-06T08:00:00`, and the script treats naive times as UTC, so it worked. Each arm ran once. The skill was changed together with the systemprompt bullets, so this skill's effect is not isolated from theirs. dom1, a different skill without the bullets, also succeeded. That suggests some skill-with-helper was enough here.
verdict: confounded

component: skills/log-incident-stats (SKILL.md and scripts/log_stats.py)
candidates: dom1
change: An alternative skill with seven method rules and a helper script. Its last attempt is the highest `attempt=` number, not the latest timestamp. The script drops exact-duplicate lines. It requires a strict `req= user= attempt=` header. It takes ISO timestamps with an offset. It only warns on ties and does not exit non-zero.
observed: dom1 loaded the skill (`load_skill log-incident-stats`) and ran the helper once with `+00:00` bounds (exit=0). It wrote the same 19/8/E401 as inv1 and agg1. In this data the highest attempt number and the latest timestamp pick the same last attempt, so the two helper designs gave the same answer. The two skill forms are not distinguished by outcome. Nothing shows whether the differences (duplicate dropping, tie handling) matter.
verdict: no observed effect

component: systemprompt.md, working-order bullets (inspect briefly and script it, write early and reopen, do not finish without output/, fix a failing command once, never resend it)
candidates: inv1, agg1. dom1 omitted them and kept only a trigger line.
change: Added three general bullets covering working order, a never-resend-a-failed-command rule, and a switch-approach-after-two-failures rule.
observed: Neither inv1 nor agg1 hit a shell error. Both went straight from the skill to one helper run, so the error-recovery bullets never fired. The first-action choice (`load_skill`) is explained by the trigger line below. dom1 produced the same answer without these bullets. There is no execution evidence for or against them.
verdict: no observed effect

component: systemprompt.md, trigger line
candidates: inv1, agg1 (naming `log-failure-stats`); dom1 (naming `log-incident-stats`)
change: A one-line pointer sent log-statistics tasks to a skill. Both forms named the skill.
observed: All three arms invoked `load_skill` as their first action. base1 had no pointer and never loaded a skill. It went directly to `read_file` and grep. The pointer is the most plausible reason the agent used a helper. But the skill content changed at the same time, and each arm ran once.
verdict: confounded

component: hooks.json and scripts/check_output.py (Stop hook that blocks finishing until output/ has a well-formed deliverable)
candidates: inv1
change: Added a Stop hook that exits 2 if `output/` is empty or its JSON does not parse. It is absent from agg1, the adopted harness.
observed: inv1 wrote a valid `output/answer.json` on its first helper run. Nothing in the trajectory suggests the hook blocked or changed anything. In base1 the failure was an agent that never wrote a file, and that case was not run with the hook.
verdict: no observed effect

component: guardrails.md, LongTermMEMORY.md, tool_descriptions/tool_guidance.md
candidates: none (unchanged in all three candidates)
change: No edits.
observed: No difference.
verdict: no observed effect

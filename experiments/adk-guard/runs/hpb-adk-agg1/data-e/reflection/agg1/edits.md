component: scripts/net_revenue.py (new; stdlib-only helper with a required `--month`)
candidates: inv1, agg1 (same file in both; dom1 did not carry it)
change: Added a script that parses ISO and "Mon DD, YYYY" dates, thousands separators and "(x)" accounting negatives. It dedupes by txn_id, filters status and month by parsed date, multiplies by the fx rate, and rounds once. It writes `{"net_usd","transactions"}` and prints a diagnostic line (duplicates, conflicts, included count) to stderr.
observed: base1 hand-wrote a pandas script. It filtered months with `str.contains('Sep')`, then crashed on `float('(954.34)')` and reran the failing script until the 40-call limit, so it never wrote answer.json. inv1 and agg1 ran the script once after `list_files` and got 18691.64 / 21 in about 2 commands. dom1 reached the same answer with its own equivalent script, so the helper-script idea is supported by two independent implementations. The comparison is one rollout per arm, and the file was never tested without the systemprompt pointer.
verdict: confounded (the script and the systemprompt pointer to it always shipped together, so neither effect is isolated; the base1 vs helper-script contrast is clear but rests on one rollout per arm)

component: systemprompt.md "Working rules" block plus the settled-revenue pointer paragraph
candidates: inv1, agg1 (inv1 wording: "first attempts with pandas failed… '(954.34)' crashed"; agg1/current wording: "hand-written pandas attempts failed… accounting negatives crashed float()"); dom1 added only a short trigger line plus "don't rerun an unchanged failing command"
change: Added call-budget rules: write the deliverable early, never rerun an unchanged failing command, fall back to stdlib if pandas is missing, start with list_files, inspect distinct formats, and recheck the output shape. It also tells the agent to use the helper script and check its stderr diagnostics. The wording was generalised from the literal "(954.34)" to "accounting negatives" in agg1.
observed: In inv1 and agg1 the agent ran `list_files`, then went straight to the script. The working rules had no visible effect because the script succeeded on the first run, so the failure-recovery rules never fired. The only visible effect of the pointer is that the agent used the script. The agg1 vs inv1 wording difference changed nothing observable.
verdict: confounded (the pointer is inseparable from the script, and the working rules were never exercised)

component: hooks.json + scripts/check_output.py (Stop hook validating output/answer.json)
candidates: inv1, agg1
change: A Stop hook that exits 2 if answer.json is missing or its keys or types are wrong.
observed: It never fired. Every run wrote a valid file on the first command. The record shows nothing for or against it.
verdict: no observed effect

component: skills/payment-revenue-reconcile/ (SKILL.md plus settled_revenue.py) and its trigger line in systemprompt.md
candidates: dom1
change: Added a skill with a stdlib reconcile script and a quirk and checklist document. The quirks were this workspace's specifics: six duplicate rows, mixed dates, CRLF line endings, and USD/EUR/INR. The prompt got a trigger line to load the skill.
observed: The agent called `load_skill`, then ran the script once and got 18691.64 / 21. The per-currency reconciliation printed in its output was a useful cross-check. Its result was the same as the other two helper-script candidates, and it took about as many steps.
verdict: no observed effect (equal to the plain script; it added a skill-loading step and workspace-specific text for no measured gain)

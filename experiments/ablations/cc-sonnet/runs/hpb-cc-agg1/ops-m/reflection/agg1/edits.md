component: systemprompt.md (procedure block for log-analysis tasks)
candidates: agg1, inv1 (identical harnesses); dom1 carried a different form
change: The base prompt was one generic paragraph. agg1 and inv1 added a procedure block with four parts. (1) Compute with a script and run `scripts/request_failures.py logs START END`. (2) Workspace facts: req-less INFO lines and indented traceback lines quote look-alike ERROR text, the window applies to the last attempt, and file order is not time order. (3) "Write the deliverable as soon as the numbers are computed, then reopen it and confirm keys and types. Computing and printing without writing is not finishing." (4) Report ties instead of guessing. dom1 replaced all of that with a one-line trigger telling the agent to load the `log-incident-stats` skill first, plus a short "write the file as soon as numbers are computed" sentence.
observed: base1 computed 19/8/E401 with a hand-rolled parser and its last action was the printout; `output/` stayed empty and the deliverable reads "(no deliverable produced)". agg1 and inv1 both ran the script, then ran it again with `--write output/answer.json`, reopened the file and asserted keys and types. Both ended with `{"failed": 19, "users": 8, "top_code": "E401"}` on disk. dom1 had the short write-reminder but still ended on the printout with no file. The extra write-before-finish sentence in dom1 was therefore not enough on its own. The explicit "printing is not finishing" instruction plus a re-open check coincided with delivery in the two rollouts that had them. Each harness has only one rollout, and the script and prompt changed together, so the prompt's own contribution is not isolated.
verdict: confounded

component: scripts/request_failures.py
candidates: agg1, inv1 (top-level `scripts/`); dom1 (copy under `skills/log-incident-stats/scripts/`)
change: A new script reads `app.log*` including gzip, groups attempts by req across files, converts offsets to UTC, takes the last attempt, and applies a half-open window. It prints each failed request and the counts. `--write` emits the three keys and refuses to write on a tie or on zero failures.
observed: Every rollout got the same answer, 19/8/E401, with or without the script. base1 used its own parser and agreed. The script did not change the numbers. What it changed is that one command computes and writes. agg1 and inv1 used it with `--write` and delivered. dom1 ran the same script without `--write` and delivered nothing. The script alone does not guarantee a file. In dom1 its path was also nested in the skill directory.
verdict: confounded

component: scripts/check_output.py and hooks.json (Stop hook)
candidates: agg1, inv1
change: Added a Stop hook that blocks finishing while `output/` is empty or holds invalid JSON.
observed: It never fired. In agg1 and inv1 the file was already written and verified before the agent finished. The hook targets exactly the failure seen in base1 and dom1, but no trace shows it intervening.
verdict: no observed effect

component: skills/log-incident-stats/SKILL.md and the skill trigger line
candidates: dom1
change: Moved the log-analysis knowledge into a skill: rules for last attempt, UTC window, noise lines and ties, a finish section, and a cross-check section. The system prompt only says to load the skill first.
observed: In dom1 the agent loaded the skill and ran the script from the skill path. It stopped at the printout and wrote no file, even though the skill's Finish section says computing without writing is not finishing. The rule sat in a skill file read earlier, and the agent did not act on it at the end. Only one rollout stands behind this.
verdict: confounded

component: plugin/README.md, skills/README.md, scripts/README.md
candidates: agg1, inv1, dom1
change: Placeholder README files in the scaffolding directories.
observed: None.
verdict: no observed effect

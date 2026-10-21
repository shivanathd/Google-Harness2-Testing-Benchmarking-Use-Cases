component: systemprompt.md
candidates: agg1, dom1, inv1
change: agg1 adds one trigger paragraph naming `log-window-stats` for incident or traffic statistics over a time window. dom1 adds a one-sentence trigger for counts, distinct users, or top code from a timestamped log. inv1 replaces the trigger with a six-step procedure: read CLAUDE.md; load the skill; one script pass over every record; write the file before anything else, since "a run that ends with the figures only in the transcript has failed"; run `scripts/check_json_output.py`; finish with a one-line message. The base sentence "write the requested deliverables under output/" is kept in all three.
observed: In all three candidate runs the first action is `Skill log-window-stats` (rollouts/dom1.md:1, inv1.md:1, agg1.md:1). base1 has no skill to load and its first action is an `ls` (base1.md:1). base1 printed the figures from its own /tmp script (base1.md:208–226) and never wrote output/answer.json. Each candidate wrote it (dom1.md:202, inv1.md:163, agg1.md:148). All four computed 15/6/E500. No run read CLAUDE.md, although it was listed in each (base1.md:6, dom1.md:175, inv1.md:10, agg1.md:10) and inv1's step 1 asks for it. CLAUDE.md is systemprompt plus 20 bytes in every arm, so the miss had no visible effect.
verdict: confounded

component: skills/log-window-stats/SKILL.md
candidates: agg1, dom1, inv1
change: Three different forms, with no shared text. agg1: deliverable contract (named file is the deliverable, exact keys and types, one-line final message), header-only event rule, UTC time rule, statistics with tie and empty-window rules, helper at `<skill-dir>/scripts/`, consistency checks, and a verify command. dom1: the same contract, event, time, and statistics sections plus a consistency list, no helper, and a "facts observed in this workspace" section with this app.log's counts, offset forms, and traceback mismatch. inv1: a six-step procedure whose helper path is `skills/log-window-stats/scripts/` (no `.claude` prefix), with evidence checks (unparsed empty, headers plus continuation equal `grep -c .`, levels contain the task level) and a tie rule. inv1 has no deliverable contract and no final-message line; it defers key shape to the systemprompt checker step.
observed: Figures were identical in all three (15/6/E500). agg1 listed the helper directory (agg1.md:4), ran it from `.claude/skills/...` (agg1.md:15), compared 130+33 headers and continuation lines with `grep -c .` = 163 (agg1.md:140, 147), wrote the file (agg1.md:148), and ran the SKILL's verify command verbatim (agg1.md:151; SKILL line 35). It ends with no closing line, although SKILL line 11 asks for one. dom1 never used its facts section. It wrote its own parser (dom1.md:180), checked the per-code sum (dom1.md:201), wrote the file (dom1.md:202), verified it with its own one-liner (dom1.md:203–207), and gave no closing line. inv1 ran the helper from `.claude/skills/...` (inv1.md:20), although its SKILL names `skills/...`. The path was written before the listing that showed it (the listing is in the same command output), so this was not a correction after observation. inv1 ran the checks its SKILL lists (inv1.md:156–162), wrote the file, ran the checker, and gave the one-line close (inv1.md:175–177).
verdict: confounded

component: skills/log-window-stats/scripts/window_stats.py
candidates: agg1, inv1 (byte-identical copies)
change: New read-only helper. It parses header lines, requires explicit UTC offsets, converts timestamps to UTC, applies a half-open window, and prints JSON with count, users, top_code, codes, headers, continuation_lines, levels, and unparsed.
observed: inv1 ran it once (inv1.md:20–155) and agg1 ran it once (agg1.md:15–138). Both returned count 15, users 6, top E500, headers 130, continuation 33, unparsed []. Without the helper, base1's own script (base1.md:208–226) and dom1's stats.py (dom1.md:180–199) also returned 15/6/E500. The helper did not change any figure. It replaced hand-written parsing in two runs.
verdict: no observed effect

component: scripts/check_json_output.py
candidates: inv1
change: New checker. It loads the JSON file and compares its key set and value types with `name:type` specs, printing problems and exiting 1, or printing OK.
observed: inv1 ran it once (inv1.md:164) and got `OK output/answer.json` (inv1.md:168). The file was already correct, so the checker had no failure to catch. dom1 and agg1 checked shape with a one-line parse (dom1.md:203, agg1.md:151). base1 wrote no file.
verdict: no observed effect

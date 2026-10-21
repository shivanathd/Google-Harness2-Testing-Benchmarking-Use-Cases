# ops-m

- adopted: `agg1`  (run `hpb-adk-agg1/ops-m/agg1`)
- components: 1 skills; 842 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: skills/request-failure-stats/ (SKILL.md and scripts/request_failures.py), new
candidates: agg1, inv1
change: Added a skill with a script that reads every file in the log directory and detects gzip by magic bytes. It skips indented traceback lines and lines with no `req=`. It groups attempts by request across files, takes the highest `attempt=` as the last attempt, and checks that against the latest UTC time. It applies the [start, end) window in UTC, counts a request as failed only if its last attempt is ERROR, and writes the three-key JSON. It exits 2 on ambiguity and 3 on a tie.
observed: base1 never loaded such a skill. It read the `.gz` with `read_file` and got binary garbage. It then counted per-line ERRORs with grep/awk, which is the wrong unit, and ended with no `output/answer.json`. In agg1 and inv1, whose rollouts are byte-identical, the agent loaded the skill as its first action and ran one script command. That command exited 0 with 110 requests, failed=19, users=8, E401, and wrote the deliverable. All of this changed at once (skill, trigger line, tool guidance), and the only baseline is one rollout, so the script's own contribution is not isolated.
verdict: confounded

component: systemprompt.md (trigger line)
candidates: agg1, inv1 (naming `request-failure-stats`); dom1 (naming `log-request-outcomes`)
change: Added one paragraph. It says to load a named skill for count, user or top-code questions over service logs, never to answer from a quick read, and to reopen the deliverable. The agg1/inv1 version also says "make sure output/answer.json exists before you stop". The dom1 version asks for "an explicit per-request list or the skill's script".
observed: In all three candidates the first action was `load_skill` with the named skill, so the trigger line fired. base1 had no such line and went straight to read_file/grep. This does not isolate the line from the skill's existence. The two wordings produced identical outcomes. None of the candidate rollouts reopened the deliverable, so that clause had no observable effect.
verdict: confounded

component: skills/log-request-outcomes/ (SKILL.md and scripts/request_outcomes.py), new
candidates: dom1
change: Added a skill with equivalent rules: group by request, take the last attempt, convert to UTC, skip traceback and cache-warm lines, handle gzip. Its script takes explicit file paths, rejects ties and unparseable lines, and writes the JSON. It also includes a workspace-fact cross-check.
observed: dom1 loaded it and ran one command. It listed 19 failed requests and wrote `{"failed":19,"users":8,"top_code":"E401"}`, the same deliverable as agg1/inv1. Its rollout was shorter (57 lines against 89 for agg1), but only because of a shorter SKILL.md. This is a second, differently written implementation that reaches the same result, so the shape of the skill matters more than its wording.
verdict: confounded

component: tool_descriptions/tool_guidance.md
candidates: agg1, inv1
change: Added two lines. The first says `read_file` shows `.gz` as binary garbage, so use gzip or the script. The second says that after a shell syntax error you should not resend the command but write a .py file, and that after two failed attempts you should switch approach.
observed: Both lines target base1's failures (the `.gz` read, and the unclosed-quote command sent twice). In the candidate rollouts the skill's script ran first and cleanly, so neither failure situation arose and the lines never fired. dom1 did not change this file.
verdict: no observed effect

component: scripts/README.md and skills/README.md (placeholder stubs)
candidates: agg1, inv1 (removal of the skills README stub)
change: Removed comment-only placeholder files.
observed: Nothing observable. The candidate rollouts did not depend on them.
verdict: no observed effect

## Transferable lesson
- **cue**: A task over raw operational data, such as rotated or compressed logs, with mixed time zones, retries and tricky continuation lines. The unit of analysis (a request) differs from the unit of the raw rows (a line). A baseline run read the data by eye or with ad-hoc shell and delivered nothing.
- **lesson**: In the harness, add a skill whose script does the whole pipeline (decompress by magic bytes, group rows into the analysis unit, apply the window in UTC, count, and write the deliverable file itself). Add one trigger line in systemprompt.md that names that skill and says to load it instead of reading the raw files. Have the script exit non-zero on ties or ambiguity so the agent has a defined stop condition. Then check the new rollout for the same first move: a `load_skill` call followed by a single script run that writes the output file.
- **evidence**: The skill-plus-trigger-line edit rows (agg1, inv1, and dom1 with a differently written skill) against base1. base1 used read_file on the .gz and per-line grep, resent a broken shell command, and wrote no answer. All three candidate rollouts started with load_skill and one script run, and each wrote the identical 19/8/E401 answer. The tool_guidance lines did not fire, so the lesson does not rest on them.
- **confidence**: low. Only one baseline rollout and one rollout per candidate exist, and the three candidates carried the same kind of edit, so the contrast is skill-versus-no-skill and not between components. The task is also small and deterministic, so the effect may not carry over to open-ended analysis.

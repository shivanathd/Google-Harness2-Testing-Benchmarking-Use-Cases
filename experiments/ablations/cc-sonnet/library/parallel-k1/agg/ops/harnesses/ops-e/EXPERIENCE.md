# ops-e

- adopted: `agg1`  (run `hpb-cc-agg1/ops-e/agg1`)
- components: 2 scripts, 1 hooks; 1,505 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md (log-analysis procedure block)
candidates: inv1, agg1 (identical harnesses). dom1 replaced the block with a one-line trigger for a skill.
change: inv1 and agg1 added four rules to the always-loaded prompt.
- Compute with a script, not by eye.
- Preview the log shape. Only the level token right after the timestamp counts. Take user and code from the header line, not from indented traceback lines or from INFO lines that quote "ERROR".
- "Write the deliverable as soon as the numbers are computed, then reopen it… Computing without writing is not finishing."
- On a tie or no matches, re-check and state it.
dom1 instead added "load the `log-incident-stats` skill first" and no write instruction.
observed: Both rollouts with the procedure delivered a valid answer.json.
- inv1 ran the script with `--write`, then reopened the file and checked keys and types.
- agg1 grepped the other "ERROR" mentions to confirm they were indented or INFO lines, then wrote and verified the file.
base1 (no procedure) computed 15/6/E500 correctly with its own throwaway script, but the trajectory ends on that printout and `output/` stays empty.
dom1 (skill, no write rule) also computed correctly, ran a missed-timestamp grep, and ended there with nothing produced.
All four rollouts got the numbers right, so the prompt block did not change correctness. It changed whether the file got written.
Which sentence did the work is not isolated, because the script and hook shipped alongside it.
verdict: confounded

component: scripts/log_window_stats.py
candidates: inv1, agg1
change: New CLI that parses header lines only, converts offsets to UTC, and applies a half-open window. It prints every matched event and the counts. `--write` emits the three-key JSON. It exits 1 and writes nothing on a tie or when no events match.
observed: In both inv1 and agg1 the agent ran it and then re-ran it with `--write`, so computing and writing took one command. base1 and dom1 each wrote an ad-hoc parser that only printed, which is where they stopped.
The agg1 trace shows the agent first read the script's source in its `head` output, then trusted it.
No rollout had a tie, so the guard was never exercised.
verdict: confounded

component: scripts/check_output.py and hooks.json (Stop hook)
candidates: inv1, agg1
change: A Stop hook runs `check_output.py`. It exits 2 if `output/` is empty or a file is empty or invalid JSON.
observed: No trace shows the hook blocking anything. Both rollouts had already written the file before finishing and also called `check_output.py` by hand, getting OK / check=0. base1 and dom1 had no hook and ended with an empty `output/`.
Whether the hook fires in the real run is not visible in the transcripts.
Its contribution is therefore unobserved.
verdict: no observed effect

component: skills/log-incident-stats/SKILL.md
candidates: dom1
change: Added an on-demand skill with event-definition rules, UTC and half-open window rules, counting rules, and consistency checks. The system prompt got a trigger line pointing at it. The scripts and hook were removed.
observed: dom1 loaded the skill as its first action. It parsed correctly and ran extra checks: a header/continuation line-count split and a missed-timestamp grep. Then it ended without writing `output/answer.json` ("nothing produced"). The skill's last check, "Write it as soon as the checks pass", did not prevent that. The method guidance matched the other rollouts' numbers but gave no mechanism for writing the file.
There is one rollout, and the skill also removed the script and hook.
verdict: confounded

## Transferable lesson
- **cue**: An agent computes a correct result with an ad-hoc script and then finishes without writing the required deliverable file. The trajectory ends on a printout, and `output/` is empty.
- **lesson**: In the always-loaded `systemprompt.md`, add a rule that computing is not finishing and that the deliverable must be written and reopened. Also ship a helper under `scripts/` where one command both prints the matched evidence and writes the exact-schema file (a `--write` flag). Do not rely on an on-demand skill that only carries analysis rules. When choosing between edits, check that the executing rollout ends with the file on disk, not only that the numbers are right. The record did not isolate whether the prompt rule or the script mattered more, so ship both.
- **evidence**: Edit rows for systemprompt.md, log_window_stats.py and the skill (all confounded individually).
- **confidence**: low-medium. The delivered and non-delivered split is 2 vs 2, one rollout per arm, and the winning arm bundled prompt, script and hook. The Stop hook was never seen firing. The failure mode itself is clearly visible in two trajectories, which is the reason to keep the entry.

# ops-h

- adopted: `agg1`  (run `hpb-adk-agg1/ops-h/agg1`)
- components: 1 skills; 1,194 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: skills/service-traffic-stats/SKILL.md and skills/service-traffic-stats/scripts/traffic_stats.py (new skill with a helper script)
candidates: agg1
change: Added a skill that describes the method: half-open UTC window, probe-route exclusion, error = status >= 500, per-record latency unit conversion, nearest-rank p95. It ships with a helper script that reads gzip by magic bytes, skips truncated JSON lines, applies those rules, prints skip and unit tallies, and writes answer.json. The skill has no instance data, with window values as placeholders. It includes a no-shell fallback.
observed: In base1 the agent never reached a computation. It made 12 `list_files` and 28 `read_file` calls, re-read the 260-line logs, hit the 40-call limit and produced no deliverable. In agg1 the first action was `load_skill`. One `run_command` of the helper then produced all three services, including billing's mixed `latency_ms` (68) and `latency_s` (56) records, and wrote `output/answer.json`. The whole run took about 3 tool calls. The `units=` census and `invalid_json` tallies printed in the output.
verdict: helped (the strongest candidate for the cause of the base1-to-agg1 contrast, but the systemprompt edit was needed to trigger it, and there is one rollout per arm)

## Transferable lesson
- **cue**: A solver is given a data-analysis task over raw files (logs, mixed formats, compressed or truncated records) with a hard model-call budget. The base run spent the whole budget viewing raw files through a read tool and never wrote the deliverable.
- **lesson**: In the harness, add a generic skill (a SKILL.md plus a deterministic helper script that parses the files, applies the rules and writes the output file), and add a line to systemprompt.md that names the skill and says when to load it. Keep window bounds and expected values out as placeholders. A solver that loads the skill can finish in a few calls, instead of reading data by hand until the budget runs out.
- **evidence**: Skill and helper row, plus systemprompt row. base1 made 40 calls (28 `read_file`, 12 `list_files`) with no output. agg1 made `load_skill`, `list_files` and one `run_command`, and wrote a complete answer.json whose counts include per-record unit handling, truncated-line skipping and probe exclusion. The contrast is a single rollout per arm. The skill and the trigger line were never tested separately.
- **confidence**: medium. The contrast is large and its mechanism is visible in the trajectories (skill loaded, helper run). However, there is one rollout per arm, the edits were bundled, and nothing shows the helper's rules were checked against the RUNBOOK in the run itself.

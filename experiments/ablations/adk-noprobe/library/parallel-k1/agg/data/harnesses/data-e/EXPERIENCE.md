# data-e

- adopted: `agg1`  (run `hpb-adk-agg1/data-e/agg1`)
- components: 1 skills, 1 scripts; 1,506 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: tool_descriptions/tool_guidance.md, LongTermMEMORY.md, guardrails.md
candidates: agg1
change: Nothing. These files are identical to base_harness in the adopted harness and in the pool copy.
observed: Neither rollout shows any behavior tied to these files.
verdict: no observed effect

component: systemprompt.md (working rules: stdlib-only Python, never rerun a failed command unchanged, inspect the input once, write the deliverable early and check its shape)
candidates: agg1
change: Added a short always-on block aimed at base1's failure. In base1 the agent used pandas, hit a ModuleNotFoundError and a pip timeout, then re-ran the same crashing command about 32 times until the 40-call cap, and no answer.json was written.
observed: agg1 never hit the failure these rules guard against. It made two actions and no error occurred, so the rules were never exercised. Nothing shows whether they would stop a retry loop. It also never opened the input files, so "inspect the whole input once" did not run. Its answer.json has the requested object shape, but that comes from the script's own check.
verdict: no observed effect

component: systemprompt.md (trigger line: load the payment-revenue-reconcile skill, then run scripts/net_revenue.py with a fallback to a hand-written stdlib script)
candidates: agg1
change: Routed the agent to the skill, then to the one-line script invocation, and told it to sanity-check the output.
observed: agg1's first action was load_skill, and its second was exactly the prompted command `python3 scripts/net_revenue.py transactions.csv fx.csv 2026-09 output/answer.json`. That produced {"net_usd": 18691.64, "transactions": 21}, and the agent returned it. Base1 took a different route: it listed files, read both CSVs, and wrote a pandas script. The trigger line plausibly caused the divergence, because the script call mirrors its wording. But the line, the skill and the script were added together and there is one rollout per arm, so none is isolated. The fallback sentence was never used.
verdict: confounded

component: scripts/net_revenue.py (new; replaces scripts/README.md)
candidates: agg1
change: Added a stdlib-only script. It dedupes txn_id, parses ISO and "Sep 05, 2026" dates, handles thousands commas and parenthesised negatives, filters on SETTLED plus the parsed year and month, multiplies by usd_per_unit, rounds half-up once, writes {"net_usd","transactions"}, and re-reads the file to check its shape.
observed: In agg1 it ran with exit=0 and reported the 6 exact-duplicate rows skipped. It found 36 unique ids, and the final answer is 21 transactions and 18691.64. Each of base1's code bugs maps to a script feature. Base1's `str.contains('Sep')` filter misses ISO dates, and the script parses dates properly. Base1 never deduped, and the script dedupes. Base1's bare float() crashed on '(954.34)', and the script parses it. Base1 would have written a list-shaped JSON, and the script writes an object. The deliverable in agg1 is the script's own output. The decision log also says scripts/ might not be reachable in the solver workspace. agg1 shows it was. This is the component the successful path most directly runs through. Even so, it came with the prompt and skill edits and there is one rollout per arm, so I cannot attribute the gain to it alone.
verdict: confounded

component: skills/payment-revenue-reconcile/SKILL.md
candidates: agg1
change: Added an on-demand skill with generic rules: dedupe on key, parse amounts and dates, exact status match, keep refunds, multiply by the FX rate, round once, check the output shape. It also has a reconciliation identity and export-specific checks, with task data removed after an earlier rejection.
observed: agg1 loaded it as its first action. Nothing afterward shows the agent applying it. It never printed distinct statuses, never checked the reconciliation identity, and never inspected the raw data. The script did the work. The skill's content had no visible effect in this run, though loading it cost one call out of a 40-call budget.
verdict: no observed effect

component: plugin/README.md, scripts/README.md, skills/README.md
candidates: agg1
change: Scaffolding or placeholder README files. The decision log notes the scripts README was dropped in favor of the script.
observed: No trace shows any of them being read.
verdict: no observed effect

## Transferable lesson
- **cue**: A recurring export-cleaning task (mixed date and amount formats, repeated keys, FX conversion) where the base run died in a retry loop on its own hand-written parsing code and delivered no output file.
- **lesson**: In the harness, ship a tested stdlib-only helper under scripts/ that does the whole computation, parse, dedupe, filter, convert and write the deliverable, and have systemprompt.md name its exact one-line invocation. Tell the agent to fall back to a hand-written stdlib script if the helper is missing or fails. Before relying on it, confirm scripts/ is reachable from the solver workspace.
- **evidence**: Rows "scripts/net_revenue.py" and "systemprompt.md trigger line", both confounded, plus the base1 versus agg1 contrast. base1 hand-wrote a pandas script that crashed and repeated the same command about 32 times until the cap, with no answer.json. agg1 loaded the skill and ran the prompted script command. It exited 0, reported the 6 duplicate rows skipped, and wrote a correct-shaped answer.json after two actions. agg1 also shows scripts/ was reachable in the solver run, which the decision log had flagged as unconfirmed.
- **confidence**: low. This is one rollout per arm, and the helper, the invocation line, the skill and the working rules were all added together. The retry-loop rules were never exercised in agg1, so only "a ready, invoked script yields a delivered file" is observed, not which part caused it. The record also does not show that the output is correct beyond the script's own checks.

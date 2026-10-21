# data-m

- adopted: `agg1`  (run `hpb-adk-agg1/data-m/agg1`)
- components: 2 scripts, 1 hooks; 2,340 always-on chars

## Why this was chosen
trivial pool: single final at k=1; delivered without a selector session

## What each edit did
component: systemprompt.md (revenue-reconciliation paragraph that points to `scripts/net_revenue.py` and states the domain rules)
candidates: dom1, inv1, agg1
change: The base prompt was one sentence ("complete the task, write under output/"). Every candidate added a paragraph that tells the agent to run `python3 scripts/net_revenue.py --month YYYY-MM`. dom1 and agg1 also spelled out the rules: settled_on/refunded_on month logic, the refund's own currency and day rate, dedupe by txn_id, a zero fx rate raised only if needed, and a boundary-row check. inv1 used a longer "Working rules" block (about a 40-call budget, a pandas fallback) plus a short description of the helper and the data.
observed: base1 read all three CSVs, ended on a plan in prose, and wrote no `output/answer.json`. Its last fx rows showed INR 0 on 2026-10-31, and refund R03 is dated that day. All three candidates ran the helper and wrote `{"net_usd": 24317.47, "transactions": 16, "refunds": 5}`. Their diagnostics were identical: 3 duplicate rows dropped, 16 recognised transactions, 5 refunds applied. The prompt text and the script arrived together in every candidate, so no run separates them. The extra rules were never tested, because all three runs hit the same correct path. The base-versus-candidate contrast is one rollout each.
verdict: confounded

component: scripts/net_revenue.py
candidates: dom1 (also in agg1, byte-identical), inv1 (variant)
change: This is a new stdlib helper that dedupes by txn_id, parses comma amounts, applies the settled_on and refunded_on month rules with that day's rate, and writes the three-key JSON. The dom1/agg1 version reports orphan refunds and refunds on non-SETTLED transactions in its diagnostics. The inv1 version exits 1 on an unknown refund txn_id and on a missing or zero rate, and has fuller input validation.
observed: Both variants gave the same figures on this data, and the zero-rate INR day (2026-10-31) fell outside the target month in both. The decision notes mention the difference between abort and report, but no run exercised it. In agg1 the script ran only after three argparse failures, so it was not at fault. The script is the likeliest reason the three candidates produced a file and base1 did not, but base1 differs in the prompt as well.
verdict: confounded

component: systemprompt.md (generic line "never rerun an unchanged failing command, pass a value after every flag, e.g. --out output/answer.json")
candidates: agg1 (adopted); the closely related "Working rules" block in inv1
change: Added a sentence to the opening paragraph telling the agent to change something after a failure and to give a value to every flag. dom1 did not have this sentence.
observed: In the agg1 run, the agent still sent bare flags. `--tx --refunds --fx --status --out` failed with exit 2. It then supplied values one flag at a time and failed on `--status` and then `--out`, which is three failures before the fourth call succeeded. In inv1, which had the longer working-rules block and no explicit flag line, the agent ran a bare `--out` once (exit 2) and fixed it next call. In dom1, with neither line, the agent ran `--month 2026-09` once and finished cleanly. agg1 also did not start by listing the workspace, although the line says to. The line did not prevent the failure it was added for, and the run with it was the least efficient. This is single-rollout evidence, and the flag-error behaviour looks like sampling noise.
verdict: no observed effect

component: hooks.json and scripts/check_output.py (Stop hook that rejects a missing or malformed answer.json)
candidates: dom1, inv1, agg1 (identical in all three)
change: New Stop hook. It runs `check_output.py`, which exits 2 with a message if `output/answer.json` is missing, has the wrong types, or is not rounded to 2 decimals.
observed: All three candidates had written a valid file before stopping, so the hook never fired. Nothing shows whether it would have rescued a base1-style run that stopped on a plan.
verdict: no observed effect

component: plugin/README.md, scripts/README.md, skills/README.md, tool_descriptions/tool_guidance.md
candidates: agg1 (and the other candidates, unchanged or placeholder)
change: The README files are placeholder stubs, and `tool_guidance.md` is identical to the base.
observed: Nothing in any rollout references them.
verdict: no observed effect

## Transferable lesson
- **cue**: A task asks for a deterministic number or structured file computed from messy tabular exports (duplicate rows, formatted amounts, date-windowed joins, a bad-value trap on a boundary date), and the base harness gives only generic "do the work and write output/" text.
- **lesson**: Put the computation in the harness as an executable, stdlib-only helper under `scripts/`, with defaults for its input paths and a one-line invocation in `systemprompt.md`. Have it write the deliverable itself and print per-currency and per-count diagnostics. Do not rely on prose rules alone. Do not also expect an extra "never rerun a failing command / pass a value after every flag" sentence in `systemprompt.md` to prevent argument errors, because this record shows no effect from it. Keep the call short enough that the agent has no reason to invent flags, for example by stating the exact working command with no optional flags listed.
- **evidence**: Rows 1 and 2 (systemprompt.md pointer and scripts/net_revenue.py), both confounded because they were added together. base1 had no script and ended on a plan with no answer.json. dom1, inv1 and agg1 each ran the helper and wrote the same figures (24317.47 / 16 / 5). Row 3 shows the generic flag-value line did nothing: agg1 had it and failed three times on bare flags, while dom1, without it, ran cleanly.
- **confidence**: low-to-medium. The contrast is one base rollout against three candidates that all carried the same package, so the script and the prompt pointer cannot be separated. The base failure (stopping on a plan) may also be sampling variance. The rules for dedupe, boundary dates and zero rates were never put under test, since every candidate took the same correct path.

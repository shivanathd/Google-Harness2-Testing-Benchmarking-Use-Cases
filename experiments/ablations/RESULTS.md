# Harness² ablations on HPB-9: self-improvement, no-probe, library off

Date: 2026-10-19, runs 11:50–13:35 IST.
- harness2 core: unmodified (commit 1cfe254). Drivers: `hpb/ablate.py`. Tables: `hpb/ablations.py`.
- Design: PREREG.md Amendment 5, written before any ablation result.
- Leak guard in every arm, including the adk-guard reference: the study-2 guard. That is `validate_tree` with `bench.leaked` plus the workspace-fact filter, with the c8 `hooks.json` surface; `HPB_LEAKGUARD` is unset.
- Re-rolls: ADK base R=4 and in-task R=3; CC base R=4, in-task and transfer R=4, variants R=2.
- Cross-process caps: at most 4 concurrent `claude -p` and 8 ADK/Ollama rollouts.

## Arms

| arm | root | executor | improver | what changes | base / evidence |
|---|---|---|---|---|---|
| reference | `experiments/adk-guard` | ADK + qwen3:8b | Sonnet 5.5 | parallel k=1, library on (study 2) | — |
| no-probe | `adk-noprobe` | ADK + qwen3:8b | Sonnet 5.5 | INV/DOM proposals composed into agg1 with no probe rollouts; aggregate prompt says so | shared with adk-guard |
| library off | `adk-nolib` | ADK + qwen3:8b | Sonnet 5.5 | medium/hard only, each task alone with an empty library | shared with adk-guard |
| CC, Sonnet improver | `cc-sonnet` | CC + Haiku 5.5, **4-turn cap** | Sonnet 5.5 | turn cap gives headroom (base mean 0.58) | own base |
| CC, Haiku improver | `cc-haiku` | CC + Haiku 5.5, 4-turn cap | **Haiku 5.5** (improver = executor) | improver only | same 9 base1 rollouts and base rows as cc-sonnet |

**Turn cap.** I piloted caps 3, 4 and 5 (`cc-pilot-t*`, 2 rollouts per task, not reused); means were 0.37, 0.50 and 0.44. The cap was fixed at 4 before any treatment run. At the full 40 turns CC is at ceiling, and using only the hard tier gives no headroom either, since CC scores 1.0 there.

**ADK self-improvement was not run.** harness2's only non-Claude improver channel is OpenCode, which is not installed. A qwen3:8b improver through `adk_agent.py` would add about 27 long agentic sessions on the shared 8 Ollama slots. So the ADK gains in every arm come from a Sonnet 5.5 improver.

## Findings

1. **Most of the CC gain comes from the stronger improver.** At the 4-turn cap:
   - **Sonnet as improver:** +0.42 [+0.17, +0.69], 8 up / 0 down, n=9.
   - **Haiku as its own improver:** only 5/9 tasks were adopted. On the other four (ops-m, ops-h, swe-e, swe-h), its composed agg1 rollout delivered nothing.
     - Over the adopted tasks: +0.20 [−0.20, +0.55].
     - Counting each non-adopted final by re-rolling it (ITT): +0.17 [−0.08, +0.42], n=9.
   - **Haiku minus Sonnet:** −0.25 [−0.53, 0.00], 0 up / 3 down (ITT). The losses are all ops tasks: ops-e 1.00→0.25, ops-h 1.00→0.00, ops-m 1.00→0.50.
   - Haiku's improver sessions cost $0.74 against Sonnet's $4.84.
   - **Noise caveat:** both improvers kept the base harness on data-e and data-h. Those cells are fresh base re-rolls, so their +0.25 and +0.50 are rollout noise at the cap, and that noise is in Sonnet's +0.42.
   - This supports the distillation concern: CC + Haiku improves itself a little, but most of the in-task gain needs the stronger improver.
2. **Skipping the probe rollouts made no detectable difference on ADK.** The paper reports that adopting edits without probing them first hurts; this rig does not reproduce that.
   - No-probe vs base: +0.64 [+0.42, +0.85] (ITT, n=9), against +0.65 for probe.
   - No-probe minus probe: −0.004 [−0.11, +0.10], 1 up / 1 down.
   - The one check-level loss is data-h `net_usd` (1.00→0.00 in one of three rollouts).
   - No-probe skips 2 of every 4 rollouts and loses nothing measurable. Caveats:
     - At k=1 the composer reads one probe rollout per candidate. The probe is weak evidence by construction; the aggregate prompt itself calls it "weak evidence either way".
     - Without probes, swe-m adopted nothing (its agg1 delivered nothing), while adk-guard adopted a harness at +0.13. A no-probe pipeline therefore also loses the delivered-nothing signal before adoption.
3. **Turning the library off cost little on average; one data-h drop drives most of it.**
   - Library off vs base: +0.59 [+0.26, +0.90] (ITT, n=6), against +0.72 for library on.
   - Off minus on: −0.13 [−0.39, +0.01], 0 up / 2 down.
   - **data-h, 1.00→0.33, is a library effect:**
     - With the library, data-h's improver read the data-e and data-m entries, which ship a `scripts/net_revenue.py` solver. data-h adopted a rewritten solver and finishes in 2–3 tool calls.
     - Without it, the adopted harness only has an output checker. Two of three rollouts hit the 40-call limit.
   - swe-m: 0.13→0.00, ITT.
   - Everything else is unchanged. ops-m, ops-h, data-m and swe-h gain just as much with an empty library.
   - So most of the in-task gain is task-level recursion. Harnessing-level recursion (the library) adds a little within a domain, here mainly by passing a reusable solver script down the data domain.
   - This matches the near-zero easy→medium/hard transfer in studies 1 and 2: library entries help when the improver re-adapts them, not when they are reused frozen.

## Check-level flips (eval.py)
`eval.py report` and the tables below list, per task, the grader checks whose pass rate moved by at least 0.5 from reference to treatment.
- In every ADK arm, the gains are whole-answer flips: all checks of a task go 0→1 together, e.g. all 9 ops-h service metrics, or `net_usd`, `transactions` and `refunds` on data-m. The adopted harnesses make the agent deliver a correct answer file, rather than fix individual fields.
- The swe-h gains are per-test: 6–7 of 10 tests flip.
- Partial regressions:
  - swe-h `add_then_report`: library off vs on, 1.00→0.33.
  - CC Haiku ops tasks: every check falls together, because the answer file is missing.

## Caveats
- n is 9 tasks (6 for the library arm) with one Harness² run per arm. All of this is descriptive, as PREREG states.
- **Non-adopted tasks.** harness2's k=1 selection has no base fallback, so a final whose single rollout delivers nothing leaves the task with no adopted harness. The primary rows use adopted tasks only. The ITT rows also count those tasks, by re-rolling the non-adopted final (`eval.py --only itt`): adk-noprobe swe-m, adk-nolib swe-m, and cc-haiku ops-m, ops-h, swe-e, swe-h.
- **Restart incident.** At 12:15 all runs were restarted to enforce the 4-slot `claude -p` cap that the session that started this one asked for.
  - Two ADK agg1 rollouts killed mid-run (no-probe data-m, library-off swe-m) were scored as agent failures. The agent died without writing meta, and the adapter recorded a stderr warning as the error.
  - Both were deleted and re-run. The adapter now records a missing meta as infra (`no meta: ...`), so such rollouts are retried, never scored.
  - No-probe data-h composed after data-m's re-run, so its library matches the reference's.
- **Improver spend**, from the audit metadata, including retries and work lost at the restart:
  - adk-noprobe: $6.46, 50 sessions.
  - adk-nolib: $3.84, 30 sessions.
  - cc-sonnet: $4.84, 43 sessions.
  - cc-haiku: $0.74, 37 sessions.
  - adk-guard: $10.45, 80 sessions, including its aborted launch.
- **.git exposure, 12:28–13:20 IST.** `git init` at the repo root left `.git`, which holds the committed grader `hpb/bench.py`, readable inside the sandbox. It is now denied (efd91a1).
  - I scanned every rollout stream and improver session in all five roots (table below).
  - Agents ran only `git status` and `git log`; those printed our commit messages, never grader content.
  - No git show, cat-file, grep, archive or ls-* command ran, and no git command named hpb/. No cell is voided.
- **Second-layer audit** (`leakguard.py`, table below): 7 harnesses flagged across the four ablation roots, against 0 in adk-guard. None trips the pre-registered rule. By inspection:
  - **Instance values quoted as format examples:**
    - "2,845.66" as an example of a comma-separated amount (adk-nolib and cc-haiku data-m).
    - "(954.34)" as an example of an accounting negative (adk-noprobe data-e).
    - "0.074*1000" as an example of float rounding (adk-noprobe ops-h).
  - **Instance facts the workspace-fact filter misses (it does not match "in this workspace"):**
    - adk-nolib ops-h describes this workspace's offsets, latency-field switch time and gz file.
    - cc-sonnet ops-m describes its log-line quirks.
    - These are instance knowledge rather than answers, and they would inflate in-task scores relative to fresh seeds. ADK ops-h also reaches 1.00 in adk-guard and adk-noprobe, whose harnesses carry no such text. cc-sonnet ops-m has no such comparator.
  - **Verbatim:** cc-sonnet data-m copies the transactions CSV header as a column-list docstring.

<!-- tables -->
## Results table

| ablation | comparison | Δ partial | 95% CI | sign-flip p | up/down | tasks | leak-voided cells | strict Δ (clean tasks) |
|---|---|---|---|---|---|---|---|---|
| 1 self-improvement (CC) | Sonnet improver vs base | +0.423 | [+0.173, +0.694] | 0.008 | 8/0 | 9 | none | - |
| 1 self-improvement (CC) | Haiku improver vs base | +0.200 | [-0.200, +0.550] | 0.438 | 4/1 | 5 | none | - |
| 1 self-improvement (CC) | Haiku minus Sonnet improver | -0.150 | [-0.500, +0.000] | 1.000 | 0/1 | 5 | none | - |
| 1 self-improvement (CC) | Sonnet improver transfer vs base | +0.125 | [-0.083, +0.375] | 0.500 | 2/0 | 6 | none | - |
| 1 self-improvement (CC) | Haiku improver transfer vs base | +0.250 | [-0.125, +0.625] | 0.500 | 2/0 | 4 | none | - |
| 1 self-improvement (CC) | Haiku improver vs base, ITT | +0.173 | [-0.077, +0.417] | 0.172 | 6/1 | 9 | none | - |
| 1 self-improvement (CC) | Haiku minus Sonnet improver, ITT | -0.250 | [-0.528, +0.000] | 0.250 | 0/3 | 9 | none | - |
| 2 no-probe (ADK) | probe (parallel k=1) vs base | +0.647 | [+0.391, +0.878] | 0.008 | 8/0 | 9 | none | - |
| 2 no-probe (ADK) | no-probe vs base | +0.670 | [+0.427, +0.885] | 0.016 | 7/0 | 8 | none | - |
| 2 no-probe (ADK) | no-probe minus probe | -0.042 | [-0.125, +0.015] | 1.000 | 0/1 | 8 | none | - |
| 2 no-probe (ADK) | no-probe vs base, ITT | +0.643 | [+0.423, +0.848] | 0.008 | 8/0 | 9 | none | - |
| 2 no-probe (ADK) | no-probe minus probe, ITT | -0.004 | [-0.111, +0.097] | 1.000 | 1/1 | 9 | none | - |
| 3 library (ADK) | library on vs base | +0.721 | [+0.431, +0.958] | 0.031 | 6/0 | 6 | none | - |
| 3 library (ADK) | library off vs base | +0.705 | [+0.400, +0.967] | 0.062 | 5/0 | 5 | none | - |
| 3 library (ADK) | library off minus on | -0.133 | [-0.462, +0.024] | 1.000 | 0/1 | 5 | none | - |
| 3 library (ADK) | library off vs base, ITT | +0.587 | [+0.264, +0.900] | 0.062 | 5/0 | 6 | none | - |
| 3 library (ADK) | library off minus on, ITT | -0.133 | [-0.389, +0.012] | 0.500 | 0/2 | 6 | none | - |

Δ = mean over tasks of (treatment mean partial − reference mean partial); CI = hierarchical bootstrap (tasks, then rollouts; 10k draws); up/down = tasks with Δ > 0.001 / < −0.001. A cell is leak-voided when its harness contains the evaluated task's own literals (bench.leaked, the pre-registered rule); strict Δ drops those tasks.

## Check-level flips

A check flips fail→pass (pass→fail) when its pass rate over the rollouts rises (falls) by at least 0.5 from reference to treatment. Rates shown as reference->treatment.

| comparison | task | mean partial | fail→pass | pass→fail |
|---|---|---|---|---|
| Sonnet improver vs base | data-e | 0.75 -> 1.00 | - | - |
| Sonnet improver vs base | data-m | 0.75 -> 1.00 | - | - |
| Sonnet improver vs base | data-h | 0.50 -> 1.00 | chargebacks 0.50->1.00; net_usd 0.50->1.00; transactions 0.50->1.00 | - |
| Sonnet improver vs base | ops-e | 0.75 -> 1.00 | - | - |
| Sonnet improver vs base | ops-m | 0.00 -> 1.00 | failed 0.00->1.00; top_code 0.00->1.00; users 0.00->1.00 | - |
| Sonnet improver vs base | ops-h | 0.00 -> 1.00 | billing.error_rate 0.00->1.00; billing.p95_ms 0.00->1.00; billing.requests 0.00->1.00; gateway.error_rate 0.00->1.00; gateway.p95_ms 0.00->1.00; gateway.requests 0.00->1.00; search.error_rate 0.00->1.00; search.p95_ms 0.00->1.00; search.requests 0.00->1.00 | - |
| Sonnet improver vs base | swe-e | 1.00 -> 1.00 | - | - |
| Sonnet improver vs base | swe-m | 0.50 -> 1.00 | basic_us 0.50->1.00; empty 0.50->1.00; eu_discount 0.50->1.00; float_cents 0.50->1.00; half_up_line 0.50->1.00; lowercase_region 0.50->1.00; multi_line_in 0.50->1.00; strings 0.50->1.00; tax_after_discount 0.50->1.00; unknown_region 0.50->1.00 | - |
| Sonnet improver vs base | swe-h | 0.95 -> 1.00 | - | - |
| Haiku improver vs base | data-e | 0.75 -> 1.00 | - | - |
| Haiku improver vs base | data-m | 0.75 -> 1.00 | - | - |
| Haiku improver vs base | data-h | 0.50 -> 1.00 | chargebacks 0.50->1.00; net_usd 0.50->1.00; transactions 0.50->1.00 | - |
| Haiku improver vs base | ops-e | 0.75 -> 0.25 | - | errors 0.75->0.25; top_code 0.75->0.25; users 0.75->0.25 |
| Haiku improver vs base | swe-m | 0.50 -> 1.00 | basic_us 0.50->1.00; empty 0.50->1.00; eu_discount 0.50->1.00; float_cents 0.50->1.00; half_up_line 0.50->1.00; lowercase_region 0.50->1.00; multi_line_in 0.50->1.00; strings 0.50->1.00; tax_after_discount 0.50->1.00; unknown_region 0.50->1.00 | - |
| Haiku minus Sonnet improver | data-e | 1.00 -> 1.00 | - | - |
| Haiku minus Sonnet improver | data-m | 1.00 -> 1.00 | - | - |
| Haiku minus Sonnet improver | data-h | 1.00 -> 1.00 | - | - |
| Haiku minus Sonnet improver | ops-e | 1.00 -> 0.25 | - | errors 1.00->0.25; top_code 1.00->0.25; users 1.00->0.25 |
| Haiku minus Sonnet improver | swe-m | 1.00 -> 1.00 | - | - |
| Sonnet improver transfer vs base | data-m | 0.75 -> 1.00 | - | - |
| Sonnet improver transfer vs base | data-h | 0.50 -> 1.00 | chargebacks 0.50->1.00; net_usd 0.50->1.00; transactions 0.50->1.00 | - |
| Sonnet improver transfer vs base | ops-m | 0.00 -> 0.00 | - | - |
| Sonnet improver transfer vs base | ops-h | 0.00 -> 0.00 | - | - |
| Sonnet improver transfer vs base | swe-m | 0.50 -> 0.50 | - | - |
| Sonnet improver transfer vs base | swe-h | 0.95 -> 0.95 | - | - |
| Haiku improver transfer vs base | data-m | 0.75 -> 0.75 | - | - |
| Haiku improver transfer vs base | data-h | 0.50 -> 0.75 | - | - |
| Haiku improver transfer vs base | ops-m | 0.00 -> 0.75 | failed 0.00->0.75; top_code 0.00->0.75; users 0.00->0.75 | - |
| Haiku improver transfer vs base | ops-h | 0.00 -> 0.00 | - | - |
| Haiku improver vs base, ITT | data-e | 0.75 -> 1.00 | - | - |
| Haiku improver vs base, ITT | data-m | 0.75 -> 1.00 | - | - |
| Haiku improver vs base, ITT | data-h | 0.50 -> 1.00 | chargebacks 0.50->1.00; net_usd 0.50->1.00; transactions 0.50->1.00 | - |
| Haiku improver vs base, ITT | ops-e | 0.75 -> 0.25 | - | errors 0.75->0.25; top_code 0.75->0.25; users 0.75->0.25 |
| Haiku improver vs base, ITT | ops-m | 0.00 -> 0.50 | failed 0.00->0.50; top_code 0.00->0.50; users 0.00->0.50 | - |
| Haiku improver vs base, ITT | ops-h | 0.00 -> 0.00 | - | - |
| Haiku improver vs base, ITT | swe-e | 1.00 -> 1.00 | - | - |
| Haiku improver vs base, ITT | swe-m | 0.50 -> 1.00 | basic_us 0.50->1.00; empty 0.50->1.00; eu_discount 0.50->1.00; float_cents 0.50->1.00; half_up_line 0.50->1.00; lowercase_region 0.50->1.00; multi_line_in 0.50->1.00; strings 0.50->1.00; tax_after_discount 0.50->1.00; unknown_region 0.50->1.00 | - |
| Haiku improver vs base, ITT | swe-h | 0.95 -> 1.00 | - | - |
| Haiku minus Sonnet improver, ITT | data-e | 1.00 -> 1.00 | - | - |
| Haiku minus Sonnet improver, ITT | data-m | 1.00 -> 1.00 | - | - |
| Haiku minus Sonnet improver, ITT | data-h | 1.00 -> 1.00 | - | - |
| Haiku minus Sonnet improver, ITT | ops-e | 1.00 -> 0.25 | - | errors 1.00->0.25; top_code 1.00->0.25; users 1.00->0.25 |
| Haiku minus Sonnet improver, ITT | ops-m | 1.00 -> 0.50 | - | failed 1.00->0.50; top_code 1.00->0.50; users 1.00->0.50 |
| Haiku minus Sonnet improver, ITT | ops-h | 1.00 -> 0.00 | - | billing.error_rate 1.00->0.00; billing.p95_ms 1.00->0.00; billing.requests 1.00->0.00; gateway.error_rate 1.00->0.00; gateway.p95_ms 1.00->0.00; gateway.requests 1.00->0.00; search.error_rate 1.00->0.00; search.p95_ms 1.00->0.00; search.requests 1.00->0.00 |
| Haiku minus Sonnet improver, ITT | swe-e | 1.00 -> 1.00 | - | - |
| Haiku minus Sonnet improver, ITT | swe-m | 1.00 -> 1.00 | - | - |
| Haiku minus Sonnet improver, ITT | swe-h | 1.00 -> 1.00 | - | - |
| probe (parallel k=1) vs base | data-e | 0.00 -> 1.00 | net_usd 0.00->1.00; transactions 0.00->1.00 | - |
| probe (parallel k=1) vs base | data-m | 0.00 -> 1.00 | net_usd 0.00->1.00; refunds 0.00->1.00; transactions 0.00->1.00 | - |
| probe (parallel k=1) vs base | data-h | 0.08 -> 1.00 | chargebacks 0.25->1.00; net_usd 0.00->1.00; transactions 0.00->1.00 | - |
| probe (parallel k=1) vs base | ops-e | 0.50 -> 1.00 | errors 0.00->1.00; users 0.50->1.00 | - |
| probe (parallel k=1) vs base | ops-m | 0.17 -> 1.00 | failed 0.00->1.00; top_code 0.50->1.00; users 0.00->1.00 | - |
| probe (parallel k=1) vs base | ops-h | 0.00 -> 1.00 | billing.error_rate 0.00->1.00; billing.p95_ms 0.00->1.00; billing.requests 0.00->1.00; gateway.error_rate 0.00->1.00; gateway.p95_ms 0.00->1.00; gateway.requests 0.00->1.00; search.error_rate 0.00->1.00; search.p95_ms 0.00->1.00; search.requests 0.00->1.00 | - |
| probe (parallel k=1) vs base | swe-e | 0.20 -> 0.20 | - | - |
| probe (parallel k=1) vs base | swe-m | 0.00 -> 0.13 | - | - |
| probe (parallel k=1) vs base | swe-h | 0.18 -> 0.62 | add_accumulates 0.50->1.00; add_nonpositive 0.00->1.00; add_then_report 0.00->1.00; load_empty 0.00->1.00; load_missing 0.00->1.00; report_format 0.50->1.00; report_missing_file 0.00->1.00 | - |
| no-probe vs base | data-e | 0.00 -> 1.00 | net_usd 0.00->1.00; transactions 0.00->1.00 | - |
| no-probe vs base | data-m | 0.00 -> 1.00 | net_usd 0.00->1.00; refunds 0.00->1.00; transactions 0.00->1.00 | - |
| no-probe vs base | data-h | 0.08 -> 0.67 | chargebacks 0.25->1.00; transactions 0.00->1.00 | - |
| no-probe vs base | ops-e | 0.50 -> 1.00 | errors 0.00->1.00; users 0.50->1.00 | - |
| no-probe vs base | ops-m | 0.17 -> 1.00 | failed 0.00->1.00; top_code 0.50->1.00; users 0.00->1.00 | - |
| no-probe vs base | ops-h | 0.00 -> 1.00 | billing.error_rate 0.00->1.00; billing.p95_ms 0.00->1.00; billing.requests 0.00->1.00; gateway.error_rate 0.00->1.00; gateway.p95_ms 0.00->1.00; gateway.requests 0.00->1.00; search.error_rate 0.00->1.00; search.p95_ms 0.00->1.00; search.requests 0.00->1.00 | - |
| no-probe vs base | swe-e | 0.20 -> 0.20 | - | - |
| no-probe vs base | swe-h | 0.18 -> 0.62 | add_accumulates 0.50->1.00; add_nonpositive 0.00->1.00; add_then_report 0.00->1.00; load_empty 0.00->1.00; load_missing 0.00->1.00; report_format 0.50->1.00; report_missing_file 0.00->1.00 | - |
| no-probe minus probe | data-e | 1.00 -> 1.00 | - | - |
| no-probe minus probe | data-m | 1.00 -> 1.00 | - | - |
| no-probe minus probe | data-h | 1.00 -> 0.67 | - | net_usd 1.00->0.00 |
| no-probe minus probe | ops-e | 1.00 -> 1.00 | - | - |
| no-probe minus probe | ops-m | 1.00 -> 1.00 | - | - |
| no-probe minus probe | ops-h | 1.00 -> 1.00 | - | - |
| no-probe minus probe | swe-e | 0.20 -> 0.20 | - | - |
| no-probe minus probe | swe-h | 0.62 -> 0.62 | - | - |
| no-probe vs base, ITT | data-e | 0.00 -> 1.00 | net_usd 0.00->1.00; transactions 0.00->1.00 | - |
| no-probe vs base, ITT | data-m | 0.00 -> 1.00 | net_usd 0.00->1.00; refunds 0.00->1.00; transactions 0.00->1.00 | - |
| no-probe vs base, ITT | data-h | 0.08 -> 0.67 | chargebacks 0.25->1.00; transactions 0.00->1.00 | - |
| no-probe vs base, ITT | ops-e | 0.50 -> 1.00 | errors 0.00->1.00; users 0.50->1.00 | - |
| no-probe vs base, ITT | ops-m | 0.17 -> 1.00 | failed 0.00->1.00; top_code 0.50->1.00; users 0.00->1.00 | - |
| no-probe vs base, ITT | ops-h | 0.00 -> 1.00 | billing.error_rate 0.00->1.00; billing.p95_ms 0.00->1.00; billing.requests 0.00->1.00; gateway.error_rate 0.00->1.00; gateway.p95_ms 0.00->1.00; gateway.requests 0.00->1.00; search.error_rate 0.00->1.00; search.p95_ms 0.00->1.00; search.requests 0.00->1.00 | - |
| no-probe vs base, ITT | swe-e | 0.20 -> 0.20 | - | - |
| no-probe vs base, ITT | swe-m | 0.00 -> 0.43 | basic_us 0.00->1.00; float_cents 0.00->1.00; half_up_line 0.00->1.00; strings 0.00->1.00 | - |
| no-probe vs base, ITT | swe-h | 0.18 -> 0.62 | add_accumulates 0.50->1.00; add_nonpositive 0.00->1.00; add_then_report 0.00->1.00; load_empty 0.00->1.00; load_missing 0.00->1.00; report_format 0.50->1.00; report_missing_file 0.00->1.00 | - |
| no-probe minus probe, ITT | data-e | 1.00 -> 1.00 | - | - |
| no-probe minus probe, ITT | data-m | 1.00 -> 1.00 | - | - |
| no-probe minus probe, ITT | data-h | 1.00 -> 0.67 | - | net_usd 1.00->0.00 |
| no-probe minus probe, ITT | ops-e | 1.00 -> 1.00 | - | - |
| no-probe minus probe, ITT | ops-m | 1.00 -> 1.00 | - | - |
| no-probe minus probe, ITT | ops-h | 1.00 -> 1.00 | - | - |
| no-probe minus probe, ITT | swe-e | 0.20 -> 0.20 | - | - |
| no-probe minus probe, ITT | swe-m | 0.13 -> 0.43 | basic_us 0.33->1.00; float_cents 0.33->1.00; half_up_line 0.00->1.00; strings 0.33->1.00 | - |
| no-probe minus probe, ITT | swe-h | 0.62 -> 0.62 | - | - |
| library on vs base | data-m | 0.00 -> 1.00 | net_usd 0.00->1.00; refunds 0.00->1.00; transactions 0.00->1.00 | - |
| library on vs base | data-h | 0.08 -> 1.00 | chargebacks 0.25->1.00; net_usd 0.00->1.00; transactions 0.00->1.00 | - |
| library on vs base | ops-m | 0.17 -> 1.00 | failed 0.00->1.00; top_code 0.50->1.00; users 0.00->1.00 | - |
| library on vs base | ops-h | 0.00 -> 1.00 | billing.error_rate 0.00->1.00; billing.p95_ms 0.00->1.00; billing.requests 0.00->1.00; gateway.error_rate 0.00->1.00; gateway.p95_ms 0.00->1.00; gateway.requests 0.00->1.00; search.error_rate 0.00->1.00; search.p95_ms 0.00->1.00; search.requests 0.00->1.00 | - |
| library on vs base | swe-m | 0.00 -> 0.13 | - | - |
| library on vs base | swe-h | 0.18 -> 0.62 | add_accumulates 0.50->1.00; add_nonpositive 0.00->1.00; add_then_report 0.00->1.00; load_empty 0.00->1.00; load_missing 0.00->1.00; report_format 0.50->1.00; report_missing_file 0.00->1.00 | - |
| library off vs base | data-m | 0.00 -> 1.00 | net_usd 0.00->1.00; refunds 0.00->1.00; transactions 0.00->1.00 | - |
| library off vs base | data-h | 0.08 -> 0.33 | - | - |
| library off vs base | ops-m | 0.17 -> 1.00 | failed 0.00->1.00; top_code 0.50->1.00; users 0.00->1.00 | - |
| library off vs base | ops-h | 0.00 -> 1.00 | billing.error_rate 0.00->1.00; billing.p95_ms 0.00->1.00; billing.requests 0.00->1.00; gateway.error_rate 0.00->1.00; gateway.p95_ms 0.00->1.00; gateway.requests 0.00->1.00; search.error_rate 0.00->1.00; search.p95_ms 0.00->1.00; search.requests 0.00->1.00 | - |
| library off vs base | swe-h | 0.18 -> 0.62 | add_accumulates 0.50->1.00; add_nonpositive 0.00->1.00; load_empty 0.00->1.00; load_missing 0.00->1.00; remove_unknown 0.25->1.00; report_format 0.50->1.00; report_missing_file 0.00->1.00 | - |
| library off minus on | data-m | 1.00 -> 1.00 | - | - |
| library off minus on | data-h | 1.00 -> 0.33 | - | chargebacks 1.00->0.33; net_usd 1.00->0.33; transactions 1.00->0.33 |
| library off minus on | ops-m | 1.00 -> 1.00 | - | - |
| library off minus on | ops-h | 1.00 -> 1.00 | - | - |
| library off minus on | swe-h | 0.62 -> 0.62 | remove_unknown 0.33->1.00 | add_then_report 1.00->0.33 |
| library off vs base, ITT | data-m | 0.00 -> 1.00 | net_usd 0.00->1.00; refunds 0.00->1.00; transactions 0.00->1.00 | - |
| library off vs base, ITT | data-h | 0.08 -> 0.33 | - | - |
| library off vs base, ITT | ops-m | 0.17 -> 1.00 | failed 0.00->1.00; top_code 0.50->1.00; users 0.00->1.00 | - |
| library off vs base, ITT | ops-h | 0.00 -> 1.00 | billing.error_rate 0.00->1.00; billing.p95_ms 0.00->1.00; billing.requests 0.00->1.00; gateway.error_rate 0.00->1.00; gateway.p95_ms 0.00->1.00; gateway.requests 0.00->1.00; search.error_rate 0.00->1.00; search.p95_ms 0.00->1.00; search.requests 0.00->1.00 | - |
| library off vs base, ITT | swe-m | 0.00 -> 0.00 | - | - |
| library off vs base, ITT | swe-h | 0.18 -> 0.62 | add_accumulates 0.50->1.00; add_nonpositive 0.00->1.00; load_empty 0.00->1.00; load_missing 0.00->1.00; remove_unknown 0.25->1.00; report_format 0.50->1.00; report_missing_file 0.00->1.00 | - |
| library off minus on, ITT | data-m | 1.00 -> 1.00 | - | - |
| library off minus on, ITT | data-h | 1.00 -> 0.33 | - | chargebacks 1.00->0.33; net_usd 1.00->0.33; transactions 1.00->0.33 |
| library off minus on, ITT | ops-m | 1.00 -> 1.00 | - | - |
| library off minus on, ITT | ops-h | 1.00 -> 1.00 | - | - |
| library off minus on, ITT | swe-m | 0.13 -> 0.00 | - | - |
| library off minus on, ITT | swe-h | 0.62 -> 0.62 | remove_unknown 0.33->1.00 | add_then_report 1.00->0.33 |

## Second-layer leak audit (hpb/leakguard.py, read-only)

Every arm ran with the study-2 guard only: validate_tree with bench.leaked and the workspace-fact filter, with HPB_LEAKGUARD unset. The audit is run afterwards.

| root | adopted harnesses | flagged | flags |
|---|---|---|---|
| adk-guard | 9 | 0 | - |
| adk-noprobe | 8 | 2 | ops-h: {"skills/service-traffic-stats/SKILL.md": {"datum": ["0.074"]}}; data-e: {"scripts/net_revenue.py": {"datum": ["954.34"]}} |
| adk-nolib | 5 | 2 | data-m: {"systemprompt.md": {"datum": ["2845.66"]}}; ops-h: {"skills/log-traffic-report/SKILL.md": {"fact": ["in this workspace"]}} |
| cc-sonnet | 7 | 2 | ops-m: {"systemprompt.md": {"fact": ["In this workspace"]}}; data-m: {"scripts/reconcile_revenue.py": {"verbatim": ["txn id created on settled on amount currency", "id created on settled on amount currency status"]}} |
| cc-haiku | 3 | 1 | data-m: {"skills/revenue-reconciliation/SKILL.md": {"datum": ["2845.66"]}} |

## Exposure check: .git readable 12:28-13:20 IST

| root | rollouts + improver sessions scanned | ran any git command | read repo content via git | voided |
|---|---|---|---|---|
| adk-guard | 221 | 0 | 0 | none |
| adk-noprobe | 98 | 1 | 0 | none |
| adk-nolib | 75 | 0 | 0 | none |
| cc-sonnet | 199 | 4 | 0 | none |
| cc-haiku | 133 | 10 | 0 | none |
<!-- /tables -->

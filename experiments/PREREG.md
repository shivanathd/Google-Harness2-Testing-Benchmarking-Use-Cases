# HPB × Harness² — pre-registration (written 2026-10-19 01:20 IST, before any treatment run)

Task data hash: 8aec868f593e. Base-harness pilots were run only for calibration, on an earlier task version.

## Arms
- **Executors**
  - ADK + qwen3:8b (local; primary arm, chosen because it has headroom).
  - Claude Code + Haiku 5.5 (negative control: at ceiling in the pilot).
- **Improver** (all methods): Claude Sonnet 5.5, effort high, through the harness2 `claude_cli` channel, sandboxed.
- **Conditions**
  - `base`: one-sentence system prompt.
  - `h2`: Harness² parallel k=1, unmodified core, domains in order easy→medium→hard, library on.
  - `h2seq`: Harness² sequential k=2, `data` domain only.
  - `ar`: Karpathy-style autoresearch, 4 iterations on the domain's easy task with the real grader. An edit is kept only if its single rollout strictly beats the incumbent. The final harness is frozen.

## Measurements (fresh rollouts, unique run ids; nothing reused from the improvement runs)
- `base`: R=4 per task (ADK); R=3 (CC).
- `h2` in-task: the harness adopted for task t, re-rolled R times on t.
- `h2` variant: the same harness on t's fresh-seed variant (data/ops only), R=2. This is the memorisation check.
- `h2` transfer: the harness adopted on the domain's easy task, re-rolled on that domain's medium and hard tasks, R times.
- `ar`: the frozen harness re-rolled on easy (in-sample), medium and hard (transfer), and on variants.

## Endpoints
- **Primary (per executor):** the paired change in mean partial score, `h2` in-task minus `base`, averaged over the 9 tasks.
- **Secondary:**
  - Transfer change versus `base` on medium and hard tasks (h2-transfer, ar-transfer).
  - all-pass@R and pass^k.
  - Variant change (memorisation).
  - Cost per point gained.
- **Statistics**
  - Hierarchical bootstrap: resample tasks, then rollouts; 10k draws; 95% CI.
  - Exact sign-flip permutation test over the per-task deltas.
  - Results are descriptive at n=9. No per-domain or per-tier inference.

## Failure handling
- Timeouts and step-limit exhaustion are agent failures and score 0.
- Plumbing failures (CLI or model-server errors) are retried up to 3 times. They are reported, never scored.

## Leak audit
- Grep adopted harnesses for instance literals (expected numbers, ids).
- Grep executor trajectories and improver tool streams for grader paths and for "Operation not permitted" (blocked escape attempts).
- Any hit voids the affected cell.

## Amendment 1 (01:27 IST, before any treatment result)
At launch, ADK aborted whole runs when a tool raised. "No such directory" was now an error,
and it killed the run instead of reaching the model. Every ADK tool now returns
`ERROR: ...` text as its observation, as standard agent frameworks do. All ADK results were
discarded and the ADK arm relaunched. The CC arm was unaffected.

## Amendment 2 (01:33 IST, before any treatment result)
The host is CPU-saturated (load avg about 200 from EDR, syspolicyd and Spotlight). ADK rollouts
that use all 40 steps take 5-15 min. ADK re-roll counts after the Harness2 and autoresearch
runs drop to R=3 (in-task, transfer, autoresearch) and R=2 (variants). Base stays at R=4.
The CC arm keeps R=3 throughout.

## Amendment 3 (02:00 IST, before any ADK treatment result)
The ADK sequential k=2 arm is dropped to free local-GPU capacity for the primary ADK
comparison. Sequential k=2 is reported for the CC arm only.

## Amendment 4 (02:25 IST)
Found: under concurrent startup, the Claude CLI sometimes returned "Not logged in · Please run
/login" with subtype=success. It hit 11/237 CC executor rollouts (including the first base
rollout of every CC Harness² domain) and 4 improver sessions. The infra classifier missed it.
Fix: auth failures are now infra (executor rollouts are re-run, never scored) and improver
sessions retry with backoff. All CC-arm derived results were discarded and the CC arm was re-run.
Cached CC rollouts are reused only when their harness fingerprint matches and they are not
auth failures. ADK: the improver never hit this (0/14 sessions). The ADK Harness2 and
autoresearch processes were restarted on the fixed code and resume from cache.

## Amendment 5 (2026-10-19 12:05 IST): ablations, written before any ablation result
Root: `experiments/ablations/`. Driver: `hpb/ablate.py`, which imports harness2 core and does not modify it. Tables: `hpb/ablations.py` writes them to `experiments/ablations/RESULTS.md`. Every ablation uses Harness² parallel k=1 with the leak guard and c8 hook from study 2 (`experiments/leak-guard-results.md`).

**1. Self-improvement (CC arm).** Study 1 used Sonnet 5.5 as the improver for Haiku 5.5, so its gains may be distillation. CC is at ceiling with 40 turns.
- **Turn cap.** In a pilot (2 base rollouts per task at caps 3/4/5, roots `cc-pilot-t*`, not reused), the mean was 0.37/0.50/0.44, so `HPB_CC_MAX_TURNS=4` was fixed.
- **Runs at the cap.** Base R=4 (variants R=2) in `cc-sonnet`. Two Harness² runs: `cc-sonnet` (Sonnet improver) and `cc-haiku` (`HPB_IMPROVER=claude-haiku-5-5`). Both share the same 9 `base1` evidence rollouts and the same base eval rows.
- **Eval.** In-task, variant and transfer, R=4 (variants R=2).
- **Endpoints.** Each improver's in-task Δ vs base, and Haiku minus Sonnet (in-task).
- **ADK.** No ADK self-improvement arm. harness2's only non-Claude channel is OpenCode, which is not installed. A qwen3:8b improver would also add about 27 multi-step sessions on the shared 8 Ollama slots.

**2. No-probe (ADK).** `ablate.py --no-probe` runs the same INV and DOM stages, `recursion._run_stage`, with the library on. It then composes `agg1` from the two proposals with no probe rollouts.
- The aggregate prompt's sentence "Each candidate was rolled out ONCE and you have that rollout." is replaced by a statement that no candidate was rolled out.
- `agg1` is rolled and adopted as usual. Budget: R=2, P=3 per task.
- Base rollouts and base eval rows are shared with `experiments/adk-guard`.
- **Comparison.** In-task R=3 vs base, and vs adk-guard parallel k=1 in-task (no-probe minus probe), over all 9 tasks.

**3. Library off (ADK).** `ablate.py --no-library --tiers medium hard`: each medium and hard task runs as a one-task stream with a fresh, empty library. Easy tasks already see an empty library in the library-on run.
- Base is shared with adk-guard.
- **Comparison.** In-task R=3 vs base, and vs adk-guard in-task (library off minus on), over the 6 medium and hard tasks.

**Statistics and leak rule.** Unchanged (eval.py, now via `hpb/stats.py`).

**Added: check-level flips.** For each task, a grader check counts as fail→pass (or pass→fail) when its pass rate over the rollouts rises (or falls) by ≥0.5 between reference and treatment. It is reported in `eval.py report` and in RESULTS.md.

**Re-rolls.** ADK ablation eval rolls in-task only (`eval.py --only intask`) to fit the shared GPU.

## Amendment 6 (12:20 IST, before any ablation or LAB treatment result is read)
Leak prevention, defence in depth:
1. Guard v1 (leak-guard session): reject the task's own answers or ids and "workspace fact" blocks at adoption.
2. Guard v2 (hpb/leakguard.py, HPB_LEAKGUARD=2): also rejects distinctive numbers or rare ids from the instance data, verbatim 8-word passages, and 3+ case-specific names. Restated instructions are allowed. On by default for new arms; in-flight arms keep v1 for consistency.
3. Post-hoc audit of every adopted harness with v2 in every arm (flags study 1 at 7/8, study 2 at 0/9).
4. Headline metric: fresh-seed or held-out-task performance, which is leak-free by construction. The in-task number is reported as test-time adaptation.

## Amendment 7 (2026-10-19 13:40 IST): post-hoc additions to the ablations, made after results were seen
- **ITT rows.** Some arms adopted nothing on some tasks, because harness2's k=1 selection has no base fallback when the final delivers nothing. For those tasks, `eval.py --only itt` re-rolls the non-adopted final, and RESULTS.md reports these ITT rows next to the adopted-only primary rows. They were added after the non-adoptions were seen.
- **Exposure check.** From 12:28 to 13:20 IST `.git` was readable inside the sandbox; it is now denied in `adapters.sandboxed`. A cell would be voided if its rollout read repo content through git. The scan found none.
- **Missing meta.** A rollout whose agent died without writing meta is now infra, not an agent failure.

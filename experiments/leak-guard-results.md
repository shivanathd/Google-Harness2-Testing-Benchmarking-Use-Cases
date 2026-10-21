# Harness² on HPB-9, ADK arm: leak guard + c8 Stop hook (study 2) vs study 1

Date: 2026-10-19, run 10:39–11:43 IST.
- Executor: Google ADK + qwen3:8b (Ollama, same server settings as study 1).
- Improver: Claude Sonnet 5.5, sandboxed `claude` CLI.
- Method: Harness² parallel k=1. harness2 core is unmodified (commit 1cfe254).
- Root: `experiments/adk-guard`. Study 1's root `experiments/adk` was not touched.
- Report: `experiments/adk-guard/eval/report.json`. Study 1's report: `experiments/adk/eval/report.json`.

## What changed in the rig
1. **Answer-leak guard.** `HPBAdapter.validate_tree` (`hpb/adapters.py`) rejects a proposed tree that has any of:
   - the current task's own expected values or instance ids. This is the PREREG leak rule; it now lives in `bench.leaked`, eval.py imports it, and it reproduces study 1's 11 voided cells exactly.
   - a "workspace fact(s)" style block.
   - an OpenCode `plugin/*.ts`, which neither executor runs.

   The task reaches `validate_tree` through a thread-local, set in `task_prompt`; harness2's `context.build` calls that in the proposing thread just before validation. The rejection text goes back to the improver, harness2 retries once, then falls back.
2. **c8 component: `hooks.json`.** It uses the Claude Code hooks format, with the Stop event only.
   - harness2 core only accepts plugins as `plugin/<name>.ts`, so a Python `plugin/<name>.py` could not go on the surface without changing core.
   - ADK (`hpb/adk_agent.py`): when the model finishes, the hook commands run in the workspace. Exit 2 re-prompts the model with the command's stderr, at most 3 times, inside the same 40-call budget.
   - Claude Code: the file is copied to `work/.claude/settings.json`.
3. **Sandbox fix found on the way.** `sandboxed()` blocked `stat` on the workspace's ancestor directories, so Claude Code refused to load `.claude/settings.json` ("path could not be vetted"). Hooks could never have fired. It now allows `file-read-metadata` on the ancestors only; listing them is still denied.
   - Study 1 is unaffected: its CC rollouts did load CLAUDE.md and `.claude/skills`, which I checked in the init events and Skill tool calls.

Self-checks, both passing:
- `cd hpb && ../repo/.venv/bin/python adapters.py` (guard).
- `cd hpb && ../adk-venv/bin/python adk_agent.py --selfcheck` (Stop hook).

Live smoke tests:
- CC with Haiku 5.5: the hook blocked the first finish, and the agent then wrote the file.
- ADK with qwen3:8b: one block, then the agent wrote the file.

Reused from study 1:
- the base harness (fingerprint `7f0c60f515956056`, identical);
- the 48 base eval rows;
- the 9 Harness² `base1` rollouts, which are the improver's evidence.

All treatment rollouts and all improver sessions are new.

## Results (Δ mean partial score vs base; hierarchical bootstrap 95% CI; exact sign-flip p)

| Endpoint | Study 1 (no guard) | Study 2 (guard + c8) |
|---|---|---|
| In-task | +0.74 [+0.53, +0.93], n=8, 8 up / 0 down, p=0.008 | +0.65 [+0.39, +0.88], n=9, 8 up / 0 down, p=0.008 |
| In-task, strict (voided cells dropped) | +0.33 [+0.20, +0.54], n=2, p=0.50 | +0.65 [+0.39, +0.88], n=9, p=0.008 |
| **In-task voided cells** | **6/8** | **0/9** |
| Variant (fresh seed) | +0.81 [+0.47, +1.00], n=6, 5 up / 0 down, p=0.062 | +0.97 [+0.89, +1.00], n=6, 6 up / 0 down, p=0.031 |
| Variant, strict | +0.50 [+0.00, +1.00], n=2, p=1.00 | +0.97 [+0.87, +1.00], n=5, p=0.062 |
| **Variant voided cells** | **4/6** | **1/6** |
| Transfer (easy harness → medium/hard) | +0.01 [−0.07, +0.11], n=6, 1 up / 2 down | −0.03 [−0.11, +0.04], n=6, 1 up / 2 down |
| Transfer, strict | +0.03 [−0.05, +0.14], n=5 | −0.03 [−0.11, +0.04], n=6 |
| **Transfer voided cells** | **1/6** | **0/6** |
| Total voided cells | 11/20 | 1/21 |
| Improver spend (H² run) | $3.93, 27 calls | $5.74, 50 calls, plus about $4.70 on an aborted launch (see caveats) |

Per task, in-task:
- data and ops are identical across the two studies: all six go to 1.00, all-pass 3/3.
- swe: swe-e +0.20 → +0.00; swe-h +0.46 → +0.44; swe-m, missing from study 1 because its Harness² task failed, is +0.13.

So the drop from +0.74 to +0.65 comes entirely from the swe domain plus swe-m now being counted. It is not a data/ops loss.

## What the guard and hook did
- **Guard firings.** It rejected 10 proposals in the completed run (5 for answer literals, 8 for workspace-fact blocks; some had both) and 13 in the aborted launch, whose easy-task proposals were reused from cache.
  - Every retry passed. There were 0 fallbacks in the completed run.
  - All 9 adopted harnesses are non-base (`agg1`). Study 1's adopted harnesses had computed answers in skills; these carry the method in scripts instead.
- **The 1 remaining voided cell** is data-h-v. The match is "15", which comes from a `--fee` default of `15.00` in the data-h harness. That is a policy constant that happens to equal the variant's expected count of 15, not a leak.
  - The guard only checks the current task's literals, and the pre-registered token rule flags any matching int ≥ 10.
- **c8 adoption.** The improver added `hooks.json` to 6/9 adopted harnesses (all data and swe); the ops harnesses use skill-bundled scripts instead.
  - Of 36 eval rollouts with a hook, the hook fired in 6, with 10 blocks in total: swe-e in-task 3/3, data-m transfer 2, swe-h transfer 1.
  - None of those rollouts gained from it. swe-e stayed at 0.20, and data-m transfer stayed at 0.
- **data-e-v, the motivating cell, went from 0.00 to 1.00, but not because of the hook.** The hook never fired there. The adopted script writes `output/answer.json` itself (`--out`), so the agent no longer has to copy a printed answer into a file.
- **Transfer is still absent.** The easy harnesses' scripts are task-shaped, as in study 1.

## Caveats
- **One run per study, n=9 tasks.** Treat the comparison as descriptive. Study 2 also changed two things at once: the guard and c8.
- **Aborted launch.** The first launch passed a relative `--root`, and the sandbox cannot resolve relative paths, so every treatment rollout failed with "Operation not permitted". Those exec dirs were deleted and the run relaunched; `run.py` and `eval.py` now resolve `--root`.
  - Cached improver replies from that launch were reused where their evidence was unchanged: the easy tasks' dom/inv stages.
  - Log: `experiments/logs/adk-guard-h2-par.relpath-bug.log`.
- **Global leak audit.** It flags one literal: "234", inside the format example `'(1,234.50)'` in data-e's script. It matches ops-h-v's expected value. Not instance data; it does not void a cell under the per-cell rule.
- **Mean eval wall time.** In-task 177 s (study 1: 153 s). Transfer 527 s (study 1: 284 s).
  - Transfer rollouts that hit the 40-call limit: 10/18 (study 1: 3/18).
  - Stop-hook blocks in transfer rollouts: 7.
  - The host was also more loaded during the eval (load average about 100 by the end).

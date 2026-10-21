# Harness² on LAB (harvey-labs) legal tasks, run on our sandboxed Claude Code rig

**Status: FINAL (2026-10-19 20:51 IST).** All planned cells ran:
- base, R=3;
- Harness² in-task for both improver arms, R=3;
- the full held-out matrix, 4 harnesses × 3 unseen tasks, R=3.

No Vertex, Gemini or gcloud project was used.

## 1. Setup (fixed at 11:10 IST, before any treatment run)
- **Data.** `harveyai/harvey-labs` at the harness2 pin `b58a28a`, fetched as `harness2-setup lab` does: a git checkout plus the judge patch.
- **Practice area.** `arbitration-international-dispute-resolution`. Four docx/eml tasks, run in sorted order (harness2's reference stream order):

  | task | type | checks |
  |---|---|---|
  | draft-markup-of-arbitration-agreement | redline + memo | 59 |
  | draft-markup-of-procedural-order (the public-demo task) | redline + cover letter | 55 |
  | draft-markup-of-proposed-interim-order | redline | 37 |
  | identify-arbitration-agreement-issues | issues memo | 40 |

- **Executor.** `claude -p` with Haiku 5.5, max 40 turns, in the `hpb/adapters.py` sandbox.
  - Base harness: harness2's LAB base body (`CODEX_BASE_BODY`).
  - Assignment message: the LAB runner's `build_prompt`.
  - Data room: `documents/`, plus `scripts/read_doc.py` (pandoc).
- **Improver.** harness2 core, unmodified, via the sandboxed `claude_cli` channel. Parallel k=1, library on.
  - Arm A: Haiku 5.5, the same model as the executor (self-improvement).
  - Arm B: Sonnet 5.5 (stronger improver).
- **Judge.** Sonnet 5.5 via sandboxed, tool-less `claude -p`. It mirrors LAB's `evaluation/scoring.py`:
  - the `rubric_criterion.txt` prompt;
  - one call per criterion, seeing only that criterion's deliverables;
  - pandoc `--track-changes=accept`;
  - judge failure scores None, never 0.
- **Score.** The fraction of criteria passed (LAB partial score), in %. A check flip is a criterion whose pass rate over R crosses 0.5 versus base.
- **Two metrics.**
  - **In-task:** the adopted harness re-rolled on its own matter. This is the paper's protocol, and it is test-time adaptation, because the improver read that data room.
  - **Held-out:** each adopted Arm B harness re-rolled on the 3 tasks its improver never saw.
- **Code.** `hpb/lab.py`, a `LabAdapter` subclass of `HPBAdapter` (`adapters.py` is not edited). Phases: `selfcheck`, `base`, `h2`, `adopted`, `transfer`, `audit`, `report`.

**Leak-guard version per arm**

| arm, cells | guard |
|---|---|
| Arm B, all tasks; Arm A, tasks 1–2 | layer 1 only: harness2 LAB invariants, c8 rule, workspace-fact regex |
| Arm A, tasks 3–4 (resumed after the auth outage) | layer 2 on |

- Layer 2 is `hpb/leakguard.py` plus `lab.LabInstance`. It flags:
  - instance numbers and ids;
  - 3+ case-specific proper nouns;
  - 8-word verbatim passages;
  - fact phrasing.
- LAB tuning (`LEAKGUARD_VERSION`):
  - an entity must contain a non-dictionary word;
  - years are ignored;
  - a datum hit needs two or more distinct values.
- Every adopted harness from both arms was also audited post-hoc with layer 2.

## 2. Rubric isolation (verified)
- **Single reader.** Criteria are read in one function (`lab.criteria()`), called only by the judge.
- **What the executor and improver see.** `task.json` with criteria removed, and `task.json` is a leak glob kept out of the context tree.
- **Sandbox.** Every executor, improver and judge sandbox denies reads of the whole harvey-labs checkout. The self-check proves a sandboxed `cat task.json` fails, while the staged documents stay readable.
- **Audit.** `lab.py audit` searched all improver streams, context trees, harnesses, library entries and executor streams of both arms (2,781 files) for:
  - verbatim 60-character criterion slices that are not also in the data room;
  - `match_criteria`;
  - the LAB task path.
- **Result: 0 rubric leaks.** There was one hit, reviewed:
  - Location: an Arm A interim-order executor stream (`agg1`).
  - Match: its own drafted sentence, "...including confidential commercial relationships with unrelated third parties", which matches 60 characters of criterion C-007.
  - Why it is not a leak: the phrase is in no harness or library file and in no other run, and that executor was under the LAB-checkout deny. It is ordinary legal phrasing of the point C-007 tests.
- **`.git` exposure window (12:28–13:20).** A grep of all executor and improver streams for `git show`, `cat-file`, `git log` and `.git/` found only `find . -not -path '*/.git/*'`, which excludes `.git`. No process read `.git`.

## 3. In-task results (test-time adaptation), partial score %, R=3
| task | checks | base | Arm B: Sonnet improver | Δ | gained / lost | Arm A: Haiku self-improver | Δ | gained / lost |
|---|---|---|---|---|---|---|---|---|
| arbitration-agreement | 59 | 97.2 | 98.9 | +1.7 | 0 / 0 | 96.0 (kept base tree) | −1.1 | 0 / 0 |
| procedural-order (demo) | 55 | 60.6 | 72.1 | **+11.5** | 13 / 2 | 42.4 | **−18.2** | 1 / 6 |
| interim-order | 37 | 71.2 | 98.2 ⚠ | +27.0 | 10 / 0 | 74.8 | +3.6 | 2 / 0 |
| agreement-issues | 40 | 73.3 | 71.7 | −1.7 | 3 / 2 | 72.5 | −0.8 | 2 / 3 |
| **mean** | | **75.6** | 85.2 | **+9.6** (+3.8 without ⚠) | | 71.4 | **−4.1** | |

**Raw checks on the 55-check demo task**

| condition | runs (/55) | mean (/55) |
|---|---|---|
| base | 27, 30, 43 | 33.3 |
| Arm B | 40, 39, 40 | 39.7 |
| Arm A | 23, 20, 27 | 23.3 |

⚠ = instance answer key (§5).

## 4. Held-out results: Arm B harnesses on matters their improver never saw
Δ pts vs base, R=3 per cell.

| harness adopted on ↓ / scored on → | arbitration-agreement | procedural-order | interim-order | agreement-issues | row mean |
|---|---|---|---|---|---|
| arbitration-agreement | — | **+21.8** | **+26.1** | −1.7 | +15.4 |
| procedural-order | −1.7 | — | **+24.3** | +1.7 | +8.1 |
| interim-order ⚠ | +1.7 | **+22.4** | — | +5.8 | +10.0 |
| agreement-issues | −2.8 | **−15.8** | +0.9 | — | −5.9 |

**Mean held-out Δ: +6.9 pts over 12 cells (+5.9 without the ⚠ row).**

**By kind of transfer**

| from → to | cells | mean Δ |
|---|---|---|
| redline → redline | 6 | +15.8 (+24.2 on the two tasks with headroom; arbitration-agreement is at ceiling) |
| redline → memo | 3 | +1.9 |
| memo → redline | 3 | −5.9 |

**On the 55-check demo task**
- Base: 33.3 /55.
- With harnesses adopted on other redline tasks: 45.3 /55 (from arbitration-agreement) and 45.7 /55 (from interim-order). That is higher than Arm B's in-task 39.7 /55.

**What transfers**
- A redline method transfers: a tracked-changes builder skill (`redline-docx`), plus the rule that each objection goes in the body as an inline note.
- That rule reflects a reader fact the improver inferred from deliverables shown through the judge's reader. In the adopted harness's words: the reader "shows body text only: tracked insertions appear; deleted text and Word comment balloons do not".
- harness2 shows the improver deliverables through the judge's reader by design, so this is legitimate. But much of the LAB gain on redline tasks is format alignment with pandoc-accept rather than better legal analysis.
- A memo-task harness carries the wrong format to redline tasks and loses checks.

## 5. Instance leak: the improver wrote answer keys without seeing the rubric
- **Arm B (layer 1 only).** The interim-order harness has a 12.6 KB skill, `interim-measures-order-review`. It holds this matter's facts:
  - parties (NIS, KEH, Grupo Andino);
  - the arithmetic (54,000 MT × 879.63; 65.0 − 47.5 = 17.5m);
  - paragraph pinpoints;
  - "pinpoints below were verified in the workspace record";
  - verbatim text of clause 14.4.

  Two audits agree: the literal audit counts 24 own-matter literals, and layer 2 post-hoc flags datum, entity and verbatim hits. No other adopted harness in either arm is flagged.
- **Arm A (layer 2 live).** On interim-order the Haiku improver also proposed an answer key:
  - numbers 22,800, 31,200, 54,000, 879.63;
  - Bogotá, Calle Carrera, Moorgate (counsel addresses);
  - clause 14.4 verbatim.

  The guard rejected it, and the adopted tree is a clean 2.4 KB.
- **How much the leak was worth.** Little. Interim-order gains as much from clean harnesses adopted on other tasks (+24.3, +26.1) as in-task from its own answer key (+27.0). The answer key appears to have been a costly but redundant shortcut on top of the transferable redline method.
- **Implication for the paper's protocol.** harness2's LAB `validate_tree` checks only environment invariants. Given the data room, both a strong and a weak improver write instance answer keys. In-task LAB numbers therefore need an instance guard or a held-out check before they can be read as reusable-harness gains.

## 6. Comparison with the published LAB numbers
| | published / brief | here |
|---|---|---|
| single-step gain, LAB partial pass rate | up to +11.8 pp (harness2 README; Gemini 3.5 Flash / GLM-5) | Arm B in-task +9.6 (+3.8 without the leaky cell); held-out +6.9; Arm A in-task −4.1 |
| average per round | about +2 pts (brief; not in this checkout) | one round only |
| best case | 44 → 94 (brief) | 71.2 → 98.2 in-task (leak-flagged); 71.2 → 97.3 held-out (clean harness from another task) |
| demo task, 55 checks | Gemini 3.5 Flash 20/55 → 22/55, +2 (brief) | Haiku 5.5 base 33.3/55. Arm B +6.4 checks in-task, +12 held-out; Arm A −10 checks |

**Reading.**
- The rig reproduces LAB's scale. The base on the demo task is 24–43 /55, against 20/55 for Gemini 3.5 Flash.
- **With a stronger improver,** the Harness² effect sits in the paper's range: +9.6 in-task against up to +11.8.
- **The +6.9 held-out survives the rubric and instance controls,** but it is concentrated in redline-to-redline transfer and is substantially format alignment with the judge's reader.
- **Self-improvement by the same small model** (Haiku improving Haiku) does not help on average (−4.1). It badly damaged the hardest task, where a single run of the public Gemini 3.5 Flash demo moved only +2.
- **Caveats:** n=3 per cell, 4 tasks, one practice area, one round, and one judge model (Sonnet 5.5, not LAB's Vertex judge). Base variance on the demo task is ±8 checks.

## 7. Plumbing incidents (none scored)
- **Judge v1 discarded whole runs on any failed criterion call.**
  - 7 base runs were judged twice. Their logged judge cost is mostly cache reads, and about $18 of discarded calls is not itemised.
  - Fixed with a per-criterion verdict cache, backoff, and judge calls under the rig-wide 4-slot cap.
- **CLI OAuth refresh race, then expiry.** The CLI's OAuth refresh raced under about 15 concurrent CLIs, then the session expired at about 15:00. Effects:
  - Arm A task 1: the `dom1` probe rollout failed with "Not logged in"; task 1 kept base.
  - Arm A tasks 3–4: the "Failed to authenticate" replies were not yet classified as infra, so harness2 recorded them as agent failures. Those cells were voided (`summary.json.authfail`) and re-run after the 18:24 re-login, with fresh processes (current sandbox profile with `.git` denied, auth classifier, layer-2 guard, 4-process cap).
  - No auth-failed rollout was ever scored. Verified over all `meta.json` files.
- **Executor `pip install` attempts** (16) were blocked by the sandbox.

## 8. Cost (USD, from `total_cost_usd` of every `claude -p` call)
| per task | executor $/rollout | judge $/run (uncached) | $/judged rollout |
|---|---|---|---|
| arbitration-agreement | 0.22 | 2.55 | 2.77 |
| procedural-order | 0.37 | 3.12 | 3.48 |
| interim-order | 0.43 | 1.96 | 2.40 |
| agreement-issues | 0.17 | 2.87 | 3.04 |

| block | $ |
|---|---|
| base eval (12 judged rollouts) | 14.83 (logged; partly cache reads) |
| Arm B: improvement rollouts 5.78 + improver 6.05 + in-task eval 45.36 | 57.19 |
| Arm B held-out matrix (36 judged rollouts) | 96.32 |
| Arm A: improvement rollouts 5.25 + improver 4.13 + in-task eval 33.66 | 43.04 |
| pilot | 3.26 |
| **logged total** | **214.64** (about 233 with the unitemised discarded judge calls) |
| since the 18:23 approval (~$144): held-out 96.32 + finishing Arm A about 30 | **about 126** |

**Cost drivers**
- The judge is about 85% of spend. One Sonnet call per criterion over 20–110 KB deliverables costs 6–17× the Haiku rollout it grades.
- Harness² improvement for 4 tasks cost $12 with Sonnet and $9 with Haiku.

## 9. Reproduce
```
cd hpb
../repo/.venv/bin/python lab.py selfcheck
../repo/.venv/bin/python lab.py base --reps 3
../repo/.venv/bin/python lab.py h2 --k 1                                   # Arm A
LAB_IMPROVER=claude-sonnet-5-5 ../repo/.venv/bin/python lab.py h2 --k 1 --root ../experiments/lab-sonnet-imp
../repo/.venv/bin/python lab.py adopted --reps 3 [--root ...]
../repo/.venv/bin/python lab.py transfer --root ../experiments/lab-sonnet-imp --src <task> --reps 3
../repo/.venv/bin/python lab.py audit [--root ...]; ../repo/.venv/bin/python lab.py report [--root ...]
```
- Logs: `experiments/logs/lab-*.log`.
- Arm B reuses the base rows through the symlink `lab-sonnet-imp/eval/base`.
- Per-harness audits: `experiments/{lab,lab-sonnet-imp}/instance_audit.json`.

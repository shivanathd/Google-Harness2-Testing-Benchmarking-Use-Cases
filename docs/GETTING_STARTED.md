# Getting started

Run the Harness² field test yourself: re-check our numbers for free, or run the full loop on your own machine.

## What you need

| | Required for | Notes |
|---|---|---|
| macOS | everything | Every agent runs inside `sandbox-exec`, which is macOS-only. |
| `git`, [`uv`](https://docs.astral.sh/uv/) | everything | `brew install uv` |
| [Claude Code](https://docs.claude.com/en/docs/claude-code) logged in | any run that calls a model | `claude auth login`, then `claude auth status` shows `"loggedIn": true` |
| [Ollama](https://ollama.com) + about 6 GB disk | the weak local agent (ADK + qwen3:8b) | `brew install ollama` |
| Apple-silicon GPU memory | ADK arm at 8 parallel slots | Lower `HPB_ADK_SLOTS` on smaller machines |

No Google Cloud project is needed. Harness²'s own benchmarks need Vertex Gemini; this rig doesn't.

## 1. Set up (5 minutes, no cost)

```bash
git clone <this repo> harness2-field-test && cd harness2-field-test
scripts/setup.sh                 # Claude Code arm
scripts/setup.sh --with-adk      # optional: Google ADK + local qwen3:8b
scripts/setup.sh --with-lab      # optional: Google's LAB legal tasks
```

The script:
- checks out Harness² at the exact commit we tested (`1cfe254`) into `repo/`;
- creates its virtualenv;
- optionally fetches LAB at the commit Harness² pins;
- runs three self-checks that make no model calls: the graders score every task about 0 untouched and 1.0 on the reference solution, the leak detector catches the known leaks, and the adoption guard rejects a leaky harness.

## 2. Re-check our numbers (free)

Every rollout and every adopted harness is committed under `experiments/`, so the statistics rebuild offline:

```bash
cd hpb
../repo/.venv/bin/python eval.py adk report                                    # study 1, weak local agent
../repo/.venv/bin/python eval.py cc report                                     # study 1, Claude Code
../repo/.venv/bin/python eval.py adk report --root ../experiments/adk-guard    # study 2, leak guard on
../repo/.venv/bin/python ablations.py                  # ablations -> experiments/ablations/RESULTS.md
../repo/.venv/bin/python build_v3.py                   # the consolidated report -> report/v3.html
```

## 3. Run it yourself

Run every command from `hpb/`. Always pass a fresh `--root`, so your runs don't mix with ours: rollouts are cached by harness fingerprint, and a reused root replays our cache.

```bash
cd hpb
PY=../repo/.venv/bin/python

# a. Smoke test: one sandboxed rollout plus one improver session (a few cents)
$PY smoke.py cc

# b. Harness² on the 9 tasks: parallel k=1, Sonnet improver, Haiku executor
HPB_LEAKGUARD=2 HPB_CC_MAX_TURNS=4 $PY run.py cc --mode parallel --k 1 --root ../experiments/mine-cc

# c. Fresh re-rolls of the base and the adopted harnesses, then the statistics
HPB_CC_MAX_TURNS=4 $PY eval.py cc base --reps 4 --root ../experiments/mine-cc
HPB_CC_MAX_TURNS=4 $PY eval.py cc h2 --run parallel-k1 --reps 4 --root ../experiments/mine-cc
$PY eval.py cc report --root ../experiments/mine-cc
```

- **`HPB_CC_MAX_TURNS=4`:** full-strength Claude Code already passes every task, which leaves Harness² nothing to improve. Capping it at 4 turns creates headroom.
- **Weak local agent:** swap `cc` for `adk` after `ollama serve` is running.
- **Sequential mode:** `--mode sequential --k 2`.
- **Autoresearch baseline** (the grader stays in the loop): `autoresearch.py cc`.

### What it costs

These are the improver figures we logged (Claude Sonnet 5.5 unless noted). Executor rollouts on Haiku or a local model add a little on top.

| Run | Improver spend we logged |
|---|---|
| Harness² on 9 tasks, Claude Code | $2–3 |
| Harness² on 9 tasks, ADK, leak guard on | about $6 |
| Haiku as its own improver, 9 tasks | about $0.50 |
| LAB legal tasks | about $1.50 per task to improve, plus $2.40–3.50 per judged rollout |

### Knobs

| Variable | Default | What it does |
|---|---|---|
| `HPB_IMPROVER` | `claude-sonnet-5-5` | Model that proposes and composes harness edits; set `claude-haiku-5-5` for self-improvement |
| `HPB_CC_MAX_TURNS` | `40` | Turn cap for the Claude Code executor |
| `HPB_LEAKGUARD` | unset | `2` adds the stricter leak detector at adoption (recommended) |
| `HPB_CLAUDE_SLOTS` | `4` | Parallel `claude` processes; keep it low on a busy machine |
| `HPB_ADK_SLOTS` | `8` | Parallel local-model rollouts |

## 4. Bring your own agent or task

- **A task:** add a generator to `hpb/bench.py` (easy) or `hpb/tiers.py` (medium and hard). It returns the workspace files, the expected values and the prompt. Grading code stays in `hpb/`, which the sandbox hides from every agent. Add a fresh-seed variant (`<id>-v`), so you can score on data the improver never saw.
- **An agent:** implement `execute()` and `trajectory()` in `hpb/adapters.py`, the way the `cc` and `adk` executors do. Harness²'s core stays unmodified; the adapter is the only seam.
- **Claude Code users:** the adopted harness maps directly onto Claude Code:

  | Harness² writes | Claude Code uses |
  |---|---|
  | `systemprompt.md` | `CLAUDE.md` |
  | `skills/` | `.claude/skills/` |
  | `scripts/` | scripts the agent runs |
  | `hooks.json` | `.claude/settings.json` hooks |

  See "Applying it to Claude Code" in the report.

## Before you trust a gain

1. **Score on data the improver never saw:** fresh-seed variants, or held-out tasks. In-task numbers are test-time adaptation.
2. **Grep the adopted harness for the task's own answers.** Our unguarded improver wrote them into 6 of 8 harnesses. `leakguard.py audit <harness dirs>` does this check.
3. **Run an A/A check** (base against base) once per arm. In our runs a login glitch faked a +0.11 gain.
4. **Write the analysis plan before the first treatment run,** and record every change with its time (`experiments/PREREG.md`).

## Troubleshooting

| Symptom | Fix |
|---|---|
| Rollouts end at once with "Not logged in" or "OAuth session expired" | Run `claude auth login`. The rig retries these failures as infrastructure and never scores them. |
| Everything is slow, hooks time out | Check `uptime`. Lower `HPB_CLAUDE_SLOTS` and `HPB_ADK_SLOTS`, and quit heavy apps (a VM, for example). |
| ADK rollouts fail to connect | Start `ollama serve` and check `ollama list` shows `qwen3:8b`. |
| `Operation not permitted` in an agent log | The sandbox is working: an agent tried to read something outside its workspace. |
| "no candidate produced an artifact" | A legitimate outcome: nothing was adopted for that task. Evaluation reports it as intent-to-treat. |

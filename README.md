# Harness² on the Bench

An independent field test of Google Research's [Harness²](https://github.com/google-research/harness2)
("recursive agent harnessing"). Its claim is that an agent can improve itself job after job,
without changing the model, by rewriting the harness around it: system prompt, guardrails,
memory, tool guidance, skills, scripts, subagents and plugins.

We ran Harness² unmodified, on a benchmark we built with hidden graders, with Claude Code and a
small local model as the agents, and measured what held up.

**Short answer:** Harness² is real but narrow.
- It turns a weak agent's repeated failures into correct runs, and those gains hold on data the improver never saw.
- It does nothing for an agent already at ceiling, and correctly leaves that agent alone.
- Its gains don't carry to harder tasks. The lesson library and the probe step mattered little.
- A model improving itself does about half as well as a stronger improver.
- Unguarded, it writes the answers straight into the harness.

→ **[Getting started](docs/GETTING_STARTED.md)**: re-check our numbers for free, or run it yourself.
→ **[Full report](report/index.html)**: download it and open it in a browser for charts, check flips and the decision lineage.

## How we built the test

![How we tested Harness²: method and mental model](docs/diagrams/method.svg)

The mental model behind every decision:

- **The harness is everything around a fixed model.** The improver edits the harness, the executor runs it, and the grader stays hidden from both, in code the sandbox never shows to any agent.
- **Score on data the improver never saw.** Each task has a fresh-seed variant, and the legal tasks have held-out matters. A gain on the task the harness was tuned on counts only as test-time adaptation.
- **Assume a result is wrong until it is checked.**
  - The analysis plan was written before any treatment run, and every later change is a dated amendment ([PREREG.md](experiments/PREREG.md)).
  - Adversarial and security reviews ran before any treatment run and caught a silent blocker and 7 grader or spec bugs.
  - A/A checks exposed a fake +0.11 gain caused by a login glitch.
  - Leak audits found the improver writing answers into its skills.
- **Isolate every agent.** Every model process runs under macOS `sandbox-exec` with an allow-listed environment: no tokens, no access to the graders, other runs or `.git`, and writes only inside its own workspace.

## What Harness² does

![The Harness² per-task loop](docs/diagrams/harness2-loop.svg)

For each task, Harness² works in five steps:
1. **Propose:** draft two kinds of harness edits, about working in general and about domain knowledge.
2. **Probe:** try each edit on the same task.
3. **Compose:** build a refined harness from what helped.
4. **Adopt:** keep the result.
5. **Reflect:** write a lesson into a per-domain library that later tasks read.

## The rig

![The test rig: benchmark, adapters, sandbox, executors and improver](docs/diagrams/test-rig.svg)

- **Benchmark (HPB):** 9 tasks across data reconciliation, log analytics and issue fixing, at easy, medium and hard, plus 6 fresh-seed variants. Programmatic graders live only in `hpb/`.
- **Google LAB:** 4 arbitration tasks from [harvey-labs](https://github.com/harveyai/harvey-labs), the legal benchmark Harness² ships with. Each task has 37–59 rubric checks, scored by a Claude rubric judge.
- **Executors:**
  - Claude Code (`claude -p`, Haiku 5.5): full strength, and capped at 4 turns to create headroom.
  - A Google ADK agent on local qwen3:8b through Ollama.
- **Improvers:** Claude Sonnet 5.5, or Haiku improving itself.
- **Baseline:** Karpathy-style autoresearch, which keeps an edit only when the real grader score rises.

## Results

Δ is the mean change in the fraction of grader checks passed, against the base harness, with a 95% hierarchical-bootstrap interval.

| Question | Result | Δ (95% CI) |
|---|---|---|
| Weak agent, guarded, on data the improver never saw | Large, consistent gain (6 of 6 tasks up) | **+0.97** (+0.89 to +1.00) |
| Claude Code capped at 4 turns, Sonnet improving Haiku | Clear gain (8 up, 0 down) | **+0.42** (+0.17 to +0.69) |
| Full-strength Claude Code | Already at ceiling; Harness² kept the base harness | +0.00 |
| Haiku improving its own harness | About half the Sonnet gain; one task regressed | +0.17 (−0.08 to +0.42) |
| Harness from an easy task, reused on medium/hard | No transfer | −0.03 (−0.11 to +0.04) |
| Lesson library off minus on | Small cost, all on one task | −0.13 (−0.39 to +0.01) |
| No probe minus probe | No difference; the paper's claim did not reproduce here | −0.00 (−0.11 to +0.10) |
| Unguarded improver | Wrote the task's own answers into 6 of 8 harnesses; 0 of 9 with the guard | — |
| Google LAB, Sonnet harnesses on unseen legal matters | Small and not significant; mostly deliverable format | +0.07 (−0.01 to +0.16) |
| Google LAB, Haiku improving itself | Got worse; the 55-check task fell from 33.3 to 23.3 | −0.04 (−0.15 to +0.03) |

These numbers support descriptive claims only: each comparison covers 4 to 9 tasks with 3–4 re-rolls. The full scoreboard of 20 comparisons is in the [report](report/index.html). Each study's own write-up:
- [study 2: the leak guard](experiments/leak-guard-results.md)
- [the ablations](experiments/ablations/RESULTS.md)
- [the LAB legal tasks](experiments/lab/RESULTS.md)

## Applying it to Claude Code

The edits Harness² adopted map directly onto Claude Code:

| Harness² writes | Claude Code uses |
|---|---|
| `systemprompt.md` | `CLAUDE.md` |
| `skills/` | `.claude/skills/` |
| `scripts/` | scripts the agent runs |
| `hooks.json` | `.claude/settings.json` hooks |

The edits that held up on fresh data were concrete:
- a domain skill with a tested script;
- "write the deliverable early";
- "never re-run a command that just failed".

Use it where an agent fails the same kind of job repeatedly. Always grep the result for answers to the job it was tuned on.

## Repository layout

| Path | What |
|---|---|
| `hpb/` | Benchmark and graders (`bench.py`, `tiers.py`), adapters and sandbox (`adapters.py`), ADK agent, Harness² and autoresearch drivers, evaluation and stats, leak guard, report builders |
| `experiments/` | Every run: adopted harnesses, rollout summaries, evaluation rows, per-study results, and `PREREG.md` |
| `report/` | The consolidated report (`index.html`), its data and the decision lineage (`lineage.json`) |
| `docs/` | [Getting started](docs/GETTING_STARTED.md) and the diagrams |
| `.archify/` | Diagram sources ([Archify](https://github.com/tt-a1i/archify) JSON plus interactive HTML) |
| `scripts/setup.sh` | One-command setup and self-checks |

## Credits and licences

- [Harness²](https://github.com/google-research/harness2) (Apache-2.0) is fetched at commit `1cfe254` by `scripts/setup.sh`. It isn't vendored here, and its core was used unmodified.
- LAB tasks come from [harveyai/harvey-labs](https://github.com/harveyai/harvey-labs) (MIT). The case documents in its tasks are fictional; agent outputs on them appear under `experiments/lab*`.
- This repository is released under the MIT licence ([LICENSE](LICENSE)).
- This is independent research, not affiliated with Google, Harvey or Anthropic.

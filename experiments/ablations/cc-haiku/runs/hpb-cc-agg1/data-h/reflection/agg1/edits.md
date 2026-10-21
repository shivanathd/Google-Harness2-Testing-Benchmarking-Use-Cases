component: plugin/README.md (the `plugin/` directory)
candidates: agg1, dom1, inv1 (all three pool harnesses carry it identically; decisions/inv1.md and decisions/dom1.md record that they authored no edit, so it came from the shared starting tree, not from a candidate)
change: Added a `plugin/` directory containing one README that is only an HTML comment. It states that OpenCode plugins are not run by this rig and suggests enforcing in-loop behaviour with a root `hooks.json` using a Stop hook that runs a `scripts/` check (exit 2 blocks finishing, at most 3 times). No executable code. Absent from base_harness/.
observed: No trajectory (base1, inv1, dom1, agg1) created `hooks.json`, referenced `plugin/`, or hit a finish-time check. Each run wrote output/answer.json on its first Write and none exited early, so the Stop-hook path never had a chance to fire. All four deliverables are identical, so there is no divergence to attribute. The mechanism is untested rather than shown inert.
verdict: no observed effect

component: scripts/README.md (the `scripts/` directory)
candidates: agg1, dom1, inv1 (same provenance as plugin/)
change: Added a `scripts/` directory containing one comment-only README describing deterministic helpers run as `python3 scripts/<name>.py`. No helper scripts were added.
observed: No trajectory ran or mentioned `scripts/`. Every run computed the figure with its own inline Python: base1 wrote /tmp/calc_rev.py, inv1 and dom1 used `python3 -I -` heredocs, agg1 used `python3 -I -c`. That behaviour is the same across runs and is not tied to the README. All four outputs match.
verdict: no observed effect

component: skills/README.md (the `skills/` directory)
candidates: agg1, dom1, inv1 (same provenance as plugin/)
change: Added a `skills/` directory containing one comment-only README describing skills as `skills/<name>/SKILL.md`. No SKILL.md was added.
observed: No trajectory invoked the skill tool or read `skills/`. Outputs are identical across all four runs, with no divergence in any trajectory.
verdict: no observed effect

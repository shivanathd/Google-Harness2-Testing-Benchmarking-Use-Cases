KEEP_BASE. I changed no files in `context/harness/`.

- **Inventory.** I read `task.md` and the current harness. The harness is still the near-empty original: a one-line system prompt, with the memory, guardrails and tool guidance files empty. I also read the earlier decisions and the base1, base2, dom1, c1 and inv1 outputs. Every run wrote `{"net_usd": 18691.64, "transactions": 21}`.
- **What I did not do.** I did not reopen the full trajectories, so I did not look for tool errors or inefficiencies myself. I relied on the earlier decision notes, which describe the same single-pass method in both base runs, with no divergence and no blind retries. The one error they report, a harmless `ls: ..: Operation not permitted`, was ignored without any loss. The earlier notes also report an independent recompute giving 18691.63681, which rounds to 18691.64 over 21 transactions. I did not repeat that recompute.
- **Why no change.** I can't point to a moment in any trajectory where a prose rule, skill, script or plugin would have changed what the agent did. The agent already did these things on its own:
  - deduplicated 42 rows to 36 unique txn_ids;
  - parsed both date formats and parenthesised amounts;
  - excluded the 2026-10-26 SETTLED row;
  - converted with `usd_per_unit` and rounded once at the end;
  - wrote `output/answer.json` in the requested shape.
- **dom1's `revenue-reconciliation` skill.** Its rollout loaded the skill first and then produced the same answer, so the skill changed nothing observable. It would add an always-on trigger line and extra loaded context, and it embeds one task-specific fact (42 rows, 36 unique) that doesn't generalize. Adding it would be speculation.
- **Risks I considered but did not act on.** These are conflicting duplicate txn_ids, an unfamiliar status spelling, and a missing FX rate. None showed up in any rollout. A later round can add a skill if a rollout actually fails on one of them.
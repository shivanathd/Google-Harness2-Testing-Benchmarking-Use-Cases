Both rollouts reached the same answer: `{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}`. I recomputed it independently and it matches. So no rule in the current harness needs correcting, and the change below is small and on-demand.

- **New skill `skills/revenue-reconciliation/SKILL.md`, with a trigger line added to `systemprompt.md`.**
  - **Motivating moment:** in base1, the first script subtracted `usd - 15`, which adds the fee back. It printed 5162.12 and only caught the error on a re-read, then fixed it to `usd + 15` and got 5072.12. base2 got the sign right first time. That is the one divergence between the runs.
  - **What the skill encodes:**
    - convert every timestamp with its offset to UTC before taking the month;
    - drop test customers from both revenue and chargebacks;
    - treat JPY as already in whole units;
    - deduct each chargeback as the full charge plus the fee;
    - count a chargeback in its own booking month, even if the charge came from another month;
    - count `transactions` even when the charge was later charged back.
  - **Pre-write checklist:** list the recognised charge IDs and booked chargeback IDs, give each exclusion a named reason, check the UTC month-boundary charges, recompute net as gross minus reversals minus fee × count, and confirm the output keys and number formats.
  - **Workspace facts:** I recorded only the file set, the currencies, the test-customer behaviour and the fee-sign slip, labelled as this task's data. I left the final figure out of the skill.
- **Not changed:** the guardrails, memory and tool guidance. The runs show no evidence that a change there would alter behaviour.
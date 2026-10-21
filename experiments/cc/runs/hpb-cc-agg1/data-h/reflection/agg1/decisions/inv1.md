KEEP_BASE. I changed no files.

The one rollout, `base1`, did the work correctly and without wasted steps:
- It read POLICY.md and all four CSVs, then computed the result with a Decimal script instead of by hand.
- It converted timestamps to UTC and applied the test-customer exclusion to chargebacks as well as charges.
- It booked chargebacks by the UTC month of `chargeback_at`, counting chargebacks on charges made in earlier months (ch_000).
- It wrote `output/answer.json` and reopened it with a JSON parse to check it.

I checked its result against the source data. Nine charges are captured in September UTC and belong to non-test customers. ch_028 and ch_022 fall in August UTC. ch_015 and ch_026 fall in October UTC. The three September chargebacks (cb_0, cb_2, cb_6) are the right ones. cb_5 is dropped because its customer is a test account. The answer is `{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}`, which matches the task's output shape.

There was no tool error, no repeated failure and no skipped step, and there is only one run, so there is no divergence to learn from. Any addition would be speculative:
- **Skill or script:** a skill or script would cover a procedure the agent already handled on its own.
- **Always-on prose:** extra prose would only use up context.
- **Plugin:** a plugin is not warranted, because the deliverable was written and verified.
- **Workspace facts:** I did not add facts such as the fx rates or the test-customer IDs. They are specific to this dataset, and the agent reads them from the files in seconds.
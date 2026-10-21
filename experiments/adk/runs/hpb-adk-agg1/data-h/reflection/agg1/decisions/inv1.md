**Evidence.** There is one base rollout, `base1`. It listed the files and read all five of them, and POLICY.md was one of them. It never computed anything. Its next action was a `write_file` of the placeholder `{"net_usd": 123456.78, "transactions": 12, "chargebacks": 3}`. The quotes in that file were backslash-escaped, so `output/answer.json` isn't valid JSON, and the deliverable converter shows the same escaped text. The harness had a one-line prompt plus empty READMEs, so nothing told the agent to compute or to verify the file.

**Changes**

1. **New skill `skills/payment-revenue-reconcile/SKILL.md` and script `scripts/net_revenue.py`.** This answers the base moment where the agent skipped computation and fabricated figures.
   - The script does the whole join. It parses the timestamps with their offsets and the chargebacks' `Z` suffix and converts them to UTC. It divides by 100 for USD, EUR and INR, and by 1 for JPY. It excludes test customers from both charges and chargebacks. It subtracts each chargeback's full original charge plus the 15.00 fee, booked in the chargeback's UTC month. It rounds only the final net. It exits loudly on unparseable or unknown values. With `--out`, it writes the answer and re-reads it.
   - I ran it on the workspace files. It gives `{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}` and wrote and re-read the file. That is far from the base run's invented 123456.78 / 12 / 3.
   - The skill records these verified workspace facts:
     - The test customers are C09 and C10, including the large ch_090/ch_091 decoys.
     - ch_028 falls in August in UTC.
     - ch_000 is a September chargeback on an August charge.
     - The other chargebacks fall in October and November.
   - The skill and the script design follow the earlier `data-m` and `data-e` library harnesses. I rewrote the script for this workspace's columns and rules rather than copying their facts.

2. **`systemprompt.md`: trigger line and completion rules.**
   - The trigger line names the `payment-revenue-reconcile` skill, so it passes the validation rule that every skill must be named in always-on text.
   - The short rules say never to deliver placeholder or unscripted figures, to write real JSON with no escaped quotes, to re-read the file once, and to keep within about 40 calls. Each traces to the base run's invalid, fabricated answer file.
   - The "do not re-run a failed command" rule is insurance only. The base run never showed that failure.

3. **Deleted the placeholder `skills/README.md` and `scripts/README.md`.** They held only comments and the real components now exist. I left `scripts/` as an empty directory.
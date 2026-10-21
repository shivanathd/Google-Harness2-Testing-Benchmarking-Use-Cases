**What the trajectory showed (base1):**
- The agent read all five source files, then wrote `output/answer.json` as `{\"net_usd\": 123456.78, \"transactions\": 12, \"chargebacks\": 3}` with no calculation in between.
- The values are a placeholder. My recomputation under POLICY.md gives net 5072.12, 9 transactions and 3 chargebacks.
- The quotes were backslash-escaped, so the file is not valid JSON and the reader cannot parse it.
- The agent only had `list_files`, `read_file` and `write_file`, with no shell. It never checked its work or read the file back.

**Changes:**
1. **`systemprompt.md`: working-method section (about 5 bullets).** It targets the three failures above:
   - Derive every number from the rows; guessed values count as a failed run.
   - With no shell, tally by hand, one line per row, converting each timestamp to UTC before assigning a month.
   - Write raw JSON with no escapes, then read the file back to confirm it parses.
   - Apply the test-customer and non-captured exclusions to both the charge list and the chargeback list.
   - It names no figures and adds no policy facts.
2. **`scripts/check_output.py` and `hooks.json`: Stop hook.**
   - It recomputes the figure from the CSVs using this workspace's POLICY.md and checks that `answer.json` exists, parses as plain JSON, has the three numeric keys, and matches the recomputation.
   - On a mismatch it exits 2 with a per-row breakdown, so the agent can reconcile and rewrite. That blocks finishing at most 3 times.
   - If the inputs aren't in the expected shape, it lets the run finish rather than blocking it.
   - `--show` prints the breakdown without blocking.
   - I ran it in a scratch copy against the real CSVs. It flagged the escaped-quote file from base1 with exit 2, and `--show` printed net 5072.12, 9 transactions, 3 chargebacks.
   - I hand-checked the boundary cases:
     - `ch_028` (C04, 2026-09-01 03:49+05:30) falls on 31 August UTC, so it is excluded.
     - `ch_000` was charged in August but its chargeback is in September, so it is reversed in September.
     - `ch_022` belongs to test customer C09, so it is excluded.

No skills or other plugins were added; the evidence didn't call for them.
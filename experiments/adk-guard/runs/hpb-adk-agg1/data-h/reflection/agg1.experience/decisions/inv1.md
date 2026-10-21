**Evidence:** There is one rollout, base1. It listed the workspace and read all five files, including POLICY.md. Its next call was `write_file output/answer.json` with `{\"net_usd\": 123456.78, \"transactions\": 12, \"chargebacks\": 3}`. That content is a made-up placeholder with no computation behind it. The backslash-escaped quotes also make the file invalid JSON. The agent never computed anything, never reopened the file, and then ended its turn.

The rollout only shows `list_files`, `read_file` and `write_file` calls. I can't tell whether a shell was available, so I wrote the fallback for both cases.

**Changes**
1. **`systemprompt.md`** (always-on, short). This rewrites the generic one-liner. It follows the placeholder write and the escaped-quote file in base1.
   - It forbids placeholder values and requires computing from the source files before writing.
   - It tells the agent to write JSON with plain quotes and then reopen the file to check it parses.
   - It points to the helper script, and gives a by-hand fallback if commands can't be run.
   - It carries workspace facts I checked against the data:
     - Convert timestamps to UTC before taking the month. For example, ch_028 at `2026-09-01T03:49+05:30` is 2026-08-31 in UTC.
     - Drop test customers from both charges and chargebacks. C09 and C10 are the test customers here, and ch_090 and ch_091 are large test charges.
     - JPY amounts are whole yen.
     - A chargeback can reverse a charge made in any month. cb_2 reverses ch_000, which was captured on 2026-08-31 UTC.
     - Count "transactions" before removing charged-back charges.
2. **`scripts/net_revenue.py`** (new). This replaces the hand arithmetic across 47 charges with mixed time zones and four currencies.
   - It is stdlib-only and takes `--month`. It uses Decimal, converts timestamps to UTC and rounds once.
   - It drops test customers from charges and chargebacks. It books the reversal and the 15.00 fee in the UTC month of `chargeback_at`.
   - It writes the three-key JSON and prints diagnostics on stderr. The diagnostics cover test rows dropped, charges whose month moved when converted to UTC, and chargebacks on charges that weren't captured.
   - I ran it on the source files and got `{"net_usd": 5072.12, "transactions": 9, "chargebacks": 3}`. I counted the transactions and chargebacks by hand and they match. I did not hand-check the net figure.
3. **`hooks.json` and `scripts/check_output.py`** (new Stop hook). It blocks finishing if `output/answer.json` is missing, isn't valid JSON, has the wrong types, or has a net figure with more than 2 decimals. base1 would have been stopped by this: it wrote an invalid-JSON placeholder and ended its turn. The hook accepts any valid computed file, so it doesn't block correct completion.

No skill was added, because nothing in the evidence calls for one. The README stubs and the other files are unchanged.
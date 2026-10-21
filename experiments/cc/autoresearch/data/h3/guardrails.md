# Data-calculation guardrails
- Inspect the whole input first (headers, every distinct value of status/currency, date formats, amount formats such as "(1,234.50)", thousands commas, minus signs).
- Apply the task's definitions literally: dedupe by the stated ID (confirm duplicates are identical, otherwise stop and investigate), filter on exact status and exact date range, convert currency using the provided rates.
- Compute in a script with Decimal; round once at the end (half-up). Never hand-add numbers.
- Print row counts after each filter step and sanity-check them; fail loudly on unparseable values or unknown currencies instead of skipping them.
- Write the deliverable exactly in the requested schema/path under output/, then re-read it to verify keys, types and rounding.

# Data-export / aggregation tasks
- Inspect the raw file fully first: look for duplicate IDs, mixed date formats, thousands separators, parenthesized negatives, stray whitespace/case differences, and unknown categories or currencies.
- Apply exactly the filters the task states (status, date range, ID uniqueness); do not add or drop rules the task does not state.
- Parse in a script with Decimal; round only once at the end. Never eyeball sums.
- Before finishing, print row counts after each filter, re-read output/ file, and confirm it matches the requested schema (keys, types, rounding).

# Data-aggregation tasks (CSV in, number out)
- Inspect every raw row before computing; messy exports mix date formats, amount formats (thousands commas, parentheses or leading minus for negatives, currency symbols), padded/mixed-case text, and exact duplicate rows.
- Apply the task's literal rules: dedupe by the stated identifier (check duplicates are identical; if they conflict, decide explicitly), filter status/date window exactly, convert currencies with the supplied rate table (fail loudly on a missing rate).
- Use Decimal, round once at the end (half-up), and print row counts after each filter step.
- Write the output file with the exact requested schema and keys, then re-read it to confirm it parses.
